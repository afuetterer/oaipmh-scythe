# SPDX-FileCopyrightText: 2023 Heinz-Alexander Fütterer
#
# SPDX-License-Identifier: BSD-3-Clause

from __future__ import annotations

import httpx2
import pytest

from oaipmh_scythe import Scythe
from oaipmh_scythe.models import Identify


@pytest.mark.vcr("identify.yaml")
def test_close(scythe: Scythe) -> None:
    scythe.identify()
    scythe.close()


@pytest.mark.vcr("identify.yaml")
def test_context_manager() -> None:
    with Scythe("https://zenodo.org/oai2d") as scythe:
        scythe.identify()


@pytest.mark.vcr("identify.yaml")
def test_identify(scythe: Scythe) -> None:
    identify = scythe.identify()
    assert isinstance(identify, Identify)
    assert identify.repositoryName == "Zenodo"


@pytest.mark.vcr("identify.yaml")
def test_non_oai_pmh_url() -> None:
    scythe = Scythe("https://httpbun.com/html")
    with pytest.raises(ValueError, match="Identify element not found in the XML"):
        scythe.identify()
    scythe.close()


def test_non_url() -> None:
    scythe = Scythe("XXX")
    with pytest.raises(httpx2.UnsupportedProtocol):
        scythe.identify()
    scythe.close()


@pytest.mark.vcr("identify.yaml")
def test_server_with_application_xml_header() -> None:
    with Scythe("https://www.e-periodica.ch/oai/dataprovider") as scythe:
        scythe.identify()
