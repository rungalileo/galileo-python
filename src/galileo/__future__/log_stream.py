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
        from galileo.config import GalileoConfig
        from galileo.resources.api.run_scorer_settings import (
            get_settings_projects_project_id_runs_run_id_scorer_settings_get,
        )

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
        self, metrics: builtins.list[GalileoScorers | Metric | LocalMetricConfig | str]
    ) -> builtins.list[LocalMetricConfig]:
        """
        Set (replace) the metrics on this log stream.

        This replaces any existing metrics with the new list. Alias for enable_metrics
        with clearer naming intent.

        Args:
            metrics: List of metrics to set. Supports:
                - GalileoScorers enum values (e.g., GalileoScorers.correctness)
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
                Metric.scorers.correctness,
                Metric.scorers.completeness,
                Metric.get(id="metric-from-console-uuid"),  # From console
            ])
        """
        logger.info(f"LogStream.set_metrics: id='{self.id}' metrics={[str(m) for m in metrics]} - started")
        log_streams_service = LogStreams()
        log_stream = log_streams_service.get(name=self.name, project_id=self.project_id)
        if log_stream is None:
            raise ValueError(f"Log stream '{self.name}' not found")
        result = log_stream.enable_metrics(metrics)
        logger.info(f"LogStream.set_metrics: id='{self.id}' - completed")
        return result

    def add_metrics(
        self, metrics: builtins.list[GalileoScorers | Metric | LocalMetricConfig | str]
    ) -> builtins.list[LocalMetricConfig]:
        """
        Add metrics to the existing metrics on this log stream.

        This adds to the current set of metrics without removing existing ones.

        Args:
            metrics: List of metrics to add. Supports:
                - GalileoScorers enum values (e.g., GalileoScorers.correctness)
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
            log_stream = LogStream.get(name="Production Logs", project_name="My Project")

            # Add more metrics to existing ones
            log_stream.add_metrics([
                Metric.scorers.toxicity,
                "prompt_injection",
            ])
        """
        logger.info(f"LogStream.add_metrics: id='{self.id}' adding {len(metrics)} metrics - started")

        # Get current metrics
        current_metric_names: set[str] = set(self.get_metrics())
        logger.debug(f"LogStream.add_metrics: current metrics={current_metric_names}")

        # Build combined list (avoid duplicates by name)
        combined_metrics = list(metrics)  # Start with new metrics

        # Add existing metrics that aren't being replaced
        for metric_name in current_metric_names:
            # Check if this metric is being replaced
            is_replaced = any(
                (isinstance(m, str) and m == metric_name)
                or (hasattr(m, "name") and m.name == metric_name)
                or (isinstance(m, GalileoScorers) and m.value.lstrip("_") == metric_name)
                for m in metrics
            )
            if not is_replaced:
                combined_metrics.append(metric_name)

        logger.info(f"LogStream.add_metrics: setting {len(combined_metrics)} total metrics")
        return self.set_metrics(combined_metrics)

    def enable_metrics(
        self, metrics: builtins.list[GalileoScorers | Metric | LocalMetricConfig | str]
    ) -> builtins.list[LocalMetricConfig]:
        """
        Enable metrics on this log stream.

        Alias for set_metrics() for backward compatibility.

        Args:
            metrics: List of metrics to enable.

        Returns
        -------
            List[LocalMetricConfig]: Local metric configurations that must be
                computed client-side.

        Examples
        --------
            log_stream.enable_metrics([
                Metric.scorers.correctness,
                "completeness",
            ])
        """
        return self.set_metrics(metrics)

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
