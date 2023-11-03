# SPDX-FileCopyrightText: 2015 Mathias Loesch
#
# SPDX-License-Identifier: BSD-3-Clause

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

from oaipmh_scythe import exceptions
from oaipmh_scythe.models import ResumptionToken

if TYPE_CHECKING:
    from oaipmh_scythe import Scythe


# Map OAI verbs to the XML elements
VERBS_ELEMENTS = {
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
    :type params:  dict
    :param ignore_deleted: Flag for whether to ignore deleted records.
    :type ignore_deleted: bool
    """

    def __init__(self, scythe: Scythe, params: dict[str, str], ignore_deleted: bool = False) -> None:
        self.scythe = scythe
        self.params = params
        self.ignore_deleted = ignore_deleted
        self.verb = self.params.get("verb")
        self.resumption_token = None
        self._next_response()

    def __iter__(self):
        return self

    def __next__(self):
        return self.next()

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} {self.verb}>"

    def _get_resumption_token(self) -> ResumptionToken:
        """Extract and store the resumptionToken from the last response."""
        resumption_token_element = self.oai_response.xml.find(".//" + self.scythe.oai_namespace + "resumptionToken")
        if resumption_token_element is None:
            return None
        token = resumption_token_element.text
        cursor = resumption_token_element.attrib.get("cursor")
        complete_list_size = resumption_token_element.attrib.get("completeListSize")
        expiration_date = resumption_token_element.attrib.get("expirationDate")
        resumption_token = ResumptionToken(
            token=token,
            cursor=cursor,
            complete_list_size=complete_list_size,
            expiration_date=expiration_date,
        )
        return resumption_token

    def _next_response(self):
        """Get the next response from the OAI server."""
        params = self.params
        if self.resumption_token:
            params = {"resumptionToken": self.resumption_token.token, "verb": self.verb}
        self.oai_response = self.scythe.harvest(**params)
        error = self.oai_response.xml.find(".//" + self.scythe.oai_namespace + "error")
        if error is not None:
            code = error.attrib.get("code", "UNKNOWN")
            description = error.text or ""
            try:
                raise getattr(exceptions, code[0].upper() + code[1:])(description)
            except AttributeError as exc:
                raise exceptions.OAIError(description) from exc
        self.resumption_token = self._get_resumption_token()

    @abstractmethod
    def next(self):
        pass


class OAIResponseIterator(BaseOAIIterator):
    """Iterator over OAI responses."""

    def next(self):
        """Return the next response."""
        while True:
            if self.oai_response:
                response = self.oai_response
                self.oai_response = None
                return response
            elif self.resumption_token and self.resumption_token.token:
                self._next_response()
            else:
                raise StopIteration


class OAIItemIterator(BaseOAIIterator):
    """Iterator over OAI records/identifiers/sets transparently aggregated via OAI-PMH.

    Can be used to conveniently iterate through the records of a repository.

    :param scythe: The Scythe object that issued the first request.
    :param params: The OAI arguments.
    :type params:  dict
    :param ignore_deleted: Flag for whether to ignore deleted records.
    """

    def __init__(self, scythe: Scythe, params: dict[str, str], ignore_deleted: bool = False) -> None:
        self.mapper = scythe.class_mapping[params.get("verb")]
        self.element = VERBS_ELEMENTS[params.get("verb")]
        super().__init__(scythe, params, ignore_deleted)

    def _next_response(self):
        super()._next_response()
        self._items = self.oai_response.xml.iterfind(".//" + self.scythe.oai_namespace + self.element)

    def next(self):
        """Return the next record/header/set."""
        while True:
            for item in self._items:
                mapped = self.mapper(item)
                if self.ignore_deleted and mapped.deleted:
                    continue
                return mapped
            if self.resumption_token and self.resumption_token.token:
                self._next_response()
            else:
                raise StopIteration
