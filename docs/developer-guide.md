# Developer Guide

## Purpose

This guide describes the current development conventions and component contracts for the Security Configuration Inspector.

The project is being developed incrementally using contract-driven tests, small feature branches, focused commits, and pull requests.

---

# Architecture at a Glance

```text
Configuration Resource
        │
        ▼
    FileReader
        │
        ▼
   ParserFactory
      /     \
     ▼       ▼
JsonParser YamlParser
      \     /
       ▼   ▼
  ConfigNormalizer
        │
        ▼
Canonical Configuration
        │
        ▼
 SecurityValidator
        │
        ▼
 ReportGenerator
```

Each component should have one clear responsibility and a testable boundary.

---

# ParserFactory

## Purpose

`ParserFactory` selects and instantiates the appropriate parser based on a resource's file extension.

## Current API

```python
ParserFactory.get_parser(resource)
```

### Accepted inputs

- `str`
- `pathlib.Path`

### Current registrations

```text
.json       → JsonParser
.yaml       → YamlParser
.yml        → YamlParser
```

### Responsibilities

- Normalize extensions.
- Select the registered parser class.
- Return a fresh parser instance.
- Support runtime registration.
- Raise factory-specific exceptions for invalid or unsupported resources.

### Non-responsibilities

- File I/O.
- Configuration parsing.
- Configuration normalization.
- Security validation.

## Adding a Parser

1. Create a `BaseParser` subclass.
2. Implement `parse(bytes)`.
3. Translate relevant low-level errors into domain exceptions.
4. Register the parser with `ParserFactory`.
5. Add focused parser tests.
6. Add factory routing tests.
7. Add documentation.

---

# ConfigNormalizer

## Purpose

`ConfigNormalizer` establishes the canonical configuration boundary between parser output and future security validation.

The normalizer is deliberately responsible for **representation and structural correctness**, not security-policy decisions.

For example, it can determine that `password_auth` is an alias for `password_authentication`. A future `SecurityValidator` should determine whether enabling password authentication violates a security policy.

## Base Contract

```python
from abc import ABC, abstractmethod
from typing import Any

class BaseNormalizer(ABC):
    @abstractmethod
    def normalize(self, raw_payload: Any) -> dict[str, Any]:
        ...
```

`ConfigNormalizer` implements this contract.

## Current Responsibilities

1. Validate the root type.
2. Deep-copy caller input.
3. Resolve source aliases.
4. Detect conflicting representations.
5. Require `port`.
6. Apply optional defaults.
7. Validate canonical field types and values.
8. Canonicalize `allow_users`.
9. Preserve unknown fields.
10. Return the canonical dictionary.

## Root Contract

```text
dict       → accepted for normalization
non-dict   → ConfigurationInvalidError
```

The required canonical field means an accepted dictionary must ultimately contain a valid `port`.

## Canonical Schema

| Field | Type | Rule | Default |
|---|---|---|---|
| `port` | `int` | Required, 1–65535, strict integer | — |
| `permit_root_login` | `bool` | Strict boolean | `False` |
| `password_authentication` | `bool` | Strict boolean | `False` |
| `protocol_version` | `int` | Strict value `2` | `2` |
| `max_auth_tries` | `int` | Positive integer | `3` |
| `allow_users` | `list[str]` | Valid usernames only | `[]` |

## Alias Resolution

The normalizer supports source aliases for the canonical fields.

Examples:

```python
{"listen_port": 2222}
```

becomes:

```python
{"port": 2222, ...}
```

and:

```python
{"allowed_users": ["alice"]}
```

becomes:

```python
{"allow_users": ["alice"], ...}
```

## Ambiguity Handling

Multiple representations of the same canonical field are allowed only when their values agree.

Valid:

```python
{
    "port": 22,
    "listen_port": 22,
}
```

Invalid:

```python
{
    "port": 22,
    "listen_port": 2222,
}
```

The second case raises `ConfigurationInvalidError`.

This prevents silent precedence rules from hiding contradictory configuration.

## `allow_users`

The canonicalization sequence is:

```text
validate list
    ↓
validate every item is str
    ↓
reject empty / whitespace-only usernames
    ↓
trim surrounding whitespace
    ↓
deduplicate
    ↓
preserve first-occurrence order
```

Example:

```python
["  alice  ", "\tbob\n", "alice"]
```

becomes:

```python
["alice", "bob"]
```

## Unknown Fields

Unknown fields are currently preserved.

This is intentional: the normalizer canonicalizes fields it understands without silently discarding information it does not understand.

Security meaning belongs to `SecurityValidator`.

---

# Testing Strategy

The project uses pytest and contract-focused tests.

Tests should generally follow:

```text
Arrange
  ↓
Act
  ↓
Assert
```

## Parameterization

Use `pytest.mark.parametrize` when the same behavior needs to be tested against several inputs.

Example:

```python
@pytest.mark.parametrize("invalid_port", [0, -1, 65536])
def test_invalid_port(...):
    ...
```

This keeps tests concise while preserving explicit edge cases.

## Integration Tests

Integration tests should verify important component boundaries rather than duplicate every unit test.

N-044 verifies:

```text
JSON → JsonParser → ConfigNormalizer
YAML → YamlParser → ConfigNormalizer
```

produce the same canonical output for equivalent configurations.

N-046 verifies that a realistic mixed configuration exercises the complete normalization contract.

---

# Normalizer Development Workflow

For a new normalizer behavior:

1. Define the behavior contract.
2. Add or update the testing backlog.
3. Write the failing test.
4. Implement the smallest behavior needed.
5. Run the focused test.
6. Run the complete test suite.
7. Update documentation.
8. Review the diff.
9. Commit the focused change.
10. Push the feature branch.
11. Open a pull request.
12. Merge only after tests are green.
13. Return to `main`, pull the merged changes, and delete the feature branch.

---

# Git Workflow

The project uses short-lived feature branches.

Typical workflow:

```bash
git checkout main
git pull origin main
git checkout -b test/<focused-change>

python -m pytest -v

git status
git diff

git add <files>
git diff --cached
git commit -m "<focused message>"
git push -u origin test/<focused-change>
```

After the pull request is merged:

```bash
git checkout main
git pull origin main
git status
git branch -d test/<focused-change>
```

The preferred state before starting new work is:

```text
main
up to date with origin/main
working tree clean
```

---

# Definition of Done

A feature/test backlog item is considered complete when:

- The behavior has an explicit contract.
- Tests cover the intended behavior.
- The full pytest suite passes.
- Relevant documentation is updated.
- The change is committed.
- The branch is pushed.
- The pull request is reviewed and merged.
- `main` is synchronized afterward.

---

# Current Development Position

Sprint 1 is complete.

Sprint 2 — ConfigNormalizer — is complete through N-046.

The next major development area is `SecurityValidator`, which will consume the canonical configuration produced by `ConfigNormalizer`.
