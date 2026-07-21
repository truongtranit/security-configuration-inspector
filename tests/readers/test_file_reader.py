from pathlib import Path

from src.readers.file_reader import FileReader

def test_read_returns_raw_bytes_for_valid_file():
    # Arrange
    reader = FileReader()
    resource = Path("tests/resources/valid.txt")

    # Act
    result = reader.read(str(resource))

    # Assert
    assert result == b"Hello FileReader!"