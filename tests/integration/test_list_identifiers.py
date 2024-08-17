# SPDX-FileCopyrightText: 2023 Heinz-Alexander Fütterer
#
# SPDX-License-Identifier: BSD-3-Clause

from __future__ import annotations

from collections.abc import Iterator

import httpx
import pytest
from lxml import etree

from oaipmh_scythe import OAIResponse, Scythe
from oaipmh_scythe.iterator import OAIResponseIterator
from oaipmh_scythe.models import Header


@pytest.mark.default_cassette("list_identifiers.yaml")
@pytest.mark.vcr
def test_list_identifiers_with_default_metadata_prefix(scythe: Scythe) -> None:
    headers = scythe.list_identifiers(metadata_prefix="oai_dc")
    assert isinstance(headers, Iterator)
    header = next(headers)
    assert isinstance(header, Header)
    assert header.identifier == "oai:zenodo.org:2217771"


@pytest.mark.default_cassette("list_identifiers.yaml")
@pytest.mark.vcr
def test_list_identifiers_without_metadata_prefix(scythe: Scythe) -> None:
    headers = scythe.list_identifiers()
    assert isinstance(headers, Iterator)
    header = next(headers)
    assert isinstance(header, Header)
    assert header.identifier == "oai:zenodo.org:2217771"


@pytest.mark.default_cassette("list_identifiers.yaml")
@pytest.mark.vcr
def test_list_identifiers_with_valid_metadata_prefix(scythe: Scythe) -> None:
    headers = scythe.list_identifiers(metadata_prefix="datacite")
    assert isinstance(headers, Iterator)
    header = next(headers)
    assert isinstance(header, Header)
    assert header.identifier == "oai:zenodo.org:2217771"


@pytest.mark.default_cassette("list_identifiers.yaml")
@pytest.mark.vcr
def test_list_identifiers_with_invalid_metadata_prefix(scythe: Scythe) -> None:
    # cannotDisseminateFormat
    headers = scythe.list_identifiers(metadata_prefix="XXX")
    with pytest.raises(httpx.HTTPStatusError):
        next(headers)


@pytest.mark.default_cassette("list_identifiers.yaml")
@pytest.mark.vcr
def test_list_identifiers_with_from(scythe: Scythe) -> None:
    headers = scythe.list_identifiers(from_="2024-01-16")
    assert isinstance(headers, Iterator)
    header = next(headers)
    assert header.identifier == "oai:zenodo.org:10516016"


@pytest.mark.default_cassette("list_identifiers.yaml")
@pytest.mark.vcr
def test_list_identifiers_with_until(scythe: Scythe) -> None:
    headers = scythe.list_identifiers(until="2024-01-17")
    assert isinstance(headers, Iterator)
    header = next(headers)
    assert header.identifier == "oai:zenodo.org:2217771"


@pytest.mark.default_cassette("list_identifiers.yaml")
@pytest.mark.vcr
def test_list_identifiers_with_from_and_until(scythe: Scythe) -> None:
    headers = scythe.list_identifiers(from_="2024-01-16", until="2024-01-17")
    header = next(headers)
    assert header.identifier == "oai:zenodo.org:10517528"


@pytest.mark.default_cassette("list_identifiers.yaml")
@pytest.mark.vcr
def test_list_identifiers_with_valid_set(scythe: Scythe) -> None:
    headers = scythe.list_identifiers(set_="software")
    header = next(headers)
    assert header.identifier == "oai:zenodo.org:32712"


@pytest.mark.default_cassette("list_identifiers.yaml")
@pytest.mark.vcr
def test_list_identifiers_with_invalid_set(scythe: Scythe) -> None:
    # noRecordsMatch
    headers = scythe.list_identifiers(set_="XXX")
    with pytest.raises(httpx.HTTPStatusError):
        next(headers)


@pytest.mark.default_cassette("list_identifiers.yaml")
@pytest.mark.vcr
def test_list_identifiers_with_valid_resumption_token(scythe: Scythe) -> None:
    token = "eJyNzt1ugjAYgOF7"
    headers = scythe.list_identifiers(resumption_token=token)
    assert isinstance(headers, Iterator)
    header = next(headers)
    assert header


@pytest.mark.default_cassette("list_identifiers.yaml")
@pytest.mark.vcr
def test_list_identifiers_with_invalid_resumption_token(scythe: Scythe) -> None:
    # badResumptionToken
    headers = scythe.list_identifiers(resumption_token="XXX")
    with pytest.raises(httpx.HTTPStatusError):
        next(headers)


@pytest.mark.default_cassette("list_identifiers.yaml")
@pytest.mark.vcr
def test_list_identifiers_raises_no_records_match(scythe: Scythe) -> None:
    # noRecordsMatch
    headers = scythe.list_identifiers(from_="2025-01-15")
    with pytest.raises(httpx.HTTPStatusError):
        next(headers)


@pytest.mark.default_cassette("list_identifiers.yaml")
@pytest.mark.vcr
def test_list_identifiers_ignore_deleted(scythe: Scythe) -> None:
    headers = scythe.list_identifiers(ignore_deleted=True)
    headers = list(headers)
    # there are 9 canned responses in list_identifiers.yaml
    # one of them is manually set to "status=deleted"
    assert len(headers) == 8


@pytest.mark.default_cassette("list_identifiers.yaml")
@pytest.mark.vcr
def test_list_identifiers_oai_response(scythe: Scythe) -> None:
    scythe.iterator = OAIResponseIterator
    responses = scythe.list_identifiers(metadata_prefix="oai_dc")
    assert isinstance(responses, Iterator)
    response = next(responses)
    assert isinstance(response, OAIResponse)
    assert response.params == {"metadataPrefix": "oai_dc", "verb": "ListIdentifiers"}
    assert isinstance(response.xml, etree._Element)
    assert response.xml.tag == "{http://www.openarchives.org/OAI/2.0/}OAI-PMH"
