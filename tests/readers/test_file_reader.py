import pytest
from pathlib import Path
from src.readers.file_reader import FileReader
from src.exceptions.reader_exceptions import (
    ReaderError,
    ResourceNotFoundError,
    AccessDeniedError,
    ResourceInvalidError,
)

def test_read_returns_raw_bytes_for_valid_file():
    # Arrange
    reader = FileReader()
    resource = "tests/resources/valid.txt"

    # Act
    result = reader.read(resource)

    # Assert
    assert result == b"Hello FileReader!"

def test_read_returns_empty_bytes_for_empty_file():
    reader = FileReader()
    resource = "tests/resources/empty.txt"

    result = reader.read(resource)

    assert result == b""



def test_read_raises_resource_not_found_for_missing_file():
    reader = FileReader()
    resource = Path("tests/resources/non_existent_file.txt")
    
    with pytest.raises(ResourceNotFoundError) as exc_info:
        reader.read(str(resource))

    exception = exc_info.value

    assert exception.resource == resource
    assert exception.operation == "read"


def test_read_raises_resource_invalid_for_directory():
    reader = FileReader()
    resource = Path("tests/resources/folder")  # This should be a directory, not a file

    with pytest.raises(ResourceInvalidError) as exc_info:
        reader.read(str(resource))

    exception = exc_info.value
    
    assert exception.resource == resource
    assert exception.operation == "read"


# Pin it down and get back to it later.
def test_read_raises_access_denied_for_permission_error():
    ...

def test_read_raises_reader_error_for_unexpected_io_failure():
    ...
