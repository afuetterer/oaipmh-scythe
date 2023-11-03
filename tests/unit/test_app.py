# SPDX-FileCopyrightText: 2015 Mathias Loesch
#
# SPDX-License-Identifier: BSD-3-Clause

from __future__ import annotations

from contextlib import suppress
from typing import TYPE_CHECKING

import pytest
from httpx import HTTPStatusError

from oaipmh_scythe import Scythe

if TYPE_CHECKING:
    from unittest.mock import MagicMock, Mock

    from pytest_mock.plugin import MockerFixture


def test_invalid_http_method() -> None:
    with pytest.raises(ValueError):
        Scythe("https://localhost", http_method="DELETE")


def test_wrong_protocol_version() -> None:
    with pytest.raises(ValueError):
        Scythe("https://localhost", protocol_version="3.0")


def test_invalid_iterator() -> None:
    with pytest.raises(TypeError):
        Scythe("https://localhost", iterator=None)  # type: ignore [arg-type]


@pytest.fixture
def mock_response_200(mocker: MockerFixture) -> Mock:
    return mocker.Mock(text="<xml/>", content="<xml/>", status_code=200)


@pytest.fixture
def mock_response_503(mocker: MockerFixture) -> Mock:
    return mocker.Mock(
        status_code=503,
        headers={"retry-after": "10"},
        raise_for_status=mocker.Mock(side_effect=HTTPStatusError(message="500", request="500", response="500")),
    )


@pytest.fixture
def mock_get(mocker: MockerFixture) -> MagicMock:
    return mocker.patch("oaipmh_scythe.scythe.httpx.get")


def test_pass_request_args(mock_get: MagicMock, mock_response_200: Mock) -> None:
    mock_get.return_value = mock_response_200
    params = {"timeout": 10, "proxies": {}, "auth": ("user", "password")}
    harvester = Scythe("url", **params)
    records = harvester.list_records()
    records = list(records)
    mock_get.assert_called_once_with("url", params={"verb": "ListRecords"}, **params)


def test_override_encoding(mock_get: MagicMock, mock_response_200: Mock) -> None:
    mock_get.return_value = mock_response_200
    harvester = Scythe("url", encoding="encoding")
    sets = harvester.list_sets()
    sets = list(sets)
    mock_get.assert_called_once_with("url", params={"verb": "ListSets"}, timeout=60)


def test_post_request(mocker: MockerFixture) -> None:
    mock_post = mocker.patch("oaipmh_scythe.scythe.httpx.post")
    harvester = Scythe("url", encoding="encoding")
    harvester.http_method = "POST"
    params = {"verb": "ListSets"}
    harvester.harvest(**params)
    mock_post.assert_called_once_with("url", data=params, timeout=60)


def test_422(mock_get: MagicMock, mocker) -> None:
    mock_response_422 = mocker.Mock(text="<xml/>", content="<xml/>", status_code=422)
    mock_get.return_value = mock_response_422
    harvester = Scythe("url", max_retries=1)
    invalid_oaid = "id"
    harvester.harvest(identifier=invalid_oaid)
    assert mock_get.call_count == 1
    mock_response_422.raise_for_status.assert_called_once()


def test_no_retry(mock_get: MagicMock, mock_response_503: Mock) -> None:
    mock_get.return_value = mock_response_503
    harvester = Scythe("url")
    with suppress(HTTPStatusError):
        records = harvester.list_records()
        records = list(records)
    assert mock_get.call_count == 1
    mock_response_503.raise_for_status.assert_called_once()


def test_retry_on_503(mocker: MockerFixture, mock_get: MagicMock, mock_response_503: Mock) -> None:
    mock_get.return_value = mock_response_503
    harvester = Scythe("url", max_retries=3, default_retry_after=0)
    mock_sleep = mocker.patch("time.sleep")
    with suppress(HTTPStatusError):
        records = harvester.list_records()
        records = list(records)
    assert mock_get.call_count == 4
    assert mock_sleep.call_count == 3
    mock_sleep.assert_called_with(10)


def test_retry_on_503_withour_retry_after_header(
    mocker: MockerFixture, mock_get: MagicMock, mock_response_503: Mock
) -> None:
    mock_get.return_value = mock_response_503
    mock_response_503.headers = {}
    harvester = Scythe("url", max_retries=3, default_retry_after=0)
    mock_sleep = mocker.patch("time.sleep")
    with suppress(HTTPStatusError):
        records = harvester.list_records()
        records = list(records)
    assert mock_get.call_count == 4
    assert mock_sleep.call_count == 3


def test_retry_on_custom_code(mocker: MockerFixture, mock_get: MagicMock) -> None:
    mock_response_500 = mocker.Mock(
        status_code=500,
        raise_for_status=mocker.Mock(side_effect=HTTPStatusError(message="500", request="500", response="500")),
    )
    mock_get.return_value = mock_response_500
    harvester = Scythe("url", max_retries=3, default_retry_after=0, retry_status_codes=(503, 500))
    with suppress(HTTPStatusError):
        records = harvester.list_records()
        records = list(records)
    mock_get.assert_called_with("url", params={"verb": "ListRecords"}, timeout=60)
    assert mock_get.call_count == 4


@pytest.mark.filterwarnings("ignore::DeprecationWarning")
def test_deprecated_methods(harvester: Scythe):
    harvester.Identify()
    harvester.GetRecord()
    harvester.ListIdentifiers()
    harvester.ListMetadataFormats()
    harvester.ListRecords()
    harvester.ListSets()
