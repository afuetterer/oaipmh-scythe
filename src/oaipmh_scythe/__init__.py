# SPDX-FileCopyrightText: 2015 Mathias Loesch
#
# SPDX-License-Identifier: BSD-3-Clause

"""oaipmh-scythe. OAI-PMH for Humans."""

from oaipmh_scythe.response import OAIResponse
from oaipmh_scythe.scythe import Scythe

__all__ = [
    "Scythe",
    "OAIResponse",
]

__version__ = "0.7.1"
