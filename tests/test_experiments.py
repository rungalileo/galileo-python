from datetime import datetime
from unittest.mock import ANY, MagicMock, Mock, patch
from uuid import UUID

import pytest

import galileo
from galileo.experiments import (
    Experiments,
    _get_dataset_and_records_by_id,
    _get_dataset_and_records_by_name,
    _load_dataset_and_records,
    create_experiment,
    run_experiment,
)
from galileo.projects import Project
from galileo.prompts import PromptTemplate
from galileo.resources.models import (
    BasePromptTemplateResponse,
    DatasetContent,
    DatasetRow,
    ExperimentResponse,
    ProjectCreateResponse,
    ProjectType,
    TaskType,
)


def project():
    now = datetime.now()
    return Project(
        ProjectCreateResponse(
            created_at=now, id=str(UUID(int=0)), updated_at=now, name="awesome-new-project", type_=ProjectType.GEN_AI
        )
    )


def experiment():
    return ExperimentResponse(
        id=str(UUID(int=1)),
        name="awesome-new-experiment",
        project_id=str(UUID(int=0)),
        updated_at=datetime.now(),
        created_at=datetime.now(),
    )


def prompt_template():
    return PromptTemplate(
        prompt_template=BasePromptTemplateResponse(
            id=str(UUID(int=0)),
            name="awesome-new-prompt",
            selected_version="",
            total_versions=1,
            selected_version_id=str(UUID(int=3)),
            all_versions=[str(UUID(int=3))],
            max_version="test",
            template="test",
            all_available_versions=[str(UUID(int=3))],
        )
    )


def dataset_content():
    row = DatasetRow(index=0, values=["Which continent is Spain in?", "Europe"])
    row.additional_properties = {"values_dict": {"input": "Which continent is Spain in?", "expected": "Europe"}}

    column_names = ["input", "expected"]
    return DatasetContent(column_names=column_names, rows=[row])


class TestExperiments:
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
        galileo_resources_api_create_experiment.sync.assert_called_once_with(project_id="test", client=ANY, body=ANY)

    @patch("galileo.experiments.create_experiment_v2_projects_project_id_experiments_post")
    def test_create_experiment(self, galileo_resources_api_create_experiment: Mock):
        now = datetime(2020, 1, 1).strftime("%Y-%m-%dT%H:%M:%S.%fZ")
        galileo_resources_api_create_experiment.sync = Mock(
            return_value=ExperimentResponse.from_dict(
                dict(id="test", name="test_experiment", project_id="test", created_at=now, updated_at=now)
            )
        )

        experiment = create_experiment(project_id=str(UUID(int=0)), experiment_name="test_experiment")
        assert experiment.name == "test_experiment"
        galileo_resources_api_create_experiment.sync.assert_called_once_with(
            project_id=str(UUID(int=0)), client=ANY, body=ANY
        )

    def test_get_experiment(self):
        pass

    def test_get_experiments(self):
        pass

    @patch.object(galileo.datasets.Datasets, "get")
    def test_get_dataset_and_records_by_id(self, mock_get_dataset):
        mock_get_dataset_instance = mock_get_dataset.return_value
        mock_get_dataset_instance.get_content = MagicMock(return_value=dataset_content())
        dataset_id = str(UUID(int=0))

        _, records = _get_dataset_and_records_by_id(dataset_id=dataset_id)

        assert records == [{"expected": "Europe", "input": "Which continent is Spain in?"}]

        mock_get_dataset.assert_called_once_with(id="00000000-0000-0000-0000-000000000000", name=None)
        mock_get_dataset_instance.get_content.assert_called()

    @patch.object(galileo.datasets.Datasets, "get")
    def test_get_dataset_and_records_by_id_error(self, mock_get_dataset):
        mock_get_dataset.return_value = None
        dataset_id = str(UUID(int=0))
        with pytest.raises(ValueError) as exc_info:
            _get_dataset_and_records_by_id(dataset_id=dataset_id)
        mock_get_dataset.assert_called_once_with(id="00000000-0000-0000-0000-000000000000", name=None)
        assert str(exc_info.value) == "Dataset with id 00000000-0000-0000-0000-000000000000 does not exist"

    @patch.object(galileo.datasets.Datasets, "get")
    def test_get_dataset_and_records_by_name(self, mock_get_dataset):
        mock_get_dataset_instance = mock_get_dataset.return_value
        mock_get_dataset_instance.get_content = MagicMock(return_value=dataset_content())

        _, records = _get_dataset_and_records_by_name(dataset_name="awesome-dataset")

        assert records == [{"expected": "Europe", "input": "Which continent is Spain in?"}]

        mock_get_dataset.assert_called_once_with(id=None, name="awesome-dataset")
        mock_get_dataset_instance.get_content.assert_called()

    @patch.object(galileo.datasets.Datasets, "get")
    def test_get_dataset_and_records_by_name_error(self, mock_get_dataset):
        mock_get_dataset.return_value = None

        with pytest.raises(ValueError) as exc_info:
            _get_dataset_and_records_by_name(dataset_name="awesome-dataset")
        mock_get_dataset.assert_called_once_with(id=None, name="awesome-dataset")
        assert str(exc_info.value) == "Dataset with name awesome-dataset does not exist"

    @pytest.mark.parametrize(
        "dataset,dataset_name,dataset_id",
        [("awesome-dataset", None, None), (None, "awesome-dataset", None), (None, None, "dataset_id")],
    )
    @patch.object(galileo.datasets.Datasets, "get")
    def test_load_dataset_and_records(self, mock_get_dataset, dataset, dataset_name, dataset_id):
        mock_get_dataset_instance = mock_get_dataset.return_value
        mock_get_dataset_instance.get_content = MagicMock(return_value=dataset_content())
        _, records = _load_dataset_and_records(dataset=dataset, dataset_name=dataset_name, dataset_id=dataset_id)
        assert records == [{"expected": "Europe", "input": "Which continent is Spain in?"}]
        mock_get_dataset.assert_called_once_with(id=dataset_id, name=dataset_name or dataset)

    @patch.object(galileo.datasets.Datasets, "get")
    def test_load_dataset_and_records_error(self, mock_get_dataset):
        # mock_get_dataset_instance = mock_get_dataset.return_value
        # mock_get_dataset_instance.get_content = MagicMock(return_value=dataset_content())
        with pytest.raises(ValueError) as exc_info:
            _load_dataset_and_records(dataset=None, dataset_name=None, dataset_id=None)
        assert str(exc_info.value) == "One of dataset, dataset_name, or dataset_id must be provided"

    @patch.object(galileo.datasets.Datasets, "get")
    @patch.object(galileo.jobs.Jobs, "create")
    @patch.object(galileo.experiments.Experiments, "get", return_value=experiment())
    @patch.object(galileo.experiments.Projects, "get", return_value=project())
    def test_run_experiment_without_metrics(
        self, mock_get_project: Mock, mock_get_experiment: Mock, mock_create_job: Mock, mock_get_dataset: Mock
    ):
        mock_create_job.return_value = MagicMock()

        # mock dataset.get_content
        mock_get_dataset_instance = mock_get_dataset.return_value
        mock_get_dataset_instance.get_content = MagicMock(return_value=dataset_content())

        dataset_id = str(UUID(int=0))
        run_experiment(
            "test_experiment", project="awesome-new-project", dataset_id=dataset_id, prompt_template=prompt_template()
        )
        mock_get_project.assert_called_once_with(name="awesome-new-project")
        mock_get_experiment.assert_called_once_with(project().id, "test_experiment")
        mock_get_dataset.assert_called_once_with(id="00000000-0000-0000-0000-000000000000", name=None)
        mock_get_dataset_instance.get_content.assert_called()
        mock_create_job.assert_called_once_with(
            name="playground_run",
            project_id="00000000-0000-0000-0000-000000000000",
            run_id="00000000-0000-0000-0000-000000000001",
            prompt_template_id="00000000-0000-0000-0000-000000000003",
            dataset_id=ANY,
            task_type=TaskType.VALUE_16,
            scorers=None,
            prompt_settings=ANY,
        )
