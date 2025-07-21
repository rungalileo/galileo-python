from unittest.mock import MagicMock, Mock, patch
from uuid import UUID

import pytest

from galileo.metrics import Metrics, create_custom_llm_metric
from galileo.resources.models.base_scorer_version_response import BaseScorerVersionResponse
from galileo.resources.models.create_llm_scorer_version_request import CreateLLMScorerVersionRequest
from galileo.resources.models.create_scorer_request import CreateScorerRequest
from galileo.resources.models.scorer_defaults import ScorerDefaults
from galileo.resources.models.scorer_response import ScorerResponse
from galileo.resources.models.scorer_types import ScorerTypes
from galileo_core.schemas.logging.step import StepType


@pytest.fixture
def mock_scorer_response():
    """Mock scorer response for testing."""
    return ScorerResponse(
        id=UUID("12345678-1234-5678-9012-123456789abc"),
        name="test_metric",
        scorer_type=ScorerTypes.LLM,
        description="Test metric description",
        tags=["test", "custom"],
        defaults=ScorerDefaults(model_name="GPT-4o", num_judges=3),
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
    mock_response.model_name = "GPT-4o"
    mock_response.num_judges = 3
    return mock_response


class TestMetrics:
    """Test cases for the Metrics class."""

    @patch("galileo.metrics.create_llm_scorer_version_scorers_scorer_id_version_llm_post")
    @patch("galileo.metrics.create_scorers_post")
    def test_create_custom_llm_metric_success(
        self, mock_create_scorer, mock_create_version, mock_scorer_response, mock_scorer_version_response
    ):
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
        assert scorer_request.defaults.model_name == "GPT-4o"
        assert scorer_request.defaults.num_judges == 3

        # Verify create_version was called with correct parameters
        mock_create_version.sync.assert_called_once()
        create_version_call = mock_create_version.sync.call_args
        version_request = create_version_call.kwargs["body"]

        assert isinstance(version_request, CreateLLMScorerVersionRequest)
        assert version_request.user_prompt == "Rate the quality of this response"
        assert version_request.scoreable_node_types == [StepType.llm]
        assert version_request.cot_enabled is True
        assert version_request.model_name == "GPT-4o"
        assert version_request.num_judges == 3
        assert create_version_call.kwargs["scorer_id"] == mock_scorer_response.id

    @patch("galileo.metrics.create_llm_scorer_version_scorers_scorer_id_version_llm_post")
    @patch("galileo.metrics.create_scorers_post")
    def test_create_custom_llm_metric_with_custom_parameters(
        self, mock_create_scorer, mock_create_version, mock_scorer_response, mock_scorer_version_response
    ):
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

        # Verify create_version was called with correct parameters
        version_request = mock_create_version.sync.call_args.kwargs["body"]
        assert version_request.user_prompt == "Custom prompt for evaluation"
        assert version_request.scoreable_node_types == [StepType.workflow]
        assert version_request.cot_enabled is False
        assert version_request.model_name == "GPT-3.5-turbo"
        assert version_request.num_judges == 5

    @patch("galileo.metrics.create_llm_scorer_version_scorers_scorer_id_version_llm_post")
    @patch("galileo.metrics.create_scorers_post")
    def test_create_custom_llm_metric_scorer_creation_failure(self, mock_create_scorer, mock_create_version):
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
    ):
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
    ):
        """Test that successful metric creation is logged."""
        # Setup mocks
        mock_create_scorer.sync.return_value = mock_scorer_response
        mock_create_version.sync.return_value = mock_scorer_version_response

        metrics = Metrics()

        # Create metric
        metrics.create_custom_llm_metric(name="test_metric", user_prompt="Test prompt")

        # Verify logging was called
        mock_logger.info.assert_called_once_with("Created custom LLM metric: %s", "test_metric")


class TestPublicFunctions:
    """Test cases for public functions."""

    @patch("galileo.metrics.Metrics")
    def test_create_custom_llm_metric_function(self, mock_metrics_class):
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
        )

        # Verify Metrics class was instantiated
        mock_metrics_class.assert_called_once()

        # Verify the method was called with correct parameters
        mock_metrics_instance.create_custom_llm_metric.assert_called_once_with(
            "test_metric", "Test prompt", StepType.workflow, False, "GPT-3.5-turbo", 5, "Test description", ["test"]
        )

        # Verify the result is returned
        assert result == mock_result

    @patch("galileo.metrics.Metrics")
    def test_create_custom_llm_metric_function_default_parameters(self, mock_metrics_class):
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
            "GPT-4o",  # default
            3,  # default
            "",  # default
            [],  # default
        )

        # Verify the result is returned
        assert result == mock_result


class TestEdgeCases:
    """Test edge cases and boundary conditions."""

    @patch("galileo.metrics.create_llm_scorer_version_scorers_scorer_id_version_llm_post")
    @patch("galileo.metrics.create_scorers_post")
    def test_empty_string_parameters(
        self, mock_create_scorer, mock_create_version, mock_scorer_response, mock_scorer_version_response
    ):
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
    ):
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
        assert version_request.num_judges == 100

    @patch("galileo.metrics.create_llm_scorer_version_scorers_scorer_id_version_llm_post")
    @patch("galileo.metrics.create_scorers_post")
    def test_long_tag_list(
        self, mock_create_scorer, mock_create_version, mock_scorer_response, mock_scorer_version_response
    ):
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
