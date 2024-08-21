# SPDX-FileCopyrightText: 2015 Mathias Loesch
# SPDX-FileCopyrightText: 2023 Heinz-Alexander Fütterer
#
# SPDX-License-Identifier: BSD-3-Clause

"""The response module offers a structured representation of responses from OAI-PMH services.

This module defines the Response class, which encapsulates the HTTP response from an OAI-PMH server,
providing easy access to its content both as raw text and as parsed XML. It is designed to work seamlessly
with various components of an OAI-PMH client, handling the nuances of OAI-PMH responses.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING

import httpx
from xsdata.formats.dataclass.context import XmlContext
from xsdata.formats.dataclass.parsers import XmlParser

from oaipmh_scythe import exceptions
from oaipmh_scythe.models.oai_pmh import OaiPmh
from oaipmh_scythe.utils import load_models

if TYPE_CHECKING:
    from oaipmh_scythe.models.oai_pmh import OaiPmherror

CONTEXT = XmlContext()
PARSER = XmlParser(context=CONTEXT)


def _build_response(http_response: httpx.Response, metadata_prefix: str | None) -> Response:
    """Build a response object from an HTTP response.

    This function is used to construct a response object from an HTTP response. It checks if the server returned
    an error status code and raises an exception if so. Otherwise, it parses the response content using
    `_parse_response` and returns a Response object with the parsed data.

    Args:
        http_response: The HTTP response to build a response from.
        metadata_prefix: The metadata format used in the request.

    Returns:
        A built response object.

    Raises:
        httpx.HTTPError: If the server returned an error status code >= 500.
    """
    if http_response.is_server_error:
        http_response.raise_for_status()
    parsed = _parse_response(http_response.content, metadata_prefix)
    return Response(
        url=http_response.url,
        status_code=httpx.codes(http_response.status_code),
        content=http_response.content,
        headers=http_response.headers,
        parsed=parsed,
    )


def _parse_response(content: bytes, metadata_prefix: str | None) -> OaiPmh:
    """Parse an HTTP response content into an OAI-PMH object.

    This function uses the xsdata XmlParser to convert the HTTP response content into an OAI-PMH object. It first loads
    any necessary models, then parse the content using the parser. If there are errors in the XML response,
    it raises the appropriate exception.

    Args:
        content: The HTTP response content to parse.
        metadata_prefix: The metadata format used in the request.

    Returns:
        The parsed OAI-PMH object.

    Raises:
        exceptions.OAIPMHException: If there is an error sent from the server in the response content.
    """
    load_models(metadata_prefix)
    parsed = PARSER.from_bytes(content, OaiPmh)
    raise_for_error(parsed.error)
    return parsed


def raise_for_error(errors: list[OaiPmherror] | None) -> None:
    """Raise an exception for each error in the given list.

    Args:
        errors: A list of OAI-PMH errors to raise exceptions for. If None, no exceptions are raised.

    Returns:
        None.

    Raises:
        exceptions.OAIPMHException: If the error list is empty or contains unknown error codes, the appropriate
            exception is raised. Specific exceptions are raised for each known error code.
    """
    if errors is None:
        return
    for error in errors:
        if error.code:
            match error.code:
                case error.code.BAD_ARGUMENT:
                    raise exceptions.BadArgument(error.value)
                case error.code.BAD_RESUMPTION_TOKEN:
                    raise exceptions.BadResumptionToken(error.value)
                case error.code.BAD_VERB:
                    raise exceptions.BadVerb(error.value)
                case error.code.CANNOT_DISSEMINATE_FORMAT:
                    raise exceptions.CannotDisseminateFormat(error.value)
                case error.code.ID_DOES_NOT_EXIST:
                    raise exceptions.IdDoesNotExist(error.value)
                case error.code.NO_METADATA_FORMATS:
                    raise exceptions.NoMetadataFormat(error.value)
                case error.code.NO_RECORDS_MATCH:
                    raise exceptions.NoRecordsMatch(error.value)
                case error.code.NO_SET_HIERARCHY:
                    raise exceptions.NoSetHierarchy(error.value)
        raise exceptions.UndefinedError(error)


@dataclass(slots=True)
class Response:
    """A response received from an OAI server, encapsulating the raw HTTP response and parsed content.

    Attributes:
        url: TODO
        status_code: The HTTP status code of the response.
        headers: A dictionary-like object containing metadata about the response, such as content type and length.
        content: The raw bytes of the response content.
        parsed: The parsed OAI-PMH object representing the OAI-PMH metadata in the response.
    """

    url: httpx.URL
    status_code: httpx.codes
    headers: httpx.Headers = field(repr=False)
    content: bytes = field(repr=False)
    parsed: OaiPmh = field(repr=False)
