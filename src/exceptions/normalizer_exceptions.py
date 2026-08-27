from typing import Any, Optional
from src.exceptions.base_exception import SecurityConfigurationInspectorError


class NormalizerError(SecurityConfigurationInspectorError):
    """Base exception for all configuration normalization operations.
    
    Captures the raw parsed payload that failed normalization to assist with
    downstream error reporting, triage, and telemetry.
    """

    def __init__(self, message: str, raw_payload: Optional[Any] = None):
        self.raw_payload = raw_payload
        super().__init__(message)


class ConfigurationInvalidError(NormalizerError):
    """Raised when the parsed configuration fails canonical root validation.
    
    Handles cases where the root payload is not a mapping (e.g., list, scalar)
    or when the document evaluates to None.
    """

    def __init__(self, message: str, raw_payload: Optional[Any] = None):
        super().__init__(message=message, raw_payload=raw_payload)