# src/exceptions/reader_exceptions.py

from src.exceptions.base_exception import SecurityConfigurationInspectorError

class ReaderError(SecurityConfigurationInspectorError):
    """Base exception for all configuration ingestion operations.
    
    Handles the centralized storage of metadata context (resource and operation)
    and acts as the base interceptor for orchestration layers.
    """
    def __init__(self, resource, operation="read", message=None):
        self.resource = resource
        self.operation = operation
        # If a concrete subclass doesn't provide a custom message, use a fallback standard
        self.message = message or f"Failed to perform '{operation}' operation on resource: {resource}"
        super().__init__(self.message)

class ResourceNotFoundError(ReaderError):
    """Raised when the targeted configuration resource cannot be found.
    
    Triggered when a local path does not exist on disk, a network endpoint 
    returns a 404, or an expected environment variable is missing.
    """
    def __init__(self, resource, operation="read"):
        custom_message = f"Failed to {operation} resource: File does not exist at '{resource}'"
        super().__init__(resource, operation, message=custom_message)

class AccessDeniedError(ReaderError):
    """Raised when the application lacks permission to access the resource.
    
    Triggered by OS-level permission blocks (e.g., trying to read a root-only 
    file), insufficient API token scopes, or authentication failures.
    """
    def __init__(self, resource, operation="read"):
        custom_message = f"Failed to {operation} resource: Permission denied for '{resource}'"
        super().__init__(resource, operation, message=custom_message)

class ResourceInvalidError(ReaderError):
    """Raised when the resource path target is fundamentally unusable.
    
    Triggered when the path points to an invalid object type (such as pointing 
    to a directory instead of a file), an invalid initialization type, or a broken symlink.
    """
    def __init__(self, resource, operation="read"):
        custom_message = f"Failed to {operation} resource: Target path or payload type is invalid: '{resource}'"
        super().__init__(resource, operation, message=custom_message)