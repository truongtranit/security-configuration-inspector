# Sprint 1 Learning Journal: Data Ingestion & Parsing Infrastructure

## What Did I Build?

In Sprint 1, I built the complete, decoupled core for the data ingestion and parsing layer of the Security Configuration Inspector. This layer acts as the foundation of the pipeline, taking raw inputs and transforming them into structured Python representations.

---

## What Did I Learn?

### 1. Interface Honesty & Type Contracts
I learned the importance of avoiding leaked business assumptions in base interfaces. Initially, assuming that `BaseParser.parse()` should promise a `dict` seemed logical because configuration files are typically key-value mappings. However, configuration formats like JSON and YAML allow root-level lists, scalars, or strings. Defining the contract as returning `Any` (or a `ConfigPayload` type alias) kept `BaseParser` strictly honest without forcing upstream assumptions.

### 2. The Boundary Between Storage (I/O) and Domain Logic
By strictly enforcing that `FileReader` returns raw `bytes` and `BaseParser` ingests `bytes`, I established a clear architectural invariant[cite: 1]. `FileReader` does not care if a file contains UTF-8, malformed JSON, or binary garbage[cite: 1]; its sole responsibility is bit retrieval[cite: 1]. The parser handles byte decoding and syntax evaluation.

### 3. Defensive Security with `yaml.safe_load()`
I gained a practical understanding of deserialization security. Using standard `yaml.load()` can introduce Remote Code Execution (RCE) vulnerabilities if a payload contains Python object tags (`!!python/object`). Enforcing `yaml.safe_load()` guarantees that untrusted input deserializes strictly into primitive Python types.

### 4. Advanced `pytest` Testing Patterns
* **Self-Contained Fixtures:** Using Pytest’s `tmp_path` fixture isolates tests from physical file dependencies, ensuring test suites are non-flaky, fast, and execution-environment agnostic.
* **State Isolation with Yield Fixtures:** Creating restorative fixtures (`restore_parser_registry`) using snapshotting (`.copy()`) and the `yield` teardown pattern prevents class-level state leakages (like mutating `ParserFactory._registered_parsers`) across unit tests.
* **Parametrization:** Using `@pytest.mark.parametrize` eliminates code duplication while testing edge-case variations (e.g., non-bytes input types or scalar parsing).

---

## What Challenged Me?

* **Exception Translation & Context Preservation:** Designing a domain exception hierarchy required careful thought around inheritance. Catching standard library exceptions (`FileNotFoundError`, `UnicodeDecodeError`, `JSONDecodeError`, `yaml.YAMLError`) and re-raising them as structured domain errors (`ResourceNotFoundError`, `EncodingError`, `JSONSyntaxError`) using `from e` was crucial to keep higher-level orchestration code clean while preserving debugging tracebacks.
* **DRY Exception Refactoring:** Refactoring duplicate `__init__` methods across exception subclasses into `ReaderError` required leveraging Python OOP properly to pass positional arguments (`resource`, `operation`, `message`) up to `super().__init__()`.

---

## What Mistakes Did I Make?

1. **Code Duplication in Custom Exceptions:** In the initial draft of `reader_exceptions.py`, every subclass (`ResourceNotFoundError`, `AccessDeniedError`, `ResourceInvalidError`) duplicated identical attribute assignment and message formatting logic—even accidentally repeating `"File does not exist at..."` for permission errors.
   * *Fix:* Pushed shared attributes (`self.resource`, `self.operation`) up to `ReaderError.__init__` and overridden standard messages gracefully.
2. **Path Instantiation Outside `try` Block:** `path = Path(source)` sat outside the `try...except` block in `FileReader.read()`. If a caller passed an invalid type like `None`, it threw an unhandled standard `TypeError` instead of being caught and wrapped in a domain exception.
   * *Fix:* Moved `Path(source)` inside the `try` block and mapped `TypeError` to `ResourceInvalidError`.
3. **Hardcoding Physical Fixture Files:** My initial unit test for `FileReader` relied on a static physical file (`tests/resources/valid.txt`).
   * *Fix:* Refactored to dynamic `tmp_path` setup/teardown.

---

## What Would I Improve?

* **Binary Stream & Large File Handling:** `FileReader.read_bytes()` loads the entire file payload into memory at once. For Sprint 1 this works well, but for enterprise-scale or deeply nested files, I would consider supporting streaming byte chunks or context-managed buffer streams.
* **Auto-Discovery for Parsers:** `ParserFactory` currently uses an explicit dictionary mapping (`_registered_parsers`). I could improve this by implementing dynamic auto-registration using module inspection or Python entry points so new parsers are registered automatically upon module import.
* **Enhanced Diagnostic Metadata for YAML:** While `JSONSyntaxError` captures explicit `lineno` and `colno` from `json.JSONDecodeError`, `YAMLSyntaxError` currently extracts `str(e)`. Parsing PyYAML's `ProblemMark` object directly would allow capturing line/column metadata for YAML syntax errors as well.

## Sprint 2

What did I build?

What did I learn?

What challenged me?

What mistakes did I make?

What would I improve?