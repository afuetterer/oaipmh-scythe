# SPDX-FileCopyrightText: 2015 Mathias Loesch
# SPDX-FileCopyrightText: 2023 Heinz-Alexander Fuetterer
#
# SPDX-License-Identifier: BSD-3-Clause

"""The models module defines data structures for representing various components of the OAI-PMH protocol.

This module includes classes that encapsulate different entities in OAI-PMH, such as resumption tokens and
various types of OAI items. These classes provide structured representations of OAI-PMH elements,
facilitating their manipulation and processing in client applications.

Classes:
    ResumptionToken: Represents a resumption token used in OAI-PMH for paginated data retrieval.
    OAIItem: A base class for generic OAI items.
    Identify: Represents an Identify response in OAI-PMH.
    Header: Represents an OAI Header element.
    Record: Represents an OAI Record element.
    Set: Represents an OAI Set element.
    MetadataFormat: Represents an OAI MetadataFormat element.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from lxml import etree

from oaipmh_scythe.utils import get_namespace, xml_to_dict

if TYPE_CHECKING:
    from collections.abc import Iterator

    from oaipmh_scythe.response import OAIResponse


@dataclass
class ResumptionToken:
    """A data class representing a resumption token in the OAI-PMH protocol.

    Resumption tokens are used for iterating over multiple sets of results in OAI-PMH
    harvest requests. This class encapsulates the typical components of a resumption token,
    including the token itself, cursor, complete list size, and an expiration date.

    Attributes:
        token: The actual resumption token used for continuing the iteration in subsequent OAI-PMH requests.
            Default is None.
        cursor: A marker indicating the current position in the list of results. Default is None.
        complete_list_size: The total number of records in the complete list of results. Default is None.
        expiration_date: The date and time when the resumption token expires. Default is None.
    """

    token: str | None = None
    cursor: str | None = None
    complete_list_size: str | None = None
    expiration_date: str | None = None

    def __repr__(self) -> str:
        return f"<ResumptionToken {self.token}>"


class OAIItem:
    """A base class representing a generic item in the OAI-PMH protocol.

    This class provides a common structure for handling and manipulating XML data
    associated with different types of OAI-PMH items, such as records, headers, or sets.

    Attributes:
        xml: The parsed XML element representing the OAI item.
        _strip_ns: A flag indicating whether to remove the namespaces from the element names
            in the dictionary representation.
        _oai_namespace: The namespace URI extracted from the XML element.
    """

    def __init__(self, xml: etree._Element, strip_ns: bool = True) -> None:
        super().__init__()
        self.xml = xml
        self._strip_ns = strip_ns
        self._oai_namespace = get_namespace(self.xml)

    def __bytes__(self) -> bytes:
        return etree.tostring(self.xml, encoding="utf-8")

    def __str__(self) -> str:
        return etree.tostring(self.xml, encoding="unicode")

    @property
    def raw(self) -> str:
        """Return the original XML as a unicode string."""
        return etree.tostring(self.xml, encoding="unicode")


class Identify(OAIItem):
    """A class representing an Identify container in the OAI-PMH protocol.

    This class is specifically used for handling the response of an Identify request in OAI-PMH.
    It differs from other OAI entities in that it is initialized with an OAIResponse object
    rather than a direct XML element. The class parses the Identify information from the
    response and provides access to its individual components.

    Args:
        identify_response: The response object from an Identify request.
            It should contain the XML representation of the Identify response.

    Attributes:
        xml: The XML element representing the Identify response.
        _identify_dict: A dictionary containing the parsed Identify information.
        Dynamic Attributes: Based on the content of the Identify response, additional attributes
                            are dynamically set on this object. These can include attributes like
                            repository name, base URL, protocol version, etc.

    Raises:
        ValueError: If the Identify element is not found in the provided XML.
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
        """Iterate over the Identify information, yielding key-value pairs."""
        return iter(self._identify_dict.items())


class Header(OAIItem):
    """A class representing an OAI Header in the OAI-PMH protocol.

    The header contains essential information about a record, such as its identifier, datestamp,
    and set specifications. This class parses these details from the provided XML header element
    and makes them easily accessible as attributes.

    Args:
        header_element: The XML element representing the OAI header.

    Attributes:
        deleted: Indicates whether the record is marked as deleted in the OAI-PMH repository.
        identifier: The unique identifier of the record in the OAI-PMH repository.
        datestamp: The datestamp of the record, indicating when it was last updated.
        setSpecs: A list of set specifications that the record belongs to.
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
        """Iterate over the header information, yielding key-value pairs."""
        return iter(
            [
                ("identifier", self.identifier),
                ("datestamp", self.datestamp),
                ("setSpecs", self.setSpecs),
            ]
        )


class Record(OAIItem):
    """A class representing an OAI record in the OAI-PMH protocol.

    This class encapsulates a record element from an OAI-PMH response, handling its parsing, and providing
    structured access to its details, such as header information and metadata. It checks for the presence of
    the header and metadata elements and raises an error if the header is not found.

    Args:
        record_element: The XML element representing the OAI record.
        strip_ns: If True, namespaces are removed from the element names in the parsed metadata. Defaults to True.

    Attributes:
        header: An instance of the Header class representing the header information of the record.
        deleted: Indicates whether the record is marked as deleted.
        metadata: A dictionary representation of the record's metadata, if available and not deleted.

    Raises:
        ValueError: If the header element is not found in the provided XML.
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
        """Iterate over the record's metadata, yielding key-value pairs."""
        return iter(self.metadata.items())

    def get_metadata(self):
        """Extract and return the record's metadata as a dictionary."""
        # We want to get record/metadata/<container>/*
        # <container> would be the element ``dc``
        # in the ``oai_dc`` case.
        return xml_to_dict(
            self.xml.find(".//" + self._oai_namespace + "metadata").getchildren()[0],
            strip_ns=self._strip_ns,
        )


class Set(OAIItem):
    """A class representing a set in the OAI-PMH protocol.

    This class encapsulates a set element from an OAI-PMH response and provides structured access to its details.
    It parses the set information from the provided XML element and dynamically sets attributes
    based on the parsed content.

    Args:
        set_element: The XML element representing the OAI set. The element is parsed to extract set details.

    Attributes:
        setName: The name of the set, extracted from the set's XML element.
        _set_dict: A dictionary containing the parsed set information.
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
        """Iterate over the set information, yielding key-value pairs."""
        return iter(self._set_dict.items())


class MetadataFormat(OAIItem):
    """A class representing a metadata format in the OAI-PMH protocol.

    This class handles the representation of a metadata format, which is an essential part of the OAI-PMH protocol.
    It parses the provided XML element to extract and store metadata format details such as the metadata prefix.

    Args:
        mdf_element: The XML element representing the metadata format. This element is parsed
            to extract metadata format details.

    Attributes:
        metadataPrefix: The prefix of the metadata format, extracted from the XML element.
        _mdf_dict: A dictionary containing the parsed metadata format details.
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
        """Iterate over the metadata format information, yielding key-value pairs."""
        return iter(self._mdf_dict.items())
