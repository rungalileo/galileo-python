import builtins
import datetime
import logging
from typing import Any, Callable, Optional, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from galileo import galileo_context, log
from galileo.base import BaseClientModel
from galileo.datasets import Dataset
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
from galileo.scorers import Scorers, ScorerSettings
from galileo.utils.datasets import load_dataset_and_records

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
    def create_metric_configs(
        project_id: str,
        experiment_id: str,
        metrics: builtins.list[Union[GalileoScorers, Metric, LocalMetricConfig, str]],
    ) -> tuple[builtins.list[ScorerConfig], builtins.list[LocalMetricConfig]]:
        local_metric_configs: list[LocalMetricConfig] = []
        scorer_name_versions: list[tuple[str, Optional[int]]] = []
        for metric in metrics:
            if isinstance(metric, GalileoScorers):
                scorer_name_versions.append((metric.value, None))
            elif isinstance(metric, Metric):
                scorer_name_versions.append((metric.name, metric.version))
            elif isinstance(metric, LocalMetricConfig):
                local_metric_configs.append(metric)
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
                    unknown_metrics.append(metric)
            if unknown_metrics:
                raise ValueError(
                    "One or more non-existent metrics are specified:"
                    + ", ".join(f"'{metric}'" for metric in unknown_metrics)
                )
            ScorerSettings().create(project_id=project_id, run_id=experiment_id, scorers=scorers)

        return scorers, local_metric_configs

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
        records: builtins.list[DatasetRecord],
        func: Callable,
        local_metrics: builtins.list[LocalMetricConfig],
    ) -> dict[str, Any]:
        results = []
        galileo_context.init(project=project_obj.name, experiment_id=experiment_obj.id, local_metrics=local_metrics)  # type: ignore[arg-type]

        def logged_process_func(row: DatasetRecord) -> Callable:
            return log(name=experiment_obj.name, dataset_record=row)(func)

        #  process each row in the dataset
        for row in records:
            results.append(process_row(row, logged_process_func(row)))
            galileo_context.reset_trace_context()

        # flush the logger
        galileo_context.flush()

        _logger.info(f" {len(results)} rows processed for experiment {experiment_obj.name}.")

        link = f"{self.client.get_console_url()}/project/{project_obj.id}/experiments/{experiment_obj.id}"
        message = f"Experiment {experiment_obj.name} has completed and results are available at {link}"
        print(message)

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
    dataset: Optional[Union[Dataset, list[dict[str, str]], str]] = None,
    dataset_id: Optional[str] = None,
    dataset_name: Optional[str] = None,
    metrics: Optional[list[Union[GalileoScorers, Metric, LocalMetricConfig, str]]] = None,
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
    dataset_obj, records = load_dataset_and_records(dataset, dataset_id, dataset_name)

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
    local_metrics: list[LocalMetricConfig] = list()
    if metrics is not None:
        scorer_settings, local_metrics = Experiments.create_metric_configs(project_obj.id, experiment_obj.id, metrics)

    # Execute a runner function experiment
    if function is not None:
        return Experiments().run_with_function(
            project_obj=project_obj,
            experiment_obj=experiment_obj,
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
    project_id: str, experiment_name: str
) -> Optional[Union[ExperimentResponse, HTTPValidationError]]:
    return Experiments().create(project_id, experiment_name)


def get_experiment(project_id: str, experiment_name: str) -> Optional[Union[ExperimentResponse, HTTPValidationError]]:
    return Experiments().get(project_id, experiment_name)


def get_experiments(project_id: str) -> Optional[Union[HTTPValidationError, list[ExperimentResponse]]]:
    return Experiments().list(project_id=project_id)
