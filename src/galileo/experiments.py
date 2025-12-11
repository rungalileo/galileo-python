import builtins
import datetime
import logging
from sys import getsizeof
from typing import Any, Callable, Optional, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from galileo import galileo_context, log
from galileo.config import GalileoPythonConfig
from galileo.datasets import Dataset, convert_dataset_row_to_record
from galileo.experiment_tags import upsert_experiment_tag
from galileo.jobs import Jobs
from galileo.projects import Project, Projects
from galileo.prompts import PromptTemplate
from galileo.resources.api.experiment import (
    create_experiment_projects_project_id_experiments_post,
    list_experiments_projects_project_id_experiments_get,
)
from galileo.resources.models import ExperimentResponse, HTTPValidationError, PromptRunSettings, ScorerConfig, TaskType
from galileo.schema.datasets import DatasetRecord
from galileo.schema.metrics import GalileoScorers, LocalMetricConfig, Metric
from galileo.utils.datasets import create_rows_from_records, load_dataset
from galileo.utils.logging import get_logger
from galileo.utils.metrics import create_metric_configs

_logger = get_logger(__name__)

EXPERIMENT_TASK_TYPE: TaskType = 16

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

    def create(self, project_id: str, name: str, dataset_obj: Optional[Dataset] = None) -> ExperimentResponse:
        body = ExperimentCreateRequest(name=name, task_type=EXPERIMENT_TASK_TYPE)
        if dataset_obj is not None:
            dataset = {"dataset_id": dataset_obj.dataset.id, "version_index": dataset_obj.dataset.current_version_index}
            body.additional_properties["dataset"] = dataset

        experiment = create_experiment_projects_project_id_experiments_post.sync(
            project_id=project_id, client=self.config.api_client, body=body
        )
        if experiment is None:
            raise ValueError("experiment is None")

        if isinstance(experiment, HTTPValidationError):
            raise ValueError(experiment.detail)

        return experiment

    def get(self, project_id: str, experiment_name: str) -> Optional[ExperimentResponse]:
        experiments = self.list(project_id=project_id)

        if experiments is None or isinstance(experiments, HTTPValidationError):
            return None

        for experiment in experiments:
            if experiment.name == experiment_name:
                return experiment

        return None

    def get_or_create(
        self, project_id: str, experiment_name: str
    ) -> Optional[Union[ExperimentResponse, HTTPValidationError]]:
        experiment = self.get(project_id, experiment_name)
        if not experiment:
            experiment = self.create(project_id, experiment_name)

        return experiment

    def list(self, project_id: str) -> Optional[Union[HTTPValidationError, list["ExperimentResponse"]]]:
        return list_experiments_projects_project_id_experiments_get.sync(
            project_id=project_id, client=self.config.api_client
        )

    def run(
        self,
        project_obj: Project,
        experiment_obj: ExperimentResponse,
        prompt_template: PromptTemplate,
        dataset_id: str,
        scorers: Optional[builtins.list[ScorerConfig]],
        prompt_settings: Optional[PromptRunSettings] = None,
    ) -> dict[str, Any]:
        if prompt_settings is None:
            prompt_settings = PromptRunSettings(
                n=1,
                echo=False,
                tools=None,
                top_k=40,
                top_p=1.0,
                logprobs=True,
                max_tokens=256,
                model_alias="GPT-4o",
                temperature=0.8,
                tool_choice=None,
                top_logprobs=5,
                stop_sequences=None,
                deployment_name=None,
                response_format=None,
                presence_penalty=0.0,
                frequency_penalty=0.0,
            )

        job = Jobs().create(
            name="playground_run",
            project_id=project_obj.id,
            run_id=experiment_obj.id,
            prompt_template_id=prompt_template.selected_version_id,
            dataset_id=dataset_id,
            task_type=EXPERIMENT_TASK_TYPE,
            scorers=scorers,
            prompt_settings=prompt_settings,
        )

        _logger.debug(f"job: {job}")

        link = f"{self.config.console_url}/project/{project_obj.id}/experiments/{experiment_obj.id}"
        message = f"Experiment {experiment_obj.name} has started and is currently processing. Results will be available at {link}"
        _logger.info(message)

        return {"experiment": experiment_obj, "link": link, "message": message}

    def run_with_function(
        self,
        project_obj: Project,
        experiment_obj: ExperimentResponse,
        dataset_obj: Optional[Dataset],
        records: Optional[builtins.list[DatasetRecord]],
        func: Callable,
        local_metrics: builtins.list[LocalMetricConfig],
    ) -> dict[str, Any]:
        if dataset_obj is None and records is None:
            raise ValueError("Either dataset_obj or records must be provided")
        results = []
        galileo_context.init(project=project_obj.name, experiment_id=experiment_obj.id, local_metrics=local_metrics)

        def logged_process_func(row: DatasetRecord) -> Callable:
            return log(name=experiment_obj.name, dataset_record=row)(func)

        starting_token = 0
        while True:
            if dataset_obj:
                _logger.info(f"Loading dataset content starting at token {starting_token}")
                content = dataset_obj.get_content(starting_token=starting_token, limit=DATASET_CONTENT_PAGE_SIZE)
                if not content or not content.rows:
                    _logger.info("No more dataset content to process")
                    break
                records = [convert_dataset_row_to_record(row) for row in content.rows]
            if not records:
                break
            #  process each row in the dataset
            _logger.info(f"Processing {len(records)} rows from dataset")
            for row in records:
                results.append(process_row(row, logged_process_func(row)))
                galileo_context.reset_trace_context()
                if getsizeof(results) > MAX_REQUEST_SIZE_BYTES or len(results) >= MAX_INGEST_BATCH_SIZE:
                    _logger.info("Flushing logger due to size limit")
                    galileo_context.flush()
                    results = []
            if not dataset_obj:
                break
            starting_token += len(records)

        # flush the logger
        galileo_context.flush()

        _logger.info(f" {len(results)} rows processed for experiment {experiment_obj.name}.")

        link = f"{self.config.console_url}/project/{project_obj.id}/experiments/{experiment_obj.id}"
        message = f"Experiment {experiment_obj.name} has completed and results are available at {link}"
        _logger.info(message)

        return {"experiment": experiment_obj, "link": link, "message": message}


def process_row(row: DatasetRecord, process_func: Callable) -> str:
    _logger.info(f"Processing dataset row: {row}")
    try:
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
    prompt_template: Optional[PromptTemplate] = None,
    prompt_settings: Optional[PromptRunSettings] = None,
    project: Optional[str] = None,
    project_id: Optional[str] = None,
    dataset: Optional[Union[Dataset, list[Union[dict[str, Any], str]], str]] = None,
    dataset_id: Optional[str] = None,
    dataset_name: Optional[str] = None,
    metrics: Optional[list[Union[GalileoScorers, Metric, LocalMetricConfig, str]]] = None,
    function: Optional[Callable] = None,
    experiment_tags: Optional[dict[str, str]] = None,
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
        Settings for prompt runs
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

    Returns
    -------
    Experiment run results

    Raises
    ------
    ValueError
        If required parameters are missing or invalid
    """
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

    # Create or get experiment
    existing_experiment = Experiments().get(project_obj.id, experiment_name)

    if existing_experiment:
        logging.warning(f"Experiment {existing_experiment.name} already exists, adding a timestamp")
        now = datetime.datetime.now(datetime.timezone.utc)
        # based on TS SDK implementation new Date()
        #       .toISOString()
        #       .replace('T', ' at ')
        #       .replace('Z', '');
        experiment_name = f"{existing_experiment.name} {now:%Y-%m-%d} at {now:%H:%M:%S}.{now.microsecond // 1000:03d}"

    experiment_obj = Experiments().create(project_obj.id, experiment_name, dataset_obj)

    if experiment_tags is not None:
        for key, value in experiment_tags.items():
            try:
                upsert_experiment_tag(project_obj.id, experiment_obj.id, key, value)
                _logger.debug(f"Added tag {key}={value} to experiment {experiment_obj.id}")
            except Exception as e:
                _logger.warning(f"Failed to add tag {key}={value} to experiment {experiment_obj.id}: {e}")

    # Set up metrics if provided
    scorer_settings: Optional[list[ScorerConfig]] = None
    local_metrics: list[LocalMetricConfig] = []
    if metrics is not None:
        scorer_settings, local_metrics = create_metric_configs(project_obj.id, experiment_obj.id, metrics)

    # Execute a runner function experiment
    if function is not None:
        return Experiments().run_with_function(
            project_obj=project_obj,
            experiment_obj=experiment_obj,
            dataset_obj=dataset_obj,
            records=records,
            func=function,
            local_metrics=local_metrics,
        )

    if prompt_template is None:
        raise ValueError("A prompt template must be provided")

    if dataset_obj is None:
        raise ValueError("A dataset object must be provided")

    if local_metrics:
        raise ValueError("Local metrics can only be used with a locally run experiment, not a prompt experiment.")

    # Execute a prompt template experiment
    return Experiments().run(
        project_obj, experiment_obj, prompt_template, dataset_obj.dataset.id, scorer_settings, prompt_settings
    )


def create_experiment(
    project_id: Optional[str] = None, experiment_name: Optional[str] = None, project_name: Optional[str] = None
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

    Returns
    -------
    ExperimentResponse
        The created experiment response.

    Raises
    ------
    ValueError
        If `experiment_name` is not provided, or if the project cannot be resolved from `project_id` or `project`.
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

    return Experiments().create(project_obj.id, experiment_name)


def get_experiment(
    project_id: Optional[str] = None, experiment_name: Optional[str] = None, project_name: Optional[str] = None
) -> Optional[ExperimentResponse]:
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
    project_id: Optional[str] = None, project_name: Optional[str] = None
) -> Optional[Union[HTTPValidationError, list[ExperimentResponse]]]:
    """
    Get experiments from the specified Project.

    Parameters
    ----------
    project_id
        Optional project Id. Takes preference over the GALILEO_PROJECT_ID environment variable. Leave empty if using ``project``
    project_name
        Optional project name. Takes preference over the GALILEO_PROJECT environment variable. Leave empty if using ``project_id``

    Returns
    -------
    List of ExperimentResponse results

    Raises
    ------
    HTTPValidationError
        If there's a validation error in returning a list of ExperimentResponse
    """
    # Resolve project by id, name, or environment fallbacks
    project_obj = Projects().get_with_env_fallbacks(id=project_id, name=project_name)
    if not project_obj:
        if project_name:
            raise ValueError(f"Project {project_name} does not exist")
        raise ValueError("Project not specified and no defaults found")

    return Experiments().list(project_id=project_obj.id)
