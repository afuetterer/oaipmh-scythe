<!--
SPDX-FileCopyrightText: 2015 Mathias Loesch
SPDX-FileCopyrightText: 2023 Heinz-Alexander Fütterer

SPDX-License-Identifier: BSD-3-Clause
-->

# Harvesting other Metadata Formats

By default, `oaipmh-scythe`'s mapping of the record XML into Python dataclasses is tailored to work best with
Dublin-Core-encoded metadata payloads (i.e. `metadata_prefix="oai_dc"`).

```pycon
>>> from oaipmh_scythe import Scythe
>>> scythe = Scythe("https://export.arxiv.org/oai2")
>>> record = scythe.get_record("oai:arXiv.org:2203.05794", metadata_prefix="oai_dc")
>>> record.get_metadata()
Dc(title=[Title(value='BERTopic: Neural topic modeling with a class-based TF-IDF procedure', lang=None)], creator=[Creator(value='Grootendorst, Maarten', lang=None)], subject=[Subject(value='Computer Science - Computation and Language', lang=None)], description=[Description(value='  Topic models can be useful tools to discover latent topics in collections of\ndocuments. Recent studies have shown the feasibility of approach topic modeling\nas a clustering task. We present BERTopic, a topic model that extends this\nprocess by extracting coherent topic representation through the development of\na class-based variation of TF-IDF. More specifically, BERTopic generates\ndocument embedding with pre-trained transformer-based language models, clusters\nthese embeddings, and finally, generates topic representations with the\nclass-based TF-IDF procedure. BERTopic generates coherent topics and remains\ncompetitive across a variety of benchmarks involving classical models and those\nthat follow the more recent clustering approach of topic modeling.\n', lang=None), Description(value='Comment: BERTopic has a python implementation, see\n  https://github.com/MaartenGr/BERTopic', lang=None)], publisher=[], contributor=[], date=[Date(value='2022-03-11', lang=None)], type_value=[TypeType(value='text', lang=None)], format=[], identifier=[Identifier(value='http://arxiv.org/abs/2203.05794', lang=None)], source=[], language=[], relation=[], coverage=[], rights=[])
```

```pycon
>>> record = scythe.get_record("oai:arXiv.org:2203.05794", metadata_prefix="arXiv")
>>> record
# Record(header=Header(identifier='oai:arXiv.org:2203.05794', datestamp=XmlDate(2022, 3, 14), set_spec=['cs'], status=None), metadata=Metadata(other_element=AnyElement(qname='{http://arxiv.org/OAI/arXiv/}arXiv', text='', tail=None, children=[AnyElement(qname='{http://arxiv.org/OAI/arXiv/}id', text='2203.05794', tail=None, children=[], attributes={}), AnyElement(qname='{http://arxiv.org/OAI/arXiv/}created', text='2022-03-11', tail=None, children=[], attributes={}), AnyElement(qname='{http://arxiv.org/OAI/arXiv/}authors', text='', tail=None, children=[AnyElement(qname='{http://arxiv.org/OAI/arXiv/}author', text='', tail=None, children=[AnyElement(qname='{http://arxiv.org/OAI/arXiv/}keyname', text='Grootendorst', tail=None, children=[], attributes={}), AnyElement(qname='{http://arxiv.org/OAI/arXiv/}forenames', text='Maarten', tail=None, children=[], attributes={})], attributes={})], attributes={}), AnyElement(qname='{http://arxiv.org/OAI/arXiv/}title', text='BERTopic: Neural topic modeling with a class-based TF-IDF procedure', tail=None, children=[], attributes={}), AnyElement(qname='{http://arxiv.org/OAI/arXiv/}categories', text='cs.CL', tail=None, children=[], attributes={}), AnyElement(qname='{http://arxiv.org/OAI/arXiv/}comments', text='BERTopic has a python implementation, see\n  https://github.com/MaartenGr/BERTopic', tail=None, children=[], attributes={}), AnyElement(qname='{http://arxiv.org/OAI/arXiv/}license', text='http://arxiv.org/licenses/nonexclusive-distrib/1.0/', tail=None, children=[], attributes={}), AnyElement(qname='{http://arxiv.org/OAI/arXiv/}abstract', text='  Topic models can be useful tools to discover latent topics in collections of\ndocuments. Recent studies have shown the feasibility of approach topic modeling\nas a clustering task. We present BERTopic, a topic model that extends this\nprocess by extracting coherent topic representation through the development of\na class-based variation of TF-IDF. More specifically, BERTopic generates\ndocument embedding with pre-trained transformer-based language models, clusters\nthese embeddings, and finally, generates topic representations with the\nclass-based TF-IDF procedure. BERTopic generates coherent topics and remains\ncompetitive across a variety of benchmarks involving classical models and those\nthat follow the more recent clustering approach of topic modeling.\n', tail=None, children=[], attributes={})], attributes={'{http://www.w3.org/2001/XMLSchema-instance}schemaLocation': 'http://arxiv.org/OAI/arXiv/ http://arxiv.org/OAI/arXiv.xsd'})), about=[])
```

!!! note
    The response still gets parsed into a dataclass, but the metadata has attributes of type `AnyElement`, e.g.
    `AnyElement(qname='{http://arxiv.org/OAI/arXiv/}arXiv'`.

https://xsdata.readthedocs.io/en/latest/codegen/intro/#command-line-tool

```bash
$ python -m pip install "xsdata[cli]>=24.5"
$ xsdata generate --package=arxiv http://arxiv.org/OAI/arXiv.xsd
```

```python
from arxiv import ArXiv

record = scythe.get_record("oai:arXiv.org:2203.05794", metadata_prefix="arXiv")
record
# Record(header=Header(identifier='oai:arXiv.org:2203.05794', datestamp=XmlDate(2022, 3, 14), set_spec=['cs'], status=None), metadata=Metadata(other_element=ArXiv(id=['2203.05794'], created=['2022-03-11'], updated=[], authors=[AuthorsType(author=[AuthorType(keyname='Grootendorst', forenames='Maarten', suffix=None, affiliation=[])])], title=['BERTopic: Neural topic modeling with a class-based TF-IDF procedure'], msc_class=[], acm_class=[], report_no=[], journal_ref=[], comments=['BERTopic has a python implementation, see\n  https://github.com/MaartenGr/BERTopic'], abstract=['  Topic models can be useful tools to discover latent topics in collections of\ndocuments. Recent studies have shown the feasibility of approach topic modeling\nas a clustering task. We present BERTopic, a topic model that extends this\nprocess by extracting coherent topic representation through the development of\na class-based variation of TF-IDF. More specifically, BERTopic generates\ndocument embedding with pre-trained transformer-based language models, clusters\nthese embeddings, and finally, generates topic representations with the\nclass-based TF-IDF procedure. BERTopic generates coherent topics and remains\ncompetitive across a variety of benchmarks involving classical models and those\nthat follow the more recent clustering approach of topic modeling.\n'], categories=['cs.CL'], doi=[], proxy=[], license=['http://arxiv.org/licenses/nonexclusive-distrib/1.0/'])), about=[])
```

!!! note
    The response gets parsed into a Record dataclass, and the metadata is of type `ArXiv`.

!!! note
    Take a look at the models
