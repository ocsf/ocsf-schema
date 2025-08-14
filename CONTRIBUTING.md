# OCSF Contribution Guide

This documentation presents guidelines and expected etiquettes to successfully contribute to the development of OCSF Schemas and the framework itself.

* * *

### Pull Request Guidelines

All contributors must submit their changes via pull requests. If you're not familiar with pull requests, please read [the GitHub documentation](https://help.github.com/en/articles/about-pull-requests). Following are a few guidelines and expectations for submitting a PR.

1. Fork the repo that you want to contribute to ([ocsf-schema](https://github.com/ocsf/ocsf-schema), [ocsf-docs](https://github.com/ocsf/ocsf-docs), [ocsf-server](https://github.com/ocsf/ocsf-server)).
2. Make desired changes in the forked repo, test if [everything works as expected](#verifying-the-changes) and is error-free, a local instance of the [ocsf-server](https://github.com/ocsf/ocsf-server) would be essential.
3. Push the changes to the forked repo.
4. Create a **Pull Request** to merge changes into the main repo, request at least 3 approvers.
5. Follow the guidelines in the PR template.
    1. Limit the number of commits in a single PR to aid reviewers, be as specific with the change as possible. A single PR **must** contain related changes.
    2. Each commit must include a DCO [Developer's Certificate of Origin](#developers-certificate-of-origin-11).
    3. Add an entry to the `Unreleased` section in [CHANGELOG.md](https://github.com/ocsf/ocsf-schema/blob/main/CHANGELOG.md).
    3. Describe your change in as much detail as possible.
    5. Confirm that you have tested the changes, and the server run was error free.
    6. Check the Preview tab to ensure everything looks as expected.
    7. Once the PR is ready, add relevant labels, request approvers and submit it.
    8. Resolve any github action failures, warnings reported for your pull request, and stay involved in the conversation.
6. Thank you for your contribution!

* * *

### Key OCSF Terminology

1. **Field**: A field is a unique identifier name for a piece of data contained in OCSF. Each field also designates a corresponding data_type.
2. **Object**: An object is a collection of contextually related fields and other objects.  It is also a data_type in OCSF.
3. **Attribute**: An attribute is the more generic name for both fields and objects in OCSF.  A field is a scalar attribute while an object is a complex attribute.
4. **Event Class**: An event is represented by an Event Class, which are a particular set of attributes (including fields & objects) representing a log line or telemetry submission at a point in time.
5. **Category:** A Category organizes event classes that represent a particular domain.

More details about OCSF concepts, terminology and use-cases can be found in [Understanding OCSF.](https://github.com/ocsf/ocsf-docs/blob/main/overview/understanding-ocsf.md)

## How do I add an `event_class`? 

### In brief -

1. Determine all the `attributes` (including fields and objects) you would want to add in the `event_class`.
2. Check the [dictionary](https://github.com/ocsf/ocsf-schema/blob/main/dictionary.json) and the [/objects](https://github.com/ocsf/ocsf-schema/tree/main/objects) folder, many of your desired attributes may already be present.
3. Define the missing attributes → [Adding/Modifying an `attribute`](#addingmodifying-an-attribute)
4. Determine which category you would want to add your event_class in, note it’s  `name`
5. Create a new file →  `<event_class_name.json>` inside the category specific subfolder in the [/events](https://github.com/ocsf/ocsf-schema/tree/main/events) folder. Template available [here](https://github.com/ocsf/ocsf-schema/blob/main/templates/event_class_name.json)
6. Define the `event_class` itself → [Adding/Modifying an `event_class`](#addingmodifying-an-event_class)
7. Finally, verify the changes are working as expected in your local [ocsf-server](https://github.com/ocsf/ocsf-server).

* * *

### Adding/Modifying an `attribute`

1. All the available `attributes` - `fields` & `objects` in OCSF are and will need to be defined in the attribute dictionary, the [dictionary.json](https://github.com/ocsf/ocsf-schema/blob/main/dictionary.json) file and [/objects](https://github.com/ocsf/ocsf-schema/tree/main/objects) folder if defining an object.
2. Determine if a new attribute is required for your change, it might already be defined in the attribute dictionary and/or the [/objects](https://github.com/ocsf/ocsf-schema/tree/main/objects) folder.
3. Before adding a new attribute, review the following OCSF attribute conventions -

   * Attribute names must be a valid UTF-8 sequence.
   * Attribute names must be all lower case.
   * Combine words using underscore.
   * No special characters except underscore.
   * Use present tense unless the attribute describes historical information.
   * Use singular and plural names properly to reflect the field content. Example: use `events_per_sec` rather than `event_per_sec`.
   * When attribute represents multiple entities, the attribute name should be pluralized and the value type should be an array. Example: `process.loaded_modules` includes multiple values -- a loaded module names list.
   * Avoid repetition of words. Example: `src_endpoint.src_ip` should be `src_endpoint.ip`.
   * Avoid abbreviations when possible. Some exceptions can be made for well-accepted abbreviation. Example: `ip`, `os`, `cve` etc.

#### How to define a `field` in the dictionary?

To add a new field in OCSF, you need to define it in the [dictionary.json](https://github.com/ocsf/ocsf-schema/blob/main/dictionary.json) file as described below. 

Sample entry in the dictionary - 

```
    "uid": 
    {
      "caption": "Unique ID", // "previously name"
      "description": "The unique identifier. See specific usage.",
      "type": "string_t"
    }
```

Choose a **unique** field you want to add, `uid` in the example above and populate it as described below.

1. `caption` → Add a user friendly name to the field. 
2. `description` → Add concise description to define the attributes.
    1. Note that `field` descriptions can be overridden in the `event_class/object`, therefore if it’s a common field (like name, label, uid etc) feel free to add a generic description, specific descriptions can be added in the `event_class/object` definition. For example,
    2. A generic definition of `uid` in the dictionary -
        1.  `uid` : `The unique identifier. See specific usage.`
    3. Specific description of `uid` in the `vulnerability` object -
        1. `uid` : `Unique Identifier/s of the reported vulnerability. e.g. CVE ID/s"`
3. `type` → Review OCSF data_types and ensure you utilize appropriate types while defining new fields.
    1. All the available data_types can be accessed [here](https://schema.ocsf.io/data_types).
    2. They are also accessible in your local instance of the ocsf-server - http://localhost:8000/data_types
4. `is_array` → This a boolean key:value pair that you would need to add if the field you are defining is an array.
    1. e.g. `"is_array": true`

#### How to define an `object`?

1. All the available `objects` need to be defined as individual field entries in the dictionary, the [dictionary.json](https://github.com/ocsf/ocsf-schema/blob/main/dictionary.json) file and as distinct .json files in the [/objects](https://github.com/ocsf/ocsf-schema/tree/main/objects) folder. 
2. Review existing Objects, determine if a modification of the existing object would be sufficient or if there’s a need for a completely new object.
3. Use the template available [here](https://github.com/ocsf/ocsf-schema/blob/main/templates/object_name.json), to get started with .json file definition.

An example `vulnerability.json` object file,

```
{
  "caption": "Vulnerability Details",
  "name": "vulnerability",
  "description": "The vulnerability object describes details related to the observed vulnerability.",
  "extends": "object",
  "attributes": {
    "desc": {
      "description": "The description of the vulnerability",
      "requirement": "recommended"
    },
    "kb_article_list": {
      "requirement": "optional"
    }
  }
}
```
4. `caption` → Add a user friendly name to the object.
5. `description` → Add a concise description to define the object.
6. `extends` → Ensure the value is `object` or an existing object, e.g. `entity` (All objects in OCSF must extend a base definition of `object` or another existing object.)
7. `name` → Add a **unique** name of the object. `name` must match the filename of the actual `.json` file.
8.  `attributes` → Add the attributes that you want to define in the object, 
    1. `requirement` →  For each attribute ensure you add a requirement value. Valid values are `optional`, `required`, `recommended` 
    2. `$include` → You can include attributes from other places; to do so, specify a virtual attribute called `$include` and give its value as the list of files (relative to the root of the schema repository) that should contribute their attributes to this object.  _e.g._
        ```
        "attributes": {
          "$include": [
            "profiles/host.json"
          ],
          ...
        }
        ```

**Note:** If you want to create an object which would act only as a base for other objects, you must prefix the object `name` and the actual `json` filename with an `_`. The resultant object will not be visible in the [OCSF Server.](https://schema.ocsf.io/1.0.0-rc.2/objects) For example, take a look at the [entity](https://github.com/ocsf/ocsf-schema/blob/main/objects/_entity.json) object. 

Sample entry in the `dictionary.json`,

```
    "vulnerability": 
    {
      "caption": "Vulnerability",
      "description": "The vulnerability object describes details related to the observed vulnerability.",
      "type": "vulnerability"
    }
```

Choose a **unique** object you want to add, `vulnerability` in the example above and populate it as described below.

1. `caption` → Add a user friendly name to the object
2. `description` → Add a concise description to define the object.
3. `type` → Add the type of the object you are defining. 
4. `is_array` → This a boolean key:value pair that you would need to add if the object you are defining is an array.
    1. e.g. `"is_array": true`

* * *

### Adding/Modifying an `event_class`

1. All the available Event Classes are defined as .json files in the [/events](https://github.com/ocsf/ocsf-schema/tree/main/events) folder.
2. Review existing Event Classes, determine if a modification of the existing class would be sufficient or if there’s a need for a completely new event_class.
3. To define a new class, 
    1. Create a new file →  `<event_class_name.json>` inside the category specific subfolder in the [/events](https://github.com/ocsf/ocsf-schema/tree/main/events) folder.
    2. Use the template available [here](https://github.com/ocsf/ocsf-schema/blob/main/templates/event_class_name.json), to get started with the .json definition.
    3. `uid` → Select an integer in the range 0 - 99. Ensure the integer is **unique** within the category.
        * Note: Without `uid`, an event_class won’t be visible in the ocsf-server.
    4. `caption` → Add a user friendly name to the event_class.
    5. `description` → Add a concise description to define the attributes.
    6. `name` → Add a **unique** name of the event_class. Ensure it matches the file name to maintain consistency.
    7. `extends` → Ensure the value is `base_event`.
    8. `attributes` → Add the attributes that you want to define in the event_class, 
        1. `group` → For each attribute ensure you add a group value. Valid values are - `classification`, `context`, `occurrence`, `primary`
        2. `requirement` →  For each attribute ensure you add a requirement value. Valid values are `optional`, `required`, `recommended`
        3. `$include` → As for objects, you can also include attributes from other places; to do so, specify the list of files (relative to the root of the schema repository) that should contribute their attributes to this object.  _e.g._
        ```
        "attributes": {
          "$include": [
            "profiles/cloud.json"
          ],
          ...
        }
        ```

    9. `constraints` → For each class you can add constraints on the attribute requirements. Valid constraint types are `at_least_one`, `just_one`. e.g.
        ```
         "constraints": {
            "at_least_one": [
                "uid",
                "name"
             ]
        }
        ```
    
        _(A Constraint is a documented rule subject to validation that requires at least one of the specified recommended attributes of a class to be populated.)_ 

* * *

### Deprecating an attribute

To deprecate an attribute (`field`, `object`) follow the steps below -

1. Create a github issue, explaining why an attribute needs to be deprecated and what the alternate solution is.
2. Utilize the following flag to allow deprecation of attributes. This flag needs to be added a json property of the attribute that is the subject of deprecation.
    ```
          "@deprecated": {
            "message": "Use the <code> ALTERNATE_ATTRIBUTE </code> attribute instead.",
            "since": "semver" 
          }
    ```
3. Example of a deprecated field
    ```
    "packages": {
      "@deprecated": {
        "message": "Use the <code> affected_packages </code> attribute instead.",
        "since": "1.0.0"
      },
      "caption": "Software Packages",
      "description": "List of vulnerable packages as identified by the security product",
      "is_array": true,
      "type": "package"
    }
4. Example of a deprecated object
   ```
    {
      "caption": "Finding",
      "description": "The Finding object describes metadata related to a security finding generated by a security tool or system.",
      "extends": "object",
      "name": "finding",
      "@deprecated": {
        "message": "Use the new <code>finding_info</code> object.",
        "since": "1.0.0"
      },
      "attributes": {...}
    }
***
 
### Verifying the changes

Contributors should verify the changes before they submit the PR, the best method to test and verify their changes is to run a local instance of the [ocsf-server](https://github.com/ocsf/ocsf-server). Follow the instructions [here](https://github.com/ocsf/ocsf-server/blob/main/README.md) to set your own local ocsf-server.

If there are any problems with the newly made changes, the server will throw corresponding errors.
Sample error messages - 

```
[error] dictionary: missing attribute: event_uid for Network HTTP Activity
[error] dictionary: missing attribute: event_name for Container Orchestration
```
 Address the errors before submitting the changes, your server run should be completely error free.

***

### Developer's Certificate of Origin 1.1

By making a contribution to this project, I certify that:

(a) The contribution was created in whole or in part by me and I
    have the right to submit it under the open source license
    indicated in the file; or

(b) The contribution is based upon previous work that, to the
    best of my knowledge, is covered under an appropriate open
    source license and I have the right under that license to
    submit that work with modifications, whether created in whole
    or in part by me, under the same open source license (unless
    I am permitted to submit under a different license), as
    indicated in the file; or

(c) The contribution was provided directly to me by some other
    person who certified (a), (b) or (c) and I have not modified
    it.

(d) I understand and agree that this project and the contribution
    are public and that a record of the contribution (including
    all personal information I submit with it, including my
    sign-off) is maintained indefinitely and may be redistributed
    consistent with this project or the open source license(s)
    involved.

---
We require that every contribution to this repository is signed with a Developer Certificate of Origin. Additionally, please use your real name. We do not accept anonymous contributors nor those utilizing pseudonyms.

Each commit must include a DCO which looks like this

Signed-off-by: Jane Smith <jane.smith@email.com>

You may type this line on your own when writing your commit messages. However, if your user.name and user.email are set in your git configs, you can use -s or --signoff to add the Signed-off-by line to the end of the commit message.

* * *

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
| `events`          | Create it to define new event classes.                                    |                                    |
| `objects`         | Create it to define new objects.                                          |
| `profiles`        | Create it to define new profiles.                                         |


As a reference, take a look at the [Linux Extension](https://github.com/ocsf/ocsf-schema/tree/main/extensions/linux) that is currently added to OCSF.

## Looking to contribute to OCSF Server?

See the [ocsf-server](https://github.com/ocsf/ocsf-server) project documentation.
