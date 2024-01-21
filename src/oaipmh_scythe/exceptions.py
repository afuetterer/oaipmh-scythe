# SPDX-FileCopyrightText: 2015 Mathias Loesch
# SPDX-FileCopyrightText: 2023 Heinz-Alexander Fütterer
#
# SPDX-License-Identifier: BSD-3-Clause

"""The exceptions module defines exception classes for handling error scenarios encountered in OAI-PMH operations.

These exception classes provide a structured way to capture and communicate specific errors that may occur
while interacting with OAI-PMH services. Each class corresponds to a particular type of error defined
in the OAI-PMH protocol, facilitating precise error handling and meaningful feedback in client applications.

Classes:
    OAIPMHException: The base exception class for all OAI-PMH related errors.
    GeneralOAIPMHError: A general exception class for OAI-PMH errors not specifically covered by other classes.
    BadArgument: Raised when a request contains illegal, missing, or improperly formatted arguments.
    BadVerb: Raised when the verb argument in a request is invalid or improperly used.
    BadResumptionToken: Raised when a resumption token is invalid or expired.
    CannotDisseminateFormat: Raised when a requested metadata format is not supported.
    IdDoesNotExist: Raised when an identifier does not exist or is illegal in a repository.
    NoSetHierarchy: Raised when a repository does not support set hierarchies.
    NoMetadataFormat: Raised when no metadata formats are available for an item.
    NoRecordsMatch: Raised when a query yields no results due to specific argument combinations.

These custom exceptions enhance the robustness and clarity of error handling in OAI-PMH client implementations,
aligning closely with the protocol's standard error conditions.

Ref: https://openarchives.org/OAI/openarchivesprotocol.html#ErrorConditions
"""


class OAIPMHException(Exception):
    """Base exception class for all OAI-PMH related errors."""


class BadArgument(OAIPMHException):
    """Exception raised when the OAI-PMH request contains illegal or missing arguments or arguments with illegal syntax.

    This includes scenarios where arguments are repeated, missing, have illegal values,
    or their syntax is not compliant with the OAI-PMH specifications.
    """


class BadVerb(OAIPMHException):
    """Exception raised when the verb argument in the OAI-PMH request is invalid.

    This occurs if the verb value is not a legal OAI-PMH verb, the verb argument is missing,
    or if the verb argument is repeated in the request.
    """


class BadResumptionToken(OAIPMHException):
    """Exception raised when the resumptionToken argument in the OAI-PMH request is invalid or expired.

    Indicates issues with the value of the resumptionToken, such as expiration or incorrect formatting.
    """


class CannotDisseminateFormat(OAIPMHException):
    """Exception raised when the requested metadata format is not supported.

    This error occurs if the metadata format identified by the metadataPrefix argument is not
    supported by either the requested item or the repository as a whole.
    """


class IdDoesNotExist(OAIPMHException):
    """Exception raised when the specified identifier is unknown or illegal in the repository.

    Indicates that the value of the identifier argument does not correspond to any item
    in the repository or is not formulated correctly.
    """


class NoSetHierarchy(OAIPMHException):
    """Exception raised when sets are not supported by the repository.

    This error indicates that the repository does not support the concept of set hierarchies.
    """


class NoMetadataFormat(OAIPMHException):
    """Exception raised when there are no available metadata formats for the specified item.

    Indicates a lack of metadata formats that can be disseminated for the requested item.
    """


class NoRecordsMatch(OAIPMHException):
    """Exception raised when a query does not yield any results.

    This error occurs when the combination of the 'from', 'until', 'set', and 'metadataPrefix'
    arguments in a request results in an empty list, indicating no matching records.
    """


class GeneralOAIPMHError(OAIPMHException):
    """General exception for context-specific OAI-PMH errors not covered by the other specific classes.

    This class is used for OAI-PMH errors that do not fall into the predefined categories
    of the other exception classes in this module.
    """
