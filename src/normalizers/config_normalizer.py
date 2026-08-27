import copy
from typing import Any, Dict

from src.normalizers.base_normalizer import BaseNormalizer
from src.exceptions.normalizer_exceptions import ConfigurationInvalidError


class ConfigNormalizer(BaseNormalizer):
    """Normalizes parsed configuration data into a canonical structure.

    Guarantees:
    - Root object must be a dictionary.
    - Resolves supported source field aliases.
    - Requires a valid canonical port.
    - Applies defaults to optional canonical fields.
    - Isolates the normalized result from the caller's input.
    """

    FIELD_ALIASES = {
        "port": (
            "listen_port",
            "Port",
            "ListenPort",
            "ssh_port",
        ),
        "permit_root_login": (
            "PermitRootLogin",
            "root_login",
        ),
        "password_authentication": (
            "PasswordAuthentication",
            "password_auth",
        ),
        "protocol_version": (
            "Protocol",
            "protocol",
        ),
        "max_auth_tries": (
            "MaxAuthTries",
            "max_auth",
            "max_retries",
        ),
        "allow_users": (
            "AllowUsers",
            "allowed_users",
            "users",
        ),
    }

    DEFAULTS: Dict[str, Any] = {
        "permit_root_login": False,
        "password_authentication": False,
        "protocol_version": 2,
        "max_auth_tries": 3,
        "allow_users": [],
    }

    def normalize(self, raw_payload: Any) -> dict[str, Any]:
        """Normalize parsed configuration data into a canonical mapping."""

        if not isinstance(raw_payload, dict):
            raise ConfigurationInvalidError(
                message=(
                    "Configuration root must be a dict, "
                    f"got '{type(raw_payload).__name__}'."
                ),
                raw_payload=raw_payload,
            )

        normalized_payload = copy.deepcopy(raw_payload)

        # Resolve source aliases into canonical field names.
        for canonical_field, aliases in self.FIELD_ALIASES.items():

            # Collect all supplied representations of this canonical field.
            supplied_fields = []

            if canonical_field in normalized_payload:
                supplied_fields.append(
                    (canonical_field, normalized_payload[canonical_field])
                )

            for alias in aliases:
                if alias in normalized_payload:
                    supplied_fields.append(
                        (alias, normalized_payload[alias])
                    )

            # Skip fields that were not supplied.
            if not supplied_fields:
                continue

            # Extract the supplied values.
            supplied_values = [
                value for _, value in supplied_fields
            ]

            # All representations must agree.
            if any(value != supplied_values[0] for value in supplied_values[1:]):
                supplied_names = ", ".join(
                    name for name, _ in supplied_fields
                )

                raise ConfigurationInvalidError(
                    message=(
                        f"Ambiguous configuration for '{canonical_field}': "
                        f"conflicting values supplied via {supplied_names}."
                    ),
                    raw_payload=raw_payload,
                )

            # Use the agreed value as the canonical value.
            normalized_payload[canonical_field] = supplied_values[0]

            # Remove all aliases from the normalized output.
            for alias in aliases:
                normalized_payload.pop(alias, None)

        # Validate required port field.
        if "port" not in normalized_payload:
            raise ConfigurationInvalidError(
                message="Required configuration field 'port' is missing.",
                raw_payload=raw_payload,
            )

        port = normalized_payload["port"]

        if type(port) is not int:
            raise ConfigurationInvalidError(
                message=(
                    "Configuration field 'port' must be an integer, "
                    f"got '{type(port).__name__}'."
                ),
                raw_payload=raw_payload,
            )

        if not 1 <= port <= 65535:
            raise ConfigurationInvalidError(
                message=(
                    "Configuration field 'port' must be between "
                    f"1 and 65535, got {port}."
                ),
                raw_payload=raw_payload,
            )

        # Apply defaults to missing optional fields.
        for field, default_value in self.DEFAULTS.items():
            if field not in normalized_payload:
                normalized_payload[field] = copy.deepcopy(default_value)

        if type(normalized_payload["permit_root_login"]) is not bool:
            raise ConfigurationInvalidError(
                message=(
                        "Configuration field 'permit_root_login' "
                        "must be a boolean."
                ),
                raw_payload=raw_payload,
            )

        if type(normalized_payload["password_authentication"]) is not bool:
            raise ConfigurationInvalidError(
                message=(
                        "Configuration field 'password_authentication' "
                        "must be a boolean."
                ),
                raw_payload=raw_payload,
            )

        protocol_version = normalized_payload["protocol_version"]

        if type(protocol_version) is not int or protocol_version != 2:
            raise ConfigurationInvalidError(
                message=(
                        "Configuration field 'protocol_version' "
                        "must be an integer with value 2."
                ),
                raw_payload=raw_payload,
            )

        max_auth_tries = normalized_payload["max_auth_tries"]

        if type(max_auth_tries) is not int or max_auth_tries < 1:
            raise ConfigurationInvalidError(
                message=(
                        "Configuration field 'max_auth_tries' "
                        "must be a positive integer (>= 1)."
                ),
                raw_payload=raw_payload,
            )

        allow_users = normalized_payload["allow_users"]

        if type(allow_users) is not list or not all(
            isinstance(user, str) for user in allow_users
        ):
            raise ConfigurationInvalidError(
                message=(
                    "Configuration field 'allow_users' "
                    "must be a list of strings."
                ),
                raw_payload=raw_payload,
            )

        if any(not user.strip() for user in allow_users):
            raise ConfigurationInvalidError(
                message=(
                    "Configuration field 'allow_users' "
                    "must not contain empty or whitespace-only usernames."
                ),
                raw_payload=raw_payload,
            )

        normalized_users = []

        for user in allow_users:
            normalized_user = user.strip()

            if normalized_user not in normalized_users:
                normalized_users.append(normalized_user)

        normalized_payload["allow_users"] = normalized_users

        return normalized_payload