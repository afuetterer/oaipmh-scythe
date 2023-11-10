# SPDX-FileCopyrightText: 2015 Mathias Loesch
#
# SPDX-License-Identifier: BSD-3-Clause

"""The utils module provides utility functions for handling XML data in the context of OAI-PMH services.

This module includes functions essential for parsing and transforming XML data obtained from OAI-PMH responses.
These utilities facilitate the extraction of namespaces and conversion of XML elements into
more accessible data structures.

Functions:
    get_namespace: Extracts the namespace from an XML element.
    xml_to_dict: Converts an XML tree or element into a dictionary representation.
"""

from __future__ import annotations

import re
from collections import defaultdict
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from lxml import etree


def get_namespace(element: etree._Element) -> str | None:
    """Return the namespace URI of an XML element.

    Extracts and returns the namespace URI from the tag of the given XML element.
    The namespace URI is enclosed in curly braces at the start of the tag.
    If the element does not have a namespace, `None` is returned.

    Args:
        element: The XML element from which to extract the namespace.

    Returns:
        The namespace URI as a string if the element has a namespace, otherwise `None`.
    """
    match = re.search(r"(\{.*\})", element.tag)
    return match.group(1) if match else None


def xml_to_dict(
    tree: etree._Element, paths: list[str] | None = None, nsmap: dict[str, str] | None = None, strip_ns: bool = False
) -> dict[str, list[str | None]]:
    """Convert an XML tree to a dictionary, with options for custom XPath and namespace handling.

    This function takes an XML element tree and converts it into a dictionary. The keys of the
    dictionary are the tags of the XML elements, and the values are lists of the text contents
    of these elements. It offers options to apply specific XPath expressions, handle namespaces,
    and optionally strip namespaces from the tags in the resulting dictionary.

    Args:
        tree: The root element of the XML tree to be converted.
        paths: An optional list of XPath expressions to apply on the XML tree. If None or not
            provided, the function will consider all elements in the tree.
        nsmap: An optional dictionary for namespace mapping, used to provide shorter, more
            readable paths in XPath expressions. If None or not provided, no namespace
            mapping is applied.
        strip_ns: A boolean flag indicating whether to remove namespaces from the element tags
            in the resulting dictionary. Defaults to False.

    Returns:
        A dictionary where each key is an element tag (with or without namespace, based on
        `strip_ns`) and each value is a list of strings representing the text content of
        each element with that tag.
    """
    paths = paths or [".//"]
    nsmap = nsmap or {}
    fields = defaultdict(list)
    for path in paths:
        elements = tree.findall(path, nsmap)
        for element in elements:
            tag = re.sub(r"\{.*\}", "", element.tag) if strip_ns else element.tag
            fields[tag].append(element.text)
    return dict(fields)
