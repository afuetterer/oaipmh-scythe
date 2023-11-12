# SPDX-FileCopyrightText: 2023 Heinz-Alexander Fuetterer
#
# SPDX-License-Identifier: BSD-3-Clause

from __future__ import annotations

import pytest

from oaipmh_scythe import Scythe


@pytest.fixture(scope="session")
def vcr_config() -> dict[str, str]:
    return {"cassette_library_dir": "tests/cassettes"}


@pytest.fixture
def scythe() -> Scythe:
    return Scythe("https://zenodo.org/oai2d")
