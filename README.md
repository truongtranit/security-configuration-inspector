# Security Configuration Inspector

## Project Overview

### What problem does this project solve?
This project automates the scanning of configuration files against established security policies. It addresses the operational challenge of manually checking configurations for security misconfigurations, enabling teams to quickly identify security vulnerabilities, ensure compliance, and generate structured compliance reports automatically.

### Who is the intended user?
The primary intended user is a Security Analyst who needs to audit infrastructure configurations, ensure alignment with corporate or industry benchmarks, and generate compliance data.

---

## Technical Scope & Architecture

### Processing Workflow
The system processes data linearly through decoupled components:
```mermaid
flowchart TD

A[User] --> B[FileReader]
B --> C[Raw Text]
C --> D[ParserFactory]
D --> E{Parser}

E --> F[JsonParser]
E --> G[YamlParser]

F --> H[Python Dictionary]
G --> H

H --> I[ConfigNormalizer]
I --> J[Canonical Dictionary]
J --> K[SecurityValidator]
K --> L[ValidationResult]
L --> M[ReportGenerator]
M --> N[HTML / JSON Report]
```
---
### System Architecture
```mermaid
graph TD

Application["Security Configuration Inspector"]

Application --> Readers
Application --> Parsers
Application --> Normalizers
Application --> Validators
Application --> Reporters

Readers --> FileReader
Readers --> HttpReader

Parsers --> JsonParser
Parsers --> YamlParser

Validators --> SecurityValidator

Reporters --> HtmlReporter
Reporters --> JsonReporter
```
---
### Processing Pipeline
```mermaid
flowchart TD

A[Configuration File]
--> B[Raw Text]
--> C[Python Object]
--> D[Canonical Model]
--> E[Validation Result]
--> F[HTML Report]
```
---
### Component Interaction
```mermaid
flowchart TD

A[main]
--> B[ParserFactory]
--> C[JsonParser]
--> D[ConfNormalizer]
--> E[SecurityValidator]
--> F[ReportGenerator]
```
---


## Milestones & Roadmap

### What is the current scope of Sprint 1?
Sprint 1 establishes the baseline engineering foundation and ingestion pipeline.
* Infrastructure Setup: Project structure initialization, Python virtual environment configuration, and Git repository setup.
* Ingestion Layer: Implementation of BaseReader and FileReader to ingest raw text data.
* Parsing Layer: Implementation of BaseParser, JsonParser, YamlParser, and a dynamic ParserFactory to auto-detect and deserialize files.
* Quality Assurance: Unit test suites ensuring parsing reliability.
* Deliverable: A system that ingests a JSON or YAML file and successfully converts it into a native Python object.

### What are the planned future enhancements?
The roadmap details the progressive addition of core logic, verification capabilities, and integrations:
* Sprint 2 (Normalization): Integration of ConfigNormalizer, field mapping rules, and a canonical schema to ensure uniform internal representation regardless of source format.
* Sprint 3 (Security Validation): A robust policy engine implementing CIS-style security rules providing structured evaluation outcomes (PASS / FAIL / WARNING).
* Sprint 4 (Reporting & Observability): Multi-format reporting export options (HTML, JSON, CSV) alongside detailed system logging.
* Sprint 5 (Integration): Integration capabilities to consume REST APIs.
* Extensibility: Long-term architectural goals include native support for additional configuration formats such as XML and TOML.

---
## Non-Functional Requirements

### Performance
The application should process 100 configuration files in under 5 seconds.
### Maintainability
New parsers should be added without modifying existing validator code.
### Reliability
Malformed input should produce informative errors rather than crashes.
### Security
No secrets shall be hardcoded.
Credentials must come from environment variables or configuration files.

---

