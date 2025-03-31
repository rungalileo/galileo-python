from datetime import datetime
from unittest.mock import ANY, MagicMock, Mock, patch
from uuid import UUID

import pytest
from freezegun import freeze_time

import galileo
import galileo.experiments
from galileo import galileo_context
from galileo.experiments import (
    Experiments,
    _get_dataset_and_records_by_id,
    _get_dataset_and_records_by_name,
    _load_dataset_and_records,
    create_experiment,
    get_experiment,
    get_experiments,
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
    PromptRunSettings,
    ScorerConfig,
    ScorerResponse,
    TaskType,
)
from tests.testutils.setup import setup_mock_core_api_client, setup_mock_logstreams_client, setup_mock_projects_client


@pytest.fixture
def reset_context():
    galileo_context.reset()


def project():
    now = datetime.now()
    return Project(
        ProjectCreateResponse(
            created_at=now, id=str(UUID(int=0)), updated_at=now, name="awesome-new-project", type_=ProjectType.GEN_AI
        )
    )


def experiment_response():
    return ExperimentResponse(
        id=str(UUID(int=1, version=4)),
        name="awesome-new-experiment",
        project_id=str(UUID(int=0, version=4)),
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


def local_dataset():
    return [
        {"input": "Which continent is Spain in?", "expected": "Europe"},
        {"input": "Which continent is Japan in?", "expected": "Asia"},
    ]


def scorers():
    return [
        ScorerResponse.from_dict(
            {
                "id": "aed89cbc-5515-43c3-87ae-39c3c44c043e",
                "name": "correctness",
                "scorer_type": "preset",
                "tags": ["preset", "factuality", "output quality"],
                "created_at": "2025-03-11T00:00:28.497645+00:00",
                "created_by": "7c785f66-89c8-4966-8339-6a4dd910d4a5",
                "defaults": {"filters": None, "model_name": "GPT-4o mini", "num_judges": 7},
                "description": "Measures the potential presence of factual errors or inconsistencies in the model's response.",
                "included_fields": ["model_name", "num_judges", "filters"],
                "latest_version": None,
                "updated_at": "2025-03-19T14:00:55.759587+00:00",
            }
        )
    ]


def promt_run_settings():
    return PromptRunSettings(
        n=1,
        echo=True,
        top_k=10,
        top_p=1.0,
        logprobs=True,
        max_tokens=128,
        model_alias="GPT-4o",
        temperature=0.8,
        top_logprobs=10,
        presence_penalty=0.0,
        frequency_penalty=0.0,
    )


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

    @patch("galileo.experiments.list_experiments_v2_projects_project_id_experiments_get")
    def test_get_experiment(self, list_experiments_mock: Mock):
        list_experiments_mock.sync = Mock(return_value=[experiment_response()])
        experiment = get_experiment(project_id=str(UUID(int=0)), experiment_name=experiment_response().name)
        assert experiment.name == experiment_response().name
        list_experiments_mock.sync.assert_called_once_with(project_id=str(UUID(int=0)), client=ANY)

    @patch("galileo.experiments.list_experiments_v2_projects_project_id_experiments_get")
    def test_get_experiments(self, list_experiments_mock: Mock):
        list_experiments_mock.sync = Mock(return_value=[experiment_response()])
        experiments = get_experiments(project_id=str(UUID(int=0)))
        assert len(experiments) == 1
        assert experiments[0].name == experiment_response().name
        list_experiments_mock.sync.assert_called_once_with(project_id=str(UUID(int=0)), client=ANY)

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

    def test_load_dataset_and_records_error(self):
        with pytest.raises(ValueError) as exc_info:
            _load_dataset_and_records(dataset=None, dataset_name=None, dataset_id=None)
        assert str(exc_info.value) == "One of dataset, dataset_name, or dataset_id must be provided"

    @freeze_time("2012-01-01")
    @patch.object(galileo.datasets.Datasets, "get")
    @patch.object(galileo.jobs.Jobs, "create")
    @patch.object(galileo.experiments.Experiments, "create", return_value=experiment_response())
    @patch.object(galileo.experiments.Experiments, "get", return_value=experiment_response())
    @patch.object(galileo.experiments.Projects, "get", return_value=project())
    def test_run_experiment_without_metrics(
        self,
        mock_get_project: Mock,
        mock_get_experiment: Mock,
        mock_create_experiment: Mock,
        mock_create_job: Mock,
        mock_get_dataset: Mock,
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
        mock_create_experiment.assert_called_once_with(
            project().id, "awesome-new-experiment 2012-01-01 at 00:00:00.000"
        )
        mock_get_dataset.assert_called_once_with(id="00000000-0000-0000-0000-000000000000", name=None)
        mock_get_dataset_instance.get_content.assert_called()
        mock_create_job.assert_called_once_with(
            name="playground_run",
            project_id="00000000-0000-0000-0000-000000000000",
            run_id="00000000-0000-4000-8000-000000000001",
            prompt_template_id="00000000-0000-0000-0000-000000000003",
            dataset_id=ANY,
            task_type=TaskType.VALUE_16,
            scorers=None,
            prompt_settings=ANY,
        )

    @patch("galileo.logger.LogStreams")
    @patch("galileo.logger.Projects")
    @patch("galileo.logger.GalileoCoreApiClient")
    @patch.object(galileo.datasets.Datasets, "get")
    @patch.object(galileo.experiments.Experiments, "create", return_value=experiment_response())
    @patch.object(galileo.experiments.Experiments, "get", return_value=experiment_response())
    @patch.object(galileo.experiments.Projects, "get", return_value=project())
    def test_run_experiment_with_func(
        self,
        mock_get_project: Mock,
        mock_get_experiment: Mock,
        mock_create_experiment: Mock,
        mock_get_dataset: Mock,
        mock_core_api_client: Mock,
        mock_projects_client: Mock,
        mock_logstreams_client: Mock,
        reset_context,
    ):
        mock_core_api_instance = setup_mock_core_api_client(mock_core_api_client)
        setup_mock_projects_client(mock_projects_client)
        setup_mock_logstreams_client(mock_logstreams_client)

        # mock dataset.get_content
        mock_get_dataset_instance = mock_get_dataset.return_value
        mock_get_dataset_instance.get_content = MagicMock(return_value=dataset_content())

        dataset_id = str(UUID(int=0, version=4))

        def function(*args, **kwargs):
            return "dummy_function"

        run_experiment("test_experiment", project="awesome-new-project", dataset_id=dataset_id, function=function)

        mock_get_project.assert_called_with(name="awesome-new-project")
        mock_get_experiment.assert_called_once_with("00000000-0000-0000-0000-000000000000", "test_experiment")
        mock_create_experiment.assert_called_once_with("00000000-0000-0000-0000-000000000000", ANY)

        mock_get_dataset.assert_called_once_with(id="00000000-0000-4000-8000-000000000000", name=None)
        mock_get_dataset_instance.get_content.assert_called()

        # check galileo_logger
        payload = mock_core_api_instance.ingest_traces_sync.call_args[0][0]
        assert len(payload.traces) == 1
        assert len(payload.traces[0].spans) == 1

    @freeze_time("2012-01-01")
    @patch.object(galileo.experiments.ScorerSettings, "create")
    @patch.object(galileo.experiments.Scorers, "list", return_value=scorers())
    @patch.object(galileo.datasets.Datasets, "get")
    @patch.object(galileo.jobs.Jobs, "create")
    @patch.object(galileo.experiments.Experiments, "create", return_value=experiment_response())
    @patch.object(galileo.experiments.Experiments, "get", return_value=experiment_response())
    @patch.object(galileo.experiments.Projects, "get", return_value=project())
    def test_run_experiment_w_prompt_template_and_metrics(
        self,
        mock_get_project: Mock,
        mock_get_experiment: Mock,
        mock_create_experiment: Mock,
        mock_create_job: Mock,
        mock_get_dataset: Mock,
        mock_scorers_list: Mock,
        mock_scorersettings_create: Mock,
    ):
        mock_create_job.return_value = MagicMock()

        # mock dataset.get_content
        mock_get_dataset_instance = mock_get_dataset.return_value
        mock_get_dataset_instance.get_content = MagicMock(return_value=dataset_content())

        dataset_id = str(UUID(int=0))
        run_experiment(
            "test_experiment",
            project="awesome-new-project",
            dataset_id=dataset_id,
            prompt_template=prompt_template(),
            metrics=["correctness"],
        )

        mock_get_project.assert_called_once_with(name="awesome-new-project")
        mock_get_experiment.assert_called_once_with(project().id, "test_experiment")
        mock_create_experiment.assert_called_once_with(
            project().id, "awesome-new-experiment 2012-01-01 at 00:00:00.000"
        )
        mock_get_dataset.assert_called_once_with(id="00000000-0000-0000-0000-000000000000", name=None)
        mock_get_dataset_instance.get_content.assert_called()
        mock_scorers_list.assert_called_with()
        mock_scorersettings_create.assert_called_with(
            project_id="00000000-0000-0000-0000-000000000000",
            run_id="00000000-0000-4000-8000-000000000001",
            scorers=[ScorerConfig.from_dict(scorers()[0].to_dict())],
        )

    @freeze_time("2012-01-01")
    @patch.object(galileo.datasets.Datasets, "get")
    @patch.object(galileo.jobs.Jobs, "create")
    @patch.object(galileo.experiments.Experiments, "create", return_value=experiment_response())
    @patch.object(galileo.experiments.Experiments, "get", return_value=experiment_response())
    @patch.object(galileo.experiments.Projects, "get", return_value=project())
    def test_run_experiment_w_prompt_template_and_prompt_settings(
        self,
        mock_get_project: Mock,
        mock_get_experiment: Mock,
        mock_create_experiment: Mock,
        mock_create_job: Mock,
        mock_get_dataset: Mock,
    ):
        mock_create_job.return_value = MagicMock()

        # mock dataset.get_content
        mock_get_dataset_instance = mock_get_dataset.return_value
        mock_get_dataset_instance.get_content = MagicMock(return_value=dataset_content())

        dataset_id = str(UUID(int=0))
        run_experiment(
            "test_experiment",
            project="awesome-new-project",
            dataset_id=dataset_id,
            prompt_template=prompt_template(),
            prompt_settings=promt_run_settings(),
        )

        mock_get_project.assert_called_once_with(name="awesome-new-project")
        mock_get_experiment.assert_called_once_with(project().id, "test_experiment")
        mock_create_experiment.assert_called_once_with(
            project().id, "awesome-new-experiment 2012-01-01 at 00:00:00.000"
        )

        mock_get_dataset.assert_called_once_with(id="00000000-0000-0000-0000-000000000000", name=None)
        mock_get_dataset_instance.get_content.assert_called()
        mock_create_job.assert_called_once_with(
            name="playground_run",
            project_id="00000000-0000-0000-0000-000000000000",
            run_id="00000000-0000-4000-8000-000000000001",
            prompt_template_id="00000000-0000-0000-0000-000000000003",
            dataset_id=ANY,
            task_type=TaskType.VALUE_16,
            scorers=None,
            prompt_settings=promt_run_settings(),
        )

    @patch.object(galileo.datasets.Datasets, "get")
    def test_run_experiment_with_prompt_template_and_function(self, mock_get_dataset: Mock):
        # mock dataset.get_content
        mock_get_dataset_instance = mock_get_dataset.return_value
        mock_get_dataset_instance.get_content = MagicMock(return_value=dataset_content())

        with pytest.raises(ValueError) as exc_info:
            run_experiment(
                "test_experiment",
                project="awesome-new-project",
                dataset_id=str(UUID(int=1)),
                function=lambda x: x,
                prompt_template=prompt_template(),
            )
        assert str(exc_info.value) == "A function or prompt_template should be provided, but not both"

        mock_get_dataset.assert_called_once_with(id="00000000-0000-0000-0000-000000000001", name=None)
        mock_get_dataset_instance.get_content.assert_called()

    def test_run_experiment_with_prompt_template_and_local_dataset(self):
        with pytest.raises(ValueError) as exc_info:
            run_experiment(
                "test_experiment",
                project="awesome-new-project",
                dataset=local_dataset(),
                prompt_template=prompt_template(),
            )
        assert (
            str(exc_info.value)
            == "A dataset record, id, or name of a dataset must be provided when a prompt_template is used"
        )
