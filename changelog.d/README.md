# Changelog files

Don't edit [CHANGELOG.md](../CHANGELOG.md) in a pull request. Add a file to this folder instead, named after your pull request's number, for example `changelog.d/1234.md`. Open the pull request first to get its number, then add the file. Each pull request adds its own file, so pull requests don't conflict over `CHANGELOG.md`.

When a release is prepared, a maintainer merges these files into the `Unreleased` section of `CHANGELOG.md` and deletes them.

## Format

Use the headings from `CHANGELOG.md`, and write each entry as a list item. Don't add a link to the pull request: it's added from the file name when the files are merged.

```markdown
### Added
#### Objects
- Added the `wifi` object describing IEEE 802.11 network identity, radio and security attributes.
#### Dictionary Attributes
- Added `ssid`, `bssid`, `band` and `band_id` attributes.

### Bugfixes
- Corrected the `type_uid` example in the `observable` object.
```

| Section | Sub-heading |
|---|---|
| `### Added`, `### Improved` | Required, one of: `#### Categories`, `#### Event Classes`, `#### Profiles`, `#### Objects`, `#### Observables`, `#### Platform Extensions`, `#### Dictionary Attributes` |
| `### Bugfixes`, `### Deprecated`, `### Breaking changes`, `### Misc` | None: entries go directly under the section |

An entry can wrap onto several lines; they're joined into one. Write entries the way the existing ones in `CHANGELOG.md` are written: start with what changed, such as `Added`, `Changed` or `Deprecated`, and put schema names in backticks.

## When you don't need one

- A pull request that doesn't change the schema (`events/`, `objects/`, `profiles/`, `extensions/`, `metaschema/`, `dictionary.json`, `categories.json` or `extensions.md`) doesn't need a file.
- A change that only edits the description or caption of an existing item doesn't need an entry. A maintainer adds the `skip changelog` label so the check passes.

## Checking your file

```bash
python .github/scripts/changelog.py check
```

```bash
python .github/scripts/changelog.py preview
```

`check` validates every file in this folder, and `preview` prints the `Unreleased` section with the files merged in. The Changelog check on pull requests runs the same validation and makes sure a pull request that changes the schema adds its file.

## Preparing a release

In the release prep pull request, run:

```bash
python .github/scripts/changelog.py build
```

It adds each entry, with its pull request link, under the matching heading of `Unreleased` in `CHANGELOG.md`, in pull request order, and deletes the files in this folder (except this README). Then add the version heading as usual.
