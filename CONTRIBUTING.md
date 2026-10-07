# OCSF Contribution Guide

Rajas Panat, July 2022; Updated September 2026.

Contributions by Mike Radka, Donovan Kolbly.

This documentation presents guidelines and expected etiquettes to successfully contribute to the development of OCSF Schemas and the framework itself.

---

## Pull Request Guidelines

All contributors must submit their changes via pull requests. If you're not familiar with pull requests, please read [the GitHub documentation](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/about-pull-requests). Following are a few guidelines and expectations for submitting a PR.

1. Fork [ocsf-schema](https://github.com/ocsf/ocsf-schema). For changes to [ocsf-docs](https://github.com/ocsf/ocsf-docs) or [ocsf-server](https://github.com/ocsf/ocsf-server), follow that repository's contributing docs.
2. Make the desired changes in the forked repo and [verify they work](#verifying-the-changes) before opening a PR.
3. Push the changes to the forked repo.
4. Create a **Pull Request** to merge into `ocsf/ocsf-schema`. You'll need at least 3 approvals to get the PR merged.
5. Follow the guidelines in the PR template.
    1. Keep the PR focused: a single PR **must** contain related changes.
    2. Each commit must include a DCO [Developer's Certificate of Origin](#developers-certificate-of-origin-11).
    3. Add a numbered entry to the matching subsection of `Unreleased` in [CHANGELOG.md](CHANGELOG.md) (`Added`, `Improved`, `Deprecated`, `Misc`, and so on). Include the PR link once the PR exists.
    4. Describe your change in as much detail as possible.
    5. Confirm that you have tested the changes, and the local verification run was error free.
    6. Check the Preview tab to ensure everything looks as expected.
    7. Once the PR is ready, add relevant labels and submit it.
    8. Resolve any GitHub Action failures or warnings on your pull request, and stay involved in the conversation.
6. Thank you for your contribution!

---

## Key OCSF Terminology

1. **Field**: A field is a unique identifier name for a piece of data contained in OCSF. Each field also designates a corresponding data_type.
2. **Object**: An object is a collection of contextually related fields and other objects. It is also a data_type in OCSF.
3. **Attribute**: An attribute is the more generic name for both fields and objects in OCSF. A field is a scalar attribute while an object is a complex attribute.
4. **Event Class**: An event is represented by an Event Class, which are a particular set of attributes (including fields and objects) representing a log line or telemetry submission at a point in time.
5. **Category**: A Category organizes event classes that represent a particular domain.
6. **Profile**: A mix-in set of attributes that can be applied to event classes and objects across categories, so the same extra context does not require new classes.

More details about OCSF concepts, terminology and use-cases can be found in [Understanding OCSF](https://github.com/ocsf/ocsf-docs/blob/main/overview/understanding-ocsf.md).

---

## Schema changes

### Adding an event class, in brief

1. Determine all the `attributes` (including fields and objects) you would want to add in the `event_class`.
2. Check [dictionary.json](dictionary.json) and the [objects](objects/) folder; many of your desired attributes may already be present.
3. Define the missing attributes → [Adding/Modifying an `attribute`](#addingmodifying-an-attribute)
4. Determine which category you would want to add your event_class in, note its `name`
5. Create a new file → `<event_class_name.json>` inside the category specific subfolder in the [events](events/) folder. Template: [templates/event_class_name.json](templates/event_class_name.json)
6. Define the `event_class` itself → [Adding/Modifying an `event_class`](#addingmodifying-an-event_class)
7. Finally, [verify the changes](#verifying-the-changes) before opening a PR.

---

### Adding/Modifying an `attribute`

1. All the available `attributes` — `fields` and `objects` in OCSF — are and will need to be defined in the attribute dictionary, [dictionary.json](dictionary.json), and the [objects](objects/) folder if defining an object.
2. Determine if a new attribute is required for your change; it might already be defined in the attribute dictionary and/or the [objects](objects/) folder.
3. Before adding a new attribute, review the following OCSF attribute conventions:

   - Attribute names must be a valid UTF-8 sequence.
   - Attribute names must be all lower case.
   - Combine words using underscore.
   - No special characters except underscore.
   - Use present tense unless the attribute describes historical information.
   - Use singular and plural names properly to reflect the field content. Example: use `events_per_sec` rather than `event_per_sec`.
   - When attribute represents multiple entities, the attribute name should be pluralized and the value type should be an array. Example: `process.loaded_modules` includes multiple values — a loaded module names list.
   - Avoid repetition of words. Example: `src_endpoint.src_ip` should be `src_endpoint.ip`.
   - Avoid abbreviations when possible. Some exceptions can be made for well-accepted abbreviation. Example: `ip`, `os`, `cve` etc.

#### Caption & description style (normative & neutral)

To keep OCSF suitable for international standardization (e.g. ITU ratification), captions and descriptions must be self-contained, vendor-neutral, and free of personal or politically-charged framing. An automated reviewer comments on PRs that don't follow these rules; the same rules are summarized here so you can get them right up front.

1. **No authoritative URLs in captions or descriptions.** Refer to the source by name (e.g. `RFC 1035`, `MITRE ATT&CK`, `ASTM F3411-22a`) and put the link in the container's `references` array. URLs are fine only as illustrative example values, never as the citation for a field.
2. **No trademark/registered marks (®, ™, ℠) in captions or descriptions.** Use generic wording and keep the marked, proprietary name in `references` only. See `objects/attack.json` for the canonical pattern. (The canonical proprietary-source objects — `attack`, `atlas`, `d3fend`, `d3f_tactic`, `d3f_technique` — may keep the mark in their own primary caption.)
3. **No company/vendor/product names in captions or descriptions.** Use the generic technology or standard, and keep any vendor name to `examples` only. Product names that *are* the modeled domain inside a platform extension (e.g. Windows registry concepts under `extensions/windows/`) are an exception.
4. **Keep descriptions technical, not personal or political.** Write descriptions as data definitions, not as descriptions of a real person or a nation/state. Avoid anthropomorphic/biographical framing, personal or protected-class characterization (race, religion, health, citizenship, political affiliation, etc.), and politically-charged wording. This does **not** ban legitimate entities — `user`, `account`, `identity`, `actor`, and `person` remain valid technical terms, and geographic values stored as data (e.g. an ISO country code) are fine. When phrasing drifts toward describing a human, reframe toward the account/identity/principal — e.g. prefer "the user account and its security-relevant attributes" over "the user and what they personally like to do".

#### How to define a `field` in the dictionary?

To add a new field in OCSF, you need to define it in [dictionary.json](dictionary.json) as described below.

Sample entry in the dictionary:

```json
"uid": {
  "caption": "Unique ID",
  "description": "The unique identifier. See specific usage.",
  "type": "string_t"
}
```

Choose a **unique** field you want to add, `uid` in the example above and populate it as described below.

1. `caption` → Add a user friendly name to the field.
2. `description` → Add a concise description to define the attributes.
    1. Note that `field` descriptions can be overridden in the `event_class`/`object`, therefore if it's a common field (like name, label, uid etc) feel free to add a generic description; specific descriptions can be added in the `event_class`/`object` definition. For example,
    2. A generic definition of `uid` in the dictionary:
        1. `uid`: `The unique identifier. See specific usage.`
    3. Specific description of `uid` in the `vulnerability` object:
        1. `uid`: `Unique Identifier/s of the reported vulnerability. e.g. CVE ID/s`
3. `type` → Review OCSF data_types and ensure you utilize appropriate types while defining new fields.
    1. All the available data_types can be accessed on [schema.ocsf.io/data_types](https://schema.ocsf.io/data_types).
    2. They are also accessible in your local instance of the ocsf-server: [http://localhost:8080/data_types](http://localhost:8080/data_types)
4. `is_array` → This is a boolean key:value pair that you would need to add if the field you are defining is an array.
    1. e.g. `"is_array": true`
5. Integer enums → Normalized enumerations are `integer_t` attributes whose names end in `_id` (arrays: `_ids`). Declare a string `sibling` (usually the same name without `_id`, for example `severity_id` / `severity`) and an `enum` map. Include `0` Unknown and `99` Other unless you are matching an existing documented exception. Classification siblings use `_name` (`class_uid` / `class_name`).

    ```json
    "severity_id": {
      "caption": "Severity ID",
      "description": "The normalized identifier of the event/finding severity.",
      "sibling": "severity",
      "type": "integer_t",
      "enum": {
        "0": {
          "caption": "Unknown",
          "description": "The severity is unknown."
        },
        "99": {
          "caption": "Other",
          "description": "The severity is not mapped. See the `severity` attribute."
        }
      }
    }
    ```

#### How to define an `object`?

1. All the available `objects` need to be defined as individual field entries in [dictionary.json](dictionary.json) and as distinct `.json` files in the [objects](objects/) folder.
2. Review existing Objects, determine if a modification of the existing object would be sufficient or if there's a need for a completely new object.
3. Use [templates/object_name.json](templates/object_name.json) to get started with the `.json` file definition.

    An example `vulnerability.json` object file:

    ```json
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
6. `extends` → Ensure the value is `object` or an existing object, e.g. `_entity` (All objects in OCSF must extend a base definition of `object` or another existing object.)
7. `name` → Add a **unique** name of the object. `name` must match the filename of the actual `.json` file.
8. `attributes` → Add the attributes that you want to define in the object,
    1. `requirement` → For each attribute ensure you add a requirement value. Valid values are `optional`, `required`, `recommended`
    2. `$include` → You can include attributes from other places; to do so, specify a virtual attribute called `$include` and give its value as the list of files (relative to the root of the schema repository) that should contribute their attributes to this object. e.g.

        ```json
        "attributes": {
          "$include": [
            "profiles/host.json"
          ]
        }
        ```

**Note:** If you want to create an object which would act only as a base for other objects, you must prefix the object `name` and the actual `json` filename with an `_`. The resultant object will not be visible in the [OCSF Server](https://schema.ocsf.io/objects). For example, take a look at the [`_entity`](objects/_entity.json) object.

Sample entry in `dictionary.json`:

```json
"vulnerability": {
  "caption": "Vulnerability",
  "description": "The vulnerability object describes details related to the observed vulnerability.",
  "type": "vulnerability"
}
```

Choose a **unique** object you want to add, `vulnerability` in the example above and populate it as described below.

1. `caption` → Add a user friendly name to the object
2. `description` → Add a concise description to define the object.
3. `type` → Add the type of the object you are defining.
4. `is_array` → This is a boolean key:value pair that you would need to add if the object you are defining is an array.
    1. e.g. `"is_array": true`

---

### Adding/Modifying an `event_class`

1. All the available Event Classes are defined as `.json` files in the [events](events/) folder.
2. Review existing Event Classes, determine if a modification of the existing class would be sufficient or if there's a need for a completely new event_class.
3. To define a new class:
    1. Create a new file → `<event_class_name.json>` inside the category specific subfolder in the [events](events/) folder.
    2. Use [templates/event_class_name.json](templates/event_class_name.json) to get started with the `.json` definition.
    3. `uid` → Select an integer in the range 0–99. Ensure the integer is **unique** within the category.
        - Note: Without `uid`, an event_class won't be visible in the ocsf-server.
        - Do not set `class_uid` or `type_uid` by hand; the compiler derives them (`class_uid` = `category_uid * 1000 + uid`).
    4. `caption` → Add a user friendly name to the event_class.
    5. `description` → Add a concise description to define the attributes.
    6. `name` → Add a **unique** name of the event_class. Ensure it matches the file name to maintain consistency.
    7. `extends` → Use the category class (`network`, `system`, `finding`, and so on) so the new class inherits that category's attributes. Only a new category root should extend `base_event`. For example, `events/network/http_activity.json` extends `network`.
    8. `attributes` → Add the attributes that you want to define in the event_class,
        1. `group` → For each attribute ensure you add a group value. Valid values are `classification`, `context`, `occurrence`, `primary`
        2. `requirement` → For each attribute ensure you add a requirement value. Valid values are `optional`, `required`, `recommended`
        3. `$include` → As for objects, you can also include attributes from other places; to do so, specify the list of files (relative to the root of the schema repository) that should contribute their attributes to this object. e.g.

            ```json
            "attributes": {
              "$include": [
                "profiles/cloud.json"
              ]
            }
            ```

    9. `constraints` → For each class you can add constraints on the attribute requirements. Valid constraint types are `at_least_one`, `just_one`. e.g.

        ```json
        "constraints": {
          "at_least_one": [
            "uid",
            "name"
          ]
        }
        ```

        A Constraint is a documented rule subject to validation that requires at least one of the specified recommended attributes of a class to be populated.

---

### Adding/Modifying a `profile`

A profile is a mix-in set of attributes that can be applied to event classes and objects across categories. Use a profile when the same extra context (host, cloud, security control, container, and so on) should be optional on many classes, instead of creating new classes. For design background, see [Profiles are Powerful](https://github.com/ocsf/ocsf-docs/blob/main/articles/profiles-are-powerful.md).

Review existing files in [profiles](profiles/) before adding a new one. Applying an existing profile to a class or object is often enough.

#### Define a profile

1. Every attribute in the profile must already be defined in [dictionary.json](dictionary.json) (and [objects](objects/) if it is an object).
2. Create `profiles/<name>.json`. `name` must match the filename. Template: [templates/profile_name.json](templates/profile_name.json).
3. Required keys:
    1. `caption` → A short, user-friendly name.
    2. `description` → A concise description of when to apply the profile.
    3. `meta` → Must be `profile`.
    4. `name` → A **unique** name, lowercase, words joined with underscore.
    5. `attributes` → Each attribute needs a `requirement` (`optional`, `required`, or `recommended`). You may override `description` or `group` here.
4. Optional `annotations.group` sets a default group for attributes that do not specify one. See [profiles/host.json](profiles/host.json).

Example `profiles/cloud.json`:

```json
{
  "caption": "Cloud",
  "description": "The attributes that describe information specific to Cloud services/applications.",
  "meta": "profile",
  "name": "cloud",
  "attributes": {
    "api": {
      "group": "context",
      "requirement": "optional"
    },
    "cloud": {
      "group": "primary",
      "requirement": "required"
    }
  }
}
```

The `datetime` profile is special: it has an empty `attributes` map, and the compiler adds `datetime_t` siblings next to `timestamp_t` fields. Do not copy that pattern for ordinary profiles.

#### Apply a profile to a class or object

Always list the profile `name` in the class or object's `profiles` array so events can be filtered by `metadata.profiles`. Then pick one of these patterns:

1. **Augment (most common).** `$include` the profile file so its attributes are mixed in when the profile is applied. See [events/network/network.json](events/network/network.json).

    ```json
    "profiles": ["cloud"],
    "attributes": {
      "$include": [
        "profiles/cloud.json"
      ]
    }
    ```

2. **Native.** The class already defines the profile's attributes. List the profile in `profiles`, but do not `$include` it. You can still override `group` or `requirement` on those attributes.

3. **Partially native.** `$include` the profile, then set `"profile": null` on attributes that must remain even when the profile is not applied. Without `profile: null`, turning the profile off in the browser would hide those native attributes. See `actor` and `device` on [events/system/system.json](events/system/system.json).

    ```json
    "actor": {
      "group": "primary",
      "requirement": "required",
      "profile": null
    }
    ```

4. **Hybrid.** Some attributes on an object should appear only when a profile is applied to the enclosing class, but they are *not* part of the profile definition itself. List the profile in `profiles` and set `"profile": "<name>"` on those attributes. Do **not** `$include` the profile on the object, or you would duplicate the profile's class-level attributes onto the object. See `cloud_partition`, `region`, and `zone` on [objects/resource_details.json](objects/resource_details.json).

    ```json
    "cloud_partition": {
      "profile": "cloud",
      "requirement": "optional"
    }
    ```

Apply a profile at the category class when every class in that category should offer it. Apply it on [events/base_event.json](events/base_event.json) only when it is valid on essentially every class.

Platform extension profiles live under `extensions/<platform>/profiles/` (for example [extensions/linux/profiles/linux_users.json](extensions/linux/profiles/linux_users.json)).

---

### Deprecating an attribute, object, class, or enum value

The `@deprecated` annotation can be added to a dictionary attribute, an attribute used within a class/object/profile, a whole object, a whole event class, or an individual enum value. Follow the steps below:

1. Create a GitHub issue, explaining why the item needs to be deprecated and what the alternate solution is.
2. Add the `@deprecated` annotation as a JSON property of the item that is the subject of deprecation.

    ```json
    "@deprecated": {
      "message": "Use the <code>ALTERNATE_ATTRIBUTE</code> attribute instead.",
      "since": "semver",
      "superseded_by": ["ALTERNATE_ATTRIBUTE"]
    }
    ```

    - `message` (required) — a human-readable explanation. Name the replacement in a `<code>` tag using its actual name (not its display caption), so the text matches the machine-readable `superseded_by`. Cite a path in one `<code>` tag: `Use the <code>compliance.checks</code> attribute instead.`, not `Use the <code>checks</code> array in the <code>compliance</code> object instead.` Add any extra guidance as a following sentence.
    - `since` (required) — the version after which the item is deprecated.
    - `superseded_by` (required) — a machine-readable list of the replacement(s). List every concrete replacement. When the item is removed with no successor, use an empty array `[]` to state that explicitly.

3. What `superseded_by` may reference (use the form that matches where the replacement lives):
    - A dictionary attribute name (e.g. `["application"]`), or the name of another attribute in the same class/object (e.g. `["resources"]`).
    - A fully-qualified path into another object or class — e.g. `["job_action.cmd_line"]`, `["email.uid"]`, `["dns_activity.opcode"]`, or `["cpu_info_list[*].cores"]`.
    - A class or object name, when deprecating a whole class/object — e.g. `["finding_info"]` or `["evidence_info"]`.
    - Another enum value's key, when deprecating an enum value — e.g. `["8"]`.
    - Multiple replacements are allowed — e.g. `["labels", "tags"]` or `["cpu_info_list[*].model", "cpu_info_list[*].vendor_name"]`.

    > **Arrays.** When the replacement is a field inside an array of objects, mark the array with `[*]` and name the field — `["related_cwes[*].uid"]`, not `["related_cwes"]`. Reference the array alone only when the whole array is the replacement.

    > **Caution — bare names vs. qualified paths.** A bare attribute name marks the replacement *globally*: the schema browser will show a "Supersedes" note on that attribute **everywhere it is used**. Only use a bare name when the replacement genuinely is the schema-wide successor (e.g. `tag` → `labels`). When the replacement is context-specific, use the fully-qualified path instead — e.g. `cpu_type` (a CPU field) must reference `["cpu_info_list[*].vendor_name"]`, **not** `["vendor_name"]`; the bare form would incorrectly stamp the note on `vendor_name` in every unrelated object (vulnerability, product, agent, ...) that shares that generic name.

4. How the schema browser renders it (the compiler resolves `superseded_by` in browser mode):
    - Same-scope replacement (a dictionary attribute, another attribute in the same class/object, a class/object name, or another enum value of the same attribute) → a "Supersedes" note is shown by default on the **replacement**, pointing back to the deprecated item.
    - Cross-container replacement (a dotted path into a different object/class) → a "Replaced by" link is shown on the **deprecated** item, linking to the replacement's page.

5. Example of a deprecated field (dictionary attribute)

    ```json
    "packages": {
      "@deprecated": {
        "message": "Use the <code>affected_packages</code> attribute instead.",
        "since": "1.0.0",
        "superseded_by": ["affected_packages"]
      },
      "caption": "Software Packages",
      "description": "List of vulnerable packages as identified by the security product",
      "is_array": true,
      "type": "package"
    }
    ```

6. Example of a deprecated object

    ```json
    {
      "caption": "Finding",
      "description": "The Finding object describes metadata related to a security finding generated by a security tool or system.",
      "extends": "object",
      "name": "finding",
      "@deprecated": {
        "message": "Use the new <code>finding_info</code> object.",
        "since": "1.0.0",
        "superseded_by": ["finding_info"]
      },
      "attributes": {}
    }
    ```

7. Example of a deprecated enum value (`superseded_by` references the replacement value's key)

    ```json
    "9": {
      "caption": "REG_QWORD_LITTLE_ENDIAN",
      "@deprecated": {
        "message": "Use <code>REG_QWORD</code> instead.",
        "since": "1.6.0",
        "superseded_by": ["8"]
      }
    }
    ```

8. Example of an item removed with no replacement (empty `superseded_by`)

    ```json
    "obsolete_field": {
      "@deprecated": {
        "message": "This field is obsolete and has no replacement.",
        "since": "1.6.0",
        "superseded_by": []
      },
      "caption": "Obsolete Field",
      "type": "string_t"
    }
    ```

---

## Verifying the changes

Before you open a PR, confirm the schema is valid and compiles. Pull requests to `main` run metaschema validation, a lean compile, and a backwards-compatibility check. Spellcheck runs on PRs as a warning only.

Install the tools with `pip` in a virtual environment. The compiler requires **Python 3.14+**. The validator needs Python 3.11+ (3.14 works).

1. From the schema repository root, run the metaschema validator ([ocsf-validator](https://github.com/ocsf/ocsf-validator)):

    ```bash
    pip install "ocsf-validator>=0.2,<0.3"
    python -m ocsf_validator .
    ```

    FATAL and ERROR findings fail the command. WARNINGs do not; still fix warnings that are about your change.

2. Compile the schema ([ocsf-schema-compiler](https://github.com/ocsf/ocsf-schema-compiler)). JSON is written to stdout and logs to stderr — redirect the JSON, or it will flood your terminal. This lean compile is what CI runs:

    ```bash
    pip install ocsf-schema-compiler
    ocsf-schema-compiler . > /dev/null
    ```

    A typical compile failure looks like:

    ```text
    Attribute "event_uid" from "HTTP Activity" is not a defined dictionary attribute
    Compilation failed: ...
    ```

3. To browse locally, compile in **browser mode** (`-b`) and point [ocsf-server](https://github.com/ocsf/ocsf-server) v4+ at that file via `SCHEMA_FILE`. Lean JSON will not work in the server. Follow the [ocsf-server README](https://github.com/ocsf/ocsf-server/blob/main/README.md).

    ```bash
    ocsf-schema-compiler . -b > compiled-browser.json
    ```

    The server should start with no errors.

CI also runs `python -m ocsf.validate.compatibility` (from [ocsf-lib](https://pypi.org/project/ocsf-lib/)) against the last stable release. You do not need to run that locally unless you are changing classification IDs or removing attributes.

Address every compile error and validator ERROR before submitting.

---

## Developer's Certificate of Origin 1.1

By making a contribution to this project, I certify that:

> (a) The contribution was created in whole or in part by me and I
> have the right to submit it under the open source license
> indicated in the file; or
>
> (b) The contribution is based upon previous work that, to the
> best of my knowledge, is covered under an appropriate open
> source license and I have the right under that license to
> submit that work with modifications, whether created in whole
> or in part by me, under the same open source license (unless
> I am permitted to submit under a different license), as
> indicated in the file; or
>
> (c) The contribution was provided directly to me by some other
> person who certified (a), (b) or (c) and I have not modified
> it.
>
> (d) I understand and agree that this project and the contribution
> are public and that a record of the contribution (including
> all personal information I submit with it, including my
> sign-off) is maintained indefinitely and may be redistributed
> consistent with this project or the open source license(s)
> involved.

We require that every contribution to this repository is signed with a Developer Certificate of Origin. Additionally, please use your real name. We do not accept anonymous contributors nor those utilizing pseudonyms.

Each commit must include a DCO which looks like this:

```text
Signed-off-by: Jane Smith <jane.smith@email.com>
```

You may type this line on your own when writing your commit messages. However, if your `user.name` and `user.email` are set in your git configs, you can use `-s` or `--signoff` to add the Signed-off-by line to the end of the commit message.

---

## OCSF Extensions

OCSF can be extended with additional attributes, objects, profiles, event classes, and categories. Each public extension has a unique `name` and `uid` so it does not collide with the core schema or other extensions.

Vendor extensions are **registered** in this repository; the extension schema itself is not added under `extensions/`. (The Linux, Windows, and macOS platform extensions already live there.)

### Where to host a vendor extension

Registration reserves a name and UID. The schema files live in a separate repository. You can:

1. **Host it in the OCSF GitHub organization.** Ask `@ocsf/ocsf-maintainers` about creating a repo under [github.com/ocsf](https://github.com/ocsf). Public examples include [ocsf/aws](https://github.com/ocsf/aws), [ocsf/splunk](https://github.com/ocsf/splunk), [ocsf/symantec](https://github.com/ocsf/symantec), and [ocsf/dev-ext](https://github.com/ocsf/dev-ext).
2. **Host it in your own organization** (or any other public git host).
3. **Keep it private.** You can still register a name and UID so they are reserved. Leave the registry `Repository` cell empty.

Use the same directory layout as the platform extensions; see [extensions/README.md](extensions/README.md). Compile a vendor extension with the core schema using `ocsf-schema-compiler path/to/ocsf-schema -e path/to/your-extension`.

If the code is public, add a link in the registry's optional `Repository` column.

### Register a vendor extension

To reserve a name and UID, open a pull request that only updates the registry. Follow [#1701](https://github.com/ocsf/ocsf-schema/pull/1701) as the example.

1. Add a row to the [OCSF Extensions Registry](extensions.md) with a unique caption, name, UID, a short notes line, and an optional `Repository` URL. Take the next unused vendor UID (the registry counts down from 998).
2. Add an `Unreleased` entry in [CHANGELOG.md](CHANGELOG.md), for example: `New Extension registration for <Vendor>`.
3. Open a pull request using the PR template, and request reviewers as usual.
4. Email [info@ocsf.io](mailto:info@ocsf.io) from an official company address so maintainers can confirm the request is authorized by the organization it represents.

Example registry row:

| Caption       | Name     | UID | Notes                         | Repository |
| ------------- | -------- | --- | ----------------------------- | ---------- |
| _Vendor Name_ | _vendor_ | 123 | The _Vendor_ schema extension | |

---

## Looking to contribute to OCSF Server?

See the [ocsf-server](https://github.com/ocsf/ocsf-server) project documentation.
