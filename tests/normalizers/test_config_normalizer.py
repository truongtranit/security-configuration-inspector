import pytest
from copy import deepcopy

from src.normalizers.config_normalizer import ConfigNormalizer
from src.exceptions.normalizer_exceptions import (
    ConfigurationInvalidError,
    NormalizerError,
)


@pytest.fixture
def normalizer():
    """Fixture providing a fresh ConfigNormalizer instance for each test."""
    return ConfigNormalizer()


def test_normalize_returns_mapping_for_valid_configuration(normalizer):
    """Returns a dictionary for a valid configuration mapping."""

    # Arrange
    raw_payload = {
        "server": {
            "port": 22,
            "enabled": True,
        }
    }

    # Act
    result = normalizer.normalize(raw_payload)

    # Assert
    assert result == raw_payload
    assert isinstance(result, dict)

def test_normalize_returns_empty_mapping_for_empty_configuration(normalizer):
    """Returns an empty dictionary for an empty configuration mapping."""

    # Arrange
    raw_payload = {}

    # Act
    result = normalizer.normalize(raw_payload)

    # Assert
    assert result == {}
    assert isinstance(result, dict)

def test_normalize_preserves_nested_configuration_structure(normalizer):
    """Preserves the structure of a valid nested configuration mapping."""

    # Arrange
    raw_payload = {
        "database": {
            "host": "localhost",
            "port": 5432,
            "credentials": {
                "username": "admin",
                "password": "secret",
            }
        }
    }

    # Act
    result = normalizer.normalize(raw_payload)

    # Assert
    assert result == raw_payload
    assert isinstance(result, dict)

def test_normalize_preserves_nested_list_structure(normalizer):
    """Preserves the structure of a valid configuration mapping containing lists."""

    # Arrange
    raw_payload = {
        "firewall": {
            "rules": [
                {"port": 22, "allow": False},
                {"port": 443, "allow": True},
            ]
        }
    }

    # Act
    result = normalizer.normalize(raw_payload)

    # Assert
    assert result == raw_payload
    assert isinstance(result["firewall"]["rules"], list)


@pytest.mark.parametrize("key, scalar_value", [
    ("name", "inspector"),
    ("port", 5432),
    ("enabled", True),
    ("threshold", 0.95),
    ("description", None),
])
def test_normalize_preserves_scalar_values(normalizer, key, scalar_value):
    """Preserves scalar values in the configuration mapping."""

    # Arrange
    raw_input = {key: scalar_value}

    # Act
    result = normalizer.normalize(raw_input)

    # Assert
    assert result[key] == scalar_value
    assert isinstance(result[key], type(scalar_value))

def test_normalize_raises_configuration_invalid_error_for_none(normalizer):
    """Raises ConfigurationInvalidError when the root configuration is None."""

    # Arrange
    raw_payload = None

    # Act
    with pytest.raises(ConfigurationInvalidError) as exc_info:
        normalizer.normalize(raw_payload)

    # Assert
    exception = exc_info.value

    assert exception.raw_payload is None
    assert "configuration root" in str(exception).lower()
    assert isinstance(exception, NormalizerError)

def test_normalize_raises_configuration_invalid_error_for_non_mapping(normalizer):
    """Raises ConfigurationInvalidError when the root configuration is not a mapping."""

    # Arrange
    raw_payload = ["not", "a", "mapping"]

    # Act
    with pytest.raises(ConfigurationInvalidError) as exc_info:
        normalizer.normalize(raw_payload)

    # Assert
    exception = exc_info.value

    assert exception.raw_payload == raw_payload
    assert "configuration root" in str(exception).lower()

@pytest.mark.parametrize("raw_payload", [
    "not a mapping",
    42,
    3.14,
    True,
])
def test_normalize_raises_configuration_invalid_error_for_non_mapping_scalars(
    normalizer,
    raw_payload,
):
    """Raises ConfigurationInvalidError for scalar configuration roots."""

    # Act
    with pytest.raises(ConfigurationInvalidError) as exc_info:
        normalizer.normalize(raw_payload)

    # Assert
    exception = exc_info.value

    assert exception.raw_payload == raw_payload
    assert "configuration root" in str(exception).lower()

def test_normalize_does_not_mutate_input(normalizer):
    """Does not mutate the original configuration mapping."""

    # Arrange
    raw_payload = {
        "server": {
            "port": 22,
            "enabled": True,
        },
        "firewall": {
            "rules": [
                {"port": 22, "allow": False},
            ]
        },
    }

    original_payload = deepcopy(raw_payload)

    # Act
    result = normalizer.normalize(raw_payload)

    # Assert
    assert raw_payload == original_payload