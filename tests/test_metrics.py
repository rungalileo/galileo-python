import datetime
import re
from unittest.mock import MagicMock, Mock, patch
from uuid import UUID, uuid4

import pytest

from galileo.metrics import Metrics, create_custom_llm_metric, create_decision_metric, delete_metric, get_metrics
from galileo.resources.models import (
    BucketedMetrics,
    HTTPValidationError,
    LogRecordsMetricsResponse,
    LogRecordsMetricsResponseAggregateMetrics,
    LogRecordsMetricsResponseBucketedMetrics,
    ValidationError,
)
from galileo.resources.models.base_scorer_version_response import BaseScorerVersionResponse
from galileo.resources.models.create_decision_scorer_version_request import CreateDecisionScorerVersionRequest
from galileo.resources.models.create_llm_scorer_version_request import CreateLLMScorerVersionRequest
from galileo.resources.models.create_scorer_request import CreateScorerRequest
from galileo.resources.models.decision_level import DecisionLevel
from galileo.resources.models.input_type_enum import InputTypeEnum
from galileo.resources.models.output_type_enum import OutputTypeEnum
from galileo.resources.models.scorer_defaults import ScorerDefaults
from galileo.resources.models.scorer_response import ScorerResponse
from galileo.resources.models.scorer_types import ScorerTypes
from galileo_core.schemas.logging.step import StepType

FIXED_PROJECT_ID = str(uuid4())


@pytest.fixture
def mock_scorer_response():
    """Mock scorer response for testing."""
    return ScorerResponse(
        id=UUID("12345678-1234-5678-9012-123456789abc"),
        name="test_metric",
        scorer_type=ScorerTypes.LLM,
        description="Test metric description",
        tags=["test", "custom"],
        defaults=ScorerDefaults(model_name="gpt-4.1-mini", num_judges=3),
        created_at="2025-01-01T00:00:00Z",
        created_by=UUID("87654321-4321-8765-2109-987654321cba"),
        updated_at="2025-01-01T00:00:00Z",
    )


@pytest.fixture
def mock_scorer_version_response():
    """Mock scorer version response for testing."""
    mock_response = MagicMock(spec=BaseScorerVersionResponse)
    mock_response.id = UUID("12345678-1234-5678-9012-123456789def")
    mock_response.version = 1
    mock_response.scorer_id = UUID("12345678-1234-5678-9012-123456789abc")
    mock_response.user_prompt = "Test prompt"
    mock_response.scoreable_node_types = [StepType.llm]
    mock_response.cot_enabled = True
    mock_response.model_name = "gpt-4.1-mini"
    mock_response.num_judges = 3
    return mock_response


def _log_records_metrics_response_factory() -> LogRecordsMetricsResponse:
    """Creates a realistic LogRecordsMetricsResponse for testing."""
    now = datetime.datetime.now()
    agg_metrics = LogRecordsMetricsResponseAggregateMetrics()
    agg_metrics["total_cost"] = 15.50
    agg_metrics["total_tokens"] = 2500

    bucketed_metrics_data = LogRecordsMetricsResponseBucketedMetrics()
    bucketed_metrics_data["total_cost"] = [
        BucketedMetrics(start_bucket_time=now, end_bucket_time=now + datetime.timedelta(minutes=5)),
        BucketedMetrics(
            start_bucket_time=now + datetime.timedelta(minutes=5), end_bucket_time=now + datetime.timedelta(minutes=10)
        ),
    ]

    return LogRecordsMetricsResponse(
        aggregate_metrics=agg_metrics, bucketed_metrics=bucketed_metrics_data, group_by_columns=[]
    )


class TestMetrics:
    """Test cases for the Metrics class."""

    @patch("galileo.metrics.create_llm_scorer_version_scorers_scorer_id_version_llm_post")
    @patch("galileo.metrics.create_scorers_post")
    def test_create_custom_llm_metric_success(
        self, mock_create_scorer, mock_create_version, mock_scorer_response, mock_scorer_version_response
    ) -> None:
        """Test successful creation of a custom LLM metric."""
        # Setup mocks
        mock_create_scorer.sync.return_value = mock_scorer_response
        mock_create_version.sync.return_value = mock_scorer_version_response

        metrics = Metrics()

        # Test with default parameters
        result = metrics.create_custom_llm_metric(name="test_metric", user_prompt="Rate the quality of this response")

        # Verify the result
        assert result == mock_scorer_version_response

        # Verify create_scorer was called with correct parameters
        mock_create_scorer.sync.assert_called_once()
        create_scorer_call = mock_create_scorer.sync.call_args
        scorer_request = create_scorer_call.kwargs["body"]

        assert isinstance(scorer_request, CreateScorerRequest)
        assert scorer_request.name == "test_metric"
        assert scorer_request.scorer_type == ScorerTypes.LLM
        assert scorer_request.description == ""
        assert scorer_request.tags == []
        assert scorer_request.defaults.model_name == "gpt-4.1-mini"
        assert scorer_request.defaults.num_judges == 3
        assert scorer_request.output_type == OutputTypeEnum.BOOLEAN
        assert scorer_request.defaults.cot_enabled is True
        assert scorer_request.scoreable_node_types == [StepType.llm]
        assert scorer_request.ground_truth is False

        # Verify create_version was called with correct parameters
        mock_create_version.sync.assert_called_once()
        create_version_call = mock_create_version.sync.call_args
        version_request = create_version_call.kwargs["body"]

        assert isinstance(version_request, CreateLLMScorerVersionRequest)
        assert version_request.user_prompt == "Rate the quality of this response"
        assert create_version_call.kwargs["scorer_id"] == mock_scorer_response.id

    @patch("galileo.metrics.create_llm_scorer_version_scorers_scorer_id_version_llm_post")
    @patch("galileo.metrics.create_scorers_post")
    def test_create_custom_llm_metric_with_custom_parameters(
        self, mock_create_scorer, mock_create_version, mock_scorer_response, mock_scorer_version_response
    ) -> None:
        """Test creation of a custom LLM metric with custom parameters."""
        # Setup mocks
        mock_create_scorer.sync.return_value = mock_scorer_response
        mock_create_version.sync.return_value = mock_scorer_version_response

        metrics = Metrics()

        # Test with custom parameters
        result = metrics.create_custom_llm_metric(
            name="custom_metric",
            user_prompt="Custom prompt for evaluation",
            node_level=StepType.workflow,
            cot_enabled=False,
            model_name="GPT-3.5-turbo",
            num_judges=5,
            description="Custom metric description",
            tags=["custom", "evaluation", "quality"],
            output_type=OutputTypeEnum.CATEGORICAL,
            ground_truth=True,
        )

        # Verify the result
        assert result == mock_scorer_version_response

        # Verify create_scorer was called with correct parameters
        scorer_request = mock_create_scorer.sync.call_args.kwargs["body"]
        assert scorer_request.name == "custom_metric"
        assert scorer_request.description == "Custom metric description"
        assert scorer_request.tags == ["custom", "evaluation", "quality"]
        assert scorer_request.defaults.model_name == "GPT-3.5-turbo"
        assert scorer_request.defaults.num_judges == 5
        assert scorer_request.output_type == OutputTypeEnum.CATEGORICAL
        assert scorer_request.defaults.cot_enabled is False
        assert scorer_request.scoreable_node_types == [StepType.workflow]
        assert scorer_request.ground_truth is True

        # Verify create_version was called with correct parameters
        version_request = mock_create_version.sync.call_args.kwargs["body"]
        assert version_request.user_prompt == "Custom prompt for evaluation"

    @patch("galileo.metrics.create_llm_scorer_version_scorers_scorer_id_version_llm_post")
    @patch("galileo.metrics.create_scorers_post")
    def test_create_custom_llm_metric_scorer_creation_failure(self, mock_create_scorer, mock_create_version) -> None:
        """Test handling of scorer creation failure."""
        # Setup mock to raise exception
        mock_create_scorer.sync.side_effect = Exception("Scorer creation failed")

        metrics = Metrics()

        # Test that exception is propagated
        with pytest.raises(Exception, match="Scorer creation failed"):
            metrics.create_custom_llm_metric(name="test_metric", user_prompt="Test prompt")

        # Verify create_version was not called
        mock_create_version.sync.assert_not_called()

    @patch("galileo.metrics.create_llm_scorer_version_scorers_scorer_id_version_llm_post")
    @patch("galileo.metrics.create_scorers_post")
    def test_create_custom_llm_metric_version_creation_failure(
        self, mock_create_scorer, mock_create_version, mock_scorer_response
    ) -> None:
        """Test handling of version creation failure."""
        # Setup mocks
        mock_create_scorer.sync.return_value = mock_scorer_response
        mock_create_version.sync.side_effect = Exception("Version creation failed")

        metrics = Metrics()

        # Test that exception is propagated
        with pytest.raises(Exception, match="Version creation failed"):
            metrics.create_custom_llm_metric(name="test_metric", user_prompt="Test prompt")

        # Verify create_scorer was called but create_version failed
        mock_create_scorer.sync.assert_called_once()
        mock_create_version.sync.assert_called_once()

    @patch("galileo.metrics.create_llm_scorer_version_scorers_scorer_id_version_llm_post")
    @patch("galileo.metrics.create_scorers_post")
    @patch("galileo.metrics._logger")
    def test_create_custom_llm_metric_logging(
        self, mock_logger, mock_create_scorer, mock_create_version, mock_scorer_response, mock_scorer_version_response
    ) -> None:
        """Test that successful metric creation is logged."""
        # Setup mocks
        mock_create_scorer.sync.return_value = mock_scorer_response
        mock_create_version.sync.return_value = mock_scorer_version_response

        metrics = Metrics()

        # Create metric
        metrics.create_custom_llm_metric(name="test_metric", user_prompt="Test prompt")

        # Verify logging was called
        mock_logger.info.assert_called_once_with("Created custom LLM metric: %s", "test_metric")

    @patch("galileo.metrics.delete_scorer_scorers_scorer_id_delete")
    @patch("galileo.scorers.Scorers.list")
    def test_delete_metric_success(self, mock_list_scorers, mock_delete_scorer, mock_scorer_response) -> None:
        """Test successful deletion of a metric."""
        mock_list_scorers.return_value = [mock_scorer_response]
        metrics = Metrics()
        metrics.delete_metric(name="test_metric")

        mock_list_scorers.assert_called_once_with(name="test_metric")
        mock_delete_scorer.sync.assert_called_once_with(
            scorer_id=mock_scorer_response.id, client=metrics.config.api_client
        )

    @patch("galileo.scorers.Scorers.list")
    def test_delete_metric_not_found(self, mock_list_scorers) -> None:
        """Test deleting a metric that does not exist."""
        mock_list_scorers.return_value = []
        metrics = Metrics()

        with pytest.raises(ValueError, match="Scorer with name test_metric not found."):
            metrics.delete_metric(name="test_metric")

    @patch("galileo.metrics.delete_scorer_scorers_scorer_id_delete")
    @patch("galileo.scorers.Scorers.list")
    def test_delete_metric_api_failure(self, mock_list_scorers, mock_delete_scorer, mock_scorer_response) -> None:
        """Test API failure when deleting a metric."""
        mock_list_scorers.return_value = [mock_scorer_response]
        mock_delete_scorer.sync.return_value = None
        metrics = Metrics()

        with pytest.raises(ValueError, match="Failed to delete metric."):
            metrics.delete_metric(name="test_metric")


class TestPublicFunctions:
    """Test cases for public functions."""

    @patch("galileo.metrics.Metrics")
    def test_create_custom_llm_metric_function(self, mock_metrics_class) -> None:
        """Test the public create_custom_llm_metric function."""
        # Setup mock
        mock_metrics_instance = Mock()
        mock_metrics_class.return_value = mock_metrics_instance
        mock_result = Mock(spec=BaseScorerVersionResponse)
        mock_metrics_instance.create_custom_llm_metric.return_value = mock_result

        # Call the public function
        result = create_custom_llm_metric(
            name="test_metric",
            user_prompt="Test prompt",
            node_level=StepType.workflow,
            cot_enabled=False,
            model_name="GPT-3.5-turbo",
            num_judges=5,
            description="Test description",
            tags=["test"],
            output_type=OutputTypeEnum.CATEGORICAL,
            ground_truth=True,
        )

        # Verify Metrics class was instantiated
        mock_metrics_class.assert_called_once()

        # Verify the method was called with correct parameters
        mock_metrics_instance.create_custom_llm_metric.assert_called_once_with(
            "test_metric",
            "Test prompt",
            StepType.workflow,
            False,
            "GPT-3.5-turbo",
            5,
            "Test description",
            ["test"],
            OutputTypeEnum.CATEGORICAL,
            True,
        )

        # Verify the result is returned
        assert result == mock_result

    @patch("galileo.metrics.Metrics")
    def test_create_custom_llm_metric_function_default_parameters(self, mock_metrics_class) -> None:
        """Test the public function with default parameters."""
        # Setup mock
        mock_metrics_instance = Mock()
        mock_metrics_class.return_value = mock_metrics_instance
        mock_result = Mock(spec=BaseScorerVersionResponse)
        mock_metrics_instance.create_custom_llm_metric.return_value = mock_result

        # Call the public function with minimal parameters
        result = create_custom_llm_metric(name="test_metric", user_prompt="Test prompt")

        # Verify the method was called with default parameters
        mock_metrics_instance.create_custom_llm_metric.assert_called_once_with(
            "test_metric",
            "Test prompt",
            StepType.llm,  # default
            True,  # default
            "gpt-4.1-mini",  # default
            3,  # default
            "",  # default
            [],  # default
            OutputTypeEnum.BOOLEAN,  # default
            False,  # default ground_truth
        )

        # Verify the result is returned
        assert result == mock_result

    @patch("galileo.metrics.Metrics")
    def test_delete_metric_function(self, mock_metrics_class) -> None:
        """Test the public delete_metric function."""
        mock_metrics_instance = Mock()
        mock_metrics_class.return_value = mock_metrics_instance

        delete_metric(name="test_metric")
        mock_metrics_class.assert_called_once()
        mock_metrics_instance.delete_metric.assert_called_once_with("test_metric")


class TestEdgeCases:
    """Test edge cases and boundary conditions."""

    @patch("galileo.metrics.create_llm_scorer_version_scorers_scorer_id_version_llm_post")
    @patch("galileo.metrics.create_scorers_post")
    def test_empty_string_parameters(
        self, mock_create_scorer, mock_create_version, mock_scorer_response, mock_scorer_version_response
    ) -> None:
        """Test creation with empty string parameters."""
        # Setup mocks
        mock_create_scorer.sync.return_value = mock_scorer_response
        mock_create_version.sync.return_value = mock_scorer_version_response

        metrics = Metrics()

        # Test with empty strings
        result = metrics.create_custom_llm_metric(
            name="",  # Empty name
            user_prompt="",  # Empty prompt
            description="",
            tags=[],
        )

        # Verify the result
        assert result == mock_scorer_version_response

        # Verify parameters were passed correctly
        scorer_request = mock_create_scorer.sync.call_args.kwargs["body"]
        assert scorer_request.name == ""
        assert scorer_request.description == ""

        version_request = mock_create_version.sync.call_args.kwargs["body"]
        assert version_request.user_prompt == ""

    @patch("galileo.metrics.create_llm_scorer_version_scorers_scorer_id_version_llm_post")
    @patch("galileo.metrics.create_scorers_post")
    def test_large_num_judges(
        self, mock_create_scorer, mock_create_version, mock_scorer_response, mock_scorer_version_response
    ) -> None:
        """Test creation with large number of judges."""
        # Setup mocks
        mock_create_scorer.sync.return_value = mock_scorer_response
        mock_create_version.sync.return_value = mock_scorer_version_response

        metrics = Metrics()

        # Test with large number of judges
        result = metrics.create_custom_llm_metric(name="test_metric", user_prompt="Test prompt", num_judges=100)

        # Verify the result
        assert result == mock_scorer_version_response

        # Verify num_judges was set correctly
        scorer_request = mock_create_scorer.sync.call_args.kwargs["body"]
        assert scorer_request.defaults.num_judges == 100

        version_request = mock_create_version.sync.call_args.kwargs["body"]
        assert version_request.user_prompt == "Test prompt"

    @patch("galileo.metrics.create_llm_scorer_version_scorers_scorer_id_version_llm_post")
    @patch("galileo.metrics.create_scorers_post")
    def test_long_tag_list(
        self, mock_create_scorer, mock_create_version, mock_scorer_response, mock_scorer_version_response
    ) -> None:
        """Test creation with a long list of tags."""
        # Setup mocks
        mock_create_scorer.sync.return_value = mock_scorer_response
        mock_create_version.sync.return_value = mock_scorer_version_response

        metrics = Metrics()

        # Test with many tags
        long_tag_list = [f"tag_{i}" for i in range(50)]
        result = metrics.create_custom_llm_metric(name="test_metric", user_prompt="Test prompt", tags=long_tag_list)

        # Verify the result
        assert result == mock_scorer_version_response

        # Verify tags were set correctly
        scorer_request = mock_create_scorer.sync.call_args.kwargs["body"]
        assert scorer_request.tags == long_tag_list
        assert len(scorer_request.tags) == 50


class TestGetMetrics:
    @patch("galileo.metrics.query_metrics_projects_project_id_metrics_search_post.sync")
    def test_successful_call(self, mock_api_call):
        mock_response = _log_records_metrics_response_factory()
        mock_api_call.return_value = mock_response

        start_time = datetime.datetime.now()
        end_time = start_time + datetime.timedelta(hours=1)

        response = get_metrics(project_id=FIXED_PROJECT_ID, start_time=start_time, end_time=end_time)

        mock_api_call.assert_called_once()
        assert FIXED_PROJECT_ID in mock_api_call.call_args[1]["project_id"]
        assert response == mock_response

    @patch("galileo.metrics.query_metrics_projects_project_id_metrics_search_post.sync")
    def test_api_failure_raises_value_error(self, mock_api_call):
        mock_api_call.return_value = None

        start_time = datetime.datetime.now()
        end_time = start_time + datetime.timedelta(hours=1)

        with pytest.raises(ValueError, match="Failed to query for metrics."):
            get_metrics(project_id=FIXED_PROJECT_ID, start_time=start_time, end_time=end_time)

        mock_api_call.assert_called_once()

    @patch("galileo.metrics.query_metrics_projects_project_id_metrics_search_post.sync")
    def test_http_validation_error_raises_exception(self, mock_api_call):
        detail = [ValidationError(loc=["body", "project_id"], msg="value is not a valid uuid", type_="type_error.uuid")]
        mock_api_call.return_value = HTTPValidationError(detail=detail)

        start_time = datetime.datetime.now()
        end_time = start_time + datetime.timedelta(hours=1)

        with pytest.raises(ValueError, match=re.escape(str(detail))):
            get_metrics(project_id=FIXED_PROJECT_ID, start_time=start_time, end_time=end_time)

    @patch("galileo.metrics.query_metrics_projects_project_id_metrics_search_post.sync")
    def test_passes_all_parameters_correctly(self, mock_api_call):
        mock_api_call.return_value = _log_records_metrics_response_factory()

        start_time = datetime.datetime.now()
        end_time = start_time + datetime.timedelta(hours=1)
        experiment_id = str(uuid4())
        log_stream_id = "test_stream"
        filters = [Mock()]
        group_by = "some_column"
        interval = 10

        get_metrics(
            project_id=FIXED_PROJECT_ID,
            start_time=start_time,
            end_time=end_time,
            experiment_id=experiment_id,
            log_stream_id=log_stream_id,
            filters=filters,
            group_by=group_by,
            interval=interval,
        )

        mock_api_call.assert_called_once()
        called_kwargs = mock_api_call.call_args[1]
        body = called_kwargs["body"]

        assert called_kwargs["project_id"] == FIXED_PROJECT_ID
        assert body.start_time == start_time
        assert body.end_time == end_time
        assert body.experiment_id == experiment_id
        assert body.log_stream_id == log_stream_id
        assert body.filters == filters
        assert body.group_by == group_by
        assert body.interval == interval


@pytest.fixture
def decision_scorer_response():
    return ScorerResponse(
        id=UUID("12345678-1234-5678-9012-123456789abc"),
        name="tone",
        scorer_type=ScorerTypes.DECISION,
        tags=[],
        created_at="2025-01-01T00:00:00Z",
        updated_at="2025-01-01T00:00:00Z",
    )


@patch("galileo.metrics.delete_scorer_scorers_scorer_id_delete")
@patch("galileo.metrics.create_decision_scorer_version_scorers_scorer_id_version_decision_post")
@patch("galileo.metrics.create_scorers_post")
class TestCreateDecisionMetric:
    def test_boolean_probability_defaults(
        self,
        mock_create_scorer,
        mock_create_version,
        mock_delete,
        decision_scorer_response,
        mock_scorer_version_response,
    ) -> None:
        mock_create_scorer.sync.return_value = decision_scorer_response
        mock_create_version.sync.return_value = mock_scorer_version_response

        result = create_decision_metric(name="tone", question="Is the tone professional?")

        assert result is mock_scorer_version_response
        scorer_request = mock_create_scorer.sync.call_args.kwargs["body"]
        assert isinstance(scorer_request, CreateScorerRequest)
        assert scorer_request.name == "tone"
        assert scorer_request.scorer_type == ScorerTypes.DECISION
        assert scorer_request.output_type == OutputTypeEnum.BOOLEAN_PROBABILITY
        assert scorer_request.scoreable_node_types == [StepType.llm]
        assert scorer_request.ground_truth is False
        assert scorer_request.to_dict().get("input_type") is None
        assert "defaults" not in scorer_request.to_dict()

        version_call = mock_create_version.sync.call_args
        version_request = version_call.kwargs["body"]
        assert isinstance(version_request, CreateDecisionScorerVersionRequest)
        assert version_request.model_name == "jev-1.13.0"
        assert version_request.question == "Is the tone professional?"
        assert version_request.answer_options is None
        assert version_call.kwargs["scorer_id"] == decision_scorer_response.id
        mock_delete.sync.assert_not_called()

    def test_categorical_with_options_and_node_level(
        self,
        mock_create_scorer,
        mock_create_version,
        mock_delete,
        decision_scorer_response,
        mock_scorer_version_response,
    ) -> None:
        mock_create_scorer.sync.return_value = decision_scorer_response
        mock_create_version.sync.return_value = mock_scorer_version_response

        create_decision_metric(
            name="tone",
            question="Which tone?",
            node_level=StepType.trace,
            output_type=OutputTypeEnum.CATEGORICAL,
            answer_options=["a", "b"],
            input_type=InputTypeEnum.TRACE_IO_ONLY,
            description="d",
            tags=["t"],
            ground_truth=True,
        )

        scorer_request = mock_create_scorer.sync.call_args.kwargs["body"]
        assert scorer_request.scoreable_node_types == [StepType.trace]
        assert scorer_request.output_type == OutputTypeEnum.CATEGORICAL
        assert scorer_request.input_type == InputTypeEnum.TRACE_IO_ONLY
        assert scorer_request.description == "d"
        assert scorer_request.tags == ["t"]
        assert scorer_request.ground_truth is True
        version_request = mock_create_version.sync.call_args.kwargs["body"]
        assert version_request.answer_options == ["a", "b"]
        assert version_request.to_dict()["answer_options"] == ["a", "b"]

    def test_discrete_accepts_levels_and_dicts(
        self,
        mock_create_scorer,
        mock_create_version,
        mock_delete,
        decision_scorer_response,
        mock_scorer_version_response,
    ) -> None:
        mock_create_scorer.sync.return_value = decision_scorer_response
        mock_create_version.sync.return_value = mock_scorer_version_response

        create_decision_metric(
            name="quality",
            question="How good?",
            output_type=OutputTypeEnum.DISCRETE,
            answer_options=[DecisionLevel(level=0, label="bad"), {"level": 1, "label": "good", "description": "ok"}],
        )

        version_request = mock_create_version.sync.call_args.kwargs["body"]
        assert version_request.to_dict()["answer_options"] == [
            {"level": 0, "label": "bad"},
            {"level": 1, "label": "good", "description": "ok"},
        ]

    def test_invalid_answer_option_type_raises_before_any_request(
        self, mock_create_scorer, mock_create_version, mock_delete
    ) -> None:
        with pytest.raises(ValueError, match="answer_options"):
            create_decision_metric(
                name="quality",
                question="q",
                output_type=OutputTypeEnum.DISCRETE,
                answer_options=[1, 2],  # type: ignore[list-item]
            )
        mock_create_scorer.sync.assert_not_called()

    def test_version_http_validation_error_deletes_scorer(
        self, mock_create_scorer, mock_create_version, mock_delete, decision_scorer_response
    ) -> None:
        mock_create_scorer.sync.return_value = decision_scorer_response
        mock_create_version.sync.return_value = HTTPValidationError(detail="unknown model jev-9")

        with pytest.raises(ValueError, match="unknown model jev-9"):
            create_decision_metric(name="tone", question="q", model_name="jev-9")

        mock_delete.sync.assert_called_once()
        assert mock_delete.sync.call_args.kwargs["scorer_id"] == decision_scorer_response.id

    def test_version_exception_deletes_scorer_and_reraises(
        self, mock_create_scorer, mock_create_version, mock_delete, decision_scorer_response
    ) -> None:
        mock_create_scorer.sync.return_value = decision_scorer_response
        mock_create_version.sync.side_effect = RuntimeError("boom")

        with pytest.raises(RuntimeError, match="boom"):
            create_decision_metric(name="tone", question="q")

        mock_delete.sync.assert_called_once()

    def test_version_none_response_deletes_scorer(
        self, mock_create_scorer, mock_create_version, mock_delete, decision_scorer_response
    ) -> None:
        mock_create_scorer.sync.return_value = decision_scorer_response
        mock_create_version.sync.return_value = None

        with pytest.raises(ValueError, match="Failed to create decision metric version"):
            create_decision_metric(name="tone", question="q")

        mock_delete.sync.assert_called_once()

    def test_cleanup_failure_does_not_mask_original_error(
        self, mock_create_scorer, mock_create_version, mock_delete, decision_scorer_response
    ) -> None:
        mock_create_scorer.sync.return_value = decision_scorer_response
        mock_create_version.sync.return_value = HTTPValidationError(detail="bad options")
        mock_delete.sync.side_effect = RuntimeError("delete failed")

        with pytest.raises(ValueError, match="bad options"):
            create_decision_metric(name="tone", question="q")

    @pytest.mark.parametrize("scorer_result", [HTTPValidationError(detail="name taken"), None])
    def test_scorer_failure_raises_without_version_call(
        self, mock_create_scorer, mock_create_version, mock_delete, scorer_result
    ) -> None:
        mock_create_scorer.sync.return_value = scorer_result

        with pytest.raises(ValueError):
            create_decision_metric(name="tone", question="q")

        mock_create_version.sync.assert_not_called()
        mock_delete.sync.assert_not_called()
