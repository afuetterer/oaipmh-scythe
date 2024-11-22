# SPDX-FileCopyrightText: 2015 Mathias Loesch
# SPDX-FileCopyrightText: 2023 Heinz-Alexander Fütterer
#
# SPDX-License-Identifier: BSD-3-Clause

from __future__ import annotations

from collections.abc import Iterator
from contextlib import suppress
from typing import TYPE_CHECKING

import httpx
import pytest

from oaipmh_scythe import CannotDisseminateFormat, NoSetHierarchy, Scythe
from oaipmh_scythe.models import Identify, Record

if TYPE_CHECKING:
    from pytest_mock.plugin import MockerFixture, MockType
    from respx.models import Route
    from respx.router import MockRouter


query = {"verb": "Identify"}
auth = ("username", "password")


@pytest.fixture
def mock_sleep(mocker: MockerFixture) -> MockType:
    return mocker.patch("time.sleep")


@pytest.fixture
def mock_identify(respx_mock: MockRouter, identify_response: httpx.Response) -> Route:
    return respx_mock.get("https://zenodo.org/oai2d?verb=Identify").mock(return_value=identify_response)


def test_invalid_http_method() -> None:
    with pytest.raises(ValueError, match="Invalid HTTP method"):
        Scythe("https://localhost", http_method="DELETE")


def test_invalid_iterator() -> None:
    with pytest.raises(TypeError):
        Scythe("https://localhost", iterator=None)  # type: ignore [arg-type]


def test_client_property(scythe: Scythe) -> None:
    assert isinstance(scythe.client, httpx.Client)


def test_close(scythe: Scythe) -> None:
    assert scythe.close() is None


def test_context_manager() -> None:
    with Scythe("https://zenodo.org/oai2d") as scythe:
        assert isinstance(scythe, Scythe)


def test_override_encoding(scythe: Scythe, mock_identify: Route) -> None:
    custom_encoding = "latin_1"
    scythe.encoding = custom_encoding
    http_response = scythe._request(query)
    assert mock_identify.called
    assert http_response.encoding == custom_encoding


def test_post_method(scythe: Scythe, respx_mock: MockRouter, identify_response: httpx.Response) -> None:
    mock_route = respx_mock.post("https://zenodo.org/oai2d").mock(return_value=identify_response)
    scythe.http_method = "POST"
    response = scythe.harvest(query)
    assert mock_route.call_count == 1
    assert response.status_code == httpx.codes.OK


def test_no_retry(scythe: Scythe, mock_identify: Route) -> None:
    mock_identify.return_value = httpx.Response(httpx.codes.SERVICE_UNAVAILABLE)
    with suppress(httpx.HTTPStatusError):
        scythe.harvest(query)
    assert mock_identify.call_count == 1


def test_retry_on_503(scythe: Scythe, mock_identify: Route, mock_sleep: MockType) -> None:
    scythe.max_retries = 3
    scythe.default_retry_after = 0
    mock_identify.return_value = httpx.Response(httpx.codes.SERVICE_UNAVAILABLE, headers={"retry-after": "10"})
    with suppress(httpx.HTTPStatusError):
        scythe.harvest(query)
    assert mock_identify.call_count == 4
    assert mock_sleep.call_count == 3
    mock_sleep.assert_called_with(10)


def test_retry_on_503_without_retry_after_header(scythe: Scythe, mock_identify: Route, mock_sleep: MockType) -> None:
    scythe.max_retries = 3
    scythe.default_retry_after = 0
    mock_identify.return_value = httpx.Response(httpx.codes.SERVICE_UNAVAILABLE, headers=None)
    with suppress(httpx.HTTPStatusError):
        scythe.harvest(query)
    assert mock_identify.call_count == 4
    assert mock_sleep.call_count == 3


def test_retry_on_custom_code(scythe: Scythe, mock_identify: Route, mock_sleep: MockType) -> None:
    mock_identify.return_value = httpx.Response(httpx.codes.INTERNAL_SERVER_ERROR)
    scythe.max_retries = 3
    scythe.default_retry_after = 0
    scythe.retry_status_codes = (httpx.codes.SERVICE_UNAVAILABLE, httpx.codes.INTERNAL_SERVER_ERROR)
    with suppress(httpx.HTTPStatusError):
        scythe.harvest(query)
    assert mock_identify.call_count == 4
    assert mock_sleep.call_count == 3


def test_no_set_hierarchy(scythe: Scythe, respx_mock: MockRouter) -> None:
    no_set_hierarchy_xml = """
    <OAI-PMH xmlns="http://www.openarchives.org/OAI/2.0/">
        <responseDate>2002-05-01T09:18:29Z</responseDate>
        <request verb="ListSets">https://zenodo.org/oai2d</request>
        <error code="noSetHierarchy">This repository does not support sets</error>
    </OAI-PMH>
    """
    response = httpx.Response(status_code=httpx.codes.UNPROCESSABLE_ENTITY, content=no_set_hierarchy_xml)
    respx_mock.get("https://zenodo.org/oai2d?verb=ListSets").mock(return_value=response)
    sets = scythe.list_sets()
    with pytest.raises(NoSetHierarchy, match="This repository does not support sets"):
        next(sets)


def test_cannot_disseminate_format(scythe: Scythe, respx_mock: MockRouter) -> None:
    cannot_disseminate_format_xml = """
    <OAI-PMH xmlns="http://www.openarchives.org/OAI/2.0/">
        <responseDate>2024-04-20T11:54:13Z</responseDate>
        <request metadataPrefix="XXX" verb="ListIdentifiers">https://zenodo.org/oai2d</request>
        <error code="cannotDisseminateFormat">XXX</error>
    </OAI-PMH>
    """
    response = httpx.Response(status_code=httpx.codes.UNPROCESSABLE_ENTITY, content=cannot_disseminate_format_xml)
    respx_mock.get("https://zenodo.org/oai2d?verb=ListIdentifiers&metadataPrefix=XXX").mock(return_value=response)
    headers = scythe.list_identifiers(metadata_prefix="XXX")
    with pytest.raises(CannotDisseminateFormat, match="XXX"):
        next(headers)


def test_no_auth_arguments() -> None:
    with Scythe("https://zenodo.org/oai2d") as scythe:
        assert scythe.client.auth is None


def test_auth_arguments() -> None:
    with Scythe("https://zenodo.org/oai2d", auth=auth) as scythe:
        assert scythe.client.auth


def test_auth_arguments_usage(respx_mock: MockRouter, mock_identify: Route) -> None:
    scythe = Scythe("https://zenodo.org/oai2d", auth=auth)
    http_response = scythe._request(query)
    assert http_response.request.headers["authorization"]


def test_identify(scythe: Scythe, mock_identify: Route) -> None:
    identify = scythe.identify()
    assert isinstance(identify, Identify)


@pytest.mark.default_cassette("list_records.yaml")
@pytest.mark.vcr
def test_list_records(scythe: Scythe) -> None:
    records = scythe.list_records()
    assert isinstance(records, Iterator)
    assert next(records)


@pytest.mark.default_cassette("list_identifiers.yaml")
@pytest.mark.vcr
def test_list_identifiers(scythe: Scythe) -> None:
    headers = scythe.list_identifiers()
    assert isinstance(headers, Iterator)
    assert next(headers)


@pytest.mark.default_cassette("list_metadata_formats.yaml")
@pytest.mark.vcr
def test_list_metadata_formats(scythe: Scythe, mocker) -> None:
    metadata_formats = scythe.list_metadata_formats()
    assert isinstance(metadata_formats, Iterator)
    assert next(metadata_formats)


@pytest.mark.default_cassette("list_sets.yaml")
@pytest.mark.vcr
def test_list_sets(scythe: Scythe, mocker) -> None:
    sets = scythe.list_sets()
    assert isinstance(sets, Iterator)
    assert next(sets)


@pytest.mark.default_cassette("get_record.yaml")
@pytest.mark.vcr
def test_get_record(scythe: Scythe) -> None:
    record = scythe.get_record(identifier="oai:zenodo.org:10357859")
    assert isinstance(record, Record)


@pytest.mark.parametrize("timeout", [10, 10.0, 0.1])
def test_valid_custom_timeout(timeout):
    with Scythe("https://zenodo.org/oai2d", timeout=timeout) as scythe:
        assert scythe.client.timeout


@pytest.mark.parametrize("timeout", [-1, -1.0, 0, 0.0])
def test_invalid_custom_timeout(timeout):
    with pytest.raises(ValueError, match="Invalid value for 'timeout'"):
        Scythe("https://zenodo.org/oai2d", timeout=timeout)


@pytest.mark.parametrize("retry_after", [10, 10.0, 0.1])
def test_valid_custom_retry_after(retry_after):
    with Scythe("https://zenodo.org/oai2d", default_retry_after=retry_after) as scythe:
        assert scythe.default_retry_after


@pytest.mark.parametrize("retry_after", [-1, -1.0, 0, 0.0])
def test_invalid_custom_retry_after(retry_after):
    with pytest.raises(ValueError, match="Invalid value for 'default_retry_after'"):
        Scythe("https://zenodo.org/oai2d", default_retry_after=retry_after)
