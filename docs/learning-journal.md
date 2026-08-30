# Learning Journal

# Sprint 1 — Data Ingestion & Parsing Infrastructure

## What Did I Build?

In Sprint 1, I built the decoupled data-ingestion and parsing foundation for the Security Configuration Inspector.

The layer separates:

```text
Resource → FileReader → raw bytes → ParserFactory → concrete parser → Python object
```

The completed components include `BaseReader`, `FileReader`, `BaseParser`, `JsonParser`, `YamlParser`, and `ParserFactory`.

## What Did I Learn?

### 1. Interface Honesty & Type Contracts

I learned the importance of avoiding leaked business assumptions in base interfaces.

JSON and YAML can represent root-level mappings, sequences, scalars, and null values. Therefore, the parser boundary should not assume every parsed document is a dictionary.

### 2. The Boundary Between Storage and Domain Logic

`FileReader` retrieves raw bytes. Parsers handle decoding and syntax evaluation.

This separation means the reader does not need to understand JSON, YAML, UTF-8 semantics, or configuration policy.

### 3. Defensive YAML Deserialization

I learned why `yaml.safe_load()` is important when processing untrusted configuration input. YAML deserialization should not permit arbitrary Python object construction.

### 4. Advanced pytest Patterns

I practiced:

- `tmp_path` for isolated filesystem tests.
- Yield fixtures for restoring mutable parser-factory state.
- `pytest.mark.parametrize` for boundary and type cases.
- Focused tests followed by full-suite regression testing.

## What Challenged Me?

- Translating low-level exceptions into domain-specific exceptions while preserving the original traceback.
- Designing an exception hierarchy without duplicating common initialization logic.
- Keeping reader responsibilities separate from parser responsibilities.

## What Mistakes Did I Make?

1. Duplicated exception initialization across subclasses.
2. Created `Path(source)` outside the protected error-handling boundary.
3. Initially relied on static physical fixture files.

## What Would I Improve?

- Consider streaming or chunked handling for very large resources.
- Consider more dynamic parser registration if the project later needs it.
- Improve YAML diagnostic metadata by extracting line/column information from PyYAML's parser marks.

---

# Sprint 2 — Configuration Normalization

## What Did I Build?

Sprint 2 established `ConfigNormalizer` as the canonical boundary between parser output and security validation.

The completed work includes:

- `BaseNormalizer` abstraction.
- `ConfigNormalizer` implementation.
- `ConfigurationInvalidError`.
- Root-type validation.
- Required `port` validation.
- Canonical defaults.
- Strict type/value validation.
- Source-to-canonical alias resolution.
- Ambiguity detection for conflicting representations.
- `allow_users` validation and canonicalization.
- Deep-copy immutability.
- Unknown-field preservation.
- JSON/YAML cross-format equivalence testing.
- Full configuration integration testing.

The current pipeline is:

```text
FileReader
    ↓
ParserFactory
    ↓
JsonParser / YamlParser
    ↓
Python object
    ↓
ConfigNormalizer
    ↓
Canonical configuration
    ↓
SecurityValidator (next)
```

## What Did I Learn?

### 1. Normalization Is a Boundary, Not Just Formatting

I learned that normalization should create a stable representation that downstream components can rely on.

For example:

```text
listen_port
Port
ListenPort
ssh_port
```

can all become:

```text
port
```

This means validation does not need to understand every source representation.

### 2. Canonicalization Needs Explicit Conflict Rules

A major design decision was that aliases cannot silently override one another.

This is acceptable:

```python
{"port": 22, "listen_port": 22}
```

but this is ambiguous:

```python
{"port": 22, "listen_port": 2222}
```

The second case raises `ConfigurationInvalidError`.

### 3. Strict Python Types Matter

Python's type system has edge cases that matter for configuration security.

For example:

```python
isinstance(True, int)
```

is `True`.

Therefore, validating a port with `isinstance(port, int)` alone would incorrectly accept booleans.

The implementation uses strict type checks where the contract requires them.

### 4. Canonicalization Order Matters

For `allow_users`, the order is:

```text
type validation
    ↓
blank validation
    ↓
trim
    ↓
deduplicate
```

This means:

```python
["  admin  ", "admin"]
```

correctly becomes:

```python
["admin"]
```

### 5. Unknown Data and Security Policy Are Different Concerns

Unknown configuration fields are currently preserved.

I learned that preserving an unknown field is different from deciding whether that field is secure.

The normalizer should establish representation; the future `SecurityValidator` should evaluate security policy.

### 6. Integration Tests Should Verify Architectural Contracts

N-044 verifies that equivalent JSON and YAML inputs converge to the same canonical representation.

N-046 verifies that aliases, defaults, validation, canonicalization, and unknown-field preservation work together in a realistic configuration.

## What Challenged Me?

### 1. Evolving the Contract Without Breaking Earlier Tests

The original structural tests expected mappings to pass through unchanged. Once `port` became a required canonical field, those tests represented an outdated contract.

The correct response was to update the tests so they reflect the new component boundary rather than weakening the new implementation.

### 2. Designing Alias Ambiguity

The initial implementation gave the canonical key implicit precedence over aliases. That was convenient but unsafe because contradictory configuration could be silently ignored.

The contract was changed so conflicting representations raise an error.

### 3. Keeping Mutable Defaults Safe

`allow_users` defaults to an empty list. The implementation must ensure that one normalization does not share mutable list state with another normalization.

Deep copying and constructing independent default state are important safeguards.

### 4. Building the Test Backlog as a Development Tool

The N-series backlog evolved from broad structural tests into a detailed canonicalization contract.

This made the backlog useful as both a testing plan and a record of design decisions.

## What Mistakes Did I Make?

1. Initially returned the raw payload without enforcing the new canonical schema.
2. Initially allowed canonical fields to silently coexist with conflicting aliases.
3. Added schema expectations before updating older structural tests to reflect the new contract.
4. Had to distinguish carefully between an alias with the same value and an alias with a conflicting value.

## What Would I Improve?

- Centralize field definitions, aliases, defaults, and validation metadata if the schema grows substantially.
- Consider dedicated value objects or typed models if the canonical configuration becomes more complex.
- Add stronger integration coverage once `SecurityValidator` exists.
- Keep security-policy decisions outside the normalizer.

---

# Sprint 2 Outcome

Sprint 2 is complete through N-046.

The resulting boundary is:

```text
Parser output
     ↓
ConfigNormalizer
     ↓
stable canonical configuration
     ↓
SecurityValidator
```

The next learning phase is to design and implement `SecurityValidator` without allowing policy logic to leak back into the parser or normalizer.
