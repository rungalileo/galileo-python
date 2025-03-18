from os import getenv
from typing import Optional

import httpx
from attrs import define, evolve, field

from galileo.constants import DEFAULT_API_URL
from galileo.resources.client import AuthenticatedClient


@define
class GalileoApiClient(AuthenticatedClient):
    """A Client which has been authenticated for use on secured endpoints

    The following are accepted as keyword arguments and will be used to construct httpx Clients internally:

        ``base_url``: The base URL for the API, all requests are made to a relative path to this URL
            This can also be set via the GALILEO_CONSOLE_URL environment variable

        ``api_key``: The API key to be sent with every request
            This can also be set via the GALILEO_API_KEY environment variable

        ``cookies``: A dictionary of cookies to be sent with every request

        ``headers``: A dictionary of headers to be sent with every request

        ``timeout``: The maximum amount of a time a request can take. API functions will raise
        httpx.TimeoutException if this is exceeded.

        ``verify_ssl``: Whether or not to verify the SSL certificate of the API server. This should be True in production,
        but can be set to False for testing purposes.

        ``follow_redirects``: Whether or not to follow redirects. Default value is False.

        ``httpx_args``: A dictionary of additional arguments to be passed to the ``httpx.Client`` and ``httpx.AsyncClient`` constructor.

    Attributes:
        raise_on_unexpected_status: Whether or not to raise an errors.UnexpectedStatus if the API returns a
            status code that was not documented in the source OpenAPI document. Can also be provided as a keyword
            argument to the constructor.
        token: The token to use for authentication
        prefix: The prefix to use for the Authorization header
        auth_header_name: The name of the Authorization header
    """

    _base_url: Optional[str] = field(factory=lambda: GalileoApiClient.get_api_url(), kw_only=True, alias="base_url")
    _api_key: Optional[str] = field(factory=lambda: getenv("GALILEO_API_KEY", None), kw_only=True, alias="api_key")
    token: Optional[str] = None

    api_key_header_name: str = "Galileo-API-Key"
    client_type_header_name: str = "client-type"
    client_type_header_value: str = "sdk-python"

    @staticmethod
    def get_console_url() -> str:
        console_url = getenv("GALILEO_CONSOLE_URL", DEFAULT_API_URL)
        if DEFAULT_API_URL == console_url:
            return "https://app.galileo.ai"

        return console_url

    def with_api_key(self, api_key: str) -> "GalileoApiClient":
        """Get a new client matching this one with a new API key"""
        if self._client is not None:
            self._client.headers.update({self.api_key_header_name: api_key})
        if self._async_client is not None:
            self._async_client.headers.update({self.api_key_header_name: api_key})
        return evolve(self, api_key=api_key)

    def get_httpx_client(self) -> httpx.Client:
        """Get the underlying httpx.Client, constructing a new one if not previously set"""
        if self._client is None:
            if self._api_key:
                self._headers[self.api_key_header_name] = self._api_key
            elif self.token:
                self._headers[self.auth_header_name] = f"{self.prefix} {self.token}" if self.prefix else self.token
            else:
                raise ValueError("Either api_key or token must be set")

            if not self._base_url:
                raise ValueError("base_url must be set")

            self._headers[self.client_type_header_name] = self.client_type_header_value

            self._client = httpx.Client(
                base_url=self._base_url,
                cookies=self._cookies,
                headers=self._headers,
                timeout=self._timeout,
                verify=self._verify_ssl,
                follow_redirects=self._follow_redirects,
                **self._httpx_args,
            )
        return self._client

    def get_async_httpx_client(self) -> httpx.AsyncClient:
        """Get the underlying httpx.AsyncClient, constructing a new one if not previously set"""
        if self._async_client is None:
            if self._api_key:
                self._headers[self.api_key_header_name] = self._api_key
            elif self.token:
                self._headers[self.auth_header_name] = f"{self.prefix} {self.token}" if self.prefix else self.token
            else:
                raise ValueError("Either api_key or token must be set")

            if not self._base_url:
                raise ValueError("base_url must be set")

            self._headers[self.client_type_header_name] = self.client_type_header_value

            self._async_client = httpx.AsyncClient(
                base_url=self._base_url,
                cookies=self._cookies,
                headers=self._headers,
                timeout=self._timeout,
                verify=self._verify_ssl,
                follow_redirects=self._follow_redirects,
                **self._httpx_args,
            )
        return self._async_client

    @staticmethod
    def get_api_url(base_url: Optional[str] = None) -> str:
        api_url = base_url or getenv("GALILEO_CONSOLE_URL", DEFAULT_API_URL)
        if api_url is None:
            raise ValueError("base_url or GALILEO_CONSOLE_URL must be set")
        if any(map(api_url.__contains__, ["localhost", "127.0.0.1"])):
            api_url = "http://localhost:8088"
        else:
            api_url = api_url.replace("app.galileo.ai", "api.galileo.ai").replace("console", "api")
        return api_url
