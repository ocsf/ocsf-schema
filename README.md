# <img src="ocsf.png" alt="OCSF Logo" width="32"/> Open Cybersecurity Schema Framework

[![Version](https://img.shields.io/badge/version-1.8.0--dev-blue.svg)](version.json)
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
