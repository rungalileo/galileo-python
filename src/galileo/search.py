import logging
from enum import Enum
from typing import Optional

from galileo.config import GalileoPythonConfig
from galileo.resources.api.trace import (
    query_sessions_projects_project_id_sessions_search_post,
    query_spans_projects_project_id_spans_search_post,
    query_traces_projects_project_id_traces_search_post,
)
from galileo.resources.models import (
    HTTPValidationError,
    LogRecordsQueryRequest,
    LogRecordsQueryResponse,
    LogRecordsSortClause,
)
from galileo.schema.filters import FilterType

logger = logging.getLogger(__name__)


class RecordType(str, Enum):
    SPAN = "spans"
    TRACE = "traces"
    SESSION = "sessions"


class Search:
    config: GalileoPythonConfig

    def __init__(self) -> None:
        self.config = GalileoPythonConfig.get()

    def query(
        self,
        project_id: str,
        record_type: RecordType,
        experiment_id: Optional[str] = None,
        log_stream_id: Optional[str] = None,
        filters: Optional[list[FilterType]] = None,
        sort: Optional[LogRecordsSortClause] = None,
        limit: int = 100,
        starting_token: int = 0,
    ) -> LogRecordsQueryResponse:
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

        response = api_function.sync(client=self.config.api_client, project_id=str(project_id), body=body)

        if isinstance(response, HTTPValidationError):
            raise ValueError(response.detail)
        if not response:
            raise ValueError(f"Failed to query for {record_type.value}")

        return response


def get_spans(
    project_id: str,
    experiment_id: Optional[str] = None,
    log_stream_id: Optional[str] = None,
    filters: Optional[list[FilterType]] = None,
    sort: Optional[LogRecordsSortClause] = None,
    limit: int = 100,
    starting_token: int = 0,
) -> LogRecordsQueryResponse:
    """Queries for spans in a project.

    Parameters
    ----------
    project_id
        The unique identifier of the project.
    experiment_id
        Filter records by a specific experiment ID.
    log_stream_id
        Filter records by a specific run ID.
    filters
        A list of filters to apply to the query.
    sort
        A sort clause to order the query results.
    limit
        The maximum number of records to return.
    starting_token
        The token for the next page of results.

    Returns
    -------
    A LogRecordsQueryResponse object containing the query results.
    """
    return Search().query(
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
    project_id: str,
    experiment_id: Optional[str] = None,
    log_stream_id: Optional[str] = None,
    filters: Optional[list[FilterType]] = None,
    sort: Optional[LogRecordsSortClause] = None,
    limit: int = 100,
    starting_token: int = 0,
) -> LogRecordsQueryResponse:
    """Queries for traces in a project.

    Parameters
    ----------
    project_id
        The unique identifier of the project.
    experiment_id
        Filter records by a specific experiment ID.
    log_stream_id
        Filter records by a specific run ID.
    filters
        A list of filters to apply to the query.
    sort
        A sort clause to order the query results.
    limit
        The maximum number of records to return.
    starting_token
        The token for the next page of results.

    Returns
    -------
    A LogRecordsQueryResponse object containing the query results.
    """
    return Search().query(
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
    project_id: str,
    experiment_id: Optional[str] = None,
    log_stream_id: Optional[str] = None,
    filters: Optional[list[FilterType]] = None,
    sort: Optional[LogRecordsSortClause] = None,
    limit: int = 100,
    starting_token: int = 0,
) -> LogRecordsQueryResponse:
    """Queries for sessions in a project.

    Parameters
    ----------
    project_id
        The unique identifier of the project.
    experiment_id
        Filter records by a specific experiment ID.
    log_stream_id
        Filter records by a specific run ID.
    filters
        A list of filters to apply to the query.
    sort
        A sort clause to order the query results.
    limit
        The maximum number of records to return.
    starting_token
        The token for the next page of results.

    Returns
    -------
    A LogRecordsQueryResponse object containing the query results.
    """
    return Search().query(
        project_id=project_id,
        record_type=RecordType.SESSION,
        experiment_id=experiment_id,
        log_stream_id=log_stream_id,
        filters=filters,
        sort=sort,
        limit=limit,
        starting_token=starting_token,
    )
