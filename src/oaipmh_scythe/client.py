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

import inspect
import logging
import time
from importlib.metadata import version
from typing import TYPE_CHECKING

import httpx

from oaipmh_scythe.iterator import BaseOAIIterator, OAIItemIterator
from oaipmh_scythe.models import Header, Identify, MetadataFormat, OAIItem, Record, Set
from oaipmh_scythe.response import OAIResponse
from oaipmh_scythe.utils import filter_dict_except_resumption_token, log_response, remove_none_values

if TYPE_CHECKING:
    from collections.abc import Iterable, Iterator
    from types import TracebackType

    from httpx._types import AuthTypes

logger = logging.getLogger(__name__)

__version__ = version("oaipmh-scythe")
USER_AGENT: str = f"oaipmh-scythe/{__version__}"
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
        http_method: The HTTP method to use for requests (either 'GET' or 'POST').
        iterator: The iterator class to be used for iterating over responses.
        max_retries: The maximum number of retries for a request in case of failures.
        retry_status_codes: The HTTP status codes on which to retry the request.
        default_retry_after: The default wait time (in seconds) between retries if no 'retry-after' header is present.
        class_mapping: A mapping from OAI verbs to classes representing OAI items.
        encoding: The character encoding for decoding responses. Defaults to the server's specified encoding.
        auth: Optional authentication credentials for accessing the OAI-PMH interface.
        timeout: The timeout (in seconds) for HTTP requests.

    Examples:
        >>> with Scythe("https://zenodo.org/oai2d") as scythe:
        >>>     records = scythe.list_records()
        >>>     for record in records:
        >>>         print(record)

    """

    def __init__(
        self,
        endpoint: str,
        http_method: str = "GET",
        iterator: type[BaseOAIIterator] = OAIItemIterator,
        max_retries: int = 0,
        retry_status_codes: Iterable[int] | None = None,
        default_retry_after: int | float = 60,
        class_mapping: dict[str, type[OAIItem]] | None = None,
        encoding: str = "utf-8",
        auth: AuthTypes | None = None,
        timeout: int | float = 60,
    ):
        self.endpoint = endpoint
        if http_method not in ("GET", "POST"):
            raise ValueError("Invalid HTTP method: %s! Must be GET or POST.")
        self.http_method = http_method
        if inspect.isclass(iterator) and issubclass(iterator, BaseOAIIterator):
            self.iterator = iterator
        else:
            raise TypeError(f"Argument 'iterator' must be subclass of {BaseOAIIterator.__name__}")
        self.max_retries = max_retries
        self.retry_status_codes = retry_status_codes or (503,)
        if default_retry_after <= 0:
            raise ValueError(
                f"Invalid value for 'default_retry_after': {default_retry_after}. default_retry_after must be positive int or float."
            )
        self.default_retry_after = default_retry_after
        self.oai_namespace = OAI_NAMESPACE
        self.class_mapping = class_mapping or DEFAULT_CLASS_MAP
        self.encoding = encoding
        self.auth = auth
        if timeout <= 0:
            raise ValueError(f"Invalid value for 'timeout': {timeout}. Timeout must be positive int or float.")
        self.timeout = timeout
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
            headers = {"Accept": "text/xml; charset=utf-8", "user-agent": USER_AGENT}
            self._client = httpx.Client(
                headers=headers,
                timeout=self.timeout,
                auth=self.auth,
                default_encoding=self.encoding,
                event_hooks={"response": [log_response]},
            )
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

    def __enter__(self) -> Scythe:
        return self

    def __exit__(
        self, exc_type: type[BaseException] | None, exc_val: type[BaseException] | None, exc_tb: TracebackType | None
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
            httpx.HTTPError: If the HTTP request fails after the maximum number of retries.
        """
        http_response = self._request(query)
        for _ in range(self.max_retries):
            if httpx.codes.is_error(http_response.status_code) and http_response.status_code in self.retry_status_codes:
                retry_after = self.get_retry_after(http_response)
                logger.warning("HTTP %d! Retrying after %d seconds...", http_response.status_code, retry_after)
                time.sleep(retry_after)
                http_response = self._request(query)
        http_response.raise_for_status()
        return OAIResponse(http_response, params=query)

    def _request(self, query: dict[str, str]) -> httpx.Response:
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
        query = remove_none_values(filter_dict_except_resumption_token(_query))
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

        query = remove_none_values(filter_dict_except_resumption_token(_query))
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
        query = remove_none_values(filter_dict_except_resumption_token(_query))
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

    def get_retry_after(self, http_response: httpx.Response) -> int | float:
        """Determine the appropriate time to wait before retrying a request, based on the server's response.

        Check the status code of the provided HTTP response. If it's 503 (Service Unavailable),
        attempt to parse the 'retry-after' header to find the suggested wait time. If parsing fails
        or a different status code is received, use the default retry time.

        Args:
            http_response: The HTTP response received from the server.

        Returns:
            An integer representing the number of seconds to wait before retrying the request.
        """
        if http_response.status_code == httpx.codes.SERVICE_UNAVAILABLE:
            try:
                return int(http_response.headers.get("retry-after"))
            except TypeError:
                return self.default_retry_after
        return self.default_retry_after
