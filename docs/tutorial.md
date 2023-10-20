# Tutorial

This section gives a brief overview on how to use oaipmh-scythe for querying OAI interfaces.

## Initialize an OAI Interface

To make a connection to an OAI interface, you need to import the Scythe class:

```pycon
>>> from oaipmh_scythe import Scythe
```

Next, you can initialize the connection by passing it the base URL. In
our example, we use the OAI interface of Zenodo:

```pycon
>>> scythe = Scythe("https://zenodo.org/oai2d")
```

## Issuing Requests

oaipmh-scythe provides methods for each of the six OAI verbs (ListRecords,
GetRecord, Idenitfy, ListSets, ListMetadataFormats, ListIdentifiers).
Start with a ListRecords request:

```pycon
>>> records = scythe.ListRecords(metadataPrefix='oai_dc')
```

Note that all keyword arguments you provide to this function are passed
to the OAI interface as HTTP parameters. Therefore the example request
would send the parameters `verb=ListRecords&metadataPrefix=oai_dc`. We
can add additional parameters, like, for example, an OAI `set`:

```pycon
>>> records = scythe.ListRecords(metadataPrefix="oai_dc", set="driver")
```

## Consecutive Harvesting

Since most OAI verbs yield more than one element, their respective
Scythe methods return iterator objects which can be used to iterate over
the records of a repository:

```pycon
>>> records = scythe.ListRecords(metadataPrefix="oai_dc")
>>> records.next()
<Record oai:oai:zenodo.org:4574771>
```

Note that this works with all verbs that return more than one element.
These are: [ListRecords()][oaipmh_scythe.app.Scythe.ListRecords],
[ListIdentifiers()][oaipmh_scythe.app.Scythe.ListIdentifiers], [ListSets()][oaipmh_scythe.app.Scythe.ListSets],
and [ListMetadataFormats()][oaipmh_scythe.app.Scythe.ListMetadataFormats].

The following example shows how to iterate over the headers returned by
`ListIdentifiers`:

```pycon
>>> headers = scythe.ListIdentifiers(metadataPrefix="oai_dc")
>>> headers.next()
<Header oai:eprints.rclis.org:4088>
```

Iterating over the sets returned by `ListSets` works similarly:

```pycon
>>> sets = scythe.ListSets()
>>> sets.next()
<Set Status = In Press>
```

## Using the `from` Parameter

If you need to perform selective harvesting by date using the `from`
parameter, you may face the problem that `from` is a reserved word in
Python:

```pycon
>>> records = scythe.ListRecords(metadataPrefix="oai_dc", from="2012-12-12")
  File "<stdin>", line 1
    records = scythe.ListRecords(metadataPrefix="oai_dc", from="2012-12-12")
                                                              ^
SyntaxError: invalid syntax
```

Fortunately, you can circumvent this problem by using a dictionary together with the `**` operator:

```pycon
>>> records = scythe.ListRecords(
...             **{'metadataPrefix': 'oai_dc',
...             'from': '2012-12-12'
...            })
```

## Getting a Single Record

OAI-PMH allows you to get a single record by using the `GetRecord` verb:

```pycon
>>> scythe.GetRecord(identifier='oai:eprints.rclis.org:4088',
...                  metadataPrefix='oai_dc')
<Record oai:eprints.rclis.org:4088>
```

## Harvesting OAI Items vs. OAI Responses

Scythe supports two harvesting modes that differ in the type of the
returned objects. The default mode returns OAI-specific *items*
(records, headers etc.) encoded as Python objects as seen earlier. If
you want to save the whole XML response returned by the server, you have
to pass the [oaipmh_scythe.iterator.OAIResponseIterator][] during the instantiation of the
[Scythe][oaipmh_scythe.app.Scythe] object:

```pycon
>>> scythe = Scythe('http://elis.da.ulcc.ac.uk/cgi/oai2', iterator=OAIResponseIterator)
>>> responses = Scythe.ListRecords(metadataPrefix='oai_dc')
>>> responses.next()
<OAIResponse ListRecords>
```

You could then save the returned responses to disk:

```pycon
>>> with open("response.xml", "w") as f:
...     f.write(responses.next().raw.encode("utf8"))
```

## Ignoring Deleted Records

The [ListRecords()][oaipmh_scythe.app.Scythe.ListRecords] and
[ListIdentifiers()][oaipmh_scythe.app.Scythe.ListIdentifiers] methods accept an optional parameter `ignore_deleted`.
If set to `True`, the returned [OAIItemIterator][oaipmh_scythe.iterator.OAIItemIterator] will skip deleted records/headers:

```pycon
>>> records = scythe.ListRecords(metadataPrefix="oai_dc", ignore_deleted=True)
```

!!! note

    This works only using the [oaipmh_scythe.iterator.OAIItemIterator][]. If you use the
    [oaipmh_scythe.iterator.OAIResponseIterator][], the resulting OAI responses will still contain the deleted records.
