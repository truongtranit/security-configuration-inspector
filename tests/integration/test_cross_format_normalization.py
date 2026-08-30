import pytest

from src.parsers.parser_factory import ParserFactory
from src.normalizers.config_normalizer import ConfigNormalizer

@pytest.fixture
def normalizer():
    return ConfigNormalizer()

def test_n044_equivalent_json_and_yaml_normalize_to_same_canonical_configuration():
    """N-044: Equivalent JSON and YAML inputs produce identical canonical output."""

    # Arrange
    json_resource = "config.json"
    yaml_resource = "config.yaml"

    json_bytes = b"""
    {
        "listen_port": 2222,
        "root_login": false,
        "password_auth": false,
        "protocol": 2,
        "max_retries": 3,
        "allowed_users": ["alice", "bob"]
    }
    """

    yaml_bytes = b"""
    Port: 2222
    PermitRootLogin: false
    PasswordAuthentication: false
    Protocol: 2
    MaxAuthTries: 3
    AllowUsers:
      - alice
      - bob
    """

    expected = {
        "port": 2222,
        "permit_root_login": False,
        "password_authentication": False,
        "protocol_version": 2,
        "max_auth_tries": 3,
        "allow_users": ["alice", "bob"],
    }

    normalizer = ConfigNormalizer()

    # Act
    json_parser = ParserFactory.get_parser(json_resource)
    yaml_parser = ParserFactory.get_parser(yaml_resource)

    json_parsed = json_parser.parse(json_bytes)
    yaml_parsed = yaml_parser.parse(yaml_bytes)

    json_normalized = normalizer.normalize(json_parsed)
    yaml_normalized = normalizer.normalize(yaml_parsed)

    # Assert
    assert json_normalized == expected
    assert yaml_normalized == expected
    assert json_normalized == yaml_normalized

def test_n045_unknown_fields_are_preserved(normalizer):
    """N-045: Unknown configuration fields are preserved during normalization."""

    # Arrange
    raw_payload = {
        "port": 22,
        "future_security_setting": True,
        "custom_banner": "Authorized access only",
    }

    # Act
    result = normalizer.normalize(raw_payload)

    # Assert
    assert result["future_security_setting"] is True
    assert result["custom_banner"] == "Authorized access only"