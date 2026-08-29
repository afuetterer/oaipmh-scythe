# SPDX-FileCopyrightText: 2026 Heinz-Alexander Fütterer
#
# SPDX-License-Identifier: BSD-3-Clause

"""The config module defines data structures for configuring the Scythe client.

This module includes configuration data classes that group related Scythe arguments,
simplifying the construction of the Scythe class.

Classes:
    RetryConfig: Groups the retry arguments controlling how failed requests are retried.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class RetryConfig:
    """A data class grouping the retry arguments of the Scythe client.

    The retry configuration controls how failed HTTP requests are retried. It determines the number
    of retries, the HTTP status codes that trigger a retry, and the default wait time between retries
    if the server does not provide a 'retry-after' header.

    Attributes:
        max_retries: The maximum number of retries for a request in case of failures. Default is 0 (no retries).
        retry_status_codes: The HTTP status codes on which to retry the request. Default is (503,).
        default_retry_after: The default wait time (in seconds) between retries if no 'retry-after' header is
            present. Default is 60.
    """

    max_retries: int = 0
    retry_status_codes: tuple[int, ...] = (503,)
    default_retry_after: float = 60

    def __post_init__(self) -> None:
        if self.max_retries < 0:
            raise ValueError(
                f"Invalid value for 'max_retries': {self.max_retries}. max_retries must be a non-negative int."
            )
        if self.default_retry_after <= 0:
            raise ValueError(
                f"Invalid value for 'default_retry_after': {self.default_retry_after}. "
                "default_retry_after must be positive int or float."
            )
