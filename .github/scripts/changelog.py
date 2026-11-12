#!/usr/bin/env python3
"""Changelog files for ocsf-schema.

Each pull request that changes the schema adds ``changelog.d/<PR number>.md``
instead of editing CHANGELOG.md, so pull requests don't conflict over one
file. See changelog.d/README.md for the format.

  check [--pr N --base SHA]  Validate every changelog file. With --pr, also
                             require this pull request's file (used by CI).
  preview                    Print the Unreleased section with the changelog
                             files merged in. Changes nothing.
  build                      Merge the changelog files into the Unreleased
                             section of CHANGELOG.md and delete them. Run when
                             preparing a release.

Uses only the standard library.
"""

from __future__ import annotations

import argparse
import os
import re
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
FRAGMENT_DIR = ROOT / "changelog.d"
CHANGELOG = ROOT / "CHANGELOG.md"
README_NAME = "README.md"
PR_URL = "https://github.com/ocsf/ocsf-schema/pull/{}"
SKIP_LABEL = "skip changelog"

# Sections as CHANGELOG.md lists them. Added and Improved group their entries
# under a sub-heading; the other sections take entries directly.
SECTIONS = ["Added", "Improved", "Bugfixes", "Deprecated", "Breaking changes", "Misc"]
SECTIONS_WITH_KINDS = {"Added", "Improved"}
KINDS = [
    "Categories",
    "Event Classes",
    "Profiles",
    "Objects",
    "Observables",
    "Platform Extensions",
    "Dictionary Attributes",
]

# A pull request that changes any of these needs a changelog file.
SCHEMA_PATHS = (
    "events/",
    "objects/",
    "profiles/",
    "extensions/",
    "metaschema/",
    "dictionary.json",
    "categories.json",
    "extensions.md",
)

FRAGMENT_NAME = re.compile(r"^(\d+)\.md$")
SECTION_LINE = re.compile(r"^###\s+(.+?)\s*$")
# Matches both `#### Objects` and CHANGELOG.md's `* #### Objects`.
KIND_LINE = re.compile(r"^\s*(?:[-*]\s+)?####\s+(.+?)\s*$")
# Group 1 is the list prefix (`- `, `* `, `1. `, with any indent).
ENTRY_LINE = re.compile(r"^(\s*(?:[-*]|\d+\.)\s+)(.*?)\s*$")
PR_LINK_AT_END = re.compile(r"\[#\d+\]\([^)\s]+\)$")


@dataclass
class Entry:
    pr: int
    section: str
    kind: str | None
    text: str


@dataclass
class Problem:
    message: str
    path: str | None = None
    line: int | None = None
    level: str = "error"


def _canonical(name: str, choices: list[str]) -> str | None:
    folded = name.casefold()
    return next((c for c in choices if c.casefold() == folded), None)


def _rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def fragment_paths() -> list[Path]:
    if not FRAGMENT_DIR.is_dir():
        return []
    return sorted(
        p
        for p in FRAGMENT_DIR.iterdir()
        if p.is_file() and p.name != README_NAME and not p.name.startswith(".")
    )


def parse_fragment(path: Path, pr: int) -> tuple[list[Entry], list[Problem]]:
    """Read one changelog file into entries, reporting any format problems."""
    entries: list[Entry] = []
    problems: list[Problem] = []
    rel = _rel(path)

    def problem(message: str, lineno: int) -> None:
        problems.append(Problem(message, rel, lineno))

    section: str | None = None
    kind: str | None = None
    # Entries under an unknown or misplaced heading are skipped; the heading
    # itself is reported once.
    bad_section = bad_kind = False
    current: Entry | None = None  # the entry that wrapped lines join

    for lineno, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        line = raw.rstrip()
        if not line.strip():
            current = None
            continue

        if m := KIND_LINE.match(line):
            current = None
            kind = _canonical(m.group(1), KINDS)
            bad_kind = True
            if bad_section:
                pass
            elif section is None:
                problem(
                    "Put an `### Added` or `### Improved` heading before "
                    "this sub-heading.",
                    lineno,
                )
            elif section not in SECTIONS_WITH_KINDS:
                problem(
                    f"`### {section}` takes entries directly, "
                    "without a `####` sub-heading.",
                    lineno,
                )
            elif kind is None:
                problem(
                    f"Unknown sub-heading `{m.group(1)}`. "
                    f"Use one of: {', '.join(KINDS)}.",
                    lineno,
                )
            else:
                bad_kind = False
            continue

        if m := SECTION_LINE.match(line):
            current = None
            section = _canonical(m.group(1), SECTIONS)
            kind = None
            bad_section, bad_kind = section is None, False
            if bad_section:
                problem(
                    f"Unknown section `### {m.group(1)}`. "
                    f"Use one of: {', '.join(SECTIONS)}.",
                    lineno,
                )
            continue

        skipping = bad_section or bad_kind
        if line.lstrip().startswith("#"):
            current = None
            problem("Use `###` for a section and `####` for a sub-heading.", lineno)
        elif m := ENTRY_LINE.match(line):
            current = None
            if skipping:
                continue
            if section is None:
                problem("Put a `###` section heading before this entry.", lineno)
            elif section in SECTIONS_WITH_KINDS and kind is None:
                problem(
                    f"Entries under `### {section}` go under a `####` "
                    f"sub-heading: {', '.join(KINDS)}.",
                    lineno,
                )
            elif not m.group(2):
                problem("This entry is empty.", lineno)
            else:
                current = Entry(pr, section, kind, m.group(2))
                entries.append(current)
        elif current is not None:
            current.text += " " + line.strip()
        elif not skipping:
            problem(
                "Expected a `###` section, a `####` sub-heading, "
                "or an entry starting with `-`.",
                lineno,
            )

    if not entries and not problems:
        problems.append(Problem("This file has no entries.", rel))
    return entries, problems


def load_fragments(
    renaming: frozenset[str] = frozenset(),
) -> tuple[list[Entry], list[Problem]]:
    """Read every changelog file, with entries in pull request order.

    `renaming` holds files already told to take this pull request's number,
    so they don't also get the general naming message.
    """
    entries: list[Entry] = []
    problems: list[Problem] = []
    for path in fragment_paths():
        name = FRAGMENT_NAME.match(path.name)
        if not name and _rel(path) not in renaming:
            problems.append(
                Problem(
                    "Name changelog files after the pull request number, "
                    "for example `changelog.d/1234.md`.",
                    _rel(path),
                )
            )
        found, found_problems = parse_fragment(path, int(name.group(1)) if name else 0)
        if name:
            entries += found
        problems += found_problems
    entries.sort(key=lambda e: e.pr)  # stable, so each file keeps its order
    return entries, problems


def _unreleased_bounds(lines: list[str]) -> tuple[int, int] | None:
    starts = (i for i, line in enumerate(lines) if line.startswith("## [Unreleased]"))
    start = next(starts, None)
    if start is None:
        return None
    ends = (i for i in range(start + 1, len(lines)) if lines[i].startswith("## "))
    return start, next(ends, len(lines))


def merge(changelog: str, entries: list[Entry]) -> tuple[str, list[str]]:
    """Insert entries under their headings in the Unreleased section.

    Each entry goes after the last line under its heading and reuses the list
    prefix of the entry above it. Existing lines are never changed.
    """
    lines = changelog.split("\n")
    bounds = _unreleased_bounds(lines)
    if bounds is None:
        return changelog, ["CHANGELOG.md has no `## [Unreleased]` heading."]
    start, end = bounds

    # (section, kind) -> [index of the block's last line, prefix of its last entry]
    blocks: dict[tuple[str, str | None], list] = {}
    section: str | None = None
    key: tuple[str, str | None] | None = None
    for i in range(start + 1, end):
        line = lines[i]
        if m := KIND_LINE.match(line):
            kind = _canonical(m.group(1), KINDS)
            key = (section, kind) if section and kind else None
            if key:
                blocks[key] = [i, None]
        elif m := SECTION_LINE.match(line):
            section = _canonical(m.group(1), SECTIONS)
            key = (section, None) if section else None
            if key:
                blocks[key] = [i, None]
        elif key and (m := ENTRY_LINE.match(line)):
            blocks[key] = [i, m.group(1)]
        elif key and line[:1].isspace() and line.strip():
            blocks[key][0] = i  # a wrapped line of the entry above

    inserts: dict[int, list[str]] = {}
    errors: dict[str, None] = {}  # an ordered set
    for entry in entries:
        block = blocks.get((entry.section, entry.kind))
        if block is None:
            if entry.kind:
                heading = f"`* #### {entry.kind}` heading under `### {entry.section}`"
            else:
                heading = f"`### {entry.section}` heading"
            errors[
                f"The Unreleased section of CHANGELOG.md has no {heading}. Restore "
                "it from the list of sections at the top of the file."
            ] = None
            continue
        last, prefix = block
        if prefix is None:
            prefix = "  1. " if entry.kind else "1. "
        text = entry.text
        if not PR_LINK_AT_END.search(text):
            text += f" [#{entry.pr}]({PR_URL.format(entry.pr)})"
        inserts.setdefault(last, []).append(prefix + text)

    merged: list[str] = []
    for i, line in enumerate(lines):
        merged.append(line)
        merged += inserts.get(i, [])
    return "\n".join(merged), list(errors)


def changed_files(base: str) -> list[tuple[str, str]]:
    """(status letter, path) for each file changed since the merge base."""
    out = subprocess.run(
        ["git", "diff", "--name-status", "--no-renames", "-z", f"{base}...HEAD"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    ).stdout
    fields = out.split("\0")
    return [(fields[i][0], fields[i + 1]) for i in range(0, len(fields) - 1, 2)]


def check_pull_request(pr: int, base: str) -> list[Problem]:
    """Require this pull request's changelog file when it changes the schema."""
    expected = f"changelog.d/{pr}.md"
    changes = changed_files(base)
    paths = [path for _, path in changes]

    misnamed = [
        path
        for status, path in changes
        if status == "A"
        and path.startswith("changelog.d/")
        and path not in (expected, f"changelog.d/{README_NAME}")
    ]
    if misnamed:
        return [
            Problem(
                f"Rename this file to `{expected}`, after this pull request's number.",
                path,
            )
            for path in misnamed
        ]

    if (ROOT / expected).is_file():
        print(f"Found {expected}.")
        return []
    if "CHANGELOG.md" in paths:
        return [
            Problem(
                f"This pull request edits CHANGELOG.md. Move the entry to "
                f"`{expected}` so it doesn't conflict with other pull requests; "
                "see changelog.d/README.md.",
                level="warning",
            )
        ]
    if not any(path.startswith(SCHEMA_PATHS) for path in paths):
        print("No schema files changed, so no changelog file is needed.")
        return []
    return [
        Problem(
            f"Add `{expected}` describing this change; see changelog.d/README.md. "
            "If the change doesn't need an entry, for example it only edits "
            f"descriptions, a maintainer can add the `{SKIP_LABEL}` label."
        )
    ]


def report(problems: list[Problem]) -> bool:
    """Print problems, as annotations under GitHub Actions. True if any is an error."""
    in_actions = os.environ.get("GITHUB_ACTIONS") == "true"
    for p in problems:
        place = [(k, v) for k, v in (("file", p.path), ("line", p.line)) if v]
        if in_actions:
            props = ",".join(f"{k}={v}" for k, v in place)
            message = p.message.replace("%", "%25").replace("\n", "%0A")
            print(
                f"::{p.level} {props}::{message}"
                if props
                else f"::{p.level}::{message}"
            )
        else:
            where = ":".join(str(v) for _, v in place)
            print(
                f"{where}: {p.level}: {p.message}"
                if where
                else f"{p.level}: {p.message}"
            )
    return any(p.level == "error" for p in problems)


def _merged_changelog() -> tuple[str | None, list[Entry]]:
    entries, problems = load_fragments()
    if report(problems):
        return None, entries
    text, errors = merge(CHANGELOG.read_text(encoding="utf-8"), entries)
    if report([Problem(e) for e in errors]):
        return None, entries
    return text, entries


def cmd_check(args: argparse.Namespace) -> int:
    pr_problems = []
    if args.pr is not None:
        pr_problems = check_pull_request(args.pr, args.base)
    _, problems = load_fragments(frozenset(p.path for p in pr_problems if p.path))
    if report(problems + pr_problems):
        return 1
    print(f"Checked {len(fragment_paths())} changelog file(s).")
    return 0


def cmd_preview(args: argparse.Namespace) -> int:
    text, _ = _merged_changelog()
    if text is None:
        return 1
    lines = text.split("\n")
    start, end = _unreleased_bounds(lines)
    print("\n".join(lines[start:end]).rstrip())
    return 0


def cmd_build(args: argparse.Namespace) -> int:
    paths = fragment_paths()
    text, entries = _merged_changelog()
    if text is None:
        return 1
    if not entries:
        print("No changelog files to merge.")
        return 0
    CHANGELOG.write_text(text, encoding="utf-8")
    for path in paths:
        path.unlink()
    print(
        f"Merged {len(entries)} entries from {len(paths)} file(s) into "
        "CHANGELOG.md and deleted the files."
    )
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    commands = parser.add_subparsers(dest="command", required=True)

    check = commands.add_parser("check", help="validate the changelog files")
    check.add_argument("--pr", type=int, help="require this pull request's file")
    check.add_argument("--base", help="the pull request's base commit (with --pr)")
    check.set_defaults(func=cmd_check)

    preview = commands.add_parser(
        "preview", help="print Unreleased with the files merged"
    )
    preview.set_defaults(func=cmd_preview)

    build = commands.add_parser("build", help="merge the files into CHANGELOG.md")
    build.set_defaults(func=cmd_build)

    args = parser.parse_args()
    if args.command == "check" and (args.pr is None) != (args.base is None):
        parser.error("--pr and --base go together")
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
