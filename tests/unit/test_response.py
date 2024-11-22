# SPDX-FileCopyrightText: 2023 Heinz-Alexander Fütterer
#
# SPDX-License-Identifier: BSD-3-Clause

from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from oaipmh_scythe import IdDoesNotExist
from oaipmh_scythe.models import Identify, OaiPmh
from oaipmh_scythe.models.oai_pmh import OaiPmherror, OaiPmherrorcode
from oaipmh_scythe.response import Response, _build_response, raise_for_error

if TYPE_CHECKING:
    import httpx


def test_build_response(identify_response: httpx.Response) -> None:
    response = _build_response(identify_response, metadata_prefix="oai_dc")
    assert isinstance(response, Response)
    assert isinstance(response.parsed, OaiPmh)
    assert response.status_code == identify_response.status_code
    assert response.content == identify_response.content
    assert isinstance(response.parsed.identify, Identify)
    assert response.parsed.identify.repository_name == "Zenodo"


def test_raise_for_error_no_errors() -> None:
    assert raise_for_error(None) is None


def test_raise_for_error() -> None:
    error = OaiPmherror(code=OaiPmherrorcode.ID_DOES_NOT_EXIST, value="No matching identifier")
    with pytest.raises(IdDoesNotExist):
        raise_for_error([error])
