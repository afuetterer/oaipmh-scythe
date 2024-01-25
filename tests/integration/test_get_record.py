# SPDX-FileCopyrightText: 2023 Heinz-Alexander Fütterer
#
# SPDX-License-Identifier: BSD-3-Clause

from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from oaipmh_scythe import BadArgument, IdDoesNotExist
from oaipmh_scythe.models import Record

if TYPE_CHECKING:
    from oaipmh_scythe import Scythe

IDENTIFIER = "oai:zenodo.org:10357859"
TITLE = "Research Data Management Organiser (RDMO)"


@pytest.mark.default_cassette("get_record.yaml")
@pytest.mark.vcr()
def test_get_record_with_default_metadata_prefix(scythe: Scythe) -> None:
    record = scythe.get_record(identifier=IDENTIFIER, metadata_prefix="oai_dc")
    assert isinstance(record, Record)
    assert record.metadata.other_element.title[0].value == TITLE


@pytest.mark.default_cassette("get_record.yaml")
@pytest.mark.vcr()
def test_get_record_without_metadata_prefix(scythe: Scythe) -> None:
    record = scythe.get_record(identifier=IDENTIFIER)
    assert isinstance(record, Record)
    assert record.metadata.other_element.title[0].value == TITLE


@pytest.mark.default_cassette("get_record.yaml")
@pytest.mark.vcr
def test_get_record_with_datacite_metadata_prefix(scythe: Scythe) -> None:
    record = scythe.get_record(identifier=IDENTIFIER, metadata_prefix="datacite")
    assert isinstance(record, Record)
    assert record.metadata.other_element.titles.title[0].value == TITLE


@pytest.mark.default_cassette("get_record.yaml")
@pytest.mark.vcr
def test_get_record_with_marcxml_metadata_prefix(scythe: Scythe) -> None:
    record = scythe.get_record(identifier=IDENTIFIER, metadata_prefix="marcxml")
    assert isinstance(record, Record)
    controlfield = record.metadata.other_element.controlfield[0]
    assert controlfield.value == "10357859"
    assert controlfield.tag == "001"


@pytest.mark.default_cassette("get_record.yaml")
@pytest.mark.vcr
def test_get_record_with_invalid_metadata_prefix(scythe: Scythe) -> None:
    with pytest.raises(BadArgument, match="metadataPrefix does not exist"):
        scythe.get_record(identifier=IDENTIFIER, metadata_prefix="XXX")


@pytest.mark.default_cassette("id_does_not_exist.yaml")
@pytest.mark.vcr
def test_get_record_with_invalid_identifier(scythe: Scythe) -> None:
    with pytest.raises(IdDoesNotExist, match="No matching identifier"):
        scythe.get_record(identifier="oai:zenodo.org:XXX", metadata_prefix="oai_dc")
