import logging
import os
from typing import Any, Optional
from uuid import UUID

import httpx

from galileo.config import GalileoPythonConfig
from galileo.constants.routes import Routes
from galileo.schema.trace import (
    LoggingMethod,
    LogRecordsSearchRequest,
    SessionCreateRequest,
    SpansIngestRequest,
    SpanUpdateRequest,
    TracesIngestRequest,
    TraceUpdateRequest,
)
from galileo.utils.decorators import async_warn_catch_exception
from galileo.utils.headers_data import get_sdk_header
from galileo_core.constants.http_headers import HttpHeaders
from galileo_core.constants.request_method import RequestMethod

_logger = logging.getLogger(__name__)

INGEST_SERVICE_TIMEOUT_SECONDS = 120.0


class Traces:
    """
    A class for interacting with the Galileo API using the galileo_core package.
    Currently used by the GalileoLogger to create and upload traces to Galileo.

    Attributes
    ----------
    project_id : Optional[str]
        The ID of the project.
    log_stream_id : Optional[str]
        The ID of the log stream.
    """

    project_id: Optional[str] = None
    log_stream_id: Optional[str] = None
    config: GalileoPythonConfig

    def __init__(
        self, project_id: Optional[str] = None, log_stream_id: Optional[str] = None, experiment_id: Optional[str] = None
    ):
        self.config = GalileoPythonConfig.get()
        self.project_id = project_id
        self.log_stream_id = log_stream_id
        self.experiment_id = experiment_id

        if self.log_stream_id is None and self.experiment_id is None:
            raise ValueError("log_stream_id or experiment_id must be set")

    async def _make_async_request(
        self,
        request_method: RequestMethod,
        endpoint: str,
        json: Optional[dict] = None,
        data: Optional[dict] = None,
        files: Optional[dict] = None,
        params: Optional[dict] = None,
    ) -> Any:
        headers = {"X-Galileo-SDK": get_sdk_header()} | HttpHeaders.json()

        return await self.config.api_client.arequest(
            method=request_method,
            path=endpoint,
            content_headers=headers,
            json=json,
            data=data,
            files=files,
            params=params,
        )

    @async_warn_catch_exception(logger=_logger)
    async def ingest_traces(self, traces_ingest_request: TracesIngestRequest) -> dict[str, str]:
        if self.experiment_id:
            traces_ingest_request.experiment_id = UUID(self.experiment_id)
        elif self.log_stream_id:
            traces_ingest_request.log_stream_id = UUID(self.log_stream_id)

        json = traces_ingest_request.model_dump(mode="json")

        return await self._make_async_request(
            RequestMethod.POST, endpoint=Routes.traces.format(project_id=self.project_id), json=json
        )

    @async_warn_catch_exception(logger=_logger)
    async def ingest_spans(self, spans_ingest_request: SpansIngestRequest) -> dict[str, str]:
        if self.experiment_id:
            spans_ingest_request.experiment_id = UUID(self.experiment_id)
        elif self.log_stream_id:
            spans_ingest_request.log_stream_id = UUID(self.log_stream_id)

        json = spans_ingest_request.model_dump(mode="json")

        return await self._make_async_request(
            RequestMethod.POST, endpoint=Routes.spans.format(project_id=self.project_id), json=json
        )

    @async_warn_catch_exception(logger=_logger)
    async def update_trace(self, trace_update_request: TraceUpdateRequest) -> dict[str, str]:
        if self.experiment_id:
            trace_update_request.experiment_id = UUID(self.experiment_id)
        elif self.log_stream_id:
            trace_update_request.log_stream_id = UUID(self.log_stream_id)

        json = trace_update_request.model_dump(mode="json")

        return await self._make_async_request(
            RequestMethod.PATCH,
            endpoint=Routes.trace.format(project_id=self.project_id, trace_id=trace_update_request.trace_id),
            json=json,
        )

    @async_warn_catch_exception(logger=_logger)
    async def update_span(self, span_update_request: SpanUpdateRequest) -> dict[str, str]:
        if self.experiment_id:
            span_update_request.experiment_id = UUID(self.experiment_id)
        elif self.log_stream_id:
            span_update_request.log_stream_id = UUID(self.log_stream_id)

        json = span_update_request.model_dump(mode="json")

        return await self._make_async_request(
            RequestMethod.PATCH,
            endpoint=Routes.span.format(project_id=self.project_id, span_id=span_update_request.span_id),
            json=json,
        )

    @async_warn_catch_exception(logger=_logger)
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

    async def get_trace(self, trace_id: str) -> dict[str, str]:
        return await self._make_async_request(
            RequestMethod.GET, endpoint=Routes.trace.format(project_id=self.project_id, trace_id=trace_id)
        )

    async def get_span(self, span_id: str) -> dict[str, str]:
        return await self._make_async_request(
            RequestMethod.GET, endpoint=Routes.span.format(project_id=self.project_id, span_id=span_id)
        )


class IngestTraces:
    """Client for the orbit ingest service (``/ingest/traces/:project_id``).

    The ingest service accepts multimodal content blocks natively and
    runs on a separate URL from the main Galileo API.

    The service URL is resolved from ``GALILEO_INGEST_URL`` env var.
    If not set, it falls back to ``{api_url}/ingest/traces/{project_id}``.
    """

    def __init__(self, project_id: str, log_stream_id: Optional[str] = None, experiment_id: Optional[str] = None):
        self.config = GalileoPythonConfig.get()
        self.project_id = project_id
        self.log_stream_id = log_stream_id
        self.experiment_id = experiment_id

        if self.log_stream_id is None and self.experiment_id is None:
            raise ValueError("log_stream_id or experiment_id must be set")

    def _get_ingest_base_url(self) -> str:
        explicit = os.environ.get("GALILEO_INGEST_URL")
        if explicit:
            return explicit.rstrip("/")
        return str(self.config.api_url or self.config.console_url).rstrip("/")

    def _get_auth_headers(self) -> dict[str, str]:
        headers: dict[str, str] = {"Content-Type": "application/json", "X-Galileo-SDK": get_sdk_header()}
        if self.config.api_key:
            headers["Galileo-API-Key"] = self.config.api_key.get_secret_value()
        elif self.config.jwt_token:
            headers["Authorization"] = f"Bearer {self.config.jwt_token.get_secret_value()}"
        return headers

    @async_warn_catch_exception(logger=_logger)
    async def ingest_traces(self, traces_ingest_request: TracesIngestRequest) -> dict[str, Any]:
        if self.experiment_id:
            traces_ingest_request.experiment_id = UUID(self.experiment_id)
        elif self.log_stream_id:
            traces_ingest_request.log_stream_id = UUID(self.log_stream_id)

        traces_ingest_request.logging_method = LoggingMethod.python_client

        base_url = self._get_ingest_base_url()
        url = f"{base_url}{Routes.ingest_traces.format(project_id=self.project_id)}"
        json_body = traces_ingest_request.model_dump(mode="json")

        _logger.info(
            "Sending traces to ingest service",
            extra={"url": url, "project_id": self.project_id, "num_traces": len(traces_ingest_request.traces)},
        )

        async with httpx.AsyncClient(
            timeout=httpx.Timeout(INGEST_SERVICE_TIMEOUT_SECONDS, connect=10.0), verify=self.config.ssl_context
        ) as client:
            response = await client.post(url, json=json_body, headers=self._get_auth_headers())
            response.raise_for_status()
            return response.json()
