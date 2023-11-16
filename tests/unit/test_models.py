# SPDX-FileCopyrightText: 2023 Heinz-Alexander Fuetterer
#
# SPDX-License-Identifier: BSD-3-Clause

import pytest
from lxml import etree

from oaipmh_scythe import OAIResponse
from oaipmh_scythe.models import Header, Identify, MetadataFormat, Record, ResumptionToken, Set


def test_resumption_token_repr() -> None:
    token = ResumptionToken(token="some-token")
    assert repr(token) == "<ResumptionToken some-token>"


@pytest.fixture()
def identify_response(mocker):
    xml = """
    <OAI-PMH xmlns="http://www.openarchives.org/OAI/2.0/">
        <responseDate>2023-11-09T09:53:46Z</responseDate>
        <request verb="Identify">https://zenodo.org/oai2d</request>
        <Identify>
            <repositoryName>Zenodo</repositoryName>
            <baseURL>https://zenodo.org/oai2d</baseURL>
            <protocolVersion>2.0</protocolVersion>
        </Identify>
    </OAI-PMH>
    """
    mock_response = mocker.MagicMock(spec=OAIResponse)
    mock_response.xml = etree.fromstring(xml)
    return mock_response


@pytest.fixture()
def identify(identify_response) -> Identify:
    return Identify(identify_response)


def test_identify_bytes(identify):
    assert isinstance(identify.__bytes__(), bytes)
    assert b"<baseURL>https://zenodo.org/oai2d</baseURL>" in identify.__bytes__()


def test_identify_str(identify):
    assert isinstance(identify.__str__(), str)
    assert "<baseURL>https://zenodo.org/oai2d</baseURL>" in str(identify)


def test_identify_raw(identify):
    assert isinstance(identify.raw, str)
    assert "<baseURL>https://zenodo.org/oai2d</baseURL>" in identify.raw


def test_identify_repr(identify):
    assert repr(identify) == "<Identify>"


def test_identify_attributes(identify):
    assert identify.repositoryName == "Zenodo"
    assert identify.baseURL == "https://zenodo.org/oai2d"
    assert identify.protocolVersion == "2.0"


def test_identify_iter(identify):
    identify_items = dict(identify)
    assert identify_items["repositoryName"] == ["Zenodo"]
    assert identify_items["baseURL"] == ["https://zenodo.org/oai2d"]
    assert identify_items["protocolVersion"] == ["2.0"]


@pytest.fixture(scope="session")
def header_element():
    xml = """
    <header xmlns="http://www.openarchives.org/OAI/2.0/">
        <identifier>oai:zenodo.org:6538892</identifier>
        <datestamp>2022-05-11T13:49:36Z</datestamp>
    </header>
    """
    return etree.fromstring(xml.encode())


@pytest.fixture(scope="session")
def deleted_header_element():
    xml = """
    <header xmlns="http://www.openarchives.org/OAI/2.0/" status="deleted">
        <identifier>oai:zenodo.org:6538892</identifier>
        <datestamp>2022-05-11T13:49:36Z</datestamp>
    </header>
    """
    return etree.fromstring(xml.encode())


@pytest.fixture()
def header(header_element):
    return Header(header_element)


@pytest.fixture()
def deleted_header(deleted_header_element):
    return Header(deleted_header_element)


def test_header_init(header):
    assert header.identifier == "oai:zenodo.org:6538892"
    assert header.datestamp == "2022-05-11T13:49:36Z"
    assert not header.deleted


def test_header_init_with_deleted(deleted_header):
    assert deleted_header.identifier == "oai:zenodo.org:6538892"
    assert deleted_header.datestamp == "2022-05-11T13:49:36Z"
    assert deleted_header.deleted


def test_header_repr(header, deleted_header):
    assert repr(header) == "<Header oai:zenodo.org:6538892>"
    assert repr(deleted_header) == "<Header oai:zenodo.org:6538892 [deleted]>"


def test_header_iter(header):
    items = dict(header)
    assert items == {"identifier": "oai:zenodo.org:6538892", "datestamp": "2022-05-11T13:49:36Z", "setSpecs": []}


@pytest.fixture()
def record_element():
    xml = """
    <record xmlns="http://www.openarchives.org/OAI/2.0/">
        <header>
            <identifier>oai:example.org:record1</identifier>
            <datestamp>2021-01-01</datestamp>
            <setSpec>set1</setSpec>
        </header>
        <metadata>
            <dc xmlns="http://purl.org/dc/elements/1.1/">
                <title>Example Title</title>
                <creator>Example Creator</creator>
            </dc>
        </metadata>
    </record>
    """
    return etree.fromstring(xml.encode())


@pytest.fixture()
def deleted_record_lement():
    xml = """
    <record xmlns="http://www.openarchives.org/OAI/2.0/">
        <header status="deleted">
            <identifier>oai:example.org:record1</identifier>
            <datestamp>2021-01-01</datestamp>
            <setSpec>set1</setSpec>
        </header>
        <metadata>
            <dc xmlns="http://purl.org/dc/elements/1.1/">
                <title>Example Title</title>
                <creator>Example Creator</creator>
            </dc>
        </metadata>
    </record>
    """
    return etree.fromstring(xml.encode())


@pytest.fixture()
def record(record_element):
    return Record(record_element)


@pytest.fixture()
def deleted_record(deleted_record_lement):
    return Record(deleted_record_lement)


def test_record_init(record):
    assert isinstance(record.header, Header)
    assert record.header.identifier == "oai:example.org:record1"
    assert not record.deleted
    assert "title" in record.metadata
    assert record.metadata["title"] == ["Example Title"]


def test_record_repr(record):
    assert repr(record) == "<Record oai:example.org:record1>"


def test_deleted_record_repr(deleted_record):
    assert repr(deleted_record) == "<Record oai:example.org:record1 [deleted]>"


def test_record_iter(record):
    record_metadata = dict(record)
    assert record_metadata["title"] == ["Example Title"]
    assert record_metadata["creator"] == ["Example Creator"]


def test_deleted_record_no_metadata(deleted_record):
    assert deleted_record.deleted
    with pytest.raises(AttributeError):
        _ = record.metadata


@pytest.fixture()
def set_element():
    xml = """
    <set>
        <setSpec>user-emi</setSpec>
        <setName>European Middleware Initiative</setName>
        <setDescription></setDescription>
    </set>
    """
    return etree.fromstring(xml.encode())


@pytest.fixture()
def oai_set(set_element):
    return Set(set_element)


def test_set_init(oai_set):
    assert oai_set.setName == "European Middleware Initiative"
    assert "ser-emi" in oai_set.setSpec


def test_set_repr(oai_set):
    assert repr(oai_set) == "<Set European Middleware Initiative>"


def test_set_iter(oai_set):
    set_items = dict(oai_set)
    assert set_items["setName"] == ["European Middleware Initiative"]
    assert set_items["setSpec"] == ["user-emi"]


@pytest.fixture()
def mdf_element():
    xml = """
    <metadataFormat>
        <metadataPrefix>marcxml</metadataPrefix>
        <schema>https://www.loc.gov/standards/marcxml/schema/MARC21slim.xsd</schema>
        <metadataNamespace>https://www.loc.gov/standards/marcxml/</metadataNamespace>
    </metadataFormat>
    """
    return etree.fromstring(xml.encode())


@pytest.fixture()
def mdf(mdf_element):
    return MetadataFormat(mdf_element)


def test_metadata_format_init(mdf):
    assert mdf.metadataPrefix == "marcxml"
    assert mdf.schema == "https://www.loc.gov/standards/marcxml/schema/MARC21slim.xsd"
    assert mdf.metadataNamespace == "https://www.loc.gov/standards/marcxml/"


def test_metadata_format_repr(mdf):
    assert repr(mdf) == "<MetadataFormat marcxml>"


def test_metadata_format_iter(mdf):
    mdf_items = dict(mdf)
    assert mdf_items["metadataPrefix"] == ["marcxml"]
    assert mdf_items["schema"] == ["https://www.loc.gov/standards/marcxml/schema/MARC21slim.xsd"]
    assert mdf_items["metadataNamespace"] == ["https://www.loc.gov/standards/marcxml/"]
