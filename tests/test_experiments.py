import operator
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
from galileo.schema.metrics import LocalMetricConfig
from galileo.utils.datasets import load_dataset_and_records
from galileo_core.schemas.logging.span import Span, StepWithChildSpans
from galileo_core.schemas.shared.metric import MetricValueType
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
        task_type=TaskType.VALUE_16,
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


class TestExperiments:
    @patch("galileo.experiments.create_experiment_projects_project_id_experiments_post")
    def test_create(self, galileo_resources_api_create_experiment: Mock):
        now = datetime(2020, 1, 1).strftime("%Y-%m-%dT%H:%M:%S.%fZ")
        galileo_resources_api_create_experiment.sync = Mock(
            return_value=ExperimentResponse.from_dict(
                dict(
                    id="test",
                    name="test_experiment",
                    project_id="test",
                    created_at=now,
                    updated_at=now,
                    task_type=TaskType.VALUE_16,
                )
            )
        )
        experiment = Experiments().create(project_id="test", name="test_experiment")
        assert experiment.name == "test_experiment"
        assert experiment.project_id == "test"
        galileo_resources_api_create_experiment.sync.assert_called_once_with(project_id="test", client=ANY, body=ANY)

    @patch("galileo.experiments.create_experiment_projects_project_id_experiments_post")
    def test_create_experiment(self, galileo_resources_api_create_experiment: Mock):
        now = datetime(2020, 1, 1).strftime("%Y-%m-%dT%H:%M:%S.%fZ")
        galileo_resources_api_create_experiment.sync = Mock(
            return_value=ExperimentResponse.from_dict(
                dict(
                    id="test",
                    name="test_experiment",
                    project_id="test",
                    created_at=now,
                    updated_at=now,
                    task_type=TaskType.VALUE_16,
                )
            )
        )

        experiment = create_experiment(project_id=str(UUID(int=0)), experiment_name="test_experiment")
        assert experiment.name == "test_experiment"
        galileo_resources_api_create_experiment.sync.assert_called_once_with(
            project_id=str(UUID(int=0)), client=ANY, body=ANY
        )

    @patch("galileo.experiments.list_experiments_projects_project_id_experiments_get")
    def test_get_experiment(self, list_experiments_mock: Mock):
        list_experiments_mock.sync = Mock(return_value=[experiment_response()])
        experiment = get_experiment(project_id=str(UUID(int=0)), experiment_name=experiment_response().name)
        assert experiment.name == experiment_response().name
        list_experiments_mock.sync.assert_called_once_with(project_id=str(UUID(int=0)), client=ANY)

    @patch("galileo.experiments.list_experiments_projects_project_id_experiments_get")
    def test_get_experiments(self, list_experiments_mock: Mock):
        list_experiments_mock.sync = Mock(return_value=[experiment_response()])
        experiments = get_experiments(project_id=str(UUID(int=0)))
        assert len(experiments) == 1
        assert experiments[0].name == experiment_response().name
        list_experiments_mock.sync.assert_called_once_with(project_id=str(UUID(int=0)), client=ANY)

    @patch("galileo.experiments.list_experiments_projects_project_id_experiments_get")
    def test_get_experiment_not_found(self, list_experiments_mock: Mock):
        list_experiments_mock.sync = Mock(return_value=None)
        experiment = get_experiment(experiment_name=experiment_response().name, project_id=str(UUID(int=0)))
        assert experiment is None
        list_experiments_mock.sync.assert_called_once_with(project_id=str(UUID(int=0)), client=ANY)

    @pytest.mark.parametrize(
        "dataset,dataset_name,dataset_id",
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
    ):
        mock_get_dataset_instance = mock_get_dataset.return_value
        mock_get_dataset_instance.get_content = MagicMock(return_value=dataset_content)
        _, records = load_dataset_and_records(dataset=dataset, dataset_name=dataset_name, dataset_id=dataset_id)
        assert records == [
            DatasetRecord(
                id=test_dataset_row_id, input="Which continent is Spain in?", output="Europe", metadata={"meta": "data"}
            )
        ]
        if dataset_id:
            mock_get_dataset.assert_called_once_with(id=dataset_id, name=None)
        elif dataset_name:
            mock_get_dataset.assert_called_once_with(id=None, name=dataset_name)

    def test_load_dataset_and_records_error(self):
        with pytest.raises(ValueError) as exc_info:
            load_dataset_and_records(dataset=None, dataset_name=None, dataset_id=None)
        assert str(exc_info.value) == "One of dataset, dataset_name, or dataset_id must be provided"

    @travel(datetime(2012, 1, 1))
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
        dataset_content: DatasetContent,
    ):
        mock_create_job.return_value = MagicMock()

        # mock dataset.get_content
        mock_get_dataset_instance = mock_get_dataset.return_value
        mock_get_dataset_instance.get_content = MagicMock(return_value=dataset_content)

        dataset_id = str(UUID(int=0))
        result = run_experiment(
            "test_experiment", project="awesome-new-project", dataset_id=dataset_id, prompt_template=prompt_template()
        )
        assert result is not None
        assert result["experiment"] is not None
        assert f"/project/{project().id}/experiments/{experiment_response().id}" in result["link"]
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

    @staticmethod
    def complex_trace_function(input):
        logger = galileo_context.get_logger_instance()
        output = input + " output"
        logger.add_llm_span(input=input, output=output, model="example")
        return output

    @patch("galileo.logger.LogStreams")
    @patch("galileo.logger.Projects")
    @patch("galileo.logger.GalileoCoreApiClient")
    @patch.object(galileo.datasets.Datasets, "get")
    @patch.object(galileo.experiments.Experiments, "create", return_value=experiment_response())
    @patch.object(galileo.experiments.Experiments, "get", return_value=experiment_response())
    @patch.object(galileo.experiments.Projects, "get", return_value=project())
    @pytest.mark.parametrize(
        ["function", "metrics", "num_spans", "span_type", "results", "aggregate_results"],
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
        mock_get_project: Mock,
        mock_get_experiment: Mock,
        mock_create_experiment: Mock,
        mock_get_dataset: Mock,
        mock_core_api_client: Mock,
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
    ):
        mock_core_api_instance = setup_mock_core_api_client(mock_core_api_client)
        setup_mock_projects_client(mock_projects_client)
        setup_mock_logstreams_client(mock_logstreams_client)

        # mock dataset.get_content
        mock_get_dataset_instance = mock_get_dataset.return_value
        mock_get_dataset_instance.get_content = MagicMock(return_value=dataset_content)

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
        mock_get_project.assert_called_with(name="awesome-new-project")
        mock_get_experiment.assert_called_once_with("00000000-0000-0000-0000-000000000000", "test_experiment")
        mock_create_experiment.assert_called_once_with("00000000-0000-0000-0000-000000000000", ANY)

        mock_get_dataset.assert_called_once_with(id="00000000-0000-4000-8000-000000000000", name=None)
        mock_get_dataset_instance.get_content.assert_called()

        # check galileo_logger
        payload = mock_core_api_instance.ingest_traces_sync.call_args[0][0]

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

    @travel(datetime(2012, 1, 1))
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
        dataset_content: DatasetContent,
    ):
        mock_create_job.return_value = MagicMock()

        # mock dataset.get_content
        mock_get_dataset_instance = mock_get_dataset.return_value
        mock_get_dataset_instance.get_content = MagicMock(return_value=dataset_content)

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

    @travel(datetime(2012, 1, 1))
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
        dataset_content: DatasetContent,
    ):
        mock_create_job.return_value = MagicMock()

        # mock dataset.get_content
        mock_get_dataset_instance = mock_get_dataset.return_value
        mock_get_dataset_instance.get_content = MagicMock(return_value=dataset_content)

        dataset_id = str(UUID(int=0))
        run_experiment(
            "test_experiment",
            project="awesome-new-project",
            dataset_id=dataset_id,
            prompt_template=prompt_template(),
            prompt_settings=prompt_run_settings(),
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
            prompt_settings=prompt_run_settings(),
        )

    @travel(datetime(2012, 1, 1))
    @patch("galileo.logger.LogStreams")
    @patch("galileo.logger.Projects")
    @patch("galileo.logger.GalileoCoreApiClient")
    @patch.object(galileo.datasets.Datasets, "get")
    @patch.object(galileo.jobs.Jobs, "create")
    @patch.object(galileo.experiments.Experiments, "create", return_value=experiment_response())
    @patch.object(galileo.experiments.Experiments, "get", return_value=experiment_response())
    @patch.object(galileo.experiments.Projects, "get", return_value=project())
    def test_run_experiment_with_runner_and_dataset(
        self,
        mock_get_project: Mock,
        mock_get_experiment: Mock,
        mock_create_experiment: Mock,
        mock_create_job: Mock,
        mock_get_dataset: Mock,
        mock_core_api_client: Mock,
        mock_projects_client: Mock,
        mock_logstreams_client: Mock,
        reset_context,
        dataset_content_with_question: DatasetContent,
    ):
        mock_core_api_instance = setup_mock_core_api_client(mock_core_api_client)
        setup_mock_projects_client(mock_projects_client)
        setup_mock_logstreams_client(mock_logstreams_client)

        mock_create_job.return_value = MagicMock()

        # mock dataset.get_content
        mock_get_dataset_instance = mock_get_dataset.return_value
        mock_get_dataset_instance.get_content = MagicMock(return_value=dataset_content_with_question)

        def runner(input):
            # emulate using input
            return f"Say hello: {input['question']}"

        result = run_experiment(
            "test_experiment", project="awesome-new-project", dataset_id=str(UUID(int=0)), function=runner
        )
        assert result is not None
        assert result["experiment"] is not None

        mock_get_project.assert_called_with(name="awesome-new-project")
        mock_get_experiment.assert_called_once_with("00000000-0000-0000-0000-000000000000", "test_experiment")
        mock_create_experiment.assert_called_once_with("00000000-0000-0000-0000-000000000000", ANY)

        mock_get_dataset.assert_called_once_with(id="00000000-0000-0000-0000-000000000000", name=None)
        mock_get_dataset_instance.get_content.assert_called()

        # check galileo_logger
        payload = mock_core_api_instance.ingest_traces_sync.call_args[0][0]
        assert len(payload.traces) == 1
        assert (
            payload.traces[0].input == '{"input": {"question": "Which continent is Spain in?", "expected": "Europe"}}'
        )
        assert payload.traces[0].output == "Say hello: Which continent is Spain in?"

    @patch.object(galileo.datasets.Datasets, "get")
    def test_run_experiment_with_prompt_template_and_function(
        self, mock_get_dataset: Mock, dataset_content: DatasetContent
    ):
        # mock dataset.get_content
        mock_get_dataset_instance = mock_get_dataset.return_value
        mock_get_dataset_instance.get_content = MagicMock(return_value=dataset_content)

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

    def test_run_experiment_with_prompt_template_and_local_dataset(self, local_dataset: list[dict[str, str]]):
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

    @patch("galileo.logger.Projects")
    @patch.object(galileo.datasets.Datasets, "get")
    @patch.object(galileo.experiments.Experiments, "create", return_value=experiment_response())
    @patch.object(galileo.experiments.Experiments, "get", return_value=experiment_response())
    @patch.object(galileo.experiments.Projects, "get", return_value=project())
    def test_run_experiment_with_local_scorers_and_prompt_template(
        self,
        mock_get_project: Mock,
        mock_get_experiment: Mock,
        mock_create_experiment: Mock,
        mock_get_dataset: Mock,
        mock_projects_client: Mock,
        dataset_content_with_question: DatasetContent,
    ):
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

    @patch("galileo.experiments.Scorers")
    @patch("galileo.experiments.ScorerSettings")
    def test_create_scorer_configs(self, mock_scorer_settings, mock_scorers):
        # Setup mock return values
        mock_scorers_instance = mock_scorers.return_value
        mock_scorers_instance.list.return_value = [
            ScorerConfig(id="1", name="metric1", scorer_type=ScorerTypes.PRESET),
            ScorerConfig(id="2", name="metric2", scorer_type=ScorerTypes.PRESET),
        ]

        # Test valid metrics
        scorers, local_scorers = Experiments.create_metric_configs(
            "project_id", "experiment_id", ["metric1", LocalMetricConfig(name="length", scorer_fn=lambda x: len(x))]
        )
        assert len(scorers) == 1  # Should return one valid scorer
        assert len(local_scorers) == 1  # Should return one local scorer

        # Test unknown metrics
        with pytest.raises(ValueError):
            Experiments.create_metric_configs("project_id", "experiment_id", ["unknown_metric"])
