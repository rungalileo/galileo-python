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
        # Check for any supported auth method before raising.
        # TODO: also check GALILEO_USERNAME / GALILEO_PASSWORD / SSO env vars once alternative auth is surfaced.
        _AUTH_KWARGS = ("api_key", "username", "password", "sso_id_token", "sso_provider")
        if (
            cls._instance is None
            and not any(kwargs.get(k) for k in _AUTH_KWARGS)
            and not os.environ.get("GALILEO_API_KEY")
        ):
            raise ConfigurationError(
                "GALILEO_API_KEY not detected. "
                "Please set the GALILEO_API_KEY environment variable or pass api_key= as a keyword argument. "
                "See https://docs.galileo.ai for setup instructions."
            )
        cls._instance = cls._get(cls._instance, **kwargs)
        assert cls._instance is not None, "Failed to initialize GalileoPythonConfig"
        return cls._instance
