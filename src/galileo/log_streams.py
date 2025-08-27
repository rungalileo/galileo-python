import builtins
from typing import Optional, Union, overload

from galileo.base import BaseClientModel
from galileo.projects import Projects
from galileo.resources.api.log_stream import (
    create_log_stream_projects_project_id_log_streams_post,
    get_log_stream_projects_project_id_log_streams_log_stream_id_get,
    list_log_streams_projects_project_id_log_streams_get,
)
from galileo.resources.models.http_validation_error import HTTPValidationError
from galileo.resources.models.log_stream_create_request import LogStreamCreateRequest
from galileo.resources.models.log_stream_response import LogStreamResponse
from galileo.resources.models.scorer_config import ScorerConfig
from galileo.schema.metrics import GalileoScorers, Metric
from galileo.scorers import Scorers, ScorerSettings
from galileo.utils.catch_log import DecorateAllMethods


class LogStream(LogStreamResponse):
    """
    Log streams are used to organize logs within a project on the Galileo platform.
    They provide a way to categorize and group related logs, making it easier to
    analyze and monitor specific parts of your application or different environments
    (e.g., production, staging, development).

    Attributes
    ----------
    created_at : datetime.datetime
        The timestamp when the log stream was created.
    created_by : str
        The identifier of the user who created the log stream.
    id : str
        The unique identifier of the log stream.
    name : str
        The name of the log stream.
    project_id : str
        The ID of the project this log stream belongs to.
    updated_at : datetime.datetime
        The timestamp when the log stream was last updated.
    additional_properties : dict
        Additional properties associated with the log stream.

    Examples
    --------
    # Create a new log stream in a project
    from galileo.log_streams import create_log_stream

    # Create by project ID
    log_stream = create_log_stream(name="Production Logs", project_id="project-123")

    # Create by project name
    log_stream = create_log_stream(name="Production Logs", project_name="My AI Project")

    # Get a log stream by name
    from galileo.log_streams import get_log_stream
    log_stream = get_log_stream(name="Production Logs", project_name="My AI Project")

    # List all log streams in a project
    from galileo.log_streams import list_log_streams
    log_streams = list_log_streams(project_name="My AI Project")
    for stream in log_streams:
        print(f"Log Stream: {stream.name} (ID: {stream.id})")

    # Use a log stream with the context manager
    from galileo.openai import openai
    from galileo import galileo_context

    with galileo_context(project="My AI Project", log_stream="Production Logs"):
        response = openai.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": "Hello, world!"}]
        )

    # Configure metrics for an existing log stream
    from galileo.log_streams import configure_log_stream_metrics
    from galileo.schema.metrics import GalileoScorers

    configure_log_stream_metrics(
        log_stream="Production Logs",
        metrics=[GalileoScorers.correctness, GalileoScorers.groundedness, "toxicity"],
        project_name="My AI Project"
    )

    # Create a new log stream with metrics enabled
    from galileo.log_streams import create_log_stream_with_metrics

    log_stream, scorers = create_log_stream_with_metrics(
        name="Analytics Stream",
        metrics=[GalileoScorers.factuality, "bleu", "rouge"],
        project_name="My AI Project"
    )
    """

    def __init__(self, log_stream: Union[None, LogStreamResponse] = None):
        """
        Initialize a LogStream instance.

        Parameters
        ----------
        log_stream : Union[None, LogStreamResponse], optional
            The log stream data to initialize from. If None, creates an empty log stream instance.
            Defaults to None.
        """
        if log_stream is not None:
            super().__init__(
                created_at=log_stream.created_at,
                id=log_stream.id,
                name=log_stream.name,
                project_id=log_stream.project_id,
                updated_at=log_stream.updated_at,
                created_by=log_stream.created_by,
            )
            self.additional_properties = log_stream.additional_properties.copy()
            return


class LogStreams(BaseClientModel, DecorateAllMethods):
    @overload
    def list(self, *, project_id: str) -> list[LogStream]: ...

    @overload
    def list(self, *, project_name: str) -> builtins.list[LogStream]: ...

    def list(self, *, project_id: Optional[str] = None, project_name: Optional[str] = None) -> builtins.list[LogStream]:
        """
        Lists all log streams. Exactly one of `project_id` or `project_name` must be provided.

        Parameters
        ----------
        project_id : Optional[str], optional
            The ID of the project to list log streams for.
        project_name : Optional[str], optional
            The name of the project to list log streams for.

        Returns
        -------
        builtins.list[LogStream]
            A list of log streams.

        Raises
        ------
        ValueError
            If neither or both `project_id` and `project_name` are provided.
        errors.UnexpectedStatus
            If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException
            If the request takes longer than Client.timeout.
        """
        if (project_id is None) and (project_name is None):
            raise ValueError("Exactly one of 'project_id' or 'project_name' must be provided")

        if project_id:
            log_streams = list_log_streams_projects_project_id_log_streams_get.sync(
                client=self.client, project_id=project_id
            )
        else:
            project = Projects(config=self.config).get(name=project_name)
            if not project:
                raise ValueError(f"Project {project_name} not found")
            log_streams = list_log_streams_projects_project_id_log_streams_get.sync(
                client=self.client, project_id=project.id
            )
        return [LogStream(log_stream=log_stream) for log_stream in log_streams] if log_streams else []

    @overload
    def get(
        self, *, id: str, project_id: Optional[str] = None, project_name: Optional[str] = None
    ) -> Optional[LogStream]: ...
    @overload
    def get(
        self, *, name: str, project_id: Optional[str] = None, project_name: Optional[str] = None
    ) -> Optional[LogStream]: ...
    def get(
        self,
        *,
        id: Optional[str] = None,
        name: Optional[str] = None,
        project_id: Optional[str] = None,
        project_name: Optional[str] = None,
    ) -> Optional[LogStream]:
        """
        Retrieves a log stream by id or name.

        Parameters
        ----------
        id : Optional[str], optional
            The id of the log stream. Defaults to None.
        name : Optional[str], optional
            The name of the log stream. Defaults to None.
        project_id : Optional[str], optional
            The ID of the project. Defaults to None.
        project_name : Optional[str], optional
            The name of the project. Defaults to None.

        Returns
        -------
        Optional[LogStream]
            The log stream if found, None otherwise.

        Raises
        ------
        ValueError
            If neither or both `id` and `name` are provided, or if neither or both
            `project_id` and `project_name` are provided.
        errors.UnexpectedStatus
            If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException
            If the request takes longer than Client.timeout.
        """
        if (id is None) == (name is None):
            raise ValueError("Exactly one of 'id' or 'name' must be provided")

        if (project_id is None) == (project_name is None):
            raise ValueError("Exactly one of 'project_id' or 'project_name' must be provided")

        if not project_id:
            project = Projects(config=self.config).get(name=project_name)
            if not project:
                raise ValueError(f"Project {project_name} not found")
            project_id = project.id

        if id:
            log_stream_response = get_log_stream_projects_project_id_log_streams_log_stream_id_get.sync(
                project_id=project_id, log_stream_id=id, client=self.client
            )
            if not log_stream_response:
                return None
            return LogStream(log_stream=log_stream_response)

        elif name:
            log_streams = self.list(project_id=project_id)

            if not log_streams or len(log_streams) == 0:
                return None

            for log_stream in log_streams:
                if log_stream.name == name:
                    return log_stream
        return None

    @overload
    def create(self, name: str, *, project_id: Optional[str] = None) -> LogStream: ...
    @overload
    def create(self, name: str, *, project_name: str) -> LogStream: ...

    def create(self, name: str, *, project_id: Optional[str] = None, project_name: Optional[str] = None) -> LogStream:
        """
        Creates a new log stream. Exactly one of `project_id` or `project_name` must be provided.

        Parameters
        ----------
        name : str
            The name of the log stream.
        project_id : Optional[str], optional
            The ID of the project to create the log stream in. Defaults to None.
        project_name : Optional[str], optional
            The name of the project to create the log stream in. Defaults to None.

        Returns
        -------
        LogStream
            The created log stream.

        Raises
        ------
        ValueError
            If neither or both `project_id` and `project_name` are provided, or if the project is not found.
        HTTPValidationError
            If the server validation fails.
        errors.UnexpectedStatus
            If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException
            If the request takes longer than Client.timeout.
        """

        if (project_id is None) == (project_name is None):
            raise ValueError("Exactly one of 'project_id' or 'project_name' must be provided")

        if not project_id:
            project = Projects(config=self.config).get(name=project_name)
            if not project:
                raise ValueError(f"Project {project_name} not found")
            project_id = project.id

        body = LogStreamCreateRequest(name=name)
        response = create_log_stream_projects_project_id_log_streams_post.sync(
            project_id=project_id, client=self.client, body=body
        )

        if isinstance(response, HTTPValidationError):
            raise response

        if not response:
            raise ValueError("Unable to create log stream")

        return LogStream(log_stream=response)

    def configure_metrics(
        self, log_stream_id: str, project_id: str, metrics: builtins.list[Union[GalileoScorers, Metric, str]]
    ) -> builtins.list[ScorerConfig]:
        """
        Configure metrics for an existing log stream.

        Parameters
        ----------
        log_stream_id : str
            The ID of the log stream to configure metrics for.
        project_id : str
            The ID of the project containing the log stream.
        metrics : builtins.list[Union[GalileoScorers, Metric, str]]
            List of metrics to enable for the log stream.

        Returns
        -------
        builtins.list[ScorerConfig]
            List of configured scorer configs.

        Raises
        ------
        ValueError
            If one or more non-existent metrics are specified.
        """
        scorer_configs = LogStreams._create_scorer_configs_for_log_stream(project_id, log_stream_id, metrics)
        return scorer_configs

    @staticmethod
    def _create_scorer_configs_for_log_stream(
        project_id: str, log_stream_id: str, metrics: builtins.list[Union[GalileoScorers, Metric, str]]
    ) -> builtins.list[ScorerConfig]:
        """
        Create scorer configurations for log stream metrics.

        Parameters
        ----------
        project_id : str
            The ID of the project.
        log_stream_id : str
            The ID of the log stream.
        metrics : builtins.list[Union[GalileoScorers, Metric, str]]
            List of metrics to configure.

        Returns
        -------
        builtins.list[ScorerConfig]
            List of configured scorer configs.

        Raises
        ------
        ValueError
            If one or more non-existent metrics are specified.
        """
        scorer_name_versions: list[tuple[str, Optional[int]]] = []
        for metric in metrics:
            if isinstance(metric, GalileoScorers):
                scorer_name_versions.append((metric.value, None))
            elif isinstance(metric, Metric):
                scorer_name_versions.append((metric.name, metric.version))
            elif isinstance(metric, str):
                scorer_name_versions.append((metric, None))
            else:
                raise ValueError(f"Unknown metric type: {type(metric)}")

        scorers: list[ScorerConfig] = []
        if scorer_name_versions:
            all_scorers = Scorers().list()
            known_metrics = {metric.name: metric for metric in all_scorers}
            unknown_metrics = []

            for scorer_name, scorer_version in scorer_name_versions:
                if scorer_name in known_metrics:
                    raw_metric_dict = known_metrics[scorer_name].to_dict()

                    # Set the version on the ScorerConfig if provided
                    if scorer_version is not None:
                        raw_version = Scorers().get_scorer_version(
                            scorer_id=raw_metric_dict["id"], version=scorer_version
                        )
                        raw_metric_dict["scorer_version"] = raw_version.to_dict()
                    scorers.append(ScorerConfig.from_dict(raw_metric_dict))
                else:
                    unknown_metrics.append(scorer_name)

            if unknown_metrics:
                raise ValueError(
                    "One or more non-existent metrics are specified: "
                    + ", ".join(f"'{metric}'" for metric in unknown_metrics)
                )

            # Configure the scorers for the log stream (using log_stream_id as run_id)
            ScorerSettings().create(project_id=project_id, run_id=log_stream_id, scorers=scorers)

        return scorers


#
# Convenience methods
#


def get_log_stream(
    *, name: Optional[str] = None, project_id: Optional[str] = None, project_name: Optional[str] = None
) -> Optional[LogStream]:
    """
    Retrieves a log stream by name. Exactly one of `project_id` or `project_name` must be provided.

    Parameters
    ----------
    name : Optional[str], optional
        The name of the log stream. Defaults to None.
    project_id : Optional[str], optional
        The ID of the project. Defaults to None.
    project_name : Optional[str], optional
        The name of the project. Defaults to None.

    Returns
    -------
    Optional[LogStream]
        The log stream if found, None otherwise.

    Raises
    ------
    ValueError
        If neither or both `project_id` and `project_name` are provided.
    errors.UnexpectedStatus
        If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
    httpx.TimeoutException
        If the request takes longer than Client.timeout.
    """
    return LogStreams().get(name=name, project_id=project_id, project_name=project_name)


def list_log_streams(*, project_id: Optional[str] = None, project_name: Optional[str] = None) -> list[LogStream]:
    """
    Lists all log streams. Exactly one of `project_id` or `project_name` must be provided.

    Parameters
    ----------
    project_id : str
        The id of the project.
    project_name : str
        The name of the project.

    Returns
    -------
    list[LogStream]
        A list of Log streams.

    Raises
    ------
    errors.UnexpectedStatus
        If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
    httpx.TimeoutException
        If the request takes longer than Client.timeout.

    """
    return LogStreams().list(project_id=project_id, project_name=project_name)


def create_log_stream(name: str, project_id: Optional[str] = None, project_name: Optional[str] = None) -> LogStream:
    """
    Creates a new log stream. Exactly one of `project_id` or `project_name` must be provided.

    Parameters
    ----------
    name : str
        The name of the log stream.

    Returns
    -------
    LogStream
        The created project.

    Raises
    ------
    errors.UnexpectedStatus
        If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
    httpx.TimeoutException
        If the request takes longer than Client.timeout.

    """
    return LogStreams().create(name=name, project_id=project_id, project_name=project_name)


def configure_log_stream_metrics(
    log_stream: Union[LogStream, str],
    metrics: builtins.list[Union[GalileoScorers, Metric, str]],
    *,
    project_id: Optional[str] = None,
    project_name: Optional[str] = None,
) -> builtins.list[ScorerConfig]:
    """
    Configure metrics for a log stream. Exactly one of `project_id` or `project_name` must be provided.

    Parameters
    ----------
    log_stream : Union[LogStream, str]
        The log stream object or name to configure metrics for.
    metrics : builtins.list[Union[GalileoScorers, Metric, str]]
        List of metrics to enable for the log stream.
    project_id : Optional[str], optional
        The ID of the project containing the log stream. Defaults to None.
    project_name : Optional[str], optional
        The name of the project containing the log stream. Defaults to None.

    Returns
    -------
    builtins.list[ScorerConfig]
        List of configured scorer configs.

    Raises
    ------
    ValueError
        If neither or both `project_id` and `project_name` are provided,
        if the project is not found, if the log stream is not found,
        or if one or more non-existent metrics are specified.

    Examples
    --------
    # Configure metrics for a log stream by name
    from galileo.log_streams import configure_log_stream_metrics
    from galileo.schema.metrics import GalileoScorers

    configure_log_stream_metrics(
        log_stream="Production Logs",
        metrics=[GalileoScorers.correctness, GalileoScorers.groundedness, "toxicity"],
        project_name="My AI Project"
    )

    # Configure metrics for an existing LogStream object
    log_stream = get_log_stream(name="Production Logs", project_name="My AI Project")
    if log_stream:
        configure_log_stream_metrics(
            log_stream=log_stream,
            metrics=[GalileoScorers.factuality, "bleu"],
            project_name="My AI Project"
        )
    """
    if (project_id is None) == (project_name is None):
        raise ValueError("Exactly one of 'project_id' or 'project_name' must be provided")

    # Resolve project_id if needed
    if not project_id:
        project = Projects().get(name=project_name)
        if not project:
            raise ValueError(f"Project {project_name} not found")
        project_id = project.id

    # Get log stream ID
    if isinstance(log_stream, str):
        log_stream_obj = get_log_stream(name=log_stream, project_id=project_id)
        if not log_stream_obj:
            raise ValueError(f"Log stream '{log_stream}' not found in project")
        log_stream_id = log_stream_obj.id
    else:
        log_stream_id = log_stream.id

    return LogStreams().configure_metrics(log_stream_id=log_stream_id, project_id=project_id, metrics=metrics)


def create_log_stream_with_metrics(
    name: str,
    metrics: builtins.list[Union[GalileoScorers, Metric, str]],
    *,
    project_id: Optional[str] = None,
    project_name: Optional[str] = None,
) -> tuple[LogStream, builtins.list[ScorerConfig]]:
    """
    Creates a new log stream and configures metrics for it in one step.
    Exactly one of `project_id` or `project_name` must be provided.

    Parameters
    ----------
    name : str
        The name of the log stream.
    metrics : builtins.list[Union[GalileoScorers, Metric, str]]
        List of metrics to enable for the log stream.
    project_id : Optional[str], optional
        The ID of the project to create the log stream in. Defaults to None.
    project_name : Optional[str], optional
        The name of the project to create the log stream in. Defaults to None.

    Returns
    -------
    tuple[LogStream, builtins.list[ScorerConfig]]
        A tuple containing the created log stream and the configured scorer configs.

    Raises
    ------
    ValueError
        If neither or both `project_id` and `project_name` are provided,
        if the project is not found, or if one or more non-existent metrics are specified.

    Examples
    --------
    from galileo.log_streams import create_log_stream_with_metrics
    from galileo.schema.metrics import GalileoScorers

    # Create a log stream with metrics
    log_stream, scorers = create_log_stream_with_metrics(
        name="Production Logs with Metrics",
        metrics=[GalileoScorers.correctness, GalileoScorers.groundedness, "toxicity"],
        project_name="My AI Project"
    )

    print(f"Created log stream: {log_stream.name}")
    print(f"Configured {len(scorers)} metrics")
    """
    # Create the log stream first
    log_stream = create_log_stream(name=name, project_id=project_id, project_name=project_name)

    # Configure metrics for the created log stream
    scorers = configure_log_stream_metrics(
        log_stream=log_stream, metrics=metrics, project_id=project_id, project_name=project_name
    )

    return log_stream, scorers
