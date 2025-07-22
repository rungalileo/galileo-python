import logging
from enum import Enum
from typing import Optional, Union

from pydantic import UUID4

from galileo.base import BaseClientModel
from galileo.resources.api.trace import (
    query_sessions_projects_project_id_sessions_search_post,
    query_spans_projects_project_id_spans_search_post,
    query_traces_projects_project_id_traces_search_post,
)
from galileo.resources.models import (
    HTTPValidationError,
    LogRecordsBooleanFilter,
    LogRecordsDateFilter,
    LogRecordsIDFilter,
    LogRecordsNumberFilter,
    LogRecordsQueryRequest,
    LogRecordsQueryResponse,
    LogRecordsSortClause,
    LogRecordsTextFilter,
)

logger = logging.getLogger(__name__)


class RecordType(str, Enum):
    SPAN = "spans"
    TRACE = "traces"
    SESSION = "sessions"


FilterType = Union[
    LogRecordsBooleanFilter, LogRecordsDateFilter, LogRecordsIDFilter, LogRecordsNumberFilter, LogRecordsTextFilter
]


class Search(BaseClientModel):  # , DecorateAllMethods):
    def query(
        self,
        project_id: UUID4,
        record_type: RecordType,
        experiment_id: Optional[UUID4] = None,
        log_stream_id: Optional[str] = None,
        filters: Optional[list[FilterType]] = None,
        sort: Optional[LogRecordsSortClause] = None,
        limit: int = 100,
        starting_token: int = 0,
    ) -> LogRecordsQueryResponse:
        """
        Queries for spans, traces, or sessions in a project.
        """
        body = LogRecordsQueryRequest(
            experiment_id=experiment_id,
            log_stream_id=log_stream_id,
            filters=filters or [],
            sort=sort or LogRecordsSortClause(column_id="created_at", ascending=False),
            limit=limit,
            starting_token=starting_token,
        )

        api_function_map = {
            RecordType.SPAN: query_spans_projects_project_id_spans_search_post,
            RecordType.TRACE: query_traces_projects_project_id_traces_search_post,
            RecordType.SESSION: query_sessions_projects_project_id_sessions_search_post,
        }

        api_function = api_function_map[record_type]

        response = api_function.sync(client=self.client, project_id=str(project_id), body=body)
        logger.debug(f"Query {record_type.value} response: {response}")

        if not isinstance(response, LogRecordsQueryResponse):
            if isinstance(response, HTTPValidationError):
                logger.error(f"Validation error when querying for {record_type.value}: {response}")
            else:
                logger.error(f"Failed to query for {record_type.value}. Response: {response}")
            # Return an empty response on failure to avoid TypeErrors downstream
            return LogRecordsQueryResponse(records=[])

        return response


def get_spans(
    project_id: UUID4,
    experiment_id: Optional[UUID4] = None,
    log_stream_id: Optional[str] = None,
    filters: Optional[list[FilterType]] = None,
    sort: Optional[LogRecordsSortClause] = None,
    limit: int = 100,
    starting_token: int = 0,
) -> LogRecordsQueryResponse:
    """
    A helper function to query for spans in a project.
    """
    search_client = Search()
    return search_client.query(
        project_id=project_id,
        record_type=RecordType.SPAN,
        experiment_id=experiment_id,
        log_stream_id=log_stream_id,
        filters=filters,
        sort=sort,
        limit=limit,
        starting_token=starting_token,
    )


def get_traces(
    project_id: UUID4,
    experiment_id: Optional[UUID4] = None,
    log_stream_id: Optional[str] = None,
    filters: Optional[list[FilterType]] = None,
    sort: Optional[LogRecordsSortClause] = None,
    limit: int = 100,
    starting_token: int = 0,
) -> LogRecordsQueryResponse:
    """
    A helper function to query for traces in a project.
    """
    search_client = Search()
    return search_client.query(
        project_id=project_id,
        record_type=RecordType.TRACE,
        experiment_id=experiment_id,
        log_stream_id=log_stream_id,
        filters=filters,
        sort=sort,
        limit=limit,
        starting_token=starting_token,
    )


def get_sessions(
    project_id: UUID4,
    experiment_id: Optional[UUID4] = None,
    log_stream_id: Optional[str] = None,
    filters: Optional[list[FilterType]] = None,
    sort: Optional[LogRecordsSortClause] = None,
    limit: int = 100,
    starting_token: int = 0,
) -> LogRecordsQueryResponse:
    """
    A helper function to query for sessions in a project.
    """
    search_client = Search()
    return search_client.query(
        project_id=project_id,
        record_type=RecordType.SESSION,
        experiment_id=experiment_id,
        log_stream_id=log_stream_id,
        filters=filters,
        sort=sort,
        limit=limit,
        starting_token=starting_token,
    )
