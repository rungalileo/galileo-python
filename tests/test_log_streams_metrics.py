import os
from unittest.mock import ANY, patch
from uuid import UUID

import pytest

from galileo.log_streams import LogStream, LogStreams, enable_metrics
from galileo.projects import Project
from galileo.resources.models import ProjectCreateResponse, ScorerResponse, ScorerTypes
from galileo.resources.models.log_stream_response import LogStreamResponse
from galileo.schema.metrics import GalileoScorers, LocalMetricConfig


@pytest.fixture(autouse=True)
def reset_env_vars():
    """Reset environment variables before each test."""
    os.environ.pop("GALILEO_PROJECT", None)
    os.environ.pop("GALILEO_PROJECT_ID", None)
    os.environ.pop("GALILEO_LOG_STREAM", None)
    os.environ.pop("GALILEO_LOG_STREAM_ID", None)


@pytest.fixture
def mock_project():
    """Mock project object."""
    return Project(
        project=ProjectCreateResponse(
            id=UUID(int=1), name="Test Project", created_at="2023-01-01T00:00:00Z", updated_at="2023-01-01T00:00:00Z"
        )
    )


@pytest.fixture
def mock_log_stream():
    """Mock log stream object."""
    return LogStream(
        log_stream=LogStreamResponse(
            id="log-stream-123",
            name="Test Log Stream",
            project_id=str(UUID(int=1)),
            created_at="2023-01-01T00:00:00Z",
            updated_at="2023-01-01T00:00:00Z",
            created_by="test-user",
        )
    )


@pytest.fixture
def mock_scorers():
    """Mock scorer responses."""
    return [
        ScorerResponse(
            id=UUID(int=100),
            name="correctness",
            scorer_type=ScorerTypes.LLM,
            description="Test correctness scorer",
            tags=[],
        ),
        ScorerResponse(
            id=UUID(int=101),
            name="completeness",
            scorer_type=ScorerTypes.LLM,
            description="Test completeness scorer",
            tags=[],
        ),
    ]


class TestLogStreamMetrics:
    """Test cases for log stream metrics functionality."""

    @patch("galileo.utils.metrics.Scorers")
    @patch("galileo.utils.metrics.ScorerSettings")
    def test_create_metric_configs_with_builtin_metrics(
        self, mock_scorer_settings_class, mock_scorers_class, mock_scorers
    ):
        """Test create_metric_configs with built-in Galileo scorers."""
        # Setup mocks
        mock_scorers_class.return_value.list.return_value = mock_scorers
        mock_scorer_settings_class.return_value.create.return_value = None

        # Test with built-in metrics
        from galileo.utils.metrics import create_metric_configs

        scorers, local_metrics = create_metric_configs(
            "project-123", "logstream-456", [GalileoScorers.correctness, "completeness"]
        )

        # Verify scorers list was called
        mock_scorers_class.return_value.list.assert_called_once()

        # Verify scorer settings creation was called
        mock_scorer_settings_class.return_value.create.assert_called_once_with(
            project_id="project-123", run_id="logstream-456", scorers=ANY
        )

        # Verify no local metrics
        assert len(local_metrics) == 0

    @patch("galileo.utils.metrics.Scorers")
    @patch("galileo.utils.metrics.ScorerSettings")
    def test_create_metric_configs_with_local_metrics(self, mock_scorer_settings, mock_scorers_class):
        """Test create_metric_configs with local metric configs."""
        # Setup mocks
        mock_scorers_class.return_value.list.return_value = []

        # Define local metric
        def custom_scorer(trace_or_span):
            return 0.85

        local_metric = LocalMetricConfig(name="custom_metric", scorer_fn=custom_scorer)

        # Test with local metrics only
        from galileo.utils.metrics import create_metric_configs

        scorers, local_metrics = create_metric_configs("project-123", "logstream-456", [local_metric])

        # Verify no scorer settings creation for local metrics
        mock_scorer_settings.return_value.create.assert_not_called()

        # Verify local metric is returned
        assert len(local_metrics) == 1
        assert local_metrics[0].name == "custom_metric"
        assert len(scorers) == 0

    @patch("galileo.utils.metrics.Scorers")
    @patch("galileo.utils.metrics.ScorerSettings")
    def test_create_metric_configs_with_mixed_metrics(
        self, mock_scorer_settings_class, mock_scorers_class, mock_scorers
    ):
        """Test create_metric_configs with mixed metric types."""
        # Setup mocks
        mock_scorers_class.return_value.list.return_value = mock_scorers
        mock_scorer_settings_class.return_value.create.return_value = None

        def custom_scorer(trace_or_span):
            return 0.9

        local_metric = LocalMetricConfig(name="local_metric", scorer_fn=custom_scorer)

        # Test with mixed metrics (only valid ones to avoid decorator error handling)
        from galileo.utils.metrics import create_metric_configs

        scorers, local_metrics = create_metric_configs(
            "project-123", "logstream-456", [GalileoScorers.correctness, local_metric]
        )

        # Verify local metrics
        assert len(local_metrics) == 1
        assert local_metrics[0].name == "local_metric"

        # Verify scorer settings was called
        mock_scorer_settings_class.return_value.create.assert_called_once()

    def test_log_stream_enable_metrics_instance_method(self, mock_log_stream):
        """Test LogStream instance enable_metrics method."""
        with patch("galileo.utils.metrics.create_metric_configs") as mock_create_configs:
            mock_create_configs.return_value = ([], [])

            # Test instance method
            local_metrics = mock_log_stream.enable_metrics(["correctness"])

            # Verify create_metric_configs was called with correct parameters
            mock_create_configs.assert_called_once_with(mock_log_stream.project_id, mock_log_stream.id, ["correctness"])

            # Verify return value is just local metrics
            assert local_metrics == []

    def test_log_stream_enable_metrics_missing_ids(self):
        """Test LogStream enable_metrics raises error when IDs are missing."""
        log_stream = LogStream()  # Empty log stream without IDs

        with pytest.raises(ValueError, match="Log stream must have id and project_id to enable metrics"):
            log_stream.enable_metrics(["correctness"])

    @patch("galileo.log_streams.Projects")
    @patch.object(LogStreams, "get")
    @patch("galileo.utils.metrics.create_metric_configs")
    def test_logstreams_enable_metrics_with_explicit_params(
        self, mock_create_configs, mock_get, mock_projects_class, mock_project, mock_log_stream
    ):
        """Test LogStreams.enable_metrics with explicit parameters."""
        # Setup mocks
        mock_projects_instance = mock_projects_class.return_value
        mock_projects_instance.get_with_env_fallbacks.return_value = mock_project
        mock_get.return_value = mock_log_stream
        mock_create_configs.return_value = ([], [])

        # Test with explicit parameters
        log_streams = LogStreams()
        local_metrics = log_streams.enable_metrics(
            log_stream_name="Test Log Stream", project_name="Test Project", metrics=["correctness"]
        )

        # Verify project lookup
        mock_projects_instance.get_with_env_fallbacks.assert_called_once_with(name="Test Project")

        # Verify log stream lookup
        mock_get.assert_called_once_with(name="Test Log Stream", project_name=mock_project.name)

        # Verify metric config creation
        mock_create_configs.assert_called_once_with(mock_project.id, mock_log_stream.id, ["correctness"])

        # Verify return value is just local metrics
        assert local_metrics == []

    @patch("galileo.log_streams.Projects")
    @patch.object(LogStreams, "get")
    @patch("galileo.utils.metrics.create_metric_configs")
    def test_logstreams_enable_metrics_with_env_vars(
        self, mock_create_configs, mock_get, mock_projects_class, mock_project, mock_log_stream
    ):
        """Test LogStreams.enable_metrics with environment variables."""
        # Set environment variables
        os.environ["GALILEO_PROJECT"] = "Test Project"
        os.environ["GALILEO_LOG_STREAM"] = "Test Log Stream"

        # Setup mocks
        mock_projects_instance = mock_projects_class.return_value
        mock_projects_instance.get_with_env_fallbacks.return_value = mock_project
        mock_get.return_value = mock_log_stream
        mock_create_configs.return_value = ([], [])

        # Test with environment variables
        log_streams = LogStreams()
        local_metrics = log_streams.enable_metrics(metrics=["correctness"])

        # Verify project lookup used env var
        mock_projects_instance.get_with_env_fallbacks.assert_called_once_with(name="Test Project")

        # Verify log stream lookup used env var
        mock_get.assert_called_once_with(name="Test Log Stream", project_name=mock_project.name)

        # Verify return value is just local metrics
        assert local_metrics == []

    @patch("galileo.log_streams.Projects")
    def test_logstreams_enable_metrics_project_not_found(self, mock_projects_class):
        """Test LogStreams.enable_metrics handles error when project not found."""
        # Setup mock to return None
        mock_projects_instance = mock_projects_class.return_value
        mock_projects_instance.get_with_env_fallbacks.return_value = None

        # Test with non-existent project - expect None due to error decorator
        log_streams = LogStreams()
        result = log_streams.enable_metrics(
            project_name="Nonexistent Project", log_stream_name="Test Log Stream", metrics=["correctness"]
        )

        # Verify None result due to error handling
        assert result is None

    @patch("galileo.log_streams.Projects")
    @patch.object(LogStreams, "get")
    def test_logstreams_enable_metrics_logstream_not_found(self, mock_get, mock_projects_class, mock_project):
        """Test LogStreams.enable_metrics handles error when log stream not found."""
        # Setup mocks
        mock_projects_instance = mock_projects_class.return_value
        mock_projects_instance.get_with_env_fallbacks.return_value = mock_project
        mock_get.return_value = None  # Log stream not found

        # Test with non-existent log stream - expect None due to error decorator
        log_streams = LogStreams()
        result = log_streams.enable_metrics(
            project_name="Test Project", log_stream_name="Nonexistent Stream", metrics=["correctness"]
        )

        # Verify None result due to error handling
        assert result is None

    @patch.object(LogStreams, "enable_metrics")
    def test_enable_metrics_convenience_function_explicit(self, mock_enable_metrics):
        """Test enable_metrics convenience function with explicit parameters."""
        mock_enable_metrics.return_value = []

        # Test convenience function with explicit parameters
        local_metrics = enable_metrics(
            log_stream_name="Test Stream", project_name="Test Project", metrics=["correctness"]
        )

        # Verify it calls the instance method
        mock_enable_metrics.assert_called_once_with(
            log_stream_name="Test Stream", project_name="Test Project", metrics=["correctness"]
        )

        # Verify return value is just local metrics
        assert local_metrics == []

    @patch.object(LogStreams, "enable_metrics")
    def test_enable_metrics_convenience_function_env_only(self, mock_enable_metrics):
        """Test enable_metrics convenience function with environment variables only."""
        mock_enable_metrics.return_value = []

        # Test environment-only function (no explicit parameters)
        local_metrics = enable_metrics(metrics=["correctness"])

        # Verify it calls the instance method with no explicit params
        mock_enable_metrics.assert_called_once_with(log_stream_name=None, project_name=None, metrics=["correctness"])

        # Verify return value is just local metrics
        assert local_metrics == []

    @patch("galileo.log_streams.Projects")
    @patch.object(LogStreams, "get")
    @patch("galileo.utils.metrics.create_metric_configs")
    def test_enable_metrics_with_env_vars_integration(
        self, mock_create_configs, mock_get, mock_projects_class, mock_project, mock_log_stream
    ):
        """Test enable_metrics function with environment variables (integration test)."""
        # Set environment variables
        os.environ["GALILEO_PROJECT"] = "Integration Project"
        os.environ["GALILEO_LOG_STREAM"] = "Integration Stream"

        # Setup mocks
        mock_projects_instance = mock_projects_class.return_value
        mock_projects_instance.get_with_env_fallbacks.return_value = mock_project
        mock_get.return_value = mock_log_stream
        mock_create_configs.return_value = ([], [])

        # Test the full integration
        local_metrics = enable_metrics(metrics=["correctness", "completeness"])

        # Verify the entire chain was called correctly
        mock_projects_instance.get_with_env_fallbacks.assert_called_once_with(name="Integration Project")
        mock_get.assert_called_once_with(name="Integration Stream", project_name=mock_project.name)
        mock_create_configs.assert_called_once_with(
            mock_project.id, mock_log_stream.id, ["correctness", "completeness"]
        )

        # Verify return value is just local metrics
        assert local_metrics == []

    def test_enable_metrics_missing_env_vars(self):
        """Test enable_metrics handles error when environment variables are missing."""
        # Don't set any environment variables
        with patch("galileo.log_streams.Projects") as mock_projects_class:
            mock_projects_instance = mock_projects_class.return_value
            mock_projects_instance.get_with_env_fallbacks.return_value = None

            # Expect None due to error decorator
            result = enable_metrics(metrics=["correctness"])

            # Verify None result due to error handling
            assert result is None
