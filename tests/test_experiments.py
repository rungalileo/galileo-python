import operator
import os
from datetime import datetime
from functools import reduce
from statistics import mean
from typing import Callable, Union
from unittest.mock import ANY, MagicMock, Mock, patch
from uuid import UUID

import pytest
from time_machine import travel

import galileo.experiments
import galileo.utils.datasets
from galileo import galileo_context
from galileo.decorator import SPAN_TYPE
from galileo.experiments import Experiments, create_experiment, get_experiment, get_experiments, run_experiment
from galileo.projects import Project
from galileo.prompts import PromptTemplate
from galileo.resources.models import (
    BasePromptTemplateResponse,
    BasePromptTemplateVersionResponse,
    DatasetContent,
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
from galileo.schema.metrics import GalileoScorers, LocalMetricConfig
from galileo.utils.datasets import load_dataset_and_records
from galileo_core.exceptions.http import GalileoHTTPException
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
    @patch.object(galileo.jobs.Jobs, "create")
    @patch.object(galileo.experiments.Experiments, "create", return_value=experiment_response())
    @patch.object(galileo.experiments.Experiments, "get", return_value=experiment_response())
    @patch.object(galileo.experiments.Projects, "get_with_env_fallbacks", return_value=project())
    def test_run_experiment_without_metrics(
        self,
        mock_get_project: Mock,
        mock_get_experiment: Mock,
        mock_create_experiment: Mock,
        mock_create_job: Mock,
        mock_get_dataset: Mock,
        dataset_content: DatasetContent,
    ) -> None:
        mock_create_job.return_value = MagicMock()

        dataset_id = str(UUID(int=0))
        result = run_experiment(
            "test_experiment", project="awesome-new-project", dataset_id=dataset_id, prompt_template=prompt_template()
        )
        assert result is not None
        assert result["experiment"] is not None
        assert f"/project/{project().id}/experiments/{experiment_response().id}" in result["link"]
        mock_get_project.assert_called_once_with(id=None, name="awesome-new-project")
        mock_get_experiment.assert_called_once_with(project().id, "test_experiment")
        mock_create_experiment.assert_called_once_with(
            project().id, "awesome-new-experiment 2012-01-01 at 00:00:00.000", mock_get_dataset.return_value
        )
        mock_get_dataset.assert_called_once_with(
            id="00000000-0000-0000-0000-000000000000", name=None, project_id=None, project_name=None
        )
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
        metrics: list[Union[str, LocalMetricConfig]],
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

        for metric, metric_result in zip(metrics, aggregate_results):
            assert hasattr(trace.metrics, metric.name)
            assert getattr(trace.metrics, metric.name) == metric_result

        def check_span(span: Span) -> int:
            span_count = 1
            assert span.dataset_input == "Which continent is Spain in?"
            assert span.dataset_output == "Europe"
            assert span.dataset_metadata == {"meta": "data"}

            for metric, metric_result in zip(metrics, results):
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
    @patch.object(galileo.jobs.Jobs, "create")
    @patch.object(galileo.experiments.Experiments, "create", return_value=experiment_response())
    @patch.object(galileo.experiments.Experiments, "get", return_value=experiment_response())
    @patch.object(galileo.experiments.Projects, "get_with_env_fallbacks", return_value=project())
    def test_run_experiment_w_prompt_template_and_metrics(
        self,
        mock_get_project: Mock,
        mock_get_experiment: Mock,
        mock_create_experiment: Mock,
        mock_create_job: Mock,
        mock_get_dataset: Mock,
        mock_scorers_class: Mock,
        mock_scorer_settings_class: Mock,
        dataset_content: DatasetContent,
    ) -> None:
        mock_create_job.return_value = MagicMock()

        # Setup scorer mocks
        mock_scorers_class.return_value.list.return_value = scorers()
        mock_scorer_settings_class.return_value.create.return_value = None

        dataset_id = str(UUID(int=0))
        run_experiment(
            "test_experiment",
            project="awesome-new-project",
            dataset_id=dataset_id,
            prompt_template=prompt_template(),
            metrics=[GalileoScorers.correctness],
        )

        mock_get_project.assert_called_once_with(id=None, name="awesome-new-project")
        mock_get_experiment.assert_called_once_with(project().id, "test_experiment")
        mock_create_experiment.assert_called_once_with(
            project().id, "awesome-new-experiment 2012-01-01 at 00:00:00.000", mock_get_dataset.return_value
        )
        mock_get_dataset.assert_called_once_with(
            id="00000000-0000-0000-0000-000000000000", name=None, project_id=None, project_name=None
        )
        mock_scorers_class.return_value.list.assert_called_with()
        mock_scorer_settings_class.return_value.create.assert_called_with(
            project_id="00000000-0000-0000-0000-000000000000",
            run_id="00000000-0000-4000-8000-000000000001",
            scorers=[ScorerConfig.from_dict(scorers()[0].to_dict())],
        )

    @travel(datetime(2012, 1, 1), tick=False)
    @patch.object(galileo.datasets.Datasets, "get")
    @patch.object(galileo.jobs.Jobs, "create")
    @patch.object(galileo.experiments.Experiments, "create", return_value=experiment_response())
    @patch.object(galileo.experiments.Experiments, "get", return_value=experiment_response())
    @patch.object(galileo.experiments.Projects, "get_with_env_fallbacks", return_value=project())
    def test_run_experiment_w_prompt_template_and_prompt_settings(
        self,
        mock_get_project: Mock,
        mock_get_experiment: Mock,
        mock_create_experiment: Mock,
        mock_create_job: Mock,
        mock_get_dataset: Mock,
        dataset_content: DatasetContent,
    ) -> None:
        mock_create_job.return_value = MagicMock()

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
        mock_create_experiment.assert_called_once_with(
            project().id, "awesome-new-experiment 2012-01-01 at 00:00:00.000", mock_get_dataset.return_value
        )

        mock_get_dataset.assert_called_once_with(
            id="00000000-0000-0000-0000-000000000000", name=None, project_id=None, project_name=None
        )
        mock_create_job.assert_called_once_with(
            name="playground_run",
            project_id="00000000-0000-0000-0000-000000000000",
            run_id="00000000-0000-4000-8000-000000000001",
            prompt_template_id="00000000-0000-0000-0000-000000000003",
            dataset_id=ANY,
            task_type=TaskType.VALUE_16,
            scorers=None,
            prompt_settings=prompt_run_settings(),
        )

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
        # Setup mock return values
        mock_scorers_instance = mock_scorers_class.return_value
        mock_scorers_instance.list.return_value = [
            ScorerResponse(id="1", name="metric1", scorer_type=ScorerTypes.PRESET, tags=[]),
            ScorerResponse(id="2", name="metric2", scorer_type=ScorerTypes.PRESET, tags=[]),
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

        mock_scorers_instance.list.return_value = mock_scorer_responses

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

    @patch("galileo.jobs.create_job_jobs_post.sync_detailed")
    @patch.object(galileo.datasets.Datasets, "get")
    @patch.object(galileo.experiments.Experiments, "create", return_value=experiment_response())
    @patch.object(galileo.experiments.Experiments, "get", return_value=None)
    @patch.object(galileo.experiments.Projects, "get_with_env_fallbacks", return_value=project())
    def test_run_experiment_job_creation_failure(
        self,
        mock_get_project: Mock,
        mock_get_experiment: Mock,
        mock_create_experiment: Mock,
        mock_get_dataset: Mock,
        mock_create_job_sync: Mock,
        dataset_content: DatasetContent,
    ) -> None:
        mock_create_job_sync.return_value = MagicMock(
            parsed=None, content=b'{"detail":"mocked error"}', status_code=500
        )
        mock_get_dataset_instance = mock_get_dataset.return_value
        mock_get_dataset_instance.get_content = MagicMock(return_value=dataset_content)

        with pytest.raises(GalileoHTTPException) as exc_info:
            run_experiment(
                "test_experiment",
                project="awesome-new-project",
                dataset_id=str(UUID(int=0)),
                prompt_template=prompt_template(),
            )

        assert exc_info.value.message == "Create job failed"
        assert exc_info.value.status_code == 500
        assert exc_info.value.response_text == str(b'{"detail":"mocked error"}')
        mock_get_project.assert_called_once_with(id=None, name="awesome-new-project")
        assert mock_create_experiment.call_args[0][0] == "00000000-0000-0000-0000-000000000000"
        assert mock_create_experiment.call_args[0][1] == "test_experiment"
        mock_create_job_sync.assert_called_once()

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
