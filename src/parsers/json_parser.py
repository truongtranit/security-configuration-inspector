import json
from typing import Any
from src.parsers.base_parser import BaseParser
from src.exceptions.parser_exceptions import (
    ParserError,
    EncodingError,
    JSONSyntaxError,
)

class JsonParser(BaseParser):
    """Concrete parser that converts UTF-8 encoded JSON bytes into Python objects."""

    def parse(self, raw_data: bytes) -> Any:
        """Transforms raw UTF-8 JSON bytes into a native Python object.

        Raises:
            ParserError: If input is not bytes.
            EncodingError: If UTF-8 decoding fails.
            JSONSyntaxError: If JSON syntax is malformed.
        """
        if not isinstance(raw_data, bytes):
            raise TypeError(
                f"JsonParser expected bytes, got '{type(raw_data).__name__}'",
            )

        try:
            decoded_text = raw_data.decode("utf-8")
            return json.loads(decoded_text)

        except UnicodeDecodeError as e:
            raise EncodingError(encoding="utf-8", raw_data=raw_data) from e

        except json.JSONDecodeError as e:
            raise JSONSyntaxError(
                lineno=e.lineno,
                colno=e.colno,
                msg=e.msg,
                raw_data=raw_data,
            ) from e