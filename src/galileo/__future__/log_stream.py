from __future__ import annotations

import builtins
import logging
from collections.abc import Iterator
from datetime import datetime
from typing import Any

from galileo import galileo_context
from galileo.__future__.shared.base import StateManagementMixin, SyncState
from galileo.__future__.shared.exceptions import ValidationError
from galileo.export import ExportClient
from galileo.log_streams import LogStreams
from galileo.resources.models import (
    LLMExportFormat,
    LogRecordsAvailableColumnsResponse,
    LogRecordsQueryResponse,
    LogRecordsSortClause,
    RootType,
)
from galileo.schema.filters import FilterType
from galileo.schema.metrics import GalileoScorers, LocalMetricConfig, Metric
from galileo.search import RecordType, Search
from galileo.utils.validations import require_exactly_one

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
        from galileo.schema.metrics import GalileoScorers
        local_metrics = log_stream.enable_metrics([
            GalileoScorers.correctness,
            GalileoScorers.completeness,
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

    def enable_metrics(
        self, metrics: builtins.list[GalileoScorers | Metric | LocalMetricConfig | str]
    ) -> builtins.list[LocalMetricConfig]:
        """
        Enable metrics on this log stream.

        This is a convenient method that leverages the log stream's existing
        project_id and id attributes to enable metrics without requiring
        redundant parameter specification.

        Args:
            metrics: List of metrics to enable. Supports:
                - GalileoScorers enum values (e.g., GalileoScorers.correctness)
                - Metric objects with name and optional version
                - LocalMetricConfig objects for custom scoring functions
                - String names of built-in metrics

        Returns
        -------
            List[LocalMetricConfig]: Local metric configurations that must be
                computed client-side.

        Raises
        ------
            ValueError: If the log stream lacks required id or project_id attributes,
                or if any specified metrics are unknown.

        Examples
        --------
            from galileo.schema.metrics import GalileoScorers

            project = Project.get(name="My AI Project")
            log_stream = project.create_log_stream(name="Production Logs")

            # Enable built-in metrics
            local_metrics = log_stream.enable_metrics([
                GalileoScorers.correctness,
                GalileoScorers.completeness,
                "context_relevance"
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
    ) -> LogRecordsQueryResponse:
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
            LogRecordsQueryResponse: Object containing the query results.

        Raises
        ------
            ValueError: If the log stream lacks required id or project_id attributes.

        Examples
        --------
            from galileo.search import RecordType
            from galileo.__future__ import text, number, date, sort

            log_stream = LogStream.get(name="Production Logs", project_name="My AI Project")

            # Query with declarative filters and sort
            results = log_stream.query(
                record_type=RecordType.SPAN,
                filters=[
                    text("input").not_equals("example"),
                    number("score").greater_than(0.8),
                    date("created_at").after("2024-01-01")
                ],
                sort=sort("created_at").descending(),
                limit=50
            )
        """
        if self.id is None:
            raise ValueError("Log stream ID is not set. Cannot query a local-only log stream.")
        if self.project_id is None:
            raise ValueError("Project ID is not set. Cannot query log stream without project_id.")

        logger.debug(f"LogStream.query: id='{self.id}' record_type='{record_type.value}' limit={limit} - started")
        search_service = Search()
        return search_service.query(
            project_id=self.project_id,
            record_type=record_type,
            log_stream_id=self.id,
            filters=filters,
            sort=sort,
            limit=limit,
            starting_token=starting_token,
        )

    def get_spans(
        self,
        filters: builtins.list[FilterType] | None = None,
        sort: LogRecordsSortClause | None = None,
        limit: int = 100,
        starting_token: int = 0,
    ) -> LogRecordsQueryResponse:
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
            LogRecordsQueryResponse: Object containing the span query results.

        Raises
        ------
            ValueError: If the log stream lacks required id or project_id attributes.

        Examples
        --------
            from galileo.__future__ import text, number, sort

            log_stream = LogStream.get(name="Production Logs", project_name="My AI Project")

            # Get spans with filters and sorting
            spans = log_stream.get_spans(
                filters=[
                    text("status").equals("completed"),
                    number("latency_ms").less_than(1000)
                ],
                sort=sort("latency_ms").ascending(),
                limit=50
            )
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
    ) -> LogRecordsQueryResponse:
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
            LogRecordsQueryResponse: Object containing the trace query results.

        Raises
        ------
            ValueError: If the log stream lacks required id or project_id attributes.

        Examples
        --------
            from galileo.__future__ import text, date, sort

            log_stream = LogStream.get(name="Production Logs", project_name="My AI Project")

            # Get traces with filters
            traces = log_stream.get_traces(
                filters=[
                    text("user_id").equals("user-123"),
                    date("created_at").after("2024-01-01")
                ],
                sort=sort("created_at").descending(),
                limit=50
            )
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
    ) -> LogRecordsQueryResponse:
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
            LogRecordsQueryResponse: Object containing the session query results.

        Raises
        ------
            ValueError: If the log stream lacks required id or project_id attributes.

        Examples
        --------
            from galileo.__future__ import text, number, sort

            log_stream = LogStream.get(name="Production Logs", project_name="My AI Project")

            # Get sessions with filters
            sessions = log_stream.get_sessions(
                filters=[
                    text("environment").equals("production"),
                    number("session_duration").greater_than(60)
                ],
                sort=sort("created_at").descending(),
                limit=50
            )
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
            from galileo.__future__ import RecordType, text, number, sort

            log_stream = LogStream.get(name="Production Logs", project_name="My AI Project")

            # Export records with filters
            for record in log_stream.export_records(
                record_type=RecordType.TRACE,
                filters=[
                    text("model").one_of(["gpt-4", "gpt-3.5-turbo"]),
                    number("tokens").greater_than(100)
                ],
                sort=sort("created_at").descending()
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

    @property
    def project(self) -> Project | None:
        """Get the project this log stream belongs to."""
        return Project.get(id=self.project_id)

    @property
    def span_columns(self) -> LogRecordsAvailableColumnsResponse:
        """
        Get available columns for spans in this log stream.

        Returns
        -------
            LogRecordsAvailableColumnsResponse: The response containing available span columns.

        Raises
        ------
            ValueError: If the log stream lacks required id or project_id attributes.

        Examples
        --------
            log_stream = LogStream.get(name="Production Logs", project_name="My AI Project")
            columns = log_stream.span_columns
            for col in columns.columns:
                print(f"Column: {col.id}")
        """
        if self.id is None:
            raise ValueError("Log stream ID is not set. Cannot get span columns from a local-only log stream.")
        if self.project_id is None:
            raise ValueError("Project ID is not set. Cannot get span columns without project_id.")

        log_streams_service = LogStreams()
        return log_streams_service.get_span_columns(project_id=self.project_id, log_stream_id=self.id)

    @property
    def session_columns(self) -> LogRecordsAvailableColumnsResponse:
        """
        Get available columns for sessions in this log stream.

        Returns
        -------
            LogRecordsAvailableColumnsResponse: The response containing available session columns.

        Raises
        ------
            ValueError: If the log stream lacks required id or project_id attributes.

        Examples
        --------
            log_stream = LogStream.get(name="Production Logs", project_name="My AI Project")
            columns = log_stream.session_columns
            for col in columns.columns:
                print(f"Column: {col.id}")
        """
        if self.id is None:
            raise ValueError("Log stream ID is not set. Cannot get session columns from a local-only log stream.")
        if self.project_id is None:
            raise ValueError("Project ID is not set. Cannot get session columns without project_id.")

        log_streams_service = LogStreams()
        return log_streams_service.get_session_columns(project_id=self.project_id, log_stream_id=self.id)

    @property
    def trace_columns(self) -> LogRecordsAvailableColumnsResponse:
        """
        Get available columns for traces in this log stream.

        Returns
        -------
            LogRecordsAvailableColumnsResponse: The response containing available trace columns.

        Raises
        ------
            ValueError: If the log stream lacks required id or project_id attributes.

        Examples
        --------
            log_stream = LogStream.get(name="Production Logs", project_name="My AI Project")
            columns = log_stream.trace_columns
            for col in columns.columns:
                print(f"Column: {col.id}")
        """
        if self.id is None:
            raise ValueError("Log stream ID is not set. Cannot get trace columns from a local-only log stream.")
        if self.project_id is None:
            raise ValueError("Project ID is not set. Cannot get trace columns without project_id.")

        log_streams_service = LogStreams()
        return log_streams_service.get_trace_columns(project_id=self.project_id, log_stream_id=self.id)


# Import at end to avoid circular import (project.py imports LogStream)
from galileo.__future__.project import Project  # noqa: E402
