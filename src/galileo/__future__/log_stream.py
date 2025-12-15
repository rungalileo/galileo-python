from __future__ import annotations

import builtins
import logging
from collections.abc import Iterator
from datetime import datetime
from typing import TYPE_CHECKING, Any

from galileo import galileo_context
from galileo.__future__.shared.base import StateManagementMixin, SyncState
from galileo.__future__.shared.exceptions import ValidationError
from galileo.__future__.shared.query_result import QueryResult
from galileo.config import GalileoPythonConfig
from galileo.export import ExportClient
from galileo.log_streams import LogStreams
from galileo.resources.api.trace import (
    sessions_available_columns_projects_project_id_sessions_available_columns_post,
    spans_available_columns_projects_project_id_spans_available_columns_post,
    traces_available_columns_projects_project_id_traces_available_columns_post,
)
from galileo.resources.models import LLMExportFormat, LogRecordsSortClause, RootType
from galileo.resources.models.http_validation_error import HTTPValidationError
from galileo.resources.models.log_records_available_columns_request import LogRecordsAvailableColumnsRequest
from galileo.resources.models.log_records_available_columns_response import LogRecordsAvailableColumnsResponse
from galileo.schema.filters import FilterType
from galileo.schema.metrics import GalileoMetrics, LocalMetricConfig, Metric
from galileo.search import RecordType, Search
from galileo.utils.validations import require_exactly_one

if TYPE_CHECKING:
    from galileo.__future__.shared.column import ColumnCollection

logger = logging.getLogger(__name__)

# Mapping from RecordType (plural) to RootType (singular)
RECORD_TYPE_TO_ROOT_TYPE = {
    RecordType.SPAN: RootType.SPAN,
    RecordType.TRACE: RootType.TRACE,
    RecordType.SESSION: RootType.SESSION,
}


class LogStream(StateManagementMixin):
    """
    Object-centric interface for Galileo log streams.

    This class provides an intuitive way to work with Galileo log streams,
    offering methods for managing log streams and their associated metrics.

    Attributes
    ----------
        created_at (datetime.datetime): When the log stream was created.
        created_by (str): The user who created the log stream.
        id (str): The unique log stream identifier.
        name (str): The log stream name.
        project_id (str): The ID of the project this log stream belongs to.
        project_name (str | None): The name of the project. May be None if the log stream
            was retrieved using project_id only, as the API doesn't return this field.
        updated_at (datetime.datetime): When the log stream was last updated.
        additional_properties (dict): Additional properties of the log stream.

    Examples
    --------
        # Create a new log stream and persist it
        log_stream = LogStream(name="Production Logs", project_name="My AI Project").create()

        # Get an existing log stream
        log_stream = LogStream.get(name="Production Logs", project_name="My AI Project")

        # LogStreams can also be created through Project instances
        from galileo.__future__ import Project

        project = Project.get(name="My AI Project")
        log_stream = project.create_log_stream(name="Production Logs")

        # Enable metrics on the log stream
        from galileo.schema.metrics import GalileoMetrics
        local_metrics = log_stream.enable_metrics([
            GalileoMetrics.correctness,
            GalileoMetrics.completeness,
            "context_relevance"
        ])

        # Refresh log stream state from API
        log_stream.refresh()
    """

    created_at: datetime | None
    created_by: str | None
    id: str | None
    name: str
    project_id: str | None
    project_name: str | None  # May not be available when retrieved from API
    updated_at: datetime | None
    additional_properties: dict[str, Any]  # TODO: We need to validate if we will keep this one.

    def __str__(self) -> str:
        """String representation of the log stream."""
        return f"LogStream(name='{self.name}', id='{self.id}', project_id='{self.project_id}')"

    def __repr__(self) -> str:
        """Detailed string representation of the log stream."""
        return f"LogStream(name='{self.name}', id='{self.id}', project_id='{self.project_id}', created_at='{self.created_at}')"

    @require_exactly_one("project_id", "project_name")
    def __init__(self, name: str, *, project_id: str | None = None, project_name: str | None = None) -> None:
        """
        Initialize a LogStream instance locally.

        Creates a local log stream object that exists only in memory until .create()
        is called to persist it to the API.

        Args:
            name (str): The name of the log stream to create.
            project_id (Optional[str]): The project ID. Exactly one of project_id or project_name must be provided.
            project_name (Optional[str]): The project name. Exactly one of project_id or project_name must be provided.

        Raises
        ------
            ValidationError: If name is not provided, or if neither/both project_id and project_name are provided.

        Examples
        --------
            # Create by project ID
            log_stream = LogStream(name="Production Logs", project_id="project-123")

            # Create by project name
            log_stream = LogStream(name="Production Logs", project_name="My AI Project")
        """
        super().__init__()

        if not name:
            raise ValidationError("'name' must be provided to create a log stream.")

        # Initialize attributes locally
        self.name = name
        self.project_id = project_id
        self.project_name = project_name  # May be None; not returned by API
        self.id = None
        self.created_at = None
        self.created_by = None
        self.updated_at = None
        self.additional_properties = {}

        # Set initial state
        self._set_state(SyncState.LOCAL_ONLY)

    def create(self) -> LogStream:
        """
        Persist this log stream to the API.

        Returns
        -------
            LogStream: This log stream instance with updated attributes from the API.

        Raises
        ------
            ValueError: If the log stream name or project information is not set.
            Exception: If the API call fails.

        Examples
        --------
            log_stream = LogStream(name="Production Logs", project_name="My AI Project").create()
            assert log_stream.is_synced()
        """
        if not self.name:
            raise ValueError("Log stream name is not set. Cannot create log stream without a name.")

        if not self.project_id and not self.project_name:
            raise ValueError(
                "Project information is not set. Cannot create log stream without project_id or project_name."
            )

        try:
            logger.info(f"LogStream.create: name='{self.name}' project_id='{self.project_id}' - started")
            log_streams_service = LogStreams()
            created_log_stream = log_streams_service.create(
                name=self.name, project_id=self.project_id, project_name=self.project_name
            )

            # Update attributes from response
            self.created_at = created_log_stream.created_at
            self.created_by = created_log_stream.created_by
            self.id = created_log_stream.id
            self.name = created_log_stream.name
            self.project_id = created_log_stream.project_id
            self.updated_at = created_log_stream.updated_at
            self.additional_properties = created_log_stream.additional_properties
            # Note: project_name is preserved if it was set, but API doesn't return it

            # Set state to synced
            self._set_state(SyncState.SYNCED)
            logger.info(f"LogStream.create: id='{self.id}' - completed")
            return self
        except Exception as e:
            self._set_state(SyncState.FAILED_SYNC, error=e)
            logger.error(f"LogStream.create: name='{self.name}' - failed: {e}")
            raise

    @classmethod
    def _create_empty(cls) -> LogStream:
        """Internal constructor bypassing __init__ for API hydration."""
        instance = cls.__new__(cls)
        super(LogStream, instance).__init__()
        return instance

    @classmethod
    def _from_api_response(cls, retrieved_log_stream: Any) -> LogStream:
        """
        Factory method to create a LogStream instance from an API response.

        Args:
            retrieved_log_stream: The log stream data retrieved from the API.

        Returns
        -------
            LogStream: A new LogStream instance populated with the API data.
        """
        instance = cls._create_empty()
        instance.created_at = retrieved_log_stream.created_at
        instance.created_by = retrieved_log_stream.created_by
        instance.id = retrieved_log_stream.id
        instance.name = retrieved_log_stream.name
        instance.project_id = retrieved_log_stream.project_id
        instance.updated_at = retrieved_log_stream.updated_at
        instance.additional_properties = retrieved_log_stream.additional_properties
        instance.project_name = None  # API doesn't return project_name
        # Set state to synced since we just retrieved from API
        instance._set_state(SyncState.SYNCED)
        return instance

    @classmethod
    @require_exactly_one("project_id", "project_name")
    def get(cls, *, name: str, project_id: str | None = None, project_name: str | None = None) -> LogStream | None:
        """
        Get an existing log stream by name.

        Args:
            name (str): The log stream name.
            project_id (Optional[str]): The project ID.
            project_name (Optional[str]): The project name.

        Returns
        -------
            Optional[LogStream]: The log stream if found, None otherwise.

        Raises
        ------
            ValidationError: If neither or both project_id and project_name are provided.

        Examples
        --------
            # Get by project name
            log_stream = LogStream.get(
                name="Production Logs",
                project_name="My AI Project"
            )

            # Get by project ID
            log_stream = LogStream.get(
                name="Production Logs",
                project_id="project-123"
            )
        """
        log_streams_service = LogStreams()
        retrieved_log_stream = log_streams_service.get(name=name, project_id=project_id, project_name=project_name)
        if retrieved_log_stream is None:
            return None

        instance = cls._from_api_response(retrieved_log_stream)
        # Preserve project_name if it was provided
        if project_name is not None:
            instance.project_name = project_name
        return instance

    @classmethod
    @require_exactly_one("project_id", "project_name")
    def list(cls, *, project_id: str | None = None, project_name: str | None = None) -> list[LogStream]:
        """
        List all log streams for a project.

        Args:
            project_id (Optional[str]): The project ID.
            project_name (Optional[str]): The project name.

        Returns
        -------
            List[LogStream]: A list of log streams for the project.

        Raises
        ------
            ValidationError: If neither or both project_id and project_name are provided.

        Examples
        --------
            # List by project name
            log_streams = LogStream.list(project_name="My AI Project")

            # List by project ID
            log_streams = LogStream.list(project_id="project-123")
        """
        log_streams_service = LogStreams()
        retrieved_log_streams = log_streams_service.list(project_id=project_id, project_name=project_name)

        instances = [cls._from_api_response(retrieved_log_stream) for retrieved_log_stream in retrieved_log_streams]
        # Preserve project_name if it was provided
        if project_name is not None:
            for instance in instances:
                instance.project_name = project_name
        return instances

    def refresh(self) -> None:
        """
        Refresh this log stream's state from the API.

        Updates all attributes with the latest values from the remote API
        and sets the state to SYNCED.

        Raises
        ------
            ValueError: If the log stream ID or project_id is not set.
            Exception: If the API call fails or the log stream no longer exists.

        Examples
        --------
            log_stream.refresh()
            assert log_stream.is_synced()
        """
        if self.id is None:
            raise ValueError("Log stream ID is not set. Cannot refresh a local-only log stream.")

        if self.project_id is None:
            raise ValueError("Project ID is not set. Cannot refresh log stream without project_id.")

        try:
            logger.debug(f"LogStream.refresh: id='{self.id}' - started")
            log_streams_service = LogStreams()
            retrieved_log_stream = log_streams_service.get(id=self.id, project_id=self.project_id)

            if retrieved_log_stream is None:
                raise ValueError(f"Log stream with id '{self.id}' no longer exists")

            # Update all attributes from response
            self.created_at = retrieved_log_stream.created_at
            self.created_by = retrieved_log_stream.created_by
            self.id = retrieved_log_stream.id
            self.name = retrieved_log_stream.name
            self.project_id = retrieved_log_stream.project_id
            self.updated_at = retrieved_log_stream.updated_at
            self.additional_properties = retrieved_log_stream.additional_properties
            # Note: project_name is preserved from before refresh since API doesn't return it

            # Set state to synced
            self._set_state(SyncState.SYNCED)
            logger.debug(f"LogStream.refresh: id='{self.id}' - completed")
        except Exception as e:
            self._set_state(SyncState.FAILED_SYNC, error=e)
            logger.error(f"LogStream.refresh: id='{self.id}' - failed: {e}")
            raise

    def get_metrics(self) -> builtins.list[str]:
        """
        Get the list of metrics currently enabled on this log stream.

        Returns
        -------
            list[str]: List of metric names currently enabled.

        Raises
        ------
            ValueError: If the log stream lacks required id or project_id attributes.

        Examples
        --------
            log_stream = LogStream.get(name="Production Logs", project_name="My Project")
            current_metrics = log_stream.get_metrics()
            print(f"Currently enabled: {current_metrics}")
        """
        logger.info(f"LogStream.get_metrics: id='{self.id}' - started")
        config = GalileoConfig.get()

        settings = get_settings_projects_project_id_runs_run_id_scorer_settings_get.sync(
            project_id=self.project_id, run_id=self.id, client=config.api_client
        )

        if settings is None or not hasattr(settings, "scorers"):
            logger.info(f"LogStream.get_metrics: id='{self.id}' - no metrics enabled")
            return []

        # Extract metric names from scorer configs
        metric_names = [scorer.name for scorer in settings.scorers]
        logger.info(f"LogStream.get_metrics: id='{self.id}' found {len(metric_names)} metrics - completed")
        return metric_names

    def set_metrics(
        self, metrics: builtins.list[GalileoMetrics | Metric | LocalMetricConfig | str]
    ) -> builtins.list[LocalMetricConfig]:
        """
        Set (replace) the metrics on this log stream.

        This replaces any existing metrics with the new list. Alias for enable_metrics
        with clearer naming intent.

        Args:
            metrics: List of metrics to set. Supports:
                - GalileoMetrics enum values (e.g., GalileoMetrics.correctness)
                - Metric objects (including from Metric.get(id="..."))
                - LocalMetricConfig objects for custom scoring functions
                - String names of built-in metrics

        Returns
        -------
            List[LocalMetricConfig]: Local metric configurations that must be
                computed client-side.

        Raises
        ------
            ValueError: If any specified metrics are unknown.

        Examples
        --------
            from galileo.__future__ import Metric, LogStream

            log_stream = LogStream.get(name="Production Logs", project_name="My Project")

            # Set metrics (replaces existing)
            log_stream.set_metrics([
                Metric.metrics.correctness,
                Metric.metrics.completeness,
                Metric.get(id="metric-from-console-uuid"),  # From console
            ])
        """
        try:
            logger.info(f"LogStream.enable_metrics: id='{self.id}' metrics={[str(m) for m in metrics]} - started")
            log_streams_service = LogStreams()
            log_stream = log_streams_service.get(name=self.name, project_id=self.project_id)
            if log_stream is None:
                raise ValueError(f"Log stream '{self.name}' not found")
            result = log_stream.enable_metrics(metrics)
            # Set state to synced after successful operation
            self._set_state(SyncState.SYNCED)
            logger.info(f"LogStream.enable_metrics: id='{self.id}' - completed")
            return result
        except Exception as e:
            self._set_state(SyncState.FAILED_SYNC, error=e)
            logger.error(f"LogStream.enable_metrics: id='{self.id}' - failed: {e}")
            raise

    def query(
        self,
        record_type: RecordType,
        filters: builtins.list[FilterType] | None = None,
        sort: LogRecordsSortClause | None = None,
        limit: int = 100,
        starting_token: int = 0,
    ) -> QueryResult:
        """
        Query records in this log stream.

        This method provides a convenient way to search spans, traces, or sessions
        within the current log stream without needing to specify project_id or log_stream_id.

        Args:
            record_type: The type of records to query (SPAN, TRACE, or SESSION).
            filters: A list of filters to apply to the query.
            sort: A sort clause to order the query results.
            limit: The maximum number of records to return.
            starting_token: The token for the next page of results.

        Returns
        -------
            QueryResult: A list-like object containing the query results with pagination support.

        Raises
        ------
            ValueError: If the log stream lacks required id or project_id attributes.

        Examples
        --------
            from galileo.search import RecordType

            log_stream = LogStream.get(name="Production Logs", project_name="My AI Project")

            # Query with column-based filters and sort
            results = log_stream.query(
                record_type=RecordType.SPAN,
                filters=[
                    log_stream.span_columns["input"].contains("largest"),
                    log_stream.span_columns["metrics/completeness_gpt"].greater_than(0.8),
                    log_stream.span_columns["created_at"].after("2024-01-01")
                ],
                sort=log_stream.span_columns["created_at"].descending(),
                limit=50
            )

            # Access results like a list
            for record in results:
                print(record["id"], record["input"])

            # Get specific record
            first_record = results[0]

            # Pagination
            if results.has_next_page:
                next_results = results.next_page()
        """
        if self.id is None:
            raise ValueError("Log stream ID is not set. Cannot query a local-only log stream.")
        if self.project_id is None:
            raise ValueError("Project ID is not set. Cannot query log stream without project_id.")

        logger.debug(f"LogStream.query: id='{self.id}' record_type='{record_type.value}' limit={limit} - started")

        # Capture project_id and log_stream_id for use in pagination function
        project_id = self.project_id
        log_stream_id = self.id

        search_service = Search()
        response = search_service.query(
            project_id=project_id,
            record_type=record_type,
            log_stream_id=log_stream_id,
            filters=filters,
            sort=sort,
            limit=limit,
            starting_token=starting_token,
        )

        # Create a query function that returns raw response for pagination
        def query_fn(
            record_type: RecordType,
            filters: builtins.list[FilterType] | None,
            sort: LogRecordsSortClause | None,
            limit: int,
            starting_token: int,
        ) -> Any:
            return Search().query(
                project_id=project_id,
                record_type=record_type,
                log_stream_id=log_stream_id,
                filters=filters,
                sort=sort,
                limit=limit,
                starting_token=starting_token,
            )

        # Wrap the response in QueryResult for easy access and pagination
        return QueryResult(response=response, query_fn=query_fn, record_type=record_type, filters=filters, sort=sort)

    def get_spans(
        self,
        filters: builtins.list[FilterType] | None = None,
        sort: LogRecordsSortClause | None = None,
        limit: int = 100,
        starting_token: int = 0,
    ) -> QueryResult:
        """
        Query spans in this log stream.

        This is a convenience method that queries for spans specifically.

        Args:
            filters: A list of filters to apply to the query.
            sort: A sort clause to order the query results.
            limit: The maximum number of records to return.
            starting_token: The token for the next page of results.

        Returns
        -------
            QueryResult: A list-like object containing the span query results with pagination support.

        Raises
        ------
            ValueError: If the log stream lacks required id or project_id attributes.

        Examples
        --------
            log_stream = LogStream.get(name="Production Logs", project_name="My AI Project")

            # Get spans with filters and sorting
            spans = log_stream.get_spans(
                filters=[
                    log_stream.span_columns["input"].contains("world"),
                    log_stream.span_columns["metrics/num_input_tokens"].greater_than(10)
                ],
                sort=log_stream.span_columns["created_at"].descending(),
                limit=50
            )

            # Iterate over results
            for span in spans:
                print(span["id"], span["input"])

            # Pagination
            if spans.has_next_page:
                more_spans = spans.next_page()
        """
        logger.debug(f"LogStream.get_spans: id='{self.id}' limit={limit} - started")
        return self.query(
            record_type=RecordType.SPAN, filters=filters, sort=sort, limit=limit, starting_token=starting_token
        )

    def get_traces(
        self,
        filters: builtins.list[FilterType] | None = None,
        sort: LogRecordsSortClause | None = None,
        limit: int = 100,
        starting_token: int = 0,
    ) -> QueryResult:
        """
        Query traces in this log stream.

        This is a convenience method that queries for traces specifically.

        Args:
            filters: A list of filters to apply to the query.
            sort: A sort clause to order the query results.
            limit: The maximum number of records to return.
            starting_token: The token for the next page of results.

        Returns
        -------
            QueryResult: A list-like object containing the trace query results with pagination support.

        Raises
        ------
            ValueError: If the log stream lacks required id or project_id attributes.

        Examples
        --------
            log_stream = LogStream.get(name="Production Logs", project_name="My AI Project")

            # Get traces with filters
            traces = log_stream.get_traces(
                filters=[
                    log_stream.trace_columns["input"].contains("largest"),
                    log_stream.trace_columns["created_at"].after("2024-01-01")
                ],
                sort=log_stream.trace_columns["created_at"].descending(),
                limit=50
            )

            # Access like a list
            for trace in traces:
                print(trace["id"], trace["input"])
        """
        logger.debug(f"LogStream.get_traces: id='{self.id}' limit={limit} - started")
        return self.query(
            record_type=RecordType.TRACE, filters=filters, sort=sort, limit=limit, starting_token=starting_token
        )

    def get_sessions(
        self,
        filters: builtins.list[FilterType] | None = None,
        sort: LogRecordsSortClause | None = None,
        limit: int = 100,
        starting_token: int = 0,
    ) -> QueryResult:
        """
        Query sessions in this log stream.

        This is a convenience method that queries for sessions specifically.

        Args:
            filters: A list of filters to apply to the query.
            sort: A sort clause to order the query results.
            limit: The maximum number of records to return.
            starting_token: The token for the next page of results.

        Returns
        -------
            QueryResult: A list-like object containing the session query results with pagination support.

        Raises
        ------
            ValueError: If the log stream lacks required id or project_id attributes.

        Examples
        --------
            log_stream = LogStream.get(name="Production Logs", project_name="My AI Project")

            # Get sessions with filters
            sessions = log_stream.get_sessions(
                filters=[
                    log_stream.session_columns["model"].equals("gpt-4o-mini"),
                    log_stream.session_columns["metrics/num_traces"].greater_than(5)
                ],
                sort=log_stream.session_columns["created_at"].descending(),
                limit=50
            )

            # Work with results
            for session in sessions:
                print(session["id"], session["model"])
        """
        logger.debug(f"LogStream.get_sessions: id='{self.id}' limit={limit} - started")
        return self.query(
            record_type=RecordType.SESSION, filters=filters, sort=sort, limit=limit, starting_token=starting_token
        )

    def export_records(
        self,
        record_type: RecordType = RecordType.TRACE,
        filters: builtins.list[FilterType] | None = None,
        sort: LogRecordsSortClause = LogRecordsSortClause(column_id="created_at", ascending=False),
        export_format: LLMExportFormat = LLMExportFormat.JSONL,
        column_ids: builtins.list[str] | None = None,
        redact: bool = True,
    ) -> Iterator[dict[str, Any]]:
        """
        Export records from this log stream.

        This method provides a convenient way to export records without needing
        to specify project_id or log_stream_id.

        Args:
            record_type: The type of records to export (SPAN, TRACE, or SESSION).
            filters: A list of filters to apply to the export.
            sort: A sort clause to order the exported records.
            export_format: The desired format for the exported data.
            column_ids: A list of column IDs to include in the export.
            redact: Redact sensitive data from the response.

        Returns
        -------
            Iterator[dict[str, Any]]: An iterator that yields each record as a dictionary.

        Raises
        ------
            ValueError: If the log stream lacks required id or project_id attributes.

        Examples
        --------
            from galileo.__future__ import RecordType

            log_stream = LogStream.get(name="Production Logs", project_name="My AI Project")

            # Export records with filters
            for record in log_stream.export_records(
                record_type=RecordType.SPAN,
                filters=[
                    log_stream.span_columns["model"].one_of(["gpt-4", "gpt-3.5-turbo", "gpt-4o-mini"]),
                    log_stream.span_columns["metrics/num_input_tokens"].greater_than(1)
                ],
                sort=log_stream.span_columns["created_at"].descending()
            ):
                print(record)
        """
        if self.id is None:
            raise ValueError("Log stream ID is not set. Cannot export from a local-only log stream.")
        if self.project_id is None:
            raise ValueError("Project ID is not set. Cannot export log stream without project_id.")

        # Convert RecordType to RootType for the export client
        root_type = RECORD_TYPE_TO_ROOT_TYPE[record_type]

        logger.info(
            f"LogStream.export_records: id='{self.id}' record_type='{record_type.value}' "
            f"export_format='{export_format.value}' - started"
        )
        export_client = ExportClient()
        return export_client.records(
            project_id=self.project_id,
            root_type=root_type,
            filters=filters,
            sort=sort,
            export_format=export_format,
            log_stream_id=self.id,
            column_ids=column_ids,
            redact=redact,
        )

    def context(self) -> Any:
        """
        Get a galileo context manager for this log stream.

        This is a convenient method that returns a pre-configured galileo_context
        for this log stream, eliminating the need to specify project and log stream names.

        Returns
        -------
            A context manager for Galileo logging configured with this log stream.

        Examples
        --------
            log_stream = LogStream.get(
                name="Production Logs",
                project_name="My AI Project"
            )

            with log_stream.context():
                # Your logging code here
                response = openai_client.chat.completions.create(...)
        """
        return galileo_context(project=self.project.name if self.project else None, log_stream=self.name)

    def _get_columns(self, api_func: Any, error_msg: str) -> LogRecordsAvailableColumnsResponse:
        """Helper method to retrieve available columns from the API."""
        if self.id is None:
            raise ValueError("Log stream ID is not set. Cannot get columns from a local-only log stream.")
        if self.project_id is None:
            raise ValueError("Project ID is not set. Cannot get columns without project_id.")

        config = GalileoPythonConfig.get()
        body = LogRecordsAvailableColumnsRequest(log_stream_id=self.id)
        response = api_func.sync(project_id=self.project_id, client=config.api_client, body=body)
        if isinstance(response, HTTPValidationError):
            raise response
        if not response:
            raise ValueError(error_msg)
        return response

    @property
    def project(self) -> Project | None:
        """Get the project this log stream belongs to."""
        return Project.get(id=self.project_id)

    @property
    def span_columns(self) -> ColumnCollection:
        """
        Get available columns for spans in this log stream.

        Returns
        -------
            ColumnCollection: A collection of columns available for spans, accessible by column ID.

        Raises
        ------
            ValueError: If the log stream lacks required id or project_id attributes.

        Examples
        --------
            log_stream = LogStream.get(name="Production Logs", project_name="My AI Project")
            columns = log_stream.span_columns

            # Access a specific column
            input_column = columns["input"]

            # Filter using columns
            spans = log_stream.get_spans(
                filters=[columns["input"].contains("world")],
                sort=columns["created_at"].descending()
            )
        """
        response = self._get_columns(
            spans_available_columns_projects_project_id_spans_available_columns_post, "Unable to retrieve span columns"
        )
        columns = [Column(col) for col in response.columns]
        return ColumnCollection(columns)

    @property
    def session_columns(self) -> ColumnCollection:
        """
        Get available columns for sessions in this log stream.

        Returns
        -------
            ColumnCollection: A collection of columns available for sessions, accessible by column ID.

        Raises
        ------
            ValueError: If the log stream lacks required id or project_id attributes.

        Examples
        --------
            log_stream = LogStream.get(name="Production Logs", project_name="My AI Project")
            columns = log_stream.session_columns

            # Access a specific column
            model_column = columns["model"]

            # Filter using columns
            sessions = log_stream.get_sessions(
                filters=[columns["model"].equals("gpt-4o-mini")],
                sort=columns["created_at"].descending()
            )
        """
        response = self._get_columns(
            sessions_available_columns_projects_project_id_sessions_available_columns_post,
            "Unable to retrieve session columns",
        )
        columns = [Column(col) for col in response.columns]
        return ColumnCollection(columns)

    @property
    def trace_columns(self) -> ColumnCollection:
        """
        Get available columns for traces in this log stream.

        Returns
        -------
            ColumnCollection: A collection of columns available for traces, accessible by column ID.

        Raises
        ------
            ValueError: If the log stream lacks required id or project_id attributes.

        Examples
        --------
            log_stream = LogStream.get(name="Production Logs", project_name="My AI Project")
            columns = log_stream.trace_columns

            # Access a specific column
            input_column = columns["input"]

            # Filter using columns
            traces = log_stream.get_traces(
                filters=[columns["input"].contains("largest")],
                sort=columns["created_at"].descending()
            )
        """
        response = self._get_columns(
            traces_available_columns_projects_project_id_traces_available_columns_post,
            "Unable to retrieve trace columns",
        )
        columns = [Column(col) for col in response.columns]
        return ColumnCollection(columns)


# Import at end to avoid circular import (project.py imports LogStream)
from galileo.__future__.project import Project  # noqa: E402
from galileo.__future__.shared.column import Column, ColumnCollection  # noqa: E402
from galileo.config import GalileoConfig  # noqa: E402
from galileo.resources.api.run_scorer_settings import (  # noqa: E402
    get_settings_projects_project_id_runs_run_id_scorer_settings_get,
)
