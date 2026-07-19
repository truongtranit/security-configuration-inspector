from abc import ABC, abstractmethod

class BaseReader(ABC):
    """Abstract Base Class defining the contract for all configuration readers."""

    @abstractmethod
    def read(self, resource: str) -> bytes:

        """Reads raw binary content from a given source location.

        Args:
            resource: The identifier or path of the resource.

        Returns:
            bytes: The raw, unmodified binary data.
            
        Raises:
            ReaderError: If any read operation fails.
        """
        ...