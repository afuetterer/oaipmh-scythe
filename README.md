# oaipmh-scythe: OAI-PMH for Humans

This is a community maintained fork of the original [sickle](https://github.com/mloesch/sickle).

|     |     |
| --- | --- |
| CI | [![ci][ci-badge]][ci-workflow] [![coverage][coverage-badge]][ci-workflow] |
| Docs | [![docs][docs-badge]][docs-workflow] |
| Meta | [![OpenSSF Scorecard][scorecard-badge]][scorecard-url] [![hatch][hatch-badge]][hatch] [![pre-commit enabled][pre-commit-badge]][pre-commit] [![ruff][ruff-badge]][ruff] [![mypy][mypy-badge]][mypy] [![License][license-badge]][license] |

oaipmh-scythe is a lightweight [OAI-PMH](http://www.openarchives.org/OAI/openarchivesprotocol.html)
client library written in Python. It has been designed for conveniently retrieving data from OAI interfaces the Pythonic way:

```python
from oaipmh_scythe import Scythe
scythe = Scythe("https://zenodo.org/oai2d")
records = scythe.list_records(metadataPrefix="oai_dc")
next(records)
# <Record oai:zenodo.org:4574771>
```

## Features

- Easy harvesting of OAI-compliant interfaces
- Support for all six OAI verbs
- Convenient object representations of OAI items (records, headers, sets, \...)
- Automatic de-serialization of Dublin Core-encoded metadata payloads to Python dictionaries
- Option for ignoring deleted items

## Requirements

[Python](https://www.python.org/downloads/) >= 3.8

oaipmh-scythe is built with:
- [httpx](https://github.com/encode/httpx)
- [lxml](https://github.com/lxml/lxml)

## Installation

```console
python -m pip install oaipmh-scythe
```

## Documentation

The [documentation][docs-url] is made with [Material for MkDocs](https://github.com/squidfunk/mkdocs-material) and is hosted by [GitHub Pages](https://docs.github.com/en/pages).

## License

oaipmh-scythe is distributed under the terms of the [BSD](https://spdx.org/licenses/BSD-3-Clause.html) license.

<!-- Markdown links -->
<!-- dynamic -->
[ci-workflow]: https://github.com/afuetterer/oaipmh-scythe/actions/workflows/main.yml
[ci-badge]: https://github.com/afuetterer/oaipmh-scythe/actions/workflows/main.yml/badge.svg
[coverage-badge]: https://img.shields.io/endpoint?url=https://gist.githubusercontent.com/afuetterer/fcb87d45f4d7defdfeffa65eb1d65f63/raw/coverage-badge.json
[docs-url]: https://afuetterer.github.io/oaipmh-scythe
[docs-workflow]: https://github.com/afuetterer/oaipmh-scythe/actions/workflows/docs.yml
[docs-badge]: https://github.com/afuetterer/oaipmh-scythe/actions/workflows/docs.yml/badge.svg
[scorecard-url]: https://securityscorecards.dev/viewer/?uri=github.com/afuetterer/oaipmh-scythe
[scorecard-badge]: https://api.securityscorecards.dev/projects/github.com/afuetterer/oaipmh-scythe/badge
<!-- static -->
[license]: https://spdx.org/licenses/BSD-3-Clause.html
[license-badge]: https://img.shields.io/badge/License-BSD_3--Clause-blue.svg
[hatch]: https://github.com/pypa/hatch
[hatch-badge]: https://img.shields.io/badge/%F0%9F%A5%9A-Hatch-4051b5.svg
[pre-commit]: https://pre-commit.com/
[pre-commit-badge]: https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white
[ruff]: https://github.com/charliermarsh/ruff
[ruff-badge]: https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/charliermarsh/ruff/main/assets/badge/v2.json
[mypy]: https://mypy-lang.org
[mypy-badge]: https://img.shields.io/badge/types-mypy-blue.svg
[test-pypi]: https://test.pypi.org/
[pip]: https://pip.pypa.io/
