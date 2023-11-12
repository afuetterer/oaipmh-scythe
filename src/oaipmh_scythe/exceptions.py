# SPDX-FileCopyrightText: 2015 Mathias Loesch
#
# SPDX-License-Identifier: BSD-3-Clause

"""Custom exceptions for OAI-PMH related errors."""


class OAIPMHException(Exception):
    """Base exception for all OAI-PMH related errors."""


class BadArgument(OAIPMHException):
    """The request includes illegal arguments, is missing required arguments, includes a repeated argument,
    or values for arguments have an illegal syntax."""


class BadVerb(OAIPMHException):
    """Value of the verb argument is not a legal OAI-PMH verb, the verb argument is missing,
    or the verb argument is repeated."""


class BadResumptionToken(OAIPMHException):
    """The value of the resumptionToken argument is invalid or expired."""


class CannotDisseminateFormat(OAIPMHException):
    """The metadata format identified by the value given for the metadataPrefix argument
    is not supported by the item or by the repository."""


class IdDoesNotExist(OAIPMHException):
    """The value of the identifier argument is unknown or illegal in this repository."""


class NoSetHierarchy(OAIPMHException):
    """The repository does not support sets."""


class NoMetadataFormat(OAIPMHException):
    """There are no metadata formats available for the specified item."""


class NoRecordsMatch(OAIPMHException):
    """The combination of the values of the from, until, set and metadataPrefix arguments results in an empty list."""


class GeneralOAIPMHError(OAIPMHException):
    """General exception for context-specific OAI-PMH errors not covered by the other specific classes."""
