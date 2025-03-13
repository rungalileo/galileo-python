import builtins
import logging
from typing import Any, Callable, Optional, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from galileo import galileo_context, log
from galileo.base import BaseClientModel
from galileo.datasets import Dataset
from galileo.jobs import Job
from galileo.projects import Projects
from galileo.prompts import PromptTemplate
from galileo.resources.api.experiment import (
    create_experiment_v2_projects_project_id_experiments_post,
    list_experiments_v2_projects_project_id_experiments_get,
)
from galileo.resources.models import ExperimentResponse, HTTPValidationError, ScorerConfig, TaskType
from galileo.scorers import Scorer, ScorerSettings

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


class Experiment(BaseClientModel):
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

    def run(
        self,
        experiment_name: str,
        project_name: str,
        prompt: Any,
        dataset: Union[str, Dataset],
        metrics: builtins.list[str],
    ):
        project = Projects().get(name=project_name)
        if not project:
            raise ValueError(f"Project {project_name} does not exist")

        experiment = self.get_or_create(project.id, experiment_name)

        prompt_template = PromptTemplate().get(project_name=project_name, template_id=prompt.id)

        scorers = []
        all_scorers = Scorer().list()
        for metric in metrics:
            for scorer in all_scorers:
                if metric == scorer.name:
                    scorers.append(ScorerConfig.from_dict(scorer.to_dict()))
                    break

        ScorerSettings().create(project_id=project.id, run_id=experiment.id, scorers=scorers)

        job = Job().create(
            name="playground_run",
            project_id=project.id,
            run_id=experiment.id,
            prompt_template_id=prompt_template.selected_version_id,
            dataset_id=dataset.id,
            # 17
            task_type=EXPERIMENT_TASK_TYPE,
            scorers=scorers,
        )

        _logger.debug(f"job: {job}")

        print(f"open {self.client.get_console_url()}/project/{project.id}/experiments/{experiment.id}")
        return job

    def run_with_function(self, experiment_name: str, project_name: str, dataset: Any, func: Callable):
        project = Projects().get(name=project_name)
        if not project:
            raise ValueError(f"Project {project_name} does not exist")

        experiment = self.get_or_create(project.id, experiment_name)
        results = []
        galileo_context.init(project=project_name, experiment_id=experiment.id)

        logged_process_func = log(name=experiment_name)(func)

        #  process each row in the dataset
        for row in dataset:
            results.append(process_row(row, logged_process_func))
            galileo_context.reset_trace_context()

        # flush the logger
        galileo_context.flush()

        _logger.info(f"${len(results)} rows processed for experiment {experiment_name}.")

        return results


def process_row(row, process_func: Callable):
    _logger.info(f"Processing dataset row: {row}")
    # try:
    output = process_func(row)
    # except Exception as exc:
    #     _logger.error(f"error during executing: {process_func.__name__}: {exc}")
    #     output = f"error during executing: {process_func.__name__}: {exc}"

    log = galileo_context.get_logger_instance()
    log.conclude(output)
    return output


def run_experiment(
    experiment_name: str,
    *,
    prompt_template: Any = None,
    project: str = None,
    dataset: list[Any],
    metrics: list[str],
    function: Union[Callable, None] = None,
):
    if function is not None:
        return Experiment().run_with_function(experiment_name, project, dataset, function)
    return Experiment().run(experiment_name, project, prompt_template, dataset, metrics)


def create_experiment(project_id: str, experiment_name: str):
    return Experiment().create(project_id, experiment_name)


def get_experiment(project_id, experiment_name):
    return Experiment().get(project_id, experiment_name)


def get_experiments(project_id: str):
    return Experiment().list(project_id=project_id)
