# SPDX-FileCopyrightText: 2024 Heinz-Alexander Fütterer
#
# SPDX-License-Identifier: BSD-3-Clause

"""TODO."""

from typing import TypeAlias

from oaipmh_scythe.models.oai_dc import Dc  # TODO
from oaipmh_scythe.models.oai_pmh import (
    Header,
    Identify,
    MetadataFormat,
    OaiPmh,
    Record,
    ResumptionToken,
    Set,
    Verb,
)

# `Item` can be used for type annotations
Item: TypeAlias = Header | Record | Set | MetadataFormat

__all__ = [
    "Header",
    "Identify",
    "MetadataFormat",
    "OaiPmh",
    "Record",
    "ResumptionToken",
    "Set",
    "Verb",
    "Item",
    "Dc",  # TODO
]
