# SPDX-FileCopyrightText: 2015 Mathias Loesch
#
# SPDX-License-Identifier: BSD-3-Clause

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

# Map OAI verbs to the XML elements
VERBS_ELEMENTS: dict[str, str] = {
    "GetRecord": "record",
    "ListRecords": "record",
    "ListIdentifiers": "header",
    "ListSets": "set",
    "ListMetadataFormats": "metadataFormat",
    "Identify": "Identify",
}


class BaseOAIIterator(ABC):
    """Iterator over OAI records/identifiers/sets transparently aggregated via OAI-PMH.

    Can be used to conveniently iterate through the records of a repository.

    :param scythe: The Scythe object that issued the first request.
    :param params: The OAI arguments.
    :param ignore_deleted: Flag for whether to ignore deleted records.
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
        """Extract and store the resumptionToken from the last response."""
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
    """Iterator over OAI responses."""

    def __iter__(self) -> Iterator[OAIResponse]:
        """Yield the next response."""
        while True:
            if self.oai_response:
                yield self.oai_response
                self.oai_response = None
            elif self.resumption_token and self.resumption_token.token:
                self._next_response()
            else:
                return


class OAIItemIterator(BaseOAIIterator):
    """Iterator over OAI records/identifiers/sets transparently aggregated via OAI-PMH.

    Can be used to conveniently iterate through the records of a repository.

    :param scythe: The Scythe object that issued the first request.
    :param params: The OAI arguments.
    :param ignore_deleted: Flag for whether to ignore deleted records.
    """

    def __init__(self, scythe: Scythe, params: dict[str, str], ignore_deleted: bool = False) -> None:
        self.verb = params["verb"]
        self.mapper = scythe.class_mapping[self.verb]
        self.element = VERBS_ELEMENTS[self.verb]
        super().__init__(scythe, params, ignore_deleted)

    def _next_response(self) -> None:
        super()._next_response()
        if self.oai_response is not None:
            self._items = self.oai_response.xml.iterfind(f".//{self.scythe.oai_namespace}{self.element}")
        else:
            self._items = iter(())

    def __iter__(self) -> Iterator[OAIItem]:
        """Yield the next record/header/set."""
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
