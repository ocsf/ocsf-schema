#!/usr/bin/env python3
"""Release steps for ocsf-schema.

  prep [--date DATE]  For the release prep pull request: add the changelog
                      files to CHANGELOG.md under the release's heading (see
                      changelog.py build), set the release version X.Y.Z in
                      place of X.Y.Z-dev, and update the spellcheck word list.
  words               Add the words cspell doesn't know to the spellcheck word
                      list, .github/.project-words.txt. A word that looks like
                      a typo is listed instead of added: cspell can fix it with
                      one edit, and the fixed spelling is used more often in
                      the repository. Fix it, or add it to the list by hand.
                      Needs cspell (npm install -g cspell).
  next [VERSION]      After the release is published: set the next version,
                      VERSION-dev (default: the next minor version), and make
                      the release the backwards compatibility baseline.

The version is set in version.json, every extensions/*/extension.json, the
README badge, and the example in extensions/README.md.

Uses only the standard library.
"""

from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CHANGELOG_SCRIPT = ROOT / ".github" / "scripts" / "changelog.py"
CHANGELOG = ROOT / "CHANGELOG.md"
VERSION_FILE = ROOT / "version.json"
WORDS_FILE = ROOT / ".github" / ".project-words.txt"
CSPELL_CONFIG = ROOT / ".github" / ".cspell.yaml"
COMPATIBILITY_WORKFLOW = (
    ROOT / ".github" / "workflows" / "validate-backwards-compatibility.yml"
)
CONTRIBUTING = ROOT / "CONTRIBUTING.md"

RELEASE = re.compile(r"(\d+)\.(\d+)\.(\d+)")
JSON_VERSION = re.compile(r'("version"\s*:\s*")([^"]*)(")')
# shields.io reads a single dash as a separator, so the badge doubles dashes.
BADGE_VERSION = re.compile(r"(img\.shields\.io/badge/version-)(.+?)(-blue\.svg)")
BASELINE_REF = re.compile(r'(^\s*ref:\s*")([^"]*)(")', re.MULTILINE)
BASELINE_DOC = re.compile(r"(\(currently `)([^`]*)(`, set in \[validate-backwards)")
UNKNOWN_WORD = re.compile(r"^(.+?):(\d+):\d+ - Unknown word \((.+?)\)")


class ReleaseError(Exception):
    pass


class Field:
    """One version string in a file, found by a pattern that must match once."""

    def __init__(self, path: Path, pattern: re.Pattern[str], badge: bool = False):
        self.path = path
        self.pattern = pattern
        self.badge = badge

    def _match(self, text: str) -> re.Match[str]:
        matches = list(self.pattern.finditer(text))
        if len(matches) != 1:
            raise ReleaseError(
                f"{self.rel}: expected one version string, found {len(matches)}"
            )
        return matches[0]

    @property
    def rel(self) -> str:
        return self.path.relative_to(ROOT).as_posix()

    def read(self) -> str:
        value = self._match(_read(self.path)).group(2)
        return value.replace("--", "-") if self.badge else value

    def write(self, value: str) -> None:
        text = _read(self.path)
        match = self._match(text)
        if self.badge:
            value = value.replace("-", "--")
        _write(self.path, text[: match.start(2)] + value + text[match.end(2) :])


def _read(path: Path) -> str:
    return path.read_bytes().decode("utf-8")


def _write(path: Path, text: str) -> None:
    path.write_bytes(text.encode("utf-8"))


def _count(n: int, noun: str) -> str:
    return f"{n} {noun}" if n == 1 else f"{n} {noun}s"


def version_fields() -> list[Field]:
    extensions = sorted((ROOT / "extensions").glob("*/extension.json"))
    return [
        Field(VERSION_FILE, JSON_VERSION),
        *(Field(path, JSON_VERSION) for path in extensions),
        Field(ROOT / "README.md", BADGE_VERSION, badge=True),
        Field(ROOT / "extensions" / "README.md", JSON_VERSION),
    ]


def current_version() -> str:
    """version.json's version, after checking every version file agrees."""
    version = json.loads(_read(VERSION_FILE))["version"]
    problems = []
    for field in version_fields():
        try:
            found = field.read()
        except ReleaseError as e:
            problems.append(str(e))
            continue
        if found != version:
            problems.append(f"{field.rel}: has {found}, but version.json has {version}")
    if problems:
        raise ReleaseError("\n".join(["Fix the version files first:", *problems]))
    return version


def set_version(version: str) -> None:
    for field in version_fields():
        field.write(version)
    print(f"Set the version to {version} in {len(version_fields())} files.")


def parse_release(version: str) -> tuple[int, int, int]:
    match = RELEASE.fullmatch(version.removeprefix("v"))
    if not match:
        raise ReleaseError(f"{version} isn't a release version like 1.10.0")
    return tuple(int(part) for part in match.groups())


def cspell() -> str:
    path = shutil.which("cspell")
    if path is None:
        raise ReleaseError(
            "cspell isn't installed. Install it with `npm install -g cspell`, "
            "then run this again."
        )
    return path


def _run(*args: str) -> str:
    result = subprocess.run(args, cwd=ROOT, capture_output=True, text=True)
    if result.returncode != 0:
        raise ReleaseError(f"{' '.join(args[:2])} failed:\n{result.stderr.strip()}")
    return result.stdout


def unknown_words() -> dict[str, list[str]]:
    """Each word cspell doesn't know, with its places (`path:line`)."""
    out = _run(
        cspell(),
        "lint",
        "--config",
        str(CSPELL_CONFIG),
        "--no-progress",
        "--no-summary",
        "--no-exit-code",
        "--gitignore",
        "**",
    )
    words: dict[str, list[str]] = {}
    for line in out.splitlines():
        match = UNKNOWN_WORD.match(line)
        if match:
            path, lineno, word = match.groups()
            words.setdefault(word, []).append(f"{path}:{lineno}")
    return words


def one_edit_fixes(words: list[str]) -> dict[str, str]:
    """cspell's best suggestion for each word, if it's one edit away."""
    out = _run(
        cspell(),
        "suggest",
        "--config",
        str(CSPELL_CONFIG),
        "--num-changes",
        "1",
        "--num-suggestions",
        "1",
        "--no-include-ties",
        *words,
    )
    fixes: dict[str, str] = {}
    word = None
    for line in out.splitlines():
        if not line.startswith(" ") and line.endswith(":"):
            word = line[:-1]
        elif line.startswith(" - ") and word is not None:
            fixes[word] = line[3:].split()[0]
    return fixes


def uses(word: str) -> int:
    """Lines outside .github that use the word, as a whole word with this case."""
    grep = ["git", "grep", "--count", "--word-regexp", "--fixed-strings", "-e", word]
    result = subprocess.run(
        [*grep, "--", ".", ":!.github"], cwd=ROOT, capture_output=True, text=True
    )
    return sum(int(line.rsplit(":", 1)[1]) for line in result.stdout.splitlines())


def likely_typos(words: dict[str, list[str]]) -> dict[str, str]:
    """The words that look like typos, with the spelling cspell suggests."""
    typos = {}
    for word, fix in one_edit_fixes(sorted(words)).items():
        if fix.casefold() != word.casefold() and uses(fix) > len(words[word]):
            typos[word] = fix
    return typos


def update_words() -> None:
    words = unknown_words()
    typos = likely_typos(words) if words else {}
    new = sorted(word for word in words if word not in typos)
    if new:
        # A stable sort keeps the list's order for words that differ only in case.
        known = _read(WORDS_FILE).split()
        merged = sorted(known + new, key=str.lower)
        _write(WORDS_FILE, "\n".join(merged) + "\n")
    print(f"Added {_count(len(new), 'word')} to {WORDS_FILE.relative_to(ROOT)}.")
    if typos:
        print(
            "These look like typos, so they weren't added. Fix them, or add them "
            "to the word list by hand:"
        )
        for word, fix in sorted(typos.items()):
            for place in words[word]:
                print(f'  {place}: "{word}" (did you mean "{fix}"?)')


def cmd_prep(args: argparse.Namespace) -> None:
    dev = current_version()
    if not dev.endswith("-dev"):
        raise ReleaseError(
            f"version.json has {dev}, not a -dev version. Has the release been "
            "prepared already?"
        )
    release = dev.removesuffix("-dev")
    parse_release(release)
    cspell()  # before changing anything

    build = [sys.executable, str(CHANGELOG_SCRIPT), "build", "--version", release]
    if args.date:
        build += ["--date", args.date]
    if subprocess.run(build, cwd=ROOT).returncode != 0:
        raise ReleaseError("changelog.py build failed; nothing else was changed.")
    if f"## [v{release}]" not in _read(CHANGELOG):
        print(
            f"warning: CHANGELOG.md has no v{release} section, because changelog.d/ "
            f"has no files. Add `## [v{release}] - <date>` below `## [Unreleased]` "
            "by hand."
        )

    set_version(release)
    update_words()
    print(
        f"Prepared v{release}. Review the diff, including the v{release} section "
        "of CHANGELOG.md, then open the release prep pull request."
    )


def cmd_words(args: argparse.Namespace) -> None:
    update_words()


def cmd_next(args: argparse.Namespace) -> None:
    released = current_version()
    if released.endswith("-dev"):
        raise ReleaseError(
            f"version.json has {released}. Run this after the release prep pull "
            "request has merged and the release is published."
        )
    major, minor, _ = parse_release(released)
    version = (
        args.version.removeprefix("v") if args.version else f"{major}.{minor + 1}.0"
    )
    if parse_release(version) <= parse_release(released):
        raise ReleaseError(f"{version} isn't later than {released}")

    baseline = [
        Field(COMPATIBILITY_WORKFLOW, BASELINE_REF),
        Field(CONTRIBUTING, BASELINE_DOC),
    ]
    for field in baseline:
        field.read()  # before changing anything

    set_version(f"{version}-dev")
    for field in baseline:
        field.write(released)
    print(
        f"The backwards compatibility check now compares with {released}. CI checks "
        "out that tag, so the release must be published first."
    )


def main() -> int:
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    commands = parser.add_subparsers(dest="command", required=True)

    prep = commands.add_parser("prep", help="prepare the release")
    prep.add_argument("--date", help="release date for CHANGELOG.md (default: today)")
    prep.set_defaults(func=cmd_prep)
    words = commands.add_parser("words", help="update the spellcheck word list")
    words.set_defaults(func=cmd_words)
    after = commands.add_parser("next", help="start the next version")
    after.add_argument(
        "version", nargs="?", help="the next version (default: next minor version)"
    )
    after.set_defaults(func=cmd_next)

    args = parser.parse_args()
    try:
        args.func(args)
    except ReleaseError as e:
        print(f"error: {e}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
