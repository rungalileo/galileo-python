import builtins
import datetime
import logging
from typing import Any, Callable, Optional, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from galileo import galileo_context, log
from galileo.base import BaseClientModel
from galileo.datasets import Dataset, convert_dataset_content_to_records, get_dataset
from galileo.jobs import Jobs
from galileo.projects import Project, Projects
from galileo.prompts import PromptTemplate
from galileo.resources.api.experiment import (
    create_experiment_projects_project_id_experiments_post,
    list_experiments_projects_project_id_experiments_get,
)
from galileo.resources.models import ExperimentResponse, HTTPValidationError, PromptRunSettings, ScorerConfig, TaskType
from galileo.schema.metrics import LocalScorerConfig
from galileo.scorers import Scorers, ScorerSettings

_logger = logging.getLogger(__name__)

EXPERIMENT_TASK_TYPE = TaskType.VALUE_16


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


class Experiments(BaseClientModel):
    def create(self, project_id: str, name: str) -> ExperimentResponse:
        body = ExperimentCreateRequest(name=name, task_type=EXPERIMENT_TASK_TYPE)

        experiment = create_experiment_projects_project_id_experiments_post.sync(
            project_id=project_id,
            client=self.client,
            body=body,  # type: ignore[arg-type]
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
        return list_experiments_projects_project_id_experiments_get.sync(project_id=project_id, client=self.client)

    @staticmethod
    def create_scorer_configs(
        project_id: str, experiment_id: str, metrics: builtins.list[Union[str, LocalScorerConfig]]
    ) -> tuple[builtins.list[ScorerConfig], builtins.list[LocalScorerConfig]]:
        scorers = []
        scorer_names = [metric for metric in metrics if isinstance(metric, str)]
        if scorer_names:
            all_scorers = Scorers().list()
            known_metrics = {metric.name: metric for metric in all_scorers}
            unknown_metrics = []
            for metric in scorer_names:
                if metric in known_metrics:
                    scorers.append(ScorerConfig.from_dict(known_metrics[metric].to_dict()))
                else:
                    unknown_metrics.append(metric)
            if unknown_metrics:
                raise ValueError(
                    "One or more non-existent metrics are specified:"
                    + ", ".join(f"'{metric}'" for metric in unknown_metrics)
                )
            ScorerSettings().create(project_id=project_id, run_id=experiment_id, scorers=scorers)

        local_scorers = [metric for metric in metrics if isinstance(metric, LocalScorerConfig)]

        return scorers, local_scorers

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

        link = f"{self.client.get_console_url()}/project/{project_obj.id}/experiments/{experiment_obj.id}"
        message = f"Experiment {experiment_obj.name} has started and is currently processing. Results will be available at {link}"
        print(message)

        return {"experiment": experiment_obj, "link": link, "message": message}

    def run_with_function(
        self,
        project_obj: Project,
        experiment_obj: ExperimentResponse,
        records: builtins.list[dict[str, str]],
        func: Callable,
        local_scorers: builtins.list[LocalScorerConfig],
    ) -> dict[str, Any]:
        results = []
        galileo_context.init(project=project_obj.name, experiment_id=experiment_obj.id, local_scorers=local_scorers)  # type: ignore[arg-type]

        logged_process_func = log(name=experiment_obj.name)(func)

        #  process each row in the dataset
        for row in records:
            results.append(process_row(row, logged_process_func))
            galileo_context.reset_trace_context()

        # flush the logger
        galileo_context.flush()

        _logger.info(f" {len(results)} rows processed for experiment {experiment_obj.name}.")

        link = f"{self.client.get_console_url()}/project/{project_obj.id}/experiments/{experiment_obj.id}"
        message = f"Experiment {experiment_obj.name} has completed and results are available at {link}"
        print(message)

        return {"experiment": experiment_obj, "link": link, "message": message}


def process_row(row: dict[str, str], process_func: Callable) -> str:
    _logger.info(f"Processing dataset row: {row}")
    try:
        output = process_func(row)
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
    dataset: Optional[Union[Dataset, list[dict[str, str]], str]] = None,
    dataset_id: Optional[str] = None,
    dataset_name: Optional[str] = None,
    metrics: Optional[list[Union[str, LocalScorerConfig]]] = None,
    function: Optional[Callable] = None,
) -> Any:
    """
    Run an experiment with the specified parameters.

    There are two ways to run an experiment:
    1. Using a prompt template, prompt settings, and a dataset
    2. Using a runner function and a dataset

    When using a runner function, you can also pass a list of dictionaries to the function to act as a dataset.

    Args:
        experiment_name: Name of the experiment
        prompt_template: Template for prompts
        prompt_settings: Settings for prompt runs
        project: Project name
        dataset: Dataset object, list of records, or dataset name
        dataset_id: ID of the dataset
        dataset_name: Name of the dataset
        metrics: List of metrics to evaluate
        function: Optional function to run with the experiment

    Returns:
        Experiment run results

    Raises:
        ValueError: If required parameters are missing or invalid
    """
    # Get project
    if project is None:
        raise ValueError("A project name must be provided")

    # Load dataset and records
    dataset_obj, records = _load_dataset_and_records(dataset, dataset_id, dataset_name)

    # Validate experiment configuration
    if prompt_template and not dataset_obj:
        raise ValueError("A dataset record, id, or name of a dataset must be provided when a prompt_template is used")

    if function and not records:
        raise ValueError(
            "A dataset record, id or name of a dataset, or list of records must be provided when a function is used"
        )

    if function and prompt_template:
        raise ValueError("A function or prompt_template should be provided, but not both")

    # Get project
    project_obj = Projects().get(name=project)
    if not project_obj:
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

    experiment_obj = Experiments().create(project_obj.id, experiment_name)

    # Set up metrics if provided
    scorer_settings: Optional[list[ScorerConfig]] = None
    local_scorers: list[LocalScorerConfig] = list()
    if metrics is not None:
        scorer_settings, local_scorers = Experiments.create_scorer_configs(project_obj.id, experiment_obj.id, metrics)

    # Execute a runner function experiment
    if function is not None:
        return Experiments().run_with_function(project_obj, experiment_obj, records, function, local_scorers)

    if prompt_template is None:
        raise ValueError("A prompt template must be provided")

    if dataset_obj is None:
        raise ValueError("A dataset object must be provided")

    if local_scorers:
        raise ValueError("Local metrics can only be used with a locally run experiment, not a prompt experiment.")

    # Execute a prompt template experiment
    return Experiments().run(
        project_obj, experiment_obj, prompt_template, dataset_obj.dataset.id, scorer_settings, prompt_settings
    )


def _load_dataset_and_records(
    dataset: Union[Dataset, list[dict[str, str]], str, None], dataset_id: Optional[str], dataset_name: Optional[str]
) -> tuple[Optional[Dataset], list[dict[str, str]]]:
    """
    Load dataset and records based on provided parameters.

    Args:
        dataset: Dataset object, list of records, or dataset name
        dataset_id: ID of the dataset
        dataset_name: Name of the dataset

    Returns:
        Tuple containing (Dataset object or None, records list)

    Raises:
        ValueError: If no dataset information is provided or dataset doesn't exist
    """
    # Case 1: dataset_id provided
    if dataset_id is not None:
        return _get_dataset_and_records_by_id(dataset_id)

    # Case 2: dataset_name provided
    if dataset_name is not None:
        return _get_dataset_and_records_by_name(dataset_name)

    # Case 3: dataset object provided
    if dataset is not None:
        if isinstance(dataset, str):
            # Dataset name provided
            return _get_dataset_and_records_by_name(dataset)
        elif isinstance(dataset, Dataset):
            dataset_content = dataset.get_content()
            return dataset, convert_dataset_content_to_records(dataset_content)
        else:
            # Direct records list
            return None, dataset

    # No dataset provided
    raise ValueError("One of dataset, dataset_name, or dataset_id must be provided")


def _get_dataset_and_records_by_id(dataset_id: str) -> tuple[Dataset, list[dict[str, str]]]:
    """Get dataset by ID and convert to records."""
    dataset = get_dataset(id=dataset_id)
    if not dataset:
        raise ValueError(f"Dataset with id {dataset_id} does not exist")
    dataset_content = dataset.get_content()
    records = convert_dataset_content_to_records(dataset_content)
    return dataset, records


def _get_dataset_and_records_by_name(dataset_name: str) -> tuple[Dataset, list[dict[str, str]]]:
    """Get dataset by name and convert to records."""
    dataset = get_dataset(name=dataset_name)
    if not dataset:
        raise ValueError(f"Dataset with name {dataset_name} does not exist")
    dataset_content = dataset.get_content()
    records = convert_dataset_content_to_records(dataset_content)
    return dataset, records


def create_experiment(
    project_id: str, experiment_name: str
) -> Optional[Union[ExperimentResponse, HTTPValidationError]]:
    return Experiments().create(project_id, experiment_name)


def get_experiment(project_id: str, experiment_name: str) -> Optional[Union[ExperimentResponse, HTTPValidationError]]:
    return Experiments().get(project_id, experiment_name)


def get_experiments(project_id: str) -> Optional[Union[HTTPValidationError, list[ExperimentResponse]]]:
    return Experiments().list(project_id=project_id)
