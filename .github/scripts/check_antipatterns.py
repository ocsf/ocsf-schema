#!/usr/bin/env python3
"""
Static anti-pattern detection for OCSF schema PRs.

Analyzes the compiled schema and PR diff to flag structural design
anti-patterns in changed objects, event classes, and dictionary attributes.
Runs without an LLM — purely deterministic analysis.

Two-phase design (same as review_descriptions.py):

  prepare  — Runs in the pull_request workflow. Reads compiled schema
             and PR diff, detects anti-patterns in changed definitions,
             writes antipattern_results.json.

  format   — Reads antipattern_results.json and prints a markdown
             report suitable for posting as a PR comment.
"""

import json
import os
import re
import subprocess
import sys
from pathlib import Path


COMMENT_MARKER = "<!-- ocsf-antipattern-check -->"


# ---------------------------------------------------------------------------
# Anti-pattern detectors
#
# Each detector receives (attr_name, attr_def, container_name, container_def)
# and returns a list of Finding dicts (possibly empty).
# ---------------------------------------------------------------------------

def _is_deprecated(attr_def: dict) -> bool:
    """Return True if the attribute definition carries an @deprecated marker."""
    return bool(attr_def.get("@deprecated"))


class Finding:
    """A single anti-pattern finding."""

    def __init__(
        self,
        rule: str,
        severity: str,
        container: str,
        attribute: str,
        message: str,
        suggestion: str = "",
    ):
        self.rule = rule
        self.severity = severity  # "warning" or "info"
        self.container = container
        self.attribute = attribute
        self.message = message
        self.suggestion = suggestion

    def to_dict(self) -> dict:
        return {
            "rule": self.rule,
            "severity": self.severity,
            "container": self.container,
            "attribute": self.attribute,
            "message": self.message,
            "suggestion": self.suggestion,
        }


def check_boolean_trap(
    attr_name: str,
    attr_def: dict,
    container_name: str,
    all_attrs: dict,
) -> list[Finding]:
    """Flag boolean attributes that may be masking a multi-state concept.

    Heuristics:
    - boolean_t with a name like is_*_known / has_*_status — likely indirect
    - boolean_t whose description mentions 3+ distinct states or options
    """
    if attr_def.get("type") != "boolean_t":
        return []
    if _is_deprecated(attr_def):
        return []

    findings = []
    desc = attr_def.get("description", "").lower()

    # Indirect attribution: is_X_known pattern
    if re.match(r"^is_\w+_known$", attr_name):
        findings.append(Finding(
            rule="boolean-trap:indirect",
            severity="warning",
            container=container_name,
            attribute=attr_name,
            message=(
                f"`{attr_name}` uses the `is_*_known` pattern — a boolean "
                f"answering whether something is known rather than directly "
                f"encoding the value. This typically indicates the underlying "
                f"concept has more than two states."
            ),
            suggestion=(
                "Consider replacing with an `integer_t` enum attribute that "
                "directly encodes the states (including Unknown/Other)."
            ),
        ))

    # Description mentions multiple states/options
    state_indicators = [
        "in the case of", "one of:", "either", "depending on",
        "can be", "may be", "or if", "otherwise",
    ]
    hits = sum(1 for s in state_indicators if s in desc)
    if hits >= 2:
        findings.append(Finding(
            rule="boolean-trap:multi-state",
            severity="info",
            container=container_name,
            attribute=attr_name,
            message=(
                f"`{attr_name}` is `boolean_t` but its description suggests "
                f"multiple states or conditional logic, which may indicate "
                f"the concept is better represented as an enum."
            ),
            suggestion=(
                "Evaluate whether an `integer_t` enum with explicit values "
                "would capture the full range of states more accurately."
            ),
        ))

    return findings


def check_boolean_proliferation(
    container_name: str,
    all_attrs: dict,
    changed_attr_names: set[str],
) -> list[Finding]:
    """Flag objects with many is_* booleans that may be a single enum."""
    bool_attrs = [
        name for name, defn in all_attrs.items()
        if defn.get("type") == "boolean_t"
        and name.startswith("is_")
        and not _is_deprecated(defn)
    ]
    # Only flag if at least one of the booleans was changed in this PR
    if len(bool_attrs) < 3 or not (set(bool_attrs) & changed_attr_names):
        return []

    return [Finding(
        rule="boolean-proliferation",
        severity="info",
        container=container_name,
        attribute=", ".join(sorted(bool_attrs)),
        message=(
            f"`{container_name}` has {len(bool_attrs)} `is_*` boolean "
            f"attributes: {', '.join(f'`{b}`' for b in sorted(bool_attrs))}. "
            f"Multiple related booleans often indicate a concept better "
            f"modeled as a single enum."
        ),
        suggestion=(
            "Consider whether these booleans represent mutually exclusive "
            "or related states that could be a single `_id` enum attribute."
        ),
    )]


def check_missing_sibling(
    attr_name: str,
    attr_def: dict,
    container_name: str,
    all_attrs: dict,
) -> list[Finding]:
    """Flag _id enum attributes without a corresponding string sibling."""
    if not attr_name.endswith("_id"):
        return []
    if _is_deprecated(attr_def):
        return []
    if attr_def.get("type") != "integer_t":
        return []
    if not attr_def.get("enum"):
        return []

    sibling_name = attr_def.get("sibling", attr_name[:-3])
    if sibling_name in all_attrs:
        return []

    return [Finding(
        rule="missing-sibling",
        severity="warning",
        container=container_name,
        attribute=attr_name,
        message=(
            f"`{attr_name}` is an `integer_t` enum but has no corresponding "
            f"string sibling `{sibling_name}`. The OCSF convention is for "
            f"each `_id` enum to have a sibling attribute with the normalized "
            f"caption string."
        ),
        suggestion=f"Add a `{sibling_name}` string attribute as the sibling.",
    )]


def check_tautological_description(
    attr_name: str,
    attr_def: dict,
    container_name: str,
    all_attrs: dict,
) -> list[Finding]:
    """Flag descriptions that just restate the attribute name or caption."""
    if _is_deprecated(attr_def):
        return []
    desc = attr_def.get("description", "")
    caption = attr_def.get("caption", "")
    if not desc:
        return []

    clean_desc = re.sub(r"^the\s+", "", desc.lower().rstrip(".").strip())
    clean_caption = caption.lower().strip()
    clean_name = attr_name.replace("_", " ").lower()

    # "The initiator." or "The initiator. See specific usage."
    prefix = desc.split("See specific usage")[0].strip().rstrip(".")
    clean_prefix = re.sub(r"^the\s+", "", prefix.lower().strip())

    if clean_prefix and (clean_prefix == clean_name or clean_prefix == clean_caption):
        return [Finding(
            rule="tautological-description",
            severity="warning",
            container=container_name,
            attribute=attr_name,
            message=(
                f"`{attr_name}` description \"{desc}\" is essentially "
                f"restating the attribute name. Descriptions should provide "
                f"meaning beyond what the name already conveys."
            ),
            suggestion=(
                "Add context about what this attribute represents, when it "
                "applies, or how it should be populated."
            ),
        )]

    return []


def check_enum_without_description(
    attr_name: str,
    attr_def: dict,
    container_name: str,
    all_attrs: dict,
) -> list[Finding]:
    """Flag enum values that have a caption but no description."""
    if _is_deprecated(attr_def):
        return []
    enum = attr_def.get("enum")
    if not enum or not isinstance(enum, dict):
        return []

    # Skip Unknown (0) and Other (99) — these are standard and self-evident
    skip_ids = {"0", "99"}
    missing = [
        f"{eid} ({e.get('caption', '?')})"
        for eid, e in enum.items()
        if eid not in skip_ids
        and e.get("caption")
        and not e.get("description")
    ]

    if not missing:
        return []

    return [Finding(
        rule="enum-without-description",
        severity="info",
        container=container_name,
        attribute=attr_name,
        message=(
            f"`{attr_name}` has enum values without descriptions: "
            f"{', '.join(missing)}. Enum descriptions help consumers "
            f"understand when to use each value."
        ),
        suggestion="Add a `description` to each non-trivial enum value.",
    )]


def check_generic_naming(
    attr_name: str,
    attr_def: dict,
    container_name: str,
    all_attrs: dict,
) -> list[Finding]:
    """Flag attributes with overly generic names and thin descriptions."""
    if _is_deprecated(attr_def):
        return []
    generic_names = {"type", "name", "value", "data", "info", "details", "status"}
    if attr_name not in generic_names:
        return []

    desc = attr_def.get("description", "")
    # Short description on a generic name is a strong signal
    if len(desc) < 40:
        return [Finding(
            rule="generic-naming",
            severity="info",
            container=container_name,
            attribute=attr_name,
            message=(
                f"`{attr_name}` is a very generic attribute name with a "
                f"short description (\"{desc}\"). Generic names require "
                f"detailed descriptions to be useful."
            ),
            suggestion=(
                "Either use a more specific attribute name (e.g., "
                "`account_type` instead of `type`) or expand the description "
                "to fully explain the attribute's purpose and expected values."
            ),
        )]

    return []


def check_duplicate_attribute(
    attr_name: str,
    attr_def: dict,
    container_name: str,
    all_dict_attrs: dict,
) -> list[Finding]:
    """Flag is_X / X pairs in the dictionary with the same type and meaning."""
    if not attr_name.startswith("is_"):
        return []
    if _is_deprecated(attr_def):
        return []

    bare_name = attr_name[3:]
    if bare_name not in all_dict_attrs:
        return []

    bare_def = all_dict_attrs[bare_name]
    if _is_deprecated(bare_def):
        return []
    if bare_def.get("type") != attr_def.get("type"):
        return []

    # Same type — very likely a duplicate
    bare_desc = bare_def.get("description", "")
    our_desc = attr_def.get("description", "")

    return [Finding(
        rule="duplicate-attribute",
        severity="warning",
        container=container_name,
        attribute=attr_name,
        message=(
            f"`{attr_name}` and `{bare_name}` are both `{attr_def.get('type')}` "
            f"in the dictionary. Having two attributes for the same concept "
            f"with and without the `is_` prefix causes ambiguity.\n"
            f"   - `{attr_name}`: \"{our_desc[:80]}\"\n"
            f"   - `{bare_name}`: \"{bare_desc[:80]}\""
        ),
        suggestion=(
            f"Deprecate one and keep the other. The OCSF convention for "
            f"booleans uses the `is_` prefix, so `{attr_name}` is preferred "
            f"and `{bare_name}` should be deprecated."
        ),
    )]


def check_duplicate_description(
    attr_name: str,
    attr_def: dict,
    container_name: str,
    all_dict_attrs: dict,
) -> list[Finding]:
    """Flag dictionary attributes with identical descriptions to another attr."""
    if _is_deprecated(attr_def):
        return []
    desc = attr_def.get("description", "").strip()
    if not desc or len(desc) < 30 or "See specific usage" in desc:
        return []

    # Skip known intentional pairs: timestamp_t/datetime_t
    if attr_name.endswith("_dt"):
        return []
    base_dt = attr_name + "_dt"
    if base_dt in all_dict_attrs:
        return []

    # Skip sibling pairs (_id and its string counterpart)
    if attr_name.endswith("_id"):
        return []
    if attr_name + "_id" in all_dict_attrs:
        return []

    for other_name, other_def in all_dict_attrs.items():
        if other_name == attr_name:
            continue
        if other_name.endswith("_dt") or other_name.endswith("_id"):
            continue
        if _is_deprecated(other_def):
            continue
        other_desc = other_def.get("description", "").strip()
        if desc == other_desc:
            # Only report once — report the one that sorts second
            if attr_name < other_name:
                return []
            return [Finding(
                rule="duplicate-description",
                severity="warning",
                container=container_name,
                attribute=attr_name,
                message=(
                    f"`{attr_name}` has an identical description to "
                    f"`{other_name}`: \"{desc[:100]}\". Different attributes "
                    f"should have distinct descriptions that clarify their "
                    f"unique purpose."
                ),
                suggestion=(
                    "Differentiate the descriptions, or if they truly "
                    "represent the same concept, deprecate one."
                ),
            )]

    return []


def check_type_inconsistency(
    attr_name: str,
    attr_def: dict,
    container_name: str,
    all_compiled_objects: dict,
) -> list[Finding]:
    """Flag attributes with different types across objects."""
    if _is_deprecated(attr_def):
        return []
    types_seen: dict[str, list[str]] = {}
    for obj_name, obj_data in all_compiled_objects.items():
        obj_attr = obj_data.get("attributes", {}).get(attr_name)
        if obj_attr and not _is_deprecated(obj_attr):
            t = obj_attr.get("type", "?")
            types_seen.setdefault(t, []).append(obj_name)

    if len(types_seen) <= 1:
        return []

    type_summary = ", ".join(
        f"`{t}` ({len(objs)} object{'s' if len(objs) > 1 else ''})"
        for t, objs in sorted(types_seen.items())
    )

    return [Finding(
        rule="type-inconsistency",
        severity="warning",
        container=container_name,
        attribute=attr_name,
        message=(
            f"`{attr_name}` has different types across objects: "
            f"{type_summary}. Inconsistent types for the same attribute "
            f"name make the schema harder to consume programmatically."
        ),
        suggestion=(
            "Use distinct attribute names for different types, or "
            "standardize on a single type across all objects."
        ),
    )]


def load_learned_patterns() -> list[dict]:
    """Load learned anti-pattern rules from the config file."""
    config_path = Path(__file__).parent.parent / "config" / "learned_antipatterns.json"
    if not config_path.exists():
        return []
    try:
        data = json.loads(config_path.read_text())
        return data.get("patterns", [])
    except (json.JSONDecodeError, KeyError):
        print(f"Warning: Failed to parse {config_path}", file=sys.stderr)
        return []


def check_learned_patterns(
    attr_name: str,
    attr_def: dict,
    container_name: str,
    all_attrs: dict,
    learned: list[dict],
) -> list[Finding]:
    """Check an attribute against learned anti-pattern rules."""
    if _is_deprecated(attr_def):
        return []
    findings = []
    desc = attr_def.get("description", "")

    for pattern in learned:
        match_type = pattern.get("match_type", "")
        match_value = pattern.get("match_value", "")
        rule = f"learned:{pattern.get('rule', 'unknown')}"
        message = pattern.get("message", "Learned anti-pattern match")
        severity = pattern.get("severity", "warning")

        if match_type == "attr_name_pair":
            pair = match_value if isinstance(match_value, list) else str(match_value).split(",")
            if len(pair) == 2 and attr_name in pair:
                other = pair[0] if pair[1] == attr_name else pair[1]
                if other in all_attrs:
                    findings.append(Finding(
                        rule=rule,
                        severity=severity,
                        container=container_name,
                        attribute=attr_name,
                        message=message,
                    ))

        elif match_type == "attr_name_regex":
            try:
                if re.fullmatch(match_value, attr_name):
                    findings.append(Finding(
                        rule=rule,
                        severity=severity,
                        container=container_name,
                        attribute=attr_name,
                        message=message,
                    ))
            except re.error:
                pass

        elif match_type == "desc_contains":
            if isinstance(match_value, str) and match_value.lower() in desc.lower():
                findings.append(Finding(
                    rule=rule,
                    severity=severity,
                    container=container_name,
                    attribute=attr_name,
                    message=message,
                ))

    return findings


def check_id_without_enum(
    attr_name: str,
    attr_def: dict,
    container_name: str,
    all_attrs: dict,
) -> list[Finding]:
    """Flag integer_t _id attributes that have no enum values defined."""
    if not attr_name.endswith("_id"):
        return []
    if _is_deprecated(attr_def):
        return []
    if attr_def.get("type") != "integer_t":
        return []
    if attr_def.get("enum"):
        return []
    # Skip if the attribute has "See specific usage" — enum may be at class level
    desc = attr_def.get("description", "")
    if "See specific usage" in desc:
        return []

    return [Finding(
        rule="id-without-enum",
        severity="info",
        container=container_name,
        attribute=attr_name,
        message=(
            f"`{attr_name}` is `integer_t` with an `_id` suffix but has no "
            f"enum values defined. The `_id` naming convention implies "
            f"normalized categorical values, which should be enumerated."
        ),
        suggestion=(
            "Define enum values for this attribute, or rename it if it "
            "represents an arbitrary integer rather than a category."
        ),
    )]


# ---------------------------------------------------------------------------
# Diff parsing
# ---------------------------------------------------------------------------

def extract_changed_names(diff: str, path_prefix: str) -> set[str]:
    """Extract stem names of changed files under a path prefix from the diff."""
    names = set()
    for line in diff.split("\n"):
        if line.startswith("diff --git"):
            match = re.search(rf"b/({re.escape(path_prefix)}[\w/]+\.json)", line)
            if match:
                names.add(Path(match.group(1)).stem)
    return names


def extract_changed_dict_attrs(diff: str) -> set[str]:
    """Parse attribute names added/modified in dictionary.json from the diff."""
    return _extract_changed_keys_in_file(diff, "dictionary.json")


def _extract_changed_keys_in_file(diff: str, filename: str) -> set[str]:
    """Extract JSON key names that were added or modified in a file's diff.

    Tracks the current top-level attribute key context so that
    modifications inside an attribute's block (e.g. adding @deprecated)
    correctly attribute the change to the enclosing key.
    """
    in_file = False
    keys = set()
    current_key = None
    brace_depth = 0

    for line in diff.split("\n"):
        if line.startswith("diff --git") and filename in line:
            in_file = True
            current_key = None
            brace_depth = 0
            continue
        if line.startswith("diff --git") and in_file:
            break
        if not in_file:
            continue

        # Strip the diff prefix (+, -, space) for structural analysis
        content = line[1:] if line and line[0] in ("+", "-", " ") else line
        if line.startswith("@@") or line.startswith("+++") or line.startswith("---"):
            continue

        # Track top-level key names (attribute names in the "attributes" block)
        key_match = re.search(r'"(\w+)":\s*[\{\[]', content)
        if key_match:
            if brace_depth <= 1:
                current_key = key_match.group(1)

        # Added line — mark the current key as changed
        if line.startswith("+"):
            # Direct key addition
            if key_match:
                keys.add(key_match.group(1))
            # Modification inside a key's block
            if current_key:
                keys.add(current_key)

        # Track brace depth for context
        brace_depth += content.count("{") - content.count("}")

    return keys


def extract_changed_attrs_for_file(diff: str, filepath: str) -> set[str]:
    """Extract attribute names changed in a specific object/class JSON file."""
    return _extract_changed_keys_in_file(diff, filepath)


# ---------------------------------------------------------------------------
# Phase 1: prepare
# ---------------------------------------------------------------------------

def cmd_prepare() -> None:
    """Analyze compiled schema for anti-patterns in changed definitions."""
    compiled_path = Path("compiled_schema.json")
    diff_path = Path("pr_diff.txt")
    changed_path = Path("changed_files.txt")
    pr_number_path = Path("pr_number.txt")

    for p in (compiled_path, diff_path, changed_path, pr_number_path):
        if not p.exists():
            print(f"Missing required file: {p}", file=sys.stderr)
            sys.exit(1)

    compiled = json.loads(compiled_path.read_text())
    diff = diff_path.read_text()
    changed_files = [
        f.strip() for f in changed_path.read_text().strip().split("\n") if f.strip()
    ]
    pr_number = pr_number_path.read_text().strip()

    schema_files = [f for f in changed_files if f.endswith(".json")]
    if not schema_files:
        print("No schema files changed.")
        Path("antipattern_results.json").write_text(
            json.dumps({"skip": True})
        )
        return

    compiled_objects = compiled.get("objects", {})
    compiled_classes = compiled.get("classes", {})

    changed_obj_names = extract_changed_names(diff, "objects/")
    changed_class_names = extract_changed_names(diff, "events/")
    changed_dict_attrs = extract_changed_dict_attrs(diff)

    all_changed_attrs = changed_dict_attrs.copy()

    compiled_dict = compiled.get("dictionary", {}).get("attributes", {})

    # Load learned patterns from config
    learned = load_learned_patterns()
    if learned:
        print(f"Loaded {len(learned)} learned anti-pattern rule(s)")

    # Per-attribute detectors (receive: attr_name, attr_def, container, all_attrs)
    attr_detectors = [
        check_boolean_trap,
        check_missing_sibling,
        check_tautological_description,
        check_enum_without_description,
        check_generic_naming,
        check_id_without_enum,
    ]

    findings: list[dict] = []

    # Check changed objects — only attributes modified in the PR
    for obj_name in changed_obj_names:
        obj = compiled_objects.get(obj_name)
        if not obj:
            continue
        attrs = obj.get("attributes", {})
        for filepath in changed_files:
            if filepath.startswith("objects/") and Path(filepath).stem == obj_name:
                file_changed_attrs = extract_changed_attrs_for_file(diff, filepath)
                break
        else:
            file_changed_attrs = set()
        scope = file_changed_attrs | changed_dict_attrs
        for attr_name, attr_def in attrs.items():
            if attr_name not in scope:
                continue
            for detector in attr_detectors:
                for f in detector(attr_name, attr_def, obj_name, attrs):
                    findings.append(f.to_dict())
            # Cross-object type inconsistency
            for f in check_type_inconsistency(
                attr_name, attr_def, obj_name, compiled_objects
            ):
                findings.append(f.to_dict())
            # Learned pattern checks
            if learned:
                for f in check_learned_patterns(
                    attr_name, attr_def, obj_name, attrs, learned
                ):
                    findings.append(f.to_dict())
        # Container-level checks
        for f in check_boolean_proliferation(
            obj_name, attrs, all_changed_attrs
        ):
            findings.append(f.to_dict())

    # Check changed event classes — only attributes modified in the PR
    for class_name in changed_class_names:
        cls = compiled_classes.get(class_name)
        if not cls:
            continue
        attrs = cls.get("attributes", {})
        for filepath in changed_files:
            if filepath.startswith("events/") and Path(filepath).stem == class_name:
                file_changed_attrs = extract_changed_attrs_for_file(diff, filepath)
                break
        else:
            file_changed_attrs = set()
        scope = file_changed_attrs | changed_dict_attrs
        for attr_name, attr_def in attrs.items():
            if attr_name not in scope:
                continue
            for detector in attr_detectors:
                for f in detector(attr_name, attr_def, class_name, attrs):
                    findings.append(f.to_dict())
            # Learned pattern checks
            if learned:
                for f in check_learned_patterns(
                    attr_name, attr_def, class_name, attrs, learned
                ):
                    findings.append(f.to_dict())
        for f in check_boolean_proliferation(
            class_name, attrs, all_changed_attrs
        ):
            findings.append(f.to_dict())

    # Check changed dictionary attributes directly
    for attr_name in changed_dict_attrs:
        attr_def = compiled_dict.get(attr_name)
        if not attr_def:
            continue
        for detector in attr_detectors:
            for f in detector(attr_name, attr_def, "dictionary", {}):
                findings.append(f.to_dict())
        # Dictionary-level cross-checks
        for f in check_duplicate_attribute(
            attr_name, attr_def, "dictionary", compiled_dict
        ):
            findings.append(f.to_dict())
        for f in check_duplicate_description(
            attr_name, attr_def, "dictionary", compiled_dict
        ):
            findings.append(f.to_dict())
        # Learned pattern checks
        if learned:
            for f in check_learned_patterns(
                attr_name, attr_def, "dictionary", compiled_dict, learned
            ):
                findings.append(f.to_dict())

    # Deduplicate (same rule + container + attribute)
    seen = set()
    unique: list[dict] = []
    for f in findings:
        key = (f["rule"], f["container"], f["attribute"])
        if key not in seen:
            seen.add(key)
            unique.append(f)

    output = {
        "pr_number": pr_number,
        "findings": unique,
    }

    Path("antipattern_results.json").write_text(json.dumps(output, indent=2))
    print(
        f"Anti-pattern check complete: {len(unique)} finding(s) "
        f"across {len(changed_obj_names)} objects, "
        f"{len(changed_class_names)} classes, "
        f"{len(changed_dict_attrs)} dictionary attributes"
    )


# ---------------------------------------------------------------------------
# Phase 2: format
# ---------------------------------------------------------------------------

def cmd_format() -> None:
    """Read results and print a markdown report."""
    results_path = Path("antipattern_results.json")
    if not results_path.exists():
        print("antipattern_results.json not found", file=sys.stderr)
        sys.exit(1)

    data = json.loads(results_path.read_text())

    if data.get("skip"):
        print("No schema files changed, nothing to check.")
        return

    findings = data.get("findings", [])
    if not findings:
        print("No anti-patterns detected.")
        return

    warnings = [f for f in findings if f["severity"] == "warning"]
    infos = [f for f in findings if f["severity"] == "info"]

    lines = []

    if warnings:
        lines.append("### Warnings\n")
        for i, f in enumerate(warnings, 1):
            lines.append(
                f"{i}. **{f['rule']}** — `{f['container']}`.`{f['attribute']}`\n"
                f"   {f['message']}\n"
            )
            if f.get("suggestion"):
                lines.append(f"   > **Suggestion**: {f['suggestion']}\n")
            lines.append("")

    if infos:
        lines.append("### Informational\n")
        for i, f in enumerate(infos, 1):
            lines.append(
                f"{i}. **{f['rule']}** — `{f['container']}`.`{f['attribute']}`\n"
                f"   {f['message']}\n"
            )
            if f.get("suggestion"):
                lines.append(f"   > **Suggestion**: {f['suggestion']}\n")
            lines.append("")

    lines.append(
        f"**Summary**: {len(warnings)} warning(s), {len(infos)} informational finding(s)"
    )

    print("\n".join(lines))


# ---------------------------------------------------------------------------
# Phase 3: post (runs in workflow_run context with secrets)
# ---------------------------------------------------------------------------

def run_gh(*args: str, input_data: str | None = None) -> str:
    result = subprocess.run(
        ["gh", *args],
        capture_output=True,
        text=True,
        input=input_data,
    )
    if result.returncode != 0:
        print(
            f"gh failed: gh {' '.join(args)}\nstderr: {result.stderr}",
            file=sys.stderr,
        )
        raise subprocess.CalledProcessError(result.returncode, "gh")
    return result.stdout


def cmd_post() -> None:
    """Read results, format markdown, and post/update a PR comment."""
    results_path = Path("antipattern_results.json")
    if not results_path.exists():
        print("antipattern_results.json not found", file=sys.stderr)
        sys.exit(1)

    data = json.loads(results_path.read_text())

    if data.get("skip"):
        print("No schema files changed, nothing to post.")
        return

    findings = data.get("findings", [])
    pr_number = data["pr_number"]
    repo = os.environ.get("GITHUB_REPOSITORY", "")

    if not findings:
        print("No anti-patterns detected, nothing to post.")
        return

    warnings = [f for f in findings if f["severity"] == "warning"]
    infos = [f for f in findings if f["severity"] == "info"]

    lines = []

    if warnings:
        lines.append("### Warnings\n")
        for i, f in enumerate(warnings, 1):
            lines.append(
                f"{i}. **{f['rule']}** — `{f['container']}`.`{f['attribute']}`\n"
                f"   {f['message']}\n"
            )
            if f.get("suggestion"):
                lines.append(f"   > **Suggestion**: {f['suggestion']}\n")
            lines.append("")

    if infos:
        lines.append("### Informational\n")
        for i, f in enumerate(infos, 1):
            lines.append(
                f"{i}. **{f['rule']}** — `{f['container']}`.`{f['attribute']}`\n"
                f"   {f['message']}\n"
            )
            if f.get("suggestion"):
                lines.append(f"   > **Suggestion**: {f['suggestion']}\n")
            lines.append("")

    lines.append(
        f"**Summary**: {len(warnings)} warning(s), "
        f"{len(infos)} informational finding(s)"
    )

    body = (
        f"{COMMENT_MARKER}\n"
        "## Schema Anti-Pattern Check\n\n"
        "_Automated structural analysis for common schema design "
        "anti-patterns. These are advisory — not required changes._\n\n"
        + "\n".join(lines)
    )

    # Find existing comment
    jq_filter = f'.[] | select(.body | contains("{COMMENT_MARKER}")) | .id'
    try:
        output = run_gh(
            "api",
            f"repos/{repo}/issues/{pr_number}/comments",
            "--paginate",
            "--jq",
            jq_filter,
        )
        existing_id = output.strip().split("\n")[0] if output.strip() else None
    except subprocess.CalledProcessError:
        existing_id = None

    payload = json.dumps({"body": body})

    if existing_id:
        run_gh(
            "api",
            f"repos/{repo}/issues/comments/{existing_id}",
            "-X", "PATCH", "--input", "-",
            input_data=payload,
        )
        print(f"Updated existing anti-pattern comment {existing_id}")
    else:
        run_gh(
            "api",
            f"repos/{repo}/issues/{pr_number}/comments",
            "-X", "POST", "--input", "-",
            input_data=payload,
        )
        print("Posted new anti-pattern comment")


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main() -> None:
    if len(sys.argv) < 2 or sys.argv[1] not in ("prepare", "format", "post"):
        print(
            "Usage: check_antipatterns.py <prepare|format|post>",
            file=sys.stderr,
        )
        sys.exit(1)

    if sys.argv[1] == "prepare":
        cmd_prepare()
    elif sys.argv[1] == "format":
        cmd_format()
    else:
        cmd_post()


if __name__ == "__main__":
    main()
