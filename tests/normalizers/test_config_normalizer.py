from unittest import result

import pytest
from copy import deepcopy

from src.normalizers.base_normalizer import BaseNormalizer
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
        "port": 22,
        "server": {
            "enabled": True,
        },
    }

    # Act
    result = normalizer.normalize(raw_payload)

    # Assert
    assert result["port"] == 22
    assert result["server"]["enabled"] is True
    assert isinstance(result, dict)

def test_normalize_preserves_nested_configuration_structure(normalizer):
    """Preserves the structure of a valid nested configuration mapping."""

    # Arrange
    raw_payload = {
        "port": 22,
        "database": {
            "host": "localhost",
            "credentials": {
                "username": "admin",
                "password": "secret",
            },
        },
    }

    # Act
    result = normalizer.normalize(raw_payload)

    # Assert
    assert result["port"] == 22
    assert isinstance(result, dict)

def test_normalize_preserves_nested_list_structure(normalizer):
    """Preserves the structure of a valid configuration mapping containing lists."""

    # Arrange
    raw_payload = {
        "port": 22,
        "firewall": {
            "rules": [
                {"port": 443, "allow": True},
            ]
        },
    }

    # Act
    result = normalizer.normalize(raw_payload)

    # Assert
    assert result["port"] == 22
    assert isinstance(result["firewall"]["rules"], list)

@pytest.mark.parametrize("key, scalar_value", [
    ("name", "inspector"),
    ("enabled", True),
    ("threshold", 0.95),
    ("description", None),
])
def test_normalize_preserves_scalar_values(normalizer, key, scalar_value):
    """Preserves scalar values in the configuration mapping."""

    # Arrange
    raw_input = {
        "port": 22,
        key: scalar_value,
    }

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
        "port": 22,
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

def test_config_normalizer_implements_base_normalizer(normalizer):
    """ConfigNormalizer implements the BaseNormalizer contract."""

    assert isinstance(normalizer, BaseNormalizer)

def test_normalize_returns_independent_copy(normalizer):
    """Returns an independent copy of the input configuration."""

    # Arrange
    raw_payload = {
        "port": 22,
        "server": {
            "port": 22,
        },
    }

    # Act
    result = normalizer.normalize(raw_payload)

    # Assert
    assert result is not raw_payload
    assert result["server"] is not raw_payload["server"]