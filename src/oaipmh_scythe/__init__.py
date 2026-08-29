# SPDX-FileCopyrightText: 2015 Mathias Loesch
# SPDX-FileCopyrightText: 2023 Heinz-Alexander Fütterer
#
# SPDX-License-Identifier: BSD-3-Clause

"""oaipmh-scythe: A Scythe for harvesting OAI-PMH repositories."""

from oaipmh_scythe.client import Scythe
from oaipmh_scythe.config import RetryConfig
from oaipmh_scythe.exceptions import (
    BadArgument,
    BadResumptionToken,
    BadVerb,
    CannotDisseminateFormat,
    GeneralOAIPMHError,
    IdDoesNotExist,
    NoMetadataFormats,
    NoRecordsMatch,
    NoSetHierarchy,
    OAIPMHException,
)
from oaipmh_scythe.response import OAIResponse

__all__ = [
    "BadArgument",
    "BadResumptionToken",
    "BadVerb",
    "CannotDisseminateFormat",
    "GeneralOAIPMHError",
    "IdDoesNotExist",
    "NoMetadataFormats",
    "NoRecordsMatch",
    "NoSetHierarchy",
    "OAIPMHException",
    "OAIResponse",
    "RetryConfig",
    "Scythe",
]
