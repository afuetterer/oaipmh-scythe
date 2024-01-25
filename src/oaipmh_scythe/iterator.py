# SPDX-FileCopyrightText: 2015 Mathias Loesch
# SPDX-FileCopyrightText: 2023 Heinz-Alexander Fütterer
#
# SPDX-License-Identifier: BSD-3-Clause

"""The iterator module provides classes for iterating over data retrieved from OAI-PMH services.

This module includes the BaseOAIIterator, an abstract base class that defines a standard interface
for OAI-PMH data iteration, along with its specialized subclasses. Each subclass is tailored
to handle specific types of data such as records, identifiers, or sets,
ensuring efficient and structured access to OAI-PMH responses.

Classes:
    BaseOAIIterator: An abstract base class for creating iterators over OAI-PMH data.
    ResponseIterator: Iterates over OAI responses, handling pagination and resumption tokens.
    ItemIterator: Provides iteration over specific OAI items like records, identifiers, and sets.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from operator import attrgetter
from typing import TYPE_CHECKING

from oaipmh_scythe.models import Verb

if TYPE_CHECKING:
    from collections.abc import Iterator

    from oaipmh_scythe import Scythe
    from oaipmh_scythe.models import Item, ResumptionToken
    from oaipmh_scythe.response import Response


MAPPING: dict[str, tuple[str, str]] = {
    Verb.LIST_IDENTIFIERS.value: ("list_identifiers", "header"),
    Verb.GET_RECORD.value: ("get_record", "record"),
    Verb.LIST_RECORDS.value: ("list_records", "record"),
    Verb.LIST_SETS.value: ("list_sets", "set"),
    Verb.LIST_METADATA_FORMATS.value: ("list_metadata_formats", "metadata_format"),
}


class BaseOAIIterator(ABC):
    """An abstract base class for iterators over various types of data aggregated through the OAI-PMH protocol.

    This class provides a common interface and implementation for iterating over records, identifiers,
    and sets obtained via OAI-PMH. It handles OAI-PMH's resumption token mechanism, allowing seamless
    iteration over potentially large sets of data.

    Args:
        scythe: The Scythe instance used to perform OAI-PMH requests.
        query: A dictionary of parameters specifying the details of the OAI-PMH request.
        ignore_deleted: A boolean flag indicating whether to ignore deleted records in the iteration.

    Attributes:
        scythe: The Scythe instance handling OAI-PMH requests.
        query: The parameters for OAI-PMH requests.
        ignore_deleted: Indicates whether deleted records should be ignored.
        verb: The OAI-PMH verb (e.g., 'ListRecords', 'ListIdentifiers') used in the request.
        response: The most recent Response received from the OAI server.
        resumption_token: The current resumption token, if any, for paginated results.
    """

    def __init__(self, scythe: Scythe, query: dict[str, str], ignore_deleted: bool = False) -> None:
        self.scythe = scythe
        self.query = query
        self.ignore_deleted = ignore_deleted
        self.verb = self.query["verb"]
        self.response: Response | None = None
        self.resumption_token: ResumptionToken | None = None
        self._next_response()

    @abstractmethod
    def __iter__(self):
        pass

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} {self.verb}>"

    def _get_resumption_token(self) -> ResumptionToken | None:
        """Extract and store the resumption token from the latest OAI response.

        This method parses the current OAI response to extract the resumption token, if available. The token is
        used for fetching subsequent pages of results in a paginated OAI-PMH response.

        Returns:
            A ResumptionToken instance if a token is found in the response, otherwise None.
        """
        if self.response is None:
            return None
        try:
            lookup_attribute = MAPPING[self.verb][0]
            parsed_data = getattr(self.response.parsed, lookup_attribute)
            return parsed_data.resumption_token
        except AttributeError:
            return None

    def _next_response(self) -> None:
        """Request the next batch of data from the OAI server using the current resumption token.

        This method is used internally to handle the pagination of OAI-PMH responses. It updates the `response`
        attribute with the next batch of data from the server.

        If an error is encountered in the OAI response, an appropriate exception is raised.
        """
        if self.resumption_token is not None:
            self.query = {"verb": self.verb, "resumptionToken": self.resumption_token.value}
        self.response = self.scythe.harvest(self.query)
        self.resumption_token = self._get_resumption_token()


class ResponseIterator(BaseOAIIterator):
    """An iterator class for iterating over OAI responses obtained via the OAI-PMH protocol.

    This iterator specifically handles the iteration of Response objects, allowing for seamless navigation through
    a sequence of responses returned by an OAI-PMH request. It utilizes the underlying mechanisms of the
    BaseOAIIterator, including handling of resumption tokens for paginated data.
    """

    def __iter__(self) -> Iterator[Response]:
        """Yield the next Response object from the server response sequence.

        Enable the ResponseIterator to iterate over a series of Response objects, managing pagination with
        resumption tokens. Continue yielding responses until no more data is available from the server.

        Yields:
            The next available Response object in the sequence.
        """
        while True:
            if self.response:
                yield self.response
                self.response = None
            elif self.resumption_token:
                self._next_response()
            else:
                return


class ItemIterator(BaseOAIIterator):
    """An iterator class for iterating over various types of OAI items aggregated via OAI-PMH.

    This iterator is designed to handle the iteration of specific OAI items, such as records or sets, from a repository.
    It extends the functionality of the BaseOAIIterator to parse and yield individual items from the OAI-PMH responses.

    Args:
        scythe: The Scythe instance used for making OAI-PMH requests.
        query: A dictionary of OAI-PMH request parameters.
        ignore_deleted: A boolean indicating whether to ignore deleted records in the response.
    """

    def __init__(self, scythe: Scythe, query: dict[str, str], ignore_deleted: bool = False) -> None:
        self.verb = query["verb"]
        lookup_attribute = MAPPING[query["verb"]][0]
        lookup_element = MAPPING[query["verb"]][1]
        self.items_getter = attrgetter(f"{lookup_attribute}.{lookup_element}")
        super().__init__(scythe, query, ignore_deleted)

    def _next_response(self) -> None:
        """Fetch and process the next response from the OAI server.

        Override the BaseOAIIterator's _next_response method to parse and set up the iterator
        for the specific elements (e.g. records, headers) based on the current resumption token.
        """
        super()._next_response()
        if self.response is not None:
            self._items = self.items_getter(self.response.parsed)
        else:
            self._items = iter(())

    def __iter__(self) -> Iterator[Item]:
        """Iterate over individual OAI items from the response.

        Go through the items in the OAI-PMH response, applying any necessary mapping and handling
        the exclusion of deleted records if specified. Automatically handle pagination through resumption tokens.

        Yields:
            The next OAI item (e.g., record, identifier, set) from the response.
        """
        while True:
            for item in self._items:
                if self.ignore_deleted and item.deleted:
                    continue
                yield item
            if self.resumption_token:
                self._next_response()
            else:
                return
