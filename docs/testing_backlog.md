# Testing Backlog

This document tracks the planned and deferred test cases for each
project component. Test cases are organized by component and priority to
support incremental development and test-driven design.

------------------------------------------------------------------------

# FileReader

## Active Test Cases

  -----------------------------------------------------------------------------------
    ID     Priority  Behavior       Expected Result                          Status
  ------- ---------- -------------- -------------------------------------- ----------
   R-001     High    Read existing  Returns file contents as `bytes`           ✅
                     file                                                   Complete

   R-002     High    File does not  Raises `FileNotFoundError` (or project     ✅
                     exist          exception)                              Complete

   R-003     High    Path is a      Raises project exception                   ✅
                     directory                                              Complete

   R-004     High    Empty file     Returns `b""`                              ✅
                                                                            Complete
  -----------------------------------------------------------------------------------

## Deferred Tests

  ----------------------------------------------------------------------------------
    ID     Priority  Behavior           Expected Result       Status   Notes
  ------- ---------- ------------------ ------------------- ---------- -------------
   R-005    Medium   Permission denied  Raises project          📌     Requires
                                        exception            Deferred  mocking

   R-006    Medium   Unexpected I/O     Raises project          📌     Requires
                     failure            exception            Deferred  mocking
  ----------------------------------------------------------------------------------

------------------------------------------------------------------------

# JsonParser

## Active Test Cases

  ---------------------------------------------------------------------------------------
    ID     Priority  Behavior              Expected Result       Status   Notes
  ------- ---------- --------------------- ------------------- ---------- ---------------
   P-001     High    Parse valid JSON      Returns Python          ✅     Happy path
                     object                `dict`               Complete  

   P-002     High    Parse valid JSON      Returns Python          ✅     Supports array
                     array                 `list`               Complete  root

   P-003     High    Parse empty JSON      Returns empty           ✅     Structural
                     object (`{}`)         `dict`               Complete  boundary

   P-004     High    Parse empty JSON      Returns empty           ✅     Structural
                     array (`[]`)          `list`               Complete  boundary

   P-005     High    Invalid UTF-8 byte    Raises                  ✅     Exception
                     stream                `EncodingError`      Complete  translation

   P-006     High    Malformed JSON syntax Raises                  ✅     Exception
                                           `JSONSyntaxError`    Complete  translation

   P-007    Medium   Non-bytes input       Raises `TypeError`      ✅     Public API
                                                                Complete  contract
  ---------------------------------------------------------------------------------------

## Deferred Tests

  -------------------------------------------------------------------------------------------
    ID     Priority  Behavior                Expected Result   Status   Notes
  ------- ---------- ----------------------- --------------- ---------- ---------------------
   P-008    Medium   Parse JSON primitive    Returns             📌     Decide whether all
                     (`true`, `42`,          equivalent       Deferred  JSON root types are
                     `"hello"`, `null`)      Python value               supported

   P-009     Low     Extremely large JSON    Successfully    📌 Backlog Performance testing
                     document                parses                     

   P-010     Low     Deeply nested JSON      Parses          📌 Backlog Stress testing
                                             correctly or               
                                             fails                      
                                             gracefully                 

   P-011     Low     Unexpected parser       Raises          📌 Backlog Requires mocking
                     failure                 `ParserError`              
  -------------------------------------------------------------------------------------------

------------------------------------------------------------------------

# ParserFactory

## Active Test Cases

  --------------------------------------------------------------------------------------------------
    ID     Priority  Behavior               Expected Result              Status   Notes
  ------- ---------- ---------------------- -------------------------- ---------- ------------------
   F-001     High    JSON resource as `str` Returns `JsonParser`           ✅     Happy path
                                                                        Complete  

   F-002     High    JSON resource as       Returns `JsonParser`           ✅     Path input
                     `Path`                                             Complete  

   F-003     High    Uppercase extension    Returns `JsonParser`           ✅     Case-insensitive
                     (`CONFIG.JSON`)                                    Complete  lookup

   F-004     High    Unsupported extension  Raises                         ✅     Exception
                                            `UnsupportedParserError`    Complete  translation

   F-005     High    Missing extension      Raises `FactoryError`          ✅     Invalid resource
                                                                        Complete  

   F-006     High    Invalid resource type  Raises `FactoryError`          ✅     Public API
                                                                        Complete  contract

   F-007    Medium   Register new parser    Returns registered parser      ✅     Registry
                                                                        Complete  extensibility

   F-008    Medium   Register extension     Normalizes extension and       ✅     API convenience
                     without leading `.`    returns parser              Complete  

   F-009     Low     Empty resource         Raises `FactoryError`          ✅     Input validation
                                                                        Complete  
  --------------------------------------------------------------------------------------------------

## Deferred Tests

*None currently.*

------------------------------------------------------------------------

# YamlParser

## Active Test Cases

  -------------------------------------------------------------------------------------------
    ID     Priority  Behavior            Expected Result        Status   Notes
  ------- ---------- ------------------- -------------------- ---------- --------------------
   Y-001     High    Valid YAML mapping  Returns `dict`           ✅     Happy path
                                                               Complete  

   Y-002     High    Valid YAML sequence Returns `list`           ✅     Supports sequence
                                                               Complete  root

   Y-003     High    Empty YAML mapping  Returns empty `dict`     ✅     Structural boundary
                     `{}`                                      Complete  

   Y-004     High    Empty YAML sequence Returns empty `list`     ✅     Structural boundary
                     `[]`                                      Complete  

   Y-005     High    Invalid UTF-8       Raises                   ✅     Exception
                                         `EncodingError`       Complete  translation

   Y-006     High    Malformed YAML      Raises                   ✅     Exception
                                         `YAMLSyntaxError`     Complete  translation

   Y-007    Medium   Non-bytes input     Raises `ParserError`     ✅     Follows existing
                                                               Complete  parser contract

   Y-008    Medium   Nested YAML         Preserves nested         ✅     Structural
                     structure           Python structure      Complete  preservation

   Y-009     Low     Scalar YAML value   Returns                  ✅     Contract decision
                                         corresponding Python  Complete  made
                                         primitive                       

   Y-010     Low     Empty               Returns `None`           ✅     Contract decision
                     YAML/comment-only                         Complete  made
  -------------------------------------------------------------------------------------------

------------------------------------------------------------------------

# ConfigNormalizer

## Structural Contract

  ------------------------------------------------------------------------------------------------
         ID            Priority     Behavior        Expected Result                    Status
  ---------------- ---------------- --------------- ----------------------------- ----------------
       N-001             High       Valid           Returns mapping                      ✅
                                    configuration                                 
                                    mapping                                       

       N-002             High       Empty mapping   Returns empty mapping                ✅

       N-003             High       Nested mappings Preserves nested structure           ✅

       N-004             High       Nested          Preserves list structure             ✅
                                    sequences                                     

       N-005             High       Scalar values   Preserves value and Python           ✅
                                                    type                          

       N-006             High       `None` root     Raises                               ✅
                                                    `ConfigurationInvalidError`   

       N-007             High       Non-mapping     Raises                               ✅
                                    root            `ConfigurationInvalidError`   

       N-008             High       Scalar root     Raises                               ✅
                                                    `ConfigurationInvalidError`   

       N-009             High       Input           Original input remains               ✅
                                    immutability    unchanged                     

       N-010             High       Exception       Follows application exception        ✅
                                    hierarchy       hierarchy                     
  ------------------------------------------------------------------------------------------------

> Parameterized pytest cases may produce multiple test cases from a
> single behavior ID. The backlog IDs represent behavior contracts, not
> individual pytest node IDs.

## Canonical Schema and Field Mapping

  -------------------------------------------------------------------------------------
         ID            Priority     Behavior          Expected Result       Status
  ---------------- ---------------- ----------------- ---------------- ----------------
       N-011             High       Define canonical  Canonical fields        🟡
                                    schema            and types        
                                                      documented       

       N-012             High       Define required   Required fields         ⬜
                                    fields            documented       

       N-013             High       Define optional   Optional                ⬜
                                    fields/defaults   behavior         
                                                      documented       

       N-014             High       Define field      Source aliases          ⬜
                                    aliases           map to canonical 
                                                      fields           

       N-015             High       Normalize mapped  Produces                ⬜
                                    fields            canonical        
                                                      representation   

       N-016             High       JSON/YAML         Equivalent              ⬜
                                    equivalence       inputs produce   
                                                      equivalent       
                                                      canonical output 
  -------------------------------------------------------------------------------------

> Canonical field names, aliases, types, and defaults must be defined
> before implementation tests are written. They should not be inferred
> from parser fixtures.

------------------------------------------------------------------------

# Status Legend

  -----------------------------------------------------------------------
    Symbol    Meaning
  ----------- -----------------------------------------------------------
  ⬜ Planned  Test has been identified but not yet implemented

  ✅ Complete Test implemented and passing

  📌 Deferred Intentionally postponed until prerequisite work is complete

  📌 Backlog  Future enhancement or lower-priority test
  -----------------------------------------------------------------------
