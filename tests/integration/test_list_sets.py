# SPDX-FileCopyrightText: 2023 Heinz-Alexander Fütterer
#
# SPDX-License-Identifier: BSD-3-Clause

from __future__ import annotations

from collections.abc import Iterator
from typing import TYPE_CHECKING

import pytest

from oaipmh_scythe import exceptions
from oaipmh_scythe.models import Set

if TYPE_CHECKING:
    from oaipmh_scythe import Scythe


@pytest.mark.vcr("list_sets.yaml")
def test_list_sets(scythe: Scythe) -> None:
    sets = scythe.list_sets()
    assert isinstance(sets, Iterator)
    sets = list(sets)
    # there are 10 canned responses in list_identifiers.yaml
    assert len(sets) == 10
    s = sets[0]
    assert isinstance(s, Set)
    assert s.setName == "Harmonic Radar"


@pytest.mark.vcr("list_sets.yaml")
def test_list_sets_with_valid_resumption_token(scythe: Scythe) -> None:
    token = "eyJzZWVkIjowLjMyOTUxMjIzOTg3NzM4MzksInBhZ2UiOjIsImt3YXJncyI6e319.any5dw.kg_s6M1Kr5M3Ar7Z6EWcvbfu8Tg"  # spellchecker:disable-line
    sets = scythe.list_sets(resumption_token=token)
    sets = list(sets)
    # there are 5 canned responses in the second batch in list_identifiers.yaml
    assert len(sets) == 5


@pytest.mark.vcr("list_sets.yaml")
def test_list_sets_with_invalid_resumption_token(scythe: Scythe) -> None:
    sets = scythe.list_sets(resumption_token="XXX")
    with pytest.raises(exceptions.BadResumptionToken):
        sets = list(sets)
