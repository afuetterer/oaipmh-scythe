# SPDX-FileCopyrightText: 2023 Heinz-Alexander Fütterer
#
# SPDX-License-Identifier: BSD-3-Clause

from __future__ import annotations

from collections.abc import Iterator
from typing import TYPE_CHECKING

import pytest
from httpx import HTTPStatusError

from oaipmh_scythe.models import MetadataFormat

if TYPE_CHECKING:
    from oaipmh_scythe import Scythe


@pytest.mark.default_cassette("list_metadata_formats.yaml")
@pytest.mark.vcr
def test_list_metadata_formats(scythe: Scythe) -> None:
    metadata_formats = scythe.list_metadata_formats()
    assert isinstance(metadata_formats, Iterator)
    metadata_format = next(metadata_formats)
    assert isinstance(metadata_format, MetadataFormat)
    assert metadata_format.metadataPrefix == "marcxml"


@pytest.mark.default_cassette("list_metadata_formats.yaml")
@pytest.mark.vcr
def test_list_metadata_formats_with_valid_identifier(scythe: Scythe) -> None:
    metadata_formats = scythe.list_metadata_formats(identifier="oai:zenodo.org:10357859")
    assert isinstance(metadata_formats, Iterator)
    metadata_format = next(metadata_formats)
    assert isinstance(metadata_format, MetadataFormat)
    assert metadata_format.metadataPrefix == "marcxml"


@pytest.mark.default_cassette("list_metadata_formats.yaml")
@pytest.mark.vcr
def test_list_metadata_formats_with_invalid_identifier(scythe: Scythe) -> None:
    # idDoesNotExist
    metadata_formats = scythe.list_metadata_formats(identifier="oai:zenodo.org:XXX")
    with pytest.raises(HTTPStatusError):
        next(metadata_formats)
