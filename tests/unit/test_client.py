# SPDX-FileCopyrightText: 2015 Mathias Loesch
#
# SPDX-License-Identifier: BSD-3-Clause

from __future__ import annotations

from contextlib import suppress
from typing import TYPE_CHECKING

import pytest
from httpx import HTTPStatusError, Response

from oaipmh_scythe import Scythe

if TYPE_CHECKING:
    from respx.router import MockRouter


params = {"verb": "ListIdentifiers", "metadataPrefix": "oai_dc"}


def test_invalid_http_method() -> None:
    with pytest.raises(ValueError):
        Scythe("https://localhost", http_method="DELETE")


def test_wrong_protocol_version() -> None:
    with pytest.raises(ValueError):
        Scythe("https://localhost", protocol_version="3.0")


def test_invalid_iterator() -> None:
    with pytest.raises(TypeError):
        Scythe("https://localhost", iterator=None)  # type: ignore [arg-type]


def test_wrong_is_error_code(scythe: Scythe) -> None:
    assert not scythe._is_error_code(200)
    assert scythe._is_error_code(400)


def test_override_encoding(scythe: Scythe, respx_mock: MockRouter) -> None:
    mock_route = respx_mock.get("https://zenodo.org/oai2d?metadataPrefix=oai_dc&verb=ListIdentifiers").mock(
        return_value=Response(200)
    )
    scythe.encoding = "custom-encoding"
    oai_response = scythe.harvest(**params)
    assert mock_route.called
    assert oai_response.http_response.encoding == "custom-encoding"


def test_post_method(scythe: Scythe, respx_mock: MockRouter) -> None:
    mock_route = respx_mock.post("https://zenodo.org/oai2d").mock(return_value=Response(200))
    scythe.http_method = "POST"
    oai_response = scythe.harvest(**params)
    assert mock_route.called
    assert oai_response.http_response.status_code == 200


def test_no_retry(scythe: Scythe, respx_mock: MockRouter) -> None:
    mock_route = respx_mock.get("https://zenodo.org/oai2d?metadataPrefix=oai_dc&verb=ListIdentifiers").mock(
        return_value=Response(503)
    )
    with suppress(HTTPStatusError):
        scythe.harvest(**params)
    assert mock_route.call_count == 1


def test_retry_on_503(scythe: Scythe, respx_mock: MockRouter, mocker) -> None:
    scythe.max_retries = 3
    scythe.default_retry_after = 0
    mock_sleep = mocker.patch("time.sleep")
    mock_route = respx_mock.get("https://zenodo.org/oai2d?metadataPrefix=oai_dc&verb=ListIdentifiers").mock(
        return_value=Response(503, headers={"retry-after": "10"})
    )
    with suppress(HTTPStatusError):
        scythe.harvest(**params)
    assert mock_route.call_count == 4
    assert mock_sleep.call_count == 3
    mock_sleep.assert_called_with(10)


def test_retry_on_503_without_retry_after_header(scythe: Scythe, respx_mock: MockRouter, mocker) -> None:
    scythe.max_retries = 3
    scythe.default_retry_after = 0
    mock_sleep = mocker.patch("time.sleep")
    mock_route = respx_mock.get("https://zenodo.org/oai2d?metadataPrefix=oai_dc&verb=ListIdentifiers").mock(
        return_value=Response(503, headers=None)
    )
    with suppress(HTTPStatusError):
        scythe.harvest(**params)
    assert mock_route.call_count == 4
    assert mock_sleep.call_count == 3


def test_retry_on_custom_code(scythe: Scythe, respx_mock: MockRouter, mocker) -> None:
    mock_route = respx_mock.get("https://zenodo.org/oai2d?metadataPrefix=oai_dc&verb=ListIdentifiers").mock(
        return_value=Response(500)
    )
    scythe.max_retries = 3
    scythe.default_retry_after = 0
    mock_sleep = mocker.patch("time.sleep")
    scythe.retry_status_codes = (503, 500)
    with suppress(HTTPStatusError):
        scythe.harvest(**params)
    assert mock_route.call_count == 4
    assert mock_sleep.call_count == 3
