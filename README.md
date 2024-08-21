# oaipmh-scythe: A Scythe for harvesting OAI-PMH repositories.

Welcome to `oaipmh-scythe`, an updated and modernized version of the original
[sickle](https://github.com/mloesch/sickle), now with additional features and ongoing maintenance.

| __CI__      | [![pre-commit.ci status][pre-commit-ci-badge]][pre-commit-ci-status] [![ci][ci-badge]][ci-workflow] [![coverage][coverage-badge]][ci-workflow] [![codeql][codeql-badge]][codeql-workflow]                                             |
| :---------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| __Docs__    | [![docs][docs-badge]][docs-workflow]                                                                                                                                                                                                  |
| __Package__ | [![pypi-version][pypi-version-badge]][pypi-url] [![pypi-python-versions][pypi-python-versions-badge]][pypi-url] [![all-downloads][all-downloads-badge]][pepy-tech-url] [![monthly-downloads][monthly-downloads-badge]][pepy-tech-url] |
| __Meta__    | [![doi][doi-badge]][doi-url] [![OpenSSF Scorecard][scorecard-badge]][scorecard-url] [![hatch][hatch-badge]][hatch] [![ruff][ruff-badge]][ruff] [![mypy][mypy-badge]][mypy] [![License][license-badge]][license]                       |

`oaipmh-scythe` is a lightweight [OAI-PMH](http://www.openarchives.org/OAI/openarchivesprotocol.html) client library
written in Python. It has been designed for conveniently retrieving data from OAI interfaces the Pythonic way:

```python
from oaipmh_scythe import Scythe

with Scythe("https://zenodo.org/oai2d") as scythe:
    records = scythe.list_records()
    next(records)
# Record(header=Header(identifier='oai:zenodo.org:10654826', datestamp='2024-02-13T15:38:50Z', set_spec=['software'], status=None), metadata=Metadata(other_element=Dc(title=[Title(value='Research Data Management Organiser (RDMO)', lang=None)], creator=[Creator(value='Klar, Jochen', lang=None), Creator(value='Michaelis, Olaf', lang=None), Creator(value='Wallace, David', lang=None), Creator(value='Schröder, Max', lang=None), Creator(value='Fütterer, Heinz-Alexander', lang=None), Creator(value='Lanza, Giacomo', lang=None), Creator(value='Martínez Muñoz, David', lang=None), Creator(value='Pilori, Dario', lang=None), Creator(value='Harry, Enke', lang=None)], subject=[], description=[Description(value='&lt;h2&gt;&lt;a href="https://github.com/rdmorganiser/rdmo/compare/2.1.2...2.1.3"&gt;RDMO 2.1.3&lt;/a&gt; (Feb 13, 2024)&lt;/h2&gt;\n&lt;ul&gt;\n&lt;li&gt;Fix the migration of options with additional_input (#912)&lt;/li&gt;\n&lt;li&gt;Fix export urls in management when using BASE_PATH (#915)&lt;/li&gt;\n&lt;/ul&gt;\n&lt;h2&gt;How to upgrade&lt;/h2&gt;\n&lt;p&gt;In case you are upgrading from an RDMO version below 2.0.0 please read these &lt;a href="https://rdmo.readthedocs.io/en/latest/upgrade/index.html#upgrade-to-version-2-0-0"&gt;upgrade instructions&lt;/a&gt; before you proceed.&lt;/p&gt;\n&lt;pre&gt;&lt;code&gt;pip install --upgrade rdmo\npython manage.py upgrade\n&lt;/code&gt;&lt;/pre&gt;', lang=None), Description(value='If you refer to this software in a publication, please cite it as below.', lang=None)], publisher=[Publisher(value='Zenodo', lang=None)], contributor=[], date=[Date(value='2024-02-13', lang=None)], type_value=[TypeType(value='info:eu-repo/semantics/other', lang=None)], format=[], identifier=[Identifier(value='https://doi.org/10.5281/zenodo.10654826', lang=None), Identifier(value='oai:zenodo.org:10654826', lang=None)], source=[], language=[], relation=[Relation(value='https://github.com/rdmorganiser/rdmo/tree/2.1.3', lang=None), Relation(value='https://doi.org/10.5281/zenodo.596581', lang=None)], coverage=[], rights=[Rights(value='info:eu-repo/semantics/openAccess', lang=None), Rights(value='Apache License 2.0', lang=None), Rights(value='http://www.apache.org/licenses/LICENSE-2.0', lang=None)])), about=[])
```

## Features

- Easy harvesting of OAI-compliant interfaces
- Support for all six OAI verbs
- Convenient object representations of OAI items (records, headers, sets, ...) as dataclasses
- Automatic de-serialization of metadata payloads to dataclasses for Dublin Core, DataCite, Marcxml
- Option for ignoring deleted items

## Requirements

[Python](https://www.python.org/downloads/) >= 3.10

`oaipmh-scythe` is built with:

- [httpx](https://github.com/encode/httpx) for issuing HTTP requests
- [xsdata](https://github.com/tefra/xsdata) for parsing XML responses

## Installation

You can install `oaipmh-scythe` via pip from [PyPI][pypi-url]:

```shell-session
$ python -m pip install oaipmh-scythe
```

## Documentation

The [documentation][docs-url] is made with [Material for MkDocs](https://github.com/squidfunk/mkdocs-material) and is
hosted by [GitHub Pages](https://docs.github.com/en/pages).

## Similar Projects

There are a couple of similar projects available on [PyPI](https://pypi.org/search/?q=oai-pmh) and GitHub, e.g. via the
topics [oai-pmh](https://github.com/topics/oai-pmh) and [oai-pmh-client](https://github.com/topics/oai-pmh-client).
Among them are these implementations in Python:

| Project                                                                          | Description                           | Last commit                                                                                           |
| -------------------------------------------------------------------------------- | ------------------------------------- | ----------------------------------------------------------------------------------------------------- |
| [sickle](https://github.com/mloesch/sickle)                                      | `oaipmh-scythe` is a fork of `sickle` | ![last-commit](https://img.shields.io/github/last-commit/mloesch/sickle)                              |
| [pyoai](https://github.com/infrae/pyoai)                                         | `sickle` was inspired by `pyoai`      | ![last-commit](https://img.shields.io/github/last-commit/infrae/pyoai)                                |
| [pyoaiharvester](https://github.com/vphill/pyoaiharvester)                       | oai-pmh harvester CLI                 | ![last-commit](https://img.shields.io/github/last-commit/vphill/pyoaiharvester)                       |
| [ddblabs-ometha](https://github.com/Deutsche-Digitale-Bibliothek/ddblabs-ometha) | oai-pmh harvester with CLI and TUI    | ![last-commit](https://img.shields.io/github/last-commit/Deutsche-Digitale-Bibliothek/ddblabs-ometha) |
| [oai-harvest](https://github.com/bloomonkey/oai-harvest)                         | uses `pyoai` internally               | ![last-commit](https://img.shields.io/github/last-commit/bloomonkey/oai-harvest)                      |
| [oai-pmh-harvester](https://github.com/MITLibraries/oai-pmh-harvester)           | uses `sickle` internally              | ![last-commit](https://img.shields.io/github/last-commit/MITLibraries/oai-pmh-harvester)              |

There are also similar projects available in [Java](https://github.com/topics/oai-pmh-client?l=java) and
[PHP](https://github.com/topics/oai-pmh-client?l=php).

## Acknowledgments

This is a fork of [sickle](https://github.com/mloesch/sickle) which was originally written by Mathias Loesch.

## License

`oaipmh-scythe` is distributed under the terms of the [BSD license](https://spdx.org/licenses/BSD-3-Clause.html).

<!-- Refs -->

[all-downloads-badge]: https://static.pepy.tech/badge/oaipmh-scythe
[ci-badge]: https://github.com/afuetterer/oaipmh-scythe/actions/workflows/main.yml/badge.svg
[ci-workflow]: https://github.com/afuetterer/oaipmh-scythe/actions/workflows/main.yml
[codeql-badge]: https://github.com/afuetterer/oaipmh-scythe/actions/workflows/codeql.yml/badge.svg
[codeql-workflow]: https://github.com/afuetterer/oaipmh-scythe/actions/workflows/codeql.yml
[coverage-badge]: https://img.shields.io/endpoint?url=https://gist.githubusercontent.com/afuetterer/fcb87d45f4d7defdfeffa65eb1d65f63/raw/coverage-badge.json
[docs-badge]: https://github.com/afuetterer/oaipmh-scythe/actions/workflows/docs.yml/badge.svg
[docs-url]: https://afuetterer.github.io/oaipmh-scythe
[docs-workflow]: https://github.com/afuetterer/oaipmh-scythe/actions/workflows/docs.yml
[doi-badge]: https://zenodo.org/badge/DOI/10.5281/zenodo.11125401.svg
[doi-url]: https://doi.org/10.5281/zenodo.11125401
[hatch]: https://github.com/pypa/hatch
[hatch-badge]: https://img.shields.io/badge/%F0%9F%A5%9A-Hatch-4051b5.svg
[license]: https://spdx.org/licenses/BSD-3-Clause.html
[license-badge]: https://img.shields.io/badge/License-BSD_3--Clause-blue.svg
[monthly-downloads-badge]: https://static.pepy.tech/badge/oaipmh-scythe/month
[mypy]: https://mypy-lang.org
[mypy-badge]: https://img.shields.io/badge/types-mypy-blue.svg
[pepy-tech-url]: https://pepy.tech/project/oaipmh-scythe
[pre-commit-ci-badge]: https://results.pre-commit.ci/badge/github/afuetterer/oaipmh-scythe/main.svg
[pre-commit-ci-status]: https://results.pre-commit.ci/latest/github/afuetterer/oaipmh-scythe/main
[pypi-python-versions-badge]: https://img.shields.io/pypi/pyversions/oaipmh-scythe.svg?logo=python&label=Python
[pypi-url]: https://pypi.org/project/oaipmh-scythe/
[pypi-version-badge]: https://img.shields.io/pypi/v/oaipmh-scythe.svg?logo=pypi&label=PyPI
[ruff]: https://github.com/astral-sh/ruff
[ruff-badge]: https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/charliermarsh/ruff/main/assets/badge/v2.json
[scorecard-badge]: https://api.securityscorecards.dev/projects/github.com/afuetterer/oaipmh-scythe/badge
[scorecard-url]: https://securityscorecards.dev/viewer/?uri=github.com/afuetterer/oaipmh-scythe
