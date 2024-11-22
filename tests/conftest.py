# SPDX-FileCopyrightText: 2023 Heinz-Alexander Fütterer
#
# SPDX-License-Identifier: BSD-3-Clause

from __future__ import annotations

import httpx
import pytest

from oaipmh_scythe import Scythe


@pytest.fixture(scope="session")
def vcr_config() -> dict[str, str]:
    return {"cassette_library_dir": "tests/cassettes"}


@pytest.fixture
def scythe() -> Scythe:
    return Scythe("https://zenodo.org/oai2d")


@pytest.fixture
def identify_response() -> httpx.Response:
    identify_response_xml = """
    <OAI-PMH xmlns="http://www.openarchives.org/OAI/2.0/"
             xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
        <responseDate>2023-11-09T09:53:46Z</responseDate>
        <request verb="Identify">https://zenodo.org/oai2d</request>
        <Identify>
            <repositoryName>Zenodo</repositoryName>
            <baseURL>https://zenodo.org/oai2d</baseURL>
            <protocolVersion>2.0</protocolVersion>
        </Identify>
    </OAI-PMH>
    """
    return httpx.Response(
        status_code=httpx.codes.OK,
        content=identify_response_xml,
        request=httpx.Request(method="GET", url="https://zenodo.org/oai2d?verb=Identify"),
    )
