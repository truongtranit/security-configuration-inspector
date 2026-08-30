# Testing Backlog

This document tracks the planned, deferred, and completed test cases for
each project component. Test cases are organized by component and
priority to support incremental development and test-driven design.

------------------------------------------------------------------------

## Status Legend

   Symbol  Meaning
  -------- -------------
     ⬜    Planned
     🟡    In Progress
     ✅    Complete
     📌    Deferred
     📋    Backlog

------------------------------------------------------------------------

# FileReader

## Active Test Cases

  ------------------------------------------------------------------------------------
         ID            Priority     Behavior    Expected Result            Status
  ---------------- ---------------- ----------- --------------------- ----------------
       R-001             High       Read        Returns file contents   ✅ Complete
                                    existing    as `bytes`            
                                    file                              

       R-002             High       File does   Raises                  ✅ Complete
                                    not exist   `FileNotFoundError`   
                                                or project exception  

       R-003             High       Path is a   Raises project          ✅ Complete
                                    directory   exception             

       R-004             High       Empty file  Returns `b""`           ✅ Complete
  ------------------------------------------------------------------------------------

## Deferred Tests

  --------------------------------------------------------------------------------
        ID          Priority    Behavior     Expected        Status     Notes
                                             Result                     
  -------------- -------------- ------------ ----------- -------------- ----------
      R-005          Medium     Permission   Raises       📌 Deferred   Requires
                                denied       project                    mocking
                                             exception                  

      R-006          Medium     Unexpected   Raises       📌 Deferred   Requires
                                I/O failure  project                    mocking
                                             exception                  
  --------------------------------------------------------------------------------

------------------------------------------------------------------------

# JsonParser

## Active Test Cases

  ------------------------------------------------------------------------------------------
        ID          Priority    Behavior    Expected Result         Status     Notes
  -------------- -------------- ----------- ------------------- -------------- -------------
      P-001           High      Parse valid Returns Python       ✅ Complete   Happy path
                                JSON object `dict`                             

      P-002           High      Parse valid Returns Python       ✅ Complete   Supports
                                JSON array  `list`                             array root

      P-003           High      Parse empty Returns empty        ✅ Complete   Structural
                                JSON object `dict`                             boundary
                                (`{}`)                                         

      P-004           High      Parse empty Returns empty        ✅ Complete   Structural
                                JSON array  `list`                             boundary
                                (`[]`)                                         

      P-005           High      Invalid     Raises               ✅ Complete   Exception
                                UTF-8 byte  `EncodingError`                    translation
                                stream                                         

      P-006           High      Malformed   Raises               ✅ Complete   Exception
                                JSON syntax `JSONSyntaxError`                  translation

      P-007          Medium     Non-bytes   Raises parser        ✅ Complete   Public API
                                input       contract error                     contract
  ------------------------------------------------------------------------------------------

## Deferred / Backlog Tests

  ---------------------------------------------------------------------------------------
        ID          Priority    Behavior     Expected Result     Status     Notes
  -------------- -------------- ------------ --------------- -------------- -------------
      P-008          Medium     Parse JSON   Returns          📌 Deferred   Contract
                                primitive    equivalent                     decision
                                (`true`,     Python value                   
                                `42`,                                       
                                `"hello"`,                                  
                                `null`)                                     

      P-009           Low       Extremely    Successfully      📋 Backlog   Performance
                                large JSON   parses or fails                testing
                                document     gracefully                     

      P-010           Low       Deeply       Parses            📋 Backlog   Stress
                                nested JSON  correctly or                   testing
                                             fails                          
                                             gracefully                     

      P-011           Low       Unexpected   Raises            📋 Backlog   Requires
                                parser       `ParserError`                  mocking
                                failure                                     
  ---------------------------------------------------------------------------------------

------------------------------------------------------------------------

# YamlParser

## Active Test Cases

  ---------------------------------------------------------------------------------------------------
        ID          Priority    Behavior            Expected Result         Status     Notes
  -------------- -------------- ------------------- ------------------- -------------- --------------
      Y-001           High      Valid YAML mapping  Returns `dict`       ✅ Complete   Happy path

      Y-002           High      Valid YAML sequence Returns `list`       ✅ Complete   Supports
                                                                                       sequence root

      Y-003           High      Empty YAML mapping  Returns empty        ✅ Complete   Structural
                                (`{}`)              `dict`                             boundary

      Y-004           High      Empty YAML sequence Returns empty        ✅ Complete   Structural
                                (`[]`)              `list`                             boundary

      Y-005           High      Invalid UTF-8       Raises               ✅ Complete   Exception
                                                    `EncodingError`                    translation

      Y-006           High      Malformed YAML      Raises               ✅ Complete   Exception
                                                    `YAMLSyntaxError`                  translation

      Y-007          Medium     Non-bytes input     Raises               ✅ Complete   Existing
                                                    `ParserError`                      parser
                                                                                       contract

      Y-008          Medium     Nested YAML         Preserves nested     ✅ Complete   Structural
                                structure           Python structure                   preservation

      Y-009           Low       Scalar YAML value   Returns              ✅ Complete   Contract
                                                    corresponding                      decision
                                                    Python primitive                   

      Y-010           Low       Empty               Returns `None`       ✅ Complete   Contract
                                YAML/comment-only                                      decision
                                document                                               
  ---------------------------------------------------------------------------------------------------

## Deferred / Backlog Tests

*None currently.*

------------------------------------------------------------------------

# ParserFactory

## Active Test Cases

  ------------------------------------------------------------------------------------------------------------
        ID          Priority    Behavior          Expected Result                Status     Notes
  -------------- -------------- ----------------- -------------------------- -------------- ------------------
      F-001           High      JSON resource as  Returns `JsonParser`        ✅ Complete   Happy path
                                `str`                                                       

      F-002           High      JSON resource as  Returns `JsonParser`        ✅ Complete   Path input
                                `Path`                                                      

      F-003           High      Uppercase         Returns `JsonParser`        ✅ Complete   Case-insensitive
                                extension                                                   lookup
                                (`CONFIG.JSON`)                                             

      F-004           High      Unsupported       Raises                      ✅ Complete   Exception
                                extension         `UnsupportedParserError`                  translation

      F-005           High      Missing extension Raises `FactoryError`       ✅ Complete   Invalid resource

      F-006           High      Invalid resource  Raises `FactoryError`       ✅ Complete   Public API
                                type                                                        contract

      F-007          Medium     Register new      Returns registered parser   ✅ Complete   Registry
                                parser                                                      extensibility

      F-008          Medium     Extension without Normalizes extension and    ✅ Complete   API convenience
                                leading `.`       returns parser                            

      F-009           Low       Empty resource    Raises `FactoryError`       ✅ Complete   Input validation

     F/YF-001         High      `.yaml` resource  Returns `YamlParser`        ✅ Complete   YAML integration

     F/YF-002         High      `.yml` resource   Returns `YamlParser`        ✅ Complete   YAML integration

     F/YF-003         High      Uppercase YAML    Returns `YamlParser`        ✅ Complete   Case-insensitive
                                extension                                                   lookup
  ------------------------------------------------------------------------------------------------------------

## Deferred / Backlog Tests

*None currently.*

------------------------------------------------------------------------

# ConfigNormalizer

## Structural Contract

These tests establish the structural boundary between parser output and the normalization layer.

| ID | Priority | Behavior | Expected Result | Status |
|---|---|---|---|---|
| N-001 | High | Valid configuration mapping | Returns mapping | ✅ Complete |
| N-002 | High | Empty mapping | Returns empty mapping | ✅ Complete |
| N-003 | High | Nested mappings | Preserves nested structure | ✅ Complete |
| N-004 | High | Nested sequences | Preserves list structure | ✅ Complete |
| N-005 | High | Scalar values | Preserves value and Python type | ✅ Complete |
| N-006 | High | `None` root | Raises `ConfigurationInvalidError` | ✅ Complete |
| N-007 | High | Non-mapping root | Raises `ConfigurationInvalidError` | ✅ Complete |
| N-008 | High | Scalar root | Raises `ConfigurationInvalidError` | ✅ Complete |
| N-009 | High | Input immutability | Original input remains unchanged | ✅ Complete |
| N-010 | High | Exception hierarchy | Follows application exception hierarchy | ✅ Complete |

> **Note:** N-005 and N-008 use parameterized pytest cases. Backlog IDs represent behavior contracts rather than individual pytest node IDs.

---

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
| N-032 | High | Invalid `permit_root_login` | Rejects values that are not strict booleans | ✅ Complete |
| N-033 | High | Invalid `password_authentication` | Rejects values that are not strict booleans | ✅ Complete |
| N-034 | High | Valid `protocol_version` | Strict integer value `2` normalizes successfully | ✅ Complete |
| N-035 | High | Invalid `protocol_version` | Rejects invalid type or value | ✅ Complete |
| N-036 | High | Valid `max_auth_tries` | Positive integer normalizes successfully | ✅ Complete |
| N-037 | High | Invalid `max_auth_tries` | Rejects non-integers and values less than `1` | ✅ Complete |

---

## Alias Resolution & Ambiguity Handling

| ID | Priority | Behavior | Expected Result | Status |
|---|---|---|---|---|
| N-022 | High | `listen_port` alias | Resolves to canonical `port` | ✅ Complete |
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

---

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
    ├── Must be a list
    ├── Every item must be a string
    ├── Empty usernames are invalid
    ├── Whitespace-only usernames are invalid
    ├── Leading and trailing whitespace is trimmed
    ├── Duplicate canonical usernames are removed
    └── First-occurrence order is preserved
```

> **Canonicalization order:** Validate container and item types, reject blank usernames, trim surrounding whitespace, then deduplicate normalized values. This ensures `"  admin  "` and `"admin"` resolve to one canonical username.

---

## Sprint 2 Integration Backlog

| ID | Priority | Behavior | Expected Result | Status |
|---|---|---|---|---|
| N-044 | High | Equivalent JSON and YAML configurations | Produce equivalent canonical output | ✅ Complete |
| N-045 | Medium | Unknown configuration fields | Preserve, reject, or explicitly handle by contract | ✅ Complete |
| N-046 | Medium | Full canonical configuration | Aliases, defaults, validation, and canonicalization work together | ✅ Complete |

# Future: SecurityValidator

These tests belong to Sprint 3 and are intentionally not part of the
current Sprint 2 implementation.

  -------------------------------------------------------------------------------
         ID            Priority     Behavior        Expected          Status
                                                    Result       
  ---------------- ---------------- --------------- ------------ ----------------
       V-001             High       Validate        Produces        ⬜ Planned
                                    canonical       structured   
                                    configuration   validation   
                                                    result       

       V-002             High       Security policy Produces        ⬜ Planned
                                    failure         `FAIL`       
                                                    finding      

       V-003             High       Security policy Produces        ⬜ Planned
                                    success         `PASS`       
                                                    finding      

       V-004            Medium      Warning         Produces        ⬜ Planned
                                    condition       `WARNING`    
                                                    finding      
  -------------------------------------------------------------------------------

------------------------------------------------------------------------

# Future: Reporting

These tests belong to Sprint 4.

  --------------------------------------------------------------------------
         ID            Priority     Behavior   Expected          Status
                                               Result       
  ---------------- ---------------- ---------- ------------ ----------------
       RP-001           Medium      Generate   Produces        ⬜ Planned
                                    HTML       readable     
                                    report     HTML output  

       RP-002           Medium      Generate   Produces        ⬜ Planned
                                    JSON       structured   
                                    report     JSON output  

       RP-003            Low        Generate   Produces        ⬜ Planned
                                    CSV report tabular CSV  
                                               output       
  --------------------------------------------------------------------------

------------------------------------------------------------------------

# Deferred / Backlog

The following items are intentionally outside the current Sprint 2
implementation:

-   FileReader permission-denied tests requiring mocking.
-   FileReader unexpected I/O failure tests.
-   JSON parser stress and performance tests.
-   JSON primitive-root contract decision.
-   Unexpected parser failure simulation.
-   Security validation tests.
-   Reporting tests.
