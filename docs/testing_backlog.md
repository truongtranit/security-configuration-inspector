# Testing Backlog

## FileReader

| ID | Priority | Test | Status | Reason |
|----|----------|------|--------|--------|
| T-005 | Medium | Permission denied | Backlog | Waiting to learn mocking |
| T-006 | Medium | Unexpected I/O failure | Backlog | Waiting to learn mocking |

## JsonParser

| ID | Priority | Test | Status | Reason |
|----|----------|------|--------|--------|
| T-007 | High | Invalid UTF-8 | Backlog | Parser not implemented |
| T-008 | High | Malformed JSON | Backlog | Parser not implemented |

|     ID    | Priority | Behavior                                               | Expected Result                                         |    Status   | Notes                                       |
| :-------: | :------: | ------------------------------------------------------ | ------------------------------------------------------- | :---------: | ------------------------------------------- |
| **P-001** |   High   | Parse a valid JSON object                              | Returns the corresponding Python `dict`                 |  ⬜ Planned  | Happy path                                  |
| **P-002** |   High   | Parse a valid JSON array                               | Returns the corresponding Python `list`                 |  ⬜ Planned  | Confirms parser accepts any valid JSON root |
| **P-003** |   High   | Parse an empty JSON object (`{}`)                      | Returns an empty `dict`                                 |  ⬜ Planned  | Edge case                                   |
| **P-004** |   High   | Parse an empty JSON array (`[]`)                       | Returns an empty `list`                                 |  ⬜ Planned  | Edge case                                   |
| **P-005** |   High   | Invalid UTF-8 byte stream                              | Raises `EncodingError`                                  |  ⬜ Planned  | Exception translation                       |
| **P-006** |   High   | Malformed JSON syntax                                  | Raises `JSONSyntaxError`                                |  ⬜ Planned  | Exception translation                       |
| **P-007** |  Medium  | Non-bytes input                                        | Raises `TypeError` (or `ParserError`, depending on API) |  ⬜ Planned  | Validate public contract                    |
| **P-008** |  Medium  | Parse JSON primitive (`true`, `42`, `"hello"`, `null`) | Returns equivalent Python value                         | 📌 Deferred | Decide if parser supports all JSON roots    |
| **P-009** |    Low   | Extremely large JSON document                          | Successfully parses without errors                      |  📌 Backlog | Performance / stress testing                |
| **P-010** |    Low   | Deeply nested JSON                                     | Parses correctly or fails gracefully                    |  📌 Backlog | Stress testing                              |
| **P-011** |    Low   | Unexpected parser failure                              | Raises `ParserError`                                    |  📌 Backlog | Requires mocking                            |


| ID        | Behavior                | Why it exists                                                     |
| --------- | ----------------------- | ----------------------------------------------------------------- |
| **P-003** | Parse empty JSON object | Verify object structural boundary and preserve empty dictionaries |
| **P-004** | Parse empty JSON array  | Verify array structural boundary and preserve empty lists         |
