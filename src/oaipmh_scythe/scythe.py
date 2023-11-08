# SPDX-FileCopyrightText: 2015 Mathias Loesch
#
# SPDX-License-Identifier: BSD-3-Clause

from __future__ import annotations

import inspect
import logging
import time
from typing import TYPE_CHECKING, Iterable

import httpx

from oaipmh_scythe.iterator import BaseOAIIterator, OAIItemIterator
from oaipmh_scythe.models import Header, Identify, MetadataFormat, OAIItem, Record, Set
from oaipmh_scythe.response import OAIResponse

if TYPE_CHECKING:
    from collections.abc import Iterator

    from httpx import Response

logger = logging.getLogger(__name__)

OAI_NAMESPACE: str = "{http://www.openarchives.org/OAI/%s/}"


# Map OAI verbs to class representations
DEFAULT_CLASS_MAP = {
    "GetRecord": Record,
    "ListRecords": Record,
    "ListIdentifiers": Header,
    "ListSets": Set,
    "ListMetadataFormats": MetadataFormat,
    "Identify": Identify,
}


class Scythe:
    """Client for harvesting OAI interfaces.

    Use it like this:

        >>> scythe = Scythe("https://zenodo.org/oai2d")
        >>> records = scythe.list_records(metadataPrefix="oai_dc")
        >>> next(records)
        <Record oai:zenodo.org:4574771>

    :param endpoint: The endpoint of the OAI interface.
    :param http_method: Method used for requests (GET or POST, default: GET).
    :param protocol_version: The OAI protocol version.
    :param iterator: The type of the returned iterator
           (default: :class:`sickle.iterator.OAIItemIterator`)
    :param max_retries: Number of retry attempts if an HTTP request fails (default: 0 = request only once). Sickle will
                        use the value from the retry-after header (if present) and will wait the specified number of
                        seconds between retries.
    :param retry_status_codes: HTTP status codes to retry (default will only retry on 503)
    :param default_retry_after: default number of seconds to wait between retries in case no retry-after header is found
                                on the response (defaults to 60 seconds)
    :param class_mapping: A dictionary that maps OAI verbs to classes representing
                          OAI items. If not provided,
                          :data:`sickle.scythe.DEFAULT_CLASS_MAPPING` will be used.
    :param encoding:     Can be used to override the encoding used when decoding
                         the server response. If not specified, `requests` will
                         use the encoding returned by the server in the
                         `content-type` header. However, if the `charset`
                         information is missing, `requests` will fallback to
                         `'ISO-8859-1'`.
    :param request_args: Arguments to be passed to requests when issuing HTTP
                         requests. Useful examples are `auth=('username', 'password')`
                         for basic auth-protected endpoints or `timeout=<int>`.
                         See the `documentation of requests <http://docs.python-requests.org/en/master/api/#main-interface>`_
                         for all available parameters.
    """

    def __init__(
        self,
        endpoint: str,
        http_method: str = "GET",
        protocol_version: str = "2.0",
        iterator: type[BaseOAIIterator] = OAIItemIterator,
        max_retries: int = 0,
        retry_status_codes: Iterable[int] | None = None,
        default_retry_after: int = 60,
        class_mapping: dict[str, type[OAIItem]] | None = None,
        encoding: str | None = None,
        timeout: int = 60,
        **request_args: str,
    ):
        self.endpoint = endpoint
        if http_method not in ("GET", "POST"):
            raise ValueError("Invalid HTTP method: %s! Must be GET or POST.")
        if protocol_version not in ("2.0", "1.0"):
            raise ValueError("Invalid protocol version: %s! Must be 1.0 or 2.0.")
        self.http_method = http_method
        self.protocol_version = protocol_version
        if inspect.isclass(iterator) and issubclass(iterator, BaseOAIIterator):
            self.iterator = iterator
        else:
            raise TypeError("Argument 'iterator' must be subclass of %s" % BaseOAIIterator.__name__)
        self.max_retries = max_retries
        self.retry_status_codes = retry_status_codes or (503,)
        self.default_retry_after = default_retry_after
        self.oai_namespace: str = OAI_NAMESPACE % self.protocol_version
        self.class_mapping = class_mapping or DEFAULT_CLASS_MAP
        self.encoding = encoding
        self.timeout = timeout
        self.request_args = request_args

    def harvest(self, **kwargs: str) -> OAIResponse:
        """Make HTTP requests to the OAI server.

        :param kwargs: OAI HTTP parameters.
        """
        http_response = self._request(kwargs)
        for _ in range(self.max_retries):
            if self._is_error_code(http_response.status_code) and http_response.status_code in self.retry_status_codes:
                retry_after = self.get_retry_after(http_response)
                logger.warning("HTTP %d! Retrying after %d seconds..." % (http_response.status_code, retry_after))
                time.sleep(retry_after)
                http_response = self._request(kwargs)
        http_response.raise_for_status()
        if self.encoding:
            http_response.encoding = self.encoding
        return OAIResponse(http_response, params=kwargs)

    def _request(self, kwargs: str) -> Response:
        if self.http_method == "GET":
            return httpx.get(self.endpoint, timeout=self.timeout, params=kwargs, **self.request_args)
        return httpx.post(self.endpoint, data=kwargs, timeout=self.timeout, **self.request_args)

    def list_records(self, ignore_deleted: bool = False, **kwargs: str) -> Iterator[OAIResponse | OAIItem]:
        """Issue a ListRecords request.

        :param ignore_deleted: If set to :obj:`True`, the resulting
                              iterator will skip records flagged as deleted.
        """
        params = kwargs
        params.update({"verb": "ListRecords"})
        yield from self.iterator(self, params, ignore_deleted=ignore_deleted)

    def list_identifiers(self, ignore_deleted: bool = False, **kwargs: str) -> Iterator[OAIResponse | OAIItem]:
        """Issue a ListIdentifiers request.

        :param ignore_deleted: If set to :obj:`True`, the resulting
                              iterator will skip records flagged as deleted.
        """
        params = kwargs
        params.update({"verb": "ListIdentifiers"})
        yield from self.iterator(self, params, ignore_deleted=ignore_deleted)

    def list_sets(self, **kwargs: str) -> Iterator[OAIResponse | OAIItem]:
        """Issue a ListSets request."""
        params = kwargs
        params.update({"verb": "ListSets"})
        yield from self.iterator(self, params)

    def identify(self) -> Identify:
        """Issue an Identify request."""
        params = {"verb": "Identify"}
        return Identify(self.harvest(**params))

    def get_record(self, **kwargs: str) -> OAIResponse | Record:
        """Issue a GetRecord request."""
        params = kwargs
        params.update({"verb": "GetRecord"})
        return next(iter(self.iterator(self, params)))

    def list_metadata_formats(self, **kwargs: str) -> Iterator[OAIResponse | OAIItem]:
        """Issue a ListMetadataFormats request."""
        params = kwargs
        params.update({"verb": "ListMetadataFormats"})
        yield from self.iterator(self, params)

    def get_retry_after(self, http_response: Response) -> int:
        if http_response.status_code == 503:
            try:
                return int(http_response.headers.get("retry-after"))
            except TypeError:
                return self.default_retry_after
        return self.default_retry_after

    @staticmethod
    def _is_error_code(status_code: int) -> bool:
        return status_code >= 400
