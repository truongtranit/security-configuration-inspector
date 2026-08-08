# Class Diagram

```mermaid
classDiagram

class BaseReader{
    <<abstract>>
    +read(resource) bytes
}

class FileReader

BaseReader <|-- FileReader

class BaseParser{
    <<abstract>>
    +parse(bytes) dict
}

class JsonParser
class YamlParser

BaseParser <|-- JsonParser
BaseParser <|-- YamlParser

class ParserFactory{
    +get_parser(resource)
}

ParserFactory --> BaseParser

class BaseNormalizer{
    <<abstract>>
    +normalize(dict)
}

class ConfigNormalizer

BaseNormalizer <|-- ConfigNormalizer

class BaseValidator{
    <<abstract>>
    +validate(model)
}

class SecurityValidator

BaseValidator <|-- SecurityValidator

class BaseReporter{
    <<abstract>>
    +generate(result)
}

class HtmlReporter
class JsonReporter

BaseReporter <|-- HtmlReporter
BaseReporter <|-- JsonReporter
```

---

# Processing Pipeline

```mermaid
flowchart TD

    Resource["Configuration Resource"]

    Resource --> Reader["FileReader"]

    Reader --> Bytes["Raw Bytes"]

    Bytes --> ParserFactory

    ParserFactory --> JsonParser

    ParserFactory --> YamlParser

    JsonParser --> Dictionary["Python Dictionary"]

    YamlParser --> Dictionary

    Dictionary --> Normalizer["ConfigNormalizer"]

    Normalizer --> Canonical["Canonical Configuration"]

    Canonical --> Validator["SecurityValidator"]

    Validator --> Findings["Validation Findings"]

    Findings --> Reporter["HtmlReporter / JsonReporter"]

    Reporter --> Reports["Compliance Reports"]
```

---


# Full Runtime Sequence Diagram

```mermaid
sequenceDiagram

    actor User

    participant Main
    participant FileReader
    participant ParserFactory
    participant JsonParser
    participant ConfigNormalizer
    participant SecurityValidator
    participant HtmlReporter

    User->>Main: scan(resource)

    Main->>FileReader: read(resource)

    FileReader-->>Main: bytes

    Main->>ParserFactory: get_parser(resource)

    ParserFactory-->>Main: JsonParser

    Main->>JsonParser: parse(bytes)

    JsonParser-->>Main: dict

    Main->>ConfigNormalizer: normalize(dict)

    ConfigNormalizer-->>Main: canonical_dict

    Main->>SecurityValidator: validate(canonical_dict)

    SecurityValidator-->>Main: ValidationResult

    Main->>HtmlReporter: generate(result)

    HtmlReporter-->>Main: HTML

    Main-->>User: Display HTML Report
```


---


# ParserFactory

## Purpose

ParserFactory is responsible for selecting and instantiating the appropriate parser implementation based on the configuration resource.

## Responsibilities

- Accept both `str` and `pathlib.Path`
- Normalize file extensions
- Return concrete parser implementations
- Support runtime parser registration
- Raise meaningful domain exceptions

## Non-Responsibilities

- Reading files
- Parsing configuration
- Validation
- Normalization

---

## Design Decisions

### Registry stores parser classes

The registry stores parser classes rather than parser instances.

Reasons:

- fresh parser instance per request
- avoids shared mutable state
- supports dependency injection
- supports dynamic registration
- follows the Open/Closed Principle

### Public API

ParserFactory.get_parser(resource)

Accepts:

- str
- pathlib.Path

Returns:

- BaseParser

Raises:

- FactoryError
- UnsupportedParserError

---

# Adding a Parser
## 1.
Create BaseParser subclass

## 2.
Implement parse()

## 3.
Register with ParserFactory

## 4.
Write tests

## 5.
Update documentation

