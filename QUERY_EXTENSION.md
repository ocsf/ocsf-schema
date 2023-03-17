
Query extension is added in `query` directory instead of extensions folder so that changes are additive only
and can be applied to other extensions with minimal change

## Extending the Schema

Query extension can be use to extend events, objects, attributes of any of the namespace schema.
extends can be a list wherein first element denotes namepsace while second element the parent object,event or include.
Query Extensions have additional categories, event classes, attributes, objects or profiles. 
Existing categories, events, attributes, objects or profile can also be modified although we should minimize it for better forward compatibility.


| Name              | Description                                                               |
|-------------------|---------------------------------------------------------------------------|
| `categories.json` | Create it to define new categories. Note, to avoid collisions with the categories defined in the core schema, the category IDs must be greater than or equal to 30. |
| `dictionary.json` | Create it to define new attributes.                                       |
| `enums`           | Create it to define new enumerations.                                     |
| `events`          | Create it to define new event classes.                                    |
| `includes`        | Create it to define new shared data.                                      |
| `objects`         | Create it to define new objects.                                          |


## Versioning

Updates to OCSF follow [semantic versioning](https://semver.org/).

## License

This software is licensed under the Apache License, version 2 ("ALv2").
