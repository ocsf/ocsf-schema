# <img src="ocsf.png" alt="OCSF Logo" width="32"/> Open Cybersecurity Schema Framework

[![Version](https://img.shields.io/badge/version-1.9.0-dev-blue.svg)](version.json)
[![License](https://img.shields.io/badge/license-Apache%202.0-green.svg)](LICENSE)
[![Schema Browser](https://img.shields.io/badge/schema-browser-orange.svg)](https://schema.ocsf.io)

The Open Cybersecurity Schema Framework (OCSF) is an open standard for cybersecurity event logging and data normalization. The framework is made up of a set of categories, event classes, data types, and an attribute dictionary. It is not restricted to cybersecurity nor to events, however the initial focus of the framework has been a schema for cybersecurity events. 

This repository contains the core schema definitions that enable consistent representation of security events across different tools and platforms. The core schema for cybersecurity events is intended to be agnostic to implementations. OCSF is intended to be used by both products and devices which produce log events, analytic systems, and logging systems which retain log events.

## 🚀 Quick Start

**Explore the Schema**: Visit [schema.ocsf.io](https://schema.ocsf.io) to browse the complete schema interactively.

**Key Resources**:
- [Understanding OCSF](https://github.com/ocsf/ocsf-docs/blob/main/overview/understanding-ocsf.md) - Comprehensive white paper
- [Contributing Guide](CONTRIBUTING.md) - How to contribute to the schema
- [Changelog](CHANGELOG.md) - Latest updates and changes

## 📁 Repository Structure

```
├── events/          # Event class definitions organized by category
├── objects/         # Reusable object definitions
├── profiles/        # Schema profiles for specific use cases
├── extensions/      # Schema extensions (Linux, Windows, etc.)
├── metaschema/      # Schema validation rules
├── templates/       # Template definitions
├── categories.json  # Event category definitions
├── dictionary.json  # Attribute dictionary
└── version.json     # Current schema version
```

## 🎯 What is OCSF?

OCSF provides:
- **Standardized Event Schema**: Common structure for cybersecurity events
- **Extensible Framework**: Support for custom extensions and profiles  
- **Format Agnostic**: Works with JSON, Parquet, Avro, and other formats
- **Vendor Neutral**: Open standard not tied to any specific vendor

The framework consists of:
- **Categories**: High-level groupings (Network, System, Application, etc.)
- **Event Classes**: Specific event types within categories
- **Objects**: Reusable data structures
- **Attributes**: Individual data fields with standardized definitions

## 🔧 Usage

OCSF is designed for:
- **Security Tools**: SIEM, SOAR, EDR, and other security platforms
- **Log Producers**: Applications, devices, and systems generating security events
- **Analytics Platforms**: Tools processing and analyzing security data
- **Data Pipelines**: ETL processes normalizing security data

## Automated PR Review

Pull requests that change schema definitions are automatically reviewed by two complementary workflows.

### Static Anti-Pattern Check

A deterministic checker (`check_antipatterns.py`) runs on every PR and flags structural design issues in changed attributes. It runs without an API key — fast, free, and reproducible.

**What it detects:**
- **Boolean Trap** — `is_*_known` booleans that mask multi-state concepts
- **Boolean Proliferation** — objects accumulating 3+ `is_*` booleans that may belong in an enum
- **Missing Sibling** — `_id` enum attributes without a corresponding string sibling
- **Tautological Description** — descriptions that just restate the attribute name
- **Enum Without Description** — enum values that have captions but no descriptions
- **Generic Naming** — attributes named `type`, `name`, `value` with thin descriptions
- **Type Inconsistency** — same attribute name with different types across objects
- **ID Without Enum** — `integer_t` `_id` attributes with no enum values defined
- **Duplicate Attribute** — `is_X` / `X` pairs with the same type
- **Duplicate Description** — different attribute names sharing identical description text
- **Learned Patterns** — rules extracted from previous LLM reviews (stored in `.github/config/learned_antipatterns.json`)

Deprecated attributes are ignored across all checks.

### LLM Description Review

A Claude-powered reviewer (`review_descriptions.py`) evaluates the compiled (fully resolved) schema for description quality and semantic anti-patterns that static analysis cannot catch.

**How it works:**
1. The `description-review-compile` workflow triggers on `pull_request` events, compiles the schema with `ocsf-schema-compiler`, and saves review context as an artifact
2. The `description-review-comment` workflow triggers on successful compilation, downloads the artifact, calls Claude, and posts an advisory comment on the PR

**What it evaluates:**
- Description clarity, precision, and self-containedness
- Whether descriptions are specific enough for an LLM to correctly populate fields from raw telemetry
- Semantic anti-patterns (overlap between attributes, incorrect type choices, indirect attribution)
- CHANGELOG.md convention compliance

The LLM reviewer is context-aware — on re-reviews it acknowledges fixed suggestions and re-raises outstanding ones.

### LLM-to-Static Learning Pipeline

When the LLM discovers a novel anti-pattern not covered by static rules, the finding is labeled in the PR comment and logged as JSON ready for addition to `.github/config/learned_antipatterns.json`. Once a human approves and merges the learned pattern, the static checker picks it up on all future PRs — turning a one-time LLM insight into a permanent, free, deterministic check.

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details on:
- How to propose schema changes
- Development workflow
- Community guidelines

## 📋 Versioning

OCSF follows [semantic versioning](https://semver.org/). Check [version.json](version.json) for the current version.

## 📄 License

Licensed under the [Apache License 2.0](LICENSE).

---

**Need Help?** 
- 📖 [Documentation](https://github.com/ocsf/ocsf-docs)
- 🌐 [Schema Browser](https://schema.ocsf.io)
- 💬 [Community Discussions](https://github.com/ocsf/ocsf-schema/discussions)
- ⚡ [Slack Workspace](https://github.com/ocsf#slack-workspace)
