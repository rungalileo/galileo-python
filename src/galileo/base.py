from typing import Optional

from galileo.config import GalileoPythonConfig
from galileo_core.helpers.api_client import ApiClient


class BaseClientModel:
    """
    A base class for all client data models.
    Used by the model classes to lazy load the API client.

    Args:
        config (Optional[GalileoPythonConfig], optional): The config to use. Defaults to None.
    """

    config: GalileoPythonConfig

    def __init__(self, config: Optional[GalileoPythonConfig] = None) -> None:
        if config is not None:
            self.config = config
        else:
            self.config = GalileoPythonConfig.get()

    @property
    def client(self) -> ApiClient:
        """
        Returns a fresh client from the config, ensuring the token is up-to-date.
        """
        return self.config.api_client
