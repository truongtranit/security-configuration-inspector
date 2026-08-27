# Security Configuration Inspector

## Project Overview

### What problem does this project solve?

This project automates the scanning of configuration files against
established security policies. It addresses the operational challenge of
manually checking configurations for security misconfigurations,
enabling teams to quickly identify security vulnerabilities, ensure
compliance, and generate structured compliance reports automatically.

### Who is the intended user?

The primary intended user is a Security Analyst who needs to audit
infrastructure configurations, ensure alignment with corporate or
industry benchmarks, and generate compliance data.

------------------------------------------------------------------------

# Architecture

## System Architecture

``` mermaid
flowchart LR
    subgraph Input["Input Layer"]
        Resource["Configuration Resource"]
        Reader["FileReader"]
    end

    subgraph Parsing["Parsing Layer"]
        Factory["ParserFactory"]
        JSON["JsonParser"]
        YAML["YamlParser"]
    end

    subgraph Processing["Processing Layer"]
        Normalizer["ConfigNormalizer"]
        Validator["SecurityValidator"]
    end

    subgraph Output["Output Layer"]
        Reporter["ReportGenerator"]
    end

    Resource --> Reader
    Reader -->|bytes| Factory

    Factory -->|.json| JSON
    Factory -->|.yaml / .yml| YAML

    JSON --> Normalizer
    YAML --> Normalizer

    Normalizer --> Validator
    Validator --> Reporter
```

> **Note:** This diagram illustrates the static component architecture
> of the application. Runtime execution and data transformation are
> documented separately in the Processing Pipeline and Sequence Diagram.

------------------------------------------------------------------------

## Processing Pipeline

The system processes data linearly through decoupled components:

``` mermaid
flowchart TD
    A["Configuration Resource"] --> B["FileReader"]

    B --> C["Raw Bytes"]

    C --> D["ParserFactory"]

    D --> E{"File Extension"}

    E -->|".json"| F["JsonParser"]
    E -->|".yaml"| G["YamlParser"]
    E -->|".yml"| G

    F --> H["Python Object"]
    G --> H

    H --> I["ConfigNormalizer"]

    I --> J["Canonical Configuration Model"]

    J --> K["SecurityValidator"]

    K --> L["Validation Results"]

    L --> M["ReportGenerator"]

    M --> N["Security Report"]
```

------------------------------------------------------------------------

## Sequence Diagram

``` mermaid
sequenceDiagram
    participant App as Application
    participant Reader as FileReader
    participant Factory as ParserFactory
    participant Parser as Concrete Parser
    participant Normalizer as ConfigNormalizer
    participant Validator as SecurityValidator
    participant Reporter as ReportGenerator

    App->>Reader: read(resource)
    Reader-->>App: raw bytes

    App->>Factory: get_parser(resource)
    Factory->>Factory: Resolve file extension

    alt .json
        Factory-->>App: JsonParser instance
    else .yaml / .yml
        Factory-->>App: YamlParser instance
    end

    App->>Parser: parse(raw bytes)
    Parser-->>App: Python object

    App->>Normalizer: normalize(object)
    Normalizer-->>App: canonical configuration

    App->>Validator: validate(configuration)
    Validator-->>App: validation results

    App->>Reporter: generate(results)
    Reporter-->>App: security report
```

------------------------------------------------------------------------

# Features

## Current Features

-   Binary-safe file ingestion
-   JSON configuration parsing
-   YAML configuration parsing
-   Extensible parser selection via `ParserFactory`
-   Dynamic parser registration
-   Case-insensitive `.json`, `.yaml`, and `.yml` extension handling
-   Application-level parser and factory exception hierarchy
-   Comprehensive unit tests for the implemented ingestion and parsing
    components
-   Initial `ConfigNormalizer` structural validation
-   Clean Architecture inspired component boundaries

## Current Normalizer Contract

`ConfigNormalizer` currently:

-   Accepts configuration mappings.
-   Preserves empty mappings.
-   Preserves nested mappings and lists.
-   Preserves scalar values and their Python types.
-   Rejects `None` roots.
-   Rejects non-mapping roots.
-   Does not mutate caller input.

Canonical field mapping and the final canonical schema are still Sprint
2 work.

------------------------------------------------------------------------

# Installation

Clone the repository:

``` bash
git clone https://github.com/<username>/SecurityConfigInspector.git

cd SecurityConfigInspector
```

Create a virtual environment:

``` bash
python -m venv .venv
```

Activate it.

Windows

``` bash
.venv\Scripts\activate
```

Linux/macOS

``` bash
source .venv/bin/activate
```

Install dependencies

``` bash
pip install -r requirements.txt
```

Run tests

``` bash
python -m pytest
```

------------------------------------------------------------------------

# Usage

The command-line interface is currently under development.

At this stage, components can be exercised independently through unit
tests:

``` bash
python -m pytest
```

Future releases will support:

``` bash
python main.py config.json
```

------------------------------------------------------------------------

# Development Progress

| Component | Status |
|---|:---:|
| Project Setup | ✅ Complete |
| BaseReader | ✅ Complete |
| FileReader | ✅ Complete |
| BaseParser | ✅ Complete |
| JsonParser | ✅ Complete |
| YamlParser | ✅ Complete |
| ParserFactory | ✅ Complete |
| Unit Tests | ✅ Complete |
| BaseNormalizer | ✅ Complete |
| ConfigNormalizer — Structural Contract | ✅ Complete |
| ConfigNormalizer — Canonical Schema | 🟡 In Progress |
| ConfigNormalizer — Field Mapping | ⬜ Planned |
| SecurityValidator | ⬜ Planned |
| ReportGenerator | ⬜ Planned |
| CLI | ⬜ Planned |

------------------------------------------------------------------------

# Milestones & Roadmap

## Sprint 1 --- Ingestion and Parsing

Sprint 1 established the engineering foundation and ingestion pipeline.

-   Project setup and Git workflow.
-   `BaseReader` and `FileReader`.
-   `BaseParser`, `JsonParser`, and `YamlParser`.
-   Dynamic `ParserFactory`.
-   Comprehensive unit tests.
-   Architecture documentation and diagrams.

**Deliverable:** JSON and YAML configuration data can be read and
converted into native Python objects.

## Sprint 2 --- Configuration Normalization

Sprint 2 establishes the canonical configuration boundary.

### Completed so far

-   Initial `ConfigNormalizer`.
-   Root mapping validation.
-   Empty mapping support.
-   Nested structure preservation.
-   Scalar preservation.
-   Invalid root handling.
-   Input immutability tests.
-   Normalizer exception hierarchy tests.

### Remaining work

-   Define `BaseNormalizer`.
-   Define the canonical configuration schema.
-   Define canonical field names and types.
-   Define field mapping rules.
-   Implement source-to-canonical mappings.
-   Verify equivalent JSON and YAML configurations produce equivalent
    canonical representations.
-   Integrate the normalized representation with validation.

## Sprint 3 --- Security Validation

Planned: security policy engine, CIS-style rules, and structured PASS /
FAIL / WARNING findings.

## Sprint 4 --- Reporting & Observability

Planned: HTML, JSON/CSV reporting and structured logging.

## Sprint 5 --- Integration

Planned: REST API integration.

## Long-Term Extensibility

Potential support for additional configuration formats such as XML and
TOML.

------------------------------------------------------------------------

# Non-Functional Requirements

## Performance

The application should process 100 configuration files in under 5
seconds. \## Maintainability New parsers should be added without
modifying existing validator code. \## Reliability Malformed input
should produce informative errors rather than crashes. \## Security No
secrets shall be hardcoded. Credentials must come from environment
variables or configuration files.

------------------------------------------------------------------------

# Project Structure

    SecurityConfigInspector/

    ├── docs/
    │   ├── architecture.md
    │   ├── developer-guide.md
    │   ├── testing_strategy.md
    │   └── adr/
    │
    ├── src/
    │   ├── readers/
    │   ├── parsers/
    │   ├── factories/
    │   ├── exceptions/
    │   └── ...
    │
    ├── tests/
    │   ├── readers/
    │   ├── parsers/
    │   └── factories/
    │
    ├── requirements.txt
    ├── pyproject.toml
    └── README.md

------------------------------------------------------------------------

# Documentation

The project documentation includes:

-   Architecture Overview
-   Processing Pipeline
-   Sequence Diagrams
-   Architecture Decision Records (ADRs)
-   Developer Guide
-   Testing Strategy
-   Learning Journal

------------------------------------------------------------------------

# Engineering Principles

This project is intentionally designed as a portfolio-quality software
engineering project.

Key principles include:

-   SOLID principles
-   Separation of Concerns
-   Clean Architecture
-   Dependency Inversion
-   Domain-specific exception hierarchy
-   Test-driven thinking
-   Extensible component design

------------------------------------------------------------------------

# Testing

The project emphasizes contract-driven unit testing.

Current coverage includes:

-   FileReader
-   JsonParser
-   YamlParser
-   ParserFactory
-   ConfigNormalizer structural contract

Tests verify:

-   Happy paths
-   Boundary conditions
-   Exception translation
-   Public API contracts
-   Dynamic parser registration

------------------------------------------------------------------------

# License
