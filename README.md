# <img src="ocsf.png" alt="OCSF Logo" width="32"/> Open Cybersecurity Schema Framework

This repository defines the Open Cybersecurity Schema Framework (OCSF) schema.
OCSF is a framework for creating schemas and it also delivers a cybersecurity
event schema built with the framework.

The framework is made up of a set of categories, event classes, data types,
and an attribute dictionary. The framework is not restricted to cybersecurity
nor to events, however the initial focus of the framework has been a schema
for cybersecurity events. A schema browser for the cybersecurity schema can
be found at [schema.ocsf.io](https://schema.ocsf.io). This is the recommended
way to explore the schema.

OCSF is agnostic to storage format, data collection and ETL processes. The core
schema for cybersecurity events is intended to be agnostic to implementations.
The schema framework definition files and the resulting schema are written as JSON.

OCSF is intended to be used by both products and devices which produce log events,
analytic systems, and logging systems which retain log events.

## Extending the Schema

Extensions are additional categories, event classes, attributes, objects or profiles. The Open
Cybersecurity Schema Framework can be extended by adding new attributes, objects, categories
and event classes. A schema is the aggregation of core schema entities and extensions.
Extensions allow a particular vendor or customer to create a new schema or augment an existing
schema. Extensions can also be used to factor out non-essential schema domains keeping a
schema small. Extensions use the framework in the same way as a new schema, optionally
creating categories, profiles or event classes from the dictionary. Extensions can add new
attributes to the dictionary, including new objects. As with categories, event classes and profiles,
extensions have unique IDs within the framework as well as versioning.

To extend the schema create a new directory in the `schema/extensions` directory. The directory
structure is the same as the top level schema directory, and it may contain the following files
and subdirectories.


| Name              | Description                                                               |
|-------------------|---------------------------------------------------------------------------|
| `categories.json` | Create it to define a new event category to reserve a range of class IDs. |
| `dictionary.json` | Create it to define new attributes.                                       |
| `enums`           | Create it to define new enumerations.                                     |
| `events`          | Create it to define new event classes.                                    |
| `includes`        | Create it to define new shared data.                                      |
| `objects`         | Create it to define new objects.                                          |

For more information on extending the schema, please refer to the contribution guide,
[CONTRIBUTING.md](https://github.com/ocsf/ocsf-schema/blob/main/CONTRIBUTING.md)

## Versioning

Updates to OCSF follow [semantic versioning](https://semver.org/).

## License

This software is licensed under the Apache License, version 2 ("ALv2").
