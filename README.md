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

For more information about concepts in OCSF, please refer to the OCSF White paper, [Understanding OCSF](https://github.com/ocsf/ocsf-docs/blob/main/Understanding%20OCSF.pdf).

Looking to contribute? Please refer to the contribution guide,
[CONTRIBUTING.md](https://github.com/ocsf/ocsf-schema/blob/main/CONTRIBUTING.md).

## Versioning

Updates to OCSF follow [semantic versioning](https://semver.org/).

## License

This software is licensed under the [Apache License](https://github.com/ocsf/ocsf-schema/blob/main/LICENSE), version 2 ("ALv2").
