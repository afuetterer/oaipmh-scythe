# SPDX-FileCopyrightText: 2015 Mathias Loesch
#
# SPDX-License-Identifier: BSD-3-Clause

from __future__ import annotations

from collections.abc import Iterator

import pytest
from lxml import etree

from oaipmh_scythe import OAIResponse, Scythe
from oaipmh_scythe.iterator import OAIResponseIterator
from oaipmh_scythe.models import Header, Identify, MetadataFormat, Record, Set


@pytest.fixture
def harvester() -> Scythe:
    return Scythe("https://zenodo.org/oai2d")


@pytest.mark.vcr
def test_identify(harvester: Scythe) -> None:
    identify = harvester.identify()
    assert isinstance(identify, Identify)
    assert identify.repositoryName == "Zenodo"


@pytest.mark.vcr
def test_list_identifiers(harvester: Scythe) -> None:
    identifiers = harvester.list_identifiers(metadataPrefix="oai_dc")
    assert isinstance(identifiers, Iterator)
    identifier = next(identifiers)
    assert isinstance(identifier, Header)
    assert identifier.identifier == "oai:zenodo.org:6538892"


@pytest.mark.vcr
def test_list_records(harvester: Scythe) -> None:
    records = harvester.list_records(metadataPrefix="oai_dc")
    assert isinstance(records, Iterator)
    record = next(records)
    assert isinstance(record, Record)
    assert record.metadata["title"][0] == "INFORMATION YOU KNOW AND DON'T KNOW ABOUT THE UNIVERSE"


@pytest.mark.vcr
def test_get_record(harvester: Scythe) -> None:
    record = harvester.get_record(identifier="oai:zenodo.org:6538892", metadataPrefix="oai_dc")
    assert isinstance(record, Record)
    assert record.metadata["title"][0] == "INFORMATION YOU KNOW AND DON'T KNOW ABOUT THE UNIVERSE"


@pytest.mark.vcr
def test_list_sets(harvester: Scythe) -> None:
    sets = harvester.list_sets()
    assert isinstance(sets, Iterator)
    s = next(sets)
    assert isinstance(s, Set)
    assert s.setName == "European Middleware Initiative"


@pytest.mark.vcr
def test_list_metadata_formats(harvester: Scythe) -> None:
    metadata_formats = harvester.list_metadata_formats()
    assert isinstance(metadata_formats, Iterator)
    metadata_format = next(metadata_formats)
    assert isinstance(metadata_format, MetadataFormat)
    assert metadata_format.metadataPrefix == "marcxml"


@pytest.mark.vcr
def test_list_identifiers_oai_response(harvester: Scythe) -> None:
    harvester.iterator = OAIResponseIterator
    responses = harvester.list_identifiers(metadataPrefix="oai_dc")
    assert isinstance(responses, Iterator)
    response = next(responses)
    assert isinstance(response, OAIResponse)
    assert response.params == {"metadataPrefix": "oai_dc", "verb": "ListIdentifiers"}
    assert isinstance(response.xml, etree._Element)
    assert response.xml.tag == "{http://www.openarchives.org/OAI/2.0/}OAI-PMH"
