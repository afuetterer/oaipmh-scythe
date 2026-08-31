# SPDX-FileCopyrightText: 2026 Heinz-Alexander Fütterer
#
# SPDX-License-Identifier: BSD-3-Clause

from __future__ import annotations

from typing import TYPE_CHECKING

import httpx2
import pytest

from oaipmh_scythe import HTTPConfig, RetryConfig

if TYPE_CHECKING:
    from collections.abc import Iterable


@pytest.mark.parametrize("http_method", ["DELETE", "PATCH"])
def test_invalid_http_method(http_method: str) -> None:
    with pytest.raises(ValueError, match="Invalid value for 'http_method'"):
        HTTPConfig(http_method=http_method)


@pytest.mark.parametrize("timeout", [-1, -1.0, 0, 0.0])
def test_invalid_timeout(timeout: float) -> None:
    with pytest.raises(ValueError, match="Invalid value for 'timeout'"):
        HTTPConfig(timeout=timeout)


def test_default_user_agent() -> None:
    assert HTTPConfig().user_agent.startswith("oaipmh-scythe/")


@pytest.mark.parametrize("retry_after", [-1, -1.0, 0, 0.0])
def test_invalid_default_retry_after(retry_after: float) -> None:
    with pytest.raises(ValueError, match="Invalid value for 'default_retry_after'"):
        RetryConfig(default_retry_after=retry_after)


def test_invalid_max_retries() -> None:
    with pytest.raises(ValueError, match="Invalid value for 'max_retries'"):
        RetryConfig(max_retries=-1)


@pytest.mark.parametrize("initial_backoff", [-1, -1.0, 0, 0.0])
def test_invalid_initial_backoff(initial_backoff: float) -> None:
    with pytest.raises(ValueError, match="Invalid value for 'initial_backoff'"):
        RetryConfig(initial_backoff=initial_backoff)


@pytest.mark.parametrize(
    "codes",
    [
        [500, 502, 503],
        (500, 502, 503),
        {500, 502, 503},
        [httpx2.codes.INTERNAL_SERVER_ERROR, httpx2.codes.BAD_GATEWAY, httpx2.codes.SERVICE_UNAVAILABLE],
    ],
)
def test_normalize_retry_codes_valid(codes: Iterable[int]) -> None:
    retry_config = RetryConfig(retry_status_codes=codes)  # ty: ignore[invalid-argument-type]
    assert retry_config.retry_status_codes == {
        httpx2.codes.INTERNAL_SERVER_ERROR,
        httpx2.codes.BAD_GATEWAY,
        httpx2.codes.SERVICE_UNAVAILABLE,
    }


def test_normalize_retry_codes_invalid() -> None:
    with pytest.raises(ValueError, match="Invalid HTTP status code: 999"):
        RetryConfig(retry_status_codes={999})


def test_normalize_retry_codes_default() -> None:
    retry_config = RetryConfig()
    assert retry_config.retry_status_codes == {httpx2.codes.SERVICE_UNAVAILABLE}
