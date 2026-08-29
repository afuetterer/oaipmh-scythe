# SPDX-FileCopyrightText: 2026 Heinz-Alexander Fütterer
#
# SPDX-License-Identifier: BSD-3-Clause

import pytest

from oaipmh_scythe import RetryConfig


@pytest.mark.parametrize("retry_after", [-1, -1.0, 0, 0.0])
def test_invalid_default_retry_after(retry_after: float) -> None:
    with pytest.raises(ValueError, match="Invalid value for 'default_retry_after'"):
        RetryConfig(default_retry_after=retry_after)


def test_invalid_max_retries() -> None:
    with pytest.raises(ValueError, match="Invalid value for 'max_retries'"):
        RetryConfig(max_retries=-1)
