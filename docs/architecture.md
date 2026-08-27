# System Architecture

``` mermaid
graph TD

    User["Security Analyst"]

    User --> CLI["CLI / main.py"]

    CLI --> Readers
    CLI --> Parsers
    CLI --> Normalizers
    CLI --> Validators
    CLI --> Reporters

    Readers --> BaseReader
    BaseReader --> FileReader

    Parsers --> ParserFactory
    ParserFactory --> JsonParser
    ParserFactory --> YamlParser

    Normalizers --> ConfigNormalizer

    Validators --> SecurityValidator

    Reporters --> HtmlReporter
    Reporters --> JsonReporter

    Validators --> Policies["CIS Policies"]

    Readers --> Resources["Configuration Files"]

    Reporters --> Reports["Planned Security Reports"]
```

## \> **Note:** This diagram illustrates the static component architecture of the application. Runtime execution and data transformation are documented separately in the Processing Pipeline and Sequence Diagram

# Component Architecture

``` mermaid
graph TD

    CLI["main.py"]

    CLI --> ReaderFactory
    CLI --> ParserFactory

    ReaderFactory --> BaseReader
    BaseReader --> FileReader

    ParserFactory --> BaseParser
    BaseParser --> JsonParser
    BaseParser --> YamlParser

    CLI --> ConfigNormalizer

    CLI --> SecurityValidator

    CLI --> HtmlReporter
    CLI --> JsonReporter

    SecurityValidator --> Policies["CIS Policies"]

    HtmlReporter --> Reports["HTML Reports"]

    JsonReporter --> Reports
```

------------------------------------------------------------------------

# Processing Pipeline

``` mermaid
flowchart TD

    Start([Start])

    Start --> Resource["Configuration Resource"]

    Resource --> Reader["BaseReader"]

    Reader --> Bytes["Raw Bytes"]

    Bytes --> ParserFactory

    ParserFactory --> JSON["JsonParser"]

    ParserFactory --> YAML["YamlParser"]

    JSON --> Object["Python Object"]

    YAML --> Object

    Object --> Normalizer["ConfigNormalizer"]

    Normalizer --> Canonical["Canonical Configuration"]

    Canonical --> Validator["SecurityValidator"]

    Validator --> Result["Validation Result"]

    Result --> Reporter["Report Generator"]

    Reporter --> End([HTML / JSON Report])
```

------------------------------------------------------------------------

# Sequence Diagram

``` mermaid
sequenceDiagram

    actor User

    participant Main
    participant Reader
    participant ParserFactory
    participant Parser
    participant Normalizer
    participant Validator
    participant Reporter

    User->>Main: Scan()

    Main->>Reader: read(resource)

    Reader-->>Main: bytes

    Main->>ParserFactory: get_parser(resource)

    alt .json
        ParserFactory-->>Main: JsonParser
    else .yaml / .yml
        ParserFactory-->>Main: YamlParser
    end

    Main->>Parser: parse(bytes)

    Parser-->>Main: Python object

    Main->>Normalizer: normalize(dict)

    Normalizer-->>Main: canonical_dict

    Main->>Validator: validate(canonical_dict)

    Validator-->>Main: ValidationResult

    Main->>Reporter: generate(result)

    Reporter-->>Main: HTML Report

    Main-->>User: Display Report
```

------------------------------------------------------------------------

## Design Principles

-   Separation of Concerns
-   SOLID principles
-   Dependency Inversion
-   Domain-specific exception handling
-   Test-driven development
-   Extensible component boundaries

------------------------------------------------------------------------

## Project Structure

------------------------------------------------------------------------

## Dependencies
