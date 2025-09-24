"""
LogStream class for the Galileo Future API.

This module provides an object-centric interface for managing Galileo log streams,
offering a more intuitive alternative to the service-based functions.
"""

from __future__ import annotations

from galileo.log_streams import LogStream as LegacyLogStream
from galileo.log_streams import get_log_stream as service_get_log_stream
from galileo.log_streams import list_log_streams as service_list_log_streams
from galileo.schema.metrics import GalileoScorers, LocalMetricConfig, Metric


class LogStream:
    """
    Object-centric interface for Galileo log streams.

    This class provides an intuitive way to work with Galileo log streams,
    offering methods for managing log streams and their associated metrics.

    Attributes:
        created_at (datetime.datetime): When the log stream was created.
        created_by (str): The user who created the log stream.
        id (str): The unique log stream identifier.
        name (str): The log stream name.
        project_id (str): The ID of the project this log stream belongs to.
        updated_at (datetime.datetime): When the log stream was last updated.
        additional_properties (dict): Additional properties of the log stream.

    Examples:
        # LogStreams are typically created through Project instances
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
    """

    def __init__(self, *, _legacy_log_stream: LegacyLogStream | None = None) -> None:
        """
        Initialize a LogStream instance.

        Note: LogStreams should typically be created through Project methods
        rather than directly instantiated.

        Args:
            _legacy_log_stream (Optional[LegacyLogStream]): Internal parameter for
                wrapping existing log stream instances.
        """
        if _legacy_log_stream is not None:
            # Initialize from existing legacy log stream
            self._legacy_log_stream = _legacy_log_stream
            self.created_at = _legacy_log_stream.created_at
            self.created_by = _legacy_log_stream.created_by
            self.id = _legacy_log_stream.id
            self.name = _legacy_log_stream.name
            self.project_id = _legacy_log_stream.project_id
            self.updated_at = _legacy_log_stream.updated_at
            self.additional_properties = _legacy_log_stream.additional_properties
        else:
            raise ValueError("LogStream instances should be created through Project methods")

    @classmethod
    def get(cls, *, name: str, project_id: str | None = None, project_name: str | None = None) -> LogStream | None:
        """
        Get an existing log stream by name.

        Args:
            name (str): The log stream name.
            project_id (Optional[str]): The project ID.
            project_name (Optional[str]): The project name.

        Returns:
            Optional[LogStream]: The log stream if found, None otherwise.

        Raises:
            ValueError: If neither or both project_id and project_name are provided.

        Examples:
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
        legacy_log_stream = service_get_log_stream(name=name, project_id=project_id, project_name=project_name)
        if legacy_log_stream is None:
            return None
        return cls(_legacy_log_stream=legacy_log_stream)

    @classmethod
    def list(cls, *, project_id: str | None = None, project_name: str | None = None) -> list[LogStream]:
        """
        List all log streams for a project.

        Args:
            project_id (Optional[str]): The project ID.
            project_name (Optional[str]): The project name.

        Returns:
            List[LogStream]: A list of log streams for the project.

        Raises:
            ValueError: If neither or both project_id and project_name are provided.

        Examples:
            # List by project name
            log_streams = LogStream.list(project_name="My AI Project")

            # List by project ID
            log_streams = LogStream.list(project_id="project-123")
        """
        legacy_log_streams = service_list_log_streams(project_id=project_id, project_name=project_name)
        return [cls(_legacy_log_stream=legacy_stream) for legacy_stream in legacy_log_streams]

    def enable_metrics(
        self,
        metrics: list[GalileoScorers | Metric | LocalMetricConfig | str],  # type: ignore[valid-type]
    ) -> list[LocalMetricConfig]:  # type: ignore[valid-type]
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

        Returns:
            List[LocalMetricConfig]: Local metric configurations that must be
                computed client-side.

        Raises:
            ValueError: If the log stream lacks required id or project_id attributes,
                or if any specified metrics are unknown.

        Examples:
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
        return self._legacy_log_stream.enable_metrics(metrics)

    def __str__(self) -> str:
        """String representation of the log stream."""
        return f"LogStream(name='{self.name}', id='{self.id}', project_id='{self.project_id}')"

    def __repr__(self) -> str:
        """Detailed string representation of the log stream."""
        return f"LogStream(name='{self.name}', id='{self.id}', project_id='{self.project_id}', created_at='{self.created_at}')"
