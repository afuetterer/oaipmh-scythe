# SPDX-FileCopyrightText: 2023 Heinz-Alexander Fütterer
#
# SPDX-License-Identifier: BSD-3-Clause

from __future__ import annotations

from collections.abc import Iterator
from typing import TYPE_CHECKING

import httpx
import pytest
from lxml import etree

from oaipmh_scythe.iterator import OAIResponseIterator
from oaipmh_scythe.models import Record
from oaipmh_scythe.response import OAIResponse

if TYPE_CHECKING:
    from oaipmh_scythe import Scythe

TITLE = "PocketCoffea: a configuration layer for CMS analyses with Coffea"


@pytest.mark.default_cassette("list_records.yaml")
@pytest.mark.vcr
def test_list_records_with_default_metadata_prefix(scythe: Scythe) -> None:
    records = scythe.list_records(metadata_prefix="oai_dc")
    assert isinstance(records, Iterator)
    record = next(records)
    assert isinstance(record, Record)
    assert record.metadata["title"][0] == TITLE


@pytest.mark.default_cassette("list_records.yaml")
@pytest.mark.vcr
def test_list_records_without_metadata_prefix(scythe: Scythe) -> None:
    records = scythe.list_records()
    assert isinstance(records, Iterator)
    record = next(records)
    assert isinstance(record, Record)
    assert record.metadata["title"][0] == TITLE


@pytest.mark.default_cassette("list_records.yaml")
@pytest.mark.vcr
def test_list_records_with_valid_metadata_prefix(scythe: Scythe) -> None:
    records = scythe.list_records(metadata_prefix="datacite")
    assert isinstance(records, Iterator)
    record = next(records)
    assert isinstance(record, Record)
    assert record.metadata["title"][0] == TITLE


@pytest.mark.default_cassette("list_records.yaml")
@pytest.mark.vcr
def test_list_records_with_invalid_metadata_prefix(scythe: Scythe) -> None:
    # cannotDisseminateFormat
    records = scythe.list_records(metadata_prefix="XXX")
    with pytest.raises(httpx.HTTPStatusError):
        next(records)


@pytest.mark.default_cassette("list_records.yaml")
@pytest.mark.vcr
def test_list_records_with_from(scythe: Scythe) -> None:
    records = scythe.list_records(from_="2026-04-01")
    assert isinstance(records, Iterator)
    record = next(records)
    expected_title = "Visual Summary (हिन्दी): चेचक वैश्विक (1994-2024)"
    assert record.metadata["title"][0] == expected_title


@pytest.mark.default_cassette("list_records.yaml")
@pytest.mark.vcr
def test_list_records_with_until(scythe: Scythe) -> None:
    records = scythe.list_records(until="2026-04-02")
    assert isinstance(records, Iterator)
    record = next(records)
    assert record.metadata["title"][0] == TITLE


@pytest.mark.default_cassette("list_records.yaml")
@pytest.mark.vcr
def test_list_records_with_from_and_until(scythe: Scythe) -> None:
    records = scythe.list_records(from_="2026-04-01", until="2026-04-02")
    record = next(records)
    expected_title = "Science, Systèmes et Cécité Structurelle👀"
    assert record.metadata["title"][0] == expected_title


@pytest.mark.default_cassette("list_records.yaml")
@pytest.mark.vcr
def test_list_records_with_valid_set(scythe: Scythe) -> None:
    records = scythe.list_records(set_="software")
    record = next(records)
    assert record.metadata["title"][0] == "Figure generation TCR self-reactivity"


@pytest.mark.default_cassette("list_records.yaml")
@pytest.mark.vcr
def test_list_records_with_invalid_set(scythe: Scythe) -> None:
    # noRecordsMatch
    records = scythe.list_records(set_="XXX")
    with pytest.raises(httpx.HTTPStatusError):
        next(records)


@pytest.mark.default_cassette("list_records.yaml")
@pytest.mark.vcr
def test_list_records_with_valid_resumption_token(scythe: Scythe) -> None:
    token = ".eJwtzNtugjAAANB"
    records = scythe.list_records(resumption_token=token)
    assert isinstance(records, Iterator)
    record = next(records)
    assert record


@pytest.mark.default_cassette("list_records.yaml")
@pytest.mark.vcr
def test_list_records_with_invalid_resumption_token(scythe: Scythe) -> None:
    # badResumptionToken
    records = scythe.list_records(resumption_token="XXX")
    with pytest.raises(httpx.HTTPStatusError):
        next(records)


@pytest.mark.default_cassette("list_records.yaml")
@pytest.mark.vcr
def test_list_records_raises_no_records_match(scythe: Scythe) -> None:
    # noRecordsMatch
    records = scythe.list_records(from_="2030-01-01")
    with pytest.raises(httpx.HTTPStatusError):
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
def test_list_records_oai_response(scythe: Scythe) -> None:
    scythe.iterator = OAIResponseIterator
    responses = scythe.list_records()
    assert isinstance(responses, Iterator)
    responses = list(responses)
    # there are 3 canned responses in list_records.yaml
    assert len(responses) == 3
    response = responses[0]
    assert isinstance(response, OAIResponse)
    assert response.params == {"metadataPrefix": "oai_dc", "verb": "ListRecords"}
    assert isinstance(response.xml, etree._Element)
    assert response.xml.tag == "{http://www.openarchives.org/OAI/2.0/}OAI-PMH"
