import yaml
from typing import Any
from src.parsers.base_parser import BaseParser
from src.exceptions.parser_exceptions import (
    ParserError,
    EncodingError,
    YAMLSyntaxError,
)

class YamlParser(BaseParser):
    """Concrete parser that converts UTF-8 encoded YAML bytes into Python objects."""

    def parse(self, raw_data: bytes) -> Any:
        """Transforms raw UTF-8 YAML bytes into a native Python object.

        Args:
            raw_data: The raw binary data retrieved from a reader.

        Returns:
            Any: The native Python representation (dict, list, primitive) of the YAML payload.

        Raises:
            ParserError: If input is not bytes.
            EncodingError: If UTF-8 decoding fails.
            YAMLSyntaxError: If YAML syntax is malformed.
        """

        if not isinstance(raw_data, (bytes, bytearray)):
            raise ParserError(
                message=f"YamlParser expected bytes, got '{type(raw_data).__name__}'",
                raw_data=raw_data if isinstance(raw_data, (bytes, bytearray)) else None,
            )

        try:
            decoded_text = raw_data.decode("utf-8")
            # Always use safe_load to prevent arbitrary Python object execution vulnerabilities
            return yaml.safe_load(decoded_text)

        except UnicodeDecodeError as e:
            raise EncodingError(encoding="utf-8", raw_data=raw_data) from e

        except yaml.YAMLError as e:
            # Captures parse errors, scanner errors, and structural syntax issues
            raise YAMLSyntaxError(
                msg=str(e),
                raw_data=raw_data,
            ) from e