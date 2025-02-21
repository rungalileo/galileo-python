from importlib.metadata import version
from os import getenv
from time import time
from typing import Any, Optional

import jwt
import logging
from httpx import Client, AsyncClient, HTTPError, Response, Timeout, URL
from urllib.parse import urljoin

from galileo_core.constants.request_method import RequestMethod
from galileo_core.helpers.execution import async_run
from galileo_core.helpers.api_client import ApiClient as CoreApiClient
from galileo.constants.routes import Routes
from galileo.schema.trace import TracesIngestRequest, TracesIngestResponse
from galileo.utils.request import HttpHeaders, make_request
from galileo.api_client import GalileoApiClient
from galileo.projects import Projects
from galileo.log_streams import LogStreams

_logger = logging.getLogger(__name__)


class GalileoCoreApiClient:
    """
    A class for interacting with the Galileo API using the galileo_core package.
    Currently used by the GalileoLogger to create and upload traces to Galileo.

    Attributes
    ----------
    project_id : Optional[str]
        The ID of the project.
    log_stream_id : Optional[str]
        The ID of the log stream.
    base_url : Optional[str]
        The base URL for the Galileo API.
    api_key : Optional[str]
        The API key for authentication.
    """

    api_key_header_name: str = "Galileo-API-Key"

    project_id: Optional[str] = None
    log_stream_id: Optional[str] = None

    api_url: str
    api_key: str

    def __init__(
        self,
        base_url: Optional[str] = None,
        api_key: Optional[str] = None,
        project_id: Optional[str] = None,
        log_stream_id: Optional[str] = None,
    ):
        self.api_url = GalileoApiClient.get_api_url(base_url)
        self.api_key = api_key or getenv("GALILEO_API_KEY", "")  # type: ignore

        if not self.api_url or not self.api_key:
            raise ValueError("api_url and api_key must be set")

        self.project_id = project_id
        self.log_stream_id = log_stream_id

    @property
    def auth_header(self) -> dict[str, Optional[str]]:
        return {self.api_key_header_name: self.api_key}

    def _make_request(
        self,
        request_method: RequestMethod,
        endpoint: str,
        json: Optional[dict] = None,
        data: Optional[dict] = None,
        files: Optional[dict] = None,
        params: Optional[dict] = None,
        json_request_only: bool = False,
    ) -> Any:
        if json_request_only:
            content_headers = HttpHeaders.accept_json()
        else:
            content_headers = HttpHeaders.json()
        headers = {**self.auth_header, **content_headers}
        return GalileoCoreApiClient.make_request_sync(
            request_method=request_method,
            base_url=self.api_url,
            endpoint=endpoint,
            json=json,
            data=data,
            files=files,
            params=params,
            headers=headers,
        )

    async def _make_async_request(
        self,
        request_method: RequestMethod,
        endpoint: str,
        json: Optional[dict] = None,
        data: Optional[dict] = None,
        files: Optional[dict] = None,
        params: Optional[dict] = None,
        json_request_only: bool = False,
    ) -> Any:
        if json_request_only:
            content_headers = HttpHeaders.accept_json()
        else:
            content_headers = HttpHeaders.json()
        headers = {**self.auth_header, **content_headers}
        await make_request(
            request_method=request_method,
            base_url=self.api_url,
            endpoint=endpoint,
            json=json,
            data=data,
            files=files,
            params=params,
            headers=headers,
        )

    async def ingest_traces(self, traces_ingest_request: TracesIngestRequest) -> dict[str, str]:
        traces_ingest_request.log_stream_id = self.log_stream_id
        json = traces_ingest_request.model_dump()

        return await self._make_async_request(
            RequestMethod.POST, endpoint=Routes.traces.format(project_id=self.project_id), json=json
        )

    def ingest_traces_sync(self, traces_ingest_request: TracesIngestRequest) -> dict[str, str]:
        traces_ingest_request.log_stream_id = self.log_stream_id
        json = traces_ingest_request.model_dump()

        return self._make_request(
            RequestMethod.POST, endpoint=Routes.traces.format(project_id=self.project_id), json=json
        )

    # TODO: Move this method to galileo_core.helpers.api_client
    @staticmethod
    def make_request_sync(
        request_method: RequestMethod,
        base_url: str,
        endpoint: str,
        skip_ssl_validation: bool = False,
        read_timeout: float = 60.0,
        **kwargs: Any,
    ) -> Any:
        url = urljoin(base_url, endpoint)
        with Client(
            base_url=base_url, timeout=Timeout(read_timeout, connect=5.0), verify=not skip_ssl_validation
        ) as client:
            response = client.request(method=request_method.value, url=url, timeout=read_timeout, **kwargs)
            CoreApiClient.validate_response(response)
            return response.json()
