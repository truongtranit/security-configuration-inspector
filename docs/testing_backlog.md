# Testing Backlog

This document tracks the planned and deferred test cases for each project component. Test cases are organized by component and priority to support incremental development and test-driven design.

---

# FileReader

## Active Test Cases

|   ID  | Priority | Behavior            | Expected Result                                   |   Status   |
| :---: | :------: | ------------------- | ------------------------------------------------- | :--------: |
| R-001 |   High   | Read existing file  | Returns file contents as `bytes`                  | ✅ Complete |
| R-002 |   High   | File does not exist | Raises `FileNotFoundError` (or project exception) | ✅ Complete |
| R-003 |   High   | Path is a directory | Raises project exception                          | ✅ Complete |
| R-004 |   High   | Empty file          | Returns `b""`                                     | ✅ Complete |

## Deferred Tests

|   ID  | Priority | Behavior               | Expected Result          |    Status   | Notes            |
| :---: | :------: | ---------------------- | ------------------------ | :---------: | ---------------- |
| R-005 |  Medium  | Permission denied      | Raises project exception | 📌 Deferred | Requires mocking |
| R-006 |  Medium  | Unexpected I/O failure | Raises project exception | 📌 Deferred | Requires mocking |

---

# JsonParser

## Active Test Cases

|   ID  | Priority | Behavior                       | Expected Result          |   Status   | Notes                 |
| :---: | :------: | ------------------------------ | ------------------------ | :--------: | --------------------- |
| P-001 |   High   | Parse valid JSON object        | Returns Python `dict`    | ✅ Complete | Happy path            |
| P-002 |   High   | Parse valid JSON array         | Returns Python `list`    | ✅ Complete | Supports array root   |
| P-003 |   High   | Parse empty JSON object (`{}`) | Returns empty `dict`     | ✅ Complete | Structural boundary   |
| P-004 |   High   | Parse empty JSON array (`[]`)  | Returns empty `list`     | ✅ Complete | Structural boundary   |
| P-005 |   High   | Invalid UTF-8 byte stream      | Raises `EncodingError`   | ✅ Complete | Exception translation |
| P-006 |   High   | Malformed JSON syntax          | Raises `JSONSyntaxError` | ✅ Complete | Exception translation |
| P-007 |  Medium  | Non-bytes input                | Raises `TypeError`       | ✅ Complete | Public API contract   |

## Deferred Tests

|   ID  | Priority | Behavior                                               | Expected Result                      |    Status   | Notes                                            |
| :---: | :------: | ------------------------------------------------------ | ------------------------------------ | :---------: | ------------------------------------------------ |
| P-008 |  Medium  | Parse JSON primitive (`true`, `42`, `"hello"`, `null`) | Returns equivalent Python value      | 📌 Deferred | Decide whether all JSON root types are supported |
| P-009 |    Low   | Extremely large JSON document                          | Successfully parses                  |  📌 Backlog | Performance testing                              |
| P-010 |    Low   | Deeply nested JSON                                     | Parses correctly or fails gracefully |  📌 Backlog | Stress testing                                   |
| P-011 |    Low   | Unexpected parser failure                              | Raises `ParserError`                 |  📌 Backlog | Requires mocking                                 |

---

# ParserFactory

## Active Test Cases

|   ID  | Priority | Behavior                               | Expected Result                         |   Status    | Notes                   |
| :---: | :------: | -------------------------------------- | --------------------------------------- | :-------:   | ----------------------- |
| F-001 |   High   | JSON resource as `str`                 | Returns `JsonParser`                    | ✅ Complete | Happy path              |
| F-002 |   High   | JSON resource as `Path`                | Returns `JsonParser`                    | ✅ Complete | Path input              |
| F-003 |   High   | Uppercase extension (`CONFIG.JSON`)    | Returns `JsonParser`                    | ✅ Complete | Case-insensitive lookup |
| F-004 |   High   | Unsupported extension                  | Raises `UnsupportedParserError`         | ✅ Complete | Exception translation   |
| F-005 |   High   | Missing extension                      | Raises `FactoryError`                   | ✅ Complete | Invalid resource        |
| F-006 |   High   | Invalid resource type                  | Raises `FactoryError`                   | ✅ Complete | Public API contract     |
| F-007 |  Medium  | Register new parser                    | Returns registered parser               | ✅ Complete | Registry extensibility  |
| F-008 |  Medium  | Register extension without leading `.` | Normalizes extension and returns parser | ✅ Complete | API convenience         |
| F-009 |    Low   | Empty resource                         | Raises `FactoryError`                   | ✅ Complete | Input validation        |

## Deferred Tests

*None currently.*

---

# YamlParser

## Active Test Cases

|   ID  | Priority | Behavior                 | Expected Result                   |   Status   | Notes                            |
| :---: | :------: | ------------------------ | --------------------------------- | :--------: | -------------------------------- |
| Y-001 |   High   | Valid YAML mapping       | Returns `dict`                    | ✅ Complete | Happy path                       |
| Y-002 |   High   | Valid YAML sequence      | Returns `list`                    | ✅ Complete | Supports sequence root           |
| Y-003 |   High   | Empty YAML mapping `{}`  | Returns empty `dict`              | ✅ Complete | Structural boundary              |
| Y-004 |   High   | Empty YAML sequence `[]` | Returns empty `list`              | ✅ Complete | Structural boundary              |
| Y-005 |   High   | Invalid UTF-8            | Raises `EncodingError`            |  ✅ Complete | Exception translation            |
| Y-006 |   High   | Malformed YAML           | Raises `YAMLSyntaxError`          |  ✅ Complete | Exception translation            |
| Y-007 |  Medium  | Non-bytes input          | Raises `ParserError`              |  ✅ Complete | Follows existing parser contract |
| Y-008 |  Medium  | Nested YAML structure    | Preserves nested Python structure |  ✅ Complete | Structural preservation          |
| Y-009 |    Low   | Scalar YAML value        | Returns corresponding Python primitive   |  ✅ Complete | Contract decision made       |
| Y-010 |    Low   | Empty YAML/comment-only     | Returns `None`   |  ✅ Complete | Contract decision made       |


---

# Next Component

ConfigNormalizer

Status: ⬜ Planned

---

# Status Legend

|    Symbol   | Meaning                                                     |
| :---------: | ----------------------------------------------------------- |
| ⬜ Planned  | Test has been identified but not yet implemented            |
| ✅ Complete | Test implemented and passing                                |
| 📌 Deferred | Intentionally postponed until prerequisite work is complete |
| 📌 Backlog | Future enhancement or lower-priority test                   |
