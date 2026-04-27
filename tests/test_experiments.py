import operator
import os
from collections.abc import Callable
from datetime import datetime
from functools import reduce
from statistics import mean
from unittest.mock import ANY, MagicMock, Mock, patch
from unittest.mock import call as mock_call
from uuid import UUID

import pytest
from time_machine import travel

import galileo.experiments
import galileo.jobs
import galileo.utils.datasets
from galileo import galileo_context
from galileo.decorator import SPAN_TYPE
from galileo.experiments import (
    Experiments,
    create_experiment,
    get_experiment,
    get_experiments,
    list_experiment_groups,
    run_experiment,
)
from galileo.projects import Project
from galileo.prompts import PromptTemplate
from galileo.resources.models import (
    BasePromptTemplateResponse,
    BasePromptTemplateVersionResponse,
    DatasetContent,
    DatasetRow,
    DatasetRowValuesDict,
    ExperimentResponse,
    ProjectCreateResponse,
    ProjectType,
    PromptRunSettings,
    ScorerConfig,
    ScorerResponse,
    ScorerTypes,
    TaskType,
)
from galileo.schema.datasets import DatasetRecord
from galileo.schema.experiment_group import ExperimentGroupResponse
from galileo.schema.metrics import GalileoMetrics, LocalMetricConfig
from galileo.utils.datasets import load_dataset_and_records
from galileo_core.schemas.logging.span import Span, StepWithChildSpans
from galileo_core.schemas.shared.metric import MetricValueType
from tests.testutils.setup import setup_mock_logstreams_client, setup_mock_projects_client, setup_mock_traces_client


@pytest.fixture
def reset_context(auto_use=True) -> None:
    galileo_context.reset()
    os.environ.pop("GALILEO_PROJECT", None)
    os.environ.pop("GALILEO_PROJECT_ID", None)


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
        task_type=TaskType.VALUE_16,
    )


def prompt_template():
    return PromptTemplate(
        prompt_template=BasePromptTemplateResponse(
            all_available_versions=[1, 2, 3],
            created_at=datetime.now(),
            created_by_user="Test User",
            id=str(UUID(int=0)),
            max_version=3,
            name="awesome-new-prompt",
            selected_version=BasePromptTemplateVersionResponse(
                content_changed=False,
                created_at=datetime.now(),
                created_by_user="Test User",
                id=str(UUID(int=3)),
                lines_added=0,
                lines_edited=0,
                lines_removed=0,
                model_changed=False,
                settings={},
                settings_changed=False,
                template="test",
                updated_at=datetime.now(),
                version=1,
            ),
            selected_version_id=str(UUID(int=3)),
            template="test",
            total_versions=3,
            updated_at=datetime.now(),
            all_versions=[str(UUID(int=3))],
        )
    )


def scorers():
    return [
        ScorerResponse.from_dict(
            {
                "id": "aed89cbc-5515-43c3-87ae-39c3c44c043e",
                "name": "correctness",
                "label": "Correctness",
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


def prompt_run_settings():
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


def complex_trace_function(input):
    logger = galileo_context.get_logger_instance()
    output = input + " output"
    logger.add_llm_span(input=input, output=output, model="example")
    return output


def mock_scorer_version_response():
    mock_response = MagicMock()
    mock_response.id = "mock_scorer_version_id"
    mock_response.version = 1
    mock_response.to_dict.return_value = {"id": "mock_scorer_version_id", "version": 1}
    return mock_response


class TestExperiments:
    @patch("galileo.experiments.create_experiment_projects_project_id_experiments_post")
    def test_create(self, galileo_resources_api_create_experiment: Mock) -> None:
        now = datetime(2020, 1, 1).strftime("%Y-%m-%dT%H:%M:%S.%fZ")
        galileo_resources_api_create_experiment.sync = Mock(
            return_value=ExperimentResponse.from_dict(
                {
                    "id": "test",
                    "name": "test_experiment",
                    "project_id": "test",
                    "created_at": now,
                    "updated_at": now,
                    "task_type": TaskType.VALUE_16,
                }
            )
        )
        experiment = Experiments().create(project_id="test", name="test_experiment")
        assert experiment.name == "test_experiment"
        assert experiment.project_id == "test"
        galileo_resources_api_create_experiment.sync.assert_called_once_with(project_id="test", client=ANY, body=ANY)

    @patch("galileo.experiments.create_experiment_projects_project_id_experiments_post")
    def test_create_raises_value_error_with_clear_message_on_invalid_model_alias(
        self, galileo_resources_api_create_experiment: Mock
    ) -> None:
        """Experiments.create() with invalid model_alias (HTTP 422) raises ValueError with human-readable message."""
        # Given: the API returns a 422 HTTPValidationError for an invalid model alias
        from galileo.resources.models import HTTPValidationError, ValidationError

        galileo_resources_api_create_experiment.sync = Mock(
            return_value=HTTPValidationError(
                detail=[
                    ValidationError(
                        loc=["body", "prompt_settings", "model_alias"],
                        msg="Invalid model alias: 'gpt-4o-mini' is not a valid model alias.",
                        type_="value_error",
                    )
                ]
            )
        )

        # When/Then: create() raises ValueError with a clear, readable message
        with pytest.raises(ValueError, match="Request validation failed"):
            Experiments().create(
                project_id="test", name="test_experiment", prompt_settings=PromptRunSettings(model_alias="gpt-4o-mini")
            )

    @patch("galileo.experiments.create_experiment_projects_project_id_experiments_post")
    def test_create_error_message_contains_field_and_msg_on_422(
        self, galileo_resources_api_create_experiment: Mock
    ) -> None:
        """ValueError from Experiments.create() includes field path and backend message."""
        # Given: the API returns a 422 with specific validation detail
        from galileo.resources.models import HTTPValidationError, ValidationError

        galileo_resources_api_create_experiment.sync = Mock(
            return_value=HTTPValidationError(
                detail=[
                    ValidationError(
                        loc=["body", "prompt_settings", "model_alias"],
                        msg="Invalid model alias: 'gpt-4o-mini' is not a valid model alias.",
                        type_="value_error",
                    )
                ]
            )
        )

        # When/Then: the error message includes both the field path and the backend message
        with pytest.raises(ValueError) as exc_info:
            Experiments().create(project_id="test", name="test_experiment")
        msg = str(exc_info.value)
        assert "model_alias" in msg
        assert "gpt-4o-mini" in msg

    @patch("galileo.experiments.create_experiment_projects_project_id_experiments_post")
    def test_create_with_dict_prompt_settings(self, galileo_resources_api_create_experiment: Mock) -> None:
        """Test create() converts dict prompt_settings via PromptRunSettings roundtrip."""
        # Given: a dict prompt_settings and a mocked API response
        now = datetime(2020, 1, 1).strftime("%Y-%m-%dT%H:%M:%S.%fZ")
        galileo_resources_api_create_experiment.sync = Mock(
            return_value=ExperimentResponse.from_dict(
                {
                    "id": "test",
                    "name": "test_experiment",
                    "project_id": "test",
                    "created_at": now,
                    "updated_at": now,
                    "task_type": TaskType.VALUE_16,
                }
            )
        )
        dict_settings = {"model_alias": "GPT-4o", "temperature": 0.8}

        # When: creating an experiment with prompt_settings as a plain dict
        Experiments().create(project_id="test", name="test_experiment", prompt_settings=dict_settings)

        # Then: the dict is roundtripped through PromptRunSettings and the original values are preserved
        galileo_resources_api_create_experiment.sync.assert_called_once_with(project_id="test", client=ANY, body=ANY)
        call_body = galileo_resources_api_create_experiment.sync.call_args.kwargs["body"]
        actual_settings = call_body.additional_properties["prompt_settings"]
        assert actual_settings["model_alias"] == "GPT-4o"
        assert actual_settings["temperature"] == 0.8

    @patch("galileo.experiments.create_experiment_projects_project_id_experiments_post")
    @patch("galileo.experiments.Projects.get_with_env_fallbacks")
    def test_create_experiment_with_project_id(
        self, mock_get_with_env_fallbacks: Mock, galileo_resources_api_create_experiment: Mock
    ) -> None:
        mock_get_with_env_fallbacks.return_value = project()
        now = datetime(2020, 1, 1).strftime("%Y-%m-%dT%H:%M:%S.%fZ")
        galileo_resources_api_create_experiment.sync = Mock(
            return_value=ExperimentResponse.from_dict(
                {
                    "id": "test",
                    "name": "test_experiment",
                    "project_id": "test",
                    "created_at": now,
                    "updated_at": now,
                    "task_type": TaskType.VALUE_16,
                }
            )
        )

        experiment = create_experiment(project_id=str(UUID(int=0)), experiment_name="test_experiment")
        assert experiment.name == "test_experiment"
        galileo_resources_api_create_experiment.sync.assert_called_once_with(
            project_id=str(UUID(int=0)), client=ANY, body=ANY
        )
        mock_get_with_env_fallbacks.assert_called_once_with(id=str(UUID(int=0)), name=None)

    @patch("galileo.experiments.create_experiment_projects_project_id_experiments_post")
    @patch("galileo.experiments.Projects.get_with_env_fallbacks")
    def test_create_experiment_with_project_name(
        self, mock_get_with_env_fallbacks: Mock, galileo_resources_api_create_experiment: Mock
    ) -> None:
        mock_get_with_env_fallbacks.return_value = project()
        now = datetime(2020, 1, 1).strftime("%Y-%m-%dT%H:%M:%S.%fZ")
        galileo_resources_api_create_experiment.sync = Mock(
            return_value=ExperimentResponse.from_dict(
                {
                    "id": "test",
                    "name": "test_experiment",
                    "project_id": "test",
                    "created_at": now,
                    "updated_at": now,
                    "task_type": TaskType.VALUE_16,
                }
            )
        )

        experiment = create_experiment(project_name="test_project", experiment_name="test_experiment")
        assert experiment.name == "test_experiment"
        galileo_resources_api_create_experiment.sync.assert_called_once_with(
            project_id=str(UUID(int=0)), client=ANY, body=ANY
        )
        mock_get_with_env_fallbacks.assert_called_once_with(id=None, name="test_project")

    @patch("galileo.experiments.create_experiment_projects_project_id_experiments_post")
    @patch("galileo.experiments.Projects.get_with_env_fallbacks", return_value=None)
    def test_create_experiment_without_project_fails(
        self, mock_get_with_env_fallbacks: Mock, galileo_resources_api_create_experiment: Mock
    ) -> None:
        now = datetime(2020, 1, 1).strftime("%Y-%m-%dT%H:%M:%S.%fZ")
        galileo_resources_api_create_experiment.sync = Mock(
            return_value=ExperimentResponse.from_dict(
                {
                    "id": "test",
                    "name": "test_experiment",
                    "project_id": "test",
                    "created_at": now,
                    "updated_at": now,
                    "task_type": TaskType.VALUE_16,
                }
            )
        )

        with pytest.raises(ValueError, match="Project not specified and no defaults found"):
            create_experiment(experiment_name="test_experiment")

    @patch("galileo.experiments.create_experiment_projects_project_id_experiments_post")
    @patch("galileo.experiments.Projects.get_with_env_fallbacks")
    def test_create_experiment_with_wrong_project_name_fails(
        self, mock_get_with_env_fallbacks: Mock, galileo_resources_api_create_experiment: Mock
    ) -> None:
        now = datetime(2020, 1, 1).strftime("%Y-%m-%dT%H:%M:%S.%fZ")
        mock_get_with_env_fallbacks.return_value = None
        galileo_resources_api_create_experiment.sync = Mock(
            return_value=ExperimentResponse.from_dict(
                {
                    "id": "test",
                    "name": "test_experiment",
                    "project_id": "test",
                    "created_at": now,
                    "updated_at": now,
                    "task_type": TaskType.VALUE_16,
                }
            )
        )

        with pytest.raises(ValueError, match="Project test_project does not exist"):
            create_experiment(project_name="test_project", experiment_name="test_experiment")

    def test_create_experiment_missing_experiment_name_raises(self) -> None:
        with pytest.raises(ValueError, match="experiment_name is required"):
            create_experiment(project_name="test_project")

    def test_create_experiment_empty_experiment_name_raises(self) -> None:
        with pytest.raises(ValueError, match="experiment_name is required"):
            create_experiment(experiment_name="", project_name="test_project")

    @patch("galileo.experiments.list_experiments_projects_project_id_experiments_get")
    @patch("galileo.experiments.Projects.get_with_env_fallbacks")
    def test_get_experiments_with_project_id(
        self, mock_get_with_env_fallbacks: Mock, list_experiments_mock: Mock
    ) -> None:
        list_experiments_mock.sync = Mock(return_value=[experiment_response()])
        mock_get_with_env_fallbacks.return_value = project()
        experiments = get_experiments(project_id=str(UUID(int=0)))
        assert len(experiments) == 1
        assert experiments[0].name == experiment_response().name
        list_experiments_mock.sync.assert_called_once_with(project_id=str(UUID(int=0)), client=ANY)

    @patch("galileo.experiments.list_experiments_projects_project_id_experiments_get")
    @patch("galileo.experiments.Projects.get_with_env_fallbacks")
    def test_get_experiments_with_project_name(
        self, mock_get_with_env_fallbacks: Mock, list_experiments_mock: Mock
    ) -> None:
        list_experiments_mock.sync = Mock(return_value=[experiment_response()])
        mock_get_with_env_fallbacks.return_value = project()
        experiments = get_experiments(project_name="test_project")
        assert len(experiments) == 1
        assert experiments[0].name == experiment_response().name
        list_experiments_mock.sync.assert_called_once_with(project_id=str(UUID(int=0)), client=ANY)
        mock_get_with_env_fallbacks.assert_called_once_with(id=None, name="test_project")

    @patch("galileo.experiments.list_experiments_projects_project_id_experiments_get")
    @patch("galileo.experiments.Projects.get_with_env_fallbacks")
    def test_get_experiments_without_project_id_or_name_fails(
        self, mock_get_with_env_fallbacks: Mock, list_experiments_mock: Mock
    ) -> None:
        list_experiments_mock.sync = Mock(return_value=[experiment_response()])
        mock_get_with_env_fallbacks.return_value = None

        with pytest.raises(ValueError, match="Project not specified and no defaults found"):
            get_experiments()

    @patch("galileo.experiments.list_experiments_projects_project_id_experiments_get")
    @patch("galileo.experiments.Projects.get_with_env_fallbacks")
    def test_get_experiments_with_wrong_project_name_fails(
        self, mock_get_with_env_fallbacks: Mock, list_experiments_mock: Mock
    ) -> None:
        list_experiments_mock.sync = Mock(return_value=[experiment_response()])
        mock_get_with_env_fallbacks.return_value = None

        with pytest.raises(ValueError, match="Project test_project does not exist"):
            get_experiments(project_name="test_project")

    @patch("galileo.experiments.list_experiments_projects_project_id_experiments_get")
    @patch("galileo.experiments.Projects.get_with_env_fallbacks")
    def test_get_experiment_not_found(self, mock_get_with_env_fallbacks: Mock, list_experiments_mock: Mock) -> None:
        list_experiments_mock.sync = Mock(return_value=None)
        mock_get_with_env_fallbacks.return_value = project()

        experiment = get_experiment(experiment_name=experiment_response().name, project_id=str(UUID(int=0)))
        assert experiment is None
        list_experiments_mock.sync.assert_called_once_with(project_id=str(UUID(int=0)), client=ANY)

    def test_get_experiment_missing_experiment_name_raises(self) -> None:
        with pytest.raises(ValueError, match="experiment_name is required"):
            get_experiment(project_id=str(UUID(int=0)))

    def test_get_experiment_empty_experiment_name_raises(self) -> None:
        with pytest.raises(ValueError, match="experiment_name is required"):
            get_experiment(project_id=str(UUID(int=0)), experiment_name="")

    @patch("galileo.experiments.list_experiments_projects_project_id_experiments_get")
    @patch("galileo.experiments.Projects.get_with_env_fallbacks")
    def test_get_experiment_neither_project_id_nor_name_raises(
        self, mock_get_with_env_fallbacks: Mock, list_experiments_mock: Mock
    ) -> None:
        # Simulate inability to resolve project from env/defaults
        mock_get_with_env_fallbacks.return_value = None
        list_experiments_mock.sync = Mock()

        with pytest.raises(ValueError, match="Project not specified and no defaults found"):
            get_experiment(experiment_name=experiment_response().name)

        list_experiments_mock.sync.assert_not_called()

    @patch("galileo.experiments.list_experiments_projects_project_id_experiments_get")
    @patch("galileo.experiments.Projects.get_with_env_fallbacks")
    def test_get_experiment_with_project_name(
        self, mock_get_with_env_fallbacks: Mock, list_experiments_mock: Mock
    ) -> None:
        mock_get_with_env_fallbacks.return_value = project()
        list_experiments_mock.sync = Mock(return_value=[experiment_response()])

        exp = get_experiment(project_name="awesome-new-project", experiment_name=experiment_response().name)

        assert exp.name == experiment_response().name
        list_experiments_mock.sync.assert_called_once_with(project_id=project().id, client=ANY)
        mock_get_with_env_fallbacks.assert_called_once_with(id=None, name="awesome-new-project")

    @patch("galileo.experiments.list_experiments_projects_project_id_experiments_get")
    @patch("galileo.experiments.Projects.get_with_env_fallbacks")
    def test_get_experiment_with_wrong_project_name_fails(
        self, mock_get_with_env_fallbacks: Mock, list_experiments_mock: Mock
    ) -> None:
        mock_get_with_env_fallbacks.return_value = None
        list_experiments_mock.sync = Mock(return_value=[experiment_response()])

        with pytest.raises(ValueError, match="Project awesome-new-project does not exist"):
            get_experiment(project_name="awesome-new-project", experiment_name=experiment_response().name)

    @patch("galileo.experiments.list_experiments_projects_project_id_experiments_get")
    @patch("galileo.experiments.Projects.get_with_env_fallbacks")
    def test_get_experiment_with_project_id(
        self, mock_get_with_env_fallbacks: Mock, list_experiments_mock: Mock
    ) -> None:
        mock_get_with_env_fallbacks.return_value = project()
        list_experiments_mock.sync = Mock(return_value=[experiment_response()])

        exp = get_experiment(project_id=str(UUID(int=0)), experiment_name=experiment_response().name)

        assert exp.name == experiment_response().name
        list_experiments_mock.sync.assert_called_once_with(project_id=str(UUID(int=0)), client=ANY)
        mock_get_with_env_fallbacks.assert_called_once_with(id=str(UUID(int=0)), name=None)

    @pytest.mark.parametrize(
        ("dataset", "dataset_name", "dataset_id"),
        [("awesome-dataset", None, None), (None, "awesome-dataset", None), (None, None, "dataset_id")],
    )
    @patch.object(galileo.datasets.Datasets, "get")
    def test_load_dataset_and_records(
        self,
        mock_get_dataset,
        dataset,
        dataset_name,
        dataset_id,
        dataset_content: DatasetContent,
        test_dataset_row_id: str,
    ) -> None:
        mock_get_dataset_instance = mock_get_dataset.return_value
        mock_get_dataset_instance.get_content = MagicMock(return_value=dataset_content)
        _, records = load_dataset_and_records(dataset=dataset, dataset_name=dataset_name, dataset_id=dataset_id)
        assert records == [
            DatasetRecord(
                id=test_dataset_row_id, input="Which continent is Spain in?", output="Europe", metadata={"meta": "data"}
            )
        ]
        if dataset_id:
            mock_get_dataset.assert_called_once_with(id=dataset_id, name=None, project_id=None, project_name=None)
        elif dataset_name:
            mock_get_dataset.assert_called_once_with(id=None, name=dataset_name, project_id=None, project_name=None)

    def test_load_dataset_and_records_error(self) -> None:
        with pytest.raises(ValueError) as exc_info:
            load_dataset_and_records(dataset=None, dataset_name=None, dataset_id=None)
        assert str(exc_info.value) == "To load dataset records, dataset, dataset_name, or dataset_id must be provided"

    @patch.object(galileo.datasets.Datasets, "get")
    @patch.object(galileo.jobs.Jobs, "create")
    @patch.object(galileo.experiments.Experiments, "create", return_value=experiment_response())
    @patch.object(galileo.experiments.Experiments, "get", return_value=experiment_response())
    @patch.object(galileo.experiments.Projects, "get_with_env_fallbacks", return_value=project())
    def test_run_experiment_with_project_name_loads_project(
        self,
        mock_get_project: Mock,
        mock_get_experiment: Mock,
        mock_create_job: Mock,
        mock_get_dataset: Mock,
        dataset_content: DatasetContent,
    ) -> None:
        mock_create_job.return_value = MagicMock()

        dataset_id = str(UUID(int=0))
        run_experiment(
            "test_experiment", project="awesome-new-project", dataset_id=dataset_id, prompt_template=prompt_template()
        )

        mock_get_project.assert_called_once_with(id=None, name="awesome-new-project")

    @patch.object(galileo.datasets.Datasets, "get")
    @patch.object(galileo.jobs.Jobs, "create")
    @patch.object(galileo.experiments.Experiments, "create", return_value=experiment_response())
    @patch.object(galileo.experiments.Experiments, "get", return_value=experiment_response())
    @patch.object(galileo.experiments.Projects, "get_with_env_fallbacks", return_value=project())
    def test_run_experiment_with_project_id_loads_project(
        self,
        mock_get_project: Mock,
        mock_get_experiment: Mock,
        mock_create_job: Mock,
        mock_get_dataset: Mock,
        dataset_content: DatasetContent,
    ) -> None:
        mock_create_job.return_value = MagicMock()

        dataset_id = str(UUID(int=0))
        run_experiment(
            "test_experiment",
            project_id="awesome-new-project",
            dataset_id=dataset_id,
            prompt_template=prompt_template(),
        )

        mock_get_project.assert_called_once_with(id="awesome-new-project", name=None)

    @patch.object(galileo.datasets.Datasets, "get")
    @patch.object(galileo.jobs.Jobs, "create")
    @patch.object(galileo.experiments.Experiments, "create", return_value=experiment_response())
    @patch.object(galileo.experiments.Experiments, "get", return_value=experiment_response())
    @patch.object(galileo.experiments.Projects, "get_with_env_fallbacks", return_value=None)
    def test_run_experiment_with_invalid_project_id_gives_error(
        self,
        mock_get_project: Mock,
        mock_get_experiment: Mock,
        mock_create_job: Mock,
        mock_get_dataset: Mock,
        dataset_content: DatasetContent,
    ) -> None:
        mock_create_job.return_value = MagicMock()

        dataset_id = str(UUID(int=0))
        with pytest.raises(ValueError) as exc_info:
            run_experiment(
                "test_experiment",
                project_id="awesome-new-project",
                dataset_id=dataset_id,
                prompt_template=prompt_template(),
            )

        assert str(exc_info.value) == "Project with Id awesome-new-project does not exist"

    @patch.object(galileo.datasets.Datasets, "get")
    @patch.object(galileo.jobs.Jobs, "create")
    @patch.object(galileo.experiments.Experiments, "create", return_value=experiment_response())
    @patch.object(galileo.experiments.Experiments, "get", return_value=experiment_response())
    @patch.object(galileo.experiments.Projects, "get_with_env_fallbacks", return_value=None)
    def test_run_experiment_with_invalid_project_name_gives_error(
        self,
        mock_get_project: Mock,
        mock_get_experiment: Mock,
        mock_create_job: Mock,
        mock_get_dataset: Mock,
        dataset_content: DatasetContent,
    ) -> None:
        mock_create_job.return_value = MagicMock()

        dataset_id = str(UUID(int=0))
        with pytest.raises(ValueError) as exc_info:
            run_experiment(
                "test_experiment",
                project="awesome-new-project",
                dataset_id=dataset_id,
                prompt_template=prompt_template(),
            )

        assert str(exc_info.value) == "Project awesome-new-project does not exist"

    @travel(datetime(2012, 1, 1), tick=False)
    @patch.object(galileo.datasets.Datasets, "get")
    @patch.object(galileo.experiments.Experiments, "create", return_value=experiment_response())
    @patch.object(galileo.experiments.Experiments, "get", return_value=experiment_response())
    @patch.object(galileo.experiments.Projects, "get_with_env_fallbacks", return_value=project())
    def test_run_experiment_without_metrics(
        self,
        mock_get_project: Mock,
        mock_get_experiment: Mock,
        mock_create_experiment: Mock,
        mock_get_dataset: Mock,
        dataset_content: DatasetContent,
    ) -> None:
        dataset_id = str(UUID(int=0))
        result = run_experiment(
            "test_experiment", project="awesome-new-project", dataset_id=dataset_id, prompt_template=prompt_template()
        )
        assert result is not None
        assert result["experiment"] is not None
        assert f"/project/{project().id}/experiments/{experiment_response().id}" in result["link"]
        mock_get_project.assert_called_once_with(id=None, name="awesome-new-project")
        mock_get_experiment.assert_called_once_with(project().id, "test_experiment")
        # Experiments.create is called with trigger=True (single API call)
        mock_create_experiment.assert_called_once_with(
            project_id=project().id,
            name="awesome-new-experiment 2012-01-01 at 00:00:00.000",
            dataset_obj=mock_get_dataset.return_value,
            trigger=True,
            prompt_template=ANY,
            scorers=None,
            prompt_settings=ANY,
        )

    @pytest.mark.parametrize("console_url", ["http://localtest:8088", "http://localtest:8088/"])
    @travel(datetime(2012, 1, 1), tick=False)
    @patch.object(galileo.datasets.Datasets, "get")
    @patch.object(galileo.jobs.Jobs, "create")
    @patch.object(galileo.experiments.Experiments, "create", return_value=experiment_response())
    @patch.object(galileo.experiments.Experiments, "get", return_value=experiment_response())
    @patch.object(galileo.experiments.Projects, "get_with_env_fallbacks", return_value=project())
    def test_run_experiment_link_no_double_slash(
        self,
        mock_get_project: Mock,
        mock_get_experiment: Mock,
        mock_create_experiment: Mock,
        mock_create_job: Mock,
        mock_get_dataset: Mock,
        console_url: str,
        dataset_content: DatasetContent,
    ) -> None:
        # Given: a console_url with or without a trailing slash
        mock_create_job.return_value = MagicMock()
        mock_config = MagicMock()
        mock_config.console_url = console_url

        # When: running an experiment
        with patch("galileo.experiments.GalileoPythonConfig.get", return_value=mock_config):
            result = run_experiment(
                "test_experiment",
                project="awesome-new-project",
                dataset_id=str(UUID(int=0)),
                prompt_template=prompt_template(),
            )

        # Then: the link does not contain double slashes after the protocol
        assert result is not None
        link = result["link"]
        assert "//project" not in link
        assert f"/project/{project().id}/experiments/{experiment_response().id}" in link

    @travel(datetime(2012, 1, 1), tick=False)
    @patch.object(galileo.datasets.Datasets, "get")
    @patch.object(galileo.experiments.Experiments, "create", return_value=experiment_response())
    @patch.object(galileo.experiments.Experiments, "get", return_value=experiment_response())
    @patch.object(galileo.experiments.Projects, "get_with_env_fallbacks", return_value=project())
    def test_run_experiment_generated_output_flow(
        self,
        mock_get_project: Mock,
        mock_get_experiment: Mock,
        mock_create_experiment: Mock,
        mock_get_dataset: Mock,
        dataset_content: DatasetContent,
    ) -> None:
        # Given: no prompt_template, dataset provided (generated-output flow)
        dataset_id = str(UUID(int=0))

        # When: run_experiment is called without a prompt_template
        result = run_experiment("test_experiment", project="awesome-new-project", dataset_id=dataset_id)

        # Then: Experiments.create is called with trigger=True, no prompt_template, no prompt_settings
        assert result is not None
        mock_create_experiment.assert_called_once_with(
            project_id=project().id,
            name="awesome-new-experiment 2012-01-01 at 00:00:00.000",
            dataset_obj=mock_get_dataset.return_value,
            trigger=True,
            prompt_template=None,
            scorers=None,
            prompt_settings=None,
        )

    @travel(datetime(2012, 1, 1), tick=False)
    @patch.object(galileo.datasets.Datasets, "get")
    @patch.object(galileo.experiments.Experiments, "create", return_value=experiment_response())
    @patch.object(galileo.experiments.Experiments, "get", return_value=experiment_response())
    @patch.object(galileo.experiments.Projects, "get_with_env_fallbacks", return_value=project())
    def test_run_experiment_prompt_takes_precedence_over_generated_output(
        self,
        mock_get_project: Mock,
        mock_get_experiment: Mock,
        mock_create_experiment: Mock,
        mock_get_dataset: Mock,
        dataset_content: DatasetContent,
    ) -> None:
        # Given: both prompt_template and dataset provided
        dataset_id = str(UUID(int=0))

        # When: run_experiment is called with a prompt_template
        result = run_experiment(
            "test_experiment", project="awesome-new-project", dataset_id=dataset_id, prompt_template=prompt_template()
        )

        # Then: Experiments.create is called with trigger=True and prompt_template set (prompt-driven flow)
        assert result is not None
        mock_create_experiment.assert_called_once_with(
            project_id=project().id,
            name="awesome-new-experiment 2012-01-01 at 00:00:00.000",
            dataset_obj=mock_get_dataset.return_value,
            trigger=True,
            prompt_template=ANY,
            scorers=None,
            prompt_settings=ANY,
        )

    @patch.object(galileo.datasets.Datasets, "get", return_value=None)
    @patch.object(galileo.jobs.Jobs, "create")
    @patch.object(galileo.experiments.Experiments, "create", return_value=experiment_response())
    @patch.object(galileo.experiments.Experiments, "get", return_value=experiment_response())
    @patch.object(galileo.experiments.Projects, "get_with_env_fallbacks", return_value=project())
    def test_run_experiment_no_prompt_no_dataset_raises(
        self,
        mock_get_project: Mock,
        mock_get_experiment: Mock,
        mock_create_experiment: Mock,
        mock_create_job: Mock,
        mock_get_dataset: Mock,
    ) -> None:
        # Given: no prompt_template and no dataset
        # When/Then: ValueError is raised requiring a dataset
        with pytest.raises(ValueError, match="dataset"):
            run_experiment("test_experiment", project="awesome-new-project")

    @patch("galileo.logger.logger.LogStreams")
    @patch("galileo.logger.logger.Projects")
    @patch("galileo.logger.logger.Traces")
    @patch.object(galileo.datasets.Datasets, "get")
    @patch.object(galileo.experiments.Experiments, "create", return_value=experiment_response())
    @patch.object(galileo.experiments.Experiments, "get", return_value=experiment_response())
    @patch.object(galileo.experiments.Projects, "get_with_env_fallbacks", return_value=project())
    @patch("galileo.utils.metrics.Scorers")
    @patch("galileo.utils.metrics.ScorerSettings")
    @pytest.mark.parametrize("thread_pool", [True, False])
    @pytest.mark.parametrize(
        ("function", "metrics", "num_spans", "span_type", "results", "aggregate_results"),
        [
            (lambda *args, **kwargs: "dummy_function", [], 1, "llm", [], []),
            (
                lambda *args, **kwargs: "dummy_function",
                [
                    LocalMetricConfig[int](
                        name="length",
                        scorer_fn=lambda step: len(step.input),
                        scorable_types=["workflow"],
                        aggregator_fn=lambda lengths: sum(lengths),
                    ),
                    LocalMetricConfig[str](
                        name="output",
                        scorer_fn=lambda step: step.output,
                        scorable_types=["workflow"],
                        aggregator_fn=lambda outputs: ",".join(outputs),
                    ),
                    LocalMetricConfig[float](
                        name="decimal",
                        scorer_fn=lambda step: 4.53,
                        scorable_types=["workflow"],
                        aggregator_fn=lambda values: mean(values),
                    ),
                    LocalMetricConfig[bool](
                        name="bool",
                        scorer_fn=lambda step: True,
                        scorable_types=["workflow"],
                        aggregator_fn=lambda values: reduce(operator.or_, values),
                    ),
                ],
                1,
                "workflow",
                [40, "dummy_function", 4.53, True],
                [40, "dummy_function", 4.53, True],
            ),
            (complex_trace_function, [], 2, "llm", [], []),
            (
                complex_trace_function,
                [
                    LocalMetricConfig[int](
                        name="length",
                        scorer_fn=lambda step: len(step.input[0].content),
                        aggregator_fn=lambda lengths: sum(lengths),
                    ),
                    LocalMetricConfig[str](
                        name="output",
                        scorer_fn=lambda step: step.output.content,
                        aggregator_fn=lambda outputs: ",".join(outputs),
                    ),
                ],
                2,
                "llm",
                [28, "Which continent is Spain in? output"],
                [28, "Which continent is Spain in? output"],
            ),
        ],
    )
    def test_run_experiment_with_func(
        self,
        mock_scorer_settings_class: Mock,
        mock_scorers_class: Mock,
        mock_get_project: Mock,
        mock_get_experiment: Mock,
        mock_create_experiment: Mock,
        mock_get_dataset: Mock,
        mock_traces_client: Mock,
        mock_projects_client: Mock,
        mock_logstreams_client: Mock,
        reset_context,
        dataset_content: DatasetContent,
        function: Callable,
        metrics: list[str | LocalMetricConfig],
        num_spans: int,
        span_type: SPAN_TYPE,
        results: list[MetricValueType],
        aggregate_results: list[MetricValueType],
        thread_pool: bool,
    ) -> None:
        mock_traces_client_instance = setup_mock_traces_client(mock_traces_client)
        setup_mock_projects_client(mock_projects_client)
        setup_mock_logstreams_client(mock_logstreams_client)

        # mock dataset.get_content
        # Return dataset_content on first call (starting_token=0), then None to signal end of pagination
        mock_get_dataset_instance = mock_get_dataset.return_value
        mock_get_dataset_instance.get_content = MagicMock(
            side_effect=lambda starting_token=0, limit=1000: dataset_content if starting_token == 0 else None
        )

        dataset_id = str(UUID(int=0, version=4))

        result = run_experiment(
            experiment_name="test_experiment",
            project="awesome-new-project",
            dataset_id=dataset_id,
            function=function,
            metrics=metrics,
        )
        assert result is not None
        assert result["experiment"] is not None
        assert f"/project/{project().id}/experiments/{experiment_response().id}" in result["link"]
        mock_get_project.assert_called_with(id=None, name="awesome-new-project")
        mock_get_experiment.assert_called_once_with("00000000-0000-0000-0000-000000000000", "test_experiment")
        mock_create_experiment.assert_called_once_with(
            "00000000-0000-0000-0000-000000000000", ANY, mock_get_dataset.return_value
        )

        mock_get_dataset.assert_called_once_with(
            id="00000000-0000-4000-8000-000000000000", name=None, project_id=None, project_name=None
        )
        mock_get_dataset_instance.get_content.assert_called()

        # check galileo_logger
        payload = mock_traces_client_instance.ingest_traces.call_args[0][0]

        assert len(payload.traces) == 1
        trace = payload.traces[0]
        assert trace.dataset_input == "Which continent is Spain in?"
        assert trace.dataset_output == "Europe"
        assert trace.dataset_metadata == {"meta": "data"}

        for metric, metric_result in zip(metrics, aggregate_results, strict=False):
            assert hasattr(trace.metrics, metric.name)
            assert getattr(trace.metrics, metric.name) == metric_result

        def check_span(span: Span) -> int:
            span_count = 1
            assert span.dataset_input == "Which continent is Spain in?"
            assert span.dataset_output == "Europe"
            assert span.dataset_metadata == {"meta": "data"}

            for metric, metric_result in zip(metrics, results, strict=False):
                if span.type == span_type:
                    assert hasattr(span.metrics, metric.name)
                    assert getattr(span.metrics, metric.name) == metric_result
                else:
                    assert not hasattr(span.metrics, metric.name)

            if isinstance(span, StepWithChildSpans):
                for child_span in span.spans:
                    span_count += check_span(child_span)

            return span_count

        assert num_spans == sum(check_span(span) for span in trace.spans)

    @travel(datetime(2012, 1, 1), tick=False)
    @patch("galileo.utils.metrics.ScorerSettings")
    @patch("galileo.utils.metrics.Scorers")
    @patch.object(galileo.datasets.Datasets, "get")
    @patch.object(galileo.experiments.Experiments, "create", return_value=experiment_response())
    @patch.object(galileo.experiments.Experiments, "get", return_value=experiment_response())
    @patch.object(galileo.experiments.Projects, "get_with_env_fallbacks", return_value=project())
    def test_run_experiment_w_prompt_template_and_metrics(
        self,
        mock_get_project: Mock,
        mock_get_experiment: Mock,
        mock_create_experiment: Mock,
        mock_get_dataset: Mock,
        mock_scorers_class: Mock,
        mock_scorer_settings_class: Mock,
        dataset_content: DatasetContent,
    ) -> None:
        # Setup scorer mocks
        mock_scorers_class.return_value.list_by_labels.return_value = scorers()
        mock_scorer_settings_class.return_value.create.return_value = None

        dataset_id = str(UUID(int=0))
        run_experiment(
            "test_experiment",
            project="awesome-new-project",
            dataset_id=dataset_id,
            prompt_template=prompt_template(),
            metrics=[GalileoMetrics.correctness],
        )

        mock_get_project.assert_called_once_with(id=None, name="awesome-new-project")
        mock_get_experiment.assert_called_once_with(project().id, "test_experiment")
        # Experiments.create called with trigger=True and scorers
        mock_create_experiment.assert_called_once_with(
            project_id=project().id,
            name="awesome-new-experiment 2012-01-01 at 00:00:00.000",
            dataset_obj=mock_get_dataset.return_value,
            trigger=True,
            prompt_template=ANY,
            scorers=[ScorerConfig.from_dict(scorers()[0].to_dict())],
            prompt_settings=ANY,
        )
        mock_scorers_class.return_value.list_by_labels.assert_called_once()
        # ScorerSettings.create NOT called for trigger=True flow (API handles it)
        mock_scorer_settings_class.return_value.create.assert_not_called()

    @travel(datetime(2012, 1, 1), tick=False)
    @patch.object(galileo.datasets.Datasets, "get")
    @patch.object(galileo.experiments.Experiments, "create", return_value=experiment_response())
    @patch.object(galileo.experiments.Experiments, "get", return_value=experiment_response())
    @patch.object(galileo.experiments.Projects, "get_with_env_fallbacks", return_value=project())
    def test_run_experiment_w_prompt_template_and_prompt_settings(
        self,
        mock_get_project: Mock,
        mock_get_experiment: Mock,
        mock_create_experiment: Mock,
        mock_get_dataset: Mock,
        dataset_content: DatasetContent,
    ) -> None:
        dataset_id = str(UUID(int=0))
        run_experiment(
            "test_experiment",
            project="awesome-new-project",
            dataset_id=dataset_id,
            prompt_template=prompt_template(),
            prompt_settings=prompt_run_settings(),
        )

        mock_get_project.assert_called_once_with(id=None, name="awesome-new-project")
        mock_get_experiment.assert_called_once_with(project().id, "test_experiment")
        # Experiments.create is called with trigger=True and explicit prompt_settings
        mock_create_experiment.assert_called_once_with(
            project_id=project().id,
            name="awesome-new-experiment 2012-01-01 at 00:00:00.000",
            dataset_obj=mock_get_dataset.return_value,
            trigger=True,
            prompt_template=ANY,
            scorers=None,
            prompt_settings=prompt_run_settings(),
        )

    @travel(datetime(2012, 1, 1), tick=False)
    @patch.object(galileo.datasets.Datasets, "get")
    @patch.object(galileo.experiments.Experiments, "create", return_value=experiment_response())
    @patch.object(galileo.experiments.Experiments, "get", return_value=experiment_response())
    @patch.object(galileo.experiments.Projects, "get_with_env_fallbacks", return_value=project())
    def test_run_experiment_with_prompt_settings_as_dict(
        self,
        mock_get_with_env_fallbacks: Mock,
        mock_get_experiment: Mock,
        mock_create_experiment: Mock,
        mock_get_datasets: Mock,
        dataset_content: DatasetContent,
    ) -> None:
        # Given: a project, dataset, prompt template, and prompt_settings passed as a plain dict
        dataset_id = str(UUID(int=0))
        settings_dict = {
            "n": 1,
            "echo": True,
            "top_k": 10,
            "top_p": 1.0,
            "logprobs": True,
            "max_tokens": 128,
            "model_alias": "GPT-4o",
            "temperature": 0.8,
            "top_logprobs": 10,
            "presence_penalty": 0.0,
            "frequency_penalty": 0.0,
        }

        # When: run_experiment() is called with prompt_settings as a plain dict
        run_experiment(
            "test_experiment",
            project="awesome-new-project",
            dataset_id=dataset_id,
            prompt_template=prompt_template(),
            prompt_settings=settings_dict,
        )

        # Then: no AttributeError; create receives a PromptRunSettings instance with all values preserved
        mock_create_experiment.assert_called_once()
        call_kwargs = mock_create_experiment.call_args.kwargs
        ps = call_kwargs["prompt_settings"]
        assert isinstance(ps, PromptRunSettings)
        assert ps.n == 1
        assert ps.echo is True
        assert ps.top_k == 10
        assert ps.top_p == 1.0
        assert ps.logprobs is True
        assert ps.max_tokens == 128
        assert ps.model_alias == "GPT-4o"
        assert ps.temperature == 0.8
        assert ps.top_logprobs == 10
        assert ps.presence_penalty == 0.0
        assert ps.frequency_penalty == 0.0

    @patch("galileo.experiments.create_experiment_projects_project_id_experiments_post")
    def test_experiments_create_with_prompt_settings_as_dict(
        self, galileo_resources_api_create_experiment: Mock
    ) -> None:
        # Given: Experiments.create() called directly with prompt_settings as a dict
        now = datetime(2020, 1, 1).strftime("%Y-%m-%dT%H:%M:%S.%fZ")
        galileo_resources_api_create_experiment.sync = Mock(
            return_value=ExperimentResponse.from_dict(
                {
                    "id": "test-exp-id",
                    "name": "test_experiment",
                    "project_id": "test-project-id",
                    "created_at": now,
                    "updated_at": now,
                    "task_type": TaskType.VALUE_16,
                }
            )
        )
        settings_dict = {"model_alias": "GPT-4o", "temperature": 0.5, "max_tokens": 256}

        # When: create() is invoked with prompt_settings as a dict
        experiment = Experiments().create(
            project_id="test-project-id", name="test_experiment", prompt_settings=settings_dict
        )

        # Then: the dict is coerced to PromptRunSettings and to_dict() is called without error
        assert experiment.name == "test_experiment"
        call_kwargs = galileo_resources_api_create_experiment.sync.call_args.kwargs
        body = call_kwargs["body"]
        assert "prompt_settings" in body.additional_properties
        ps_dict = body.additional_properties["prompt_settings"]
        assert ps_dict["model_alias"] == "GPT-4o"
        assert ps_dict["temperature"] == 0.5
        assert ps_dict["max_tokens"] == 256

    @patch.object(galileo.experiments.Experiments, "create")
    def test_experiments_run_raises_when_create_raises(self, mock_create: Mock) -> None:
        # Given: Experiments.create raises
        mock_create.side_effect = RuntimeError("API unavailable")

        # When/Then: the exception propagates — create() is a resource management operation
        with pytest.raises(RuntimeError, match="API unavailable"):
            Experiments().run(
                project_obj=project(),
                dataset_obj=Mock(spec=galileo.datasets.Dataset),
                experiment_name="test_experiment",
                prompt_template=None,
                scorers=None,
            )

    @patch.object(galileo.experiments.Experiments, "create", return_value=experiment_response())
    def test_experiments_run_with_prompt_settings_as_dict(self, mock_create: Mock) -> None:
        # Given: a project, dataset, and prompt_settings passed as a plain dict
        settings_dict = {"model_alias": "GPT-4o", "temperature": 0.5, "max_tokens": 256}

        # When: Experiments().run() is called with prompt_settings as a plain dict
        Experiments().run(
            project_obj=project(),
            dataset_obj=Mock(spec=galileo.datasets.Dataset),
            experiment_name="test_experiment",
            prompt_template=prompt_template(),
            scorers=None,
            prompt_settings=settings_dict,
        )

        # Then: create receives a PromptRunSettings instance, not a dict
        mock_create.assert_called_once()
        call_kwargs = mock_create.call_args.kwargs
        ps = call_kwargs["prompt_settings"]
        assert isinstance(ps, PromptRunSettings)
        assert ps.model_alias == "GPT-4o"
        assert ps.temperature == 0.5
        assert ps.max_tokens == 256

    @travel(datetime(2012, 1, 1), tick=False)
    @patch("galileo.logger.logger.LogStreams")
    @patch("galileo.logger.logger.Projects")
    @patch("galileo.logger.logger.Traces")
    @patch.object(galileo.datasets.Datasets, "get")
    @patch.object(galileo.jobs.Jobs, "create")
    @patch.object(galileo.experiments.Experiments, "create", return_value=experiment_response())
    @patch.object(galileo.experiments.Experiments, "get", return_value=experiment_response())
    @patch.object(galileo.experiments.Projects, "get_with_env_fallbacks", return_value=project())
    def test_run_experiment_with_runner_and_dataset(
        self,
        mock_get_project: Mock,
        mock_get_experiment: Mock,
        mock_create_experiment: Mock,
        mock_create_job: Mock,
        mock_get_dataset: Mock,
        mock_traces_client: Mock,
        mock_projects_client: Mock,
        mock_logstreams_client: Mock,
        reset_context,
        dataset_content_with_question: DatasetContent,
    ) -> None:
        mock_core_api_instance = setup_mock_traces_client(mock_traces_client)
        setup_mock_projects_client(mock_projects_client)
        setup_mock_logstreams_client(mock_logstreams_client)

        mock_create_job.return_value = MagicMock()

        # mock dataset.get_content
        # Return dataset_content on first call (starting_token=0), then None to signal end of pagination
        mock_get_dataset_instance = mock_get_dataset.return_value
        mock_get_dataset_instance.get_content = MagicMock(
            side_effect=lambda starting_token=0, limit=1000: dataset_content_with_question
            if starting_token == 0
            else None
        )

        def runner(input) -> str:
            # emulate using input
            return f"Say hello: {input['question']}"

        result = run_experiment(
            "test_experiment", project="awesome-new-project", dataset_id=str(UUID(int=0)), function=runner
        )
        assert result is not None
        assert result["experiment"] is not None

        mock_get_project.assert_called_with(id=None, name="awesome-new-project")
        mock_get_experiment.assert_called_once_with("00000000-0000-0000-0000-000000000000", "test_experiment")
        mock_create_experiment.assert_called_once_with(
            "00000000-0000-0000-0000-000000000000", ANY, mock_get_dataset.return_value
        )

        mock_get_dataset.assert_called_once_with(
            id="00000000-0000-0000-0000-000000000000", name=None, project_id=None, project_name=None
        )
        mock_get_dataset_instance.get_content.assert_called()

        # check galileo_logger
        payload = mock_core_api_instance.ingest_traces.call_args[0][0]
        assert len(payload.traces) == 1
        assert (
            payload.traces[0].input == '{"input": {"question": "Which continent is Spain in?", "expected": "Europe"}}'
        )
        assert payload.traces[0].output == "Say hello: Which continent is Spain in?"

    @travel(datetime(2012, 1, 1), tick=False)
    @patch.object(galileo.datasets.Datasets, "get")
    @patch.object(galileo.experiments.Experiments, "create")
    @patch.object(galileo.experiments.Experiments, "get")
    @patch.object(galileo.experiments.Projects, "get_with_env_fallbacks", return_value=project())
    def test_run_experiment_raises_when_create_raises(
        self,
        mock_get_project: Mock,
        mock_get_experiment: Mock,
        mock_create_experiment: Mock,
        mock_get_dataset: Mock,
        dataset_content: DatasetContent,
    ) -> None:
        # Given: Experiments.create raises
        mock_create_experiment.side_effect = RuntimeError("server error")

        # When/Then: the exception propagates regardless of on_error — create() is a resource management operation
        with pytest.raises(RuntimeError, match="server error"):
            run_experiment(
                "test_experiment",
                project="awesome-new-project",
                dataset_id=str(UUID(int=0)),
                prompt_template=prompt_template(),
            )

    @travel(datetime(2012, 1, 1), tick=False)
    @patch.object(galileo.datasets.Datasets, "get")
    @patch.object(
        galileo.experiments.Experiments,
        "run",
        return_value={"experiment": experiment_response(), "link": "http://example.com", "message": "done"},
    )
    @patch.object(galileo.experiments.Experiments, "get", return_value=None)
    @patch.object(galileo.experiments.Projects, "get_with_env_fallbacks", return_value=project())
    def test_run_experiment_on_error_warns_when_unused_in_prompt_template_flow(
        self,
        mock_get_project: Mock,
        mock_get_experiment: Mock,
        mock_run: Mock,
        mock_get_dataset: Mock,
        dataset_content: DatasetContent,
    ) -> None:
        # Given: an on_error callback is provided for the prompt-template flow
        on_error = Mock()

        # When: run_experiment() is called with a prompt template and on_error
        with patch("galileo.experiments._logger") as mock_logger:
            run_experiment(
                "test_experiment",
                project="awesome-new-project",
                dataset_id=str(UUID(int=0)),
                prompt_template=prompt_template(),
                on_error=on_error,
            )

        # Then: a warning is logged and on_error is never invoked
        mock_logger.warning.assert_any_call(
            "on_error was provided but will not be invoked in the prompt-template flow "
            "(no flush occurs on this path). on_error is only used in the function flow."
        )
        on_error.assert_not_called()

    @patch("galileo.logger.logger.LogStreams")
    @patch("galileo.logger.logger.Projects")
    @patch("galileo.logger.logger.Traces")
    @patch.object(galileo.datasets.Datasets, "get")
    @patch.object(galileo.experiments.Experiments, "create", return_value=experiment_response())
    @patch.object(galileo.experiments.Experiments, "get", return_value=experiment_response())
    @patch.object(galileo.experiments.Projects, "get_with_env_fallbacks", return_value=project())
    def test_run_experiment_on_error_passed_to_flush_in_function_flow(
        self,
        mock_get_project: Mock,
        mock_get_experiment: Mock,
        mock_create_experiment: Mock,
        mock_get_dataset: Mock,
        mock_traces_client: Mock,
        mock_projects_client: Mock,
        mock_logstreams_client: Mock,
        dataset_content: DatasetContent,
        reset_context,
    ) -> None:
        # Given: an on_error callback is provided for the function flow
        setup_mock_traces_client(mock_traces_client)
        setup_mock_projects_client(mock_projects_client)
        setup_mock_logstreams_client(mock_logstreams_client)
        mock_get_dataset_instance = mock_get_dataset.return_value
        mock_get_dataset_instance.get_content = MagicMock(
            side_effect=lambda starting_token=0, limit=1000: dataset_content if starting_token == 0 else None
        )
        on_error = Mock()

        # When: run_experiment() is called with a function and on_error (function flow)
        with patch("galileo.experiments.galileo_context.flush") as mock_flush:
            run_experiment(
                experiment_name="test_experiment",
                project="awesome-new-project",
                dataset_id=str(UUID(int=0, version=4)),
                function=lambda x: "output",
                on_error=on_error,
            )

        # Then: every flush call received on_error — no call was made without it
        assert mock_flush.call_count >= 1
        assert all(c == mock_call(on_error=on_error) for c in mock_flush.call_args_list)

    @patch.object(galileo.datasets.Datasets, "get")
    def test_run_experiment_with_prompt_template_and_function(
        self, mock_get_dataset: Mock, dataset_content: DatasetContent
    ) -> None:
        with pytest.raises(ValueError) as exc_info:
            run_experiment(
                "test_experiment",
                project="awesome-new-project",
                dataset_id=str(UUID(int=1)),
                function=lambda x: x,
                prompt_template=prompt_template(),
            )
        assert str(exc_info.value) == "A function or prompt_template should be provided, but not both"

        mock_get_dataset.assert_called_once_with(
            id="00000000-0000-0000-0000-000000000001", name=None, project_id=None, project_name=None
        )

    @patch.object(galileo.experiments.Projects, "get_with_env_fallbacks", return_value=project())
    def test_run_experiment_with_prompt_template_and_local_dataset(
        self, mock_projects_client: Mock, local_dataset: list[dict[str, str]]
    ) -> None:
        setup_mock_projects_client(mock_projects_client)

        with pytest.raises(ValueError) as exc_info:
            run_experiment(
                "test_experiment",
                project="awesome-new-project",
                dataset=local_dataset,
                prompt_template=prompt_template(),
            )
        assert (
            str(exc_info.value)
            == "A dataset record, id, or name of a dataset must be provided when a prompt_template is used"
        )

    @patch("galileo.logger.logger.Projects")
    @patch.object(galileo.datasets.Datasets, "get")
    @patch.object(galileo.experiments.Experiments, "create", return_value=experiment_response())
    @patch.object(galileo.experiments.Experiments, "get", return_value=experiment_response())
    @patch.object(galileo.experiments.Projects, "get_with_env_fallbacks", return_value=project())
    @patch("galileo.utils.metrics.Scorers")
    @patch("galileo.utils.metrics.Scorers")
    @patch("galileo.utils.metrics.ScorerSettings")
    def test_run_experiment_with_local_scorers_and_prompt_template(
        self,
        mock_scorer_settings_create: Mock,
        mock_get_scorer_version: Mock,
        mock_scorers_list: Mock,
        mock_get_project: Mock,
        mock_get_experiment: Mock,
        mock_create_experiment: Mock,
        mock_get_dataset: Mock,
        mock_projects_client: Mock,
        dataset_content_with_question: DatasetContent,
    ) -> None:
        setup_mock_projects_client(mock_projects_client)
        mock_get_dataset_instance = mock_get_dataset.return_value
        mock_get_dataset_instance.get_content = MagicMock(return_value=dataset_content_with_question)

        local_scorer = LocalMetricConfig(
            name="local_scorer", scorer_fn=lambda x: x
        )  # Create a LocalMetricConfig instance
        with pytest.raises(ValueError) as exc_info:
            run_experiment(
                "test_experiment",
                project="awesome-new-project",
                dataset_id=str(UUID(int=1)),
                prompt_template=prompt_template(),
                metrics=[local_scorer],
            )
        assert (
            str(exc_info.value)
            == "Local metrics can only be used with a locally run experiment, not a prompt experiment."
        )

    @patch("galileo.utils.metrics.Scorers")
    @patch("galileo.utils.metrics.ScorerSettings")
    def test_create_scorer_configs(self, mock_scorer_settings_class, mock_scorers_class) -> None:
        # Setup mock return values — new code uses list_by_labels
        mock_scorers_instance = mock_scorers_class.return_value
        mock_scorers_instance.list_by_labels.return_value = [
            ScorerResponse(id="1", name="metric1", label="metric1", scorer_type=ScorerTypes.PRESET, tags=[]),
            ScorerResponse(id="2", name="metric2", label="metric2", scorer_type=ScorerTypes.PRESET, tags=[]),
        ]
        mock_scorer_settings_class.return_value.create = MagicMock()

        # Test valid metrics
        from galileo.utils.metrics import create_metric_configs

        scorers, local_scorers = create_metric_configs(
            "project_id", "experiment_id", ["metric1", LocalMetricConfig(name="length", scorer_fn=lambda x: len(x))]
        )
        assert len(scorers) == 1  # Should return one valid scorer
        assert len(local_scorers) == 1  # Should return one local scorer

        # Test unknown metrics
        mock_scorers_instance.list_by_labels.return_value = []
        with pytest.raises(ValueError):
            create_metric_configs("project_id", "experiment_id", ["unknown_metric"])

    @patch("galileo.utils.metrics.Scorers")
    @patch("galileo.utils.metrics.ScorerSettings")
    def test_create_scorer_configs_with_metric_objects(self, mock_scorer_settings_class, mock_scorers_class) -> None:
        # Setup mock return values
        mock_scorers_instance = mock_scorers_class.return_value
        mock_scorer_settings_class.return_value.create = MagicMock()

        # Create mock scorer responses
        mock_scorer_responses = [
            ScorerResponse.from_dict({"id": "1", "name": "metric1", "scorer_type": "preset", "tags": ["test"]}),
            ScorerResponse.from_dict({"id": "2", "name": "metric2", "scorer_type": "preset", "tags": ["test"]}),
            ScorerResponse.from_dict({"id": "3", "name": "versionable_metric", "scorer_type": "llm", "tags": ["test"]}),
        ]

        mock_scorers_instance.list_by_labels.return_value = mock_scorer_responses

        # Mock the get_scorer_version method
        mock_version_response = MagicMock()
        mock_version_response.to_dict.return_value = {"id": "version1", "version": 2}
        mock_scorers_instance.get_scorer_version.return_value = mock_version_response

        from galileo.schema.metrics import Metric

        # Test with Metric objects (without version)
        metric1 = Metric(name="metric1")
        metric2 = Metric(name="metric2")
        from galileo.utils.metrics import create_metric_configs

        scorers, local_scorers = create_metric_configs("project_id", "experiment_id", [metric1, metric2])

        assert len(scorers) == 2  # Should return two valid scorers
        assert len(local_scorers) == 0  # No local scorers

        # Verify get_scorer_version was not called (since no version was specified)
        mock_scorers_instance.get_scorer_version.assert_not_called()

        # Test with a Metric object with version
        versionable_metric = Metric(name="versionable_metric", version=2)

        from galileo.utils.metrics import create_metric_configs

        scorers, local_scorers = create_metric_configs("project_id", "experiment_id", [versionable_metric])

        assert len(scorers) == 1  # Should return one valid scorer
        assert len(local_scorers) == 0  # No local scorers

        # Verify get_scorer_version was called with the correct parameters
        mock_scorers_instance.get_scorer_version.assert_called_once_with(scorer_id="3", version=2)

        # Test mixed input types
        local_metric = LocalMetricConfig(name="length", scorer_fn=lambda x: len(x))

        from galileo.utils.metrics import create_metric_configs

        scorers, local_scorers = create_metric_configs(
            "project_id", "experiment_id", ["metric1", local_metric, Metric(name="metric2")]
        )

        assert len(scorers) == 2  # Should return two valid scorers
        assert len(local_scorers) == 1  # One local scorer

    @patch.object(galileo.datasets.Datasets, "get")
    @patch.object(galileo.experiments.Experiments, "create", side_effect=ValueError("experiment creation failed"))
    @patch.object(galileo.experiments.Experiments, "get", return_value=None)
    @patch.object(galileo.experiments.Projects, "get_with_env_fallbacks", return_value=project())
    def test_run_experiment_job_creation_failure(
        self,
        mock_get_project: Mock,
        mock_get_experiment: Mock,
        mock_create_experiment: Mock,
        mock_get_dataset: Mock,
        dataset_content: DatasetContent,
    ) -> None:
        # Given: Experiments.create raises an error (trigger=True handles job creation)
        mock_get_dataset_instance = mock_get_dataset.return_value
        mock_get_dataset_instance.get_content = MagicMock(return_value=dataset_content)

        # When/Then: the error propagates
        with pytest.raises(ValueError, match="experiment creation failed"):
            run_experiment(
                "test_experiment",
                project="awesome-new-project",
                dataset_id=str(UUID(int=0)),
                prompt_template=prompt_template(),
            )

        mock_get_project.assert_called_once_with(id=None, name="awesome-new-project")

    @patch("galileo.experiments.upsert_experiment_tag")
    @patch.object(galileo.datasets.Datasets, "get")
    @patch.object(galileo.jobs.Jobs, "create")
    @patch.object(galileo.experiments.Experiments, "create", return_value=experiment_response())
    @patch.object(galileo.experiments.Experiments, "get", return_value=None)
    @patch.object(galileo.experiments.Projects, "get_with_env_fallbacks", return_value=project())
    def test_run_experiment_with_experiment_tags_basic(
        self,
        mock_get_project: Mock,
        mock_get_experiment: Mock,
        mock_create_experiment: Mock,
        mock_create_job: Mock,
        mock_get_dataset: Mock,
        mock_upsert_tag: Mock,
        dataset_content: DatasetContent,
    ) -> None:
        """Test that experiment_tags are applied when running experiments."""
        mock_create_job.return_value = MagicMock()
        mock_get_dataset_instance = mock_get_dataset.return_value
        mock_get_dataset_instance.get_content = MagicMock(return_value=dataset_content)

        experiment_tags = {"environment": "test", "version": "1.0", "team": "qa"}

        run_experiment(
            experiment_name="test_experiment_with_tags",
            project="awesome-new-project",
            dataset_id=str(UUID(int=0)),
            prompt_template=prompt_template(),
            experiment_tags=experiment_tags,
        )

        assert mock_upsert_tag.call_count == 3

    @patch("galileo.logger.logger.LogStreams")
    @patch("galileo.logger.logger.Projects")
    @patch("galileo.logger.logger.Traces")
    @patch.object(galileo.datasets.Datasets, "get")
    @patch.object(galileo.experiments.Experiments, "create", return_value=experiment_response())
    @patch.object(galileo.experiments.Experiments, "get", return_value=experiment_response())
    @patch.object(galileo.experiments.Projects, "get_with_env_fallbacks", return_value=project())
    def test_run_experiment_with_dataset_limit(
        self,
        mock_get_project: Mock,
        mock_get_experiment: Mock,
        mock_create_experiment: Mock,
        mock_get_dataset: Mock,
        mock_traces_client: Mock,
        mock_projects_client: Mock,
        mock_logstreams_client: Mock,
        dataset_content_150_rows: DatasetContent,
        reset_context,
    ) -> None:
        """Test that all 150 rows are processed when no dataset_limit is specified."""
        mock_traces_client_instance = setup_mock_traces_client(mock_traces_client)
        setup_mock_projects_client(mock_projects_client)
        setup_mock_logstreams_client(mock_logstreams_client)

        # Return dataset_content on first call (starting_token=0), then None to signal end of pagination
        mock_get_dataset_instance = mock_get_dataset.return_value
        mock_get_dataset_instance.get_content = MagicMock(
            side_effect=lambda starting_token=0, limit=1000: dataset_content_150_rows if starting_token == 0 else None
        )

        run_experiment(
            "test_experiment",
            project="awesome-new-project",
            dataset_id=str(UUID(int=0)),
            function=lambda x: f"output: {x}",
        )

        # Verify get_content was called with pagination parameters
        assert mock_get_dataset_instance.get_content.call_count >= 1

        # Verify that all 150 rows were processed by checking the traces across all flush calls
        total_traces = 0
        for call in mock_traces_client_instance.ingest_traces.call_args_list:
            payload = call[0][0]
            total_traces += len(payload.traces)
        assert total_traces == 150

    @patch("galileo.logger.logger.LogStreams")
    @patch("galileo.logger.logger.Projects")
    @patch("galileo.logger.logger.Traces")
    @patch.object(galileo.experiments.Experiments, "create", return_value=experiment_response())
    @patch.object(galileo.experiments.Experiments, "get", return_value=experiment_response())
    @patch.object(galileo.experiments.Projects, "get_with_env_fallbacks", return_value=project())
    def test_run_experiment_with_function_and_list_dataset(
        self,
        mock_get_project: Mock,
        mock_get_experiment: Mock,
        mock_create_experiment: Mock,
        mock_traces_client: Mock,
        mock_projects_client: Mock,
        mock_logstreams_client: Mock,
        local_dataset: list[dict[str, str]],
        reset_context,
    ) -> None:
        """Test running experiment with a function and inline list dataset (static records path)."""
        mock_traces_client_instance = setup_mock_traces_client(mock_traces_client)
        setup_mock_projects_client(mock_projects_client)
        setup_mock_logstreams_client(mock_logstreams_client)

        def simple_function(input: dict) -> str:
            return f"Processed: {input['input']}"

        result = run_experiment(
            experiment_name="test_experiment",
            project="awesome-new-project",
            dataset=local_dataset,
            function=simple_function,
        )

        assert result is not None
        assert result["experiment"] is not None
        assert f"/project/{project().id}/experiments/{experiment_response().id}" in result["link"]

        # Verify experiment was created without dataset_obj (since we used a list)
        mock_create_experiment.assert_called_once_with("00000000-0000-0000-0000-000000000000", ANY, None)

        # Verify all rows from the list were processed
        # The traces are batched together, so we need to count all traces across all calls
        all_traces = []
        for call in mock_traces_client_instance.ingest_traces.call_args_list:
            payload = call[0][0]
            all_traces.extend(payload.traces)

        # Each record creates a trace, and they're all sent in one batch
        assert len(all_traces) >= 1  # At least one trace object

        # Count the actual workflow spans (each represents a processed record)
        total_spans = sum(len(trace.spans) for trace in all_traces)
        assert total_spans == len(local_dataset)

        # Verify both records were processed (checking the input data in the spans)
        first_trace = all_traces[0]
        assert len(first_trace.spans) == 2
        # Check that we have inputs for both Spain and Japan questions
        span_inputs = [span.input for span in first_trace.spans]
        assert '{"input": "Which continent is Spain in?"}' in span_inputs[0]
        assert '{"input": "Which continent is Japan in?"}' in span_inputs[1]

    @patch("galileo.logger.logger.LogStreams")
    @patch("galileo.logger.logger.Projects")
    @patch("galileo.logger.logger.Traces")
    @patch.object(galileo.datasets.Datasets, "get")
    @patch.object(galileo.experiments.Experiments, "create", return_value=experiment_response())
    @patch.object(galileo.experiments.Experiments, "get", return_value=experiment_response())
    @patch.object(galileo.experiments.Projects, "get_with_env_fallbacks", return_value=project())
    def test_run_experiment_with_multi_page_pagination(
        self,
        mock_get_project: Mock,
        mock_get_experiment: Mock,
        mock_create_experiment: Mock,
        mock_get_dataset: Mock,
        mock_traces_client: Mock,
        mock_projects_client: Mock,
        mock_logstreams_client: Mock,
        reset_context,
    ) -> None:
        """Test that pagination works correctly across multiple pages."""
        mock_traces_client_instance = setup_mock_traces_client(mock_traces_client)
        setup_mock_projects_client(mock_projects_client)
        setup_mock_logstreams_client(mock_logstreams_client)

        # Create three pages: 1000 rows, 500 rows, then None
        page1_rows = [
            DatasetRow(
                index=i,
                row_id=f"row{i}",
                values=[f"Question {i}", f"Answer {i}", None],
                values_dict=DatasetRowValuesDict.from_dict(
                    {"input": f"Question {i}", "output": f"Answer {i}", "metadata": None}
                ),
                metadata=None,
            )
            for i in range(1000)
        ]
        page2_rows = [
            DatasetRow(
                index=i,
                row_id=f"row{i}",
                values=[f"Question {i}", f"Answer {i}", None],
                values_dict=DatasetRowValuesDict.from_dict(
                    {"input": f"Question {i}", "output": f"Answer {i}", "metadata": None}
                ),
                metadata=None,
            )
            for i in range(1000, 1500)
        ]

        page1_content = DatasetContent(rows=page1_rows)
        page2_content = DatasetContent(rows=page2_rows)

        # Mock get_content to return pages based on starting_token
        def mock_get_content_paginated(starting_token=0, limit=1000):
            if starting_token == 0:
                return page1_content
            elif starting_token == 1000:
                return page2_content
            else:
                return None

        mock_get_dataset_instance = mock_get_dataset.return_value
        mock_get_dataset_instance.get_content = MagicMock(side_effect=mock_get_content_paginated)

        run_experiment(
            experiment_name="test_experiment",
            project="awesome-new-project",
            dataset_id=str(UUID(int=0)),
            function=lambda x: f"output: {x}",
        )

        # Verify get_content was called with correct pagination tokens
        assert mock_get_dataset_instance.get_content.call_count == 3
        call_args_list = [call[1] for call in mock_get_dataset_instance.get_content.call_args_list]
        assert {"starting_token": 0, "limit": 1000} in call_args_list
        assert {"starting_token": 1000, "limit": 1000} in call_args_list
        assert {"starting_token": 1500, "limit": 1000} in call_args_list

        # Verify all 1500 rows were processed
        total_traces = 0
        for call in mock_traces_client_instance.ingest_traces.call_args_list:
            payload = call[0][0]
            total_traces += len(payload.traces)
        assert total_traces == 1500


# ===========================================================================
# Experiment Groups V1 — group identity + discovery helper
# ===========================================================================


class TestExperimentGroups:
    """V1 experiment-group support: group-aware run/create + list_experiment_groups()."""

    @patch.object(
        galileo.experiments.Experiments,
        "run",
        return_value={"experiment": experiment_response(), "link": "x", "message": "y"},
    )
    @patch.object(galileo.experiments.Experiments, "get", return_value=None)
    @patch.object(galileo.experiments.Projects, "get_with_env_fallbacks", return_value=project())
    @patch("galileo.experiments.load_dataset")
    def test_run_experiment_with_experiment_group_name(
        self, load_dataset_mock: Mock, get_project_mock: Mock, get_experiment_mock: Mock, run_mock: Mock
    ) -> None:
        """run_experiment(experiment_group=...) forwards experiment_group_name to Experiments.run()."""
        # Given: a resolved project, no existing experiment, and a stubbed dataset
        load_dataset_mock.return_value = MagicMock()

        # When: running an experiment with experiment_group=
        run_experiment(
            experiment_name="grouped-run",
            project="awesome-new-project",
            dataset_id=str(UUID(int=0)),
            prompt_template=prompt_template(),
            experiment_group="my-rag-bench",
        )

        # Then: Experiments.run was called with the group name (and no group id)
        run_mock.assert_called_once()
        call_kwargs = run_mock.call_args.kwargs
        assert call_kwargs.get("experiment_group_name") == "my-rag-bench"
        assert "experiment_group_id" not in call_kwargs

    @patch.object(
        galileo.experiments.Experiments,
        "run",
        return_value={"experiment": experiment_response(), "link": "x", "message": "y"},
    )
    @patch.object(galileo.experiments.Experiments, "get", return_value=None)
    @patch.object(galileo.experiments.Projects, "get_with_env_fallbacks", return_value=project())
    @patch("galileo.experiments.load_dataset")
    def test_run_experiment_with_experiment_group_id(
        self, load_dataset_mock: Mock, get_project_mock: Mock, get_experiment_mock: Mock, run_mock: Mock
    ) -> None:
        """run_experiment(experiment_group_id=...) forwards experiment_group_id to Experiments.run()."""
        # Given: a resolved project, no existing experiment, and a stubbed dataset
        load_dataset_mock.return_value = MagicMock()
        group_uuid = str(UUID(int=42))

        # When: running an experiment with experiment_group_id=
        run_experiment(
            experiment_name="id-run",
            project="awesome-new-project",
            dataset_id=str(UUID(int=0)),
            prompt_template=prompt_template(),
            experiment_group_id=group_uuid,
        )

        # Then: Experiments.run was called with the group id (and no group name)
        run_mock.assert_called_once()
        call_kwargs = run_mock.call_args.kwargs
        assert call_kwargs.get("experiment_group_id") == group_uuid
        assert "experiment_group_name" not in call_kwargs

    @patch("galileo.experiments.create_experiment_projects_project_id_experiments_post")
    @patch("galileo.experiments.Projects.get_with_env_fallbacks")
    def test_create_experiment_with_experiment_group_name(
        self, get_project_mock: Mock, create_experiment_mock: Mock
    ) -> None:
        """create_experiment(experiment_group=...) flows the name through to the API body."""
        # Given: a resolved project and a mocked create endpoint
        get_project_mock.return_value = project()
        create_experiment_mock.sync = Mock(return_value=experiment_response())

        # When: creating an experiment with experiment_group=
        create_experiment(
            experiment_name="grouped-create", project_name="awesome-new-project", experiment_group="standalone-bench"
        )

        # Then: the create body carries experiment_group_name
        body = create_experiment_mock.sync.call_args.kwargs["body"]
        assert body.additional_properties["experiment_group_name"] == "standalone-bench"
        assert "experiment_group_id" not in body.additional_properties

    @patch("galileo.experiments.create_experiment_projects_project_id_experiments_post")
    @patch("galileo.experiments.Projects.get_with_env_fallbacks")
    def test_create_experiment_with_experiment_group_id(
        self, get_project_mock: Mock, create_experiment_mock: Mock
    ) -> None:
        """create_experiment(experiment_group_id=...) flows the id through to the API body."""
        # Given: a resolved project and a mocked create endpoint
        get_project_mock.return_value = project()
        create_experiment_mock.sync = Mock(return_value=experiment_response())

        # When: creating an experiment with experiment_group_id=
        group_uuid = str(UUID(int=99))
        create_experiment(
            experiment_name="id-create", project_name="awesome-new-project", experiment_group_id=group_uuid
        )

        # Then: the create body carries experiment_group_id
        body = create_experiment_mock.sync.call_args.kwargs["body"]
        assert body.additional_properties["experiment_group_id"] == group_uuid
        assert "experiment_group_name" not in body.additional_properties

    @patch("galileo.experiments.GalileoPythonConfig")
    @patch("galileo.experiments.Projects.get_with_env_fallbacks")
    def test_list_experiment_groups(self, get_project_mock: Mock, config_mock: Mock) -> None:
        """list_experiment_groups() POSTs to /experiment-groups/query and returns typed objects."""
        # Given: a resolved project and a mocked httpx client returning two groups

        get_project_mock.return_value = project()

        now_iso = datetime.now().isoformat() + "Z"
        api_payload = {
            "starting_token": 0,
            "limit": 100,
            "paginated": False,
            "next_starting_token": None,
            "experiment_groups": [
                {
                    "id": str(UUID(int=1)),
                    "name": "group-a",
                    "project_id": str(UUID(int=0)),
                    "created_at": now_iso,
                    "updated_at": now_iso,
                    "is_system": False,
                    "experiment_count": 2,
                    "datasets": [],
                },
                {
                    "id": str(UUID(int=2)),
                    "name": "Ungrouped",
                    "project_id": str(UUID(int=0)),
                    "created_at": now_iso,
                    "updated_at": now_iso,
                    "is_system": True,
                    "experiment_count": 0,
                    "datasets": [],
                },
            ],
        }

        fake_response = MagicMock()
        fake_response.json.return_value = api_payload
        fake_response.raise_for_status = MagicMock()

        # API returns a single page (paginated=False)
        api_payload["paginated"] = False
        api_payload["next_starting_token"] = None
        config_mock.get.return_value.api_client.request.return_value = fake_response

        # When: listing experiment groups
        groups = list_experiment_groups(project_name="awesome-new-project")

        # Then: it calls ApiClient.request once with the right path and pagination body
        config_mock.get.return_value.api_client.request.assert_called_once()
        call_kwargs = config_mock.get.return_value.api_client.request.call_args.kwargs
        assert call_kwargs["path"] == f"/projects/{UUID(int=0)}/experiment-groups/query"
        assert call_kwargs["json"] == {"starting_token": 0, "limit": 100}
        assert call_kwargs["return_raw_response"] is True

        assert len(groups) == 2
        assert all(isinstance(g, ExperimentGroupResponse) for g in groups)
        assert groups[0].name == "group-a"
        assert groups[0].experiment_count == 2
        assert groups[1].is_system is True

    @patch("galileo.experiments.GalileoPythonConfig")
    @patch("galileo.experiments.Projects.get_with_env_fallbacks")
    def test_list_experiment_groups_paginates_internally(self, get_project_mock: Mock, config_mock: Mock) -> None:
        """list_experiment_groups() walks all pages and returns the combined list."""
        # Given: a project and an API that returns 2 pages

        get_project_mock.return_value = project()

        now_iso = datetime.now().isoformat() + "Z"

        def make_group(idx: int, system: bool = False) -> dict:
            return {
                "id": str(UUID(int=idx)),
                "name": f"group-{idx}",
                "project_id": str(UUID(int=0)),
                "created_at": now_iso,
                "updated_at": now_iso,
                "is_system": system,
                "experiment_count": 0,
                "datasets": [],
            }

        page1 = MagicMock()
        page1.json.return_value = {
            "experiment_groups": [make_group(1), make_group(2)],
            "paginated": True,
            "next_starting_token": 100,
        }
        page1.raise_for_status = MagicMock()

        page2 = MagicMock()
        page2.json.return_value = {
            "experiment_groups": [make_group(3)],
            "paginated": False,
            "next_starting_token": None,
        }
        page2.raise_for_status = MagicMock()

        config_mock.get.return_value.api_client.request.side_effect = [page1, page2]

        # When: listing experiment groups
        groups = list_experiment_groups(project_name="awesome-new-project")

        # Then: both pages are walked and the combined list is returned
        assert config_mock.get.return_value.api_client.request.call_count == 2
        starting_tokens = [
            c.kwargs["json"]["starting_token"] for c in config_mock.get.return_value.api_client.request.call_args_list
        ]
        assert starting_tokens == [0, 100]
        assert len(groups) == 3
        assert [g.name for g in groups] == ["group-1", "group-2", "group-3"]

    @patch("galileo.experiments.GalileoPythonConfig")
    @patch("galileo.experiments.Projects.get_with_env_fallbacks")
    def test_get_experiments_with_group_name_filter(self, get_project_mock: Mock, config_mock: Mock) -> None:
        """get_experiments(experiment_group=...) calls the search endpoint with a name filter."""
        # Given: a resolved project and a search endpoint that returns one matching experiment
        get_project_mock.return_value = project()
        fake_response = MagicMock()
        fake_response.json.return_value = {
            "experiments": [experiment_response().to_dict()],
            "paginated": False,
            "next_starting_token": None,
        }
        fake_response.raise_for_status = MagicMock()
        config_mock.get.return_value.api_client.request.return_value = fake_response

        # When: filtering by group name
        result = get_experiments(project_name="awesome-new-project", experiment_group="my-group")

        # Then: it calls /experiments/search with the right filter and returns the experiment
        config_mock.get.return_value.api_client.request.assert_called_once()
        kwargs = config_mock.get.return_value.api_client.request.call_args.kwargs
        assert kwargs["path"] == f"/projects/{UUID(int=0)}/experiments/search"
        body = kwargs["json"]
        assert body["filters"] == [
            {
                "filter_type": "string",
                "name": "experiment_group_name",
                "operator": "eq",
                "value": "my-group",
                "case_sensitive": True,
            }
        ]
        assert body["starting_token"] == 0
        assert isinstance(result, list)
        assert len(result) == 1

    @patch("galileo.experiments.GalileoPythonConfig")
    @patch("galileo.experiments.Projects.get_with_env_fallbacks")
    def test_get_experiments_with_group_id_filter(self, get_project_mock: Mock, config_mock: Mock) -> None:
        """get_experiments(experiment_group_id=...) calls the search endpoint with an id filter."""
        # Given: a resolved project and a search endpoint that returns one matching experiment
        get_project_mock.return_value = project()
        fake_response = MagicMock()
        fake_response.json.return_value = {
            "experiments": [experiment_response().to_dict()],
            "paginated": False,
            "next_starting_token": None,
        }
        fake_response.raise_for_status = MagicMock()
        config_mock.get.return_value.api_client.request.return_value = fake_response

        group_uuid = str(UUID(int=42))

        # When: filtering by group ID
        result = get_experiments(project_name="awesome-new-project", experiment_group_id=group_uuid)

        # Then: filter sends a custom_uuid filter clause (matches API schema —
        # ExperimentGroupIDFilter extends CustomUUIDFilter, which has no operator)
        kwargs = config_mock.get.return_value.api_client.request.call_args.kwargs
        body = kwargs["json"]
        assert body["filters"] == [
            {
                "filter_type": "custom_uuid",
                "name": "experiment_group_id",
                "value": group_uuid,
            }
        ]
        assert isinstance(result, list)
        assert len(result) == 1

    @patch("galileo.experiments.list_experiments_projects_project_id_experiments_get")
    @patch("galileo.experiments.Projects.get_with_env_fallbacks")
    def test_get_experiments_without_filter_unchanged(
        self, get_project_mock: Mock, list_experiments_mock: Mock
    ) -> None:
        """get_experiments() without any filter still calls the legacy list endpoint."""
        # Given: a resolved project and the existing list endpoint
        get_project_mock.return_value = project()
        list_experiments_mock.sync = Mock(return_value=[experiment_response()])

        # When: calling without filter
        result = get_experiments(project_name="awesome-new-project")

        # Then: legacy list endpoint is used (no search call), returning the project's experiments
        list_experiments_mock.sync.assert_called_once_with(project_id=str(UUID(int=0)), client=ANY)
        assert isinstance(result, list)
        assert len(result) == 1
