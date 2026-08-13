# SPDX-FileCopyrightText: 2023 Heinz-Alexander Fütterer
#
# SPDX-License-Identifier: BSD-3-Clause

from __future__ import annotations

import pytest
from cassetter import Cassetter

from oaipmh_scythe import Scythe


@pytest.fixture(scope="session")
def vcr_config() -> Cassetter:
    return Cassetter(
        cassette_library_dir="tests/cassettes",
        record_mode="none",
        filter_headers=[
            "x-powered-by",
            "x-ratelimit-limit",
            "x-ratelimit-remaining",
            "x-ratelimit-reset",
            "via",
        ],
    )


@pytest.fixture
def scythe() -> Scythe:
    return Scythe("https://zenodo.org/oai2d")
