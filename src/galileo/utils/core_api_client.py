import logging
from os import getenv
from typing import Any, Optional
from urllib.parse import urljoin
from uuid import UUID

from httpx import Client, Timeout

from galileo.api_client import GalileoApiClient
from galileo.constants.routes import Routes
from galileo.schema.trace import (
    LogRecordsSearchRequest,
    SessionCreateRequest,
    SpansIngestRequest,
    SpanUpdateRequest,
    TracesIngestRequest,
    TraceUpdateRequest,
)
from galileo.utils.request import HttpHeaders, make_request
from galileo_core.constants.request_method import RequestMethod
from galileo_core.helpers.api_client import ApiClient as CoreApiClient

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
    client_type_header_name: str = "client-type"
    client_type_header_value: str = "sdk-python"

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
        experiment_id: Optional[str] = None,
    ):
        self.api_url = GalileoApiClient.get_api_url(base_url)
        self.api_key = api_key or getenv("GALILEO_API_KEY", "")  # type: ignore[assignment]

        if not self.api_url or not self.api_key:
            raise ValueError("api_url and api_key must be set")

        self.project_id = project_id
        self.log_stream_id = log_stream_id
        self.experiment_id = experiment_id

        if self.log_stream_id is None and self.experiment_id is None:
            raise ValueError("log_stream_id or experiment_id must be set")

    @property
    def auth_header(self) -> dict[str, Optional[str]]:
        return {self.api_key_header_name: self.api_key}

    @property
    def client_type_header(self) -> dict[str, Optional[str]]:
        return {self.client_type_header_name: self.client_type_header_value}

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
        headers = {**self.auth_header, **content_headers, **self.client_type_header}
        result = GalileoCoreApiClient.make_request_sync(
            request_method=request_method,
            base_url=self.api_url,
            endpoint=endpoint,
            json=json,
            data=data,
            files=files,
            params=params,
            headers=headers,
        )
        return result

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
        if self.experiment_id:
            traces_ingest_request.experiment_id = UUID(self.experiment_id)
        elif self.log_stream_id:
            traces_ingest_request.log_stream_id = UUID(self.log_stream_id)

        json = traces_ingest_request.model_dump(mode="json")

        print(f"calling ingest traces for {traces_ingest_request.traces[0].id}")

        return await self._make_async_request(
            RequestMethod.POST, endpoint=Routes.traces.format(project_id=self.project_id), json=json
        )

    def ingest_traces_sync(self, traces_ingest_request: TracesIngestRequest) -> dict[str, str]:
        if self.experiment_id:
            traces_ingest_request.experiment_id = UUID(self.experiment_id)
        elif self.log_stream_id:
            traces_ingest_request.log_stream_id = UUID(self.log_stream_id)

        json = traces_ingest_request.model_dump(mode="json")

        return self._make_request(
            RequestMethod.POST, endpoint=Routes.traces.format(project_id=self.project_id), json=json
        )

    async def ingest_spans(self, spans_ingest_request: SpansIngestRequest) -> dict[str, str]:
        if self.experiment_id:
            spans_ingest_request.experiment_id = UUID(self.experiment_id)
        elif self.log_stream_id:
            spans_ingest_request.log_stream_id = UUID(self.log_stream_id)

        json = spans_ingest_request.model_dump(mode="json")

        print(f"calling ingest spans for {spans_ingest_request.spans[0].id}")

        return await self._make_async_request(
            RequestMethod.POST, endpoint=Routes.spans.format(project_id=self.project_id), json=json
        )

    def ingest_spans_sync(self, spans_ingest_request: SpansIngestRequest) -> dict[str, str]:
        if self.experiment_id:
            spans_ingest_request.experiment_id = UUID(self.experiment_id)
        elif self.log_stream_id:
            spans_ingest_request.log_stream_id = UUID(self.log_stream_id)

        json = spans_ingest_request.model_dump(mode="json")

        return self._make_request(
            RequestMethod.POST, endpoint=Routes.spans.format(project_id=self.project_id), json=json
        )

    async def update_trace(self, trace_update_request: TraceUpdateRequest) -> dict[str, str]:
        if self.experiment_id:
            trace_update_request.experiment_id = UUID(self.experiment_id)
        elif self.log_stream_id:
            trace_update_request.log_stream_id = UUID(self.log_stream_id)

        json = trace_update_request.model_dump(mode="json")

        print(f"calling update trace for {trace_update_request.trace_id}")

        return await self._make_async_request(
            RequestMethod.PATCH,
            endpoint=Routes.trace.format(project_id=self.project_id, trace_id=trace_update_request.trace_id),
            json=json,
        )

    def update_trace_sync(self, trace_update_request: TraceUpdateRequest) -> dict[str, str]:
        if self.experiment_id:
            trace_update_request.experiment_id = UUID(self.experiment_id)
        elif self.log_stream_id:
            trace_update_request.log_stream_id = UUID(self.log_stream_id)

        json = trace_update_request.model_dump(mode="json")

        return self._make_request(
            RequestMethod.PATCH,
            endpoint=Routes.trace.format(project_id=self.project_id, trace_id=trace_update_request.trace_id),
            json=json,
        )

    async def update_span(self, span_update_request: SpanUpdateRequest) -> dict[str, str]:
        if self.experiment_id:
            span_update_request.experiment_id = UUID(self.experiment_id)
        elif self.log_stream_id:
            span_update_request.log_stream_id = UUID(self.log_stream_id)

        json = span_update_request.model_dump(mode="json")

        print(f"calling update span for {span_update_request.span_id}")

        return await self._make_async_request(
            RequestMethod.PATCH,
            endpoint=Routes.span.format(project_id=self.project_id, span_id=span_update_request.span_id),
            json=json,
        )

    def update_span_sync(self, span_update_request: SpanUpdateRequest) -> dict[str, str]:
        if self.experiment_id:
            span_update_request.experiment_id = UUID(self.experiment_id)
        elif self.log_stream_id:
            span_update_request.log_stream_id = UUID(self.log_stream_id)

        json = span_update_request.model_dump(mode="json")

        return self._make_request(
            RequestMethod.PATCH,
            endpoint=Routes.span.format(project_id=self.project_id, span_id=span_update_request.span_id),
            json=json,
        )

    def create_session_sync(self, session_create_request: SessionCreateRequest) -> dict[str, str]:
        if self.experiment_id:
            session_create_request.experiment_id = UUID(self.experiment_id)
        elif self.log_stream_id:
            session_create_request.log_stream_id = UUID(self.log_stream_id)

        json = session_create_request.model_dump(mode="json")

        response = self._make_request(
            RequestMethod.POST, endpoint=Routes.sessions.format(project_id=self.project_id), json=json
        )

        return response

    async def create_session(self, session_create_request: SessionCreateRequest) -> dict[str, str]:
        if self.experiment_id:
            session_create_request.experiment_id = UUID(self.experiment_id)
        elif self.log_stream_id:
            session_create_request.log_stream_id = UUID(self.log_stream_id)

        json = session_create_request.model_dump(mode="json")

        return await self._make_async_request(
            RequestMethod.POST, endpoint=Routes.sessions.format(project_id=self.project_id), json=json
        )

    async def get_sessions(self, session_search_request: LogRecordsSearchRequest) -> dict[str, str]:
        if self.experiment_id:
            session_search_request.experiment_id = UUID(self.experiment_id)
        elif self.log_stream_id:
            session_search_request.log_stream_id = UUID(self.log_stream_id)

        json = session_search_request.model_dump(mode="json")

        return await self._make_async_request(
            RequestMethod.POST, endpoint=Routes.sessions_search.format(project_id=self.project_id), json=json
        )

    def get_sessions_sync(self, session_search_request: LogRecordsSearchRequest) -> dict[str, str]:
        if self.experiment_id:
            session_search_request.experiment_id = UUID(self.experiment_id)
        elif self.log_stream_id:
            session_search_request.log_stream_id = UUID(self.log_stream_id)

        json = session_search_request.model_dump(mode="json")

        return self._make_request(
            RequestMethod.POST, endpoint=Routes.sessions_search.format(project_id=self.project_id), json=json
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
