import pytest
from src.parsers.json_parser import JsonParser
from src.exceptions.parser_exceptions import (
    ParserError,
    EncodingError,
    JSONSyntaxError,
)


@pytest.fixture
def parser():
    """Fixture to provide a clean JsonParser instance for each test."""
    return JsonParser()

def test_parse_returns_dictionary_for_valid_json_object(parser):
    """Returns a dictionary when given valid JSON object bytes."""
    
    raw_data = b'{"key": "value"}'

    result = parser.parse(raw_data)

    assert result == {"key": "value"}


def test_parse_returns_list_for_valid_json_array(parser):
    """Returns a list when given valid JSON array bytes."""

    raw_data = b'[1, 2, 3]'

    result = parser.parse(raw_data)

    assert result == [1, 2, 3]


def test_parse_returns_empty_dictionary_for_empty_json_object(parser):
    """Returns an empty dictionary when given empty JSON object bytes."""

    raw_data = b'{}'

    result = parser.parse(raw_data)

    assert result == {}


def test_parse_returns_empty_list_for_empty_json_array(parser):
    """Returns an empty list when given empty JSON array bytes."""

    raw_data = b'[]'

    result = parser.parse(raw_data)

    assert result == [] 



def test_parse_raises_encoding_error_for_invalid_utf8(parser):
    """Raises EncodingError when given bytes that are not valid UTF-8."""

    # Invalid UTF-8 byte sequence
    invalid_utf8_bytes = b'\x80\x81\x82'

    with pytest.raises(EncodingError) as exc_info:
        parser.parse(invalid_utf8_bytes)

    exception = exc_info.value

    assert exception.encoding == "utf-8"
    assert exception.raw_data == invalid_utf8_bytes
    assert str(exception) == "Failed to decode byte stream using 'utf-8' encoding."


def test_parse_raises_json_syntax_error_for_malformed_json(parser):
    """Raises JSONSyntaxError when given bytes that are not valid JSON."""

    # Missing value for 'port'
    malformed_bytes = b'{\n  "host": "localhost",\n  "port": \n}'

    with pytest.raises(JSONSyntaxError) as exc_info:
        parser.parse(malformed_bytes)

    exception = exc_info.value

    # Verify structural location attributes captured from JSONDecodeError
    assert exception.lineno == 4
    assert exception.colno == 1
    assert exception.raw_data == malformed_bytes
    assert isinstance(exception, ParserError)
    assert str(exception) == "Invalid JSON syntax at line 4, column 1: Expecting value"

@pytest.mark.parametrize("invalid_input", [
    '{"already": "decoded_string"}',  # str instead of bytes
    12345,                            # int
    None,                             # NoneType
    ["raw_list"],                     # list
    {"host": "localhost"},            # dict
])
def test_parse_raises_type_error_for_non_bytes_input(parser, invalid_input):
    """Raises TypeError when given input that is not bytes."""

    with pytest.raises(TypeError) as exc_info:
        parser.parse(invalid_input)

    exception = exc_info.value

    assert "JsonParser expected bytes" in str(exception)



    