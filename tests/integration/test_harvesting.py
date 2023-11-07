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


@pytest.mark.default_cassette("identify.yaml")
@pytest.mark.vcr
def test_identify(scythe: Scythe) -> None:
    identify = scythe.identify()
    assert isinstance(identify, Identify)
    assert identify.repositoryName == "Zenodo"


@pytest.mark.default_cassette("list_identifiers.yaml")
@pytest.mark.vcr
def test_list_identifiers(scythe: Scythe) -> None:
    identifiers = scythe.list_identifiers(metadataPrefix="oai_dc")
    assert isinstance(identifiers, Iterator)
    identifier = next(identifiers)
    assert isinstance(identifier, Header)
    assert identifier.identifier == "oai:zenodo.org:6538892"


@pytest.mark.default_cassette("list_records.yaml")
@pytest.mark.vcr
def test_list_records(scythe: Scythe) -> None:
    records = scythe.list_records(metadataPrefix="oai_dc")
    assert isinstance(records, Iterator)
    record = next(records)
    assert isinstance(record, Record)
    assert record.metadata["title"][0] == "INFORMATION YOU KNOW AND DON'T KNOW ABOUT THE UNIVERSE"


@pytest.mark.default_cassette("get_record.yaml")
@pytest.mark.vcr
def test_get_record(scythe: Scythe) -> None:
    record = scythe.get_record(identifier="oai:zenodo.org:6538892", metadataPrefix="oai_dc")
    assert isinstance(record, Record)
    assert record.metadata["title"][0] == "INFORMATION YOU KNOW AND DON'T KNOW ABOUT THE UNIVERSE"


@pytest.mark.default_cassette("list_sets.yaml")
@pytest.mark.vcr
def test_list_sets(scythe: Scythe) -> None:
    sets = scythe.list_sets()
    assert isinstance(sets, Iterator)
    s = next(sets)
    assert isinstance(s, Set)
    assert s.setName == "European Middleware Initiative"


@pytest.mark.default_cassette("list_metadata_formats.yaml")
@pytest.mark.vcr
def test_list_metadata_formats(scythe: Scythe) -> None:
    metadata_formats = scythe.list_metadata_formats()
    assert isinstance(metadata_formats, Iterator)
    metadata_format = next(metadata_formats)
    assert isinstance(metadata_format, MetadataFormat)
    assert metadata_format.metadataPrefix == "marcxml"


@pytest.mark.default_cassette("list_identifiers.yaml")
@pytest.mark.vcr
def test_list_identifiers_oai_response(scythe: Scythe) -> None:
    scythe.iterator = OAIResponseIterator
    responses = scythe.list_identifiers(metadataPrefix="oai_dc")
    assert isinstance(responses, Iterator)
    response = next(responses)
    assert isinstance(response, OAIResponse)
    assert response.params == {"metadataPrefix": "oai_dc", "verb": "ListIdentifiers"}
    assert isinstance(response.xml, etree._Element)
    assert response.xml.tag == "{http://www.openarchives.org/OAI/2.0/}OAI-PMH"