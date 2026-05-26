# mypy: disable-error-code=syntax
# We need to ignore syntax errors until https://github.com/python/mypy/issues/17535 is resolved.
import os
from typing import Any, ClassVar, Optional

from pydantic_core import Url

from galileo.constants import DEFAULT_CONSOLE_URL
from galileo.shared.exceptions import ConfigurationError
from galileo_core.schemas.base_config import GalileoConfig


class GalileoPythonConfig(GalileoConfig):
    # Config file for this project.
    config_filename: str = "galileo-python-config.json"
    console_url: Url = DEFAULT_CONSOLE_URL

    _instance: ClassVar[Optional["GalileoPythonConfig"]] = None

    def reset(self) -> None:
        GalileoPythonConfig._instance = None
        super().reset()

    @classmethod
    def get(cls, **kwargs: Any) -> "GalileoPythonConfig":
        if cls._instance is None:
            error_message = cls._check_auth_config(kwargs)
            if error_message is not None:
                raise ConfigurationError(error_message)
        cls._instance = cls._get(cls._instance, **kwargs)
        assert cls._instance is not None, "Failed to initialize GalileoPythonConfig"
        return cls._instance

    @staticmethod
    def _check_auth_config(kwargs: dict) -> str | None:
        """Validate that a complete auth method is configured.

        Returns None if at least one complete auth method is detectable from
        either kwargs or the environment. Otherwise returns a specific error
        message identifying what's missing.

        Auth methods supported by the underlying config model:
          - API key (standalone): api_key kwarg or GALILEO_API_KEY env
          - Pre-exchanged Galileo JWT (standalone): jwt_token or GALILEO_JWT_TOKEN
          - SSO (paired): sso_id_token + sso_provider, both kwargs and env vars
          - Username/password (paired): username + password, both kwargs and env vars

        Kwargs and env vars are interchangeable — e.g. sso_id_token can come
        from a kwarg while sso_provider comes from the environment.
        """

        def _val(kwarg_name: str, env_name: str) -> str | None:
            value = kwargs.get(kwarg_name)
            if value:
                return str(value)
            return os.environ.get(env_name)

        # Standalone methods — either alone is sufficient.
        if _val("api_key", "GALILEO_API_KEY"):
            return None
        if _val("jwt_token", "GALILEO_JWT_TOKEN"):
            return None

        # SSO requires BOTH id_token and provider.
        sso_id_token = _val("sso_id_token", "GALILEO_SSO_ID_TOKEN")
        sso_provider = _val("sso_provider", "GALILEO_SSO_PROVIDER")
        if sso_id_token and sso_provider:
            return None
        if sso_id_token and not sso_provider:
            return (
                "GALILEO_SSO_ID_TOKEN is set but GALILEO_SSO_PROVIDER is missing. "
                "SSO authentication requires both. Set GALILEO_SSO_PROVIDER to your "
                "IdP identifier (e.g. 'okta', 'custom') or pass sso_provider=... "
                "as a keyword argument."
            )
        if sso_provider and not sso_id_token:
            return (
                "GALILEO_SSO_PROVIDER is set but GALILEO_SSO_ID_TOKEN is missing. "
                "SSO authentication requires both. Set GALILEO_SSO_ID_TOKEN to your "
                "IdP-issued ID token or pass sso_id_token=... as a keyword argument."
            )

        # Username/password requires BOTH.
        username = _val("username", "GALILEO_USERNAME")
        password = _val("password", "GALILEO_PASSWORD")
        if username and password:
            return None
        if username and not password:
            return (
                "GALILEO_USERNAME is set but GALILEO_PASSWORD is missing. "
                "Username/password authentication requires both."
            )
        if password and not username:
            return (
                "GALILEO_PASSWORD is set but GALILEO_USERNAME is missing. "
                "Username/password authentication requires both."
            )

        # Nothing configured anywhere.
        return (
            "No Galileo authentication detected. Set one of: "
            "GALILEO_API_KEY; GALILEO_SSO_ID_TOKEN with GALILEO_SSO_PROVIDER; "
            "or GALILEO_USERNAME with GALILEO_PASSWORD. "
            "Alternatively, pass the equivalent kwargs to GalileoPythonConfig.get(). "
            "See https://docs.galileo.ai for setup instructions."
        )
