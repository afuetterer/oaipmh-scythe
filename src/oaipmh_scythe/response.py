# SPDX-FileCopyrightText: 2015 Mathias Loesch
# SPDX-FileCopyrightText: 2023 Heinz-Alexander Fütterer
#
# SPDX-License-Identifier: BSD-3-Clause

"""The response module offers a structured representation of responses from OAI-PMH services.

This module defines the OAIResponse class, which encapsulates the HTTP response from an OAI-PMH server,
providing easy access to its content both as raw text and as parsed XML. It is designed to work seamlessly
with various components of an OAI-PMH client, handling the nuances of OAI-PMH responses.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from lxml import etree

if TYPE_CHECKING:
    from httpx2 import Response

from oaipmh_scythe import exceptions

XMLParser = etree.XMLParser(remove_blank_text=True, recover=True, resolve_entities=False)
OAI_NAMESPACE: str = "{http://www.openarchives.org/OAI/2.0/}"


@dataclass
class OAIResponse:
    """Represents a response received from an OAI server, encapsulating the raw HTTP response and parsed XML content.

    This class provides a structured way to access various aspects of an OAI server's response.
    It offers methods to retrieve the raw text of the response, parse it as XML,
    and obtain a string representation of the response that includes the OAI verb.

    Attributes:
        http_response: The original HTTP response object from the OAI server.
        params: A dictionary of the OAI parameters used in the request that led to this response.
    """

    http_response: Response
    params: dict[str, str]

    @property
    def raw(self) -> str:
        """Return the raw text of the server's response as a unicode string."""
        return self.http_response.text

    @property
    def xml(self) -> etree.Element:
        """Parse the server's response content and return it as an `etree.Element` object."""
        return etree.XML(self.http_response.content, parser=XMLParser)

    def raise_for_oaipmh_error(self) -> None:
        """Check for OAI-PMH error elements in the XML response and raise the corresponding exception.

        Parses the response XML to detect <error> elements. If found, extracts the error code and message,
        then raises the appropriate exception from oaipmh_scythe.exceptions based on the error code.
        Non-XML responses are silently ignored.

        Raises:
            BadArgument: When the OAI response contains an error with code="badArgument".
            BadResumptionToken: When the OAI response contains an error with code="badResumptionToken".
            BadVerb: When the OAI response contains an error with code="badVerb".
            CannotDisseminateFormat: When the OAI response contains an error with code="cannotDisseminateFormat".
            IdDoesNotExist: When the OAI response contains an error with code="idDoesNotExist".
            NoMetadataFormats: When the OAI response contains an error with code="noMetadataFormats".
            NoRecordsMatch: When the OAI response contains an error with code="noRecordsMatch".
            NoSetHierarchy: When the OAI response contains an error with code="noSetHierarchy".
            GeneralOAIPMHError: When the error code is unknown, empty, or the exception class cannot be resolved.
        """
        try:
            error = self.xml.find(f"{OAI_NAMESPACE}error")
        except etree.XMLSyntaxError:
            # Response is not XML, treat as non-error
            return
        if error is None:
            return
        code = error.attrib.get("code", "")
        description = error.text or ""
        exception_name = code[0].upper() + code[1:] if code else ""
        try:
            error_class = getattr(exceptions, exception_name)
        except AttributeError:
            error_class = exceptions.GeneralOAIPMHError
        raise error_class(description)

    def __str__(self) -> str:
        verb = self.params.get("verb")
        return f"<OAIResponse {verb}>"
