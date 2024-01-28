<!-- SPDX-FileCopyrightText: 2015 Mathias Loesch -->
<!-- SPDX-FileCopyrightText: 2023 Heinz-Alexander Fütterer -->

<!-- SPDX-License-Identifier: BSD-3-Clause -->

# Harvesting other Metadata Formats than OAI-DC

By default, oaipmh-scythe's mapping of the record XML into Python dictionaries
is tailored to work only with Dublin-Core-encoded metadata payloads.
Other formats most probably won't be mapped correctly, especially if
they are more hierarchically structured than Dublin Core.

In case you want to harvest these more complex formats, you have to
write your own record model class by subclassing the default
implementation that unpacks the metadata XML:

```python
from oaipmh_scythe.models import Record

class MyRecord(Record):
    # Your XML unpacking implementation goes here.
    pass
```

!!! note
    Take a look at the implementation of [oaipmh_scythe.models.Record][] to get an idea of
    how to do this.

Next, associate your implementation with OAI verbs in the [oaipmh_scythe.client.Scythe][] object.
In this case, we want the [oaipmh_scythe.client.Scythe][] object to use our implementation to represent items returned by
ListRecords and GetRecord responses:

```python
scythe = Scythe('http://...')
scythe.class_mapping['ListRecords'] = MyRecord
scythe.class_mapping['GetRecord'] = MyRecord
```

If you need to rewrite *all* item implementations, you can also provide
a complete mapping to the [oaipmh_scythe.client.Scythe][] object at instantiation:

```python
my_mapping = {
    'ListRecords': MyRecord,
    'GetRecord': MyRecord,
    # ...
}

scythe = Scythe('https://...', class_mapping=my_mapping)
```
