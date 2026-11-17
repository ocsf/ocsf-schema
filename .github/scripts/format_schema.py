#!/usr/bin/env python3
"""Sort and format the schema's JSON files, and check their file names.

Every schema JSON file is written the same way:

- Two-space indentation, with non-ASCII characters written as they are.
- In every object, keys are ordered by the type of their value: numbers,
  strings, objects, arrays, null, then true/false. Keys of the same type are
  sorted by name, number-like keys (enum values) by number, and keys starting
  with `$` (`$include`) come first.
- A class or object's `profiles` list comes after the strings at the top of
  the file and before `attributes`.
- Every file ends with a newline.

An event class, object or profile file is named after its `name`, as
`<name>.json`. A file without `name`, such as an extension's patch of a core
object, has nothing to match.

  format_schema.py [PATH ...]          Rewrite the files that aren't formatted.
  format_schema.py --check [PATH ...]  Report them instead (used by CI).

With no paths, every schema JSON file is checked. Paths that aren't schema JSON
files are ignored, so a pre-commit hook can pass any changed files. Exits 1 if
a file needs formatting (with --check), can't be read, or doesn't match its
name.

Uses only the standard library.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SCHEMA_DIRS = ("events", "objects", "profiles", "extensions")
SCHEMA_FILES = ("categories.json", "dictionary.json", "version.json")
NAMED_DIRS = {"events", "objects", "profiles"}
FIX_COMMAND = "python .github/scripts/format_schema.py"

# Released names that differ from their file names. Renaming either one would
# break compatibility, so they stay as they are.
KNOWN_NAME_MISMATCHES = {
    "events/system/event_log_activity.json": "event_log_actvity",
    "extensions/windows/objects/registry_key.json": "reg_key",
    "extensions/windows/objects/registry_value.json": "reg_value",
}

NUMBER, STRING, PROFILES, OBJECT, ARRAY, NULL, BOOLEAN = range(7)
NUMBER_KEY = re.compile(r"-?\d+")


def is_schema_json(path: str) -> bool:
    parts = Path(path).parts
    return path.endswith(".json") and (
        path in SCHEMA_FILES or (len(parts) > 1 and parts[0] in SCHEMA_DIRS)
    )


def schema_paths() -> list[str]:
    paths = [name for name in SCHEMA_FILES if (ROOT / name).is_file()]
    for folder in SCHEMA_DIRS:
        paths += [
            p.relative_to(ROOT).as_posix() for p in (ROOT / folder).rglob("*.json")
        ]
    return sorted(paths)


def value_rank(value: object) -> int:
    if isinstance(value, bool):
        return BOOLEAN
    if isinstance(value, (int, float)):
        return NUMBER
    if isinstance(value, str):
        return STRING
    if isinstance(value, dict):
        return OBJECT
    if isinstance(value, list):
        return ARRAY
    return NULL


def sort_value(value: object, top: bool = False) -> object:
    """Return value with the keys of every object in schema order."""
    if isinstance(value, list):
        return [sort_value(item) for item in value]
    if not isinstance(value, dict):
        return value

    def key(name: str) -> tuple:
        rank = PROFILES if top and name == "profiles" else value_rank(value[name])
        if NUMBER_KEY.fullmatch(name):
            return (not name.startswith("$"), rank, 0, int(name), "")
        return (not name.startswith("$"), rank, 1, 0, name)

    return {name: sort_value(value[name]) for name in sorted(value, key=key)}


def _no_duplicates(pairs: list[tuple[str, object]]) -> dict:
    seen = {}
    for name, value in pairs:
        if name in seen:
            raise ValueError(f'"{name}" appears twice in one object')
        seen[name] = value
    return seen


def dump(value: object) -> str:
    return json.dumps(value, indent=2, ensure_ascii=False) + "\n"


def first_difference(a: str, b: str) -> int:
    """1-based number of the first line that differs."""
    a_lines, b_lines = a.splitlines(), b.splitlines()
    for number, (x, y) in enumerate(zip(a_lines, b_lines), 1):
        if x != y:
            return number
    # The lines match, so the difference is at the end: a missing newline on the
    # last line, or extra lines after it.
    return min(len(a_lines), len(b_lines)) + (len(a_lines) != len(b_lines))


def name_line(text: str) -> int | None:
    match = re.search(r'^  "name"\s*:', text, re.MULTILINE)
    return text.count("\n", 0, match.start()) + 1 if match else None


def report(level: str, path: str, line: int | None, message: str) -> None:
    if os.environ.get("GITHUB_ACTIONS") == "true":
        place = f"file={path},line={line}" if line else f"file={path}"
        print(f"::{level} {place}::{message}")
    else:
        print(
            f"{path}:{line}: {level}: {message}"
            if line
            else f"{path}: {level}: {message}"
        )


def process(path: str, check: bool) -> tuple[bool, bool]:
    """Format or check one file. Returns (needs formatting, has an error)."""
    try:
        text = (ROOT / path).read_text(encoding="utf-8-sig")
        data = json.loads(text, object_pairs_hook=_no_duplicates)
    except (OSError, ValueError) as e:
        report(
            "error",
            path,
            getattr(e, "lineno", None),
            f"Can't read this file as JSON: {e}",
        )
        return False, True

    error = False
    name = data.get("name") if isinstance(data, dict) else None
    folders = set(Path(path).parts[:-1])
    if isinstance(name, str) and NAMED_DIRS & folders:
        stem = Path(path).stem
        if name != stem and KNOWN_NAME_MISMATCHES.get(path) != name:
            report(
                "error",
                path,
                name_line(text),
                f'`name` is "{name}", so the file should be named {name}.json. '
                "Rename the file or change `name` so they match.",
            )
            error = True

    formatted = dump(sort_value(data, top=True))
    if formatted == text:
        return False, error
    if not check:
        (ROOT / path).write_text(formatted, encoding="utf-8")
        print(f"Formatted {path}")
        return True, error

    problems = []
    as_is = dump(data)
    if as_is != formatted:
        problems.append("its keys are out of order")
    if as_is == text + "\n":
        problems.append("it doesn't end with a newline")
    elif as_is != text:
        problems.append("its spacing differs from the other schema files")
    report(
        "error",
        path,
        first_difference(text, formatted),
        f"This file isn't formatted: {' and '.join(problems)}. "
        f"Run `{FIX_COMMAND}` to fix it.",
    )
    return True, error


def main() -> int:
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument(
        "paths", nargs="*", help="files to format (default: all schema JSON files)"
    )
    parser.add_argument(
        "--check", action="store_true", help="report files instead of rewriting them"
    )
    args = parser.parse_args()

    if args.paths:
        relative = [
            Path(os.path.relpath(Path(p).resolve(), ROOT)).as_posix()
            for p in args.paths
        ]
        paths = [p for p in relative if is_schema_json(p)]
    else:
        paths = schema_paths()

    results = [process(path, args.check) for path in paths]
    unformatted = sum(needs for needs, _ in results)
    errors = any(error for _, error in results)
    done = "Files that need formatting" if args.check else "Files formatted"
    print(f"Checked {len(paths)} schema file(s). {done}: {unformatted}.")
    return 1 if errors or (args.check and unformatted) else 0


if __name__ == "__main__":
    sys.exit(main())
