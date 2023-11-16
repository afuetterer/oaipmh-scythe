# Changelog

All notable changes to this project will be documented in this file.

This project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html). See
[conventional commits](https://www.conventionalcommits.org/en/v1.0.0/) for commit guidelines.


## [Unreleased](https://github.com/afuetterer/oaipmh-scythe/compare/0.8.0...main)


## [0.8.0](https://github.com/afuetterer/oaipmh-scythe/compare/0.7.0...0.8.0) (2023-11-YY)

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
