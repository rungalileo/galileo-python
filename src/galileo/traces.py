import logging
from typing import Optional
from uuid import UUID

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

    async def ingest_traces(self, traces_ingest_request: TracesIngestRequest) -> dict[str, str]:
        if self.experiment_id:
            traces_ingest_request.experiment_id = UUID(self.experiment_id)
        elif self.log_stream_id:
            traces_ingest_request.log_stream_id = UUID(self.log_stream_id)

        json = traces_ingest_request.model_dump(mode="json")

        return await self.config.api_client.arequest(
            method=RequestMethod.POST, path=Routes.traces.format(project_id=self.project_id), json=json
        )

    async def ingest_spans(self, spans_ingest_request: SpansIngestRequest) -> dict[str, str]:
        if self.experiment_id:
            spans_ingest_request.experiment_id = UUID(self.experiment_id)
        elif self.log_stream_id:
            spans_ingest_request.log_stream_id = UUID(self.log_stream_id)

        json = spans_ingest_request.model_dump(mode="json")

        return await self.config.api_client.arequest(
            method=RequestMethod.POST, path=Routes.spans.format(project_id=self.project_id), json=json
        )

    async def update_trace(self, trace_update_request: TraceUpdateRequest) -> dict[str, str]:
        if self.experiment_id:
            trace_update_request.experiment_id = UUID(self.experiment_id)
        elif self.log_stream_id:
            trace_update_request.log_stream_id = UUID(self.log_stream_id)

        json = trace_update_request.model_dump(mode="json")

        return await self.config.api_client.arequest(
            method=RequestMethod.PATCH,
            path=Routes.trace.format(project_id=self.project_id, trace_id=trace_update_request.trace_id),
            json=json,
        )

    async def update_span(self, span_update_request: SpanUpdateRequest) -> dict[str, str]:
        if self.experiment_id:
            span_update_request.experiment_id = UUID(self.experiment_id)
        elif self.log_stream_id:
            span_update_request.log_stream_id = UUID(self.log_stream_id)

        json = span_update_request.model_dump(mode="json")

        return await self.config.api_client.arequest(
            method=RequestMethod.PATCH,
            path=Routes.span.format(project_id=self.project_id, span_id=span_update_request.span_id),
            json=json,
        )

    async def create_session(self, session_create_request: SessionCreateRequest) -> dict[str, str]:
        if self.experiment_id:
            session_create_request.experiment_id = UUID(self.experiment_id)
        elif self.log_stream_id:
            session_create_request.log_stream_id = UUID(self.log_stream_id)

        json = session_create_request.model_dump(mode="json")

        return await self.config.api_client.arequest(
            method=RequestMethod.POST, path=Routes.sessions.format(project_id=self.project_id), json=json
        )

    async def get_sessions(self, session_search_request: LogRecordsSearchRequest) -> dict[str, str]:
        if self.experiment_id:
            session_search_request.experiment_id = UUID(self.experiment_id)
        elif self.log_stream_id:
            session_search_request.log_stream_id = UUID(self.log_stream_id)

        json = session_search_request.model_dump(mode="json")

        return await self.config.api_client.arequest(
            method=RequestMethod.POST, path=Routes.sessions_search.format(project_id=self.project_id), json=json
        )

    async def get_trace(self, trace_id: str) -> dict[str, str]:
        return await self.config.api_client.arequest(
            method=RequestMethod.GET, path=Routes.trace.format(project_id=self.project_id, trace_id=trace_id)
        )

    async def get_span(self, span_id: str) -> dict[str, str]:
        return await self.config.api_client.arequest(
            method=RequestMethod.GET, path=Routes.span.format(project_id=self.project_id, span_id=span_id)
        )
