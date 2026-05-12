import builtins
from typing import overload

from galileo.config import GalileoPythonConfig
from galileo.projects import Projects
from galileo.resources.api.log_stream import (
    create_log_stream_projects_project_id_log_streams_post,
    get_log_stream_projects_project_id_log_streams_log_stream_id_get,
    list_log_streams_paginated_projects_project_id_log_streams_paginated_get,
)
from galileo.resources.models.http_validation_error import HTTPValidationError
from galileo.resources.models.log_stream_create_request import LogStreamCreateRequest
from galileo.resources.models.log_stream_response import LogStreamResponse
from galileo.resources.types import Unset
from galileo.schema.metrics import GalileoMetrics, LocalMetricConfig, Metric
from galileo.utils.env_helpers import _get_log_stream_from_env, _get_project_from_env
from galileo.utils.log_config import get_logger
from galileo.utils.metrics import create_metric_configs

logger = get_logger(__name__)


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
    ```python
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
        logger.info(f"Log Stream: {stream.name} (ID: {stream.id})")

    # Use a log stream with the context manager
    from galileo.openai import openai
    from galileo import galileo_context

    with galileo_context(project="My AI Project", log_stream="Production Logs"):
        response = openai.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": "Hello, world!"}]
        )

    # Enable metrics on a log stream - RECOMMENDED APPROACH
    from galileo.log_streams import enable_metrics
    from galileo.schema.metrics import GalileoMetrics

    # Set environment variables first
    # export GALILEO_LOG_STREAM="Production Logs"
    # export GALILEO_PROJECT="My AI Project"

    # Clean and simple - just pass the metrics!
    local_metrics = enable_metrics([
        GalileoMetrics.correctness,
        GalileoMetrics.completeness,
        "context_relevance"
    ])

    # Alternative: Use explicit parameters
    local_metrics = enable_metrics(
        log_stream_name="Production Logs",
        project_name="My AI Project",
        metrics=["correctness", "completeness"]
    )
    ```
    """

    def __init__(self, log_stream: None | LogStreamResponse = None):
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

    def enable_metrics(
        self, metrics: builtins.list[GalileoMetrics | Metric | LocalMetricConfig | str]
    ) -> builtins.list[LocalMetricConfig]:
        """
        Enable metrics directly on this log stream instance.

        This is the most intuitive and clean way to enable metrics when you already have a
        LogStream object. The method leverages the log stream's existing project_id and id
        attributes, eliminating the need for redundant parameter specification and reducing
        the potential for errors.

        This approach is ideal for object-oriented workflows where you're working with LogStream
        instances directly, and it provides the clearest semantic meaning: "enable these metrics
        on this specific log stream."

        Parameters
        ----------
        metrics : builtins.list[Union[GalileoMetrics, Metric, LocalMetricConfig, str]]
            List of metrics to enable on this log stream. Supports multiple input formats:

            - **GalileoMetrics enum values**: Built-in metrics like `GalileoMetrics.correctness`
            - **Metric objects**: Custom metrics with optional version specifications
            - **LocalMetricConfig objects**: Client-side metrics with custom scoring functions
            - **String names**: Built-in metric names like "correctness" or "toxicity"

        Returns
        -------
        builtins.list[LocalMetricConfig]
            List of local metric configurations that must be computed client-side.
            Server-side metrics are automatically registered with Galileo and don't
            need to be returned since users don't interact with them.

        Raises
        ------
        ValueError
            - If this LogStream instance lacks required `id` or `project_id` attributes
            - If any specified metrics are unknown or unavailable
            - If there are issues with metric configuration or registration
        GalileoHTTPException
            If there are network or API errors when communicating with Galileo services

        Examples
        --------
        Basic usage with built-in metrics:

        ```python
        from galileo.log_streams import LogStreams
        from galileo.schema.metrics import GalileoMetrics

        # Get a log stream first
        log_streams = LogStreams()
        log_stream = log_streams.get(name="Production Logs", project_name="My AI Project")

        # Enable metrics directly - clean and intuitive!
        local_metrics = log_stream.enable_metrics([
            GalileoMetrics.correctness,
            GalileoMetrics.completeness,
            "context_relevance",
            "toxicity"
        ])

        logger.info(f"Server-side metrics enabled automatically")
        logger.info(f"Need to process {len(local_metrics)} local metrics")
        ```

        Advanced usage with custom metrics:

        ```python
        from galileo.schema.metrics import Metric, LocalMetricConfig

        def custom_scorer(trace_or_span):
            return 0.75  # Your scoring logic

        local_metrics = log_stream.enable_metrics([
            GalileoMetrics.correctness,
            "completeness",
            Metric(name="domain_relevance", version=3),
            LocalMetricConfig(name="custom_metric", scorer_fn=custom_scorer)
        ])

        # Process local metrics if any
        for local_metric in local_metrics:
            logger.info(f"Need to process local metric: {local_metric.name}")
        ```

        Notes
        -----
        **Requirements:**

        - The LogStream instance must have valid `id` and `project_id` attributes
        - These are automatically set when retrieving LogStream objects via LogStreams methods

        **Recommended Usage:**

        - Use this method when you already have a LogStream object
        - More intuitive than specifying project/log stream names again
        - Cleaner object-oriented design pattern
        """
        if not hasattr(self, "id") or not hasattr(self, "project_id"):
            raise ValueError("Log stream must have id and project_id to enable metrics")

        _, local_metrics = create_metric_configs(self.project_id, self.id, metrics)
        return local_metrics


class LogStreams:
    config: GalileoPythonConfig

    def __init__(self) -> None:
        self.config = GalileoPythonConfig.get()

    @overload
    def list(
        self, *, project_id: str, limit: Unset | int = 100, starting_token: Unset | int = 0
    ) -> builtins.list[LogStream]: ...

    @overload
    def list(
        self, *, project_name: str, limit: Unset | int = 100, starting_token: Unset | int = 0
    ) -> builtins.list[LogStream]: ...

    def list(
        self,
        *,
        project_id: str | None = None,
        project_name: str | None = None,
        limit: Unset | int = 100,
        starting_token: Unset | int = 0,
    ) -> builtins.list[LogStream]:
        """
        Lists log streams. Exactly one of `project_id` or `project_name` must be provided.

        Returns a single page of results. Use `starting_token` (from
        `next_starting_token` on a prior response) to fetch subsequent pages.

        Parameters
        ----------
        project_id : Optional[str], optional
            The ID of the project to list log streams for.
        project_name : Optional[str], optional
            The name of the project to list log streams for.
        limit : Union[Unset, int], optional
            The maximum number of log streams to return per page. Defaults to 100.
        starting_token : Union[Unset, int], optional
            The pagination token to start from. Defaults to 0 (first page).

        Returns
        -------
        builtins.list[LogStream]
            A page of log streams.

        Raises
        ------
        ValueError
            If neither or both `project_id` and `project_name` are provided,
            if the named project is not found, if the server returns a
            validation error, or if the response is unexpectedly empty.
        errors.UnexpectedStatus
            If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException
            If the request takes longer than Client.timeout.
        """
        if (project_id is None) == (project_name is None):
            raise ValueError("Exactly one of 'project_id' or 'project_name' must be provided")

        if not project_id:
            project = Projects().get(name=project_name)
            if not project:
                raise ValueError(f"Project {project_name} not found")
            project_id = project.id

        response = list_log_streams_paginated_projects_project_id_log_streams_paginated_get.sync(
            client=self.config.api_client, project_id=project_id, limit=limit, starting_token=starting_token
        )

        if isinstance(response, HTTPValidationError):
            raise ValueError(f"Failed to list log streams: {response.detail}")
        if response is None:
            raise ValueError("Unexpected empty response while listing log streams")

        return [LogStream(log_stream=log_stream) for log_stream in response.log_streams]

    # Page size used by `_list_all`. Larger than the default `list()` page size so
    # full scans (name-based `get`, oldest-stream fallback) issue fewer round trips.
    _LIST_ALL_PAGE_SIZE = 500

    def _list_all(self, *, project_id: str) -> builtins.list[LogStream]:
        """Internal helper: paginate through every page and return all log streams.

        Used by callers that need a globally-complete view (e.g. name-based lookup,
        oldest-stream fallback). Public callers should use `list()` with explicit
        pagination instead.

        Raises ValueError on server validation failures or unexpected protocol
        errors so mid-pagination failures aren't silently swallowed into a
        truncated result.
        """
        all_log_streams: builtins.list[LogStream] = []
        starting_token: int = 0
        seen_tokens: set[int] = {starting_token}
        while True:
            response = list_log_streams_paginated_projects_project_id_log_streams_paginated_get.sync(
                client=self.config.api_client,
                project_id=project_id,
                starting_token=starting_token,
                limit=self._LIST_ALL_PAGE_SIZE,
            )
            if isinstance(response, HTTPValidationError):
                raise ValueError(f"Failed to list log streams: {response.detail}")
            if response is None:
                raise ValueError("Unexpected empty response while paginating log streams")

            all_log_streams.extend(LogStream(log_stream=log_stream) for log_stream in response.log_streams)

            next_token = response.next_starting_token
            if next_token is None or isinstance(next_token, Unset) or not response.paginated:
                break
            # Progress guard: stop if we've already seen this token. Catches both
            # repeated and non-advancing tokens without assuming monotonic-integer
            # ordering, so the loop stays safe if the server ever switches to
            # opaque cursor tokens.
            if not isinstance(next_token, int) or next_token in seen_tokens:
                break
            seen_tokens.add(next_token)
            starting_token = next_token

        return all_log_streams

    @overload
    def get(self, *, id: str, project_id: str | None = None, project_name: str | None = None) -> LogStream | None: ...
    @overload
    def get(self, *, name: str, project_id: str | None = None, project_name: str | None = None) -> LogStream | None: ...
    def get(
        self,
        *,
        id: str | None = None,
        name: str | None = None,
        project_id: str | None = None,
        project_name: str | None = None,
    ) -> LogStream | None:
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
            project = Projects().get(name=project_name)
            if not project:
                raise ValueError(f"Project {project_name} not found")
            project_id = project.id

        if id:
            log_stream_response = get_log_stream_projects_project_id_log_streams_log_stream_id_get.sync(
                project_id=project_id, log_stream_id=id, client=self.config.api_client
            )
            if not log_stream_response:
                return None
            return LogStream(log_stream=log_stream_response)

        if name:
            for log_stream in self._list_all(project_id=project_id):
                if log_stream.name == name:
                    return log_stream
        return None

    @overload
    def create(self, name: str, *, project_id: str | None = None) -> LogStream: ...
    @overload
    def create(self, name: str, *, project_name: str) -> LogStream: ...

    def create(self, name: str, *, project_id: str | None = None, project_name: str | None = None) -> LogStream:
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
            project = Projects().get(name=project_name)
            if not project:
                raise ValueError(f"Project {project_name} not found")
            project_id = project.id

        body = LogStreamCreateRequest(name=name)
        response = create_log_stream_projects_project_id_log_streams_post.sync(
            project_id=project_id, client=self.config.api_client, body=body
        )

        if isinstance(response, HTTPValidationError):
            raise response

        if not response:
            raise ValueError("Unable to create log stream")

        return LogStream(log_stream=response)

    def enable_metrics(
        self,
        *,
        log_stream_name: str | None = None,
        project_name: str | None = None,
        metrics: builtins.list[GalileoMetrics | Metric | LocalMetricConfig | str],
    ) -> builtins.list[LocalMetricConfig]:
        """
        Enable metrics for a log stream by configuring scorers.

        The project name can be provided via the 'project_name' parameter or the
        GALILEO_PROJECT environment variable.

        The log stream name can be provided via the 'log_stream_name' parameter or the
        GALILEO_LOG_STREAM environment variable.

        Parameters
        ----------
        log_stream_name : Optional[str], optional
            The name of the log stream. Takes precedence over the GALILEO_LOG_STREAM environment variable. Defaults to None.
        project_name : Optional[str], optional
            The name of the project. Takes precedence over the GALILEO_PROJECT environment variable. Defaults to None.
        metrics : builtins.list[Union[GalileoMetrics, Metric, LocalMetricConfig, str]]
            List of metrics to enable. Can include:
            - GalileoMetrics enum values (e.g., GalileoMetrics.correctness)
            - Metric objects with name and optional version
            - LocalMetricConfig objects for custom local metrics
            - String names of built-in metrics

        Returns
        -------
        tuple[builtins.list[ScorerConfig], builtins.list[LocalMetricConfig]]
            A tuple containing the configured scorer configs and local metric configs.

        Raises
        ------
        ValueError
            If log stream or project cannot be found, or if metrics are unknown.

        Examples
        --------
        ```python
        # Enable built-in metrics with explicit parameters
        from galileo.log_streams import LogStreams
        from galileo.schema.metrics import GalileoMetrics

        log_streams = LogStreams()
        scorer_configs, local_metrics = log_streams.enable_metrics(
            log_stream_name="Production Logs",
            project_name="My AI Project",
            metrics=[
                GalileoMetrics.correctness,
                GalileoMetrics.completeness,
                "context_relevance",
            ],
        )

        # Enable metrics using environment variables
        # export GALILEO_LOG_STREAM="Production Logs"
        # export GALILEO_PROJECT="My AI Project"
        scorer_configs, local_metrics = log_streams.enable_metrics(
            metrics=["correctness", "completeness"]
        )

        # Enable custom metrics with mixed parameters
        from galileo.schema.metrics import Metric, LocalMetricConfig

        def custom_scorer(trace_or_span):
            return 0.85  # Custom scoring logic

        # export GALILEO_PROJECT="My AI Project"
        scorer_configs, local_metrics = log_streams.enable_metrics(
            log_stream_name="Production Logs",  # Explicit log stream
            # project_name from env var
            metrics=[
                Metric(name="my_custom_metric", version=2),
                LocalMetricConfig(name="local_scorer", scorer_fn=custom_scorer)
            ]
        )
        ```
        """
        # Apply environment variable fallbacks
        project_name = project_name or _get_project_from_env()
        log_stream_name = log_stream_name or _get_log_stream_from_env()

        # Get project using environment fallbacks
        project_obj = Projects().get_with_env_fallbacks(name=project_name)
        if not project_obj:
            raise ValueError(f"Project '{project_name}' not found")

        # Get log stream - error out if not found
        log_stream = self.get(name=log_stream_name, project_name=project_obj.name)
        if not log_stream:
            raise ValueError(f"Log stream '{log_stream_name}' not found in project '{project_obj.name}'")

        # Use the shared utility function directly
        _, local_metrics = create_metric_configs(project_obj.id, log_stream.id, metrics)
        return local_metrics


#
# Convenience methods
#


def get_log_stream(
    *, name: str | None = None, project_id: str | None = None, project_name: str | None = None
) -> LogStream | None:
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


def list_log_streams(
    *,
    project_id: str | None = None,
    project_name: str | None = None,
    limit: Unset | int = 100,
    starting_token: Unset | int = 0,
) -> builtins.list[LogStream]:
    """
    Lists log streams. Exactly one of `project_id` or `project_name` must be provided.

    Returns a single page of results. Use `starting_token` (from
    `next_starting_token` on a prior response) to fetch subsequent pages.

    Parameters
    ----------
    project_id : str
        The id of the project.
    project_name : str
        The name of the project.
    limit : Union[Unset, int], optional
        The maximum number of log streams to return per page. Defaults to 100.
    starting_token : Union[Unset, int], optional
        The pagination token to start from. Defaults to 0 (first page).

    Returns
    -------
    builtins.list[LogStream]
        A page of log streams.

    Raises
    ------
    errors.UnexpectedStatus
        If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
    httpx.TimeoutException
        If the request takes longer than Client.timeout.

    """
    return LogStreams().list(
        project_id=project_id, project_name=project_name, limit=limit, starting_token=starting_token
    )


def create_log_stream(name: str, project_id: str | None = None, project_name: str | None = None) -> LogStream:
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


def enable_metrics(
    *,
    log_stream_name: str | None = None,
    project_name: str | None = None,
    metrics: builtins.list[GalileoMetrics | Metric | LocalMetricConfig | str],
) -> builtins.list[LocalMetricConfig]:
    """
    Enable metrics for a log stream with flexible parameter and environment variable support.

    This unified function supports both explicit parameters and environment variable fallbacks,
    making it perfect for all use cases - from production CI/CD pipelines to development testing.

    **Flexible Usage Patterns:**
    - **Environment-only**: Just pass metrics, names from env vars (production/CI)
    - **Explicit parameters**: Specify project/log stream names directly (development)
    - **Mixed approach**: Combine explicit params with environment fallbacks

    Environment Variables (Optional Fallbacks)
    ------------------------------------------
    GALILEO_PROJECT : str
        The name of the Galileo project (used when project_name not provided)
    GALILEO_LOG_STREAM : str
        The name of the log stream (used when log_stream_name not provided)

    Parameters
    ----------
    log_stream_name : Optional[str], optional
        The name of the log stream. Takes precedence over GALILEO_LOG_STREAM environment variable.
        If None, will use GALILEO_LOG_STREAM env var. Defaults to None.
    project_name : Optional[str], optional
        The name of the project. Takes precedence over GALILEO_PROJECT environment variable.
        If None, will use GALILEO_PROJECT env var. Defaults to None.
    metrics : builtins.list[Union[GalileoMetrics, Metric, LocalMetricConfig, str]]
        List of metrics to enable on the log stream. Can include:
        - GalileoMetrics enum values (e.g., GalileoMetrics.correctness)
        - Metric objects with name and optional version for custom metrics
        - LocalMetricConfig objects for client-side custom scoring functions
        - String names of built-in metrics (e.g., "correctness", "toxicity")

    Returns
    -------
    builtins.list[LocalMetricConfig]
        List of local metric configurations that must be computed client-side.
        Server-side metrics are automatically registered with Galileo and don't
        need to be returned since users don't interact with them.

    Raises
    ------
    ValueError
        If log stream or project cannot be found, or if any specified metrics are unknown.
    errors.UnexpectedStatus
        If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
    httpx.TimeoutException
        If the request takes longer than Client.timeout.

    Examples
    --------
    ```python
    # Enable built-in metrics with explicit parameters
    from galileo.log_streams import enable_metrics
    from galileo.schema.metrics import GalileoMetrics

    local_metrics = enable_metrics(
        log_stream_name="Production Logs",
        project_name="My AI Project",
        metrics=[
            GalileoMetrics.correctness,
            GalileoMetrics.completeness,
            "context_relevance",
        ],
    )

    # Enable metrics using environment variables only
    # export GALILEO_LOG_STREAM="Production Logs"
    # export GALILEO_PROJECT="My AI Project"
    local_metrics = enable_metrics(metrics=["correctness", "completeness"])

    # Enable custom and local metrics with environment variable fallbacks
    from galileo.schema.metrics import Metric, LocalMetricConfig
    from galileo_core.schemas.logging.step import StepType

    def response_length_scorer(trace_or_span):
        '''Custom metric that scores based on response length'''
        if hasattr(trace_or_span, "output") and trace_or_span.output:
            return min(len(trace_or_span.output) / 100.0, 1.0)  # Normalize 0-1
        return 0.0

    local_metrics = enable_metrics(
        log_stream_name="Development Logs",
        metrics=[
            GalileoMetrics.correctness,
            "toxicity",
            Metric(name="my_custom_metric", version=2),
            LocalMetricConfig(
                name="response_length",
                scorer_fn=response_length_scorer,
                scorable_types=[StepType.llm],
                aggregatable_types=[StepType.trace],
            ),
        ],
    )

    # Process local metrics
    for local_metric in local_metrics:
        logger.info(f"Need to process local metric: {local_metric.name}")
    ```
    """
    return LogStreams().enable_metrics(log_stream_name=log_stream_name, project_name=project_name, metrics=metrics)
