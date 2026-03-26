import os
import warnings
from unittest.mock import ANY, patch
from uuid import UUID

import pytest

from galileo.log_streams import LogStream, LogStreams, enable_metrics
from galileo.projects import Project
from galileo.resources.models import ProjectCreateResponse, ScorerResponse, ScorerTypes
from galileo.resources.models.log_stream_response import LogStreamResponse
from galileo.schema.metrics import GalileoMetricNames, GalileoMetrics, LocalMetricConfig, Metric
from galileo.utils.metrics import create_metric_configs


@pytest.fixture(autouse=True)
def reset_env_vars():
    """Reset environment variables before each test and restore after."""
    saved = {
        k: os.environ.pop(k, None)
        for k in ("GALILEO_PROJECT", "GALILEO_PROJECT_ID", "GALILEO_LOG_STREAM", "GALILEO_LOG_STREAM_ID")
    }
    yield
    for k, v in saved.items():
        if v is not None:
            os.environ[k] = v
        else:
            os.environ.pop(k, None)


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
    ) -> None:
        """Test create_metric_configs with built-in Galileo scorers."""
        # Setup mocks — new code uses list_by_labels instead of list
        mock_scorers_class.return_value.list_by_labels.return_value = mock_scorers
        mock_scorer_settings_class.return_value.create.return_value = None

        # Test with built-in metrics
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", DeprecationWarning)
            scorers, local_metrics = create_metric_configs(
                "project-123", "logstream-456", [GalileoMetrics.correctness, "completeness"]
            )

        # Verify scorers list_by_labels was called
        mock_scorers_class.return_value.list_by_labels.assert_called_once()

        # Verify scorer settings creation was called
        mock_scorer_settings_class.return_value.create.assert_called_once_with(
            project_id="project-123", run_id="logstream-456", scorers=ANY
        )

        # Verify no local metrics
        assert len(local_metrics) == 0

    @patch("galileo.utils.metrics.Scorers")
    @patch("galileo.utils.metrics.ScorerSettings")
    def test_create_metric_configs_with_local_metrics(self, mock_scorer_settings, mock_scorers_class) -> None:
        """Test create_metric_configs with local metric configs."""
        # Setup mocks
        mock_scorers_class.return_value.list.return_value = []

        # Define local metric
        def custom_scorer(trace_or_span) -> float:
            return 0.85

        local_metric = LocalMetricConfig(name="custom_metric", scorer_fn=custom_scorer)

        # Test with local metrics only
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
    ) -> None:
        """Test create_metric_configs with mixed metric types."""
        # Setup mocks — new code uses list_by_labels instead of list
        mock_scorers_class.return_value.list_by_labels.return_value = mock_scorers
        mock_scorer_settings_class.return_value.create.return_value = None

        def custom_scorer(trace_or_span) -> float:
            return 0.9

        local_metric = LocalMetricConfig(name="local_metric", scorer_fn=custom_scorer)

        # Test with mixed metrics (only valid ones to avoid decorator error handling)
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", DeprecationWarning)
            scorers, local_metrics = create_metric_configs(
                "project-123", "logstream-456", [GalileoMetrics.correctness, local_metric]
            )

        # Verify local metrics
        assert len(local_metrics) == 1
        assert local_metrics[0].name == "local_metric"

        # Verify scorer settings was called
        mock_scorer_settings_class.return_value.create.assert_called_once()

    def test_log_stream_enable_metrics_instance_method(self, mock_log_stream) -> None:
        """Test LogStream instance enable_metrics method."""
        with patch("galileo.log_streams.create_metric_configs") as mock_create_configs:
            mock_create_configs.return_value = ([], [])

            # Test instance method
            local_metrics = mock_log_stream.enable_metrics(["correctness"])

            # Verify create_metric_configs was called with correct parameters
            mock_create_configs.assert_called_once_with(mock_log_stream.project_id, mock_log_stream.id, ["correctness"])

            # Verify return value is just local metrics
            assert local_metrics == []

    def test_log_stream_enable_metrics_missing_ids(self) -> None:
        """Test LogStream enable_metrics raises error when IDs are missing."""
        log_stream = LogStream()  # Empty log stream without IDs

        with pytest.raises(ValueError, match="Log stream must have id and project_id to enable metrics"):
            log_stream.enable_metrics(["correctness"])

    @patch("galileo.log_streams.Projects")
    @patch.object(LogStreams, "get")
    @patch("galileo.log_streams.create_metric_configs")
    def test_logstreams_enable_metrics_with_explicit_params(
        self, mock_create_configs, mock_get, mock_projects_class, mock_project, mock_log_stream
    ) -> None:
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

    @patch.object(LogStreams, "get")
    @patch("galileo.log_streams.create_metric_configs")
    @patch("galileo.projects.Projects.get_with_env_fallbacks")
    def test_logstreams_enable_metrics_gets_project_correctly(
        self, mock_get_with_env_fallbacks, mock_create_configs, mock_get, mock_log_stream, mock_project
    ) -> None:
        """Test LogStreams.enable_metrics with explicit parameters."""
        # Setup mocks
        mock_get.return_value = mock_log_stream
        mock_create_configs.return_value = ([], [])
        mock_get_with_env_fallbacks.return_value = mock_project

        # Test with explicit parameters
        log_streams = LogStreams()
        local_metrics = log_streams.enable_metrics(
            log_stream_name="Test Log Stream", project_name="Test Project", metrics=["correctness"]
        )

        # Verify log stream lookup
        mock_get.assert_called_once_with(name="Test Log Stream", project_name=mock_project.name)

        # Verify metric config creation
        mock_create_configs.assert_called_once_with(mock_project.id, mock_log_stream.id, ["correctness"])

        # Verify return value is just local metrics
        assert local_metrics == []

    @patch("galileo.log_streams.Projects")
    @patch.object(LogStreams, "get")
    @patch("galileo.log_streams.create_metric_configs")
    def test_logstreams_enable_metrics_with_env_vars(
        self, mock_create_configs, mock_get, mock_projects_class, mock_project, mock_log_stream
    ) -> None:
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
    def test_logstreams_enable_metrics_project_not_found(self, mock_projects_class) -> None:
        """Test LogStreams.enable_metrics raises ValueError when project not found."""
        # Setup mock to return None
        mock_projects_instance = mock_projects_class.return_value
        mock_projects_instance.get_with_env_fallbacks.return_value = None

        # Test with non-existent project - expect ValueError
        log_streams = LogStreams()
        with pytest.raises(ValueError) as exc_info:
            log_streams.enable_metrics(
                project_name="Nonexistent Project", log_stream_name="Test Log Stream", metrics=["correctness"]
            )

        assert "Project 'Nonexistent Project' not found" in str(exc_info.value)

    @patch("galileo.log_streams.Projects")
    @patch.object(LogStreams, "get")
    def test_logstreams_enable_metrics_logstream_not_found(self, mock_get, mock_projects_class, mock_project) -> None:
        """Test LogStreams.enable_metrics raises ValueError when log stream not found."""
        # Setup mocks
        mock_projects_instance = mock_projects_class.return_value
        mock_projects_instance.get_with_env_fallbacks.return_value = mock_project
        mock_get.return_value = None  # Log stream not found

        # Test with non-existent log stream - expect ValueError
        log_streams = LogStreams()
        with pytest.raises(ValueError) as exc_info:
            log_streams.enable_metrics(
                project_name="Test Project", log_stream_name="Nonexistent Stream", metrics=["correctness"]
            )

        assert "Log stream 'Nonexistent Stream' not found" in str(exc_info.value)

    @patch.object(LogStreams, "enable_metrics")
    def test_enable_metrics_convenience_function_explicit(self, mock_enable_metrics) -> None:
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
    def test_enable_metrics_convenience_function_env_only(self, mock_enable_metrics) -> None:
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
    @patch("galileo.log_streams.create_metric_configs")
    def test_enable_metrics_with_env_vars_integration(
        self, mock_create_configs, mock_get, mock_projects_class, mock_project, mock_log_stream
    ) -> None:
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

    def test_enable_metrics_missing_env_vars(self) -> None:
        """Test enable_metrics raises ValueError when environment variables are missing."""
        # Don't set any environment variables
        with patch("galileo.log_streams.Projects") as mock_projects_class:
            mock_projects_instance = mock_projects_class.return_value
            mock_projects_instance.get_with_env_fallbacks.return_value = None

            # Expect ValueError since project is not found
            with pytest.raises(ValueError) as exc_info:
                enable_metrics(metrics=["correctness"])

            assert "Project" in str(exc_info.value)
            assert "not found" in str(exc_info.value)


class TestCreateMetricConfigsNewTypes:
    """Tests for the updated create_metric_configs with GalileoMetricNames, UUID, and deprecation support."""

    @pytest.fixture
    def mock_scorers_with_labels(self):
        """Mock scorer responses with labels set (simulating preset scorers)."""
        return [
            ScorerResponse(
                id=UUID(int=100),
                name="correctness",
                label="Correctness",
                scorer_type=ScorerTypes.LLM,
                description="Test correctness scorer",
                tags=[],
            ),
            ScorerResponse(
                id=UUID(int=101),
                name="context_adherence",
                label="Context Adherence",
                scorer_type=ScorerTypes.LLM,
                description="Test context adherence scorer",
                tags=[],
            ),
        ]

    @patch("galileo.utils.metrics.Scorers")
    @patch("galileo.utils.metrics.ScorerSettings")
    def test_galileo_metric_names_routes_through_list_by_labels(
        self, mock_settings_class, mock_scorers_class, mock_scorers_with_labels
    ) -> None:
        # Given: scorers are resolved via list_by_labels
        mock_scorers_class.return_value.list_by_labels.return_value = mock_scorers_with_labels
        mock_settings_class.return_value.create.return_value = None

        # When: using GalileoMetricNames enum
        scorers, local_metrics = create_metric_configs("project-123", "run-456", [GalileoMetricNames.context_adherence])

        # Then: list_by_labels is called with the label value
        mock_scorers_class.return_value.list_by_labels.assert_called_once_with(["Context Adherence"], strict=False)
        assert len(scorers) == 1

    @patch("galileo.utils.metrics.Scorers")
    @patch("galileo.utils.metrics.ScorerSettings")
    def test_galileo_metrics_emits_deprecation_warning(
        self, mock_settings_class, mock_scorers_class, mock_scorers_with_labels
    ) -> None:
        # Given: scorers are resolved via list_by_labels
        mock_scorers_class.return_value.list_by_labels.return_value = mock_scorers_with_labels
        mock_settings_class.return_value.create.return_value = None

        # When: using the deprecated GalileoMetrics enum
        with warnings.catch_warnings(record=True) as caught:
            warnings.simplefilter("always")
            create_metric_configs("project-123", "run-456", [GalileoMetrics.correctness])

        # Then: a DeprecationWarning is emitted
        deprecation_warnings = [w for w in caught if issubclass(w.category, DeprecationWarning)]
        assert len(deprecation_warnings) >= 1
        assert "GalileoMetricNames" in str(deprecation_warnings[0].message)

    @patch("galileo.utils.metrics.Scorers")
    @patch("galileo.utils.metrics.ScorerSettings")
    def test_uuid_string_routes_through_list_by_ids(
        self, mock_settings_class, mock_scorers_class, mock_scorers_with_labels
    ) -> None:
        # Given: a scorer resolved via list_by_ids
        scorer_id = "00000000-0000-0000-0000-000000000064"
        mock_scorers_class.return_value.list_by_ids.return_value = mock_scorers_with_labels[:1]
        mock_settings_class.return_value.create.return_value = None

        # When: passing a UUID string
        scorers, _ = create_metric_configs("project-123", "run-456", [scorer_id])

        # Then: list_by_ids is called with the UUID
        mock_scorers_class.return_value.list_by_ids.assert_called_once_with([scorer_id])
        assert len(scorers) == 1

    @patch("galileo.utils.metrics.Scorers")
    @patch("galileo.utils.metrics.ScorerSettings")
    def test_plain_string_routes_through_list_by_labels(
        self, mock_settings_class, mock_scorers_class, mock_scorers_with_labels
    ) -> None:
        # Given: a scorer resolved via list_by_labels
        mock_scorers_class.return_value.list_by_labels.return_value = mock_scorers_with_labels
        mock_settings_class.return_value.create.return_value = None

        # When: passing a plain string
        scorers, _ = create_metric_configs("project-123", "run-456", ["Context Adherence"])

        # Then: list_by_labels is called with strict=False
        mock_scorers_class.return_value.list_by_labels.assert_called_once_with(["Context Adherence"], strict=False)

    @patch("galileo.utils.metrics.Scorers")
    @patch("galileo.utils.metrics.ScorerSettings")
    def test_metric_with_version_fetches_version(
        self, mock_settings_class, mock_scorers_class, mock_scorers_with_labels
    ) -> None:
        # Given: scorers resolved and version available
        mock_scorers_class.return_value.list_by_labels.return_value = mock_scorers_with_labels[:1]
        mock_scorers_class.return_value.get_scorer_version.return_value = type(
            "MockVersion", (), {"to_dict": lambda self: {"id": "v1", "version": 2}}
        )()
        mock_settings_class.return_value.create.return_value = None

        # When: passing a Metric with version
        scorers, _ = create_metric_configs("project-123", "run-456", [Metric(name="Correctness", version=2)])

        # Then: get_scorer_version is called
        mock_scorers_class.return_value.get_scorer_version.assert_called_once()

    @patch("galileo.utils.metrics.Scorers")
    @patch("galileo.utils.metrics.ScorerSettings")
    def test_mixed_inputs(self, mock_settings_class, mock_scorers_class, mock_scorers_with_labels) -> None:
        # Given: scorers resolved via both label and ID lookup
        scorer_id = "00000000-0000-0000-0000-000000000064"
        mock_scorers_class.return_value.list_by_ids.return_value = mock_scorers_with_labels[:1]
        mock_scorers_class.return_value.list_by_labels.return_value = mock_scorers_with_labels[1:]
        mock_settings_class.return_value.create.return_value = None

        # When: passing a mix of UUID + GalileoMetricNames
        scorers, _ = create_metric_configs("project-123", "run-456", [scorer_id, GalileoMetricNames.context_adherence])

        # Then: both lookup methods are called
        mock_scorers_class.return_value.list_by_ids.assert_called_once()
        mock_scorers_class.return_value.list_by_labels.assert_called_once()
        assert len(scorers) == 2

    @patch("galileo.utils.metrics.Scorers")
    def test_unknown_metric_raises_value_error(self, mock_scorers_class) -> None:
        # Given: no scorers match
        mock_scorers_class.return_value.list_by_labels.return_value = []

        # When/Then: unknown metric raises ValueError
        with pytest.raises(ValueError, match="non-existent metrics"):
            create_metric_configs("project-123", "run-456", ["NonexistentMetric"])

    @patch("galileo.utils.metrics.Scorers")
    @patch("galileo.utils.metrics.ScorerSettings")
    def test_local_metrics_still_work(self, mock_settings_class, mock_scorers_class) -> None:
        # Given: no server-side metrics, only local
        def custom_scorer(trace_or_span) -> float:
            return 0.85

        local_metric = LocalMetricConfig(name="custom", scorer_fn=custom_scorer)

        # When: passing only a LocalMetricConfig
        scorers, local_metrics = create_metric_configs("project-123", "run-456", [local_metric])

        # Then: local metrics returned, no API calls for scorer retrieval
        assert len(local_metrics) == 1
        assert local_metrics[0].name == "custom"
        assert len(scorers) == 0
        mock_scorers_class.return_value.list_by_labels.assert_not_called()
        mock_scorers_class.return_value.list_by_ids.assert_not_called()

    @patch("galileo.utils.metrics.Scorers")
    @patch("galileo.utils.metrics.ScorerSettings")
    def test_run_id_none_skips_registration(
        self, mock_settings_class, mock_scorers_class, mock_scorers_with_labels
    ) -> None:
        # Given: scorers resolved via labels
        mock_scorers_class.return_value.list_by_labels.return_value = mock_scorers_with_labels
        mock_settings_class.return_value.create.return_value = None

        # When: run_id is None (trigger=True flow)
        scorers, _ = create_metric_configs("project-123", None, [GalileoMetricNames.correctness])

        # Then: ScorerSettings.create is NOT called
        mock_settings_class.return_value.create.assert_not_called()
        assert len(scorers) == 1
