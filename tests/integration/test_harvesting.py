# SPDX-FileCopyrightText: 2015 Mathias Loesch
# SPDX-FileCopyrightText: 2023 Heinz-Alexander Fütterer
#
# SPDX-License-Identifier: BSD-3-Clause

from __future__ import annotations

from collections.abc import Iterator

import pytest
from httpx import HTTPStatusError
from lxml import etree

from oaipmh_scythe import OAIResponse, Scythe
from oaipmh_scythe.iterator import OAIResponseIterator
from oaipmh_scythe.models import Header, Identify, MetadataFormat, Record, Set


@pytest.mark.default_cassette("identify.yaml")
@pytest.mark.vcr()
def test_identify(scythe: Scythe) -> None:
    identify = scythe.identify()
    assert isinstance(identify, Identify)
    assert identify.repositoryName == "Zenodo"


@pytest.mark.default_cassette("identify.yaml")
@pytest.mark.vcr()
def test_close(scythe: Scythe) -> None:
    scythe.identify()
    scythe.close()


@pytest.mark.default_cassette("identify.yaml")
@pytest.mark.vcr()
def test_context_manager() -> None:
    with Scythe("https://zenodo.org/oai2d") as scythe:
        scythe.identify()


@pytest.mark.default_cassette("list_identifiers.yaml")
@pytest.mark.vcr()
def test_list_identifiers(scythe: Scythe) -> None:
    identifiers = scythe.list_identifiers(metadataPrefix="oai_dc")
    assert isinstance(identifiers, Iterator)
    identifier = next(identifiers)
    assert isinstance(identifier, Header)
    assert identifier.identifier == "oai:zenodo.org:6538892"


@pytest.mark.default_cassette("list_identifiers.yaml")
@pytest.mark.vcr()
def test_list_identifiers_ignore_deleted(scythe: Scythe) -> None:
    identifiers = scythe.list_identifiers(metadataPrefix="oai_dc", ignore_deleted=True)
    identifiers = list(identifiers)
    # there are 15 canned responses in list_identifiers.yaml
    # one of them is manually set to "status=deleted"
    assert len(identifiers) == 14


@pytest.mark.default_cassette("list_records.yaml")
@pytest.mark.vcr()
def test_list_records(scythe: Scythe) -> None:
    records = scythe.list_records(metadataPrefix="oai_dc")
    assert isinstance(records, Iterator)
    record = next(records)
    assert isinstance(record, Record)
    assert record.metadata["title"][0] == "INFORMATION YOU KNOW AND DON'T KNOW ABOUT THE UNIVERSE"


@pytest.mark.default_cassette("get_record.yaml")
@pytest.mark.vcr()
def test_get_record(scythe: Scythe) -> None:
    record = scythe.get_record(identifier="oai:zenodo.org:10357859", metadataPrefix="oai_dc")
    assert isinstance(record, Record)
    assert record.metadata["title"][0] == "Research Data Management Organiser (RDMO)"


@pytest.mark.default_cassette("get_record.yaml")
@pytest.mark.vcr()
def test_get_record_with_other_metadata_prefix(scythe: Scythe) -> None:
    record = scythe.get_record(identifier="oai:zenodo.org:10357859", metadataPrefix="datacite")
    assert isinstance(record, Record)
    assert record.metadata["title"][0] == "Research Data Management Organiser (RDMO)"


@pytest.mark.default_cassette("id_does_not_exist.yaml")
@pytest.mark.vcr()
def test_get_record_invalid_id(scythe: Scythe) -> None:
    with pytest.raises(HTTPStatusError):
        scythe.get_record(identifier="oai:zenodo.org:XXX", metadataPrefix="oai_dc")


@pytest.mark.default_cassette("list_sets.yaml")
@pytest.mark.vcr()
def test_list_sets(scythe: Scythe) -> None:
    sets = scythe.list_sets()
    assert isinstance(sets, Iterator)
    s = next(sets)
    assert isinstance(s, Set)
    assert s.setName == "European Middleware Initiative"


@pytest.mark.default_cassette("list_metadata_formats.yaml")
@pytest.mark.vcr()
def test_list_metadata_formats(scythe: Scythe) -> None:
    metadata_formats = scythe.list_metadata_formats()
    assert isinstance(metadata_formats, Iterator)
    metadata_format = next(metadata_formats)
    assert isinstance(metadata_format, MetadataFormat)
    assert metadata_format.metadataPrefix == "marcxml"


@pytest.mark.default_cassette("list_identifiers.yaml")
@pytest.mark.vcr()
def test_list_identifiers_oai_response(scythe: Scythe) -> None:
    scythe.iterator = OAIResponseIterator
    responses = scythe.list_identifiers(metadataPrefix="oai_dc")
    assert isinstance(responses, Iterator)
    response = next(responses)
    assert isinstance(response, OAIResponse)
    assert response.params == {"metadataPrefix": "oai_dc", "verb": "ListIdentifiers"}
    assert isinstance(response.xml, etree._Element)
    assert response.xml.tag == "{http://www.openarchives.org/OAI/2.0/}OAI-PMH"
