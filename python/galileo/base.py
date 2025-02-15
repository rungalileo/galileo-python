from os import getenv

from typing import Optional

from galileo.client import AuthenticatedClient


class BaseClientModel:
    client: Optional[AuthenticatedClient] = None

    @staticmethod
    def _log_request(request):
        print(
            f"Request event hook: {request.method} {request.url} - Waiting for response"
        )

    @staticmethod
    def _log_response(response):
        request = response.request
        print(
            f"Response event hook: {request.method} {request.url} - Status {response.status_code}"
        )

    @staticmethod
    def create_client() -> AuthenticatedClient:
        base_url = getenv("GALILEO_CONSOLE_URL")
        api_key = getenv("GALILEO_API_KEY")
        return AuthenticatedClient(
            base_url=base_url,
            api_key=api_key,
            # httpx_args={
            #     "event_hooks": {"request": [_log_request], "response": [_log_response]}
            # },
        )

    def _get_client(self) -> AuthenticatedClient:
        if self.client is None:
            self.client = self.create_client()
        return self.client
