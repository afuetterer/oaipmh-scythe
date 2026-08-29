# SPDX-FileCopyrightText: 2015 Mathias Loesch
# SPDX-FileCopyrightText: 2023 Heinz-Alexander Fütterer
#
# SPDX-License-Identifier: BSD-3-Clause

from __future__ import annotations

from contextlib import suppress
from typing import TYPE_CHECKING

import httpx  # We still need legacy httpx for using httpx.Response as return value in the mocks. There is an open issue about this in https://github.com/lundberg/pytest-httpx2/issues/3
import httpx2
import pytest
from httpx2 import HTTPStatusError

from oaipmh_scythe import HTTPConfig, RetryConfig, Scythe, exceptions

if TYPE_CHECKING:
    from pytest_mock import MockerFixture
    from respx.router import MockRouter

query = {"verb": "ListIdentifiers", "metadataPrefix": "oai_dc"}
auth = ("username", "password")


def build_oaipmh_error_response(error_code: str, error_message: str) -> httpx.Response:
    """Generate an OAI-PMH error response with the given code and message."""
    xml = f"""<?xml version="1.0" encoding="UTF-8"?>
    <OAI-PMH xmlns="http://www.openarchives.org/OAI/2.0/">
        <responseDate>2026-08-10T09:18:29Z</responseDate>
        <request>https://zenodo.org/oai2d</request>
        <error code="{error_code}">{error_message}</error>
    </OAI-PMH>"""
    return httpx.Response(
        422,
        content=xml.encode(),
        headers={"Content-Type": "application/xml; charset=utf-8"},
    )


def test_invalid_iterator() -> None:
    with pytest.raises(TypeError):
        Scythe("https://localhost", iterator=None)  # ty: ignore [invalid-argument-type]


def test_client_property(scythe: Scythe) -> None:
    assert isinstance(scythe.client, httpx2.Client)


def test_close(scythe: Scythe) -> None:
    assert scythe.close() is None


def test_context_manager() -> None:
    with Scythe("https://zenodo.org/oai2d") as scythe:
        assert isinstance(scythe, Scythe)


def test_override_encoding(scythe: Scythe, httpx2_mock: MockRouter) -> None:
    mock_route = httpx2_mock.get("https://zenodo.org/oai2d?verb=ListIdentifiers&metadataPrefix=oai_dc").mock(
        return_value=httpx.Response(200)
    )
    custom_encoding = "latin_1"
    scythe.encoding = custom_encoding
    oai_response = scythe.harvest(query)
    assert mock_route.called
    assert oai_response.http_response.encoding == custom_encoding


def test_post_method(scythe: Scythe, httpx2_mock: MockRouter) -> None:
    mock_route = httpx2_mock.post("https://zenodo.org/oai2d").mock(return_value=httpx.Response(200))
    scythe.http_method = "POST"
    oai_response = scythe.harvest(query)
    assert mock_route.called
    assert oai_response.http_response.status_code == 200


def test_no_retry(scythe: Scythe, httpx2_mock: MockRouter) -> None:
    mock_route = httpx2_mock.get("https://zenodo.org/oai2d?verb=ListIdentifiers&metadataPrefix=oai_dc").mock(
        return_value=httpx.Response(503)
    )
    with suppress(HTTPStatusError):
        scythe.harvest(query)
    assert mock_route.call_count == 1


def test_retry_on_503(scythe: Scythe, httpx2_mock: MockRouter, mocker: MockerFixture) -> None:
    scythe.max_retries = 3
    scythe.default_retry_after = 0
    mock_sleep = mocker.patch("time.sleep")
    mock_route = httpx2_mock.get("https://zenodo.org/oai2d?verb=ListIdentifiers&metadataPrefix=oai_dc").mock(
        return_value=httpx.Response(503, headers={"retry-after": "10"})
    )
    with suppress(HTTPStatusError):
        scythe.harvest(query)
    assert mock_route.call_count == 4
    assert mock_sleep.call_count == 3
    mock_sleep.assert_called_with(10)


def test_retry_on_503_without_retry_after_header(
    scythe: Scythe, httpx2_mock: MockRouter, mocker: MockerFixture
) -> None:
    scythe.max_retries = 3
    scythe.default_retry_after = 0
    mock_sleep = mocker.patch("time.sleep")
    mock_route = httpx2_mock.get("https://zenodo.org/oai2d?verb=ListIdentifiers&metadataPrefix=oai_dc").mock(
        return_value=httpx.Response(503, headers=None)
    )
    with suppress(HTTPStatusError):
        scythe.harvest(query)
    assert mock_route.call_count == 4
    assert mock_sleep.call_count == 3


def test_retry_on_custom_code(scythe: Scythe, httpx2_mock: MockRouter, mocker: MockerFixture) -> None:
    mock_route = httpx2_mock.get("https://zenodo.org/oai2d?verb=ListIdentifiers&metadataPrefix=oai_dc").mock(
        return_value=httpx.Response(500)
    )
    scythe.max_retries = 3
    scythe.default_retry_after = 0
    mock_sleep = mocker.patch("time.sleep")
    scythe.retry_status_codes = (503, 500)
    with suppress(HTTPStatusError):
        scythe.harvest(query)
    assert mock_route.call_count == 4
    assert mock_sleep.call_count == 3


def test_no_auth_arguments() -> None:
    with Scythe("https://zenodo.org/oai2d") as scythe:
        assert scythe.client.auth is None


def test_auth_arguments() -> None:
    with Scythe("https://zenodo.org/oai2d", http_config=HTTPConfig(auth=auth)) as scythe:
        assert scythe.client.auth


def test_auth_arguments_usage(httpx2_mock: MockRouter) -> None:
    scythe = Scythe("https://zenodo.org/oai2d", http_config=HTTPConfig(auth=auth))
    httpx2_mock.get("https://zenodo.org/oai2d").mock(return_value=httpx.Response(200))
    oai_response = scythe.harvest(query)
    assert oai_response.http_response.request.headers["authorization"]


@pytest.mark.parametrize("timeout", [10, 10.0, 0.1])
def test_valid_custom_timeout(timeout: float) -> None:
    with Scythe("https://zenodo.org/oai2d", http_config=HTTPConfig(timeout=timeout)) as scythe:
        assert scythe.client.timeout


def test_http_config() -> None:
    http_config = HTTPConfig(http_method="POST", timeout=30, auth=auth, encoding="latin-1")
    with Scythe("https://zenodo.org/oai2d", http_config=http_config) as scythe:
        assert scythe.http_config is http_config
        assert scythe.http_method == "POST"
        assert scythe.timeout == 30
        assert scythe.auth == auth
        assert scythe.encoding == "latin-1"


def test_default_http_config() -> None:
    scythe = Scythe("https://zenodo.org/oai2d")
    assert scythe.http_config == HTTPConfig()
    assert scythe.http_method == "GET"
    assert scythe.timeout == 60
    assert scythe.auth is None
    assert scythe.encoding == "utf-8"


@pytest.mark.parametrize(
    ("legacy_kwargs", "expected"),
    [
        ({"http_method": "POST"}, HTTPConfig(http_method="POST")),
        ({"timeout": 30}, HTTPConfig(timeout=30)),
        ({"auth": auth}, HTTPConfig(auth=auth)),
        ({"encoding": "latin-1"}, HTTPConfig(encoding="latin-1")),
    ],
)
def test_legacy_http_arguments_warn(legacy_kwargs: dict[str, object], expected: HTTPConfig) -> None:
    with pytest.warns(FutureWarning, match="removed in version 0.19.0"):
        scythe = Scythe("https://zenodo.org/oai2d", **legacy_kwargs)  # ty: ignore [invalid-argument-type]
    assert scythe.http_config == expected


def test_legacy_http_arguments_defaults_do_not_warn() -> None:
    scythe = Scythe("https://zenodo.org/oai2d", http_method="GET", timeout=60, auth=None, encoding="utf-8")
    assert scythe.http_config == HTTPConfig()


def test_http_config_conflict_with_legacy_arguments() -> None:
    with pytest.raises(ValueError, match="Cannot specify both"):
        Scythe("https://zenodo.org/oai2d", http_config=HTTPConfig(), http_method="POST")


def test_retry_config() -> None:
    retry_config = RetryConfig(max_retries=3, retry_status_codes=(503, 500), default_retry_after=5)
    with Scythe("https://zenodo.org/oai2d", retry_config=retry_config) as scythe:
        assert scythe.retry_config is retry_config
        assert scythe.max_retries == 3
        assert scythe.retry_status_codes == (503, 500)
        assert scythe.default_retry_after == 5


def test_default_retry_config() -> None:
    scythe = Scythe("https://zenodo.org/oai2d")
    assert scythe.retry_config == RetryConfig()
    assert scythe.max_retries == 0
    assert scythe.retry_status_codes == (503,)
    assert scythe.default_retry_after == 60


@pytest.mark.parametrize(
    ("legacy_kwargs", "expected"),
    [
        ({"max_retries": 2}, RetryConfig(max_retries=2)),
        ({"retry_status_codes": (503, 500)}, RetryConfig(retry_status_codes=(503, 500))),
        ({"default_retry_after": 10}, RetryConfig(default_retry_after=10)),
        (
            {"max_retries": 2, "retry_status_codes": (503, 500), "default_retry_after": 10},
            RetryConfig(max_retries=2, retry_status_codes=(503, 500), default_retry_after=10),
        ),
    ],
)
def test_legacy_retry_arguments_warn(legacy_kwargs: dict[str, object], expected: RetryConfig) -> None:
    with pytest.warns(FutureWarning, match="removed in version 0.19.0"):
        scythe = Scythe("https://zenodo.org/oai2d", **legacy_kwargs)  # ty: ignore [invalid-argument-type]
    assert scythe.retry_config == expected


def test_legacy_retry_arguments_defaults_do_not_warn() -> None:
    scythe = Scythe("https://zenodo.org/oai2d", max_retries=0, retry_status_codes=None, default_retry_after=60)
    assert scythe.retry_config == RetryConfig()


def test_retry_config_conflict_with_legacy_arguments() -> None:
    with pytest.raises(ValueError, match="Cannot specify both"):
        Scythe("https://zenodo.org/oai2d", retry_config=RetryConfig(), max_retries=2)


def test_retry_with_retry_config(httpx2_mock: MockRouter, mocker: MockerFixture) -> None:
    scythe = Scythe("https://zenodo.org/oai2d", retry_config=RetryConfig(max_retries=3, default_retry_after=0.1))
    mock_sleep = mocker.patch("time.sleep")
    mock_route = httpx2_mock.get("https://zenodo.org/oai2d?verb=ListIdentifiers&metadataPrefix=oai_dc").mock(
        return_value=httpx.Response(503, headers={"retry-after": "10"})
    )
    with suppress(HTTPStatusError):
        scythe.harvest(query)
    assert mock_route.call_count == 4
    assert mock_sleep.call_count == 3
    mock_sleep.assert_called_with(10)


@pytest.mark.parametrize("retry_after", [10, 10.0, 0.1])
def test_valid_custom_retry_after(retry_after: float) -> None:
    with Scythe("https://zenodo.org/oai2d", retry_config=RetryConfig(default_retry_after=retry_after)) as scythe:
        assert scythe.default_retry_after


@pytest.mark.parametrize("retry_after", [-1, -1.0, 0, 0.0])
def test_invalid_custom_retry_after(retry_after: float) -> None:
    with pytest.raises(ValueError, match="Invalid value for 'default_retry_after'"):
        Scythe("https://zenodo.org/oai2d", default_retry_after=retry_after)


def test_server_with_application_xml_header(scythe: Scythe, httpx2_mock: MockRouter, mocker: MockerFixture) -> None:
    mock_route = httpx2_mock.get("https://zenodo.org/oai2d?verb=ListIdentifiers&metadataPrefix=oai_dc").mock(
        return_value=httpx.Response(200, headers={"Content-Type": "application/xml; charset=utf-8"})
    )
    scythe.harvest(query)
    assert mock_route.called


def test_bad_verb_response(scythe: Scythe, httpx2_mock: MockRouter) -> None:
    error_response = build_oaipmh_error_response(
        "badVerb",
        "Value of the verb argument is not a legal OAI-PMH verb, the verb argument is missing, or the verb argument is repeated.",
    )
    mock_route = httpx2_mock.get("https://zenodo.org/oai2d?verb=ListMetadataFormats").mock(return_value=error_response)
    with pytest.raises(exceptions.BadVerb):
        next(scythe.list_metadata_formats())
    assert mock_route.called


def test_no_set_hierarchy_response(scythe: Scythe, httpx2_mock: MockRouter) -> None:
    error_response = build_oaipmh_error_response("noSetHierarchy", "This repository does not support sets.")
    mock_route = httpx2_mock.get("https://zenodo.org/oai2d?verb=ListSets").mock(return_value=error_response)
    with pytest.raises(exceptions.NoSetHierarchy):
        next(scythe.list_sets())
    assert mock_route.called


def test_no_metadata_formats_response(scythe: Scythe, httpx2_mock: MockRouter) -> None:
    error_response = build_oaipmh_error_response(
        "noMetadataFormats",
        "There are no metadata formats available for the specified item.",
    )
    mock_route = httpx2_mock.get("https://zenodo.org/oai2d?verb=ListMetadataFormats").mock(return_value=error_response)
    with pytest.raises(exceptions.NoMetadataFormats):
        next(scythe.list_metadata_formats())
    assert mock_route.called


def test_cannot_disseminate_format_response(scythe: Scythe, httpx2_mock: MockRouter) -> None:
    error_response = build_oaipmh_error_response(
        "cannotDisseminateFormat",
        "The metadata format identified by the value given for the metadataPrefix argument is not supported by the item or by the repository.",
    )
    mock_route = httpx2_mock.get(
        "https://zenodo.org/oai2d?verb=GetRecord&identifier=oai%3Aexample.org%3A123&metadataPrefix=XXX"
    ).mock(return_value=error_response)
    with pytest.raises(exceptions.CannotDisseminateFormat):
        scythe.get_record(identifier="oai:example.org:123", metadata_prefix="XXX")
    assert mock_route.called


@pytest.mark.parametrize("error_code", ["unknownCode", ""])
def test_unknown_oaipmh_error_code(scythe: Scythe, httpx2_mock: MockRouter, error_code: str) -> None:
    error_response = build_oaipmh_error_response(error_code, "An unknown error occurred.")
    mock_route = httpx2_mock.get("https://zenodo.org/oai2d?verb=ListIdentifiers&metadataPrefix=oai_dc").mock(
        return_value=error_response
    )
    with pytest.raises(exceptions.GeneralOAIPMHError, match="An unknown error occurred"):
        next(scythe.list_identifiers())
    assert mock_route.called


def test_positional_arguments() -> None:
    scythe = Scythe("https://zenodo.org/oai2d")
    assert scythe


def test_keyword_arguments() -> None:
    scythe = Scythe("https://zenodo.org/oai2d", http_method="GET")
    assert scythe
