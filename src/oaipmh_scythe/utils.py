# SPDX-FileCopyrightText: 2015 Mathias Loesch
#
# SPDX-License-Identifier: BSD-3-Clause

from __future__ import annotations

import re
from collections import defaultdict
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from lxml import etree


def get_namespace(element: etree._Element) -> str | None:
    """Return the namespace of an XML element.

    :param element: An XML element.
    """
    match = re.search(r"(\{.*\})", element.tag)
    return match.group(1) if match else None


def xml_to_dict(
    tree: etree._Element, paths: list[str] | None = None, nsmap: dict[str, str] | None = None, strip_ns: bool = False
) -> dict[str, list[str | None]]:
    """Convert an XML tree to a dictionary.

    :param tree: etree Element
    :param paths: An optional list of XPath expressions applied on the XML tree.
    :param nsmap: An optional prefix-namespace mapping for conciser spec of paths.
    :param strip_ns: Flag for whether to remove the namespaces from the tags.
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
