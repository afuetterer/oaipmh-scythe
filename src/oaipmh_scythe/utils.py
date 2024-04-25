# SPDX-FileCopyrightText: 2015 Mathias Loesch
# SPDX-FileCopyrightText: 2023 Heinz-Alexander Fütterer
#
# SPDX-License-Identifier: BSD-3-Clause

"""The utils module provides utility functions for handling XML data in the context of OAI-PMH services.

This module includes functions essential for parsing and transforming XML data obtained from OAI-PMH responses.
These utilities facilitate the extraction of namespaces and conversion of XML elements into
more accessible data structures.

Functions:
    log_response: Log the details of an HTTP response.
    remove_none_values: Remove keys from the dictionary where the value is `None`.
    filter_dict_except_resumption_token: Filter keys from the dictionary, if resumption token is not `None`.
"""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Any

    import httpx


logger = logging.getLogger(__name__)


def log_response(response: httpx.Response) -> None:
    """Log the details of an HTTP response.

    This function logs the HTTP method, URL, and status code of the response for debugging purposes.
    It uses the 'debug' logging level to provide detailed diagnostic information.

    Args:
        response: The response object received from an HTTP request.

    Returns:
        None
    """
    logger.debug(
        "[http] Response: %s %s - Status %s", response.request.method, response.request.url, response.status_code
    )


def remove_none_values(d: dict[str, Any | None]) -> dict[str, Any]:
    """Remove keys from the dictionary where the value is `None`.

    Args:
        d: The input dictionary.

    Returns:
        A new dictionary with the same keys as the input dictionary but none values have been removed.
    """
    return {key: value for key, value in d.items() if value is not None}


def filter_dict_except_resumption_token(d: dict[str, Any | None]) -> dict[str, Any]:
    """Filter out keys with None values from a dictionary, with special handling for 'resumptionToken'.

    If 'resumptionToken' is present and not None, and there are other non-None keys, log a warning and
    retain only 'resumptionToken' and 'verb' keys. Otherwise, return a dictionary excluding any keys
    with None values.

    Args:
        d: The dictionary to filter.

    Returns:
        A filtered dictionary based on the defined criteria.
    """
    allowed_keys = ("verb", "resumptionToken")
    resumption_token_present = d["resumptionToken"] is not None
    non_empty_keys = [k for k, v in d.items() if v is not None and k not in allowed_keys]
    if resumption_token_present and resumption_token_present:
        logger.warning(
            "`resumption_token` should not be used in combination with other parameters. Dropping %s", non_empty_keys
        )
        return {k: v for k, v in d.items() if k in allowed_keys}
    return d


def load_models(metadata_prefix: str | None = None) -> None:
    """Load models based on the provided metadata prefix.

    After loading these models, they are available to the xsdata XmlParser for parsing XML responses into the
    appropriate dataclasses.

    Args:
        metadata_prefix: The metadata format of the response to be parsed. Possible values are 'oai_dc' and 'datacite'.

    Returns:
        None
    """
    match metadata_prefix:
        case "oai_dc":
            from oaipmh_scythe.models.oai_dc import Dc  # noqa: F401
        case "datacite":
            from oaipmh_scythe.models.datacite import Resource  # noqa: F401
        case "marcxml":
            from oaipmh_scythe.models.marcxml import Record  # noqa: F401
        case _:
            pass
