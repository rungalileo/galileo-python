from typing import Optional

from galileo.api_client import GalileoApiClient
from galileo.config import GalileoSDKConfig


class BaseClientModel:
    """
    A base class for all client data models.
    Used by the model classes to lazy load the API client.

    Args:
        client (Optional[GalileoApiClient], optional): The client to use. Defaults to None.
    """

    client: GalileoApiClient

    def __init__(self, client: Optional[GalileoApiClient] = None) -> None:
        if client is not None:
            self.client = client
        else:
            config = GalileoSDKConfig.get()
            # Accessing the api_client property triggers the token refresh logic
            _ = config.api_client
            self.client = GalileoApiClient(_base_url=str(config.api_url), token=config.jwt_token.get_secret_value())
