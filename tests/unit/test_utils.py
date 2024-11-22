# SPDX-FileCopyrightText: 2015 Mathias Loesch
# SPDX-FileCopyrightText: 2023 Heinz-Alexander Fütterer
#
# SPDX-License-Identifier: BSD-3-Clause

from typing import TYPE_CHECKING

import pytest

if TYPE_CHECKING:
    from pytest_mock.plugin import MockerFixture

from oaipmh_scythe.utils import filter_dict_except_resumption_token, load_models, remove_none_values


def test_remove_none_values() -> None:
    d = {"a": 1, "b": None, "c": 3}
    result = remove_none_values(d)
    assert result == {"a": 1, "c": 3}


def test_remove_none_values_noop() -> None:
    d = {"a": 1, "b": 2}
    result = remove_none_values(d)
    assert result == d


def test_filter_dict_except_resumption_token() -> None:
    d = {"resumptionToken": "token-abc", "verb": "ListRecords", "metadataPrefix": "oai_dc"}
    expected = {"resumptionToken": "token-abc", "verb": "ListRecords"}
    result = filter_dict_except_resumption_token(d)
    assert result == expected


def test_filter_dict_except_resumption_token_noop() -> None:
    d = {"resumptionToken": None, "verb": "ListRecords"}
    result = filter_dict_except_resumption_token(d)
    assert result == d


@pytest.mark.parametrize("metadata_prefix", ["oai_dc", "datacite"])
def test_load_models(mocker: "MockerFixture", metadata_prefix: str) -> None:
    mock_import = mocker.patch("builtins.__import__")
    load_models(metadata_prefix)
    mock_import.assert_called_once()
