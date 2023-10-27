# Changelog

All notable changes to this project will be documented in this file.

This project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html). See
[conventional commits](https://www.conventionalcommits.org/en/v1.0.0/) for commit guidelines.

## [Unreleased](https://github.com/afuetterer/oaipmh-scythe/compare/0.8.0...main)

      ## [0.8.0](https://github.com/afuetterer/oaipmh-scythe/compare/0.7.1...0.8.0) (2023-10-27)
        ### Feature
          * feat: psr ([`a8cf066`](https://github.com/afuetterer/oaipmh-scythe/commit/a8cf06607a2f29bfff3d56ef7a62d282da0be5d3))
        ### Fix
          * fix: psr ([`1706597`](https://github.com/afuetterer/oaipmh-scythe/commit/1706597dd275f22a821e8710e08b681576f5ec20))
      ## [0.7.1](https://github.com/afuetterer/oaipmh-scythe/compare/0.7.0...0.7.1) (2023-10-27)
        ### Documentation
          * docs(readme): add license badge to readme ([`2446ba4`](https://github.com/afuetterer/oaipmh-scythe/commit/2446ba4a3bafc43412f828b773d49231fc2e69c2))
          * docs: add contributor guide ([`6138ff1`](https://github.com/afuetterer/oaipmh-scythe/commit/6138ff12a657e4dea63efa29b57116671b4d4b29))
          * docs(api): update api docs ([`e46dd83`](https://github.com/afuetterer/oaipmh-scythe/commit/e46dd839469f812fe3009ecd8468f852db55f34a))
          * docs(readme): update code example in readme ([`fe23cd7`](https://github.com/afuetterer/oaipmh-scythe/commit/fe23cd7674cd4de5b386bdb5391d3a8d4423f776))
          * docs(tutorial): update tutorial ([`7e17382`](https://github.com/afuetterer/oaipmh-scythe/commit/7e173827c0c9e40873500d484c9603d7f03c233b))
          * docs: update license file ([`fbfa256`](https://github.com/afuetterer/oaipmh-scythe/commit/fbfa2565fcea659d069f25779ec9d9927173f304))
          * docs(readme): remove black badge ([`869d072`](https://github.com/afuetterer/oaipmh-scythe/commit/869d072c4beca367d45ef2ced1628fa969100803))
          * docs: add dark mode switch to mkdocs config ([`4b732c4`](https://github.com/afuetterer/oaipmh-scythe/commit/4b732c4d4c872c6cf8d8a62a5325a856d83eabc0))
          * docs: rename scythe to oaipmh-scythe (__init__.py) ([`ea11d35`](https://github.com/afuetterer/oaipmh-scythe/commit/ea11d3574576c3d395ab7f1298a3330891b9454a))
          * docs: set up documentation with mkdocs (#21) ([`3945eb7`](https://github.com/afuetterer/oaipmh-scythe/commit/3945eb78e1cc7728eaff2bd8e50da8afb4545521))
          * docs: add ci badge to readme ([`b6541ef`](https://github.com/afuetterer/oaipmh-scythe/commit/b6541ef9cba004d70e76e5ddfdebb7ffa7b30102))
          * docs: add hatch environment for linting ([`a409013`](https://github.com/afuetterer/oaipmh-scythe/commit/a4090133aea51f441a48fedf1a4255f5485b1af1))
          * docs: update authors file ([`86c07c3`](https://github.com/afuetterer/oaipmh-scythe/commit/86c07c3fb1b4c61e07b27793997cb9f5433283a8))
          * docs: update readme ([`5df475e`](https://github.com/afuetterer/oaipmh-scythe/commit/5df475e063be5282378dffd723718053e731fd2a))
          * docs: update changelog ([`69b3c7e`](https://github.com/afuetterer/oaipmh-scythe/commit/69b3c7e302170c8e72a91c3d337860980709ec38))
        ### Fix
          * fix: changelog ([`db39285`](https://github.com/afuetterer/oaipmh-scythe/commit/db39285db745daf5d3790fdbae9986de72c9b593))
        ### Test
          * test: ignore deprecation warnings ([`9fa640d`](https://github.com/afuetterer/oaipmh-scythe/commit/9fa640dbdacbe3c7a9776f91aa6705b4eaa8b7f5))
          * test: switch to pytest tests ([`2904283`](https://github.com/afuetterer/oaipmh-scythe/commit/29042833388e0cb94825c60050ad6f0ade507003))

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

## [0.6.2](https://github.com/afuetterer/oaipmh-scythe/compare/v0.6.1...0.6.2) (2017-08-11)

- missing datestamp and identifier elements in record header don\'t break harvesting
- lxml resolve_entities disabled (<http://lxml.de/FAQ.html#how-do-i-use-lxml-safely-as-a-web-service-endpoint>)

## [0.6.1](https://github.com/afuetterer/oaipmh-scythe/compare/v0.5...v0.6.1) (2016-11-13)

- it is now possible to pass any keyword arguments to requests
- the encoding used to decode the server response can be overridden

## [0.5](https://github.com/afuetterer/oaipmh-scythe/compare/v0.4...v0.5) (2015-11-12)

- support for Python 3
- consider resumption tokens with empty tag bodies

## [0.4](https://github.com/afuetterer/oaipmh-scythe/compare/v0.3...v0.4) (2015-05-31)

- bug fix: resumptionToken parameter is exclusive
- added support for harvesting complete OAI-XML responses

## [0.3](https://github.com/afuetterer/oaipmh-scythe/compare/v0.2...v0.3) (2013-04-17)

- added support for protected OAI interfaces (basic authentication)
- made class mapping for OAI elements configurable
- added options for HTTP timeout and max retries
- added handling of HTTP 503 responses

## 0.2 (2013-02-26)

- OAI items are now represented as their own classes instead of XML elements
- library raises OAI-specific exceptions
- made lxml a required dependency

## 0.1 (2013-02-20)

First public release.
