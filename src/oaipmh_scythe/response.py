# SPDX-FileCopyrightText: 2015 Mathias Loesch
#
# SPDX-License-Identifier: BSD-3-Clause

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from lxml import etree

if TYPE_CHECKING:
    from httpx import Response

XMLParser = etree.XMLParser(remove_blank_text=True, recover=True, resolve_entities=False)


@dataclass
class OAIResponse:
    """A response from an OAI server.

    Provides access to the returned data on different abstraction
    levels.

    :param http_response: The original HTTP response.
    :param params: The OAI parameters for the request.
    """

    http_response: Response
    params: dict[str, str]

    @property
    def raw(self) -> str:
        """The server's response as unicode."""
        return self.http_response.text

    @property
    def xml(self) -> etree._Element:
        """The server's response as parsed XML."""
        return etree.XML(self.http_response.content, parser=XMLParser)

    def __str__(self) -> str:
        """Return a string representation of the response."""
        verb = self.params.get("verb")
        return f"<OAIResponse {verb}>"
