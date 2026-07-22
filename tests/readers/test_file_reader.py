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

def test_read_raises_resource_not_found_for_missing_file():
    reader = FileReader()
    resource = "tests/resources/non_existent_file.txt"
    
    with pytest.raises(ResourceNotFoundError) as exc_info:
        reader.read(resource)

    assert exc_info.value.resource == resource
    assert exc_info.value.operation == "read"

def test_read_raises_resource_invalid_for_directory():
    reader = FileReader()
    resource = "tests/resources/folder"  # This should be a directory, not a file

    with pytest.raises(ResourceInvalidError) as exc_info:
        reader.read(resource)

    assert exc_info.value.resource == resource
    assert exc_info.value.operation == "read"


