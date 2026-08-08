from pathlib import Path
from typing import Dict, Type, Union
from src.parsers.base_parser import BaseParser
from src.parsers.json_parser import JsonParser
from src.exceptions.factory_exceptions import FactoryError, UnsupportedParserError


class ParserFactory:
    """Factory responsible for selecting and instantiating the appropriate BaseParser."""

    _registered_parsers: Dict[str, Type[BaseParser]] = {
        ".json": JsonParser,
        # Add more extensions and parsers here
    }

    @classmethod
    def register_parser(cls, extension: str, parser_cls: Type[BaseParser]) -> None:
        """Registers a new parser for a given file extension.

        Args:
            extension: The file extension (e.g., '.yaml').
            parser_cls: The parser class to register.
        """

        normalized_extension = extension.lower() if extension.startswith(".") else f".{extension.lower()}"
        cls._registered_parsers[normalized_extension] = parser_cls


    @classmethod
    def get_parser(cls, resource: Union[str, Path]) -> BaseParser:
        """Selects and returns an instantiated BaseParser based on the resource's extension.

        Args:
            resource: The string file path or Path object.

        Returns:
            BaseParser: An instance of the matching concrete parser.

        Raises:
            UnsupportedParserError: If the extension is not registered.
            FactoryError: If resource is invalid or has no file extension.
        """

        try:
            path = Path(resource)
        except TypeError as e:
            raise FactoryError(f"Invalid resource type for factory routing: {type(resource).__name__}") from e

        extension = path.suffix.lower()

        if not extension:
            raise FactoryError(f"Resource target missing file extension: '{resource}'", resource=str(resource))

        parser_cls = cls._registered_parsers.get(extension)

        if parser_cls is None:
            raise UnsupportedParserError(resource=str(resource), extension=extension)

        return parser_cls()






    