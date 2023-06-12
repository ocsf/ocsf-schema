# Schema Extensions

## Extending the Schema
The OCSF Schema can be extended by adding an extension that defines new attributes, objects, profiles, and event classes.

To extend the schema create a new subdirectory in the `extensions` directory, and add a new `extension.json` file, which defines the extension's `name` and `uid`. For example:

```json
{
  "caption": "New Extension",
  "name": "new_ex",
  "uid": 123,
  "version": "0.0.0"
}
```

The extension's directory structure is the same as the top level schema directory, and it may contain the following files and subdirectories.

| Name              | Description                                                               |
|-------------------|---------------------------------------------------------------------------|
| `categories.json` | Create it to define a new event category to reserve a range of class IDs. |
| `dictionary.json` | Create it to define new attributes.                                       |
| `enums`           | Create it to define new enumerations.                                     |
| `events`          | Create it to define new event classes.                                    |
| `objects`         | Create it to define new objects.                                          |
| `includes`        | Create it to define new shared data.                                      |
| `profiles`        | Create it to define new profiles.                                         |
