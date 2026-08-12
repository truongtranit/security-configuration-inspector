from typing import Optional
from src.exceptions.base_exception import SecurityConfigurationInspectorError

class ParserError(SecurityConfigurationInspectorError):
    """Base exception for all configuration deserialization operations.
    
    Captures the raw binary payload that caused the failure to allow for
    downstream telemetry, error logging, or triage.
    """
    def __init__(self, message: str, raw_data: Optional[bytes] = None):
        self.raw_data = raw_data
        super().__init__(message)


class EncodingError(ParserError):
    """Raised when raw binary data fails text decoding (e.g., non-UTF-8 bytes)."""

    def __init__(self, encoding: str = "utf-8", raw_data: Optional[bytes] = None):
        self.encoding = encoding
        message = f"Failed to decode byte stream using '{encoding}' encoding."
        super().__init__(message=message, raw_data=raw_data)


class JSONSyntaxError(ParserError):
    """Raised when text content contains invalid JSON syntax."""

    def __init__(self, lineno: int, colno: int, msg: str, raw_data: Optional[bytes] = None):
        self.lineno = lineno
        self.colno = colno
        self.msg = msg
        message = f"Invalid JSON syntax at line {lineno}, column {colno}: {msg}"
        super().__init__(message=message, raw_data=raw_data)


class YAMLSyntaxError(ParserError):
    """Raised when text content contains invalid YAML syntax."""

    def __init__(self, msg: str, raw_data: Optional[bytes] = None):
        self.msg = msg
        message = f"Invalid YAML syntax: {msg}"
        super().__init__(message=message, raw_data=raw_data)

    