from pathlib import Path
from src.readers.base_reader import BaseReader
from src.exceptions.reader_exceptions import (
    ReaderError,
    ResourceNotFoundError,
    AccessDeniedError,
    ResourceInvalidError,
)

class FileReader(BaseReader):
    """Concrete implementation of BaseReader designed for local disk file system operations."""

    def read(self, resource: str) -> bytes:
        """Reads the raw binary bytes of a file from the local disk.

        Args:
            resource: The string file path to read.

        Returns:
            bytes: The raw binary content of the file.

        Raises:
            ResourceNotFoundError: If the file does not exist.
            AccessDeniedError: If permission to read the file is denied.
            ResourceInvalidError: If the path is a directory or invalid target.
            ReaderError: For any other unhandled I/O failures.
        """
        
        
        try:
            path: Path = Path(resource)
            return path.read_bytes()
            
        except FileNotFoundError as e:
            raise ResourceNotFoundError(resource=path, operation="read") from e
            
        except PermissionError as e:
            raise AccessDeniedError(resource=path, operation="read") from e
            
        except IsADirectoryError as e:
            raise ResourceInvalidError(resource=path, operation="read") from e
            
        except OSError as e:
            # Fallback wrapper for raw OS errors, bad symlinks, etc.
            raise ReaderError(resource=path, operation="read", message=
                f"An unexpected storage error occurred reading '{resource}': {str(e)}"
            ) from e