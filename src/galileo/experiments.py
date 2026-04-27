import builtins
import datetime
import logging
from collections.abc import Callable
from sys import getsizeof
from typing import Any

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from galileo.config import GalileoPythonConfig
from galileo.datasets import Dataset, convert_dataset_row_to_record
from galileo.decorator import galileo_context, galileo_dataset_context, log
from galileo.experiment_tags import upsert_experiment_tag
from galileo.projects import Project, Projects
from galileo.prompts import PromptTemplate
from galileo.resources.api.experiment import (
    create_experiment_projects_project_id_experiments_post,
    list_experiments_projects_project_id_experiments_get,
)
from galileo.resources.models import ExperimentResponse, HTTPValidationError, PromptRunSettings, ScorerConfig, TaskType
from galileo.schema.datasets import DatasetRecord
from galileo.schema.experiment_group import ExperimentGroupResponse
from galileo.schema.metrics import GalileoMetrics, LocalMetricConfig, Metric
from galileo.utils.datasets import create_rows_from_records, load_dataset
from galileo.utils.exceptions import _format_http_validation_error
from galileo.utils.headers_data import get_sdk_header
from galileo.utils.log_config import get_logger
from galileo.utils.metrics import create_metric_configs
from galileo_core.constants.request_method import RequestMethod

_logger = get_logger(__name__)

EXPERIMENT_TASK_TYPE: TaskType = 16


def _default_prompt_settings(model_alias: str = "GPT-4o") -> PromptRunSettings:
    """Return a PromptRunSettings with complete defaults for prompt-driven experiment flows.

    The server requires a fully populated settings object to start the experiment runner job.
    Omitting fields (relying on server defaults) causes the job to silently never start.
    """
    return PromptRunSettings(
        n=1,
        echo=False,
        tools=None,
        top_k=40,
        top_p=1.0,
        logprobs=True,
        max_tokens=256,
        model_alias=model_alias,
        temperature=0.8,
        tool_choice=None,
        top_logprobs=5,
        stop_sequences=None,
        deployment_name=None,
        response_format=None,
        presence_penalty=0.0,
        frequency_penalty=0.0,
    )


MAX_REQUEST_SIZE_BYTES = 10 * 1024 * 1024  # 10 MB
MAX_INGEST_BATCH_SIZE = 128
DATASET_CONTENT_PAGE_SIZE = 1000


@_attrs_define
class ExperimentCreateRequest:
    name: str
    task_type: int
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name = self.name
        task_type = self.task_type

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({"name": name})
        field_dict.update({"task_type": task_type})

        return field_dict


class Experiments:
    config: GalileoPythonConfig

    def __init__(self) -> None:
        self.config = GalileoPythonConfig.get()

    def create(
        self,
        project_id: str,
        name: str,
        dataset_obj: Dataset | None = None,
        trigger: bool = False,
        prompt_template: PromptTemplate | None = None,
        scorers: builtins.list[ScorerConfig] | None = None,
        prompt_settings: PromptRunSettings | dict[str, Any] | None = None,
        experiment_group_id: str | None = None,
        experiment_group_name: str | None = None,
    ) -> ExperimentResponse:
        # If both experiment_group_id and experiment_group_name are provided, the API gives
        # precedence to the ID and silently ignores the name (see resolve_and_assign_group).
        # We log it here so customers can spot unintentional duplication, but we do not
        # reject — the API contract permits both.
        if experiment_group_id is not None and experiment_group_name is not None:
            _logger.debug(
                "Both experiment_group_id and experiment_group_name provided; "
                "the API will use experiment_group_id and ignore the name."
            )

        resolved_settings: PromptRunSettings | None = (
            PromptRunSettings.from_dict(prompt_settings) if isinstance(prompt_settings, dict) else prompt_settings
        )

        body = ExperimentCreateRequest(name=name, task_type=EXPERIMENT_TASK_TYPE)

        if dataset_obj is not None:
            body.additional_properties["dataset"] = {
                "dataset_id": str(dataset_obj.dataset.id),
                "version_index": dataset_obj.dataset.current_version_index,
            }

        if prompt_template is not None:
            body.additional_properties["prompt_template_version_id"] = str(prompt_template.selected_version_id)

        if resolved_settings is not None:
            body.additional_properties["prompt_settings"] = resolved_settings.to_dict()

        if scorers is not None:
            body.additional_properties["scorers"] = [s.to_dict() for s in scorers]

        if trigger:
            body.additional_properties["trigger"] = True

        if experiment_group_id is not None:
            body.additional_properties["experiment_group_id"] = experiment_group_id
        if experiment_group_name is not None:
            body.additional_properties["experiment_group_name"] = experiment_group_name

        experiment = create_experiment_projects_project_id_experiments_post.sync(
            project_id=project_id, client=self.config.api_client, body=body
        )
        if experiment is None:
            raise ValueError("experiment is None")

        if isinstance(experiment, HTTPValidationError):
            raise ValueError(_format_http_validation_error(experiment))

        return experiment

    def get(self, project_id: str, experiment_name: str) -> ExperimentResponse | None:
        experiments = self.list(project_id=project_id)

        if experiments is None or isinstance(experiments, HTTPValidationError):
            return None

        for experiment in experiments:
            if experiment.name == experiment_name:
                return experiment

        return None

    def get_or_create(self, project_id: str, experiment_name: str) -> ExperimentResponse | HTTPValidationError | None:
        experiment = self.get(project_id, experiment_name)
        if not experiment:
            experiment = self.create(project_id, experiment_name)

        return experiment

    def list(self, project_id: str) -> HTTPValidationError | list["ExperimentResponse"] | None:
        return list_experiments_projects_project_id_experiments_get.sync(
            project_id=project_id, client=self.config.api_client
        )

    def run(
        self,
        project_obj: Project,
        dataset_obj: Dataset,
        experiment_name: str,
        prompt_template: PromptTemplate | None,
        scorers: builtins.list[ScorerConfig] | None,
        prompt_settings: PromptRunSettings | dict[str, Any] | None = None,
        experiment_group_id: str | None = None,
        experiment_group_name: str | None = None,
    ) -> dict[str, Any]:
        if isinstance(prompt_settings, dict):
            prompt_settings = PromptRunSettings.from_dict(prompt_settings)

        # Only set default prompt_settings for prompt-driven flow (when a template is provided)
        if prompt_template is not None and prompt_settings is None:
            prompt_settings = _default_prompt_settings()

        # Single API call: create experiment + trigger job via trigger=True
        # Only forward group kwargs when set so existing callers/tests aren't affected.
        group_kwargs: dict[str, Any] = {}
        if experiment_group_id is not None:
            group_kwargs["experiment_group_id"] = experiment_group_id
        if experiment_group_name is not None:
            group_kwargs["experiment_group_name"] = experiment_group_name
        experiment_obj = self.create(
            project_id=project_obj.id,
            name=experiment_name,
            dataset_obj=dataset_obj,
            trigger=True,
            prompt_template=prompt_template,
            scorers=scorers,
            prompt_settings=prompt_settings,
            **group_kwargs,
        )

        link = f"{str(self.config.console_url).rstrip('/')}/project/{project_obj.id}/experiments/{experiment_obj.id}"
        message = f"Experiment {experiment_obj.name} has started and is currently processing. Results will be available at {link}"
        _logger.info(message)

        return {"experiment": experiment_obj, "link": link, "message": message}

    def run_with_function(
        self,
        project_obj: Project,
        experiment_obj: ExperimentResponse,
        dataset_obj: Dataset | None,
        records: builtins.list[DatasetRecord] | None,
        func: Callable,
        local_metrics: builtins.list[LocalMetricConfig],
        on_error: Callable[[Exception], None] | None = None,
    ) -> dict[str, Any]:
        if dataset_obj is None and records is None:
            raise ValueError("Either dataset_obj or records must be provided")
        results = []
        galileo_context.init(project=project_obj.name, experiment_id=experiment_obj.id, local_metrics=local_metrics)

        def logged_process_func(row: DatasetRecord) -> Callable:
            return log(name=experiment_obj.name, dataset_record=row)(func)

        # For static records (list), process once
        if records is not None:
            _logger.info(f"Processing {len(records)} rows from dataset")
            for row in records:
                results.append(process_row(row, logged_process_func(row)))
                galileo_context.reset_trace_context()
                if getsizeof(results) > MAX_REQUEST_SIZE_BYTES or len(results) >= MAX_INGEST_BATCH_SIZE:
                    _logger.info("Flushing logger due to size limit")
                    galileo_context.flush(on_error=on_error)
                    results = []
        # For dataset object, paginate through content
        elif dataset_obj is not None:
            starting_token = 0
            has_more_data = True

            while has_more_data:
                _logger.info(f"Loading dataset content starting at token {starting_token}")
                content = dataset_obj.get_content(starting_token=starting_token, limit=DATASET_CONTENT_PAGE_SIZE)

                if not content or not content.rows:
                    _logger.info("No more dataset content to process")
                    has_more_data = False
                else:
                    batch_records = [convert_dataset_row_to_record(row) for row in content.rows]
                    _logger.info(f"Processing {len(batch_records)} rows from dataset")

                    for row in batch_records:
                        results.append(process_row(row, logged_process_func(row)))
                        galileo_context.reset_trace_context()
                        if getsizeof(results) > MAX_REQUEST_SIZE_BYTES or len(results) >= MAX_INGEST_BATCH_SIZE:
                            _logger.info("Flushing logger due to size limit")
                            galileo_context.flush(on_error=on_error)
                            results = []

                    starting_token += len(batch_records)

        # flush the logger
        galileo_context.flush(on_error=on_error)

        _logger.info(f" {len(results)} rows processed for experiment {experiment_obj.name}.")

        link = f"{str(self.config.console_url).rstrip('/')}/project/{project_obj.id}/experiments/{experiment_obj.id}"
        message = f"Experiment {experiment_obj.name} has completed and results are available at {link}"
        _logger.info(message)

        return {"experiment": experiment_obj, "link": link, "message": message}


def process_row(row: DatasetRecord, process_func: Callable) -> str:
    _logger.info(f"Processing dataset row: {row}")
    try:
        # Set dataset context for OTEL spans (ground truth for scorers)
        # This ensures OTEL-instrumented frameworks get dataset fields attached to their spans
        with galileo_dataset_context(dataset_input=row.input, dataset_output=row.output, dataset_metadata=row.metadata):
            output = process_func(row.deserialized_input)
            log = galileo_context.get_logger_instance()
            log.conclude(output)
    except Exception as exc:
        output = f"error during executing: {process_func.__name__}: {exc}"
        _logger.error(output)
    return output


def run_experiment(
    experiment_name: str,
    *,
    prompt_template: PromptTemplate | None = None,
    prompt_settings: PromptRunSettings | dict[str, Any] | None = None,
    project: str | None = None,
    project_id: str | None = None,
    dataset: Dataset | list[dict[str, Any] | str] | str | None = None,
    dataset_id: str | None = None,
    dataset_name: str | None = None,
    metrics: list[GalileoMetrics | Metric | LocalMetricConfig | str] | None = None,
    function: Callable | None = None,
    experiment_tags: dict[str, str] | None = None,
    on_error: Callable[[Exception], None] | None = None,
    experiment_group: str | None = None,
    experiment_group_id: str | None = None,
) -> Any:
    """
    Run an experiment with the specified parameters.

    There are two ways to run an experiment:
    1. Using a prompt template, prompt settings, and a dataset
    2. Using a runner function and a dataset

    When using a runner function, you can also pass a list of dictionaries to the function to act as a dataset.

    The project can be specified by providing exactly one of the project name (via the 'project' parameter or the GALILEO_PROJECT environment variable) or the project ID (via the 'project_id' parameter or the GALILEO_PROJECT_ID environment variable).

    Parameters
    ----------
    experiment_name
        Name of the experiment
    prompt_template
        Template for prompts
    prompt_settings
        Settings for prompt runs. Accepts a ``PromptRunSettings`` instance or a plain ``dict``
        with matching field names, which will be coerced to ``PromptRunSettings`` automatically.
    project
        Optional project name. Takes preference over the GALILEO_PROJECT environment variable. Leave empty if using project_id
    project_id
        Optional project Id. Takes preference over the GALILEO_PROJECT_ID environment variable. Leave empty if using project
    dataset
        Dataset object, list of records, or dataset name
    dataset_id
        ID of the dataset
    dataset_name
        Name of the dataset
    metrics
        List of metrics to evaluate
    function
        Optional function to run with the experiment
    experiment_tags
        Optional dictionary of key-value pairs to tag the experiment with
    on_error
        Optional callback invoked with the exception when a flush error occurs. Only applies
        to the function flow — ignored in the prompt-template flow (a warning is logged if
        provided there). Creation errors always propagate regardless of this callback. If None,
        flush errors are logged as warnings. Defaults to None.
    experiment_group
        Optional name of an experiment group to assign this run to. If a group with this
        name does not exist in the project, the API auto-creates it. If neither
        ``experiment_group`` nor ``experiment_group_id`` is provided and the run has a
        dataset, the API auto-creates a group named ``"<dataset_name> Experiment Group"``;
        otherwise the run lands in the project's system "Ungrouped" group.
    experiment_group_id
        Optional UUID of an existing experiment group. If the group does not exist in this
        project, the SDK raises ``galileo.NotFoundError`` (HTTP 404,
        API error_code 3520) before the run is created.
        If both ``experiment_group_id`` and ``experiment_group`` are provided, the API
        uses the ID and silently ignores the name.

    Returns
    -------
    Experiment run results

    Raises
    ------
    ValueError
        If required parameters are missing or invalid.
    galileo.NotFoundError
        If ``experiment_group_id`` is provided but the group does not exist in the project.
    """
    if isinstance(prompt_settings, dict):
        prompt_settings = PromptRunSettings.from_dict(prompt_settings)

    # Load dataset and records
    dataset_obj = load_dataset(dataset, dataset_id, dataset_name)

    # Validate experiment configuration
    if prompt_template and not dataset_obj:
        raise ValueError("A dataset record, id, or name of a dataset must be provided when a prompt_template is used")

    if function and prompt_template:
        raise ValueError("A function or prompt_template should be provided, but not both")

    records = None
    if not dataset_obj and isinstance(dataset, list):
        records = create_rows_from_records(dataset)

    if function and not dataset_obj and not records:
        raise ValueError("A dataset record, id, name, or a list of records must be provided when a function is used")

    # Get the project from the name or Id
    project_obj = Projects().get_with_env_fallbacks(id=project_id, name=project)

    # Ensure we have a valid project
    if not project_obj:
        if project_id:
            raise ValueError(f"Project with Id {project_id} does not exist")
        raise ValueError(f"Project {project} does not exist")

    # Handle experiment name collision
    existing_experiment = Experiments().get(project_obj.id, experiment_name)

    if existing_experiment:
        logging.warning(f"Experiment {existing_experiment.name} already exists, adding a timestamp")
        now = datetime.datetime.now(datetime.timezone.utc)
        experiment_name = f"{existing_experiment.name} {now:%Y-%m-%d} at {now:%H:%M:%S}.{now.microsecond // 1000:03d}"

    # Execute a runner function experiment (custom function flow — uses logstream pipeline)
    # Only forward group kwargs when set so existing callers/tests aren't affected.
    group_kwargs: dict[str, Any] = {}
    if experiment_group_id is not None:
        group_kwargs["experiment_group_id"] = experiment_group_id
    if experiment_group is not None:
        group_kwargs["experiment_group_name"] = experiment_group

    if function is not None:
        experiment_obj = Experiments().create(project_obj.id, experiment_name, dataset_obj, **group_kwargs)

        # Set up metrics WITH run_id — custom function flow needs ScorerSettings registered
        local_metrics: list[LocalMetricConfig] = []
        if metrics is not None:
            _, local_metrics = create_metric_configs(project_obj.id, experiment_obj.id, metrics)

        if experiment_tags is not None:
            for key, value in experiment_tags.items():
                try:
                    upsert_experiment_tag(project_obj.id, experiment_obj.id, key, value)
                    _logger.debug(f"Added tag {key}={value} to experiment {experiment_obj.id}")
                except Exception as e:
                    _logger.warning(f"Failed to add tag {key}={value} to experiment {experiment_obj.id}: {e}")

        return Experiments().run_with_function(
            project_obj=project_obj,
            experiment_obj=experiment_obj,
            dataset_obj=dataset_obj,
            records=records,
            func=function,
            local_metrics=local_metrics,
            on_error=on_error,
        )

    if dataset_obj is None:
        raise ValueError("A dataset object must be provided")

    # Set up metrics WITHOUT run_id — trigger=True flow, API handles scorer registration
    scorer_settings: list[ScorerConfig] | None = None
    local_metrics_check: list[LocalMetricConfig] = []
    if metrics is not None:
        scorer_settings, local_metrics_check = create_metric_configs(project_obj.id, None, metrics)

    if local_metrics_check:
        raise ValueError("Local metrics can only be used with a locally run experiment, not a prompt experiment.")

    if on_error is not None:
        _logger.warning(
            "on_error was provided but will not be invoked in the prompt-template flow "
            "(no flush occurs on this path). on_error is only used in the function flow."
        )

    # Execute a prompt template or generated-output experiment via trigger=True.
    # Single API call: creates experiment + triggers runner job.
    # If prompt_template is None, the API determines the flow based on the dataset contents.
    # The API will return error 3512 if the dataset has no generated_output column.
    result = Experiments().run(
        project_obj, dataset_obj, experiment_name, prompt_template, scorer_settings, prompt_settings, **group_kwargs
    )

    if experiment_tags is not None:
        experiment_obj = result["experiment"]
        for key, value in experiment_tags.items():
            try:
                upsert_experiment_tag(project_obj.id, experiment_obj.id, key, value)
                _logger.debug(f"Added tag {key}={value} to experiment {experiment_obj.id}")
            except Exception as e:
                _logger.warning(f"Failed to add tag {key}={value} to experiment {experiment_obj.id}: {e}")

    return result


def create_experiment(
    project_id: str | None = None,
    experiment_name: str | None = None,
    project_name: str | None = None,
    *,
    experiment_group: str | None = None,
    experiment_group_id: str | None = None,
) -> ExperimentResponse:
    """
    Create an experiment with the specified parameters.

    The project can be specified by providing exactly one of the project name (via the 'project' parameter or the GALILEO_PROJECT environment variable)
    or the project ID (via the 'project_id' parameter or the GALILEO_PROJECT_ID environment variable).

    Parameters
    ----------
    project_id
        Optional project Id. Takes preference over the GALILEO_PROJECT_ID environment variable. Leave empty if using project
    experiment_name
        Name of the experiment. Required.
    project
        Optional project name. Takes preference over the GALILEO_PROJECT environment variable. Leave empty if using project_id
    experiment_group
        Optional name of an experiment group to assign this experiment to. If a group with
        this name does not exist in the project, the API auto-creates it.
    experiment_group_id
        Optional UUID of an existing experiment group. If the group does not exist in this
        project, the SDK raises ``galileo.NotFoundError`` (HTTP 404,
        API error_code 3520).
        If both ``experiment_group_id`` and ``experiment_group`` are provided, the API
        uses the ID and silently ignores the name.

    Returns
    -------
    ExperimentResponse
        The created experiment response.

    Raises
    ------
    ValueError
        If `experiment_name` is not provided or if the project cannot be resolved from
        `project_id` or `project`.
    galileo.NotFoundError
        If ``experiment_group_id`` is provided but the group does not exist in the project.
    HTTPValidationError
        If there's a validation error in returning an ExperimentResponse.
    """
    # Enforce required experiment_name at runtime while keeping signature backward compatible for positional calls.
    if not experiment_name:
        raise ValueError("experiment_name is required")

    # Resolve project by id, name, or environment fallbacks
    project_obj = Projects().get_with_env_fallbacks(id=project_id, name=project_name)
    if not project_obj:
        if project_name:
            raise ValueError(f"Project {project_name} does not exist")
        raise ValueError("Project not specified and no defaults found")

    group_kwargs: dict[str, Any] = {}
    if experiment_group_id is not None:
        group_kwargs["experiment_group_id"] = experiment_group_id
    if experiment_group is not None:
        group_kwargs["experiment_group_name"] = experiment_group
    return Experiments().create(project_obj.id, experiment_name, **group_kwargs)


def get_experiment(
    project_id: str | None = None, experiment_name: str | None = None, project_name: str | None = None
) -> ExperimentResponse | None:
    """
    Get an experiment with the specified parameters.

    The project can be specified by providing exactly one of the project name (via the 'project' parameter or the GALILEO_PROJECT environment variable)
    or the project ID (via the 'project_id' parameter or the GALILEO_PROJECT_ID environment variable).

    Parameters
    ----------
    project_id
        Optional project Id. Takes preference over the GALILEO_PROJECT_ID environment variable. Leave empty if using ``project``
    experiment_name
        Name of the experiment. Required.
    project_name
        Optional project name. Takes preference over the GALILEO_PROJECT environment variable. Leave empty if using ``project_id``

    Returns
    -------
    ExperimentResponse results or ``None`` if not found.

    Raises
    ------
    ValueError
        If ``experiment_name`` is not provided, or if the project cannot be resolved from ``project_id`` or ``project``.
    HTTPValidationError
        If there's a validation error in returning an ExperimentResponse.
    """
    # Enforce required experiment_name at runtime while keeping signature backward compatible for positional calls.
    if not experiment_name:
        raise ValueError("experiment_name is required")

    # Resolve project by id, name, or environment fallbacks
    project_obj = Projects().get_with_env_fallbacks(id=project_id, name=project_name)
    if not project_obj:
        if project_name:
            raise ValueError(f"Project {project_name} does not exist")
        raise ValueError("Project not specified and no defaults found")

    return Experiments().get(project_obj.id, experiment_name)


def get_experiments(
    project_id: str | None = None,
    project_name: str | None = None,
    *,
    experiment_group: str | None = None,
    experiment_group_id: str | None = None,
) -> HTTPValidationError | list[ExperimentResponse] | None:
    """
    Get experiments from the specified Project.

    When no group filter is given, returns all experiments in the project (existing
    behavior, calls ``GET /projects/{id}/experiments``). When ``experiment_group`` or
    ``experiment_group_id`` is provided, returns only experiments assigned to that group
    (calls ``POST /projects/{id}/experiments/search`` and pages internally).

    Parameters
    ----------
    project_id
        Optional project Id. Takes preference over the GALILEO_PROJECT_ID environment variable. Leave empty if using ``project``
    project_name
        Optional project name. Takes preference over the GALILEO_PROJECT environment variable. Leave empty if using ``project_id``
    experiment_group
        Optional experiment-group name to filter by. Returns only experiments assigned to
        a group with this name. Mutually compatible with ``experiment_group_id``: if both
        are provided, both filters are sent and the API resolves precedence.
    experiment_group_id
        Optional experiment-group UUID to filter by. Returns only experiments assigned to
        this group.

    Returns
    -------
    List of ExperimentResponse results. When a filter is set, the list is scoped to the
    matching group; otherwise it is the full project listing.

    Raises
    ------
    HTTPValidationError
        If there's a validation error in returning a list of ExperimentResponse
    httpx.HTTPStatusError
        If the search endpoint returns a non-2xx response (only when a group filter is set).
    """
    # Resolve project by id, name, or environment fallbacks
    project_obj = Projects().get_with_env_fallbacks(id=project_id, name=project_name)
    if not project_obj:
        if project_name:
            raise ValueError(f"Project {project_name} does not exist")
        raise ValueError("Project not specified and no defaults found")

    # No filter → keep existing behavior unchanged (calls GET /experiments via generated client)
    if experiment_group is None and experiment_group_id is None:
        return Experiments().list(project_id=project_obj.id)

    # Filter set → call the search endpoint, page through all results.
    # The search endpoint is not in the generated client today; once it is, this branch
    # should be rewritten to use the generated function.
    filters: list[dict[str, Any]] = []
    if experiment_group_id is not None:
        filters.append(
            {
                "filter_type": "id",
                "name": "experiment_group_id",
                "operator": "eq",
                "value": experiment_group_id,
            }
        )
    if experiment_group is not None:
        filters.append(
            {
                "filter_type": "string",
                "name": "experiment_group_name",
                "operator": "eq",
                "value": experiment_group,
                "case_sensitive": True,
            }
        )

    config = GalileoPythonConfig.get()
    headers = {"Content-Type": "application/json", "X-Galileo-SDK": get_sdk_header()}
    path = f"/projects/{project_obj.id}/experiments/search"

    all_experiments: list[ExperimentResponse] = []
    starting_token: int | None = 0
    while starting_token is not None:
        response = config.api_client.request(
            method=RequestMethod.POST,
            path=path,
            json={"filters": filters, "starting_token": starting_token, "limit": _LIST_EXPERIMENT_GROUPS_PAGE_SIZE},
            content_headers=headers,
            return_raw_response=True,
        )
        response.raise_for_status()
        payload = response.json()
        all_experiments.extend(ExperimentResponse.from_dict(e) for e in payload.get("experiments", []))
        starting_token = payload.get("next_starting_token") if payload.get("paginated") else None

    return all_experiments


_LIST_EXPERIMENT_GROUPS_PAGE_SIZE = 100


def list_experiment_groups(
    project_id: str | None = None, project_name: str | None = None
) -> list[ExperimentGroupResponse]:
    """List all experiment groups in a project.

    Calls ``POST /projects/{project_id}/experiment-groups/query`` and pages through
    every group internally. The full list is returned in a single call; customers
    do not need to handle pagination tokens.

    The project can be specified by providing exactly one of the project name (via the
    ``project_name`` parameter or the ``GALILEO_PROJECT`` environment variable) or the
    project ID (via the ``project_id`` parameter or the ``GALILEO_PROJECT_ID``
    environment variable).

    Parameters
    ----------
    project_id
        Optional project ID. Takes preference over the ``GALILEO_PROJECT_ID`` env var.
    project_name
        Optional project name. Takes preference over the ``GALILEO_PROJECT`` env var.

    Returns
    -------
    list[ExperimentGroupResponse]
        All experiment groups in the project.

    Raises
    ------
    ValueError
        If the project cannot be resolved.
    httpx.HTTPStatusError
        If the API returns a non-2xx response.
    """
    project_obj = Projects().get_with_env_fallbacks(id=project_id, name=project_name)
    if not project_obj:
        if project_name:
            raise ValueError(f"Project {project_name} does not exist")
        raise ValueError("Project not specified and no defaults found")

    # Use the SDK's configured ApiClient — the same client every generated endpoint call
    # uses (see src/galileo/resources/api/experiment/*.py). This preserves auth, base URL,
    # timeout, and SDK headers. The experiment-group routes are not yet in the generated
    # client; once they are, this helper should be rewritten to use the generated function.
    config = GalileoPythonConfig.get()
    headers = {"Content-Type": "application/json", "X-Galileo-SDK": get_sdk_header()}
    path = f"/projects/{project_obj.id}/experiment-groups/query"

    all_groups: list[ExperimentGroupResponse] = []
    starting_token: int | None = 0
    while starting_token is not None:
        response = config.api_client.request(
            method=RequestMethod.POST,
            path=path,
            json={"starting_token": starting_token, "limit": _LIST_EXPERIMENT_GROUPS_PAGE_SIZE},
            content_headers=headers,
            return_raw_response=True,
        )
        response.raise_for_status()
        payload = response.json()
        all_groups.extend(ExperimentGroupResponse.model_validate(g) for g in payload.get("experiment_groups", []))
        starting_token = payload.get("next_starting_token") if payload.get("paginated") else None

    return all_groups
