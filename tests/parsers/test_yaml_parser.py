import pytest
from src.parsers.yaml_parser import YamlParser
from src.exceptions.parser_exceptions import (
    ParserError,
    EncodingError,
    YAMLSyntaxError,
)

@pytest.fixture
def parser():
    """Fixture to provide a fresh YamlParser instance for each test."""
    return YamlParser()


def test_parse_returns_dict_for_valid_yaml_mapping(parser):
    """Test that valid YAML representing a dictionary is parsed correctly."""

    # Arrange
    raw_bytes = b"service:\n  name: inspector\n  enabled: true\n"

    # Act
    result = parser.parse(raw_bytes)

    # Assert
    assert result == {"service": {"name": "inspector", "enabled": True}}
    assert isinstance(result, dict)


def test_parse_returns_list_for_valid_yaml_sequence(parser):
    """Test that valid YAML representing a list is parsed correctly."""

    # Arrange
    raw_bytes = b"- firewall\n- ssh\n- logging\n"

    # Act
    result = parser.parse(raw_bytes)

    # Assert
    assert result == ["firewall", "ssh", "logging"]
    assert isinstance(result, list)

def test_parse_returns_empty_dict_for_empty_yaml_mapping(parser):
    """Test that an empty YAML mapping is parsed as an empty dictionary."""

    # Arrange
    raw_bytes = b"{}\n"

    # Act
    result = parser.parse(raw_bytes)

    # Assert
    assert result == {}
    assert isinstance(result, dict)

def test_parse_returns_empty_list_for_empty_yaml_sequence(parser):
    """Test that an empty YAML sequence is parsed as an empty list."""

    # Arrange
    raw_bytes = b"[]\n"

    # Act
    result = parser.parse(raw_bytes)

    # Assert
    assert result == []
    assert isinstance(result, list)

def test_parse_raises_encoding_error_for_invalid_utf8_bytes(parser):
    """Test that invalid UTF-8 bytes raise an EncodingError."""

    # Arrange
    invalid_utf8_bytes = b"\x80\x81\x82"

    # Act
    with pytest.raises(EncodingError) as exc_info:
        parser.parse(invalid_utf8_bytes)

    exception = exc_info.value

    # Assert
    assert exception.encoding == "utf-8"
    assert exception.raw_data == invalid_utf8_bytes
    assert isinstance(exception, ParserError)

def test_parse_raises_yaml_syntax_error_for_malformed_yaml(parser):
    """Test that malformed YAML raises a YAMLSyntaxError."""

    # Arrange
    malformed_yaml_bytes = b"service:\n  name: inspector\n  enabled: true\n  - invalid"

    # Act
    with pytest.raises(YAMLSyntaxError) as exc_info:
        parser.parse(malformed_yaml_bytes)

    exception = exc_info.value

    # Assert
    assert "Invalid YAML syntax" in str(exception)
    assert exception.raw_data == malformed_yaml_bytes
    assert isinstance(exception, ParserError)
    
@pytest.mark.parametrize("invalid_input", [
    "server: localhost",  # str instead of bytes
    12345,                # int
    None,                 # NoneType
    ["raw_list"],         # list
])
def test_parse_raises_parser_error_for_non_bytes_input(parser, invalid_input):
    """Test that non-bytes input raises a ParserError."""

    # Act
    with pytest.raises(ParserError) as exc_info:
        parser.parse(invalid_input)

    exception = exc_info.value

    # Assert
    assert f"YamlParser expected bytes, got '{type(invalid_input).__name__}'" in str(exception)
    assert exception.raw_data is None

def test_parse_preserves_nested_python_structures(parser):
    """Test that nested YAML structures are parsed correctly into Python objects."""

    # Arrange
    nested_yaml_bytes = (
        b"network:\n"
        b"  firewall:\n"
        b"    rules:\n"
        b"      - port: 80\n"
        b"        allow: true\n"
        b"      - port: 22\n"
        b"        allow: false\n"
    )
    expected_result = {
        "network": {
            "firewall": {
                "rules": [
                    {"port": 80, "allow": True},
                    {"port": 22, "allow": False},
                ]
            }
        }
    }

    # Act
    result = parser.parse(nested_yaml_bytes)

    # Assert
    assert result == expected_result
    assert isinstance(result, dict)

@pytest.mark.parametrize("raw_bytes, expected_primitive", [
    (b"42", 42),
    (b"true", True),
    (b"hello_world", "hello_world"),
    (b"3.14159", 3.14159),
])
def test_parse_converts_yaml_scalars_to_correct_python_types(parser, raw_bytes, expected_primitive):
    """Test that YAML scalars are converted to the correct Python types."""

    # Act
    result = parser.parse(raw_bytes)

    # Assert
    assert result == expected_primitive
    assert isinstance(result, type(expected_primitive))

@pytest.mark.parametrize("empty_bytes", [
    b"",
    b"\n",
    b"   \n",
    b"# Only YAML comments here\n# Second comment line\n",
])
def test_parse_returns_none_for_empty_or_comment_only_yaml(parser, empty_bytes):
    """Test that empty or comment-only YAML returns None."""

    # Act
    result = parser.parse(empty_bytes)

    # Assert
    assert result is None


