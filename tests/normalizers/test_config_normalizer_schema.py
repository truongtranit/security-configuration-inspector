from sys import exc_info, exception

import pytest
from src.normalizers.config_normalizer import ConfigNormalizer
from src.exceptions.normalizer_exceptions import ConfigurationInvalidError


@pytest.fixture
def normalizer():
    return ConfigNormalizer()


# -----------------------------------------------------------------------------
# Required Field & Validation Boundary Tests (N-011 - N-016)
# -----------------------------------------------------------------------------

def test_n011_valid_port_supplied_normalizes_successfully(normalizer):
    """N-011: A valid port normalizes successfully and applies defaults."""

    # Arrange
    raw_payload = {
        "port": 22,
    }

    # Act
    result = normalizer.normalize(raw_payload)

    # Assert
    assert result["port"] == 22

    # Verify canonical defaults
    assert result["permit_root_login"] is False
    assert result["password_authentication"] is False
    assert result["protocol_version"] == 2
    assert result["max_auth_tries"] == 3
    assert result["allow_users"] == []

def test_n012_port_missing_raises_configuration_invalid_error(normalizer):
    """N-012: Missing required port raises ConfigurationInvalidError."""

    # Arrange
    raw_payload = {
        "permit_root_login": True,
    }

    # Act / Assert
    with pytest.raises(ConfigurationInvalidError) as exc_info:
        normalizer.normalize(raw_payload)

    exception = exc_info.value

    assert exception.raw_payload == raw_payload
    assert "port" in str(exception).lower()

@pytest.mark.parametrize("invalid_port", [0, -1, -22])
def test_n013_port_below_1_raises_configuration_invalid_error(
    normalizer,
    invalid_port,
):
    """N-013: Port below 1 raises ConfigurationInvalidError."""

    # Arrange
    raw_payload = {"port": invalid_port}

    # Act
    with pytest.raises(ConfigurationInvalidError) as exc_info:
        normalizer.normalize(raw_payload)

    exception = exc_info.value

    # Assert
    assert exception.raw_payload == raw_payload
    assert "port" in str(exception).lower()


@pytest.mark.parametrize("invalid_port", [65536, 70000, 999999])
def test_n014_port_above_65535_raises_configuration_invalid_error(
    normalizer,
    invalid_port,
):
    """N-014: Port above 65535 raises ConfigurationInvalidError."""

    # Arrange
    raw_payload = {"port": invalid_port}

    # Act
    with pytest.raises(ConfigurationInvalidError) as exc_info:
        normalizer.normalize(raw_payload)

    exception = exc_info.value

    # Assert
    assert exception.raw_payload == raw_payload
    assert "port" in str(exception).lower()

@pytest.mark.parametrize("invalid_port", ["twenty_two", [22], {"port": "22"}, 22.5, None])
def test_n015_port_is_not_an_integer_raises_configuration_invalid_error(normalizer, invalid_port):
    """N-015: Port is not an integer raises ConfigurationInvalidError."""

    # Arrange
    raw_payload = {"port": invalid_port}

    # Act
    with pytest.raises(ConfigurationInvalidError) as exc_info:
        normalizer.normalize(raw_payload)

    exception = exc_info.value

    # Assert
    assert exception.raw_payload == raw_payload
    assert "port" in str(exception).lower()


@pytest.mark.parametrize("bool_port", [True, False])
def test_n016_port_is_boolean_raises_configuration_invalid_error(normalizer, bool_port):
    """N-016: Port is True/False raises ConfigurationInvalidError."""

    # Arrange
    raw_payload = {"port": bool_port}

    # Act
    with pytest.raises(ConfigurationInvalidError) as exc_info:
        normalizer.normalize(raw_payload)

    exception = exc_info.value

    # Assert
    assert exception.raw_payload == raw_payload
    assert "port" in str(exception).lower()


# -----------------------------------------------------------------------------
# Default Values Tests (N-017 - N-021)
# -----------------------------------------------------------------------------

def test_n017_permit_root_login_missing_defaults_to_false(normalizer):
    """N-017: permit_root_login missing defaults to False."""

    # Arrange
    raw_payload = {"port": 22}

    # Act
    result = normalizer.normalize(raw_payload)

    # Assert
    assert result["permit_root_login"] is False
    assert isinstance(result["permit_root_login"], bool)

def test_n018_password_authentication_missing_defaults_to_false(normalizer):
    """N-018: password_authentication missing defaults to False."""

    # Arrange
    raw_payload = {"port": 22}

    # Act
    result = normalizer.normalize(raw_payload)

    # Assert
    assert result["password_authentication"] is False
    assert isinstance(result["password_authentication"], bool)


def test_n019_protocol_version_missing_defaults_to_two(normalizer):
    """N-019: protocol_version missing defaults to 2."""

    # Arrange
    raw_payload = {"port": 22}

    # Act
    result = normalizer.normalize(raw_payload)

    # Assert
    assert result["protocol_version"] == 2
    assert isinstance(result["protocol_version"], int)
    assert not isinstance(result["protocol_version"], bool)


def test_n020_max_auth_tries_missing_defaults_to_three(normalizer):
    """N-020: max_auth_tries missing defaults to 3."""

    # Arrange
    raw_payload = {"port": 22}

    # Act
    result = normalizer.normalize(raw_payload)

    # Assert
    assert result["max_auth_tries"] == 3
    assert isinstance(result["max_auth_tries"], int)
    assert not isinstance(result["max_auth_tries"], bool)


def test_n021_allow_users_missing_defaults_to_empty_list(normalizer):
    """N-021: allow_users missing defaults to empty list []."""

    # Arrange
    raw_payload = {"port": 22}

    # Act
    result = normalizer.normalize(raw_payload)

    # Assert
    assert result["allow_users"] == []
    assert isinstance(result["allow_users"], list)

def test_allow_users_default_is_independent_between_normalizations(normalizer):
    """Default allow_users lists are independent between normalizations."""

    # Arrange
    first_result = normalizer.normalize({"port": 22})
    second_result = normalizer.normalize({"port": 2222})

    # Act
    first_result["allow_users"].append("admin")

    # Assert
    assert second_result["allow_users"] == []


# -----------------------------------------------------------------------------
# Alias Resolution Tests (N-022 - N-027)
# -----------------------------------------------------------------------------

def test_n022_alias_listen_port_resolves_to_port(normalizer):
    """N-022: listen_port resolves to the canonical port field."""

    # Arrange
    raw_payload = {"listen_port": 2222}

    # Act
    result = normalizer.normalize(raw_payload)

    # Assert
    assert result["port"] == 2222
    assert "listen_port" not in result

def test_n023_alias_root_login_resolves_to_permit_root_login(normalizer):
    """N-023: root_login resolves to the canonical permit_root_login field."""

    # Arrange
    raw_payload = {
        "port": 22, 
        "root_login": True,
    }

    # Act
    result = normalizer.normalize(raw_payload)

    # Assert
    assert result["permit_root_login"] is True
    assert "root_login" not in result

def test_n024_alias_password_auth_resolves_to_password_authentication(normalizer):
    """N-024: password_auth resolves to the canonical password_authentication field."""

    # Arrange
    raw_payload = {
        "port": 22, 
        "password_auth": True
    }

    # Act
    result = normalizer.normalize(raw_payload)

    # Assert
    assert result["password_authentication"] is True
    assert "password_auth" not in result

def test_n025_alias_protocol_resolves_to_protocol_version(normalizer):
    """N-025: protocol resolves to the canonical protocol_version field."""

    # Arrange
    raw_payload = {
        "port": 22,
        "protocol": 2,
    }

    # Act
    result = normalizer.normalize(raw_payload)

    # Assert
    assert result["protocol_version"] == 2
    assert "protocol" not in result


def test_n026_alias_max_retries_resolves_to_max_auth_tries(normalizer):
    """N-026: max_retries resolves to the canonical max_auth_tries field."""

    # Arrange
    raw_payload = {
        "port": 22, 
        "max_retries": 5,
    }

    # Act
    result = normalizer.normalize(raw_payload)

    # Assert
    assert result["max_auth_tries"] == 5
    assert "max_retries" not in result


def test_n027_alias_allowed_users_resolves_to_allow_users(normalizer):
    """N-027: allowed_users resolves to the canonical allow_users field."""

    # Arrange
    raw_payload = {
        "port": 22, 
        "allowed_users": ["sec_admin", "auditor"],
    }

    # Act
    result = normalizer.normalize(raw_payload)

    # Assert    
    assert result["allow_users"] == ["sec_admin", "auditor"]
    assert "allowed_users" not in result

def test_n028_conflicting_canonical_and_alias_raise_configuration_invalid_error(
    normalizer,
):
    """N-028: Conflicting canonical and alias values raise ConfigurationInvalidError."""

    # Arrange
    raw_payload = {
        "port": 22,
        "listen_port": 2222,
    }

    # Act / Assert
    with pytest.raises(ConfigurationInvalidError) as exc_info:
        normalizer.normalize(raw_payload)

    exception = exc_info.value

    # Assert
    assert exception.raw_payload == raw_payload
    assert "port" in str(exception).lower()
    assert "ambiguous" in str(exception).lower()

def test_n029_conflicting_aliases_for_same_canonical_field_raise_error(normalizer):
    """N-029: Conflicting aliases for the same field raise ConfigurationInvalidError."""

    # Arrange
    raw_payload = {
        "listen_port": 2222,
        "Port": 2200,
    }

    # Act / Assert
    with pytest.raises(ConfigurationInvalidError) as exc_info:
        normalizer.normalize(raw_payload)

    exception = exc_info.value

    assert exception.raw_payload == raw_payload
    assert "port" in str(exception).lower()
    assert "ambiguous" in str(exception).lower()

def test_n030_matching_aliases_for_same_canonical_field_normalize_successfully(normalizer):
    """N-030: Multiple aliases with the same value normalize successfully."""

    # Arrange
    raw_payload = {
        "listen_port": 2222,
        "Port": 2222,
    }

    # Act
    result = normalizer.normalize(raw_payload)

    # Assert
    assert result["port"] == 2222
    assert "listen_port" not in result
    assert "Port" not in result

def test_n031_matching_canonical_and_alias_normalize_successfully(normalizer):
    """N-031: Matching canonical and alias values normalize successfully."""

    # Arrange
    raw_payload = {
        "port": 22,
        "listen_port": 22,
    }

    # Act
    result = normalizer.normalize(raw_payload)

    # Assert
    assert result["port"] == 22
    assert "listen_port" not in result


# -----------------------------------------------------------------------------
# Type Validation & Value Constraint Tests (N-032 - N-036)
# -----------------------------------------------------------------------------

@pytest.mark.parametrize(
    "invalid_val",
    [
        "yes",
        "true",
        1,
        0,
        [True],
        {"enabled": True},
    ],
)
def test_n032_permit_root_login_non_bool_raises_configuration_invalid_error(
    normalizer, invalid_val
):
    """N-032: Non-boolean permit_root_login raises ConfigurationInvalidError."""

    # Arrange
    raw_payload = {
        "port": 22,
        "permit_root_login": invalid_val,
    }

    # Act
    with pytest.raises(ConfigurationInvalidError) as exc_info:
        normalizer.normalize(raw_payload)

    # Assert
    exception = exc_info.value

    assert exception.raw_payload == raw_payload
    assert "permit_root_login" in str(exception).lower()


@pytest.mark.parametrize(
    "invalid_val",
    [
        "no",
        "false",
        1,
        0,
        [False],
        {"enabled": False},
    ],
)
def test_n033_password_authentication_non_bool_raises_configuration_invalid_error(
    normalizer, invalid_val
):
    """N-033: Non-boolean password_authentication raises ConfigurationInvalidError."""

    # Arrange
    raw_payload = {
        "port": 22,
        "password_authentication": invalid_val,
    }
    
    # Act
    with pytest.raises(ConfigurationInvalidError) as exc_info:
        normalizer.normalize(raw_payload)

    # Assert
    exception = exc_info.value

    assert exception.raw_payload == raw_payload
    assert "password_authentication" in str(exception).lower()

def test_n034_protocol_version_two_normalizes_successfully(normalizer):
    """N-034: Explicit protocol_version 2 normalizes successfully."""

    # Arrange
    raw_payload = {
        "port": 22,
        "protocol_version": 2,
    }

    # Act
    result = normalizer.normalize(raw_payload)

    # Assert
    assert result["protocol_version"] == 2
    assert type(result["protocol_version"]) is int

@pytest.mark.parametrize(
    "invalid_version",
    [
        1,  # Insecure/outdated SSH version
        3,  # Non-existent SSH version
        "2",  # String representation
        True,  # Boolean
        2.0,  # Float
        [2],  # List
    ],
)
def test_n035_protocol_version_invalid_raises_configuration_invalid_error(
    normalizer, invalid_version
):
    """N-035: protocol_version must be a strict int  with value 2."""

    # Arrange
    raw_payload = {
        "port": 22,
        "protocol_version": invalid_version,
    }

    # Act
    with pytest.raises(ConfigurationInvalidError) as exc_info:
        normalizer.normalize(raw_payload)

    # Assert
    exception = exc_info.value

    assert exception.raw_payload == raw_payload
    assert "protocol_version" in str(exception).lower()

@pytest.mark.parametrize("valid_tries", [1, 3, 5, 10])
def test_n036_valid_max_auth_tries_normalizes_successfully(
    normalizer, valid_tries
):
    """N-036: Positive integer max_auth_tries normalizes successfully."""

    # Arrange
    raw_payload = {
        "port": 22,
        "max_auth_tries": valid_tries,
    }

    # Act
    result = normalizer.normalize(raw_payload)

    # Assert
    assert result["max_auth_tries"] == valid_tries
    assert type(result["max_auth_tries"]) is int

@pytest.mark.parametrize(
    "invalid_tries",
    [
        0,  # Non-positive integer
        -1,  # Negative integer
        "3",  # String
        True,  # Boolean
        3.5,  # Float
        [3],  # List
    ],
)
def test_n037_max_auth_tries_invalid_raises_configuration_invalid_error(
    normalizer, invalid_tries
):
    """N-037: Invalid max_auth_tries raises ConfigurationInvalidError."""

    # Arrange
    raw_payload = {
        "port": 22,
        "max_auth_tries": invalid_tries,
    }

    # Act
    with pytest.raises(ConfigurationInvalidError) as exc_info:
        normalizer.normalize(raw_payload)

    # Assert
    exception = exc_info.value

    assert exception.raw_payload == raw_payload
    assert "max_auth_tries" in str(exception).lower()

@pytest.mark.parametrize(
    "invalid_users_payload",
    [
        "admin",                 # Plain string instead of list
        [123, "admin"],          # List containing non-string item
        ["admin", None],         # List containing None
        {"admin": True},         # Dict instead of list
        ("admin", "auditor"),    # Tuple instead of list
        None,                    # None instead of list
    ],
)
def test_n038_allow_users_non_list_or_non_string_items_raise_configuration_invalid_error(
    normalizer, invalid_users_payload
):
    """N-038: allow_users must be a list containing only strings."""

    # Arrange
    raw_payload = {
        "port": 22,
        "allow_users": invalid_users_payload,
    }

    # Act
    with pytest.raises(ConfigurationInvalidError) as exc_info:
        normalizer.normalize(raw_payload)

    # Assert
    exception = exc_info.value

    assert exception.raw_payload == raw_payload
    assert "allow_users" in str(exception).lower()


# -----------------------------------------------------------------------------
# String Hygiene & List Sanitization Tests (N-037 - N-040)
# -----------------------------------------------------------------------------

@pytest.mark.parametrize(
    "invalid_users",
    [
        [""],
        ["admin", ""],
        ["", "sec_admin"],
    ],
)
def test_n039_allow_users_rejects_empty_string_usernames(
    normalizer, invalid_users
):
    """N-039: allow_users containing an empty username raises ConfigurationInvalidError."""

    # Arrange
    raw_payload = {
        "port": 22,
        "allow_users": invalid_users,
    }

    # Act / Assert
    with pytest.raises(ConfigurationInvalidError) as exc_info:
        normalizer.normalize(raw_payload)

    # Assert
    exception = exc_info.value

    assert exception.raw_payload == raw_payload
    assert "allow_users" in str(exception).lower()
    assert (
        "empty" in str(exception).lower()
        or "blank" in str(exception).lower()
    )

@pytest.mark.parametrize(
    "whitespace_users",
    [
        ["   "],
        ["\t"],
        ["\n"],
        ["admin", "   "],
        ["  ", "auditor"],
    ],
)
def test_n040_allow_users_rejects_whitespace_only_usernames(
    normalizer, whitespace_users
):
    """N-040: allow_users containing whitespace-only usernames raises ConfigurationInvalidError."""

    # Arrange
    raw_payload = {
        "port": 22,
        "allow_users": whitespace_users,
    }

    # Act
    with pytest.raises(ConfigurationInvalidError) as exc_info:
        normalizer.normalize(raw_payload)

    # Assert
    exception = exc_info.value

    assert exception.raw_payload == raw_payload
    assert "allow_users" in str(exception).lower()
    assert (
        "whitespace" in str(exception).lower()
        or "blank" in str(exception).lower()
        or "empty" in str(exception).lower()
    )

def test_n041_allow_users_trims_leading_and_trailing_whitespace(normalizer):
    """N-041: allow_users trims surrounding whitespace from usernames."""

    # Arrange
    raw_payload = {
        "port": 22,
        "allow_users": ["  alice  ", "\tbob\n", " charlie"],
    }

    # Act
    result = normalizer.normalize(raw_payload)

    # Assert
    assert result["allow_users"] == ["alice", "bob", "charlie"]

@pytest.mark.parametrize(
    "duplicate_users, expected_deduped",
    [
        (["admin", "admin"], ["admin"]),
        (
            ["admin", "sec_admin", "admin"],
            ["admin", "sec_admin"],
        ),
        (
            ["alice", "bob", "alice", "charlie", "bob"],
            ["alice", "bob", "charlie"],
        ),
        (["  admin  ", "admin"], ["admin"]),
    ],
)
def test_n042_allow_users_deduplicates_preserving_order(
    normalizer, duplicate_users, expected_deduped
):
    """N-042: Duplicate usernames are removed while preserving first occurrence order."""

    # Arrange
    raw_payload = {
        "port": 22,
        "allow_users": duplicate_users,
    }

    # Act
    result = normalizer.normalize(raw_payload)

    # Assert
    assert result["allow_users"] == expected_deduped

def test_n043_allow_users_normalization_does_not_mutate_original_input(
    normalizer
):
    """N-043: Username normalization does not mutate the caller's payload."""

    # Arrange
    raw_payload = {
        "port": 22,
        "allow_users": ["  alice  ", "alice"],
    }

    # Act
    result = normalizer.normalize(raw_payload)

    # Assert
    assert raw_payload["allow_users"] == ["  alice  ", "alice"]
    assert result["allow_users"] == ["alice"]