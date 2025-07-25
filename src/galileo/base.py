from typing import Optional

from galileo.config import GalileoConfig
from galileo_core.helpers.api_client import ApiClient


class BaseClientModel:
    """
    A base class for all client data models.
    Used by the model classes to lazy load the API client.

    Args:
        config (Optional[GalileoConfig], optional): The config to use. Defaults to None.
    """

    config: GalileoConfig

    def __init__(self, config: Optional[GalileoConfig] = None) -> None:
        if config is not None:
            self.config = config
        else:
            self.config = GalileoConfig.get()

    @property
    def client(self) -> ApiClient:
        """
        Returns a fresh client from the config, ensuring the token is up-to-date.
        """
        return self.config.api_client
