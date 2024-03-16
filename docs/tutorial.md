<!--
SPDX-FileCopyrightText: 2015 Mathias Loesch
SPDX-FileCopyrightText: 2023 Heinz-Alexander Fütterer

SPDX-License-Identifier: BSD-3-Clause
-->

# Tutorial

This section gives a brief overview on how to use oaipmh-scythe for querying OAI interfaces.

## Initializing an OAI-PMH Interface

To make a connection to an OAI-PMH interface, you need to import the Scythe class:

```python
from oaipmh_scythe import Scythe
```

We initialize the connection by passing it the base URL. In our example, we use the OAI-PMH interface of
[Zenodo](https://zenodo.org/oai2d).

It is recommended to use the Scythe class as a context manager to close established HTTP connections, when they are no
longer needed.

```python
with Scythe("https://zenodo.org/oai2d") as scythe:
    # ... some OAI-PMH harvesting operation(s)
```

If you want to instantiate the class directly, you can of course do so.

```python
scythe = Scythe("https://zenodo.org/oai2d")
```

In this case make sure to close the connection explicitly, when you are done harvesting.

```python
# ... some OAI-PMH harvesting operation(s)
scythe.close()
```

## Issuing Requests

oaipmh-scythe provides methods for each of the six OAI verbs (ListRecords, GetRecord, Identify, ListSets,
ListMetadataFormats, ListIdentifiers).

Start with a ListRecords request:

```python
records = scythe.list_records()
```

Note that all keyword arguments you provide to this function are passed to the OAI interface as HTTP parameters.
Therefore, the example request would send the parameter `verb=ListRecord`.

## Performing Selective Harvesting

### Harvesting Records Based on Publication Date

To selectively harvest records within a specific publication date range, the
[list_records()][oaipmh_scythe.client.Scythe.list_records] and
[list_identifiers()][oaipmh_scythe.client.Scythe.list_identifiers] methods of the Scythe client can be utilized with
`from_` and `until` parameters. These parameters allow you to specify the lower and upper bounds of the desired date
range, respectively. The accepted date format is YYYY-MM-DD (`str`).

#### Using the from\_ Parameter

The `from_` parameter (note the trailing underscore) is used to set the lower bound of the publication date range.

!!! note
    The trailing underscore is necessary because `from` is a reserved keyword in Python.

Example: Fetching Records Published On or After a Specific Date

```python
records = scythe.list_records(from_="2024-01-16")
next(records)
# <Record oai:zenodo.org:10529175>
```

In this example, `scythe.list_records(from_="2024-01-16")` retrieves records published on or after January 16, 2024.

#### Using the until Parameter

The `until` parameter sets the upper bound for the publication date of the records, enabling you to fetch records
published up to and including the specified date.

Example: Fetching records published until a specific date

```python
records = scythe.list_records(until="2024-01-17")
next(records)
# <Record oai:zenodo.org:2217771>
```

This line will harvest records published up to and including January 17, 2024.

#### Combining from\_ and until

Both `from_` and `until` parameters can be used together to define a specific date range for harvesting records.

Example: Fetching records within a specific date range

```python
records = scythe.list_records(from_="2024-01-16", until="2024-01-17")
next(records)
# <Record oai:zenodo.org:10517528>
```

Here, `scythe.list_records(from_="2024-01-16", until="2024-01-17")` fetches records published between January 16 and
January 17, 2024, inclusive.

### Harvesting Records based on Set Specification

In addition to date-based filtering, the Scythe client offers the capability to selectively harvest records by
specifying a set specification. This feature is particularly useful for fetching records that belong to a specific
category or collection.

#### Using the set\_ Parameter

The `set_` parameter allows you to specify a particular set of records for harvesting.

!!! note
    It is important to note the trailing underscore in `set_`. This is used because `set` is a reserved keyword in Python.

Example: Fetching records from a specific set

```python
records = scythe.list_records(set_="software")
next(records)
# <Record oai:zenodo.org:32712>
```

In this example, `scythe.list_records(set_="software")` retrieves records that are part of the 'software' set. The call
to `next(records)` fetches the first record from the retrieved set.

#### Considerations when using the set\_ Parameter

Set Identifier: The value passed to the `set_` parameter should match the identifier used by the OAI-PMH service for the
desired set. These identifiers are often predefined by the data provider and should be used as documented.

Combining with Other Parameters: The `set_` parameter can be combined with other parameters like `from_` and `until` for
more refined filtering. This allows for fetching records from a specific set within a certain date range.

Example: Combining `set_` with Date Filters

```python
records = scythe.list_records(set_="software", from_="2024-01-01", until="2024-01-31")
next(records)
# <Record oai:zenodo.org:10456652>
```

This code will harvest records from the 'software' set that were published in January 2024.

### Default Metadata Format and Specifying Custom Formats

When harvesting records using the `Scythe` client, it's important to understand how metadata formats are handled. By
default, if no specific metadata format is provided, `Scythe` retrieves records in the `oai_dc` format. This format is
universally supported by all OAI-PMH repositories, ensuring broad compatibility.

#### Default Behavior: Harvesting in oai_dc Format

If you do not specify a metadata format, scythe will automatically use the "oai_dc" metadata format. This is the Dublin
Core format, a standard for simple and generic metadata representation.

Example: Fetching records with default metadata format

```python
records = scythe.list_records()
```

This code will harvest records using the default `oai_dc` metadata format. It is equivalent to using
`scythe.list_records(metadata_prefix="oai_dc")` explicitly.

#### Specifying a different Metadata Format

If you need to harvest records in a format other than "oai_dc", you can specify this with the `metadata_prefix`
parameter. Note that the format you request must be supported by the OAI-PMH repository you are querying.

#### Listing Available Metadata Formats

Before specifying a different format, you can check the available formats using the list_metadata_formats method:

```python
metadata_formats = scythe.list_metadata_formats()
for metadata_format in metadata_formats:
    print(metadata_format)
```

Example: Fetching records in a custom metadata format

```python
records = scythe.list_records(metadata_prefix="datacite")
```

In this example, `scythe.list_records(metadata_prefix="datacite")` retrieves records in the "datacite" metadata format.

!!! note
    It's important to remember that in the absence of a specified `metadata_prefix`, scythe will default to using the
    "oai_dc" format. This ensures that you can always retrieve records even if the specific format requirements are not
    known.

## Consecutive Harvesting

Since most OAI verbs yield more than one element, their respective Scythe methods return iterator objects which can be
used to iterate over the records of a repository:

```python
records = scythe.list_records()
next(records)
# <Record oai:zenodo.org:4574771>
```

Note that this works with all verbs that return more than one element. These are:
[list_records()][oaipmh_scythe.client.Scythe.list_records],
[list_identifiers()][oaipmh_scythe.client.Scythe.list_identifiers],
[list_sets()][oaipmh_scythe.client.Scythe.list_sets], and
[list_metadata_formats()][oaipmh_scythe.client.Scythe.list_metadata_formats].

The following example shows how to iterate over the headers returned by `list_identifiers()`:

```python
headers = scythe.list_identifiers()
next(headers)
# <Header oai:zenodo.org:4574771>
```

Iterating over the sets returned by `list_sets()` works similarly:

```python
sets = scythe.list_sets()
next(sets)
# <Set European Middleware Initiative>
```

To explore all the metadata formats supported by the repository, you can iterate through the formats returned by the
`list_metadata_formats()` method:

```python
metadata_formats = scythe.list_metadata_formats()
next(metadata_formats)
# <MetadataFormat marcxml>
```

## Getting a Single Record

OAI-PMH allows you to get a single record by using the `GetRecord` verb:

```python
scythe.get_record(identifier="oai:zenodo.org:4574771")
# <Record oai:zenodo.org:4574771>
```

## Harvesting OAI Items vs. OAI Responses

Scythe supports two harvesting modes that differ in the type of the returned objects. The default mode returns
OAI-specific *items* (records, headers etc.) encoded as Python objects as seen earlier. If you want to save the whole
XML response returned by the server, you have to pass the
[OAIResponseIterator][oaipmh_scythe.iterator.OAIResponseIterator] during the instantiation of the
[Scythe][oaipmh_scythe.client.Scythe] object:

```python
from oaipmh_scythe.iterator import OAIResponseIterator

scythe = Scythe("https://zenodo.org/oai2d", iterator=OAIResponseIterator)
responses = scythe.list_records()
next(responses)
# <OAIResponse ListRecords>
```

You could then save the returned responses to disk:

```python
with open("response.xml", "w") as f:
    f.write(next(responses).raw.encode("utf-8"))
```

## Ignoring Deleted Records

The [list_records()][oaipmh_scythe.client.Scythe.list_records] and
[list_identifiers()][oaipmh_scythe.client.Scythe.list_identifiers] methods accept an optional parameter
`ignore_deleted`. If set to `True`, the returned [OAIItemIterator][oaipmh_scythe.iterator.OAIItemIterator] will skip
deleted records/headers:

```python
records = scythe.list_records(ignore_deleted=True)
```

!!! note
    This works only using the [oaipmh_scythe.iterator.OAIItemIterator][]. If you use the
    [oaipmh_scythe.iterator.OAIResponseIterator][], the resulting OAI responses will still contain the deleted records.

## Authentication

Certain OAI-PMH repositories may require authentication for accessing data or certain functionality. `oaipmh-scythe`
provides support for HTTP Basic authentication and other methods, which can be used to authenticate requests made by the
client.

The `auth` parameter of the Scythe client allows you to specify an authentication method when creating a new instance of
the client.

### HTTP Basic Authentication

To use HTTP basic authentication with the Scythe client, simply provide a tuple containing your username and password as
the value for the `auth` parameter when instantiating the Scythe object:

```python
auth = ("username", "password")
scythe = Scythe("https://example.org/oai2d", auth=auth)
```

!!! note
    `oaipmh-scythe` uses [httpx](https://www.python-httpx.org) under the hood. The `auth` parameter accepts subclasses of
    `httpx.Auth`, e.g. `httpx.BasicAuth`, `httpx.DigestAuth`, or `httpx.NetRCAuth`, see
    [Authentication - HTTPX](https://www.python-httpx.org/advanced/authentication/) for further information

Once the authentication method is set, Scythe will use it to authenticate requests made by the client. This allows you
to access restricted data or functionality from an OAI-PMH repository without having to handle authentication manually.
