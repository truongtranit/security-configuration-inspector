from abc import ABC, abstractmethod
from typing import Any

class BaseParser(ABC):
    @abstractmethod
    def parse(self, data: bytes) -> Any:
        """
        Transform raw bytes into a native Python object.

        This class knows nothing about:
        - files
        - HTTP
        - JSON
        - YAML
        - business rules
        - validation
        """
        ...


    