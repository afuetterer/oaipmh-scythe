# SPDX-FileCopyrightText: 2015 Mathias Loesch
# SPDX-FileCopyrightText: 2023 Heinz-Alexander Fütterer
#
# SPDX-License-Identifier: BSD-3-Clause

"""The client module provides a client interface for interacting with OAI-PMH services.

This module defines the Scythe class, which facilitates the harvesting of records, identifiers, and sets
from OAI-PMH compliant repositories. It handles various OAI-PMH requests, manages pagination with resumption tokens,
and supports customizable error handling and retry logic.
"""

from __future__ import annotations

import logging
import random
import sys
import time
import warnings
from typing import TYPE_CHECKING

if sys.version_info >= (3, 11):
    from typing import Self
else:
    from typing_extensions import Self
if sys.version_info >= (3, 13):
    from warnings import deprecated
else:
    from typing_extensions import deprecated

import httpx2

from oaipmh_scythe.config import HTTPConfig, RetryConfig
from oaipmh_scythe.iterator import BaseOAIIterator, OAIItemIterator
from oaipmh_scythe.models import Header, Identify, MetadataFormat, OAIItem, Record, Set
from oaipmh_scythe.response import OAIResponse
from oaipmh_scythe.utils import filter_dict_except_resumption_token, log_response, remove_none_values

if TYPE_CHECKING:
    from collections.abc import Iterable, Iterator
    from types import TracebackType

    from httpx2._types import AuthTypes

logger = logging.getLogger(__name__)

OAI_NAMESPACE: str = "{http://www.openarchives.org/OAI/2.0/}"

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
        http_config: A HTTPConfig instance controlling how HTTP requests are made.
        retry_config: A RetryConfig instance controlling the retry behavior for failed requests.
        http_method: (Deprecated, will be removed in version 0.19.0) Use `http_config.http_method` instead.
        iterator: The iterator class to be used for iterating over responses.
        max_retries: (Deprecated, will be removed in version 0.19.0) Use `retry_config.max_retries` instead.
        retry_status_codes: (Deprecated, will be removed in version 0.19.0) Use `retry_config.retry_status_codes` instead.
        default_retry_after: (Deprecated, will be removed in version 0.19.0) Use `retry_config.default_retry_after` instead.
        class_mapping: A mapping from OAI verbs to classes representing OAI items.
        encoding: (Deprecated, will be removed in version 0.19.0) Use `http_config.encoding` instead.
        auth: (Deprecated, will be removed in version 0.19.0) Use `http_config.auth` instead.
        timeout: (Deprecated, will be removed in version 0.19.0) Use `http_config.timeout` instead.

    Examples:
        >>> with Scythe("https://zenodo.org/oai2d") as scythe:
        >>>     records = scythe.list_records()
        >>>     for record in records:
        >>>         print(record)

    """

    def __init__(
        self,
        endpoint: str,
        *,
        http_config: HTTPConfig | None = None,
        retry_config: RetryConfig | None = None,
        http_method: str = "GET",
        iterator: type[BaseOAIIterator] = OAIItemIterator,
        max_retries: int = 0,
        retry_status_codes: Iterable[int] | None = None,
        default_retry_after: float = 60,
        class_mapping: dict[str, type[OAIItem]] | None = None,
        encoding: str = "utf-8",
        auth: AuthTypes | None = None,
        timeout: float = 60,
    ) -> None:
        self.endpoint = endpoint
        if issubclass(iterator, BaseOAIIterator):
            self.iterator = iterator
        else:
            raise TypeError(f"Argument 'iterator' must be subclass of {BaseOAIIterator.__name__}")
        retry_defaults = RetryConfig()
        legacy_retry_arguments_used = (
            max_retries != retry_defaults.max_retries
            or retry_status_codes is not None
            or default_retry_after != retry_defaults.default_retry_after
        )
        if retry_config is not None:
            if legacy_retry_arguments_used:
                raise ValueError(
                    "Cannot specify both 'retry_config' and the deprecated arguments 'max_retries', 'retry_status_codes', "
                    "or 'default_retry_after'. Use only the 'retry_config' argument."
                )
            self.retry_config = retry_config
        else:
            if legacy_retry_arguments_used:
                warnings.warn(
                    "The arguments 'max_retries', 'retry_status_codes', and 'default_retry_after' are deprecated. "
                    "Use the 'retry_config' argument with a RetryConfig instance instead. "
                    "These arguments will be removed in version 0.19.0.",
                    FutureWarning,
                    stacklevel=2,
                )
            self.retry_config = RetryConfig(
                max_retries=max_retries,
                retry_status_codes=(
                    tuple(retry_status_codes) if retry_status_codes is not None else retry_defaults.retry_status_codes
                ),
                default_retry_after=default_retry_after,
            )
        self.max_retries = self.retry_config.max_retries
        self.retry_status_codes = self.retry_config.retry_status_codes
        self.default_retry_after = self.retry_config.default_retry_after
        http_defaults = HTTPConfig()
        legacy_http_arguments_used = (
            http_method != http_defaults.http_method
            or timeout != http_defaults.timeout
            or auth is not None
            or encoding != http_defaults.encoding
        )
        if http_config is not None:
            if legacy_http_arguments_used:
                raise ValueError(
                    "Cannot specify both 'http_config' and the deprecated arguments 'http_method', 'timeout', 'auth', "
                    "or 'encoding'. Use only the 'http_config' argument."
                )
            self.http_config = http_config
        else:
            if legacy_http_arguments_used:
                warnings.warn(
                    "The arguments 'http_method', 'timeout', 'auth', and 'encoding' are deprecated. "
                    "Use the 'http_config' argument with an HTTPConfig instance instead. "
                    "These arguments will be removed in version 0.19.0.",
                    FutureWarning,
                    stacklevel=2,
                )
            self.http_config = HTTPConfig(http_method=http_method, timeout=timeout, auth=auth, encoding=encoding)
        self.http_method = self.http_config.http_method
        self.timeout = self.http_config.timeout
        self.auth = self.http_config.auth
        self.encoding = self.http_config.encoding
        self.oai_namespace = OAI_NAMESPACE
        self.class_mapping = class_mapping or DEFAULT_CLASS_MAP
        self._client: httpx2.Client | None = None

    @property
    def client(self) -> httpx2.Client:
        """Provide a reusable HTTP client instance for making requests.

        This property ensures that an `httpx2.Client` instance is created and maintained for
        the lifecycle of the `Scythe` instance. It handles the creation of the client and
        ensures that a new client is created if the existing one is closed.

        Returns:
            A reusable HTTP client instance for making HTTP requests.
        """
        if self._client is None or self._client.is_closed:
            headers = {
                "Accept": "text/xml; charset=utf-8, application/xml; charset=utf-8",
                "user-agent": self.http_config.user_agent,
            }
            self._client = httpx2.Client(
                headers=headers,
                timeout=self.timeout,
                auth=self.auth,
                default_encoding=self.encoding,
                event_hooks={"response": [log_response]},
            )
        return self._client

    def close(self) -> None:
        """Close the internal HTTP client if it exists and is open.

        This method is responsible for explicitly closing the `httpx2.Client` instance used
        by the `Scythe` class. It should be called when the client is no longer needed, to
        ensure proper cleanup and release of resources.

        Note:
            It's recommended to call this method at the end of operations or when the `Scythe`
            instance is no longer in use, especially if it's not being used as a context manager.
        """
        if self._client and not self._client.is_closed:
            self._client.close()

    def __enter__(self) -> Self:
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        self.close()

    def harvest(self, query: dict[str, str]) -> OAIResponse:
        """Perform an HTTP request to the OAI server with the given parameters.

        Send an OAI-PMH request to the server using the specified parameters. Handle retry logic
        for failed requests based on the configured retry settings and response status codes.

        Args:
            query: A dictionary containing the request parameters.

        Returns:
            An OAIResponse object encapsulating the server's response.

        Raises:
            OAIPMHException: If the response contains an OAI-PMH <error> element, regardless of the HTTP
                status code. The exception type corresponds to the error code (e.g. IdDoesNotExist).
            httpx2.HTTPError: If the HTTP request fails after the maximum number of retries.
        """
        http_response = self._request_with_retry(query)

        oai_response = OAIResponse(http_response, params=query)
        oai_response.raise_for_oaipmh_error()
        http_response.raise_for_status()
        return oai_response

    def _request_with_retry(self, query: dict[str, str]) -> httpx2.Response:
        """Send an HTTP request, retrying failed requests according to the retry configuration.

        Retries are triggered by HTTP status codes in ``retry_status_codes`` (waiting for the 'retry-after' header
        or ``default_retry_after`` seconds) and, when ``retry_on_transport_error`` is enabled, by
        ``httpx2.TransportError`` exceptions (waiting with exponential backoff starting at ``initial_backoff``
        seconds, capped at ``default_retry_after``, and randomized between 50% and 100% of the computed wait).
        Both retry types share the ``max_retries`` budget.

        Args:
            query: A dictionary containing the request parameters.

        Returns:
            A Response object representing the server's response to the HTTP request.

        Raises:
            httpx2.TransportError: If a transport error occurs and retries are disabled or the retry budget is
                exhausted.
        """
        attempt = 0
        while True:
            try:
                http_response = self._request(query)
            except httpx2.TransportError as error:
                if not (self.retry_config.retry_on_transport_error and attempt < self.max_retries):
                    raise
                backoff = min(self.retry_config.initial_backoff * 2**attempt, self.default_retry_after)
                sleep_for = random.uniform(backoff / 2, backoff)
                logger.warning("Transport error: %s! Retrying after %.2f seconds...", error, sleep_for)
                time.sleep(sleep_for)
                attempt += 1
                continue
            if (
                httpx2.codes.is_error(http_response.status_code)
                and http_response.status_code in self.retry_status_codes
                and attempt < self.max_retries
            ):
                retry_after = self._get_retry_after(http_response)
                logger.warning("HTTP %d! Retrying after %d seconds...", http_response.status_code, retry_after)
                time.sleep(retry_after)
                attempt += 1
                continue
            return http_response

    def _request(self, query: dict[str, str]) -> httpx2.Response:
        """Send an HTTP request to the OAI server using the configured HTTP method and given query parameters.

        Args:
            query: A dictionary containing the request parameters.

        Returns:
            A Response object representing the server's response to the HTTP request.
        """
        if self.http_method == "GET":
            return self.client.get(self.endpoint, params=query)
        return self.client.post(self.endpoint, data=query)

    def list_records(
        self,
        from_: str | None = None,
        until: str | None = None,
        metadata_prefix: str = "oai_dc",
        set_: str | None = None,
        resumption_token: str | None = None,
        ignore_deleted: bool = False,
    ) -> Iterator[OAIResponse | Record]:
        """Issue a ListRecords request to the OAI server.

        Send a request to list records from the OAI server, allowing for selective harvesting based on date range,
        set membership, and metadata format. This method supports pagination via resumption tokens and can optionally
        ignore records marked as deleted.

        Ref: <https://openarchives.org/OAI/openarchivesprotocol.html#ListRecords>

        Args:
            from_: An optional date string specifying the start of a date range for harvesting records.
            until: An optional date string specifying the end of a date range for harvesting records.
            metadata_prefix: The metadata format for the records to be harvested. Defaults to "oai_dc".
            set_: An optional set identifier to restrict the harvest to records within a specific set.
            resumption_token: An optional token for pagination, used to continue a request for the next page of records.
            ignore_deleted: If True, skip records flagged as deleted in the response.

        Yields:
            An iterator over OAIResponse or Record objects, each representing an individual record or response
                from the server.

        Raises:
            BadArgument: If the arguments provided do not conform to the expectations of the OAI server.
            BadResumptionToken: If the provided resumption token is invalid or expired.
            CannotDisseminateFormat: If the specified metadata_prefix is not supported by the OAI server.
            NoRecordsMatch: If no records match the provided criteria.
            NoSetHierarchy: If set-based harvesting is requested but the OAI server does not support sets.

        """
        _query = {
            "verb": "ListRecords",
            "from": from_,
            "until": until,
            "metadataPrefix": metadata_prefix,
            "set": set_,
            "resumptionToken": resumption_token,
        }
        query = filter_dict_except_resumption_token(_query)
        yield from self.iterator(self, query, ignore_deleted=ignore_deleted)

    def list_identifiers(
        self,
        from_: str | None = None,
        until: str | None = None,
        metadata_prefix: str = "oai_dc",
        set_: str | None = None,
        resumption_token: str | None = None,
        ignore_deleted: bool = False,
    ) -> Iterator[OAIResponse | Header]:
        """Issue a ListIdentifiers request to the OAI server.

        Send a request to list record identifiers from the OAI server. This method allows filtering records based on
        date range, set membership, and metadata format. It also supports pagination through resumption tokens and has
        an option to ignore deleted records.

        Ref: <https://openarchives.org/OAI/openarchivesprotocol.html#ListIdentifiers>

        Args:
            from_: An optional date string specifying the start of a date range for harvesting records.
            until: An optional date string specifying the end of a date range for harvesting records.
            metadata_prefix: The metadata format for the records to be harvested. Defaults to "oai_dc".
            set_: An optional set identifier to restrict the harvest to records within a specific set.
            resumption_token: An optional token for pagination, used to continue a request for the next page of
                identifiers.
            ignore_deleted: If True, skip records flagged as deleted in the response.

        Yields:
            An iterator over OAIResponse or Header objects, each representing an individual record identifier
                or response from the server.

        Raises:
            BadResumptionToken: If the provided resumption token is invalid or expired.
            CannotDisseminateFormat: If the specified metadata_prefix is not supported by the OAI server.
            NoRecordsMatch: If no records match the provided criteria.
            NoSetHierarchy: If set-based harvesting is requested but the OAI server does not support sets.

        """
        _query = {
            "verb": "ListIdentifiers",
            "from": from_,
            "until": until,
            "metadataPrefix": metadata_prefix,
            "set": set_,
            "resumptionToken": resumption_token,
        }

        query = filter_dict_except_resumption_token(_query)
        yield from self.iterator(self, query, ignore_deleted=ignore_deleted)

    def list_sets(self, resumption_token: str | None = None) -> Iterator[OAIResponse | Set]:
        """Issue a ListSets request to the OAI server.

        Send a request to list all sets defined in the OAI server. Sets are used to categorize records in the OAI
        repository. This method allows for the retrieval of these sets, optionally using a resumption token to handle
        pagination.

        Ref: <https://openarchives.org/OAI/openarchivesprotocol.html#ListSets>

        Args:
            resumption_token: An optional token for pagination, used to continue a request for the next batch of sets.

        Yields:
            An iterator over OAIResponse or Set objects, representing an individual set or response from the server.

        Raises:
            BadResumptionToken: If the provided resumption token is invalid or expired.
            NoSetHierarchy: If the OAI server does not support sets or has no set hierarchy available.

        """
        _query = {
            "verb": "ListSets",
            "resumptionToken": resumption_token,
        }
        query = filter_dict_except_resumption_token(_query)
        yield from self.iterator(self, query)

    def identify(self) -> Identify:
        """Issue an Identify request to the OAI server.

        Send a request to identify the OAI server and retrieve its information. This includes details such as the repository name,
        the base URL, the protocol version, and other relevant data about the OAI server. It's useful for understanding the
        capabilities and configuration of the server.

        Ref: <https://openarchives.org/OAI/openarchivesprotocol.html#Identify>

        Returns:
            An object encapsulating the server's identify response, which contains various pieces of information about
                the OAI server.

        """
        query = {"verb": "Identify"}
        return Identify(self.harvest(query))

    def get_record(self, identifier: str, metadata_prefix: str = "oai_dc") -> OAIResponse | Record:
        """Issue a GetRecord request to the OAI server.

        Send a request to the OAI server to retrieve a specific record. The request is constructed with the provided
        identifier and metadata prefix. The method then processes and returns the relevant OAIResponse or Record object
        using an iterator.


        Ref: <https://openarchives.org/OAI/openarchivesprotocol.html#GetRecord>

        Args:
            identifier: A unique identifier for the record to be retrieved from the OAI server.
            metadata_prefix: The metadata format to be returned for the record. Defaults to "oai_dc".

        Returns:
            An OAIResponse or Record object representing the requested record.

        Raises:
            CannotDisseminateFormat: If the specified metadata_prefix is not supported by the OAI server for
                the requested record.
            IdDoesNotExist: If the specified identifier does not correspond to any record in the OAI server.

        """
        query = {
            "verb": "GetRecord",
            "identifier": identifier,
            "metadataPrefix": metadata_prefix,
        }
        return next(iter(self.iterator(self, query)))

    def list_metadata_formats(self, identifier: str | None = None) -> Iterator[OAIResponse | MetadataFormat]:
        """Issue a ListMetadataFormats request to the OAI server.

        Send a request to list the metadata formats available from the OAI server. This can be done for the entire
        repository or for a specific record if an identifier is provided. The method constructs a query and yields an
        iterator over OAIResponse or MetadataFormat objects, each representing a different metadata format or response
        from the server.

        Ref: <https://openarchives.org/OAI/openarchivesprotocol.html#ListMetadataFormats>

        Args:
            identifier: An optional unique identifier for a specific record to query available metadata formats.
                        If None, all metadata formats available in the repository are listed.

        Yields:
            An iterator over OAIResponse or MetadataFormat objects, each representing an individual metadata format
                or response from the server.

        Raises:
            IdDoesNotExist: If the specified identifier does not correspond to any record in the OAI server.
            NoMetadataFormats: If there are no metadata formats available for the requested record or repository.

        """
        _query = {
            "verb": "ListMetadataFormats",
            "identifier": identifier,
        }
        query = remove_none_values(_query)
        yield from self.iterator(self, query)

    def _get_retry_after(self, http_response: httpx2.Response) -> int | float:
        """Determine the appropriate time to wait before retrying a request, based on the server's response.

        Check the status code of the provided HTTP response. If it's 503 (Service Unavailable), attempt to parse
        the [Retry-After](https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Retry-After)
        response header to find the suggested wait time. If parsing fails or a different status code is received,
        use the default retry time.

        Args:
            http_response: The HTTP response received from the OAI server.

        Returns:
            An integer representing the number of seconds to wait before retrying the request.
        """
        if http_response.status_code == httpx2.codes.SERVICE_UNAVAILABLE:
            retry_after = http_response.headers.get("retry-after")
            if retry_after is not None:
                return int(retry_after)
        return self.default_retry_after

    @deprecated(
        "Scythe.get_retry_after() is not part of the public API. There is no public replacement. "
        "To customize retries, use the retry_config argument instead. "
        "This method will be removed in version 0.18.0.",
        category=FutureWarning,
    )
    def get_retry_after(self, http_response: httpx2.Response) -> int | float:
        """See _get_retry_after."""
        return self._get_retry_after(http_response)
