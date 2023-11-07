from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

import pytest

from oaipmh_scythe import Scythe
from oaipmh_scythe.response import OAIResponse

if TYPE_CHECKING:
    from unittest.mock import MagicMock

    from pytest_mock.plugin import MockerFixture

TESTS_DIR = Path(__file__).parent
TEST_DATA_DIR = TESTS_DIR.joinpath("data")


class MockHttpResponse:
    status_code: int = 200
    text: str
    content: bytes

    def __init__(self, filename: str = ""):
        # request's response object carry an attribute 'text' which contains
        # the server's response data encoded as unicode.
        path = TEST_DATA_DIR.joinpath(filename)
        self.text = path.read_text()
        self.content = path.read_bytes()

    def raise_for_status(self) -> None:
        pass


class MockHttpResponseWrongEncoding(MockHttpResponse):
    """Mimics a case where the requests library misidentifies the text encoding.

    If HTTP headers do not specify the correct encoding, requests will default
    to 'ISO-8859-1', even though the oai-pmh document might specify e.g.
    <xml encoding='utf-8'>.
    """

    def __init__(self, filename: str = ""):
        super().__init__(filename)
        self.text = self.content.decode("ISO-8859-1")


def oairesponse_from_file(filename: str, params: dict[str, str]) -> OAIResponse:
    response = MockHttpResponse(filename)
    return OAIResponse(response, params)


def mock_harvest(*args, **kwargs) -> OAIResponse:
    """Read test data from files instead of from an OAI interface.

    The data is read from the `data` directory by using the provided
    :attr:`verb` as file name. The following returns an OAIResponse created
    from the file ``ListRecords.xml``::

        fake_harvest(verb='ListRecords', metadataPrefix='oai_dc')

    The file names for consecutive resumption responses are expected in the
    resumptionToken parameter::

        fake_harvest(verb='ListRecords', resumptionToken='ListRecords2.xml')

    The parameter :attr:`error` can be used to invoke a specific OAI error
    response. For instance, the following returns a ``badArgument`` error
    response::

        fake_harvest(verb='ListRecords', error='badArgument')

    :param kwargs: OAI arguments that would normally be passed to
                   :meth:`sickle.scythe.Sickle.harvest`.
    """

    verb = kwargs.get("verb")
    resumption_token = kwargs.get("resumptionToken")
    error = kwargs.get("error")
    if resumption_token:
        filename = resumption_token
    elif error:
        filename = f"{error}.xml"
    else:
        filename = f"{verb}.xml"
    return oairesponse_from_file(filename, kwargs)


@pytest.fixture
def harvester(mocker: MockerFixture) -> Scythe:
    mocker.patch("oaipmh_scythe.scythe.Scythe.harvest", mock_harvest)
    return Scythe("https://localhost")


@pytest.fixture
def mock_get(mocker: MockerFixture) -> MagicMock:
    return mocker.patch("oaipmh_scythe.scythe.httpx.get")


@pytest.fixture(scope="module")
def vcr_config() -> dict[str, str]:
    return {"cassette_library_dir": "tests/cassettes"}


@pytest.fixture
def scythe() -> Scythe:
    return Scythe("https://zenodo.org/oai2d")
