from importlib.metadata import version
from os import getenv
from time import time
from typing import Any, Optional

import jwt
import logging

from galileo_core.constants.request_method import RequestMethod
from galileo_core.helpers.execution import async_run
from galileo_core.helpers.api_client import ApiClient as CoreApiClient
from galileo.constants.routes import Routes
from galileo.schema.trace import TracesIngestRequest, TracesIngestResponse
from galileo.utils.request import HttpHeaders, make_request
from httpx import Client, AsyncClient, HTTPError, Response, Timeout
from urllib.parse import urljoin

_logger = logging.getLogger(__name__)


class ApiClient:
    project_id: Optional[str] = None
    log_stream_id: Optional[str] = None

    def __init__(self, project_name: str, log_stream_name: Optional[str] = None):
        self.project_id = None
        self.api_url = self.get_api_url()
        if self.healthcheck():
            self.token = self.get_token()
            project = self.get_project_by_name(project_name)
            if project is None:
                self.project_id = self.create_project(project_name)["id"]
                _logger.info(
                    f"🚀 Creating new project... project {project_name} created!"
                )
            else:
                if project["type"] != "gen_ai":
                    raise Exception(
                        f"Project {project_name} is not a Galileo 2.0 project"
                    )
                self.project_id = project["id"]

            log_stream = self.get_log_stream_by_name(
                project_id=self.project_id, log_stream_name=log_stream_name
            )
            if log_stream is None:
                self.log_stream_id = self.create_log_stream(
                    project_id=self.project_id, log_stream_name=log_stream_name
                )["id"]
                _logger.info(
                    f"🚀 Creating new log stream... log stream {log_stream_name} created!"
                )
            else:
                self.log_stream_id = log_stream["id"]

    def get_api_url(self) -> str:
        console_url = getenv("GALILEO_CONSOLE_URL")
        if console_url is None:
            # TODO: Set to the multi-tenant cluster when it's ready
            raise Exception("GALILEO_CONSOLE_URL must be set")
        if any(map(console_url.__contains__, ["localhost", "127.0.0.1"])):
            api_url = "http://localhost:8088"
        else:
            api_url = console_url.replace("console", "api")
        return api_url

    def get_token(self) -> str:
        api_key = getenv("GALILEO_API_KEY")
        if api_key:
            return self.api_key_login(api_key).get("access_token", "")

        raise Exception("GALILEO_API_KEY must be set")

    def healthcheck(self) -> bool:
        async_run(
            make_request(
                RequestMethod.GET, base_url=self.base_url, endpoint=Routes.healthcheck
            )
        )
        return True

    def api_key_login(self, api_key: str) -> dict[str, str]:
        return async_run(
            make_request(
                RequestMethod.POST,
                base_url=self.base_url,
                endpoint=Routes.api_key_login,
                json={"api_key": api_key},
            )
        )

    @property
    def base_url(self) -> str:
        return self.api_url

    @property
    def auth_header(self) -> dict[str, str]:
        return {"Authorization": f"Bearer {self.token}"}

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
        # Check to see if our token is expired before making a request
        # and refresh token if it's expired
        if endpoint not in [Routes.login, Routes.api_key_login] and self.token:
            claims = jwt.decode(self.token, options={"verify_signature": False})
            if claims.get("exp", 0) < time():
                self.token = self.get_token()

        if json_request_only:
            content_headers = HttpHeaders.accept_json()
        else:
            content_headers = HttpHeaders.json()
        headers = {**self.auth_header, **content_headers}
        return ApiClient.make_request_sync(
            request_method=request_method,
            base_url=self.base_url,
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
        # Check to see if our token is expired before making a request
        # and refresh token if it's expired
        if endpoint not in [Routes.login, Routes.api_key_login] and self.token:
            claims = jwt.decode(self.token, options={"verify_signature": False})
            if claims.get("exp", 0) < time():
                self.token = self.get_token()

        if json_request_only:
            content_headers = HttpHeaders.accept_json()
        else:
            content_headers = HttpHeaders.json()
        headers = {**self.auth_header, **content_headers}
        await make_request(
            request_method=request_method,
            base_url=self.base_url,
            endpoint=endpoint,
            json=json,
            data=data,
            files=files,
            params=params,
            headers=headers,
        )

    async def ingest_traces(
        self, traces_ingest_request: TracesIngestRequest
    ) -> dict[str, str]:
        traces_ingest_request.log_stream_id = self.log_stream_id
        json = traces_ingest_request.model_dump()

        return await self._make_async_request(
            RequestMethod.POST,
            endpoint=Routes.traces.format(project_id=self.project_id),
            json=json,
        )

    def ingest_traces_sync(
        self, traces_ingest_request: TracesIngestRequest
    ) -> dict[str, str]:
        traces_ingest_request.log_stream_id = self.log_stream_id
        json = traces_ingest_request.model_dump()

        return self._make_request(
            RequestMethod.POST,
            endpoint=Routes.traces.format(project_id=self.project_id),
            json=json,
        )

    def get_project_by_name(self, project_name: str) -> Any | None:
        projects = self._make_request(
            RequestMethod.GET,
            endpoint=Routes.projects,
            params={"project_name": project_name},
        )
        if len(projects) < 1:
            return None
        return projects[0]

    def create_project(self, project_name: str) -> dict[str, str]:
        return self._make_request(
            RequestMethod.POST,
            endpoint=Routes.projects,
            # Default project type is gen_ai (Galileo 2.0)
            json={"name": project_name, "type": "gen_ai"},
        )

    def get_log_stream_by_name(
        self, project_id: str, log_stream_name: str
    ) -> Any | None:
        log_streams = self._make_request(
            RequestMethod.GET,
            # TODO: update to an endpoint that allows filtering by name
            endpoint=Routes.log_streams.format(project_id=project_id),
        )
        if len(log_streams) < 1:
            return None
        for log_stream in log_streams:
            if log_stream["name"] == log_stream_name:
                return log_stream
        return None

    def create_log_stream(
        self, project_id: str, log_stream_name: str
    ) -> dict[str, str]:
        return self._make_request(
            RequestMethod.POST,
            endpoint=Routes.log_streams.format(project_id=project_id),
            json={"name": log_stream_name},
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
            base_url=base_url,
            timeout=Timeout(read_timeout, connect=5.0),
            verify=not skip_ssl_validation,
        ) as client:
            response = client.request(
                method=request_method.value, url=url, timeout=read_timeout, **kwargs
            )
            CoreApiClient.validate_response(response)
            return response.json()
