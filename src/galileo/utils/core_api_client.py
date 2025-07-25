import logging
from typing import Any, Optional
from uuid import UUID

from galileo.config import GalileoConfig
from galileo.constants.routes import Routes
from galileo.schema.trace import LogRecordsSearchRequest, SessionCreateRequest, TracesIngestRequest
from galileo_core.constants.request_method import RequestMethod

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
    """

    project_id: Optional[str] = None
    log_stream_id: Optional[str] = None
    config: GalileoConfig

    def __init__(
        self, project_id: Optional[str] = None, log_stream_id: Optional[str] = None, experiment_id: Optional[str] = None
    ):
        self.config = GalileoConfig.get()
        self.project_id = project_id
        self.log_stream_id = log_stream_id
        self.experiment_id = experiment_id

        if self.log_stream_id is None and self.experiment_id is None:
            raise ValueError("log_stream_id or experiment_id must be set")

    def _make_request(
        self,
        request_method: RequestMethod,
        endpoint: str,
        json: Optional[dict] = None,
        data: Optional[dict] = None,
        files: Optional[dict] = None,
        params: Optional[dict] = None,
    ) -> Any:
        return self.config.api_client.request(
            method=request_method, path=endpoint, json=json, data=data, files=files, params=params
        )

    async def _make_async_request(
        self,
        request_method: RequestMethod,
        endpoint: str,
        json: Optional[dict] = None,
        data: Optional[dict] = None,
        files: Optional[dict] = None,
        params: Optional[dict] = None,
    ) -> Any:
        return await self.config.api_client.arequest(
            method=request_method, path=endpoint, json=json, data=data, files=files, params=params
        )

    async def ingest_traces(self, traces_ingest_request: TracesIngestRequest) -> dict[str, str]:
        if self.experiment_id:
            traces_ingest_request.experiment_id = UUID(self.experiment_id)
        elif self.log_stream_id:
            traces_ingest_request.log_stream_id = UUID(self.log_stream_id)

        json = traces_ingest_request.model_dump(mode="json")

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
