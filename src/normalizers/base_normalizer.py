from abc import ABC, abstractmethod
from typing import Any


class BaseNormalizer(ABC):
    """Abstract base class establishing the contract for all configuration normalizers."""

    @abstractmethod
    def normalize(self, raw_payload: Any) -> dict[str, Any]:
        """Transforms raw parsed configuration data into a canonical mapping.

        Args:
            raw_payload: The raw Python object output emitted by a BaseParser.

        Returns:
            Dict[str, Any]: A canonical configuration mapping ready for validation.

        Raises:
            NormalizerError: If the raw payload violates normalizer boundary contracts.
        """
        pass