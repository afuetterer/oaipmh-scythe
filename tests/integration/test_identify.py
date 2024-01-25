# SPDX-FileCopyrightText: 2023 Heinz-Alexander Fütterer
#
# SPDX-License-Identifier: BSD-3-Clause

from __future__ import annotations

import httpx
import pytest

from oaipmh_scythe import Response, Scythe
from oaipmh_scythe.iterator import ResponseIterator
from oaipmh_scythe.models import Identify


@pytest.mark.default_cassette("identify.yaml")
@pytest.mark.vcr
def test_close(scythe: Scythe) -> None:
    scythe.identify()
    scythe.close()


@pytest.mark.default_cassette("identify.yaml")
@pytest.mark.vcr
def test_context_manager() -> None:
    with Scythe("https://zenodo.org/oai2d") as scythe:
        scythe.identify()


@pytest.mark.default_cassette("identify.yaml")
@pytest.mark.vcr
def test_identify(scythe: Scythe) -> None:
    identify = scythe.identify()
    assert isinstance(identify, Identify)
    assert identify.repository_name == "Zenodo"


@pytest.mark.default_cassette("identify.yaml")
@pytest.mark.vcr()
def test_identify_response(scythe: Scythe) -> None:
    scythe.iterator = ResponseIterator
    response = scythe.identify()
    assert isinstance(response, Response)
    assert response.status_code == httpx.codes.OK
    assert response.url == httpx.URL("https://zenodo.org/oai2d?verb=Identify")


@pytest.mark.default_cassette("identify.yaml")
@pytest.mark.vcr
def test_non_oai_pmh_url() -> None:
    scythe = Scythe("https://duckduckgo.com/")
    with pytest.raises(ValueError, match="Unknown property {http://www.openarchives.org/OAI/2.0/}OAI-PMH:head"):
        scythe.identify()
    scythe.close()


def test_non_url() -> None:
    scythe = Scythe("XXX")
    with pytest.raises(httpx.UnsupportedProtocol):
        scythe.identify()
    scythe.close()
