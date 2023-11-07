from __future__ import annotations

import pytest

from oaipmh_scythe import OAIResponse, Scythe
from oaipmh_scythe.iterator import OAIItemIterator, OAIResponseIterator
from oaipmh_scythe.models import Header


@pytest.mark.default_cassette("list_identifiers.yaml")
@pytest.mark.vcr
def test_oai_response_iterator(scythe: Scythe) -> None:
    params = {"metadataPrefix": "oai_dc", "verb": "ListIdentifiers"}
    iterator = OAIResponseIterator(scythe, params)
    responses = list(iterator)
    assert isinstance(responses[0], OAIResponse)
    # there are 3 canned responses in list_identifiers.yaml
    assert len(responses) == 3


@pytest.mark.default_cassette("list_identifiers.yaml")
@pytest.mark.vcr
def test_oai_item_iterator(scythe: Scythe) -> None:
    params = {"metadataPrefix": "oai_dc", "verb": "ListIdentifiers"}
    iterator = OAIItemIterator(scythe, params)
    identifiers = list(iterator)
    assert isinstance(identifiers[0], Header)
    # there are 15 canned identifiers in list_identifiers.yaml
    assert len(identifiers) == 15
