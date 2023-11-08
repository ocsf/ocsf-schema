## OCSF Extensions

The OCSF Schema can be extended by adding an extension that defines additional attributes, objects, profiles, event classes and/or categories. Extensions allow one to create vendor/customer specific schemas or augment an existing schema to better suit their custom requirements. Extensions can also be used to factor out non-essential schema domains keeping the core schema succinct. Extensions use the framework in the same way as a new schema, optionally creating categories, profiles or event classes from the dictionary. 

As with categories and event classes, extensions have unique IDs within the framework as well as their own versioning. The following sections provide guidelines to create extensions within OCSF.

### Reserve a UID and Name for your extension:

In order to reserve an ID space, and make your extension public, add a unique identifier & a unique name for your extension in the OCSF Extensions Registry [here](https://github.com/ocsf/ocsf-schema/blob/main/extensions.md). This is done to avoid collisions with core or other extension schemas.  For example, a new sample extension would have a row in the table as follows:

| **Caption** | **Name** | **UID** | **Notes**                         |
| ------------------ | -------- | ------- | --------------------------------- |
| New Extension      | new_ex   | 123     | The development schema extensions |

### Create your Extension's sub-directory:

To extend the schema, create a new subdirectory in the `extensions` directory, and add a new `extension.json` file, which defines the extension's `name` and `uid`. For example:

```
{
  "caption": "New Extension",
  "name": "new_ex",
  "uid": 123,
  "version": "0.0.0"
}
```

The extension's directory structure is the same as the top level schema directory, and it may contain the following files and subdirectories, depending on what type of extension is desired:

| Name              | Description                                                               |
|-------------------|---------------------------------------------------------------------------|
| `categories.json` | Create it to define new categories. Note, to avoid collisions with the categories defined in the core schema, the category IDs must be greater than or equal to 30. |
| `dictionary.json` | Create it to define new attributes.                                       |
| `events`          | Create it to define new event classes.                                    |
| `includes`        | Create it to define new shared data.                                      |
| `objects`         | Create it to define new objects.                                          |
| `profiles`        | Create it to define new profiles.                                         |


As a reference, take a look at the [Linux Extension](https://github.com/ocsf/ocsf-schema/tree/main/extensions/linux) that is currently added to OCSF.
