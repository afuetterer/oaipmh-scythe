# SPDX-FileCopyrightText: 2023 Heinz-Alexander Fütterer
#
# SPDX-License-Identifier: BSD-3-Clause

from xsdata.formats.dataclass.context import XmlContext
from xsdata.formats.dataclass.parsers import XmlParser
from xsdata.models.datatype import XmlDateTime

from oaipmh_scythe.models import Header, Identify, MetadataFormat, Record, ResumptionToken, Set
from oaipmh_scythe.models.oai_dc import Dc, Title
from oaipmh_scythe.models.oai_pmh import Metadata, OaiPmherror, OaiPmherrorcode, ProtocolVersion, Status

PARSER = XmlParser(context=XmlContext())


def test_identify_parsing() -> None:
    identify_xml = """
    <Identify xmlns="http://www.openarchives.org/OAI/2.0/">
        <repositoryName>Zenodo</repositoryName>
        <baseURL>https://zenodo.org/oai2d</baseURL>
        <protocolVersion>2.0</protocolVersion>
    </Identify>
    """
    identify = PARSER.from_string(identify_xml, Identify)
    assert isinstance(identify, Identify)
    expected = Identify(
        repository_name="Zenodo", base_url="https://zenodo.org/oai2d", protocol_version=ProtocolVersion.VALUE_2_0
    )
    assert identify == expected


def test_header_parsing():
    header_xml = """
    <header xmlns="http://www.openarchives.org/OAI/2.0/">
        <identifier>oai:zenodo.org:10357859</identifier>
        <datestamp>2023-12-11T17:26:46Z</datestamp>
    </header>
    """
    header = PARSER.from_string(header_xml, Header)
    assert isinstance(header, Header)
    expected = Header(identifier="oai:zenodo.org:10357859", datestamp="2023-12-11T17:26:46Z")
    assert header == expected
    assert not header.deleted


def test_header_deleted():
    header_xml = '<header status="deleted" xmlns="http://www.openarchives.org/OAI/2.0/"></header>'
    header = PARSER.from_string(header_xml, Header)
    assert header.deleted


def test_resumption_token_parsing() -> None:
    token_xml = """
    <resumptionToken expirationDate="2024-01-21T16:55:57Z" cursor="0" completeListSize="3677115">eJyNzt1ugjAYgOF7</resumptionToken>
    """
    token = PARSER.from_string(token_xml, ResumptionToken)
    assert isinstance(token, ResumptionToken)
    expiration_date = XmlDateTime(2024, 1, 21, 16, 55, 57)
    expected = ResumptionToken(
        value="eJyNzt1ugjAYgOF7", cursor=0, expiration_date=expiration_date, complete_list_size=3677115
    )
    assert token == expected


def test_record_parsing():
    record_xml = """
    <record xmlns="http://www.openarchives.org/OAI/2.0/">
        <header></header>
        <metadata>
            <oai_dc:dc  xmlns:dc="http://purl.org/dc/elements/1.1/"
                        xmlns:oai_dc="http://www.openarchives.org/OAI/2.0/oai_dc/">
                <dc:title>Research Data Management Organiser (RDMO)</dc:title>
            </oai_dc:dc>
        </metadata>
    </record>
    """
    record = PARSER.from_string(record_xml, Record)
    assert isinstance(record, Record)
    expected = Record(
        header=Header(),
        metadata=Metadata(other_element=Dc(title=[Title(value="Research Data Management Organiser (RDMO)")])),
    )
    assert record == expected
    assert not record.deleted


def test_record_deleted():
    record = Record(header=Header(status=Status.DELETED))
    assert record.deleted


def test_record_get_metadata():
    expected = Dc(title=[Title(value="Research Data Management Organiser (RDMO)")])
    record = Record(header=Header(), metadata=Metadata(other_element=expected))
    metadata = record.get_metadata()
    assert isinstance(metadata, Dc)
    assert metadata == expected


def test_error_parsing():
    error_xml = '<error code="idDoesNotExist">No matching identifier</error>'
    error = PARSER.from_string(error_xml, OaiPmherror)
    assert isinstance(error, OaiPmherror)
    expected = OaiPmherror(code=OaiPmherrorcode.ID_DOES_NOT_EXIST, value="No matching identifier")
    assert error == expected


def test_set_parsing():
    set_xml = """
    <set xmlns="http://www.openarchives.org/OAI/2.0/">
        <setSpec>software</setSpec>
        <setName>Software</setName>
    </set>
    """
    set_ = PARSER.from_string(set_xml, Set)
    expected = Set(set_spec="software", set_name="Software")
    assert isinstance(set_, Set)
    assert set_ == expected


def test_metadata_format_parsing():
    metadata_format_xml = """
    <metadataFormat xmlns="http://www.openarchives.org/OAI/2.0/">
        <metadataPrefix>oai_dc</metadataPrefix>
        <schema>http://www.openarchives.org/OAI/2.0/oai_dc.xsd</schema>
        <metadataNamespace>http://www.openarchives.org/OAI/2.0/oai_dc/</metadataNamespace>
    </metadataFormat>
    """
    metadata_format = PARSER.from_string(metadata_format_xml, MetadataFormat)
    assert isinstance(metadata_format, MetadataFormat)
    expected = MetadataFormat(
        metadata_prefix="oai_dc",
        schema="http://www.openarchives.org/OAI/2.0/oai_dc.xsd",
        metadata_namespace="http://www.openarchives.org/OAI/2.0/oai_dc/",
    )
    assert metadata_format == expected
