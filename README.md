# oaipmh-scythe: A Scythe for harvesting OAI-PMH repositories.

Welcome to `oaipmh-scythe`, an updated and modernized version of the original
[sickle](https://github.com/mloesch/sickle), now with additional features and ongoing maintenance.

| __CI__      | [![pre-commit.ci status][pre-commit-ci-badge]][pre-commit-ci-status] [![ci][ci-badge]][ci-workflow] [![coverage][coverage-badge]][ci-workflow]                                                                                        |
| :---------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| __Docs__    | [![docs][docs-badge]][docs-workflow]                                                                                                                                                                                                  |
| __Package__ | [![pypi-version][pypi-version-badge]][pypi-url] [![pypi-python-versions][pypi-python-versions-badge]][pypi-url] [![all-downloads][all-downloads-badge]][pepy-tech-url] [![monthly-downloads][monthly-downloads-badge]][pepy-tech-url] |
| __Meta__    | [![OpenSSF Scorecard][scorecard-badge]][scorecard-url] [![hatch][hatch-badge]][hatch] [![ruff][ruff-badge]][ruff] [![mypy][mypy-badge]][mypy] [![License][license-badge]][license]                                                    |

`oaipmh-scythe` is a lightweight [OAI-PMH](http://www.openarchives.org/OAI/openarchivesprotocol.html) client library
written in Python. It has been designed for conveniently retrieving data from OAI interfaces the Pythonic way:

```python
from oaipmh_scythe import Scythe

with Scythe("https://zenodo.org/oai2d") as scythe:
    records = scythe.list_records()
    next(records)
# <Record oai:zenodo.org:4574771>
```

## Features

- Easy harvesting of OAI-compliant interfaces
- Support for all six OAI verbs
- Convenient object representations of OAI items (records, headers, sets, ...)
- Automatic de-serialization of Dublin Core-encoded metadata payloads to Python dictionaries
- Option for ignoring deleted items

## Requirements

[Python](https://www.python.org/downloads/) >= 3.10

`oaipmh-scythe` is built with:

- [httpx](https://github.com/encode/httpx) for issuing HTTP requests
- [lxml](https://github.com/lxml/lxml) for parsing XML responses

## Installation

You can install `oaipmh-scythe` via pip from [PyPI][pypi-url]:

```console
python -m pip install oaipmh-scythe
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
[coverage-badge]: https://img.shields.io/endpoint?url=https://gist.githubusercontent.com/afuetterer/fcb87d45f4d7defdfeffa65eb1d65f63/raw/coverage-badge.json
[docs-badge]: https://github.com/afuetterer/oaipmh-scythe/actions/workflows/docs.yml/badge.svg
[docs-url]: https://afuetterer.github.io/oaipmh-scythe
[docs-workflow]: https://github.com/afuetterer/oaipmh-scythe/actions/workflows/docs.yml
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
