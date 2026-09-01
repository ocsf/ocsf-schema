# OCSF Extensions

This directory holds the **platform** extensions that ship with the core schema: Linux, Windows, and macOS.

Vendor extensions are registered in the [OCSF Extensions Registry](../extensions.md); the extension schema itself is not added here. Host the code in the OCSF GitHub org, in your own org, or keep it private. See [Where to host a vendor extension](../CONTRIBUTING.md#where-to-host-a-vendor-extension). To reserve a name and UID, follow [Register a vendor extension](../CONTRIBUTING.md#register-a-vendor-extension).

## Extension layout

Each extension is a subdirectory with an `extension.json` that defines its `caption`, `name`, `uid`, and `version`. For example, the Linux extension:

```json
{
  "caption": "Linux",
  "name": "linux",
  "uid": 1,
  "version": "1.10.0-dev"
}
```

The rest of the directory mirrors the top-level schema layout and may include:

| Name              | Description                                                                 |
| ----------------- | --------------------------------------------------------------------------- |
| `categories.json` | New categories. Category IDs must be `>= 30` to avoid collisions with core. |
| `dictionary.json` | New attributes.                                                             |
| `events`          | New event classes.                                                          |
| `includes`        | Shared data.                                                                |
| `objects`         | New objects.                                                                |
| `profiles`        | New profiles.                                                               |

See the [Linux extension](linux/) as a reference. If you are building a vendor extension schema in your own repository, use the same layout.
