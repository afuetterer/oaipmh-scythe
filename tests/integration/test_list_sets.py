# SPDX-FileCopyrightText: 2023 Heinz-Alexander Fütterer
#
# SPDX-License-Identifier: BSD-3-Clause

from __future__ import annotations

from collections.abc import Iterator
from typing import TYPE_CHECKING

import pytest
from httpx import HTTPStatusError

from oaipmh_scythe.models import Set

if TYPE_CHECKING:
    from oaipmh_scythe import Scythe


@pytest.mark.default_cassette("list_sets.yaml")
@pytest.mark.vcr
def test_list_sets(scythe: Scythe) -> None:
    sets = scythe.list_sets()
    assert isinstance(sets, Iterator)
    sets = list(sets)
    # there are 10 canned responses in list_identifiers.yaml
    assert len(sets) == 10
    s = sets[0]
    assert isinstance(s, Set)
    assert s.setName == "Harmonic Radar"


@pytest.mark.default_cassette("list_sets.yaml")
@pytest.mark.vcr
def test_list_sets_with_valid_resumption_token(scythe: Scythe) -> None:
    token = "eyJzZWVkIjowLjM1ODM1NjU5NDkzNDU3MjE3LCJwYWdlIjoyLCJrd2FyZ3MiOnt9fQ.abZnTA.XmYCr7-cbxvBh7bSF42hlCtMVVI"  # spellchecker:disable-line
    sets = scythe.list_sets(resumption_token=token)
    sets = list(sets)
    # there are 5 canned responses in the second batch in list_identifiers.yaml
    assert len(sets) == 5


@pytest.mark.default_cassette("list_sets.yaml")
@pytest.mark.vcr
def test_list_sets_with_invalid_resumption_token(scythe: Scythe) -> None:
    # badResumptionToken
    sets = scythe.list_sets(resumption_token="XXX")
    with pytest.raises(HTTPStatusError):
        sets = list(sets)
