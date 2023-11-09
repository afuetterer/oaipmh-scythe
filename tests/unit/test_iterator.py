from __future__ import annotations

import pytest

from oaipmh_scythe import OAIResponse, Scythe
from oaipmh_scythe.iterator import OAIItemIterator, OAIResponseIterator
from oaipmh_scythe.models import Header

params = {"metadataPrefix": "oai_dc", "verb": "ListIdentifiers"}


@pytest.mark.default_cassette("list_identifiers.yaml")
@pytest.mark.vcr
def test_iterator_str(scythe: Scythe) -> None:
    iterator = OAIResponseIterator(scythe, params)
    assert str(iterator) == "<OAIResponseIterator ListIdentifiers>"


@pytest.mark.default_cassette("list_identifiers.yaml")
@pytest.mark.vcr
def test_oai_response_iterator(scythe: Scythe) -> None:
    iterator = OAIResponseIterator(scythe, params)
    responses = list(iterator)
    assert isinstance(responses[0], OAIResponse)
    # there are 3 canned responses in list_identifiers.yaml
    assert len(responses) == 3


@pytest.mark.default_cassette("list_identifiers.yaml")
@pytest.mark.vcr
def test_oai_item_iterator(scythe: Scythe) -> None:
    iterator = OAIItemIterator(scythe, params)
    identifiers = list(iterator)
    assert isinstance(identifiers[0], Header)
    # there are 15 canned identifiers in list_identifiers.yaml
    assert len(identifiers) == 15


@pytest.mark.default_cassette("list_identifiers.yaml")
@pytest.mark.vcr
def test_oai_item_iterator_ignore_deleted(scythe: Scythe) -> None:
    iterator = OAIItemIterator(scythe, params, ignore_deleted=True)
    identifiers = list(iterator)
    assert isinstance(identifiers[0], Header)
    # there are 15 canned responses in list_identifiers.yaml
    # one of them is manually set to "status=deleted"
    assert len(identifiers) == 14
