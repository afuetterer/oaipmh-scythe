# Changelog

All notable changes to this project will be documented in this file.

This project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html). See
[conventional commits](https://www.conventionalcommits.org/en/v1.0.0/) for commit guidelines.


## [Unreleased](https://github.com/afuetterer/oaipmh-scythe/compare/0.10.0...main)


## [0.10.0](https://github.com/afuetterer/oaipmh-scythe/compare/0.9.0...0.10.0) (2024-01-22)

### Breaking Changes

- make request arguments explicit (#212) ([`c61fab3`](https://github.com/afuetterer/oaipmh-scythe/commit/c61fab3126a33d0d793d5a07f0c88b37e83f0378))
- remove request_args from scythe class and _request method (#199) ([`2be27aa`](https://github.com/afuetterer/oaipmh-scythe/commit/2be27aa837e4d9590150e6e36492d2910a88d7c9))
- drop support for oai-pmh version 1.0 (#183) ([`8644c4b`](https://github.com/afuetterer/oaipmh-scythe/commit/8644c4b82abd91f4d847912fad811c0936f5d0b1))
- drop support for python &lt; 3.10 (#180) ([`cb3b99c`](https://github.com/afuetterer/oaipmh-scythe/commit/cb3b99cd1946b577ede8f5b471f32a3b1508c5ad))

### Code Refactoring

- **client:** remove obsolete is_error_code() (#177) ([`1e6dfe1`](https://github.com/afuetterer/oaipmh-scythe/commit/1e6dfe19487874969f0d0c76ca69934d66dd1446))
- add accept text/xml headers to client config (#155) ([`4d92818`](https://github.com/afuetterer/oaipmh-scythe/commit/4d92818573d39797fd83544e942b5e186db4bdf2))

### Testing

- update getrecord example (#200) ([`77c8ee6`](https://github.com/afuetterer/oaipmh-scythe/commit/77c8ee64c58f4bbbb976139fed5c44666e644c99))

### Documentation

- update author name ([`5f286e1`](https://github.com/afuetterer/oaipmh-scythe/commit/5f286e1006f94ff7559586e0541a4d47f4f9d5a1))
- **readme:** update required python version ([`8237d2c`](https://github.com/afuetterer/oaipmh-scythe/commit/8237d2cfb3add763d199ba40a3da65fa9e91ddd7))
- **readme:** restyle project metadata table (#214) ([`e2487cc`](https://github.com/afuetterer/oaipmh-scythe/commit/e2487ccf9c6887ada9ee684e577fd1c5bef3afba))
- **readme:** rephrase introduction about fork (#202) ([`de65418`](https://github.com/afuetterer/oaipmh-scythe/commit/de654186aefbdbb075a64ad1986f9f489cd6e9a0))
- add more alternatives (#192) ([`5062a38`](https://github.com/afuetterer/oaipmh-scythe/commit/5062a3887fe5c72c44c918dab8d5ccc3e534e8e8))
- add full changelog to release notes (#149) ([`19a98f5`](https://github.com/afuetterer/oaipmh-scythe/commit/19a98f5e498016989e506bfa29384143dfc3c781))

## [0.9.0](https://github.com/afuetterer/oaipmh-scythe/compare/0.8.0...0.9.0) (2023-11-18)

### Features

- add context manager to scythe class (#144) ([`d660f77`](https://github.com/afuetterer/oaipmh-scythe/commit/d660f77715b35a847828929b63373f9a759d5a59))

### Performance improvements

- set up internal httpx.Client (#140) ([`969e868`](https://github.com/afuetterer/oaipmh-scythe/commit/969e868ab844be62db0fadef2326aa51d6682a58))

### Documentation

- **readme:** add similar projects section ([`f45781f`](https://github.com/afuetterer/oaipmh-scythe/commit/f45781f405b5122507ef92d0f0e679c7709d5bc8))
- **readme:** add acknowledgments section ([`20ecd64`](https://github.com/afuetterer/oaipmh-scythe/commit/20ecd641831a7a4dcd457726490c5c5591d022a1))
- **readme:** add short descriptions of requirements ([`a573150`](https://github.com/afuetterer/oaipmh-scythe/commit/a573150ff8d16c14c2d4271b912387172f0225cd))
- remove outdated credits page ([`47c80e8`](https://github.com/afuetterer/oaipmh-scythe/commit/47c80e8fbd99281193a175dcd2c905a1ff0bfb8b))
- rename api docs page to client ([`cf77d57`](https://github.com/afuetterer/oaipmh-scythe/commit/cf77d5757e1a8a4ddfecb3c22fba01dfddf3bd79))
- change breaking changes heading (#138) ([`69a8572`](https://github.com/afuetterer/oaipmh-scythe/commit/69a8572345a2f582ad6ec01a434df5dfc327f037))


## [0.8.0](https://github.com/afuetterer/oaipmh-scythe/compare/0.7.0...0.8.0) (2023-11-16)

Note: Rename project to oaipmh-scythe when forking it from [mloesch/sickle](https://github.com/mloesch/sickle) to
[afuetterer/oaipmh-scythe](https://github.com/afuetterer/oaipmh-scythe)

### Breaking Changes

- drop support for Python 2
- drop support for EOL Python 3.7 and below
- rename Sickle class to Scythe to reflect the change of the project name
- switch to PEP8 compliant names for methods (ListRecords() -> list_records())
- remove .next() method from iterator classes

### Features

- set up default custom user agent (oaipmh-scythe/{version})

### Performance Improvements

- make iterator classes yield their responses

### Code Refactoring

- switch from requests to httpx
- make BaseOAIIterator an ABC
- move version information to __about__.py
- add a custom base exception

### Testing

- switch from nose to pytest
- add tests for Python 3.8 - 3.12 in CI
- use canned responses from Zenodo to test harvesting logic (vcr.py)

### Documentation

- update license text
- update authors and contributors
- update copyright notice in src files
- add contributor guide
- add security policy
- add issue and pull request templates
- add custom GitHub labels
- switch from Sphinx to mkdocs-material
- switch from Read the Docs to GitHub pages
- switch from reStructuredText to Markdown
- switch to Zenodo for harvesting examples
- update README badges

### Other

- switch from Travis CI to Github actions for CI
- add scheduled dependency updates with Dependabot
- add pre-commit hooks (e.g. ruff, mypy)
- switch to src layout
- switch from setup.py to pyproject.toml
- switch to hatch for project setup
- add type annotations
- switch to Google style docstrings
- rename first tags of sickle project for consistency (e.g. v0.5 -> 0.5.0)
- enable CodeQL scanning
- add OpenSSF Scorecard report

## [0.7.0](https://github.com/afuetterer/oaipmh-scythe/compare/0.6.5...0.7.0) (2020-05-17)

- method for record metadata extraction has been extracted (`Record.get_metadata()`) to make subclassing easier ([mloesch/sickle#38](https://github.com/mloesch/sickle/pull/38))
- retryable HTTP status codes and default wait time between retries can be customized ([mloesch/sickle#21](https://github.com/mloesch/sickle/issues/21) [mloesch/sickle#41](https://github.com/mloesch/sickle/pull/41))
- retry logic has been fixed: `max_retries` parameter now refers to no. of retries, not counting the initial request anymore
- the default number of HTTP retries has been set to 0 (= no retries)
- fix for [mloesch/sickle#39](https://github.com/mloesch/sickle/pull/39)

## [0.6.5](https://github.com/afuetterer/oaipmh-scythe/compare/0.6.4...0.6.5) (2020-01-12)

- fix: repr methods where causing an exception on Python 3 ([mloesch/sickle#30](https://github.com/mloesch/sickle/issues/30))

## [0.6.4](https://github.com/afuetterer/oaipmh-scythe/compare/0.6.3...0.6.4) (2018-10-02)

- fix: resumption token with empty body indicates last response ([mloesch/sickle#25](https://github.com/mloesch/sickle/issues/25))

## [0.6.3](https://github.com/afuetterer/oaipmh-scythe/compare/0.6.2...0.6.3) (2018-04-08)

- fix unicode problems (issues 20 & 22)

## [0.6.2](https://github.com/afuetterer/oaipmh-scythe/compare/0.6.1...0.6.2) (2017-08-11)

- missing datestamp and identifier elements in record header don\'t break harvesting
- lxml resolve_entities disabled (<http://lxml.de/FAQ.html#how-do-i-use-lxml-safely-as-a-web-service-endpoint>)

## [0.6.1](https://github.com/afuetterer/oaipmh-scythe/compare/0.5.0...0.6.1) (2016-11-13)

- it is now possible to pass any keyword arguments to requests
- the encoding used to decode the server response can be overridden

## [0.5.0](https://github.com/afuetterer/oaipmh-scythe/compare/0.4.0...0.5.0) (2015-11-12)

- support for Python 3
- consider resumption tokens with empty tag bodies

## [0.4.0](https://github.com/afuetterer/oaipmh-scythe/compare/0.3.0...0.4.0) (2015-05-31)

- bug fix: resumptionToken parameter is exclusive
- added support for harvesting complete OAI-XML responses

## [0.3.0](https://github.com/afuetterer/oaipmh-scythe/compare/0.2.0...0.3.0) (2013-04-17)

- added support for protected OAI interfaces (basic authentication)
- made class mapping for OAI elements configurable
- added options for HTTP timeout and max retries
- added handling of HTTP 503 responses

## 0.2.0 (2013-02-26)

- OAI items are now represented as their own classes instead of XML elements
- library raises OAI-specific exceptions
- made lxml a required dependency

## 0.1.0 (2013-02-20)

First public release.
