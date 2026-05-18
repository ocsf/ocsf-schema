#!/usr/bin/env python3
"""
Review OCSF schema descriptions in PRs for LLM comprehension quality.

Two-phase design for fork PR compatibility:

  prepare  — Runs in the pull_request workflow (no secrets needed).
             Reads the compiled schema, PR diff, and changed file list
             produced by earlier workflow steps, extracts only the
             relevant compiled objects/classes/dictionary attributes,
             and writes review_context.json.

  review   — Runs in the workflow_run workflow (has secrets).
             Reads review_context.json, sends it to Claude, and
             posts an advisory comment on the PR.
"""

import json
import os
import re
import subprocess
import sys
from pathlib import Path

COMMENT_MARKER = "<!-- ocsf-description-review -->"
DEFAULT_MODEL = "claude-sonnet-4-20250514"
MAX_CONTEXT_CHARS = 400_000

SYSTEM_PROMPT = """\
You are an expert reviewer for the Open Cybersecurity Schema Framework (OCSF).
Your job is to review schema description fields in PR changes for clarity,
precision, and LLM comprehension quality.

You will receive the COMPILED (fully resolved) schema output — not the raw source
files. This means all inheritance (`extends`) has been resolved, dictionary
definitions have been merged with object-level overrides, and types are fully
enriched. This is the final form that downstream consumers and LLMs will see.

The compiled schema contains:
- **objects** / **classes**: Fully resolved definitions. Each carries a
  `_changed_attributes` list naming the attributes added or modified in this
  PR — **only flag findings on those attributes**. The remaining attributes
  in the container are unchanged siblings, included as compact summaries
  (`type`, `caption`, truncated `description`, `has_enum`) so you can reason
  about the changed attribute in context.
- **dictionary_attributes**: Changed dictionary entries that carry a full,
  standalone description. Entries whose dictionary description ends with
  the `See specific usage.` marker are intentionally generic placeholders
  — the authoritative descriptions live on the per-class/per-object
  overrides in the compiled objects/classes above. Those placeholder
  entries are deliberately omitted from this section and **must not be
  flagged** (e.g., as `tautological-description`); review only the
  resolved descriptions in the compiled objects/classes for those
  attributes.
- **cross_reference_index**: Maps each changed attribute name to every other
  container (object/class) that uses the same name, with the type seen there.
  Only attributes appearing in 2+ containers are listed. Use it to detect
  cross-container type inconsistency and naming conflicts.
- **dictionary_neighbors**: For each changed dictionary attribute, lists
  closely related existing entries — `is_X`/`X` name pairs and entries with
  identical descriptions. Use it to detect duplicate or conflicting
  dictionary entries.

Deprecated attributes (those with an `@deprecated` marker) have been
pre-filtered from the compiled schema data. Do not flag or comment on
deprecated attributes — they are intentionally being phased out.

## Review Criteria

Evaluate ONLY the changed/added descriptions against these criteria:

### 1. Self-Contained Descriptions
Every attribute description must be understandable in isolation. Flag:
- Vague references like "an item", "a group", "the object" where a
  domain-specific term should be used
- Descriptions that cannot be understood without cross-referencing other schema
  elements

The `See specific usage.` marker on a **dictionary** entry is an
intentional placeholder that defers the meaningful description to the
per-class/per-object override; do not flag dictionary entries that use
this convention. Review the resolved object/class description instead.

### 2. Name/Description Semantic Consistency
Flag where the attribute name implies one thing but the description says another.
Example: a name containing "attacks_count" but a description that counts
"privileges" is confusing.

### 3. No Tautological Phrasing
Flag circular or redundant descriptions like
"The X object describes details about X."

### 4. Relationship Clarity
When a new attribute is semantically close to an existing one (e.g., singular
`attack` vs plural `attacks`), the description should note the distinction.

### 5. Plural/Array Attribute Completeness
Array attributes should describe what each element represents, not just
"A list of X."

### 6. CHANGELOG Conventions
Every CHANGELOG entry MUST:
- End with a PR reference link: `[#NNNN](https://github.com/ocsf/ocsf-schema/pull/NNNN)`
- Use `1.` numbering with 2-space indent under `####` subsections
- Be placed under the correct section (Added/Improved/Bugfixes/etc.) and
  subsection (Objects/Dictionary Attributes/etc.)

### 7. Machine Comprehension
Descriptions should be specific enough for an LLM to correctly populate the
field from raw security telemetry and distinguish it from similar attributes.

## Anti-Pattern Detection

In addition to description quality, flag structural design anti-patterns in
changed/added attributes. Use the cross-schema context to catch issues that
cannot be seen from the diff alone:

- **Sibling attributes on the same container** (everything in `attributes`
  outside `_changed_attributes`) → use to detect boolean proliferation,
  missing `_id` siblings, and semantic overlap with neighbors.
- **`cross_reference_index`** → use to detect type inconsistency where the
  same attribute name has different types across containers (`distinct_types`
  with more than one entry is an immediate signal).
- **`dictionary_neighbors`** → use to detect duplicate dictionary entries
  (`is_X`/`X` name pairs) and identical descriptions across distinct attrs.

### 8. Boolean Trap
Flag `boolean_t` attributes where the concept has more than two meaningful
states. Common signals:
- The description mentions conditional logic, multiple options, or "depending on"
- The boolean answers a meta-question ("is X known?") instead of directly
  encoding the value — prefer an `integer_t` enum with explicit states
- Example: `is_src_dst_assignment_known` (boolean) should be `initiator_id`
  (enum: Unknown, Source Endpoint, Destination Endpoint, Other)

### 9. Semantic Overlap
Flag attributes on the same object/class that appear to represent the same
or nearly identical concepts without clear differentiation. Each attribute
should have a distinct, non-overlapping purpose.

### 10. Incorrect Type Choice
Flag attributes where the chosen type doesn't match the described semantics:
- `string_t` used for values that have a fixed set of options (should be enum)
- `integer_t` without enum for categorical values
- `boolean_t` for multi-state concepts (see Boolean Trap above)

### 11. Indirect Attribution
Flag attributes that describe a meta-property about another value rather than
directly encoding the information. Prefer direct representation.
- Anti-pattern: `is_connection_type_known` (boolean meta-property)
- Better: `connection_type_id` (enum that directly encodes the type, with
  Unknown as a value)

### 12. Cross-Attribute Inconsistency
When the same attribute name appears on multiple objects in the compiled schema,
flag cases where the descriptions or types are inconsistent without clear reason.

## Output Format

Use this markdown structure:

### Suggestions
Numbered list. Each item:
- **Object/Class**: `name`
- **Attribute**: `attribute_name`
- **Issue**: concise problem statement
- **Current**: the current description (quoted)
- **Suggested**: your improved description (quoted)

### Anti-Pattern Findings
Numbered list. Each item:
- **Pattern**: name of the anti-pattern (e.g., Boolean Trap, Semantic Overlap)
- **Object/Class**: `name`
- **Attribute**: `attribute_name`
- **Issue**: what makes this an anti-pattern
- **Recommendation**: how to restructure it

If no anti-patterns are found, omit this section entirely.

### CHANGELOG Issues
List any convention violations.

### Summary
1-2 sentence overall assessment covering both descriptions and anti-patterns.

If no issues are found, respond with only:
> ✅ No description issues found — descriptions look clear for LLM consumption.

## Previous Review Awareness

You may receive a "Previous Review" section containing your earlier review of
this same PR. When present:
1. Check which of your previous suggestions have been addressed in the current
   code — acknowledge them briefly (e.g., "✅ Fixed: `attr_name` description
   improved")
2. Re-raise any suggestions that were NOT addressed — keep the same format
3. Note any NEW issues introduced since the last review
4. Keep the Summary section updated to reflect current state

These are advisory suggestions to help improve clarity. They are not required
changes. Only review CHANGED or ADDED content. Do not flag pre-existing
descriptions.
"""


# ---------------------------------------------------------------------------
# Helpers
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


# OCSF keys that look structural (`"foo": { ... }`) but are never the
# name of a reviewable attribute, so we never add them to `keys`.
_RESERVED_FILE_KEYS = frozenset({
    "attributes",
    "constraints",
    "profiles",
    "associations",
    "references",
    "types",
    "enum",
})

# Reserved wrappers whose direct children are *also* not attribute names
# (enum entries, constraint specs, profile names, etc.). When we enter one,
# nested keys are ignored and any modifications inside should be attributed
# to the enclosing attribute (i.e., the previously tracked `current_key`).
# `"attributes"` is reserved but not opaque — its direct children *are*
# attribute names.
_OPAQUE_WRAPPERS = frozenset({
    "enum",
    "constraints",
    "profiles",
    "associations",
    "references",
    "types",
})


def _extract_changed_attr_keys(diff: str, filename: str) -> set[str]:
    """Extract attribute names added or modified in a file's diff.

    Heuristic parser tuned for OCSF schema JSON files. It tracks brace
    depth and a stack of "opaque" wrappers (`enum`, `constraints`,
    `profiles`, etc.) so that:

    - Modifications nested inside an attribute's body (tweaking a
      `description`, adding `@deprecated`, etc.) attribute to the
      enclosing attribute name.
    - Modifications inside `enum` (e.g. adding/editing enum entries
      `"1": {...}`) attribute to the enclosing attribute, never to the
      enum entry IDs themselves.
    - `"attributes"`, `"constraints"`, `"profiles"`, etc. are never
      reported as changed attribute names.
    - Each diff hunk starts with a fresh state — cross-hunk brace depth
      is not reliable because untouched lines between hunks aren't in
      the diff.
    """
    in_file = False
    keys: set[str] = set()
    current_key: str | None = None
    brace_depth = 0
    opaque_depth: int | None = None  # depth at which we entered the current opaque wrapper

    for line in diff.split("\n"):
        if line.startswith("diff --git") and filename in line:
            in_file = True
            current_key = None
            brace_depth = 0
            opaque_depth = None
            continue
        if line.startswith("diff --git") and in_file:
            break
        if not in_file:
            continue
        if line.startswith("@@"):
            current_key = None
            brace_depth = 0
            opaque_depth = None
            continue
        if line.startswith("+++") or line.startswith("---"):
            continue

        content = line[1:] if line and line[0] in ("+", "-", " ") else line
        in_opaque = opaque_depth is not None

        key_match = re.search(r'"(\w+)":\s*[\{\[]', content)
        matched_key = key_match.group(1) if key_match else None

        if matched_key in _OPAQUE_WRAPPERS and not in_opaque:
            # Entering an opaque wrapper; preserve current_key so inner
            # additions are attributed to the enclosing attribute.
            opaque_depth = brace_depth
        elif matched_key == "attributes":
            # Entering the attributes wrapper itself; not an attribute.
            current_key = None
        elif matched_key and matched_key not in _RESERVED_FILE_KEYS and not in_opaque:
            current_key = matched_key

        if line.startswith("+"):
            if (
                matched_key
                and matched_key not in _RESERVED_FILE_KEYS
                and not in_opaque
            ):
                keys.add(matched_key)
            elif current_key:
                keys.add(current_key)
            # else: inside a file-level wrapper with no enclosing attr -> drop

        brace_depth += content.count("{") - content.count("}")

        if opaque_depth is not None and brace_depth <= opaque_depth:
            opaque_depth = None

    return keys


def extract_changed_dict_attrs(diff: str) -> set[str]:
    """Parse attribute names added/modified in dictionary.json from the diff."""
    return _extract_changed_attr_keys(diff, "dictionary.json")


def extract_changed_attrs_in_file(diff: str, filename: str) -> set[str]:
    """Extract attribute names that were added or modified in a file's diff."""
    return _extract_changed_attr_keys(diff, filename)


SIBLING_DESC_MAX = 200
CROSS_REF_MAX = 20


def _summarize_sibling_attr(attr_def: dict) -> dict:
    """Compact summary of an unchanged sibling attribute.

    Provides enough signal for the LLM to detect proliferation, missing
    siblings, and semantic overlap without inflating the prompt.
    """
    desc = attr_def.get("description", "") or ""
    if len(desc) > SIBLING_DESC_MAX:
        desc = desc[:SIBLING_DESC_MAX].rstrip() + "..."
    summary = {
        "type": attr_def.get("type", "?"),
        "caption": attr_def.get("caption", ""),
        "description": desc,
    }
    if attr_def.get("enum"):
        summary["has_enum"] = True
    if attr_def.get("sibling"):
        summary["sibling"] = attr_def["sibling"]
    return summary


def _build_container_context(
    compiled_def: dict,
    changed_attrs: set[str],
) -> dict:
    """Return a compiled object/class with full info on changed attrs and
    summarized info on their (non-deprecated) siblings.

    Adds a `_changed_attributes` field listing the attrs the LLM should
    actually flag findings on. Other attrs are present as context only.
    """
    result: dict = {"_changed_attributes": sorted(changed_attrs)}
    for key, value in compiled_def.items():
        if key != "attributes":
            result[key] = value
            continue
        attrs_out: dict = {}
        for attr_name, attr_def in value.items():
            if attr_def.get("@deprecated"):
                continue
            if attr_name in changed_attrs:
                attrs_out[attr_name] = attr_def
            else:
                attrs_out[attr_name] = _summarize_sibling_attr(attr_def)
        result["attributes"] = attrs_out
    return result


def _build_cross_reference_index(
    attr_names: set[str],
    compiled_objects: dict,
    compiled_classes: dict,
) -> dict:
    """Map each changed attribute name to other containers using that name.

    Skipped when the name appears in only one container — there's nothing
    to cross-check. Capped at CROSS_REF_MAX entries to avoid blowing up
    on common attrs like `name` or `type`.
    """
    index: dict[str, dict] = {}
    for attr_name in attr_names:
        refs: list[dict] = []
        for obj_name, obj_data in compiled_objects.items():
            attr = obj_data.get("attributes", {}).get(attr_name)
            if not attr or attr.get("@deprecated"):
                continue
            refs.append({
                "container": obj_name,
                "container_kind": "object",
                "type": attr.get("type", "?"),
            })
        for cls_name, cls_data in compiled_classes.items():
            attr = cls_data.get("attributes", {}).get(attr_name)
            if not attr or attr.get("@deprecated"):
                continue
            refs.append({
                "container": cls_name,
                "container_kind": "class",
                "type": attr.get("type", "?"),
            })

        if len(refs) < 2:
            continue

        truncated = False
        if len(refs) > CROSS_REF_MAX:
            refs = refs[:CROSS_REF_MAX]
            truncated = True

        types_seen = sorted({r["type"] for r in refs})
        index[attr_name] = {
            "containers": refs,
            "distinct_types": types_seen,
            "truncated": truncated,
        }
    return index


def _build_dictionary_neighbors(
    attr_name: str,
    attr_def: dict,
    compiled_dict: dict,
) -> list[dict]:
    """Return dictionary entries closely related to a changed dict attr.

    Surfaces:
    - Name pairs: `is_X` <-> `X` (likely-duplicate boolean/value pair)
    - Other dict entries with an identical description
    """
    neighbors: list[dict] = []
    desc = (attr_def.get("description", "") or "").strip()

    pair_name: str | None = None
    if attr_name.startswith("is_"):
        pair_name = attr_name[3:]
    else:
        pair_name = f"is_{attr_name}"

    if pair_name and pair_name in compiled_dict:
        pair_def = compiled_dict[pair_name]
        if not pair_def.get("@deprecated"):
            pair_desc = pair_def.get("description", "") or ""
            if len(pair_desc) > SIBLING_DESC_MAX:
                pair_desc = pair_desc[:SIBLING_DESC_MAX].rstrip() + "..."
            neighbors.append({
                "name": pair_name,
                "relation": "name_pair",
                "type": pair_def.get("type", "?"),
                "description": pair_desc,
            })

    if desc and len(desc) >= 30 and "See specific usage" not in desc:
        for other_name, other_def in compiled_dict.items():
            if other_name == attr_name or other_name == pair_name:
                continue
            if other_def.get("@deprecated"):
                continue
            other_desc = (other_def.get("description", "") or "").strip()
            if other_desc == desc:
                neighbors.append({
                    "name": other_name,
                    "relation": "identical_description",
                    "type": other_def.get("type", "?"),
                    "description": other_desc[:SIBLING_DESC_MAX],
                })

    return neighbors


# ---------------------------------------------------------------------------
# Phase 1: prepare
# ---------------------------------------------------------------------------

def cmd_prepare() -> None:
    """Read compiled schema + PR metadata files, extract context, save JSON."""
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

    schema_files = [
        f for f in changed_files if f.endswith(".json") or f == "CHANGELOG.md"
    ]
    if not schema_files:
        print("No schema files changed, writing empty context.")
        Path("review_context.json").write_text(json.dumps({"skip": True}))
        return

    context = {
        "objects": {},
        "classes": {},
        "dictionary_attributes": {},
        "cross_reference_index": {},
        "dictionary_neighbors": {},
    }

    compiled_objects = compiled.get("objects", {})
    compiled_classes = compiled.get("classes", {})
    compiled_dict_attrs = compiled.get("dictionary", {}).get("attributes", {})

    all_changed_attr_names: set[str] = set()
    changed_dict_attr_names: set[str] = set()

    for filepath in changed_files:
        if filepath.endswith(".json") and filepath.startswith("objects/"):
            name = Path(filepath).stem
            if name in compiled_objects:
                changed_attrs = extract_changed_attrs_in_file(diff, filepath)
                if changed_attrs:
                    context["objects"][name] = _build_container_context(
                        compiled_objects[name], changed_attrs
                    )
                    all_changed_attr_names |= changed_attrs

        elif filepath.endswith(".json") and filepath.startswith("events/"):
            name = Path(filepath).stem
            if name in compiled_classes:
                changed_attrs = extract_changed_attrs_in_file(diff, filepath)
                if changed_attrs:
                    context["classes"][name] = _build_container_context(
                        compiled_classes[name], changed_attrs
                    )
                    all_changed_attr_names |= changed_attrs

    if "dictionary.json" in changed_files:
        for attr_name in extract_changed_dict_attrs(diff):
            if attr_name not in compiled_dict_attrs:
                continue
            dict_entry = compiled_dict_attrs[attr_name]
            if dict_entry.get("@deprecated"):
                continue
            desc = dict_entry.get("description", "")

            if "See specific usage" in desc:
                # `See specific usage.` is an intentional placeholder
                # convention: the dictionary entry stays deliberately
                # generic and the meaningful description lives on each
                # per-class/per-object override. Do not surface the
                # placeholder text to the reviewer (it would trip the
                # tautological-description check); only surface the
                # resolved usages from compiled objects/classes.
                for obj_name, obj_data in compiled_objects.items():
                    if attr_name in obj_data.get("attributes", {}):
                        if obj_name not in context["objects"]:
                            context["objects"][obj_name] = _build_container_context(
                                obj_data, {attr_name}
                            )
                for cls_name, cls_data in compiled_classes.items():
                    if attr_name in cls_data.get("attributes", {}):
                        if cls_name not in context["classes"]:
                            context["classes"][cls_name] = _build_container_context(
                                cls_data, {attr_name}
                            )
            else:
                context["dictionary_attributes"][attr_name] = dict_entry

            changed_dict_attr_names.add(attr_name)
            all_changed_attr_names.add(attr_name)

    if all_changed_attr_names:
        context["cross_reference_index"] = _build_cross_reference_index(
            all_changed_attr_names, compiled_objects, compiled_classes
        )

    for attr_name in changed_dict_attr_names:
        attr_def = compiled_dict_attrs.get(attr_name)
        if not attr_def:
            continue
        neighbors = _build_dictionary_neighbors(
            attr_name, attr_def, compiled_dict_attrs
        )
        if neighbors:
            context["dictionary_neighbors"][attr_name] = neighbors

    output = {
        "pr_number": pr_number,
        "changed_files": changed_files,
        "compiled_context": context,
        "diff": diff,
    }

    Path("review_context.json").write_text(json.dumps(output))
    print(f"Saved review context ({len(json.dumps(output))} chars)")


# ---------------------------------------------------------------------------
# Phase 2: review
# ---------------------------------------------------------------------------

def build_review_prompt(
    data: dict,
    previous_review: str | None = None,
) -> str:
    """Build the prompt string from the saved review context."""
    ctx = data["compiled_context"]
    diff = data["diff"]
    changed_files = data["changed_files"]
    parts = []

    if previous_review:
        parts.append(
            "## Previous Review\n"
            "The following is your previous review of this PR. Check which "
            "suggestions have been addressed and which remain outstanding.\n\n"
            + previous_review
            + "\n\n---\n"
        )

    if ctx["objects"]:
        parts.append(
            "## Compiled Objects (fully resolved)\n```json\n"
            + json.dumps(ctx["objects"], indent=2)
            + "\n```\n"
        )

    if ctx["classes"]:
        parts.append(
            "## Compiled Event Classes (fully resolved)\n```json\n"
            + json.dumps(ctx["classes"], indent=2)
            + "\n```\n"
        )

    if ctx.get("dictionary_attributes"):
        parts.append(
            "## Dictionary Attributes (changed, non-placeholder descriptions)\n```json\n"
            + json.dumps(ctx["dictionary_attributes"], indent=2)
            + "\n```\n"
        )

    if ctx.get("cross_reference_index"):
        parts.append(
            "## Cross-Reference Index\n"
            "_Other containers in the schema that use each changed attribute "
            "name. Use this to detect type inconsistency and cross-container "
            "drift. Only names that appear in 2+ containers are listed._\n"
            "```json\n"
            + json.dumps(ctx["cross_reference_index"], indent=2)
            + "\n```\n"
        )

    if ctx.get("dictionary_neighbors"):
        parts.append(
            "## Dictionary Neighbors\n"
            "_Existing dictionary entries closely related to each changed "
            "dictionary attribute (`is_X`/`X` name pairs and entries with "
            "identical descriptions). Use this to detect duplicate or "
            "conflicting dictionary entries._\n"
            "```json\n"
            + json.dumps(ctx["dictionary_neighbors"], indent=2)
            + "\n```\n"
        )

    if "CHANGELOG.md" in changed_files:
        changelog_lines = []
        in_changelog = False
        for line in diff.split("\n"):
            if line.startswith("diff --git") and "CHANGELOG.md" in line:
                in_changelog = True
                continue
            if line.startswith("diff --git") and in_changelog:
                break
            if in_changelog:
                changelog_lines.append(line)
        if changelog_lines:
            parts.append(
                "## CHANGELOG.md diff\n```diff\n"
                + "\n".join(changelog_lines)
                + "\n```\n"
            )

    parts.append(
        "## Full PR diff (for reference)\n```diff\n" + diff + "\n```\n"
    )

    return _fit_within_budget(parts, diff)


def _fit_within_budget(parts: list[str], diff: str) -> str:
    """Shed low-signal sections progressively until the prompt fits.

    Order of preference (most to least valuable):
        1. Previous Review            — agent-state continuity
        2. Compiled Objects/Classes   — primary review subject
        3. Dictionary Attributes      — primary review subject
        4. Cross-Reference Index      — cross-container anti-pattern signal
        5. Dictionary Neighbors       — duplicate/conflict signal
        6. CHANGELOG.md diff          — convention checks
        7. Full PR diff               — verbose, mostly redundant with structured sections

    The full PR diff is shed first when over budget. We replace it with a
    head-and-tail diff stub (~50 KB) so the LLM still has line-level
    grounding for the most prominent changes. If still over budget, the
    CHANGELOG diff and finally the diff stub are dropped. As a last resort,
    the joined context is hard-truncated.
    """
    context = "\n".join(parts)
    if len(context) <= MAX_CONTEXT_CHARS:
        return context

    parts = [p for p in parts if not p.startswith("## Full PR diff")]
    diff_stub = (
        "## PR diff (truncated due to size — structured sections above carry "
        "the same information more compactly)\n```diff\n"
        + diff[:50_000]
        + "\n```\n"
    )
    parts.append(diff_stub)
    context = "\n".join(parts)
    if len(context) <= MAX_CONTEXT_CHARS:
        return context

    parts = [p for p in parts if not p.startswith("## CHANGELOG.md diff")]
    context = "\n".join(parts)
    if len(context) <= MAX_CONTEXT_CHARS:
        return context

    parts = [p for p in parts if not p.startswith("## PR diff (truncated")]
    context = "\n".join(parts)
    if len(context) <= MAX_CONTEXT_CHARS:
        return context

    return context[:MAX_CONTEXT_CHARS] + "\n\n[CONTEXT HARD-TRUNCATED]"


def find_existing_comment(pr_number: str) -> str | None:
    """Find an existing bot comment on the PR and return its ID."""
    repo = os.environ.get("GITHUB_REPOSITORY", "")
    jq_filter = f'.[] | select(.body | contains("{COMMENT_MARKER}")) | .id'
    try:
        output = run_gh(
            "api",
            f"repos/{repo}/issues/{pr_number}/comments",
            "--paginate",
            "--jq",
            jq_filter,
        )
        first_id = output.strip().split("\n")[0]
        return first_id if first_id else None
    except subprocess.CalledProcessError:
        return None


def fetch_previous_review(pr_number: str) -> str | None:
    """Fetch the body of the existing review comment, stripped of boilerplate."""
    repo = os.environ.get("GITHUB_REPOSITORY", "")
    jq_filter = f'.[] | select(.body | contains("{COMMENT_MARKER}")) | .body'
    try:
        output = run_gh(
            "api",
            f"repos/{repo}/issues/{pr_number}/comments",
            "--paginate",
            "--jq",
            jq_filter,
        )
        body = output.strip()
        if not body:
            return None
        # Strip the marker and preamble to get Claude's actual review text.
        for delimiter in ["_\n\n", "_\r\n\r\n"]:
            idx = body.find(delimiter)
            if idx != -1:
                return body[idx + len(delimiter):]
        return body
    except subprocess.CalledProcessError:
        return None


def post_or_update_comment(pr_number: str, body: str) -> None:
    """Post a new comment or update the existing one (idempotent)."""
    repo = os.environ.get("GITHUB_REPOSITORY", "")
    full_body = (
        f"{COMMENT_MARKER}\n"
        "## Schema Description Review\n\n"
        "_Automated suggestions for improving description clarity "
        "for LLM consumption. These are advisory — not required changes._\n\n"
        f"{body}"
    )
    payload = json.dumps({"body": full_body})

    existing_id = find_existing_comment(pr_number)

    if existing_id:
        run_gh(
            "api",
            f"repos/{repo}/issues/comments/{existing_id}",
            "-X", "PATCH", "--input", "-",
            input_data=payload,
        )
        print(f"Updated existing comment {existing_id}")
    else:
        run_gh(
            "api",
            f"repos/{repo}/issues/{pr_number}/comments",
            "-X", "POST", "--input", "-",
            input_data=payload,
        )
        print("Posted new comment")


def cmd_review() -> None:
    """Read review_context.json, call Claude, post PR comment."""
    context_path = Path("review_context.json")
    if not context_path.exists():
        print("review_context.json not found", file=sys.stderr)
        sys.exit(1)

    data = json.loads(context_path.read_text())

    if data.get("skip"):
        print("No schema files were changed, nothing to review.")
        return

    pr_number = data["pr_number"]
    ctx = data["compiled_context"]

    has_content = bool(
        ctx.get("objects")
        or ctx.get("classes")
        or ctx.get("dictionary_attributes")
    )
    has_changelog = "CHANGELOG.md" in data["changed_files"]

    if not has_content and not has_changelog:
        print("No reviewable content, skipping.")
        return

    import anthropic

    print("Checking for previous review comment...")
    previous_review = fetch_previous_review(pr_number)
    if previous_review:
        print(f"Found previous review ({len(previous_review)} chars)")
    else:
        print("No previous review found (first review)")

    prompt_context = build_review_prompt(
        data,
        previous_review=previous_review,
    )

    print("Calling Claude for review...")
    client = anthropic.Anthropic()
    model = os.environ.get("CLAUDE_MODEL", DEFAULT_MODEL)

    message = client.messages.create(
        model=model,
        max_tokens=4096,
        system=SYSTEM_PROMPT,
        messages=[
            {
                "role": "user",
                "content": (
                    "Review the following OCSF schema PR changes for "
                    "description quality, LLM comprehension, and structural "
                    "anti-patterns. The objects and classes below are "
                    "COMPILED output — fully resolved with inheritance, "
                    "dictionary merging, and type enrichment applied.\n\n"
                    + prompt_context
                ),
            }
        ],
    )
    review = message.content[0].text

    print("Posting review comment...")
    post_or_update_comment(pr_number, review)
    print("Done!")


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main() -> None:
    if len(sys.argv) < 2 or sys.argv[1] not in ("prepare", "review"):
        print("Usage: review_descriptions.py <prepare|review>", file=sys.stderr)
        sys.exit(1)

    if sys.argv[1] == "prepare":
        cmd_prepare()
    else:
        cmd_review()


if __name__ == "__main__":
    main()
