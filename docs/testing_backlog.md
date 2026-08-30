# Testing Backlog

This document tracks planned, deferred, and completed test contracts for the Security Configuration Inspector. Test IDs describe behaviors, not necessarily individual pytest node IDs.

## Status Legend

| Symbol | Meaning |
|---|---|
| ⬜ | Planned |
| 🟡 | In Progress |
| ✅ | Complete |
| 📌 | Deferred |
| 📋 | Backlog |

---

# FileReader

## Active Test Cases

| ID | Priority | Behavior | Expected Result | Status |
|---|---|---|---|---|
| R-001 | High | Read existing file | Returns file contents as `bytes` | ✅ Complete |
| R-002 | High | File does not exist | Raises project exception | ✅ Complete |
| R-003 | High | Path is a directory | Raises project exception | ✅ Complete |
| R-004 | High | Empty file | Returns `b""` | ✅ Complete |

## Deferred Tests

| ID | Priority | Behavior | Expected Result | Status | Notes |
|---|---|---|---|---|---|
| R-005 | Medium | Permission denied | Raises project exception | 📌 Deferred | Requires mocking |
| R-006 | Medium | Unexpected I/O failure | Raises project exception | 📌 Deferred | Requires mocking |

---

# JsonParser

## Active Test Cases

| ID | Priority | Behavior | Expected Result | Status |
|---|---|---|---|---|
| P-001 | High | Parse valid JSON object | Returns Python `dict` | ✅ Complete |
| P-002 | High | Parse valid JSON array | Returns Python `list` | ✅ Complete |
| P-003 | High | Parse empty JSON object | Returns `{}` | ✅ Complete |
| P-004 | High | Parse empty JSON array | Returns `[]` | ✅ Complete |
| P-005 | High | Invalid UTF-8 | Raises `EncodingError` | ✅ Complete |
| P-006 | High | Malformed JSON | Raises `JSONSyntaxError` | ✅ Complete |
| P-007 | Medium | Non-bytes input | Raises parser contract error | ✅ Complete |

## Deferred / Backlog Tests

| ID | Priority | Behavior | Expected Result | Status | Notes |
|---|---|---|---|---|---|
| P-008 | Medium | JSON primitive root | Contract decision / equivalent Python value | 📌 Deferred | Contract decision |
| P-009 | Low | Extremely large JSON document | Parses or fails gracefully | 📋 Backlog | Performance |
| P-010 | Low | Deeply nested JSON | Parses or fails gracefully | 📋 Backlog | Stress testing |
| P-011 | Low | Unexpected parser failure | Raises `ParserError` | 📋 Backlog | Requires mocking |

---

# YamlParser

## Active Test Cases

| ID | Priority | Behavior | Expected Result | Status |
|---|---|---|---|---|
| Y-001 | High | Valid YAML mapping | Returns `dict` | ✅ Complete |
| Y-002 | High | Valid YAML sequence | Returns `list` | ✅ Complete |
| Y-003 | High | Empty YAML mapping | Returns `{}` | ✅ Complete |
| Y-004 | High | Empty YAML sequence | Returns `[]` | ✅ Complete |
| Y-005 | High | Invalid UTF-8 | Raises `EncodingError` | ✅ Complete |
| Y-006 | High | Malformed YAML | Raises `YAMLSyntaxError` | ✅ Complete |
| Y-007 | Medium | Non-bytes input | Raises `ParserError` | ✅ Complete |
| Y-008 | Medium | Nested YAML structure | Preserves nested Python structure | ✅ Complete |
| Y-009 | Low | Scalar YAML value | Returns corresponding Python primitive | ✅ Complete |
| Y-010 | Low | Empty/comment-only document | Returns `None` | ✅ Complete |

## Deferred / Backlog Tests

None currently.

---

# ParserFactory

## Active Test Cases

| ID | Priority | Behavior | Expected Result | Status |
|---|---|---|---|---|
| F-001 | High | JSON resource as `str` | Returns `JsonParser` | ✅ Complete |
| F-002 | High | JSON resource as `Path` | Returns `JsonParser` | ✅ Complete |
| F-003 | High | Uppercase JSON extension | Returns `JsonParser` | ✅ Complete |
| F-004 | High | Unsupported extension | Raises `UnsupportedParserError` | ✅ Complete |
| F-005 | High | Missing extension | Raises `FactoryError` | ✅ Complete |
| F-006 | High | Invalid resource type | Raises `FactoryError` | ✅ Complete |
| F-007 | Medium | Register new parser | Registered parser is returned | ✅ Complete |
| F-008 | Medium | Extension without leading `.` | Normalizes and routes extension | ✅ Complete |
| F-009 | Low | Empty resource | Raises `FactoryError` | ✅ Complete |
| F/YF-001 | High | `.yaml` resource | Returns `YamlParser` | ✅ Complete |
| F/YF-002 | High | `.yml` resource | Returns `YamlParser` | ✅ Complete |
| F/YF-003 | High | Uppercase YAML extension | Returns `YamlParser` | ✅ Complete |

## Deferred / Backlog Tests

None currently.

---

# ConfigNormalizer

## Structural Contract

These tests establish the boundary between parser output and normalization.

| ID | Priority | Behavior | Expected Result | Status |
|---|---|---|---|---|
| N-001 | High | Valid configuration mapping | Returns mapping | ✅ Complete |
| N-002 | High | Empty mapping | Covered by structural tests / schema contract | ✅ Complete |
| N-003 | High | Nested mappings | Preserves nested structure | ✅ Complete |
| N-004 | High | Nested sequences | Preserves list structure | ✅ Complete |
| N-005 | High | Scalar values | Preserves value and Python type where accepted | ✅ Complete |
| N-006 | High | `None` root | Raises `ConfigurationInvalidError` | ✅ Complete |
| N-007 | High | Non-mapping root | Raises `ConfigurationInvalidError` | ✅ Complete |
| N-008 | High | Scalar root | Raises `ConfigurationInvalidError` | ✅ Complete |
| N-009 | High | Input immutability | Original input remains unchanged | ✅ Complete |
| N-010 | High | Exception hierarchy | Uses application exception hierarchy | ✅ Complete |

> The original structural contract was superseded by the canonical schema requirement that `port` is required. Tests now reflect the current normalizer contract.

## Canonical Schema & Field Validation

| ID | Priority | Behavior | Expected Result | Status |
|---|---|---|---|---|
| N-011 | High | Valid `port` supplied | Normalizes successfully and applies defaults | ✅ Complete |
| N-012 | High | Missing `port` | Raises `ConfigurationInvalidError` | ✅ Complete |
| N-013 | High | `port` below `1` | Raises `ConfigurationInvalidError` | ✅ Complete |
| N-014 | High | `port` above `65535` | Raises `ConfigurationInvalidError` | ✅ Complete |
| N-015 | High | `port` is not a strict integer | Raises `ConfigurationInvalidError` | ✅ Complete |
| N-016 | High | `port` is boolean | Raises `ConfigurationInvalidError` | ✅ Complete |
| N-017 | High | Missing `permit_root_login` | Defaults to `False` | ✅ Complete |
| N-018 | High | Missing `password_authentication` | Defaults to `False` | ✅ Complete |
| N-019 | High | Missing `protocol_version` | Defaults to `2` | ✅ Complete |
| N-020 | High | Missing `max_auth_tries` | Defaults to `3` | ✅ Complete |
| N-021 | High | Missing `allow_users` | Defaults to an independent empty list | ✅ Complete |
| N-032 | High | Invalid `permit_root_login` | Rejects non-boolean values | ✅ Complete |
| N-033 | High | Invalid `password_authentication` | Rejects non-boolean values | ✅ Complete |
| N-034 | High | Valid `protocol_version` | Strict value `2` normalizes successfully | ✅ Complete |
| N-035 | High | Invalid `protocol_version` | Rejects invalid type or value | ✅ Complete |
| N-036 | High | Valid `max_auth_tries` | Positive integer normalizes successfully | ✅ Complete |
| N-037 | High | Invalid `max_auth_tries` | Rejects non-integers and values less than `1` | ✅ Complete |

## Alias Resolution & Ambiguity Handling

| ID | Priority | Behavior | Expected Result | Status |
|---|---|---|---|---|
| N-022 | High | `listen_port` alias | Resolves to `port` | ✅ Complete |
| N-023 | High | `root_login` alias | Resolves to `permit_root_login` | ✅ Complete |
| N-024 | High | `password_auth` alias | Resolves to `password_authentication` | ✅ Complete |
| N-025 | High | `protocol` alias | Resolves to `protocol_version` | ✅ Complete |
| N-026 | High | `max_retries` alias | Resolves to `max_auth_tries` | ✅ Complete |
| N-027 | High | `allowed_users` alias | Resolves to `allow_users` | ✅ Complete |
| N-028 | High | Canonical field and alias conflict | Raises `ConfigurationInvalidError` | ✅ Complete |
| N-029 | High | Multiple aliases conflict | Raises `ConfigurationInvalidError` | ✅ Complete |
| N-030 | High | Multiple aliases have matching values | Normalizes successfully | ✅ Complete |
| N-031 | High | Canonical field and alias have matching values | Normalizes successfully | ✅ Complete |

> **Ambiguity rule:** Multiple representations of the same canonical field are accepted only when their values agree. Conflicting values raise `ConfigurationInvalidError`; the normalizer must not silently choose one value.

## `allow_users` Validation & Canonicalization

| ID | Priority | Behavior | Expected Result | Status |
|---|---|---|---|---|
| N-038 | High | Invalid `allow_users` container or items | Rejects non-lists and non-string items | ✅ Complete |
| N-039 | High | Empty username | Raises `ConfigurationInvalidError` | ✅ Complete |
| N-040 | High | Whitespace-only username | Raises `ConfigurationInvalidError` | ✅ Complete |
| N-041 | High | Surrounding whitespace | Usernames are trimmed | ✅ Complete |
| N-042 | High | Duplicate usernames | Deduplicates while preserving first-occurrence order | ✅ Complete |
| N-043 | High | Canonicalization immutability | Original input remains unchanged | ✅ Complete |

### `allow_users` Contract

```text
allow_users
    │
    ├── must be a list
    ├── every item must be a string
    ├── empty usernames are invalid
    ├── whitespace-only usernames are invalid
    ├── leading/trailing whitespace is trimmed
    ├── duplicate canonical usernames are removed
    └── first-occurrence order is preserved
```

## Sprint 2 Integration

| ID | Priority | Behavior | Expected Result | Status |
|---|---|---|---|---|
| N-044 | High | Equivalent JSON and YAML configurations | Produce equivalent canonical output | ✅ Complete |
| N-045 | Medium | Unknown configuration fields | Preserve unknown fields | ✅ Complete |
| N-046 | Medium | Full canonical configuration | Aliases, defaults, validation, canonicalization, and unknown-field preservation work together | ✅ Complete |

### Sprint 2 Result

All ConfigNormalizer backlog items through N-046 are complete.

The next planned component is `SecurityValidator`.

---

# SecurityValidator — Sprint 3

These tests are intentionally planned for the next development phase.

| ID | Priority | Behavior | Expected Result | Status |
|---|---|---|---|---|
| V-001 | High | Validate canonical configuration | Produces structured validation result | ⬜ Planned |
| V-002 | High | Security policy failure | Produces `FAIL` finding | ⬜ Planned |
| V-003 | High | Security policy success | Produces `PASS` finding | ⬜ Planned |
| V-004 | Medium | Warning condition | Produces `WARNING` finding | ⬜ Planned |

---

# Reporting — Sprint 4

| ID | Priority | Behavior | Expected Result | Status |
|---|---|---|---|---|
| RP-001 | Medium | Generate HTML report | Produces readable HTML | ⬜ Planned |
| RP-002 | Medium | Generate JSON report | Produces structured JSON | ⬜ Planned |
| RP-003 | Low | Generate CSV report | Produces tabular CSV | ⬜ Planned |

---

# Deferred / Backlog

The following items remain intentionally outside the completed Sprint 2 work:

- FileReader permission-denied tests requiring mocking.
- FileReader unexpected I/O failure simulation.
- JSON parser stress and performance tests.
- JSON primitive-root contract follow-up.
- Unexpected parser failure simulation.
- Security validation tests.
- Reporting tests.

## Current Next Step

The next feature branch should focus on the `SecurityValidator` contract and its first security-policy tests.
