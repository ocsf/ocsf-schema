# Schema Extensions

## Extending the Schema
The Event Schema can be extended by adding new attributes, objects, and event classes.

To extend the schema create a new directory in the `schema/extensions` directory and add `extension.json` file. 
For example:
```json
{
  "caption": "New Extension",
  "meta": "profile",
  "name": "new_ex",
  "version": "0.0.0",
  "uid": 123
}
```

The directory structure is the same as the top level schema directory and it may contain the following files and subdirectories.

| Name              | Description                                                               |
|-------------------|---------------------------------------------------------------------------|
| `categories.json` | Create it to define a new event category to reserve a range of class IDs. |
| `dictionary.json` | Create it to define new attributes.                                       |
| `enums`           | Create it to define new enumerations.                                     |
| `events`          | Create it to define new event classes.                                    |
| `includes`        | Create it to define new shared data.                                      |
| `objects`         | Create it to define new objects.                                          |