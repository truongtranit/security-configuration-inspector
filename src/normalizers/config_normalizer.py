from typing import Any

from src.exceptions.normalizer_exceptions import ConfigurationInvalidError

class ConfigNormalizer:
    """Normalizes parsed configuration data into a canonical representation."""

    def normalize(self, raw_payload: Any) -> dict[str, Any]:
        """Normalize the raw configuration payload into a canonical form."""

        if not isinstance(raw_payload, dict):
            raise ConfigurationInvalidError(
                message="Configuration root must be a mapping.", 
                raw_payload=raw_payload, 
            )

        return raw_payload