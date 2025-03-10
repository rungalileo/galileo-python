import builtins
import logging
from typing import Any, Optional, Union

from galileo.base import BaseClientModel
from galileo.datasets import Dataset
from galileo.jobs import Job
from galileo.projects import Projects
from galileo.prompts import PromptTemplate
from galileo.resources.api.experiment import (
    create_experiment_v2_projects_project_id_experiments_post,
    list_experiments_v2_projects_project_id_experiments_get,
)
from galileo.resources.models import (
    CorrectnessScorer,
    ExperimentCreateRequest,
    ExperimentResponse,
    HTTPValidationError,
    ScorerConfig,
    TaskType,
)
from galileo.scorers import Scorer, ScorerSettings

_logger = logging.getLogger(__name__)

EXPERIMENT_TASK_TYPE = TaskType.VALUE_9

# Order of operations:

# Create a new experiment (using the name) if it doesn't already exist
# Get the ScorerConfig objects for the specified metrics
# Get the project id from the name

# Optionally get the dataset id from the name (if name is used)
# Call the /galileo/job endpoint
# Job name = "prompt_run"
# dataset_id
# project_id
# Prompt settings
# prompt_template_version_id
# run_id = experiment_id
# task_type = TaskType.experiment (16)
# Scorers = List[ScorerConfig]
# For #5, you can analyze the call to the /galileo/job endpoint in the Playground feature in the UI, and also look at api/routers/content/jobs.py:create_job()


SCORERS = {"correctness": CorrectnessScorer}


class Experiment(BaseClientModel):
    def create(self, project_id: str, name: str):
        body = ExperimentCreateRequest(name=name)

        experiment = create_experiment_v2_projects_project_id_experiments_post.sync(
            project_id=project_id, client=self.client, body=body
        )

        return experiment

    def get(self, project_id: str, experiment_name: str) -> Optional[Union[ExperimentResponse, HTTPValidationError]]:
        experiments = self.list(project_id=project_id)

        for experiment in experiments:
            if experiment.name == experiment_name:
                return experiment

        # experiment = get_experiment_v2_projects_project_id_experiments_experiment_id_get.sync(
        #     project_id, experiment_id, client=self.client
        # )
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
            name="prompt_run",  # TODO
            project_id=project.id,
            run_id=experiment.id,
            prompt_template_id=prompt_template.selected_version_id,
            dataset_id=dataset.id,
            task_type=EXPERIMENT_TASK_TYPE,
            scorers=scorers,
        )

        _logger.debug(f"job: {job}")

        print(f"open {self.client.get_console_url()}project/{project.id}/experiments/{experiment.id}")
        return job


# datasetName | datasetId | dataset,
# prompt_settings (PromptRunSettings | None),
def run_experiment(experiment_name: str, *, prompt: Any, project: str, dataset: list[str], metrics: list[str]):
    return Experiment().run(experiment_name, project, prompt, dataset, metrics)
