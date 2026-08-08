from src.exceptions.base_exception import SecurityConfigurationInspectorError

class FactoryError(SecurityConfigurationInspectorError):
    """Base exception for all factory dispatch operations."""
    def __init__(self, message: str, resource: str = None):
        self.resource = resource
        self.message = message
        super().__init__(self.message)

class UnsupportedParserError(FactoryError):
    """Raised when no parser is registered for the resource extension."""
    def __init__(self, resource: str, extension: str):
        self.extension = extension
        message = f"No parser registered for file extension '{extension}' in resource: '{resource}'"
        super().__init__(message=message, resource=resource)
