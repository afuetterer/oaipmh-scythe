# SPDX-FileCopyrightText: 2023 Heinz-Alexander Fuetterer
#
# SPDX-License-Identifier: BSD-3-Clause

from __future__ import annotations

from typing import TYPE_CHECKING

import pytest
from lxml import etree

from oaipmh_scythe.response import OAIResponse

if TYPE_CHECKING:
    from pytest_mock import MockerFixture


IDENTIFY_XML: str = """
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


@pytest.fixture()
def mock_response(mocker: MockerFixture):
    response = mocker.Mock()
    response.text = IDENTIFY_XML
    response.content = response.text.encode()
    return response


def test_oai_response_raw(mock_response) -> None:
    params = {"verb": "Identify"}
    oai_response = OAIResponse(http_response=mock_response, params=params)
    assert oai_response.raw == mock_response.text


def test_oai_response_xml(mock_response):
    params = {"verb": "Identify"}
    oai_response = OAIResponse(http_response=mock_response, params=params)
    assert isinstance(oai_response.xml, etree._Element)
    assert oai_response.xml.tag == "{http://www.openarchives.org/OAI/2.0/}OAI-PMH"


def test_oai_response_str(mock_response):
    params = {"verb": "Identify"}
    oai_response = OAIResponse(http_response=mock_response, params=params)
    assert str(oai_response) == "<OAIResponse Identify>"
