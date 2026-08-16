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

These tests establish the current structural contract between parser
output and the validation layer.

  ------------------------------------------------------------------------------------------------
         ID            Priority     Behavior        Expected Result                    Status
  ---------------- ---------------- --------------- ----------------------------- ----------------
       N-001             High       Valid           Returns mapping                 ✅ Complete
                                    configuration                                 
                                    mapping                                       

       N-002             High       Empty mapping   Returns empty mapping           ✅ Complete

       N-003             High       Nested mappings Preserves nested structure      ✅ Complete

       N-004             High       Nested          Preserves list structure        ✅ Complete
                                    sequences                                     

       N-005             High       Scalar values   Preserves value and Python      ✅ Complete
                                                    type                          

       N-006             High       `None` root     Raises                          ✅ Complete
                                                    `ConfigurationInvalidError`   

       N-007             High       Non-mapping     Raises                          ✅ Complete
                                    root            `ConfigurationInvalidError`   

       N-008             High       Scalar root     Raises                          ✅ Complete
                                                    `ConfigurationInvalidError`   

       N-009             High       Input           Original input remains          ✅ Complete
                                    immutability    unchanged                     

       N-010             High       Exception       Follows application exception   ✅ Complete
                                    hierarchy       hierarchy                     
  ------------------------------------------------------------------------------------------------

> **Note:** N-005 and N-008 use parameterized pytest cases. The backlog
> IDs represent behavior contracts rather than individual pytest node
> IDs.

## Canonical Schema & Field Mapping

These are the remaining Sprint 2 normalization behaviors.

  ---------------------------------------------------------------------------------------------------
        ID          Priority    Behavior          Expected Result      Status     Notes
  -------------- -------------- ----------------- ---------------- -------------- -------------------
      N-011           High      Define canonical  Canonical fields 🟡 In Progress Design decision
                                schema            and types are                   required
                                                  documented                      

      N-012           High      Define required   Required fields    ⬜ Planned   Depends on N-011
                                fields            are explicitly                  
                                                  documented                      

      N-013           High      Define optional   Optional           ⬜ Planned   Depends on N-011
                                fields/defaults   behavior is                     
                                                  explicitly                      
                                                  documented                      

      N-014           High      Define field      Source aliases     ⬜ Planned   Depends on N-011
                                aliases           map to canonical                
                                                  fields                          

      N-015           High      Normalize mapped  Produces           ⬜ Planned   Depends on
                                fields            canonical                       N-011--N-014
                                                  representation                  

      N-016           High      JSON/YAML         Equivalent         ⬜ Planned   Integration-level
                                equivalence       JSON/YAML inputs                normalization test
                                                  produce                         
                                                  equivalent                      
                                                  canonical output                
  ---------------------------------------------------------------------------------------------------

> **Design rule:** Canonical field names, aliases, types, and defaults
> must be defined before implementation tests are written. They should
> not be inferred from parser fixtures.

------------------------------------------------------------------------

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
