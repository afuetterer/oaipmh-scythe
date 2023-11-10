# SPDX-FileCopyrightText: 2015 Mathias Loesch
#
# SPDX-License-Identifier: BSD-3-Clause
from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from lxml import etree

from oaipmh_scythe.response import OAIResponse
from oaipmh_scythe.utils import get_namespace, xml_to_dict

if TYPE_CHECKING:
    from collections.abc import Iterator


@dataclass
class ResumptionToken:
    """Represents a resumption token."""

    token: str | None = None
    cursor: str | None = None
    complete_list_size: str | None = None
    expiration_date: str | None = None

    def __repr__(self) -> str:
        return f"<ResumptionToken {self.token}>"


class OAIItem:
    """A generic OAI item.

    :param xml: XML representation of the entity.
    :param strip_ns: Flag for whether to remove the namespaces from the
                     element names in the dictionary representation.
    """

    def __init__(self, xml: etree._Element, strip_ns: bool = True) -> None:
        super().__init__()

        # The original parsed XML
        self.xml = xml
        self._strip_ns = strip_ns
        self._oai_namespace = get_namespace(self.xml)

    def __bytes__(self) -> bytes:
        return etree.tostring(self.xml, encoding="utf-8")

    def __str__(self) -> str:
        return etree.tostring(self.xml, encoding="unicode")

    @property
    def raw(self) -> str:
        """The original XML as unicode."""
        return etree.tostring(self.xml, encoding="unicode")


class Identify(OAIItem):
    """Represents an Identify container.

    This object differs from the other entities in that is has to be created
    from a :class:`sickle.response.OAIResponse` instead of an XML element.

    :param identify_response: The response for an Identify request.
    """

    def __init__(self, identify_response: OAIResponse) -> None:
        super().__init__(identify_response.xml, strip_ns=True)
        identify_element = self.xml.find(f".//{self._oai_namespace}Identify")
        if identify_element is None:
            raise ValueError("Identify element not found in the XML.")
        self.xml = identify_element
        self._identify_dict = xml_to_dict(self.xml, strip_ns=True)
        for k, v in self._identify_dict.items():
            setattr(self, k.replace("-", "_"), v[0])

    def __repr__(self) -> str:
        return "<Identify>"

    def __iter__(self) -> Iterator:
        return iter(self._identify_dict.items())


class Header(OAIItem):
    """Represents an OAI Header.

    :param header_element: The XML element 'header'.
    """

    def __init__(self, header_element: etree._Element) -> None:
        super().__init__(header_element, strip_ns=True)
        self.deleted = self.xml.attrib.get("status") == "deleted"
        _identifier_element = self.xml.find(f"{self._oai_namespace}identifier")
        _datestamp_element = self.xml.find(f"{self._oai_namespace}datestamp")

        self.identifier = getattr(_identifier_element, "text", None)
        self.datestamp = getattr(_datestamp_element, "text", None)
        self.setSpecs = [setSpec.text for setSpec in self.xml.findall(f"{self._oai_namespace}setSpec")]

    def __repr__(self) -> str:
        return f"<Header {self.identifier}{' [deleted]' if self.deleted else ''}>"

    def __iter__(self) -> Iterator:
        return iter(
            [
                ("identifier", self.identifier),
                ("datestamp", self.datestamp),
                ("setSpecs", self.setSpecs),
            ]
        )


class Record(OAIItem):
    """Represents an OAI record.

    :param record_element: The XML element 'record'.
    :param strip_ns: Flag for whether to remove the namespaces from the
                     element names.
    """

    def __init__(self, record_element: etree._Element, strip_ns: bool = True) -> None:
        super().__init__(record_element, strip_ns=strip_ns)
        header_element = self.xml.find(f".//{self._oai_namespace}header")
        if header_element is None:
            raise ValueError("Header element not found in the XML.")
        self.header = Header(header_element)
        self.deleted = self.header.deleted
        if not self.deleted:
            self.metadata = self.get_metadata()

    def __repr__(self) -> str:
        return f"<Record {self.header.identifier}{' [deleted]' if self.header.deleted else ''}>"

    def __iter__(self) -> Iterator:
        return iter(self.metadata.items())

    def get_metadata(self):
        # We want to get record/metadata/<container>/*
        # <container> would be the element ``dc``
        # in the ``oai_dc`` case.
        return xml_to_dict(
            self.xml.find(".//" + self._oai_namespace + "metadata").getchildren()[0],
            strip_ns=self._strip_ns,
        )


class Set(OAIItem):
    """Represents an OAI set.

    :param set_element: The XML element 'set'.
    :type set_element: :class:`lxml.etree._Element`
    """

    def __init__(self, set_element: etree._Element) -> None:
        super().__init__(set_element, strip_ns=True)
        self._set_dict = xml_to_dict(self.xml, strip_ns=True)
        self.setName: str | None = None
        for k, v in self._set_dict.items():
            setattr(self, k.replace("-", "_"), v[0])

    def __repr__(self) -> str:
        return f"<Set {self.setName}>"

    def __iter__(self) -> Iterator:
        return iter(self._set_dict.items())


class MetadataFormat(OAIItem):
    """Represents an OAI MetadataFormat.

    :param mdf_element: The XML element 'metadataFormat'.
    """

    def __init__(self, mdf_element: etree._Element) -> None:
        super().__init__(mdf_element, strip_ns=True)
        self._mdf_dict = xml_to_dict(self.xml, strip_ns=True)
        self.metadataPrefix: str | None = None
        for k, v in self._mdf_dict.items():
            setattr(self, k.replace("-", "_"), v[0])

    def __repr__(self) -> str:
        return f"<MetadataFormat {self.metadataPrefix}>"

    def __iter__(self) -> Iterator:
        return iter(self._mdf_dict.items())
