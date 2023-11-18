# SPDX-FileCopyrightText: 2015 Mathias Loesch
# SPDX-FileCopyrightText: 2023 Heinz-Alexander Fuetterer
#
# SPDX-License-Identifier: BSD-3-Clause

"""The client module provides a client interface for interacting with OAI-PMH services.

This module defines the Scythe class, which facilitates the harvesting of records, identifiers, and sets
from OAI-PMH compliant repositories. It handles various OAI-PMH requests, manages pagination with resumption tokens,
and supports customizable error handling and retry logic.
"""

from __future__ import annotations

import inspect
import logging
import time
from typing import TYPE_CHECKING, Iterable

import httpx

from oaipmh_scythe.__about__ import __version__
from oaipmh_scythe.iterator import BaseOAIIterator, OAIItemIterator
from oaipmh_scythe.models import Header, Identify, MetadataFormat, OAIItem, Record, Set
from oaipmh_scythe.response import OAIResponse

if TYPE_CHECKING:
    from collections.abc import Iterator

logger = logging.getLogger(__name__)

USER_AGENT: str = f"oaipmh-scythe/{__version__}"
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
    """A client for interacting with OAI-PMH interfaces, facilitating the harvesting of records, identifiers, and sets.

    The Scythe class is designed to simplify the process of making OAI-PMH requests and processing the responses.
    It supports various OAI-PMH verbs and handles pagination through resumption tokens, error handling, and retry logic.

    Attributes:
        endpoint: The base URL of the OAI-PMH service.
        http_method: The HTTP method to use for requests (either 'GET' or 'POST').
        protocol_version: The version of the OAI-PMH protocol being used.
        iterator: The iterator class to be used for iterating over responses.
        max_retries: The maximum number of retries for a request in case of failures.
        retry_status_codes: The HTTP status codes on which to retry the request.
        default_retry_after: The default wait time (in seconds) between retries if no 'retry-after' header is present.
        class_mapping: A mapping from OAI verbs to classes representing OAI items.
        encoding: The character encoding for decoding responses. Defaults to the server's specified encoding.
        timeout: The timeout (in seconds) for HTTP requests.
        request_args: Additional arguments to be passed to the HTTP request.

    Examples:
        >>> scythe = Scythe("https://zenodo.org/oai2d")
        >>> records = scythe.list_records(metadataPrefix="oai_dc")
        >>> for record in records:
        >>>     print(record)

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
        self.request_args: dict[str, str] = request_args
        self._client: httpx.Client | None = None

    @property
    def client(self) -> httpx.Client:
        """Provide a reusable HTTP client instance for making requests.

        This property ensures that an `httpx.Client` instance is created and maintained for
        the lifecycle of the `Scythe` instance. It handles the creation of the client and
        ensures that a new client is created if the existing one is closed.

        Returns:
            A reusable HTTP client instance for making HTTP requests.
        """
        if self._client is None or self._client.is_closed:
            headers = {"user-agent": USER_AGENT}
            self._client = httpx.Client(headers=headers, timeout=self.timeout)
        return self._client

    def close(self) -> None:
        """Close the internal HTTP client if it exists and is open.

        This method is responsible for explicitly closing the `httpx.Client` instance used
        by the `Scythe` class. It should be called when the client is no longer needed, to
        ensure proper cleanup and release of resources.

        Note:
            It's recommended to call this method at the end of operations or when the `Scythe`
            instance is no longer in use, especially if it's not being used as a context manager.
        """
        if self._client and not self._client.is_closed:
            self._client.close()

    def harvest(self, **kwargs: str) -> OAIResponse:
        """Perform an HTTP request to the OAI server with the given parameters.

        Send an OAI-PMH request to the server using the specified parameters. Handle retry logic
        for failed requests based on the configured retry settings and response status codes.

        Args:
            **kwargs: Arbitrary keyword arguments representing OAI-PMH request parameters.

        Returns:
            An OAIResponse object encapsulating the server's response.

        Raises:
            HTTPError: If the HTTP request fails after the maximum number of retries.
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

    def _request(self, kwargs: dict[str, str]) -> httpx.Response:
        """Send an HTTP request to the OAI server using the configured HTTP method and additional request arguments.

        Args:
            kwargs: A dictionary containing the request parameters.

        Returns:
            A Response object representing the server's response to the HTTP request.
        """
        if self.http_method == "GET":
            return self.client.get(self.endpoint, params=kwargs, **self.request_args)  # type: ignore [arg-type]
        return self.client.post(self.endpoint, data=kwargs, **self.request_args)  # type: ignore [arg-type]

    def list_records(self, ignore_deleted: bool = False, **kwargs: str) -> Iterator[OAIResponse | Record]:
        """Issue a ListRecords request to the OAI server.

        Send a request to list records from the OAI server, optionally ignoring deleted records.

        Args:
            ignore_deleted: If True, skip records flagged as deleted in the response.
            **kwargs: Additional OAI-PMH request parameters.

        Yields:
            An iterator over OAIResponse or Record objects representing individual records or responses.
        """
        params = kwargs
        params.update({"verb": "ListRecords"})
        yield from self.iterator(self, params, ignore_deleted=ignore_deleted)

    def list_identifiers(self, ignore_deleted: bool = False, **kwargs: str) -> Iterator[OAIResponse | Header]:
        """Issue a ListIdentifiers request to the OAI server.

        Send a request to list identifiers from the OAI server, optionally ignoring deleted records.

        Args:
            ignore_deleted: If True, skip records flagged as deleted in the response.
            **kwargs: Additional OAI-PMH request parameters.

        Yields:
            An iterator over OAIResponse or Header objects representing individual identifiers or responses.
        """
        params = kwargs
        params.update({"verb": "ListIdentifiers"})
        yield from self.iterator(self, params, ignore_deleted=ignore_deleted)

    def list_sets(self, **kwargs: str) -> Iterator[OAIResponse | Set]:
        """Issue a ListSets request to the OAI server.

        Send a request to list sets from the OAI server.

        Args:
            **kwargs: Additional OAI-PMH request parameters.

        Yields:
            An iterator over OAIResponse or Set objects representing individual sets or responses.
        """
        params = kwargs
        params.update({"verb": "ListSets"})
        yield from self.iterator(self, params)

    def identify(self) -> Identify:
        """Issue an Identify request to the OAI server.

        Send a request to identify the OAI server and retrieve its information.

        Returns:
            An Identify object encapsulating the server's identify response.
        """
        params = {"verb": "Identify"}
        return Identify(self.harvest(**params))

    def get_record(self, **kwargs: str) -> OAIResponse | Record:
        """Issue a GetRecord request to the OAI server.

        Send a request to retrieve a specific record from the OAI server.

        Args:
            **kwargs: Additional OAI-PMH request parameters, including the record's identifier.

        Returns:
            An OAIResponse or Record object representing the requested record.
        """
        params = kwargs
        params.update({"verb": "GetRecord"})
        return next(iter(self.iterator(self, params)))

    def list_metadata_formats(self, **kwargs: str) -> Iterator[OAIResponse | MetadataFormat]:
        """Issue a ListMetadataFormats request to the OAI server.

        Send a request to list metadata formats available from the OAI server.

        Args:
            **kwargs: Additional OAI-PMH request parameters.

        Yields:
            An iterator over OAIResponse or MetadataFormat objects representing individual formats or responses.
        """
        params = kwargs
        params.update({"verb": "ListMetadataFormats"})
        yield from self.iterator(self, params)

    def get_retry_after(self, http_response: httpx.Response) -> int:
        """Determine the appropriate time to wait before retrying a request, based on the server's response.

        Check the status code of the provided HTTP response. If it's 503 (Service Unavailable),
        attempt to parse the 'retry-after' header to find the suggested wait time. If parsing fails
        or a different status code is received, use the default retry time.

        Args:
            http_response: The HTTP response received from the server.

        Returns:
            An integer representing the number of seconds to wait before retrying the request.
        """
        if http_response.status_code == 503:
            try:
                return int(http_response.headers.get("retry-after"))
            except TypeError:
                return self.default_retry_after
        return self.default_retry_after

    @staticmethod
    def _is_error_code(status_code: int) -> bool:
        """Check if the given status code represents an error.

        Determine whether the provided HTTP status code is indicative of an error condition.
        In general, any status code equal to or greater than 400 is considered an error.

        Args:
            status_code: The HTTP status code to evaluate.

        Returns:
            A boolean indicating whether the status code represents an error.
        """
        return status_code >= 400
