import builtins
import logging
from typing import Any, Callable, Optional, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from galileo import galileo_context, log
from galileo.base import BaseClientModel
from galileo.datasets import Dataset, convert_dataset_content_to_records, get_dataset
from galileo.jobs import Jobs
from galileo.projects import Project, Projects
from galileo.prompts import PromptTemplate, PromptTemplates
from galileo.resources.api.experiment import (
    create_experiment_v2_projects_project_id_experiments_post,
    list_experiments_v2_projects_project_id_experiments_get,
)
from galileo.resources.models import ExperimentResponse, HTTPValidationError, PromptRunSettings, ScorerConfig, TaskType
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
    def create(self, project_id: str, name: str):
        body = ExperimentCreateRequest(name=name, task_type=EXPERIMENT_TASK_TYPE)

        experiment = create_experiment_v2_projects_project_id_experiments_post.sync(
            project_id=project_id, client=self.client, body=body
        )

        return experiment

    def get(self, project_id: str, experiment_name: str) -> Optional[Union[ExperimentResponse, HTTPValidationError]]:
        experiments = self.list(project_id=project_id)

        for experiment in experiments:
            if experiment.name == experiment_name:
                return experiment

        return None

    def get_or_create(self, project_id: str, experiment_name: str):
        experiment = self.get(project_id, experiment_name)
        if not experiment:
            experiment = self.create(project_id, experiment_name)

        return experiment

    def list(self, project_id: str):
        return list_experiments_v2_projects_project_id_experiments_get.sync(project_id=project_id, client=self.client)

    @staticmethod
    def create_run_scorer_settings(
        project_id: str, experiment_id: str, metrics: builtins.list[str]
    ) -> builtins.list[ScorerConfig]:
        scorers = []
        all_scorers = Scorers().list()
        for metric in metrics:
            for scorer in all_scorers:
                if metric == scorer.name:
                    scorers.append(ScorerConfig.from_dict(scorer.to_dict()))
                    break

        ScorerSettings().create(project_id=project_id, run_id=experiment_id, scorers=scorers)
        return scorers

    def run(
        self,
        project_obj: Project,
        experiment_obj: ExperimentResponse,
        prompt: Any,
        dataset_id: str,
        scorers: builtins.list[ScorerConfig],
        prompt_settings: Optional[PromptRunSettings] = None,
    ):
        prompt_template = PromptTemplates().get(project_name=project_obj.name, template_id=prompt.id)

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

        print(
            f"Experiment {experiment_obj.name} has started and is currently processing. Results will be available at {self.client.get_console_url()}/project/{project_obj.id}/experiments/{experiment_obj.id}"
        )
        return job

    def run_with_function(
        self,
        project_obj: Project,
        experiment_obj: ExperimentResponse,
        records: builtins.list[dict[str, str]],
        func: Callable,
    ):
        results = []
        galileo_context.init(project=project_obj.name, experiment_id=experiment_obj.id)

        logged_process_func = log(name=experiment_obj.name)(func)

        #  process each row in the dataset
        for row in records:
            results.append(process_row(row, logged_process_func))
            galileo_context.reset_trace_context()

        # flush the logger
        galileo_context.flush()

        _logger.info(f" {len(results)} rows processed for experiment {experiment_obj.name}.")

        print(
            f"Experiment {experiment_obj.name} has completed and results are available at {self.client.get_console_url()}/project/{project_obj.id}/experiments/{experiment_obj.id}"
        )

        return results


def process_row(row, process_func: Callable):
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
    prompt_template: Any = None,
    prompt_settings: Optional[PromptRunSettings] = None,
    project: str = None,
    dataset: Union[Dataset, list[dict[str, str]], str] = None,
    dataset_id: Optional[str] = None,
    metrics: list[str],
    function: Union[Callable, None] = None,
):
    project_obj = Projects().get(name=project)
    if not project_obj:
        raise ValueError(f"Project {project} does not exist")

    experiment_obj = Experiments().get_or_create(project_obj.id, experiment_name)

    if metrics is not None:
        scorer_settings = Experiments.create_run_scorer_settings(project_obj.id, experiment_obj.id, metrics)

    if dataset_id is None:
        dataset_ = get_dataset(id=dataset_id)
        dataset_content = dataset_.get_content()
        records = convert_dataset_content_to_records(dataset_content)
    else:
        if isinstance(dataset, str):
            dataset_ = get_dataset(name=dataset)
            dataset_content = dataset_.get_content()
            records = convert_dataset_content_to_records(dataset_content)
        elif isinstance(dataset, Dataset):
            dataset_ = dataset
            dataset_content = dataset.get_content()
            records = convert_dataset_content_to_records(dataset_content)
        elif isinstance(dataset, list):
            records = dataset
        else:
            raise ValueError("One of dataset, dataset_name, or dataset_id must be provided")

    if function is not None:
        return Experiments().run_with_function(project_obj, experiment_obj, records, function)
    return Experiments().run(
        project_obj, experiment_obj, prompt_template, dataset_.dataset.id, scorer_settings, prompt_settings
    )


def create_experiment(project_id: str, experiment_name: str):
    return Experiments().create(project_id, experiment_name)


def get_experiment(project_id, experiment_name):
    return Experiments().get(project_id, experiment_name)


def get_experiments(project_id: str):
    return Experiments().list(project_id=project_id)
