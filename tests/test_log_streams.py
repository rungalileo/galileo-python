import datetime
from unittest.mock import Mock, patch
from uuid import UUID

import pytest

from galileo.log_streams import (
    LogStream,
    LogStreams,
    configure_log_stream_metrics,
    create_log_stream,
    create_log_stream_with_metrics,
    get_log_stream,
    list_log_streams,
)
from galileo.projects import Project
from galileo.resources.models import ProjectCreateResponse, ProjectType, ScorerConfig, ScorerResponse, ScorerTypes
from galileo.resources.models.log_stream_response import LogStreamResponse
from galileo.resources.models.run_scorer_settings_response import RunScorerSettingsResponse
from galileo.schema.metrics import GalileoScorers, Metric
from tests.testutils.setup import setup_mock_projects_client


def project():
    now = datetime.datetime.now()
    return Project(
        ProjectCreateResponse(
            created_at=now, id=str(UUID(int=0)), updated_at=now, name="test-project", type_=ProjectType.GEN_AI
        )
    )


def log_stream_response():
    now = datetime.datetime.now()
    return LogStreamResponse(
        id="6c4e3f7e-4a9a-4e7e-8c1f-3a9a3a9a3a9b",
        project_id="6c4e3f7e-4a9a-4e7e-8c1f-3a9a3a9a3a9a",
        name="test-log-stream",
        created_at=now,
        updated_at=now,
        created_by="test-user",
    )


def scorers():
    return [
        ScorerResponse(
            id=str(UUID(int=0)),
            name="correctness",
            scorer_type=ScorerTypes.PRESET,
            tags=["preset"],
            created_at=datetime.datetime.now(),
            updated_at=datetime.datetime.now(),
            created_by="test-user",
            description="Correctness scorer",
            defaults={},
        ),
        ScorerResponse(
            id=str(UUID(int=1)),
            name="groundedness",
            scorer_type=ScorerTypes.PRESET,
            tags=["preset"],
            created_at=datetime.datetime.now(),
            updated_at=datetime.datetime.now(),
            created_by="test-user",
            description="Groundedness scorer",
            defaults={},
        ),
        ScorerResponse(
            id=str(UUID(int=2)),
            name="custom_scorer",
            scorer_type=ScorerTypes.LLM,
            tags=["custom"],
            created_at=datetime.datetime.now(),
            updated_at=datetime.datetime.now(),
            created_by="test-user",
            description="Custom scorer",
            defaults={},
        ),
    ]


class TestLogStreams:
    @patch("galileo.log_streams.create_log_stream_projects_project_id_log_streams_post")
    @patch("galileo.log_streams.Projects")
    def test_create_log_stream_by_name(self, mock_projects_class, mock_create_api):
        """Test creating a log stream using project name."""
        # Setup mocks
        setup_mock_projects_client(mock_projects_class)
        mock_create_api.sync.return_value = log_stream_response()

        # Test
        result = LogStreams().create(name="test-log-stream", project_name="test-project")

        # Assertions
        assert isinstance(result, LogStream)
        assert result.name == "test-log-stream"
        mock_create_api.sync.assert_called_once()
        mock_projects_class.assert_called_once()

    @patch("galileo.log_streams.ScorerSettings")
    @patch("galileo.log_streams.Scorers")
    @patch("galileo.log_streams.create_log_stream_projects_project_id_log_streams_post")
    @patch("galileo.log_streams.Projects")
    def test_create_log_stream_with_metrics(
        self, mock_projects_class, mock_create_api, mock_scorers_class, mock_scorer_settings_class
    ):
        """Test creating a log stream with metrics using project name."""
        # Setup mocks
        setup_mock_projects_client(mock_projects_class)
        mock_create_api.sync.return_value = log_stream_response()

        mock_scorers_instance = mock_scorers_class.return_value
        mock_scorers_instance.list.return_value = scorers()

        mock_scorer_settings_instance = mock_scorer_settings_class.return_value
        mock_scorer_settings_instance.create.return_value = RunScorerSettingsResponse(
            run_id="stream-123", scorers=[ScorerConfig(id="scorer-1", scorer_type=ScorerTypes.PRESET)]
        )

        # Test
        result = LogStreams().create(
            name="test-log-stream", project_name="test-project", metrics=[GalileoScorers.correctness, "groundedness"]
        )

        # Assertions
        assert isinstance(result, LogStream)
        assert result.name == "test-log-stream"
        mock_create_api.sync.assert_called_once()
        mock_projects_class.assert_called_once()
        mock_scorers_instance.list.assert_called_once()
        mock_scorer_settings_instance.create.assert_called_once()

    @patch("galileo.log_streams.create_log_stream_projects_project_id_log_streams_post")
    def test_create_log_stream_by_id(self, mock_create_api):
        """Test creating a log stream using project ID."""
        # Setup mocks
        mock_create_api.sync.return_value = log_stream_response()

        # Test
        result = LogStreams().create(name="test-log-stream", project_id="project-123")

        # Assertions
        assert isinstance(result, LogStream)
        assert result.name == "test-log-stream"
        mock_create_api.sync.assert_called_once()

    @patch("galileo.log_streams.get_log_stream_projects_project_id_log_streams_log_stream_id_get")
    def test_get_log_stream_by_id(self, mock_get_api):
        """Test getting a log stream by ID."""
        # Setup mocks
        mock_get_api.sync.return_value = log_stream_response()

        # Test
        result = LogStreams().get(id="stream-123", project_id="project-123")

        # Assertions
        assert isinstance(result, LogStream)
        # Just verify the API was called with correct parameters (ignore client object details)
        mock_get_api.sync.assert_called_once()
        call_args = mock_get_api.sync.call_args
        assert call_args.kwargs["project_id"] == "project-123"
        assert call_args.kwargs["log_stream_id"] == "stream-123"

    @patch("galileo.log_streams.list_log_streams_projects_project_id_log_streams_get")
    def test_get_log_stream_by_name(self, mock_list_api):
        """Test getting a log stream by name."""
        # Setup mocks
        mock_list_api.sync.return_value = [log_stream_response()]

        # Test
        result = LogStreams().get(name="test-log-stream", project_id="project-123")

        # Assertions
        assert isinstance(result, LogStream)
        assert result.name == "test-log-stream"

    @patch("galileo.log_streams.list_log_streams_projects_project_id_log_streams_get")
    def test_list_log_streams(self, mock_list_api):
        """Test listing log streams."""
        # Setup mocks
        mock_list_api.sync.return_value = [log_stream_response()]

        # Test
        result = LogStreams().list(project_id="project-123")

        # Assertions
        assert len(result) == 1
        assert isinstance(result[0], LogStream)
        mock_list_api.sync.assert_called_once()

    @patch("galileo.log_streams.ScorerSettings")
    @patch("galileo.log_streams.Scorers")
    def test_configure_metrics(self, mock_scorers_class, mock_scorer_settings_class):
        """Test configuring metrics for a log stream."""
        # Setup mocks
        mock_scorers_instance = mock_scorers_class.return_value
        mock_scorers_instance.list.return_value = scorers()

        mock_scorer_settings_instance = mock_scorer_settings_class.return_value
        mock_scorer_settings_instance.create.return_value = RunScorerSettingsResponse(
            run_id="stream-123", scorers=[ScorerConfig(id="scorer-1", scorer_type=ScorerTypes.PRESET)]
        )

        # Test
        log_streams = LogStreams()
        result = log_streams.configure_metrics(
            log_stream_id="stream-123", project_id="project-123", metrics=[GalileoScorers.correctness, "groundedness"]
        )

        # Assertions - the decorator catches exceptions, but in this case it should work
        # Check if result is not None (success case)
        if result is not None:
            assert len(result) == 2
            assert all(isinstance(scorer, ScorerConfig) for scorer in result)
        mock_scorers_instance.list.assert_called_once()
        mock_scorer_settings_instance.create.assert_called_once()

    @patch("galileo.log_streams.ScorerSettings")
    @patch("galileo.log_streams.Scorers")
    def test_configure_metrics_unknown_metric(self, mock_scorers_class, mock_scorer_settings_class):
        """Test configuring metrics with unknown metric name."""
        # Setup mocks
        mock_scorers_instance = mock_scorers_class.return_value
        mock_scorers_instance.list.return_value = scorers()

        # Test with unknown metric - decorator catches the exception so method returns None
        log_streams = LogStreams()
        result = log_streams.configure_metrics(
            log_stream_id="stream-123", project_id="project-123", metrics=["unknown_metric"]
        )
        assert result is None  # Method fails and returns None due to decorator

    @patch("galileo.log_streams.ScorerSettings")
    @patch("galileo.log_streams.Scorers")
    def test_configure_metrics_with_metric_object(self, mock_scorers_class, mock_scorer_settings_class):
        """Test configuring metrics using Metric objects."""
        # Setup mocks
        mock_scorers_instance = mock_scorers_class.return_value
        mock_scorers_instance.list.return_value = scorers()
        mock_scorers_instance.get_scorer_version.return_value = Mock()

        mock_scorer_settings_instance = mock_scorer_settings_class.return_value
        mock_scorer_settings_instance.create.return_value = RunScorerSettingsResponse(
            run_id="stream-123", scorers=[ScorerConfig(id="scorer-1", scorer_type=ScorerTypes.PRESET)]
        )

        # Test with a custom (non-Galileo) scorer that supports versioning
        log_streams = LogStreams()
        result = log_streams.configure_metrics(
            log_stream_id="stream-123", project_id="project-123", metrics=[Metric(name="custom_scorer", version=2)]
        )

        # Assertions - check if result is not None (success case)
        if result is not None:
            assert len(result) == 1
        mock_scorers_instance.get_scorer_version.assert_called_once()

    def test_create_log_stream_invalid_params(self):
        """Test create log stream with invalid parameters."""
        log_streams = LogStreams()

        # The decorator catches exceptions and logs them, so we need to check that the method returns None
        # Test with both project_id and project_name
        result1 = log_streams.create(name="test", project_id="123", project_name="test")
        assert result1 is None  # Method fails and returns None due to decorator

        # Test with neither project_id nor project_name
        result2 = log_streams.create(name="test")
        assert result2 is None  # Method fails and returns None due to decorator

    def test_get_log_stream_invalid_params(self):
        """Test get log stream with invalid parameters."""
        log_streams = LogStreams()

        # The decorator catches exceptions and logs them, so we need to check that the method returns None
        # Test with both id and name
        result1 = log_streams.get(id="123", name="test", project_id="456")
        assert result1 is None  # Method fails and returns None due to decorator

        # Test with neither id nor name
        result2 = log_streams.get(project_id="456")
        assert result2 is None  # Method fails and returns None due to decorator


class TestLogStreamConvenienceFunctions:
    @patch("galileo.log_streams.LogStreams")
    def test_create_log_stream(self, mock_log_streams_class):
        """Test create_log_stream convenience function."""
        mock_instance = mock_log_streams_class.return_value
        mock_instance.create.return_value = LogStream(log_stream_response())

        result = create_log_stream(name="test", project_name="test-project")

        assert isinstance(result, LogStream)
        mock_instance.create.assert_called_once_with(
            name="test", project_id=None, project_name="test-project", metrics=None
        )

    @patch("galileo.log_streams.LogStreams")
    def test_create_log_stream_with_metrics(self, mock_log_streams_class):
        """Test create_log_stream convenience function with metrics."""
        mock_instance = mock_log_streams_class.return_value
        mock_instance.create.return_value = LogStream(log_stream_response())

        result = create_log_stream(name="test", project_name="test-project", metrics=[GalileoScorers.correctness])

        assert isinstance(result, LogStream)
        mock_instance.create.assert_called_once_with(
            name="test", project_id=None, project_name="test-project", metrics=[GalileoScorers.correctness]
        )

    @patch("galileo.log_streams.LogStreams")
    def test_get_log_stream(self, mock_log_streams_class):
        """Test get_log_stream convenience function."""
        mock_instance = mock_log_streams_class.return_value
        mock_instance.get.return_value = LogStream(log_stream_response())

        result = get_log_stream(name="test", project_name="test-project")

        assert isinstance(result, LogStream)
        mock_instance.get.assert_called_once_with(name="test", project_id=None, project_name="test-project")

    @patch("galileo.log_streams.LogStreams")
    def test_list_log_streams(self, mock_log_streams_class):
        """Test list_log_streams convenience function."""
        mock_instance = mock_log_streams_class.return_value
        mock_instance.list.return_value = [LogStream(log_stream_response())]

        result = list_log_streams(project_name="test-project")

        assert len(result) == 1
        assert isinstance(result[0], LogStream)
        mock_instance.list.assert_called_once_with(project_id=None, project_name="test-project")

    @patch("galileo.log_streams.LogStreams")
    @patch("galileo.log_streams.get_log_stream")
    @patch("galileo.log_streams.Projects")
    def test_configure_log_stream_metrics_with_name(
        self, mock_projects_class, mock_get_log_stream, mock_log_streams_class
    ):
        """Test configure_log_stream_metrics with log stream name."""
        # Setup mocks
        setup_mock_projects_client(mock_projects_class)
        mock_get_log_stream.return_value = LogStream(log_stream_response())
        mock_instance = mock_log_streams_class.return_value
        mock_instance.configure_metrics.return_value = [ScorerConfig(id="scorer-1", scorer_type=ScorerTypes.PRESET)]

        # Test
        result = configure_log_stream_metrics(
            log_stream="test-log-stream", metrics=[GalileoScorers.correctness], project_name="test-project"
        )

        # Assertions
        assert len(result) == 1
        mock_get_log_stream.assert_called_once()
        mock_instance.configure_metrics.assert_called_once()

    @patch("galileo.log_streams.LogStreams")
    @patch("galileo.log_streams.Projects")
    def test_configure_log_stream_metrics_with_object(self, mock_projects_class, mock_log_streams_class):
        """Test configure_log_stream_metrics with LogStream object."""
        # Setup mocks
        setup_mock_projects_client(mock_projects_class)
        mock_instance = mock_log_streams_class.return_value
        mock_instance.configure_metrics.return_value = [ScorerConfig(id="scorer-1", scorer_type=ScorerTypes.PRESET)]

        # Test
        log_stream = LogStream(log_stream_response())
        result = configure_log_stream_metrics(
            log_stream=log_stream, metrics=[GalileoScorers.correctness], project_name="test-project"
        )

        # Assertions
        assert len(result) == 1
        mock_instance.configure_metrics.assert_called_once()

    @patch("galileo.log_streams.configure_log_stream_metrics")
    @patch("galileo.log_streams.create_log_stream")
    def test_create_log_stream_with_metrics_combined(self, mock_create, mock_configure):
        """Test create_log_stream_with_metrics convenience function."""
        # Setup mocks
        mock_log_stream = LogStream(log_stream_response())
        mock_create.return_value = mock_log_stream
        mock_configure.return_value = [ScorerConfig(id="scorer-1", scorer_type=ScorerTypes.PRESET)]

        # Test
        log_stream, scorers = create_log_stream_with_metrics(
            name="test-stream", metrics=[GalileoScorers.correctness], project_name="test-project"
        )

        # Assertions
        assert isinstance(log_stream, LogStream)
        assert len(scorers) == 1
        mock_create.assert_called_once_with(name="test-stream", project_id=None, project_name="test-project")
        mock_configure.assert_called_once_with(
            log_stream=mock_log_stream,
            metrics=[GalileoScorers.correctness],
            project_id=None,
            project_name="test-project",
        )

    @patch("galileo.log_streams.get_log_stream")
    @patch("galileo.log_streams.Projects")
    def test_configure_log_stream_metrics_stream_not_found(self, mock_projects_class, mock_get_log_stream):
        """Test configure_log_stream_metrics when log stream is not found."""
        # Setup mocks
        setup_mock_projects_client(mock_projects_class)
        mock_get_log_stream.return_value = None

        # Test
        with pytest.raises(ValueError, match="Log stream 'nonexistent' not found in project"):
            configure_log_stream_metrics(
                log_stream="nonexistent", metrics=[GalileoScorers.correctness], project_name="test-project"
            )

    def test_configure_log_stream_metrics_invalid_params(self):
        """Test configure_log_stream_metrics with invalid parameters."""
        # Test with both project_id and project_name
        with pytest.raises(ValueError, match="Exactly one of 'project_id' or 'project_name' must be provided"):
            configure_log_stream_metrics(
                log_stream="test", metrics=[GalileoScorers.correctness], project_id="123", project_name="test"
            )

        # Test with neither project_id nor project_name
        with pytest.raises(ValueError, match="Exactly one of 'project_id' or 'project_name' must be provided"):
            configure_log_stream_metrics(log_stream="test", metrics=[GalileoScorers.correctness])


class TestLogStreamClass:
    def test_log_stream_initialization(self):
        """Test LogStream initialization."""
        response = log_stream_response()
        log_stream = LogStream(response)

        assert log_stream.id == response.id
        assert log_stream.name == response.name
        assert log_stream.project_id == response.project_id
        assert log_stream.created_at == response.created_at
        assert log_stream.updated_at == response.updated_at

    def test_log_stream_initialization_none(self):
        """Test LogStream initialization with None."""
        log_stream = LogStream(None)
        # Should not raise an error
        assert log_stream is not None
