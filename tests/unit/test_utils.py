# SPDX-FileCopyrightText: 2015 Mathias Loesch
# SPDX-FileCopyrightText: 2023 Heinz-Alexander Fütterer
#
# SPDX-License-Identifier: BSD-3-Clause

import pytest
from lxml import etree

from oaipmh_scythe.utils import filter_dict_except_resumption_token, get_namespace, remove_none_values, xml_to_dict


@pytest.fixture()
def xml_element_with_namespace() -> etree._Element:
    xml = '<OAI-PMH xmlns="http://www.openarchives.org/OAI/2.0/"><request verb="Identify">https://zenodo.org/oai2d</request></OAI-PMH>'
    return etree.fromstring(xml)


@pytest.fixture()
def xml_element_without_namespace() -> etree._Element:
    xml = '<OAI-PMH><request verb="Identify">https://zenodo.org/oai2d</request></OAI-PMH>'
    return etree.fromstring(xml)


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


def test_get_namespace(xml_element_with_namespace: etree._Element) -> None:
    namespace = get_namespace(xml_element_with_namespace)
    assert namespace == "{http://www.openarchives.org/OAI/2.0/}"


def test_get_namespace_without_namespace(xml_element_without_namespace: etree._Element) -> None:
    namespace = get_namespace(xml_element_without_namespace)
    assert namespace is None


def test_xml_to_dict_default(xml_element_with_namespace: etree._Element) -> None:
    result = xml_to_dict(xml_element_with_namespace)
    expected = {"{http://www.openarchives.org/OAI/2.0/}request": ["https://zenodo.org/oai2d"]}
    assert result == expected


def test_xml_to_dict_with_paths(xml_element_with_namespace: etree._Element) -> None:
    result = xml_to_dict(xml_element_with_namespace, paths=["./{http://www.openarchives.org/OAI/2.0/}request"])
    expected = {
        "{http://www.openarchives.org/OAI/2.0/}request": ["https://zenodo.org/oai2d"],
    }
    assert result == expected


def test_xml_to_dict_with_nsmap(xml_element_with_namespace: etree._Element) -> None:
    nsmap = {"oai": "http://www.openarchives.org/OAI/2.0/"}
    result = xml_to_dict(xml_element_with_namespace, paths=["oai:request"], nsmap=nsmap)
    expected = {"{http://www.openarchives.org/OAI/2.0/}request": ["https://zenodo.org/oai2d"]}
    assert result == expected


def test_xml_to_dict_strip_namespace(xml_element_with_namespace: etree._Element) -> None:
    result = xml_to_dict(xml_element_with_namespace, strip_ns=True)
    expected = {"request": ["https://zenodo.org/oai2d"]}
    assert result == expected
