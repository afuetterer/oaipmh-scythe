# SPDX-FileCopyrightText: 2023 Heinz-Alexander Fütterer
#
# SPDX-License-Identifier: BSD-3-Clause

from __future__ import annotations

from collections.abc import Iterator
from typing import TYPE_CHECKING

import httpx
import pytest

from oaipmh_scythe import BadArgument, BadResumptionToken, NoRecordsMatch
from oaipmh_scythe.iterator import ResponseIterator
from oaipmh_scythe.models import Record
from oaipmh_scythe.response import Response

if TYPE_CHECKING:
    from oaipmh_scythe import Scythe

TITLE_1 = "Some Remarkable Oxidation-Products of Benzidine"
TITLE_2 = "Déclaration N°9 de La Nouvelle Donne: Tel est pris qui croyait prendre…"  # spellchecker:disable-line


@pytest.mark.default_cassette("list_records.yaml")
@pytest.mark.vcr
def test_list_records_with_default_metadata_prefix(scythe: Scythe) -> None:
    records = scythe.list_records(metadata_prefix="oai_dc")
    assert isinstance(records, Iterator)
    record = next(records)
    assert isinstance(record, Record)
    assert record.metadata.other_element.title[0].value == TITLE_1


@pytest.mark.default_cassette("list_records.yaml")
@pytest.mark.vcr
def test_list_records_without_metadata_prefix(scythe: Scythe) -> None:
    records = scythe.list_records()
    assert isinstance(records, Iterator)
    record = next(records)
    assert isinstance(record, Record)
    assert record.metadata.other_element.title[0].value == TITLE_1


@pytest.mark.default_cassette("list_records.yaml")
@pytest.mark.vcr
def test_list_records_with_valid_metadata_prefix(scythe: Scythe) -> None:
    records = scythe.list_records(metadata_prefix="datacite")
    assert isinstance(records, Iterator)
    record = next(records)
    assert isinstance(record, Record)
    assert record.metadata.other_element.titles.title[0].value == TITLE_1


@pytest.mark.default_cassette("list_records.yaml")
@pytest.mark.vcr
def test_list_records_with_invalid_metadata_prefix(scythe: Scythe) -> None:
    records = scythe.list_records(metadata_prefix="XXX")
    with pytest.raises(BadArgument, match="metadataPrefix does not exist"):
        next(records)


@pytest.mark.default_cassette("list_records.yaml")
@pytest.mark.vcr
def test_list_records_with_from(scythe: Scythe) -> None:
    records = scythe.list_records(from_="2024-01-16")
    assert isinstance(records, Iterator)
    record = next(records)
    assert record.metadata.other_element.title[0].value == TITLE_2


@pytest.mark.default_cassette("list_records.yaml")
@pytest.mark.vcr
def test_list_records_with_until(scythe: Scythe) -> None:
    records = scythe.list_records(until="2024-01-17")
    assert isinstance(records, Iterator)
    record = next(records)
    assert record.metadata.other_element.title[0].value == TITLE_1


@pytest.mark.default_cassette("list_records.yaml")
@pytest.mark.vcr
def test_list_records_with_from_and_until(scythe: Scythe) -> None:
    records = scythe.list_records(from_="2024-01-16", until="2024-01-17")
    record = next(records)
    assert record.metadata.other_element.title[0].value == TITLE_2


@pytest.mark.default_cassette("list_records.yaml")
@pytest.mark.vcr
def test_list_records_with_valid_set(scythe: Scythe) -> None:
    records = scythe.list_records(set_="software")
    record = next(records)
    assert record.metadata.other_element.title[0].value == "plasmo-dev/PlasmoExamples: Initial Release"


@pytest.mark.default_cassette("list_records.yaml")
@pytest.mark.vcr
def test_list_records_with_invalid_set(scythe: Scythe) -> None:
    records = scythe.list_records(set_="XXX")
    with pytest.raises(NoRecordsMatch):
        next(records)


@pytest.mark.default_cassette("list_records.yaml")
@pytest.mark.vcr
def test_list_records_with_valid_resumption_token(scythe: Scythe) -> None:
    token = "eJyNzE1vgjAcgPHv8j"
    records = scythe.list_records(resumption_token=token)
    assert isinstance(records, Iterator)
    record = next(records)
    assert isinstance(record, Record)


@pytest.mark.default_cassette("list_records.yaml")
@pytest.mark.vcr
def test_list_records_with_invalid_resumption_token(scythe: Scythe) -> None:
    records = scythe.list_records(resumption_token="XXX")
    with pytest.raises(BadResumptionToken, match="The value of the resumptionToken argument is invalid or expired."):
        next(records)


@pytest.mark.default_cassette("list_records.yaml")
@pytest.mark.vcr
def test_list_records_raises_no_records_match(scythe: Scythe) -> None:
    records = scythe.list_records(from_="2025-01-15")
    with pytest.raises(NoRecordsMatch):
        next(records)


@pytest.mark.default_cassette("list_records.yaml")
@pytest.mark.vcr
def test_list_records_ignore_deleted(scythe: Scythe) -> None:
    records = scythe.list_records(ignore_deleted=True)
    records = list(records)
    # there are 9 canned records in list_records.yaml
    # one of them is manually set to "status=deleted"
    assert len(records) == 8


@pytest.mark.default_cassette("list_records.yaml")
@pytest.mark.vcr
def test_list_records_response(scythe: Scythe) -> None:
    scythe.iterator = ResponseIterator
    _responses = scythe.list_records()
    assert isinstance(_responses, Iterator)
    responses = list(_responses)
    # there are 3 canned responses in list_records.yaml
    assert len(responses) == 3
    response = responses[0]
    assert isinstance(response, Response)
    assert response.status_code == httpx.codes.OK
    assert response.url == httpx.URL("https://zenodo.org/oai2d?verb=ListRecords&metadataPrefix=oai_dc")
