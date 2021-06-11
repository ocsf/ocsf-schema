# Schema Extensions

## Extending the Schema
The Splunk Event Schema can be extended by adding new attributes, objects, and event classes.

To extend the schema create a new directory in the `schema/extensions` directory. The directory structure is the same as the top level schema directory and it may contain the following files and subdirectories.

| Name              | Description                                                  |
| ----------------- | ------------------------------------------------------------ |
| `categories.json` | Create it to define a new event category to reserve a range of class IDs. |
| `dictionary.json` | Create it to define new attributes.                          |
| `events`          | Create it to define new event classes.                       |
| `objects`         | Create it to define new objects.                             |