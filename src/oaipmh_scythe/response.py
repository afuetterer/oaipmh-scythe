# SPDX-FileCopyrightText: 2015 Mathias Loesch
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
    from httpx import Response

XMLParser = etree.XMLParser(remove_blank_text=True, recover=True, resolve_entities=False)


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
    def xml(self) -> etree._Element:
        """Parse the server's response content and return it as an `etree._Element` object."""
        return etree.XML(self.http_response.content, parser=XMLParser)

    def __str__(self) -> str:
        verb = self.params.get("verb")
        return f"<OAIResponse {verb}>"
