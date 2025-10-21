from __future__ import annotations

import builtins
import logging
from typing import TYPE_CHECKING, Any

from galileo.__future__.exceptions import ValidationError
from galileo.log_streams import LogStreams
from galileo.schema.metrics import GalileoScorers, LocalMetricConfig, Metric

if TYPE_CHECKING:
    from galileo.__future__.project import Project

logger = logging.getLogger(__name__)


class LogStream:
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
        updated_at (datetime.datetime): When the log stream was last updated.
        additional_properties (dict): Additional properties of the log stream.

    Examples
    --------
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

    created_at: Any
    created_by: str
    id: str
    name: str
    project_id: str
    updated_at: Any
    additional_properties: dict[str, Any]

    def __init__(self) -> None:
        """
        Initialize a LogStream instance.

        Note: LogStreams should not be instantiated directly. Use LogStream.get()
        to retrieve existing log streams, or Project.create_log_stream() to create new ones.
        """
        raise ValidationError(
            "LogStream instances should not be created directly. "
            "Use LogStream.get() to retrieve existing log streams, or "
            "Project.create_log_stream() to create new ones."
        )

    @classmethod
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

        # Create a new instance and populate its attributes
        instance = cls.__new__(cls)
        instance.created_at = retrieved_log_stream.created_at
        instance.created_by = retrieved_log_stream.created_by
        instance.id = retrieved_log_stream.id
        instance.name = retrieved_log_stream.name
        instance.project_id = retrieved_log_stream.project_id
        instance.updated_at = retrieved_log_stream.updated_at
        instance.additional_properties = retrieved_log_stream.additional_properties
        return instance

    @classmethod
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

        result = []
        for retrieved_log_stream in retrieved_log_streams:
            instance = cls.__new__(cls)
            instance.created_at = retrieved_log_stream.created_at
            instance.created_by = retrieved_log_stream.created_by
            instance.id = retrieved_log_stream.id
            instance.name = retrieved_log_stream.name
            instance.project_id = retrieved_log_stream.project_id
            instance.updated_at = retrieved_log_stream.updated_at
            instance.additional_properties = retrieved_log_stream.additional_properties
            result.append(instance)

        return result

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
        logger.info(f"LogStream.enable_metrics: id='{self.id}' metrics={[str(m) for m in metrics]} - started")
        log_streams_service = LogStreams()
        log_stream = log_streams_service.get(name=self.name, project_id=self.project_id)
        if log_stream is None:
            raise ValueError(f"Log stream '{self.name}' not found")
        result = log_stream.enable_metrics(metrics)
        logger.info(f"LogStream.enable_metrics: id='{self.id}' - completed")
        return result

    def __str__(self) -> str:
        """String representation of the log stream."""
        return f"LogStream(name='{self.name}', id='{self.id}', project_id='{self.project_id}')"

    @property
    def project(self) -> Project | None:
        """Get the project this log stream belongs to."""
        from galileo.__future__.project import Project

        return Project.get(id=self.project_id)

    def __repr__(self) -> str:
        """Detailed string representation of the log stream."""
        return f"LogStream(name='{self.name}', id='{self.id}', project_id='{self.project_id}', created_at='{self.created_at}')"
