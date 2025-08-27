# mypy: disable-error-code=syntax
# We need to ignore syntax errors until https://github.com/python/mypy/issues/17535 is resolved.
from typing import Any, Optional

from pydantic_core import Url

from galileo.utils.user_agent import get_default_headers
from galileo_core.helpers.api_client import ApiClient
from galileo_core.schemas.base_config import GalileoConfig


class GalileoPythonConfig(GalileoConfig):
    # Config file for this project.
    config_filename: str = "galileo-python-config.json"
    console_url: Url = "https://app.galileo.ai"

    @property
    def api_client(self) -> ApiClient:
        """
        Returns an API client with default headers including User-Agent.
        """
        client = super().api_client

        # Add default headers including User-Agent if not already set
        default_headers = get_default_headers()
        for key, value in default_headers.items():
            if not hasattr(client, "_headers"):
                # Initialize headers if not present
                client._headers = {}
            if key not in client._headers:
                client._headers[key] = value

        return client

    def reset(self) -> None:
        global _galileo_config
        _galileo_config = None

        super().reset()

    @classmethod
    def get(cls, **kwargs: Any) -> "GalileoPythonConfig":
        global _galileo_config
        _galileo_config = cls._get(_galileo_config, **kwargs)  # type: ignore[arg-type]
        assert _galileo_config is not None  # _get should always return a non-None instance
        return _galileo_config


_galileo_config: Optional[GalileoPythonConfig] = None
