# SPDX-FileCopyrightText: 2026 Heinz-Alexander Fütterer
#
# SPDX-License-Identifier: BSD-3-Clause

"""The config module defines data structures for configuring the Scythe client.

This module includes configuration data classes that group related Scythe arguments,
simplifying the construction of the Scythe class.

Classes:
    HTTPConfig: Groups the HTTP arguments controlling how requests are made.
    RetryConfig: Groups the retry arguments controlling how failed requests are retried.
"""

from __future__ import annotations

from dataclasses import dataclass
from importlib.metadata import version
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from httpx2._types import AuthTypes


@dataclass
class HTTPConfig:
    """A data class grouping the HTTP arguments of the Scythe client.

    The HTTP configuration controls how requests are made. It determines the HTTP method, the request
    timeout, optional authentication credentials, the character encoding used for decoding responses,
    and the user agent string sent with every request.

    Attributes:
        http_method: The HTTP method to use for requests. Must be "GET" or "POST". Default is "GET".
        timeout: The timeout (in seconds) for HTTP requests. Default is 60.
        auth: Optional authentication credentials for accessing the OAI-PMH interface.
        encoding: The character encoding for decoding responses. Default is "utf-8".
        user_agent: The user agent string sent with every request. Defaults to "oaipmh-scythe/<version>".
    """

    http_method: str = "GET"
    timeout: float = 60
    auth: AuthTypes | None = None
    encoding: str = "utf-8"
    user_agent: str = f"oaipmh-scythe/{version('oaipmh-scythe')}"

    def __post_init__(self) -> None:
        if self.http_method not in {"GET", "POST"}:
            raise ValueError(f"Invalid value for 'http_method': {self.http_method}. Must be GET or POST.")
        if self.timeout <= 0:
            raise ValueError(f"Invalid value for 'timeout': {self.timeout}. Timeout must be positive int or float.")


@dataclass
class RetryConfig:
    """A data class grouping the retry arguments of the Scythe client.

    The retry configuration controls how failed HTTP requests are retried. It determines the number
    of retries, the HTTP status codes that trigger a retry, and the default wait time between retries
    if the server does not provide a 'retry-after' header. Optionally, requests failing with a transport
    error (e.g. connection failures or timeouts) can be retried using exponential backoff.

    Attributes:
        max_retries: The maximum number of retries for a request in case of failures. Default is 0 (no retries).
        retry_status_codes: The HTTP status codes on which to retry the request. Default is (503,).
        default_retry_after: The default wait time (in seconds) between retries if no 'retry-after' header is
            present. Default is 60.
        retry_on_transport_error: Whether to retry requests failing with a transport error (e.g. connection
            failures or timeouts). Default is False. Only effective if max_retries is greater than 0.
        initial_backoff: The initial wait time (in seconds) between retries after a transport error. The wait
            time doubles with each retry (exponential backoff), is capped at default_retry_after, and is
            randomized between 50% and 100% of the computed value (jitter). Default is 1.0.
    """

    max_retries: int = 0
    retry_status_codes: tuple[int, ...] = (503,)
    default_retry_after: float = 60
    retry_on_transport_error: bool = False
    initial_backoff: float = 1.0

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
        if self.initial_backoff <= 0:
            raise ValueError(
                f"Invalid value for 'initial_backoff': {self.initial_backoff}. "
                "initial_backoff must be positive int or float."
            )
