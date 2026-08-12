import pytest
from pathlib import Path

from src.parsers.parser_factory import ParserFactory
from src.parsers.base_parser import BaseParser
from src.parsers.json_parser import JsonParser
from src.parsers.yaml_parser import YamlParser
from src.exceptions.factory_exceptions import FactoryError, UnsupportedParserError


@pytest.fixture(autouse=True)
def restore_registered_parsers():
    """Fixture to restore the original registered parsers after each test."""
    original_parsers = ParserFactory._registered_parsers.copy()
    yield
    ParserFactory._registered_parsers.clear()
    ParserFactory._registered_parsers.update(original_parsers)


def test_get_parser_returns_json_parser_for_string_path():
    """Returns a JsonParser instance for a .json file string path."""
    # Arrange
    resource = "config.json"

    # Act
    parser = ParserFactory.get_parser(resource)

    # Assert
    assert isinstance(parser, JsonParser)


def test_get_parser_returns_json_parser_for_path_object():
    """Returns a JsonParser instance for a Path object with a .json extension."""

    # Arrange
    resource = Path("config.json")

    # Act
    parser = ParserFactory.get_parser(resource)

    # Assert
    assert isinstance(parser, JsonParser)


def test_get_parser_handles_case_insensitive_extension():
    """Returns a JsonParser instance regardless of file extension case."""

    # Arrange
    resource = "config.JSON"

    # Act
    parser = ParserFactory.get_parser(resource)

    # Assert
    assert isinstance(parser, JsonParser)


def test_get_parser_raises_unsupported_parser_error_for_unsupported_extension():
    """Raises UnsupportedParserError for unsupported file extensions."""

    # Arrange
    resource = "config.ini"

    # Act
    with pytest.raises(UnsupportedParserError) as exc_info:
        ParserFactory.get_parser(resource)

    exception = exc_info.value

    # Assert
    assert exception.extension == ".ini"
    assert exception.resource == "config.ini"
    assert "No parser registered for file extension" in str(exception)

    
def test_get_parser_raises_factory_error_for_missing_extension():
    """Raises FactoryError when the resource has no file extension."""

    # Arrange
    resource = "config"

    # Act
    with pytest.raises(FactoryError) as exc_info:
        ParserFactory.get_parser(resource)

    exception = exc_info.value

    # Assert   
    assert "Resource target missing file extension" in str(exception)
    assert exception.resource == resource


def test_get_parser_raises_factory_error_for_hidden_file_without_extension():
    """Raises FactoryError when a hidden file has no detectable extension."""

    # Arrange
    resource = ".env"

    # Act
    with pytest.raises(FactoryError) as exc_info:
        ParserFactory.get_parser(resource)

    exception = exc_info.value

    # Assert
    assert "Resource target missing file extension" in str(exception)
    assert exception.resource == resource

def test_register_parser_allows_dynamic_extension_mapping():
    """Allows dynamic registration of new parsers for specific file extensions."""

    # Arrange
    class DummyParser(BaseParser):
        def parse(self, data: bytes):
            return {}

    extension = ".dummy"
    ParserFactory.register_parser(extension, DummyParser)

    # Act
    resource = "config.dummy"
    parser = ParserFactory.get_parser(resource)

    # Assert
    assert isinstance(parser, DummyParser)


def test_register_parser_normalizes_extension_without_leading_dot():
    """Verifies that register_parser automatically prepends a leading dot to extensions."""
    
    class DummyYamlParser(BaseParser):
        def parse(self, data: bytes):
            return {"format": "yaml"}

    # Act
    ParserFactory.register_parser("yaml", DummyYamlParser)

    # Assert
    parser = ParserFactory.get_parser("config.yaml")
    assert isinstance(parser, DummyYamlParser)


@pytest.mark.parametrize("invalid_resource_type", [
    12345,                           # Integer
    12.34,                           # Float
    ["config", "settings.json"],     # List
    {"path": "settings.json"},       # Dictionary
    object(),                        # Generic Object Instance
])
def test_get_parser_raises_factory_error_for_invalid_resource_types(invalid_resource_type):
    """
    Verifies that get_parser raises a FactoryError when provided with 
    data types that cannot be converted into a valid file path.
    """
    with pytest.raises(FactoryError) as exc_info:
        ParserFactory.get_parser(invalid_resource_type)

    exception = exc_info.value

    assert "Invalid resource type" in str(exception)
    assert type(invalid_resource_type).__name__ in str(exception )
    assert exception.resource is None

@pytest.mark.parametrize("resource_path", [
    pytest.param("config.yaml", id="F/YF-001"),
    pytest.param("config.yml", id="F/YF-002"),
    pytest.param("CONFIG.YAML", id="F/YF-003"),
])
def test_get_parser_dispatches_yaml_parser(resource_path):
    """Returns a YamlParser for suported YAML extensions."""

    # Act
    parser = ParserFactory.get_parser(resource_path)

    # Assert
    assert isinstance(parser, YamlParser)
    assert isinstance(parser, BaseParser)
