# Changelog

All notable changes to this project will be documented in this file.

This project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html). See
[conventional commits](https://www.conventionalcommits.org/en/v1.0.0/) for commit guidelines.

## [0.14.2](https://github.com/afuetterer/oaipmh-scythe/compare/0.14.1..0.14.2) (2026-04-10)

### Performance improvements

- pre-compile regex pattern in get_namespace ([#451](https://github.com/afuetterer/oaipmh-scythe/pull/451)) ([42bd6b1](https://github.com/afuetterer/oaipmh-scythe/commit/42bd6b1eb39131d20281be0d445962101ba347b8))

## [0.14.1](https://github.com/afuetterer/oaipmh-scythe/compare/0.14.0..0.14.1) (2026-04-10)

### Bug Fixes

- **client:** add application/xml to headers ([#462](https://github.com/afuetterer/oaipmh-scythe/pull/462)) ([0d65ebe](https://github.com/afuetterer/oaipmh-scythe/commit/0d65ebe91e843f752fe8263c2e8a61b22afcf213))

### Documentation

- **readme:** add uv install instructions ([#460](https://github.com/afuetterer/oaipmh-scythe/pull/460)) ([1d298e7](https://github.com/afuetterer/oaipmh-scythe/commit/1d298e7528d54d0f8d2ff6ed1f67c42073be4eed))

## [0.14.0](https://github.com/afuetterer/oaipmh-scythe/compare/0.13.0..0.14.0) (2026-02-15)

### Features

- add support for python 3.14 ([#433](https://github.com/afuetterer/oaipmh-scythe/pull/433)) ([9614533](https://github.com/afuetterer/oaipmh-scythe/commit/9614533a0f5b9753638a1fac82dafbb856899b97))

### Documentation

- **citation:** add concept doi to citation.cff ([#368](https://github.com/afuetterer/oaipmh-scythe/pull/368)) ([41e3835](https://github.com/afuetterer/oaipmh-scythe/commit/41e38350fe42a0281a993adf1daa7e0b81232a4b))
- **readme:** add doi badge ([#367](https://github.com/afuetterer/oaipmh-scythe/pull/367)) ([609211d](https://github.com/afuetterer/oaipmh-scythe/commit/609211da61f2b99c3856dd04e927ae3178cfde0b))
- set up versioned docs with mike ([#374](https://github.com/afuetterer/oaipmh-scythe/pull/374)) ([347f7dc](https://github.com/afuetterer/oaipmh-scythe/commit/347f7dc96873bd08d6d5c9770e0a1c93940c5800))

## [0.13.0](https://github.com/afuetterer/oaipmh-scythe/compare/0.12.1..0.13.0) (2024-05-07)

### Features

- **client:** make numeric arguments accept 'int | float' ([#366](https://github.com/afuetterer/oaipmh-scythe/pull/366)) ([b53bbed](https://github.com/afuetterer/oaipmh-scythe/commit/b53bbed65440f974b6c09b161a66a303fb57c3bd))

### Documentation

- **readme:** add codeql badge ([#365](https://github.com/afuetterer/oaipmh-scythe/pull/365)) ([eca3e3b](https://github.com/afuetterer/oaipmh-scythe/commit/eca3e3b221bebdb47d72112c0e5f529298eadf77))
- **tutorial:** fix typo ([#353](https://github.com/afuetterer/oaipmh-scythe/pull/353)) ([65f75b8](https://github.com/afuetterer/oaipmh-scythe/commit/65f75b82515cc772d82cf745b8763cb291d3ff2a))
- add references to exceptions in docstrings ([#351](https://github.com/afuetterer/oaipmh-scythe/pull/351)) ([4df8491](https://github.com/afuetterer/oaipmh-scythe/commit/4df8491502bc65ae0589c6686b71756d205f4411))

## [0.12.1](https://github.com/afuetterer/oaipmh-scythe/compare/0.12.0..0.12.1) (2024-04-25)

### Bug Fixes

- **exceptions:** rename nometadataformat to nometadataformats ([#349](https://github.com/afuetterer/oaipmh-scythe/pull/349)) ([255acb2](https://github.com/afuetterer/oaipmh-scythe/commit/255acb257a35533e78b0eb1aed85704c386e4e0a))

### Code Refactoring

- **client:** set up explicit default encoding in httpx.Client ([#330](https://github.com/afuetterer/oaipmh-scythe/pull/330)) ([25ef4cb](https://github.com/afuetterer/oaipmh-scythe/commit/25ef4cbde2488426b7736e1240b5de798bd6fe34))
- **iterator:** rename params argument to query in itemiterator ([#329](https://github.com/afuetterer/oaipmh-scythe/pull/329)) ([1de6cd5](https://github.com/afuetterer/oaipmh-scythe/commit/1de6cd57efbf64dc44762243024b1b81bdcaac32))
- make all exceptions available in the main init file ([#348](https://github.com/afuetterer/oaipmh-scythe/pull/348)) ([bad60ff](https://github.com/afuetterer/oaipmh-scythe/commit/bad60ff61f6a8ceb96134e97e321eca93cbc6eab))

### Documentation

- add api reference pages for all modules ([#344](https://github.com/afuetterer/oaipmh-scythe/pull/344)) ([8578031](https://github.com/afuetterer/oaipmh-scythe/commit/8578031a21fd35ae7f8e0cd66fc955b8cc84bea0))
- add python standard library inventory ([#338](https://github.com/afuetterer/oaipmh-scythe/pull/338)) ([20d176c](https://github.com/afuetterer/oaipmh-scythe/commit/20d176cc1bbf00e40f19c836681d3bb6b46f5390))

## [0.12.0](https://github.com/afuetterer/oaipmh-scythe/compare/0.11.0..0.12.0) (2024-04-04)

### Features

- **client:** add authentication parameter ([#316](https://github.com/afuetterer/oaipmh-scythe/pull/316)) ([035c0fe](https://github.com/afuetterer/oaipmh-scythe/commit/035c0fe4af20c1a749ce3dc02d1f5174aa13c57c))

### Documentation

- **readme:** add download badges to readme ([#294](https://github.com/afuetterer/oaipmh-scythe/pull/294)) ([c375ea9](https://github.com/afuetterer/oaipmh-scythe/commit/c375ea935e226b3fc8a16ae9e2e023b7713c32b5))
- add pypi project version to release notes template ([#282](https://github.com/afuetterer/oaipmh-scythe/pull/282)) ([c9d37ea](https://github.com/afuetterer/oaipmh-scythe/commit/c9d37ea6e698f2706ac6cf893e9e97f4f2cd1c3c))
- update environment section in bug report template ([#281](https://github.com/afuetterer/oaipmh-scythe/pull/281)) ([a2c225a](https://github.com/afuetterer/oaipmh-scythe/commit/a2c225a3fc38ada61386a6abd8310bec79c6e482))
- add ci to types of changes in pr template ([#272](https://github.com/afuetterer/oaipmh-scythe/pull/272)) ([f2745e7](https://github.com/afuetterer/oaipmh-scythe/commit/f2745e74eaf2714eee8b6133924d15b050cc9ac9))
- rename code of conduct ([#270](https://github.com/afuetterer/oaipmh-scythe/pull/270)) ([1994bf3](https://github.com/afuetterer/oaipmh-scythe/commit/1994bf39cf76321dad509c189d1b7757f7bd21fb))
- add license headers to documentation ([#258](https://github.com/afuetterer/oaipmh-scythe/pull/258)) ([63aa318](https://github.com/afuetterer/oaipmh-scythe/commit/63aa318d94607571e4852315c310c71593257791))

## [0.11.0](https://github.com/afuetterer/oaipmh-scythe/compare/0.10.0..0.11.0) (2024-01-25)

### Features

- set up logging of http requests ([#250](https://github.com/afuetterer/oaipmh-scythe/pull/250)) ([3df5ba1](https://github.com/afuetterer/oaipmh-scythe/commit/3df5ba1c3247b38bc8fa0414b070296fc309a5ef))

### Documentation

- **readme:** add pypi downloads badge to readme ([#243](https://github.com/afuetterer/oaipmh-scythe/pull/243)) ([1f87b18](https://github.com/afuetterer/oaipmh-scythe/commit/1f87b18913f4ffc3c97303f41b577f402eabece7))
- **readme:** add pypi package information to readme ([#237](https://github.com/afuetterer/oaipmh-scythe/pull/237)) ([ada4dcf](https://github.com/afuetterer/oaipmh-scythe/commit/ada4dcfc84b1a7591098fb343f30815aa7efa7e6))
- **readme:** add minor improvements to readme ([#234](https://github.com/afuetterer/oaipmh-scythe/pull/234)) ([9871491](https://github.com/afuetterer/oaipmh-scythe/commit/9871491c065d9b98c06c71f83df7ae3e1fed2fa0))
- update python version in contributor guide ([#248](https://github.com/afuetterer/oaipmh-scythe/pull/248)) ([81366d8](https://github.com/afuetterer/oaipmh-scythe/commit/81366d8ffa25eceec5c18fa487a4705ccbb58d6a))
- add initial citation.cff ([#240](https://github.com/afuetterer/oaipmh-scythe/pull/240)) ([135a433](https://github.com/afuetterer/oaipmh-scythe/commit/135a4332bd7f0d0ae79406990a6d2e095618dd4f))
- make urls in docstrings clickable ([#233](https://github.com/afuetterer/oaipmh-scythe/pull/233)) ([55bf699](https://github.com/afuetterer/oaipmh-scythe/commit/55bf699998483e6b43908242bc59dc7834bcb977))

## [0.10.0](https://github.com/afuetterer/oaipmh-scythe/compare/0.9.0..0.10.0) (2024-01-22)

### Features

-  [**breaking**]make request arguments explicit ([#212](https://github.com/afuetterer/oaipmh-scythe/pull/212)) ([c61fab3](https://github.com/afuetterer/oaipmh-scythe/commit/c61fab3126a33d0d793d5a07f0c88b37e83f0378))
-  [**breaking**]remove request_args from scythe class and _request method ([#199](https://github.com/afuetterer/oaipmh-scythe/pull/199)) ([2be27aa](https://github.com/afuetterer/oaipmh-scythe/commit/2be27aa837e4d9590150e6e36492d2910a88d7c9))
-  [**breaking**]drop support for oai-pmh version 1.0 ([#183](https://github.com/afuetterer/oaipmh-scythe/pull/183)) ([8644c4b](https://github.com/afuetterer/oaipmh-scythe/commit/8644c4b82abd91f4d847912fad811c0936f5d0b1))
-  [**breaking**]drop support for python < 3.10 ([#180](https://github.com/afuetterer/oaipmh-scythe/pull/180)) ([cb3b99c](https://github.com/afuetterer/oaipmh-scythe/commit/cb3b99cd1946b577ede8f5b471f32a3b1508c5ad))

### Code Refactoring

- **client:** remove obsolete is_error_code() ([#177](https://github.com/afuetterer/oaipmh-scythe/pull/177)) ([1e6dfe1](https://github.com/afuetterer/oaipmh-scythe/commit/1e6dfe19487874969f0d0c76ca69934d66dd1446))
- add accept text/xml headers to client config ([#155](https://github.com/afuetterer/oaipmh-scythe/pull/155)) ([4d92818](https://github.com/afuetterer/oaipmh-scythe/commit/4d92818573d39797fd83544e942b5e186db4bdf2))

### Testing

- update getrecord example ([#200](https://github.com/afuetterer/oaipmh-scythe/pull/200)) ([77c8ee6](https://github.com/afuetterer/oaipmh-scythe/commit/77c8ee64c58f4bbbb976139fed5c44666e644c99))

### Documentation

- **readme:** update required python version ([8237d2c](https://github.com/afuetterer/oaipmh-scythe/commit/8237d2cfb3add763d199ba40a3da65fa9e91ddd7))
- **readme:** restyle project metadata table ([#214](https://github.com/afuetterer/oaipmh-scythe/pull/214)) ([e2487cc](https://github.com/afuetterer/oaipmh-scythe/commit/e2487ccf9c6887ada9ee684e577fd1c5bef3afba))
- **readme:** rephrase introduction about fork ([#202](https://github.com/afuetterer/oaipmh-scythe/pull/202)) ([de65418](https://github.com/afuetterer/oaipmh-scythe/commit/de654186aefbdbb075a64ad1986f9f489cd6e9a0))
- update author name ([5f286e1](https://github.com/afuetterer/oaipmh-scythe/commit/5f286e1006f94ff7559586e0541a4d47f4f9d5a1))
- add more alternatives ([#192](https://github.com/afuetterer/oaipmh-scythe/pull/192)) ([5062a38](https://github.com/afuetterer/oaipmh-scythe/commit/5062a3887fe5c72c44c918dab8d5ccc3e534e8e8))
- add full changelog to release notes ([#149](https://github.com/afuetterer/oaipmh-scythe/pull/149)) ([19a98f5](https://github.com/afuetterer/oaipmh-scythe/commit/19a98f5e498016989e506bfa29384143dfc3c781))

## [0.9.0](https://github.com/afuetterer/oaipmh-scythe/compare/0.8.0..0.9.0) (2023-11-18)

### Features

- add context manager to scythe class ([#144](https://github.com/afuetterer/oaipmh-scythe/pull/144)) ([d660f77](https://github.com/afuetterer/oaipmh-scythe/commit/d660f77715b35a847828929b63373f9a759d5a59))

### Performance improvements

- set up internal httpx.Client ([#140](https://github.com/afuetterer/oaipmh-scythe/pull/140)) ([969e868](https://github.com/afuetterer/oaipmh-scythe/commit/969e868ab844be62db0fadef2326aa51d6682a58))

### Documentation

- **readme:** add similar projects section ([f45781f](https://github.com/afuetterer/oaipmh-scythe/commit/f45781f405b5122507ef92d0f0e679c7709d5bc8))
- **readme:** add acknowledgments section ([20ecd64](https://github.com/afuetterer/oaipmh-scythe/commit/20ecd641831a7a4dcd457726490c5c5591d022a1))
- **readme:** add short descriptions of requirements ([a573150](https://github.com/afuetterer/oaipmh-scythe/commit/a573150ff8d16c14c2d4271b912387172f0225cd))
- remove outdated credits page ([47c80e8](https://github.com/afuetterer/oaipmh-scythe/commit/47c80e8fbd99281193a175dcd2c905a1ff0bfb8b))
- rename api docs page to client ([cf77d57](https://github.com/afuetterer/oaipmh-scythe/commit/cf77d5757e1a8a4ddfecb3c22fba01dfddf3bd79))
- change breaking changes heading ([#138](https://github.com/afuetterer/oaipmh-scythe/pull/138)) ([69a8572](https://github.com/afuetterer/oaipmh-scythe/commit/69a8572345a2f582ad6ec01a434df5dfc327f037))

## [0.8.0](https://github.com/afuetterer/oaipmh-scythe/compare/0.7.0..0.8.0) (2023-11-16)

Note: Rename project to oaipmh-scythe when forking it from [mloesch/sickle](https://github.com/mloesch/sickle) to
[afuetterer/oaipmh-scythe](https://github.com/afuetterer/oaipmh-scythe)

### Breaking Changes

- drop support for Python 2
- drop support for EOL Python 3.7 and below
- rename Sickle class to Scythe to reflect the change of the project name
- switch to PEP8 compliant names for methods (ListRecords() -> list_records())
- remove .next() method from iterator classes

### Features

- set up default custom user agent ([#113](https://github.com/afuetterer/oaipmh-scythe/pull/113)) ([2849e42](https://github.com/afuetterer/oaipmh-scythe/commit/2849e42de1d88ce97e32617ece0565698a05f086))

### Code Refactoring

- rename scythe module to client ([#132](https://github.com/afuetterer/oaipmh-scythe/pull/132)) ([e2c5c32](https://github.com/afuetterer/oaipmh-scythe/commit/e2c5c32444557a9dfceeea5f6a87da44b2c68c79))
- rename exceptions ([#118](https://github.com/afuetterer/oaipmh-scythe/pull/118)) ([7e333b5](https://github.com/afuetterer/oaipmh-scythe/commit/7e333b5f90312bc72a48ed66571b18beadc7d053))
- add type hints ([#116](https://github.com/afuetterer/oaipmh-scythe/pull/116)) ([beaa7ab](https://github.com/afuetterer/oaipmh-scythe/commit/beaa7ab0a91a18fe07775980641a19d46a2eb9cb))
- add type hints ([#110](https://github.com/afuetterer/oaipmh-scythe/pull/110)) ([8e62e55](https://github.com/afuetterer/oaipmh-scythe/commit/8e62e55c35e92ebf52addcf545dad1ccc5be0abc))
- move __version__ to __about__.py ([#106](https://github.com/afuetterer/oaipmh-scythe/pull/106)) ([540d15b](https://github.com/afuetterer/oaipmh-scythe/commit/540d15b7b8fc6a0b32d43116ce209d6c5422d5e1))
- make iterator classes yield their results ([#84](https://github.com/afuetterer/oaipmh-scythe/pull/84)) ([4e5f6e5](https://github.com/afuetterer/oaipmh-scythe/commit/4e5f6e5118e6ba2023922418a77b89aa44beb7f1))
- make baseoaiiterator an abc ([#85](https://github.com/afuetterer/oaipmh-scythe/pull/85)) ([19308d5](https://github.com/afuetterer/oaipmh-scythe/commit/19308d58413cb2eba51adee8018b5278fc0844f6))
- add custom base exception ([ddba030](https://github.com/afuetterer/oaipmh-scythe/commit/ddba030a8d04621f92612f67ca3ca4faefeab1e5))

### Testing

- overhaul test suite ([#112](https://github.com/afuetterer/oaipmh-scythe/pull/112)) ([a2807a4](https://github.com/afuetterer/oaipmh-scythe/commit/a2807a4591b698782850a07340c9001ac7c30141))
- reuse vcr.py cassettes in multiple tests ([#96](https://github.com/afuetterer/oaipmh-scythe/pull/96)) ([f88da9c](https://github.com/afuetterer/oaipmh-scythe/commit/f88da9cf9921fc7e2acaaf4b573bd41171f2f4a4))
- set up integration tests with vcr.py ([#86](https://github.com/afuetterer/oaipmh-scythe/pull/86)) ([4a58205](https://github.com/afuetterer/oaipmh-scythe/commit/4a582050c49f41c921269cd55a684264379d867e))
- ignore deprecation warnings ([9fa640d](https://github.com/afuetterer/oaipmh-scythe/commit/9fa640dbdacbe3c7a9776f91aa6705b4eaa8b7f5))
- switch to pytest tests ([2904283](https://github.com/afuetterer/oaipmh-scythe/commit/29042833388e0cb94825c60050ad6f0ade507003))

### Documentation

- **api:** update api docs ([e46dd83](https://github.com/afuetterer/oaipmh-scythe/commit/e46dd839469f812fe3009ecd8468f852db55f34a))
- **changelog:** update changelog header ([182420d](https://github.com/afuetterer/oaipmh-scythe/commit/182420d2455f32997e68fe9c49b4809b77ff4b74))
- **readme:** fix code example ([b49dfc1](https://github.com/afuetterer/oaipmh-scythe/commit/b49dfc1200fa6e6cad9b6ac2cf077666f8bfc632))
- **readme:** add license badge to readme ([2446ba4](https://github.com/afuetterer/oaipmh-scythe/commit/2446ba4a3bafc43412f828b773d49231fc2e69c2))
- **readme:** update code example in readme ([fe23cd7](https://github.com/afuetterer/oaipmh-scythe/commit/fe23cd7674cd4de5b386bdb5391d3a8d4423f776))
- **readme:** remove black badge ([869d072](https://github.com/afuetterer/oaipmh-scythe/commit/869d072c4beca367d45ef2ced1628fa969100803))
- **tutorial:** update tutorial ([7e17382](https://github.com/afuetterer/oaipmh-scythe/commit/7e173827c0c9e40873500d484c9603d7f03c233b))
- update changelog manually ([#135](https://github.com/afuetterer/oaipmh-scythe/pull/135)) ([9525f7b](https://github.com/afuetterer/oaipmh-scythe/commit/9525f7b322fc21266161e035124d578573095998))
- add meta section in navigation ([#134](https://github.com/afuetterer/oaipmh-scythe/pull/134)) ([a872716](https://github.com/afuetterer/oaipmh-scythe/commit/a8727169c988f176b7aa44b904ab86d21c55ffcd))
- add code of conduct ([#133](https://github.com/afuetterer/oaipmh-scythe/pull/133)) ([c6dc489](https://github.com/afuetterer/oaipmh-scythe/commit/c6dc489b45f70366892a2384cad299dd9ab07161))
- add edit_uri to mkdocs config ([#131](https://github.com/afuetterer/oaipmh-scythe/pull/131)) ([cb4905b](https://github.com/afuetterer/oaipmh-scythe/commit/cb4905be7b73463f692f0709ad07844ece2cbbab))
- add new project slogan ([#130](https://github.com/afuetterer/oaipmh-scythe/pull/130)) ([74211c8](https://github.com/afuetterer/oaipmh-scythe/commit/74211c8b4d9596a441ffa323895bb09e30521024))
- update license headers ([#121](https://github.com/afuetterer/oaipmh-scythe/pull/121)) ([3a56a9d](https://github.com/afuetterer/oaipmh-scythe/commit/3a56a9d877b4063ad0f79c53820f17fb6ba2a73b))
- add google style docstrings ([#120](https://github.com/afuetterer/oaipmh-scythe/pull/120)) ([cc23374](https://github.com/afuetterer/oaipmh-scythe/commit/cc23374ace0735f6331fc1aa57b685aef70d16b8))
- update keywords in pyproject.toml ([#117](https://github.com/afuetterer/oaipmh-scythe/pull/117)) ([927dbd4](https://github.com/afuetterer/oaipmh-scythe/commit/927dbd44d1c53b2c84a307eefb23cf288ddef6b9))
- add security policy ([#109](https://github.com/afuetterer/oaipmh-scythe/pull/109)) ([7898634](https://github.com/afuetterer/oaipmh-scythe/commit/7898634f4adf6e3387f87b19c6a8835a6ffee6c2))
- update [project.urls] ([#108](https://github.com/afuetterer/oaipmh-scythe/pull/108)) ([5282195](https://github.com/afuetterer/oaipmh-scythe/commit/5282195428346f01374cbe732e08b71b184e4182))
- add navigation.footer ([#105](https://github.com/afuetterer/oaipmh-scythe/pull/105)) ([f6b75da](https://github.com/afuetterer/oaipmh-scythe/commit/f6b75da1724e636d5ba1497bfef7967a94bb5219))
- move mkdocs.yml to docs ([fdb2dde](https://github.com/afuetterer/oaipmh-scythe/commit/fdb2dded90905ab3ee2145e3a139a654892307ef))
- add contributor guide ([6138ff1](https://github.com/afuetterer/oaipmh-scythe/commit/6138ff12a657e4dea63efa29b57116671b4d4b29))
- update license file ([fbfa256](https://github.com/afuetterer/oaipmh-scythe/commit/fbfa2565fcea659d069f25779ec9d9927173f304))
- add dark mode switch to mkdocs config ([4b732c4](https://github.com/afuetterer/oaipmh-scythe/commit/4b732c4d4c872c6cf8d8a62a5325a856d83eabc0))
- rename scythe to oaipmh-scythe (__init__.py) ([ea11d35](https://github.com/afuetterer/oaipmh-scythe/commit/ea11d3574576c3d395ab7f1298a3330891b9454a))
- set up documentation with mkdocs ([#21](https://github.com/afuetterer/oaipmh-scythe/pull/21)) ([3945eb7](https://github.com/afuetterer/oaipmh-scythe/commit/3945eb78e1cc7728eaff2bd8e50da8afb4545521))
- add ci badge to readme ([b6541ef](https://github.com/afuetterer/oaipmh-scythe/commit/b6541ef9cba004d70e76e5ddfdebb7ffa7b30102))
- add hatch environment for linting ([a409013](https://github.com/afuetterer/oaipmh-scythe/commit/a4090133aea51f441a48fedf1a4255f5485b1af1))
- update authors file ([86c07c3](https://github.com/afuetterer/oaipmh-scythe/commit/86c07c3fb1b4c61e07b27793997cb9f5433283a8))
- update readme ([5df475e](https://github.com/afuetterer/oaipmh-scythe/commit/5df475e063be5282378dffd723718053e731fd2a))
- update changelog ([69b3c7e](https://github.com/afuetterer/oaipmh-scythe/commit/69b3c7e302170c8e72a91c3d337860980709ec38))

---

Historical entries below are from upstream [mloesch/sickle](https://github.com/mloesch/sickle/blob/master/CHANGES.rst).

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
