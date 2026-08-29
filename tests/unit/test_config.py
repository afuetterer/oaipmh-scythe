# SPDX-FileCopyrightText: 2026 Heinz-Alexander Fütterer
#
# SPDX-License-Identifier: BSD-3-Clause

import pytest

from oaipmh_scythe import HTTPConfig, RetryConfig


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
