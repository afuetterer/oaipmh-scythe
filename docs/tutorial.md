# Tutorial

This section gives a brief overview on how to use oaipmh-scythe for querying OAI interfaces.

## Initialize an OAI Interface

To make a connection to an OAI interface, you need to import the Scythe class:

```python
from oaipmh_scythe import Scythe
```

Next, you can initialize the connection by passing it the base URL. In
our example, we use the OAI interface of [Zenodo](https://zenodo.org/oai2d):

```python
scythe = Scythe("https://zenodo.org/oai2d")
```

## Issuing Requests

oaipmh-scythe provides methods for each of the six OAI verbs (ListRecords,
GetRecord, Identify, ListSets, ListMetadataFormats, ListIdentifiers).

Start with a ListRecords request:

```python
records = scythe.list_records(metadataPrefix="oai_dc")
```

Note that all keyword arguments you provide to this function are passed
to the OAI interface as HTTP parameters. Therefore, the example request
would send the parameters `verb=ListRecords&metadataPrefix=oai_dc`. We
can add additional parameters, like, for example, an OAI `set`:

```python
records = scythe.list_records(metadataPrefix="oai_dc", set="user-cfa")
```

## Consecutive Harvesting

Since most OAI verbs yield more than one element, their respective
Scythe methods return iterator objects which can be used to iterate over
the records of a repository:

```python
records = scythe.list_records(metadataPrefix="oai_dc")
next(records)
# <Record oai:zenodo.org:4574771>
```

Note that this works with all verbs that return more than one element.
These are: [list_records()][oaipmh_scythe.client.Scythe.list_records],
[list_identifiers()][oaipmh_scythe.client.Scythe.list_identifiers], [list_sets()][oaipmh_scythe.client.Scythe.list_sets],
and [list_metadata_formats()][oaipmh_scythe.client.Scythe.list_metadata_formats].

The following example shows how to iterate over the headers returned by
`list_identifiers()`:

```python
headers = scythe.list_identifiers(metadataPrefix="oai_dc")
next(headers)
# <Header oai:zenodo.org:4574771>
```

Iterating over the sets returned by `list_sets()` works similarly:

```python
sets = scythe.list_sets()
next(sets)
# <Set European Middleware Initiative>
```

## Using the `from` Parameter

If you need to perform selective harvesting by date using the `from`
parameter, you may face the problem that `from` is a reserved word in
Python:

```python
records = scythe.list_records(metadataPrefix="oai_dc", from="2023-10-10")
#  File "<stdin>", line 1
#    records = scythe.list_records(metadataPrefix="oai_dc", from="2023-10-10")
#                                                           ^^^^
# SyntaxError: invalid syntax
```

Fortunately, you can circumvent this problem by using a dictionary together with the `**` operator:

```python
records = scythe.list_records(**{"metadataPrefix": "oai_dc", "from": "2023-10-10"})
```

## Getting a Single Record

OAI-PMH allows you to get a single record by using the `GetRecord` verb:

```python
scythe.get_record(identifier="oai:zenodo.org:4574771", metadataPrefix="oai_dc")
# <Record oai:eprints.rclis.org:4088>
```

## Harvesting OAI Items vs. OAI Responses

Scythe supports two harvesting modes that differ in the type of the
returned objects. The default mode returns OAI-specific *items*
(records, headers etc.) encoded as Python objects as seen earlier. If
you want to save the whole XML response returned by the server, you have
to pass the [OAIResponseIterator][oaipmh_scythe.iterator.OAIResponseIterator] during the instantiation of the
[Scythe][oaipmh_scythe.client.Scythe] object:

```python
from oaipmh_scythe.iterator import OAIResponseIterator
scythe = Scythe("https://zenodo.org/oai2d", iterator=OAIResponseIterator)
responses = scythe.list_records(metadataPrefix="oai_dc")
next(responses)
# <OAIResponse ListRecords>
```

You could then save the returned responses to disk:

```python
with open("response.xml", "w") as f:
    f.write(next(responses).raw.encode("utf8"))
```

## Ignoring Deleted Records

The [list_records()][oaipmh_scythe.client.Scythe.list_records] and
[list_identifiers()][oaipmh_scythe.client.Scythe.list_identifiers] methods accept an optional parameter `ignore_deleted`.
If set to `True`, the returned [OAIItemIterator][oaipmh_scythe.iterator.OAIItemIterator] will skip deleted records/headers:

```python
records = scythe.list_records(metadataPrefix="oai_dc", ignore_deleted=True)
```

!!! note

    This works only using the [oaipmh_scythe.iterator.OAIItemIterator][]. If you use the
    [oaipmh_scythe.iterator.OAIResponseIterator][], the resulting OAI responses will still contain the deleted records.
