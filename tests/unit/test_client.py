# SPDX-FileCopyrightText: 2015 Mathias Loesch
# SPDX-FileCopyrightText: 2023 Heinz-Alexander Fütterer
#
# SPDX-License-Identifier: BSD-3-Clause

from __future__ import annotations

from contextlib import suppress
from typing import TYPE_CHECKING

import httpx
import pytest

from oaipmh_scythe import Scythe

if TYPE_CHECKING:
    from respx.router import MockRouter


query = {"verb": "ListIdentifiers", "metadataPrefix": "oai_dc"}
auth = ("username", "password")


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


def test_override_encoding(scythe: Scythe, respx_mock: MockRouter) -> None:
    mock_route = respx_mock.get("https://zenodo.org/oai2d?verb=ListIdentifiers&metadataPrefix=oai_dc").mock(
        return_value=httpx.Response(200)
    )
    custom_encoding = "latin_1"
    scythe.encoding = custom_encoding
    oai_response = scythe.harvest(query)
    assert mock_route.called
    assert oai_response.http_response.encoding == custom_encoding


def test_post_method(scythe: Scythe, respx_mock: MockRouter) -> None:
    mock_route = respx_mock.post("https://zenodo.org/oai2d").mock(return_value=httpx.Response(200))
    scythe.http_method = "POST"
    oai_response = scythe.harvest(query)
    assert mock_route.called
    assert oai_response.http_response.status_code == 200


def test_no_retry(scythe: Scythe, respx_mock: MockRouter) -> None:
    mock_route = respx_mock.get("https://zenodo.org/oai2d?verb=ListIdentifiers&metadataPrefix=oai_dc").mock(
        return_value=httpx.Response(503)
    )
    with suppress(httpx.HTTPStatusError):
        scythe.harvest(query)
    assert mock_route.call_count == 1


def test_retry_on_503(scythe: Scythe, respx_mock: MockRouter, mocker) -> None:
    scythe.max_retries = 3
    scythe.default_retry_after = 0
    mock_sleep = mocker.patch("time.sleep")
    mock_route = respx_mock.get("https://zenodo.org/oai2d?verb=ListIdentifiers&metadataPrefix=oai_dc").mock(
        return_value=httpx.Response(503, headers={"retry-after": "10"})
    )
    with suppress(httpx.HTTPStatusError):
        scythe.harvest(query)
    assert mock_route.call_count == 4
    assert mock_sleep.call_count == 3
    mock_sleep.assert_called_with(10)


def test_retry_on_503_without_retry_after_header(scythe: Scythe, respx_mock: MockRouter, mocker) -> None:
    scythe.max_retries = 3
    scythe.default_retry_after = 0
    mock_sleep = mocker.patch("time.sleep")
    mock_route = respx_mock.get("https://zenodo.org/oai2d?verb=ListIdentifiers&metadataPrefix=oai_dc").mock(
        return_value=httpx.Response(503, headers=None)
    )
    with suppress(httpx.HTTPStatusError):
        scythe.harvest(query)
    assert mock_route.call_count == 4
    assert mock_sleep.call_count == 3


def test_retry_on_custom_code(scythe: Scythe, respx_mock: MockRouter, mocker) -> None:
    mock_route = respx_mock.get("https://zenodo.org/oai2d?verb=ListIdentifiers&metadataPrefix=oai_dc").mock(
        return_value=httpx.Response(500)
    )
    scythe.max_retries = 3
    scythe.default_retry_after = 0
    mock_sleep = mocker.patch("time.sleep")
    scythe.retry_status_codes = (503, 500)
    with suppress(httpx.HTTPStatusError):
        scythe.harvest(query)
    assert mock_route.call_count == 4
    assert mock_sleep.call_count == 3


def test_no_auth_arguments():
    with Scythe("https://zenodo.org/oai2d") as scythe:
        assert scythe.client.auth is None


def test_auth_arguments():
    with Scythe("https://zenodo.org/oai2d", auth=auth) as scythe:
        assert scythe.client.auth


def test_auth_arguments_usage(respx_mock: MockRouter) -> None:
    scythe = Scythe("https://zenodo.org/oai2d", auth=auth)
    respx_mock.get("https://zenodo.org/oai2d").mock(return_value=httpx.Response(200))
    oai_response = scythe.harvest(query)
    assert oai_response.http_response.request.headers["authorization"]


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


def test_list_records_with_custom_query(scythe: Scythe, respx_mock: MockRouter) -> None:
    """Test that custom_query parameters are properly merged into the request."""
    custom_params = {"customParam": "customValue", "anotherParam": "anotherValue"}
    expected_params = {
        "verb": "ListRecords",
        "metadataPrefix": "oai_dc",
        "customParam": "customValue",
        "anotherParam": "anotherValue",
    }

    mock_xml = """<?xml version="1.0" encoding="UTF-8"?>
    <OAI-PMH xmlns="http://www.openarchives.org/OAI/2.0/">
        <responseDate>2025-01-01T00:00:00Z</responseDate>
        <request verb="ListRecords">https://zenodo.org/oai2d</request>
        <ListRecords>
            <record>
                <header>
                    <identifier>test:1</identifier>
                    <datestamp>2025-01-01T00:00:00Z</datestamp>
                </header>
                <metadata>
                    <oai_dc:dc xmlns:oai_dc="http://www.openarchives.org/OAI/2.0/oai_dc/">
                        <dc:title>Test Record</dc:title>
                    </oai_dc:dc>
                </metadata>
            </record>
        </ListRecords>
    </OAI-PMH>"""

    mock_route = respx_mock.get("https://zenodo.org/oai2d").mock(return_value=httpx.Response(200, text=mock_xml))

    list(scythe.list_records(custom_query=custom_params))

    assert mock_route.called
    request = mock_route.calls[0].request
    query_params = dict(request.url.params)

    for key, value in expected_params.items():
        assert query_params.get(key) == value, f"Expected {key}={value}, got {query_params.get(key)}"
