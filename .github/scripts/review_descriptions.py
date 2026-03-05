#!/usr/bin/env python3
"""
Review OCSF schema descriptions in PRs for LLM comprehension quality.

Compiles the schema using ocsf-schema-compiler to produce the final resolved
output, then sends the compiled objects/classes that changed in the PR to Claude
for description quality review. Posts findings as a PR comment.
"""

import json
import os
import re
import subprocess
import sys
from pathlib import Path

import anthropic

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
  dictionary-merged attributes
- **classes**: Fully resolved event class definitions
- **dictionary**: The enriched dictionary with type information

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

## Output Format

Use this markdown structure:

### Critical Issues
Numbered list. Each item:
- **Object/Class**: `name`
- **Attribute**: `attribute_name`
- **Issue**: concise problem statement
- **Current**: the current description (quoted)
- **Suggested**: your improved description (quoted)

### Warnings
Same format, for non-critical improvements.

### CHANGELOG Issues
List any convention violations.

### Summary
1-2 sentence overall assessment.

If no issues are found, respond with only:
> No description quality issues found in this PR.

Only review CHANGED or ADDED content. Do not flag pre-existing descriptions.
"""


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


def compile_schema() -> dict:
    """Compile the OCSF schema and return the fully resolved output."""
    print("Compiling schema...")
    result = subprocess.run(
        ["ocsf-schema-compiler", "."],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        print(f"Compiler stderr:\n{result.stderr}", file=sys.stderr)
        raise RuntimeError(
            f"ocsf-schema-compiler failed with exit code {result.returncode}"
        )
    if result.stderr:
        print(f"Compiler logs:\n{result.stderr}", file=sys.stderr)
    return json.loads(result.stdout)


def get_pr_diff(pr_number: str) -> str:
    return run_gh("pr", "diff", pr_number)


def get_changed_files(pr_number: str) -> list[str]:
    output = run_gh("pr", "diff", pr_number, "--name-only")
    return [f.strip() for f in output.strip().split("\n") if f.strip()]


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


def extract_compiled_context(
    compiled: dict, changed_files: list[str], diff: str
) -> dict:
    """Extract the compiled representations of items changed in the PR."""
    context = {"objects": {}, "classes": {}, "dictionary_attributes": {}}

    compiled_objects = compiled.get("objects", {})
    compiled_classes = compiled.get("classes", {})
    compiled_dict = compiled.get("dictionary", {})
    compiled_dict_attrs = compiled_dict.get("attributes", {})

    for filepath in changed_files:
        if filepath.endswith(".json") and filepath.startswith("objects/"):
            name = Path(filepath).stem
            if name in compiled_objects:
                context["objects"][name] = compiled_objects[name]

        elif filepath.endswith(".json") and filepath.startswith("events/"):
            name = Path(filepath).stem
            if name in compiled_classes:
                context["classes"][name] = compiled_classes[name]

    if "dictionary.json" in changed_files:
        changed_attrs = extract_changed_dict_attrs(diff)
        for attr_name in changed_attrs:
            if attr_name in compiled_dict_attrs:
                context["dictionary_attributes"][attr_name] = compiled_dict_attrs[
                    attr_name
                ]

    return context


def build_review_context(
    compiled_context: dict, changed_files: list[str], diff: str
) -> str:
    """Build the context string to send to Claude."""
    parts = []

    if compiled_context["objects"]:
        parts.append(
            "## Compiled Objects (fully resolved)\n```json\n"
            + json.dumps(compiled_context["objects"], indent=2)
            + "\n```\n"
        )

    if compiled_context["classes"]:
        parts.append(
            "## Compiled Event Classes (fully resolved)\n```json\n"
            + json.dumps(compiled_context["classes"], indent=2)
            + "\n```\n"
        )

    if compiled_context["dictionary_attributes"]:
        parts.append(
            "## Compiled Dictionary Attributes (changed)\n```json\n"
            + json.dumps(compiled_context["dictionary_attributes"], indent=2)
            + "\n```\n"
        )

    changelog_in_diff = "CHANGELOG.md" in changed_files
    if changelog_in_diff:
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
        trimmed_parts = []
        if compiled_context["objects"]:
            trimmed_parts.append(parts[0])
        if compiled_context["classes"]:
            trimmed_parts.append(
                parts[1] if compiled_context["objects"] else parts[0]
            )
        trimmed_parts.append(
            "## PR diff (full context omitted due to size)\n```diff\n"
            + diff[:100_000]
            + "\n```\n"
        )
        context = "\n".join(trimmed_parts)
    return context


def call_claude(context: str) -> str:
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
                    "description quality and LLM comprehension. The objects "
                    "and classes below are COMPILED output — fully resolved "
                    "with inheritance, dictionary merging, and type "
                    "enrichment applied.\n\n" + context
                ),
            }
        ],
    )
    return message.content[0].text


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


def post_or_update_comment(pr_number: str, body: str) -> None:
    """Post a new review comment or update the existing one (idempotent)."""
    repo = os.environ.get("GITHUB_REPOSITORY", "")
    full_body = f"{COMMENT_MARKER}\n## Schema Description Review\n\n{body}"
    payload = json.dumps({"body": full_body})

    existing_id = find_existing_comment(pr_number)

    if existing_id:
        run_gh(
            "api",
            f"repos/{repo}/issues/comments/{existing_id}",
            "-X",
            "PATCH",
            "--input",
            "-",
            input_data=payload,
        )
        print(f"Updated existing comment {existing_id}")
    else:
        run_gh(
            "api",
            f"repos/{repo}/issues/{pr_number}/comments",
            "-X",
            "POST",
            "--input",
            "-",
            input_data=payload,
        )
        print("Posted new comment")


def main() -> None:
    pr_number = os.environ.get("PR_NUMBER")
    if not pr_number:
        print("PR_NUMBER environment variable is required", file=sys.stderr)
        sys.exit(1)

    print(f"Reviewing PR #{pr_number}...")

    changed_files = get_changed_files(pr_number)
    schema_files = [
        f for f in changed_files if f.endswith(".json") or f == "CHANGELOG.md"
    ]

    if not schema_files:
        print("No schema files changed, skipping review.")
        return

    print(f"Schema files changed: {schema_files}")

    compiled = compile_schema()

    diff = get_pr_diff(pr_number)
    compiled_context = extract_compiled_context(compiled, changed_files, diff)

    has_compiled_items = (
        compiled_context["objects"]
        or compiled_context["classes"]
        or compiled_context["dictionary_attributes"]
    )
    has_changelog = "CHANGELOG.md" in changed_files

    if not has_compiled_items and not has_changelog:
        print("No reviewable schema content found, skipping.")
        return

    context = build_review_context(compiled_context, changed_files, diff)

    print("Calling Claude for review...")
    review = call_claude(context)

    print("Posting review comment...")
    post_or_update_comment(pr_number, review)
    print("Done!")


if __name__ == "__main__":
    main()
