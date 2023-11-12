# SPDX-FileCopyrightText: 2015 Mathias Loesch
# SPDX-FileCopyrightText: 2023 Heinz-Alexander Fuetterer
#
# SPDX-License-Identifier: BSD-3-Clause

"""The iterator module provides classes for iterating over data retrieved from OAI-PMH services.

This module includes the BaseOAIIterator, an abstract base class that defines a standard interface
for OAI-PMH data iteration, along with its specialized subclasses. Each subclass is tailored
to handle specific types of data such as records, identifiers, or sets,
ensuring efficient and structured access to OAI-PMH responses.

Classes:
    BaseOAIIterator: An abstract base class for creating iterators over OAI-PMH data.
    OAIResponseIterator: Iterates over OAI responses, handling pagination and resumption tokens.
    OAIItemIterator: Provides iteration over specific OAI items like records, identifiers, and sets.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

from oaipmh_scythe import exceptions
from oaipmh_scythe.models import ResumptionToken

if TYPE_CHECKING:
    from collections.abc import Iterator

    from oaipmh_scythe import Scythe
    from oaipmh_scythe.models import OAIItem
    from oaipmh_scythe.response import OAIResponse

VERBS_ELEMENTS: dict[str, str] = {
    "GetRecord": "record",
    "ListRecords": "record",
    "ListIdentifiers": "header",
    "ListSets": "set",
    "ListMetadataFormats": "metadataFormat",
    "Identify": "Identify",
}


class BaseOAIIterator(ABC):
    """An abstract base class for iterators over various types of data aggregated through the OAI-PMH protocol.

    This class provides a common interface and implementation for iterating over records, identifiers,
    and sets obtained via OAI-PMH. It handles OAI-PMH's resumption token mechanism, allowing seamless
    iteration over potentially large sets of data.

    Args:
        scythe: The Scythe instance used to perform OAI-PMH requests.
        params: A dictionary of parameters specifying the details of the OAI-PMH request.
        ignore_deleted: A boolean flag indicating whether to ignore deleted records in the iteration.

    Attributes:
        scythe: The Scythe instance handling OAI-PMH requests.
        params: The parameters for OAI-PMH requests.
        ignore_deleted: Indicates whether deleted records should be ignored.
        verb: The OAI-PMH verb (e.g., 'ListRecords', 'ListIdentifiers') used in the request.
        oai_response: The most recent OAIResponse received from the OAI server.
        resumption_token: The current resumption token, if any, for paginated results.
    """

    def __init__(self, scythe: Scythe, params: dict[str, str], ignore_deleted: bool = False) -> None:
        self.scythe = scythe
        self.params = params
        self.ignore_deleted = ignore_deleted
        self.verb: str = self.params["verb"]
        self.oai_response: OAIResponse | None = None
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
        ns = self.scythe.oai_namespace
        if (
            self.oai_response is not None
            and (token_element := self.oai_response.xml.find(f".//{ns}resumptionToken")) is not None
        ):
            return ResumptionToken(
                token=token_element.text,
                cursor=token_element.attrib.get("cursor"),  # type: ignore [arg-type]
                complete_list_size=token_element.attrib.get("completeListSize"),  # type: ignore [arg-type]
                expiration_date=token_element.attrib.get("expirationDate"),  # type: ignore [arg-type]
            )
        return None

    def _next_response(self) -> None:
        """Request the next batch of data from the OAI server using the current resumption token.

        This method is used internally to handle the pagination of OAI-PMH responses. It updates the `oai_response`
        attribute with the next batch of data from the server.

        If an error is encountered in the OAI response, an appropriate exception is raised.
        """
        if self.resumption_token and self.resumption_token.token:
            self.params = {"resumptionToken": self.resumption_token.token, "verb": self.verb}
        self.oai_response = self.scythe.harvest(**self.params)

        if (error := self.oai_response.xml.find(f".//{self.scythe.oai_namespace}error")) is not None:
            code = str(error.attrib.get("code", "UNKNOWN"))
            description = error.text or ""
            try:
                exception_name = code[0].upper() + code[1:]
                raise getattr(exceptions, exception_name)(description)
            except AttributeError as exc:
                raise exceptions.GeneralOAIPMHError(description) from exc
        self.resumption_token = self._get_resumption_token()


class OAIResponseIterator(BaseOAIIterator):
    """An iterator class for iterating over OAI responses obtained via the OAI-PMH protocol.

    This iterator specifically handles the iteration of OAIResponse objects, allowing for seamless
    navigation through a sequence of responses returned by an OAI-PMH request. It utilizes the
    underlying mechanisms of the BaseOAIIterator, including handling of resumption tokens for paginated data.
    """

    def __iter__(self) -> Iterator[OAIResponse]:
        """Yield the next OAIResponse object from the server response sequence.

        Enable the OAIResponseIterator to iterate over a series of OAIResponse objects, managing pagination
        with resumption tokens. Continue yielding responses until no more data is available from the server.

        Yields:
            OAIResponse: The next available OAIResponse object in the sequence.
        """
        while True:
            if self.oai_response:
                yield self.oai_response
                self.oai_response = None
            elif self.resumption_token and self.resumption_token.token:
                self._next_response()
            else:
                return


class OAIItemIterator(BaseOAIIterator):
    """An iterator class for iterating over various types of OAI items aggregated via OAI-PMH.

    This iterator is designed to handle the iteration of specific OAI items, such as records or sets, from a repository.
    It extends the functionality of the BaseOAIIterator to parse and yield individual items from the OAI-PMH responses.

    Args:
        scythe: The Scythe instance used for making OAI-PMH requests.
        params: A dictionary of OAI-PMH request parameters.
        ignore_deleted: A boolean indicating whether to ignore deleted records in the response.
    """

    def __init__(self, scythe: Scythe, params: dict[str, str], ignore_deleted: bool = False) -> None:
        self.verb = params["verb"]
        self.mapper = scythe.class_mapping[self.verb]
        self.element = VERBS_ELEMENTS[self.verb]
        super().__init__(scythe, params, ignore_deleted)

    def _next_response(self) -> None:
        """Fetch and process the next response from the OAI server.

        Override the BaseOAIIterator's _next_response method to parse and set up the iterator
        for the specific elements (e.g. records, headers) based on the current resumption token.
        """
        super()._next_response()
        if self.oai_response is not None:
            self._items = self.oai_response.xml.iterfind(f".//{self.scythe.oai_namespace}{self.element}")
        else:
            self._items = iter(())

    def __iter__(self) -> Iterator[OAIItem]:
        """Iterate over individual OAI items from the response.

        Go through the items in the OAI-PMH response, applying any necessary mapping and handling
        the exclusion of deleted records if specified. Automatically handle pagination through resumption tokens.

        Yields:
            OAIItem: The next OAI item (e.g., record, identifier, set) from the response.
        """
        while True:
            for item in self._items:
                mapped = self.mapper(item)
                if self.ignore_deleted and mapped.deleted:
                    continue
                yield mapped
            if self.resumption_token and self.resumption_token.token:
                self._next_response()
            else:
                return
