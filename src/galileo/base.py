from typing import Optional

from galileo.api_client import GalileoApiClient


class BaseClientModel:
    """
    A base class for all client data models.
    Used by the model classes to lazy load the API client.

    Args:
        client (Optional[GalileoApiClient], optional): The client to use. Defaults to None.
    """

    client: Optional[GalileoApiClient] = None

    def __init__(self, client: Optional[GalileoApiClient] = None) -> None:
        if client is not None:
            self.client = client
        else:
            self.client = GalileoApiClient()
