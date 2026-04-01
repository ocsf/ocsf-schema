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
- **objects**: Fully resolved object definitions with all inherited and
  dictionary-merged attributes — every description is the final version
  after all overrides have been applied
- **classes**: Fully resolved event class definitions
- **dictionary_attributes**: Changed dictionary entries — these include both
  entries with full descriptions and entries whose generic description precedes
  a "See specific usage" marker (the marker is stripped). When a dictionary
  attribute also appears in the compiled objects above, review both the generic
  dictionary description and the object-specific resolved descriptions

Deprecated attributes (those with an `@deprecated` marker) have been
pre-filtered from the compiled schema data. Do not flag or comment on
deprecated attributes — they are intentionally being phased out.

## Review Criteria

Evaluate ONLY the changed/added descriptions against these criteria:

### 1. Self-Contained Descriptions
Every attribute description must be understandable in isolation. Flag:
- "See specific usage." without enough surrounding context to convey meaning
- Vague references like "an item", "a group", "the object" where a
  domain-specific term should be used
- Descriptions that cannot be understood without cross-referencing other schema
  elements

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
changed/added attributes:

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

### Structured Anti-Pattern JSON

After the Anti-Pattern Findings section (if any), append a hidden HTML comment
block containing a JSON array of your findings. This enables automated
extraction and learning. Use this exact format:

```
<!-- antipattern-json
[
  {
    "rule": "semantic-overlap",
    "container": "object_or_class_name",
    "attribute": "attribute_name",
    "pattern": "match_type:match_value",
    "message": "concise description of the anti-pattern"
  }
]
-->
```

The `pattern` field describes the structural signature so it can be codified
as a static rule. Use one of these match types:
- `attr_name_pair:name1,name2` — two attribute names that overlap
- `attr_name_regex:regex` — attribute names matching a pattern (e.g., `is_\\w+_verified`)
- `desc_contains:phrase` — attributes whose description contains a phrase

If you found no anti-patterns, omit this block entirely.

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


def extract_changed_dict_attrs(diff: str) -> list[str]:
    """Parse attribute names added/modified in dictionary.json from the diff."""
    in_dict = False
    attrs = []
    for line in diff.split("\n"):
        if line.startswith("diff --git") and "dictionary.json" in line:
            in_dict = True
            continue
        if line.startswith("diff --git") and in_dict:
            break
        if not in_dict:
            continue
        if line.startswith("+") and not line.startswith("+++"):
            match = re.search(r'"(\w+)":\s*\{', line)
            if match:
                attrs.append(match.group(1))
    return attrs


def _strip_deprecated_attrs(definition: dict) -> dict:
    """Return a copy of an object/class definition with deprecated attributes removed."""
    if "attributes" not in definition:
        return definition
    filtered = {
        name: attr for name, attr in definition["attributes"].items()
        if not attr.get("@deprecated")
    }
    result = definition.copy()
    result["attributes"] = filtered
    return result


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

    context = {"objects": {}, "classes": {}, "dictionary_attributes": {}}

    compiled_objects = compiled.get("objects", {})
    compiled_classes = compiled.get("classes", {})
    compiled_dict_attrs = compiled.get("dictionary", {}).get("attributes", {})

    for filepath in changed_files:
        if filepath.endswith(".json") and filepath.startswith("objects/"):
            name = Path(filepath).stem
            if name in compiled_objects:
                context["objects"][name] = _strip_deprecated_attrs(
                    compiled_objects[name]
                )

        elif filepath.endswith(".json") and filepath.startswith("events/"):
            name = Path(filepath).stem
            if name in compiled_classes:
                context["classes"][name] = _strip_deprecated_attrs(
                    compiled_classes[name]
                )

    if "dictionary.json" in changed_files:
        for attr_name in extract_changed_dict_attrs(diff):
            if attr_name not in compiled_dict_attrs:
                continue
            dict_entry = compiled_dict_attrs[attr_name]
            if dict_entry.get("@deprecated"):
                continue
            desc = dict_entry.get("description", "")

            if "See specific usage" in desc:
                prefix = desc.split("See specific usage")[0].strip()
                if prefix:
                    trimmed = dict_entry.copy()
                    trimmed["description"] = prefix
                    context["dictionary_attributes"][attr_name] = trimmed

                for obj_name, obj_data in compiled_objects.items():
                    if attr_name in obj_data.get("attributes", {}):
                        if obj_name not in context["objects"]:
                            context["objects"][obj_name] = _strip_deprecated_attrs(
                                obj_data
                            )
            else:
                context["dictionary_attributes"][attr_name] = dict_entry

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
    static_findings: list[dict] | None = None,
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

    if static_findings:
        parts.append(
            "## Static Anti-Pattern Findings\n"
            "The following anti-patterns were detected by static analysis. "
            "Validate these findings and include confirmed ones in your "
            "Anti-Pattern Findings section. Also look for additional "
            "anti-patterns that static analysis cannot catch (semantic "
            "overlap, incorrect type choices, indirect attribution, etc.).\n"
            "```json\n"
            + json.dumps(static_findings, indent=2)
            + "\n```\n"
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

    context = "\n".join(parts)
    if len(context) > MAX_CONTEXT_CHARS:
        trimmed = parts[:3] if len(parts) > 3 else parts[:1]
        trimmed.append(
            "## PR diff (truncated due to size)\n```diff\n"
            + diff[:100_000]
            + "\n```\n"
        )
        context = "\n".join(trimmed)
    return context


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

    has_content = ctx["objects"] or ctx["classes"] or ctx.get("dictionary_attributes")
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

    # Load static anti-pattern findings if available
    static_findings = None
    ap_path = Path("antipattern_results.json")
    if ap_path.exists():
        ap_data = json.loads(ap_path.read_text())
        findings = ap_data.get("findings", [])
        if findings:
            static_findings = findings
            print(f"Loaded {len(findings)} static anti-pattern finding(s)")

    prompt_context = build_review_prompt(
        data,
        previous_review=previous_review,
        static_findings=static_findings,
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

    # Extract structured anti-pattern JSON from Claude's response
    llm_findings = extract_llm_antipattern_json(review)
    novel_findings = diff_findings(llm_findings, static_findings or [])

    if novel_findings:
        print(f"Found {len(novel_findings)} novel LLM-discovered anti-pattern(s)")
        # Log the JSON for easy copy-paste into learned_antipatterns.json
        learned_entries = []
        for f in novel_findings:
            learned_entries.append({
                "rule": f.get("rule", "unknown"),
                "match_type": f.get("pattern", "").split(":")[0] if ":" in f.get("pattern", "") else "manual",
                "match_value": f.get("pattern", "").split(":", 1)[1] if ":" in f.get("pattern", "") else f.get("pattern", ""),
                "message": f.get("message", ""),
                "severity": "warning",
                "discovered_in_pr": pr_number,
            })
        print("--- Learned patterns JSON (add to .github/config/learned_antipatterns.json) ---")
        print(json.dumps(learned_entries, indent=2))
        print("--- End learned patterns ---")

        # Append a labeled section to the review comment
        novel_section = (
            "\n\n---\n"
            "### LLM-Discovered Anti-Patterns\n"
            "_These anti-patterns were identified by LLM analysis and are "
            "not yet covered by static rules. Consider adding them to "
            "`.github/config/learned_antipatterns.json`._\n\n"
        )
        for i, f in enumerate(novel_findings, 1):
            novel_section += (
                f"{i}. **{f.get('rule', 'unknown')}** — "
                f"`{f.get('container', '?')}`.`{f.get('attribute', '?')}`\n"
                f"   {f.get('message', '')}\n"
                f"   > Pattern: `{f.get('pattern', 'N/A')}`\n\n"
            )
        review += novel_section
    else:
        print("No novel LLM anti-patterns beyond static findings")

    print("Posting review comment...")
    post_or_update_comment(pr_number, review)
    print("Done!")


def extract_llm_antipattern_json(review_text: str) -> list[dict]:
    """Extract structured anti-pattern findings from Claude's HTML comment block."""
    match = re.search(
        r"<!--\s*antipattern-json\s*\n(.*?)\n\s*-->",
        review_text,
        re.DOTALL,
    )
    if not match:
        return []
    try:
        findings = json.loads(match.group(1))
        if isinstance(findings, list):
            return findings
    except (json.JSONDecodeError, TypeError):
        print("Warning: Failed to parse antipattern-json block", file=sys.stderr)
    return []


def diff_findings(
    llm_findings: list[dict],
    static_findings: list[dict],
) -> list[dict]:
    """Return LLM findings that don't have a matching static finding."""
    static_keys = {
        (f.get("container", ""), f.get("attribute", ""))
        for f in static_findings
    }
    return [
        f for f in llm_findings
        if (f.get("container", ""), f.get("attribute", "")) not in static_keys
    ]


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
