import logging
from threading import local
from typing import Any
from uuid import UUID

import httpx

from galileo.config import GalileoPythonConfig
from galileo.constants.routes import Routes
from galileo.schema.trace import (
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

    project_id: str | None = None
    log_stream_id: str | None = None
    config: GalileoPythonConfig

    def __init__(
        self, project_id: str | None = None, log_stream_id: str | None = None, experiment_id: str | None = None
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
        json: dict | None = None,
        data: dict | None = None,
        files: dict | None = None,
        params: dict | None = None,
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
    """Client that sends traces/spans directly to the Galileo ingest service.

    Used when the ingest service healthz check succeeds, posting to the dedicated
    Go ingest service instead of the standard API client.
    """

    def __init__(
        self,
        project_id: str,
        base_url: str,
        api_key: str,
        log_stream_id: str | None = None,
        experiment_id: str | None = None,
    ) -> None:
        self.project_id = project_id
        self.log_stream_id = log_stream_id
        self.experiment_id = experiment_id
        self.base_url = base_url.rstrip("/")
        self._headers = {
            "Content-Type": "application/json",
            "Galileo-API-Key": api_key,
            "X-Galileo-SDK": get_sdk_header(),
        }
        self._thread_local = local()

    @property
    def _client(self) -> httpx.AsyncClient:
        """Per-thread AsyncClient to avoid cross-event-loop errors."""
        if not hasattr(self._thread_local, "client"):
            self._thread_local.client = httpx.AsyncClient(timeout=60)
        return self._thread_local.client

    @async_warn_catch_exception(logger=_logger)
    async def ingest_traces(self, traces_ingest_request: TracesIngestRequest) -> dict[str, Any]:
        if self.experiment_id:
            traces_ingest_request.experiment_id = UUID(self.experiment_id)
        elif self.log_stream_id:
            traces_ingest_request.log_stream_id = UUID(self.log_stream_id)

        url = f"{self.base_url}{Routes.ingest_traces.format(project_id=self.project_id)}"
        payload = traces_ingest_request.model_dump(mode="json", exclude_none=True)
        _logger.info("IngestTraces: posting %d trace(s) to %s", len(traces_ingest_request.traces), url)
        resp = await self._client.post(url, json=payload, headers=self._headers)
        resp.raise_for_status()
        return resp.json()

    @async_warn_catch_exception(logger=_logger)
    async def ingest_spans(self, spans_ingest_request: SpansIngestRequest) -> dict[str, Any]:
        if self.experiment_id:
            spans_ingest_request.experiment_id = UUID(self.experiment_id)
        elif self.log_stream_id:
            spans_ingest_request.log_stream_id = UUID(self.log_stream_id)

        url = f"{self.base_url}{Routes.ingest_spans.format(project_id=self.project_id)}"
        payload = spans_ingest_request.model_dump(mode="json", exclude_none=True)
        _logger.info("IngestTraces: posting %d span(s) to %s", len(spans_ingest_request.spans), url)
        resp = await self._client.post(url, json=payload, headers=self._headers)
        resp.raise_for_status()
        return resp.json()

    @async_warn_catch_exception(logger=_logger)
    async def update_trace(self, trace_update_request: TraceUpdateRequest) -> dict[str, Any]:
        if self.experiment_id:
            trace_update_request.experiment_id = UUID(self.experiment_id)
        elif self.log_stream_id:
            trace_update_request.log_stream_id = UUID(self.log_stream_id)

        url = (
            f"{self.base_url}{Routes.trace.format(project_id=self.project_id, trace_id=trace_update_request.trace_id)}"
        )
        payload = trace_update_request.model_dump(mode="json")
        resp = await self._client.patch(url, json=payload, headers=self._headers)
        resp.raise_for_status()
        return resp.json()

    @async_warn_catch_exception(logger=_logger)
    async def update_span(self, span_update_request: SpanUpdateRequest) -> dict[str, Any]:
        if self.experiment_id:
            span_update_request.experiment_id = UUID(self.experiment_id)
        elif self.log_stream_id:
            span_update_request.log_stream_id = UUID(self.log_stream_id)

        url = f"{self.base_url}{Routes.span.format(project_id=self.project_id, span_id=span_update_request.span_id)}"
        payload = span_update_request.model_dump(mode="json")
        resp = await self._client.patch(url, json=payload, headers=self._headers)
        resp.raise_for_status()
        return resp.json()

    @async_warn_catch_exception(logger=_logger)
    async def create_session(self, session_create_request: SessionCreateRequest) -> dict[str, Any]:
        if self.experiment_id:
            session_create_request.experiment_id = UUID(self.experiment_id)
        elif self.log_stream_id:
            session_create_request.log_stream_id = UUID(self.log_stream_id)

        url = f"{self.base_url}{Routes.sessions.format(project_id=self.project_id)}"
        payload = session_create_request.model_dump(mode="json")
        resp = await self._client.post(url, json=payload, headers=self._headers)
        resp.raise_for_status()
        return resp.json()

    async def get_sessions(self, session_search_request: LogRecordsSearchRequest) -> dict[str, Any]:
        if self.experiment_id:
            session_search_request.experiment_id = UUID(self.experiment_id)
        elif self.log_stream_id:
            session_search_request.log_stream_id = UUID(self.log_stream_id)

        url = f"{self.base_url}{Routes.sessions_search.format(project_id=self.project_id)}"
        payload = session_search_request.model_dump(mode="json")
        resp = await self._client.post(url, json=payload, headers=self._headers)
        resp.raise_for_status()
        return resp.json()
