from datetime import datetime
from unittest import mock
from unittest.mock import Mock, patch, MagicMock
from uuid import UUID

import pytest
from pydantic import UUID4

import galileo
from galileo.projects import Project
from galileo.resources.models import ExperimentResponse, ProjectType, ProjectCreateResponse
from galileo.experiments import Experiments, run_experiment
from tests.testutils.setup import setup_mock_core_api_client, setup_mock_projects_client, setup_mock_logstreams_client


def project():
    now = datetime.now()
    return Project(
        ProjectCreateResponse(created_at=now,
        id=str(UUID(int=0)),
        updated_at=now,
        name = "awesome-new-project",
        type_=ProjectType.GEN_AI,
    ))


class TestExperiments:
    @pytest.fixture
    @patch.object(galileo.experiments.Projects, "get")
    def mock_dependency(self, mock_projects_get: Mock, project: Project):
        mock_projects_get.return_value = project

    @patch("galileo.experiments.create_experiment_v2_projects_project_id_experiments_post")
    def test_create(self, galileo_resources_api_create_experiment: Mock):

        now = datetime(2020, 1, 1).strftime("%Y-%m-%dT%H:%M:%S.%fZ")
        galileo_resources_api_create_experiment.sync = Mock(
            return_value=ExperimentResponse.from_dict(
                dict(id="test", name="test_experiment", project_id="test", created_at=now, updated_at=now)
            )
        )
        experiment = Experiments().create(project_id="test", name="test_experiment")
        assert experiment.name == "test_experiment"
        assert experiment.project_id == "test"


    @patch.object(galileo.experiments.Projects, "get", return_value=project())
    @patch.object(galileo.experiments.Experiments, "get", return_value=experiment())
    def test_run_experiment_with_function(self, mock_get_project: Mock):
        dataset = [
            {"name": "Lola"},
            {"name": "Jo"},
        ]
        experiment = run_experiment(
            "test_experiment",
            project="awesome-new-project",
            dataset=dataset,
            function=lambda *args, **kwargs: "content",
            metrics=["output_tone"]
        )
        assert experiment.name == "test_experiment"