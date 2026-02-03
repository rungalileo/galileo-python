from unittest.mock import ANY, MagicMock, patch
from uuid import uuid4

import pytest

from galileo.__future__ import LogStream
from galileo.__future__.shared.base import SyncState
from galileo.__future__.shared.column import ColumnCollection
from galileo.__future__.shared.exceptions import ValidationError
from galileo.__future__.shared.query_result import QueryResult
from galileo.resources.models import LLMExportFormat, LogRecordsSortClause, RootType
from galileo.search import RecordType


class TestLogStreamInitialization:
    """Test suite for LogStream initialization."""

    @pytest.mark.parametrize("project_kwarg", [{"project_id": "test-project-id"}, {"project_name": "Test Project"}])
    def test_init_with_name_and_project(self, project_kwarg: dict, reset_configuration: None) -> None:
        """Test initializing a log stream with name and project creates a local-only instance."""
        log_stream = LogStream(name="Test Stream", **project_kwarg)

        assert log_stream.name == "Test Stream"
        assert log_stream.id is None
        assert log_stream.sync_state == SyncState.LOCAL_ONLY

        if "project_id" in project_kwarg:
            assert log_stream.project_id == project_kwarg["project_id"]
            assert log_stream.project_name is None
        else:
            assert log_stream.project_name == project_kwarg["project_name"]
            assert log_stream.project_id is None

    def test_init_without_name_raises_validation_error(self, reset_configuration: None) -> None:
        """Test initializing a log stream without a name raises ValidationError."""
        with pytest.raises(ValidationError, match="'name' must be provided"):
            LogStream(name="", project_id="test-project-id")

    def test_init_without_project_succeeds(self, reset_configuration: None) -> None:
        """Test initializing a log stream without project info succeeds (validated at create time)."""
        # Given: no project_id or project_name provided
        # When: creating a log stream
        log_stream = LogStream(name="Test Stream")

        # Then: log stream is created with LOCAL_ONLY state, project info is None
        assert log_stream.project_id is None
        assert log_stream.project_name is None
        assert log_stream.sync_state == SyncState.LOCAL_ONLY

    def test_init_with_both_project_id_and_name_succeeds(self, reset_configuration: None) -> None:
        """Test initializing a log stream with both project_id and project_name succeeds."""
        # Given: both project_id and project_name provided
        # When: creating a log stream
        log_stream = LogStream(name="Test Stream", project_id="test-id", project_name="Test Project")

        # Then: log stream is created with both values stored
        assert log_stream.project_id == "test-id"
        assert log_stream.project_name == "Test Project"


class TestLogStreamCreate:
    """Test suite for LogStream.create() method."""

    @patch("galileo.__future__.log_stream.LogStreams")
    @patch("galileo.__future__.log_stream.Projects")
    def test_create_persists_log_stream_to_api_with_project_id(
        self,
        mock_projects_class: MagicMock,
        mock_logstreams_class: MagicMock,
        reset_configuration: None,
        mock_logstream: MagicMock,
    ) -> None:
        """Test create() with project_id persists the log stream to the API."""
        # Given: project is resolved
        mock_project = MagicMock()
        mock_project.id = "test-project-id"
        mock_project.name = "Test Project"
        mock_projects_service = MagicMock()
        mock_projects_class.return_value = mock_projects_service
        mock_projects_service.get_with_env_fallbacks.return_value = mock_project

        mock_service = MagicMock()
        mock_logstreams_class.return_value = mock_service
        mock_service.create.return_value = mock_logstream

        # When: creating log stream with project_id
        log_stream = LogStream(name="Test Stream", project_id="test-project-id").create()

        # Then: log stream is created with resolved project_id
        mock_service.create.assert_called_once_with(name="Test Stream", project_id="test-project-id", project_name=None)
        assert log_stream.id == mock_logstream.id
        assert log_stream.is_synced()

    @patch("galileo.__future__.log_stream.LogStreams")
    @patch("galileo.__future__.log_stream.Projects")
    def test_create_persists_log_stream_to_api_with_project_name(
        self,
        mock_projects_class: MagicMock,
        mock_logstreams_class: MagicMock,
        reset_configuration: None,
        mock_logstream: MagicMock,
    ) -> None:
        """Test create() with project_name persists the log stream to the API."""
        # Given: project is resolved from name
        mock_project = MagicMock()
        mock_project.id = "resolved-project-id"
        mock_project.name = "Test Project"
        mock_projects_service = MagicMock()
        mock_projects_class.return_value = mock_projects_service
        mock_projects_service.get_with_env_fallbacks.return_value = mock_project

        mock_service = MagicMock()
        mock_logstreams_class.return_value = mock_service
        mock_service.create.return_value = mock_logstream

        # When: creating log stream with project_name
        log_stream = LogStream(name="Test Stream", project_name="Test Project").create()

        # Then: log stream is created with resolved project_id
        mock_service.create.assert_called_once_with(
            name="Test Stream", project_id="resolved-project-id", project_name=None
        )
        assert log_stream.id == mock_logstream.id
        assert log_stream.is_synced()
        assert log_stream.project_name == "Test Project"

    @patch("galileo.__future__.log_stream.LogStreams")
    @patch("galileo.__future__.log_stream.Projects")
    def test_create_handles_api_failure(
        self, mock_projects_class: MagicMock, mock_logstreams_class: MagicMock, reset_configuration: None
    ) -> None:
        """Test create() handles API failures and sets state correctly."""
        # Given: project is resolved but API fails
        mock_project = MagicMock()
        mock_project.id = "test-project-id"
        mock_project.name = "Test Project"
        mock_projects_service = MagicMock()
        mock_projects_class.return_value = mock_projects_service
        mock_projects_service.get_with_env_fallbacks.return_value = mock_project

        mock_service = MagicMock()
        mock_logstreams_class.return_value = mock_service
        mock_service.create.side_effect = Exception("API Error")

        # When/Then: create() raises error and sets FAILED_SYNC state
        log_stream = LogStream(name="Test Stream", project_id="test-project-id")

        with pytest.raises(Exception, match="API Error"):
            log_stream.create()

        assert log_stream.sync_state == SyncState.FAILED_SYNC

    @patch("galileo.__future__.log_stream.Projects")
    def test_create_without_project_info_raises_error(
        self, mock_projects_class: MagicMock, reset_configuration: None
    ) -> None:
        """Test create() raises ValueError when project information is missing and no env fallback."""
        # Given: env fallback returns None (no project found)
        mock_projects_service = MagicMock()
        mock_projects_class.return_value = mock_projects_service
        mock_projects_service.get_with_env_fallbacks.return_value = None

        # Manually create instance to bypass __init__ validation
        log_stream = LogStream._create_empty()
        log_stream.name = "Test Stream"
        log_stream.project_id = None
        log_stream.project_name = None
        log_stream._set_state(SyncState.LOCAL_ONLY)

        # When/Then: create() raises ValueError with helpful message
        with pytest.raises(ValueError, match="Project not found"):
            log_stream.create()


class TestLogStreamGet:
    """Test suite for LogStream.get() class method."""

    @patch("galileo.__future__.log_stream.LogStreams")
    @patch("galileo.__future__.log_stream.Projects")
    def test_get_returns_log_stream_with_project_id(
        self,
        mock_projects_class: MagicMock,
        mock_logstreams_class: MagicMock,
        reset_configuration: None,
        mock_logstream: MagicMock,
    ) -> None:
        """Test get() with project_id returns a synced log stream instance."""
        # Given: project is resolved
        mock_project = MagicMock()
        mock_project.id = "test-project-id"
        mock_project.name = "Test Project"
        mock_projects_service = MagicMock()
        mock_projects_class.return_value = mock_projects_service
        mock_projects_service.get_with_env_fallbacks.return_value = mock_project

        mock_service = MagicMock()
        mock_logstreams_class.return_value = mock_service
        mock_service.get.return_value = mock_logstream

        # When: calling get with project_id
        log_stream = LogStream.get(name="Test Stream", project_id="test-project-id")

        # Then: log stream is returned and project_name is set from resolved project
        assert log_stream is not None
        assert log_stream.is_synced()
        assert log_stream.project_name == "Test Project"
        mock_service.get.assert_called_once_with(name="Test Stream", project_id="test-project-id")

    @patch("galileo.__future__.log_stream.LogStreams")
    @patch("galileo.__future__.log_stream.Projects")
    def test_get_returns_log_stream_with_project_name(
        self,
        mock_projects_class: MagicMock,
        mock_logstreams_class: MagicMock,
        reset_configuration: None,
        mock_logstream: MagicMock,
    ) -> None:
        """Test get() with project_name returns a synced log stream instance."""
        # Given: project is resolved
        mock_project = MagicMock()
        mock_project.id = "resolved-project-id"
        mock_project.name = "Test Project"
        mock_projects_service = MagicMock()
        mock_projects_class.return_value = mock_projects_service
        mock_projects_service.get_with_env_fallbacks.return_value = mock_project

        mock_service = MagicMock()
        mock_logstreams_class.return_value = mock_service
        mock_service.get.return_value = mock_logstream

        # When: calling get with project_name
        log_stream = LogStream.get(name="Test Stream", project_name="Test Project")

        # Then: log stream is returned using resolved project_id
        assert log_stream is not None
        assert log_stream.is_synced()
        assert log_stream.project_name == "Test Project"
        mock_service.get.assert_called_once_with(name="Test Stream", project_id="resolved-project-id")

    @patch("galileo.__future__.log_stream.LogStreams")
    @patch("galileo.__future__.log_stream.Projects")
    def test_get_returns_none_when_not_found(
        self, mock_projects_class: MagicMock, mock_logstreams_class: MagicMock, reset_configuration: None
    ) -> None:
        """Test get() returns None when log stream is not found."""
        # Given: project is resolved but log stream not found
        mock_project = MagicMock()
        mock_project.id = "test-project-id"
        mock_project.name = "Test Project"
        mock_projects_service = MagicMock()
        mock_projects_class.return_value = mock_projects_service
        mock_projects_service.get_with_env_fallbacks.return_value = mock_project

        mock_service = MagicMock()
        mock_logstreams_class.return_value = mock_service
        mock_service.get.return_value = None

        # When: calling get
        log_stream = LogStream.get(name="Nonexistent Stream", project_id="test-project-id")

        # Then: None is returned
        assert log_stream is None

    @patch("galileo.__future__.log_stream.Projects")
    def test_get_raises_error_without_project_info_and_no_env_fallback(
        self, mock_projects_class: MagicMock, reset_configuration: None
    ) -> None:
        """Test get() raises ValueError when no project and no env fallback."""
        # Given: env fallback returns None
        mock_projects_service = MagicMock()
        mock_projects_class.return_value = mock_projects_service
        mock_projects_service.get_with_env_fallbacks.return_value = None

        # When/Then: calling get raises ValueError
        with pytest.raises(ValueError, match="Project not found"):
            LogStream.get(name="Test Stream")

    @patch("galileo.__future__.log_stream.LogStreams")
    @patch("galileo.__future__.log_stream.Projects")
    def test_get_uses_env_fallback_when_no_project_specified(
        self,
        mock_projects_class: MagicMock,
        mock_logstreams_class: MagicMock,
        reset_configuration: None,
        mock_logstream: MagicMock,
    ) -> None:
        """Test get() uses Projects().get_with_env_fallbacks() when no project is specified."""
        # Given: env fallback resolves to a project
        mock_project = MagicMock()
        mock_project.id = "env-project-id"
        mock_project.name = "Env Project"
        mock_projects_service = MagicMock()
        mock_projects_class.return_value = mock_projects_service
        mock_projects_service.get_with_env_fallbacks.return_value = mock_project

        mock_service = MagicMock()
        mock_logstreams_class.return_value = mock_service
        mock_service.get.return_value = mock_logstream

        # When: calling get without project params
        log_stream = LogStream.get(name="Test Stream")

        # Then: project is resolved from env fallbacks
        mock_projects_service.get_with_env_fallbacks.assert_called_once()
        assert log_stream.project_name == "Env Project"


class TestLogStreamList:
    """Test suite for LogStream.list() class method."""

    @patch("galileo.__future__.log_stream.LogStreams")
    @patch("galileo.__future__.log_stream.Projects")
    def test_list_returns_all_log_streams_with_project_id(
        self, mock_projects_class: MagicMock, mock_logstreams_class: MagicMock, reset_configuration: None
    ) -> None:
        """Test list() with project_id returns a list of synced log stream instances."""
        # Given: project is resolved
        mock_project = MagicMock()
        mock_project.id = "test-project-id"
        mock_project.name = "Test Project"
        mock_projects_service = MagicMock()
        mock_projects_class.return_value = mock_projects_service
        mock_projects_service.get_with_env_fallbacks.return_value = mock_project

        mock_service = MagicMock()
        mock_logstreams_class.return_value = mock_service

        # Create 3 mock log streams
        mock_logstreams = []
        for i in range(3):
            mock_ls = MagicMock()
            mock_ls.id = str(uuid4())
            mock_ls.name = f"Stream {i}"
            mock_ls.project_id = "test-project-id"
            mock_ls.created_at = MagicMock()
            mock_ls.created_by = str(uuid4())
            mock_ls.updated_at = MagicMock()
            mock_ls.additional_properties = {}
            mock_logstreams.append(mock_ls)
        mock_service.list.return_value = mock_logstreams

        # When: calling list with project_id
        log_streams = LogStream.list(project_id="test-project-id")

        # Then: all log streams are returned with project_name set
        assert len(log_streams) == 3
        assert all(isinstance(ls, LogStream) for ls in log_streams)
        assert all(ls.is_synced() for ls in log_streams)
        assert all(ls.project_name == "Test Project" for ls in log_streams)
        mock_service.list.assert_called_once_with(project_id="test-project-id")

    @patch("galileo.__future__.log_stream.LogStreams")
    @patch("galileo.__future__.log_stream.Projects")
    def test_list_returns_all_log_streams_with_project_name(
        self, mock_projects_class: MagicMock, mock_logstreams_class: MagicMock, reset_configuration: None
    ) -> None:
        """Test list() with project_name returns a list of synced log stream instances."""
        # Given: project is resolved
        mock_project = MagicMock()
        mock_project.id = "resolved-project-id"
        mock_project.name = "Test Project"
        mock_projects_service = MagicMock()
        mock_projects_class.return_value = mock_projects_service
        mock_projects_service.get_with_env_fallbacks.return_value = mock_project

        mock_service = MagicMock()
        mock_logstreams_class.return_value = mock_service

        mock_ls = MagicMock()
        mock_ls.id = str(uuid4())
        mock_ls.name = "Stream 1"
        mock_ls.project_id = "resolved-project-id"
        mock_ls.created_at = MagicMock()
        mock_ls.created_by = str(uuid4())
        mock_ls.updated_at = MagicMock()
        mock_ls.additional_properties = {}
        mock_service.list.return_value = [mock_ls]

        # When: calling list with project_name
        log_streams = LogStream.list(project_name="Test Project")

        # Then: log streams are returned using resolved project_id
        assert all(ls.project_name == "Test Project" for ls in log_streams)
        mock_service.list.assert_called_once_with(project_id="resolved-project-id")

    @patch("galileo.__future__.log_stream.Projects")
    def test_list_raises_error_without_project_info_and_no_env_fallback(
        self, mock_projects_class: MagicMock, reset_configuration: None
    ) -> None:
        """Test list() raises ValueError when no project and no env fallback."""
        # Given: env fallback returns None
        mock_projects_service = MagicMock()
        mock_projects_class.return_value = mock_projects_service
        mock_projects_service.get_with_env_fallbacks.return_value = None

        # When/Then: calling list raises ValueError
        with pytest.raises(ValueError, match="Project not found"):
            LogStream.list()

    @patch("galileo.__future__.log_stream.LogStreams")
    @patch("galileo.__future__.log_stream.Projects")
    def test_list_uses_env_fallback_when_no_project_specified(
        self, mock_projects_class: MagicMock, mock_logstreams_class: MagicMock, reset_configuration: None
    ) -> None:
        """Test list() uses Projects().get_with_env_fallbacks() when no project is specified."""
        # Given: env fallback resolves to a project
        mock_project = MagicMock()
        mock_project.id = "env-project-id"
        mock_project.name = "Env Project"
        mock_projects_service = MagicMock()
        mock_projects_class.return_value = mock_projects_service
        mock_projects_service.get_with_env_fallbacks.return_value = mock_project

        mock_service = MagicMock()
        mock_logstreams_class.return_value = mock_service
        mock_service.list.return_value = []

        # When: calling list without project params
        LogStream.list()

        # Then: project is resolved from env fallbacks
        mock_projects_service.get_with_env_fallbacks.assert_called_once()
        mock_service.list.assert_called_once_with(project_id="env-project-id")


class TestLogStreamRefresh:
    """Test suite for LogStream.refresh() method."""

    @patch("galileo.__future__.log_stream.Projects")
    @patch("galileo.__future__.log_stream.LogStreams")
    def test_refresh_updates_attributes_from_api(
        self,
        mock_logstreams_class: MagicMock,
        mock_projects_class: MagicMock,
        reset_configuration: None,
        mock_project: MagicMock,
    ) -> None:
        mock_projects_class.return_value.get_with_env_fallbacks.return_value = mock_project
        """Test refresh() updates all attributes from the API."""
        mock_service = MagicMock()
        mock_logstreams_class.return_value = mock_service

        stream_id = str(uuid4())
        initial_stream = MagicMock()
        initial_stream.id = stream_id
        initial_stream.name = "Old Name"
        initial_stream.project_id = "test-project-id"
        initial_stream.created_at = MagicMock()
        initial_stream.created_by = str(uuid4())
        initial_stream.updated_at = MagicMock()
        initial_stream.additional_properties = {}

        updated_stream = MagicMock()
        updated_stream.id = stream_id
        updated_stream.name = "New Name"
        updated_stream.project_id = "test-project-id"
        updated_stream.created_at = initial_stream.created_at
        updated_stream.created_by = initial_stream.created_by
        updated_stream.updated_at = MagicMock()
        updated_stream.additional_properties = {"new_key": "new_value"}

        mock_service.get.side_effect = [initial_stream, updated_stream]

        log_stream = LogStream.get(name="Old Name", project_id="test-project-id")
        assert log_stream.name == "Old Name"

        log_stream.refresh()

        assert log_stream.name == "New Name"
        assert log_stream.additional_properties == {"new_key": "new_value"}
        assert log_stream.is_synced()

    def test_refresh_raises_error_for_local_only(self, reset_configuration: None) -> None:
        """Test refresh() raises ValueError for local-only log stream."""
        log_stream = LogStream(name="Test Stream", project_id="test-project-id")

        with pytest.raises(ValueError, match="Log stream ID is not set"):
            log_stream.refresh()

    @patch("galileo.__future__.log_stream.Projects")
    @patch("galileo.__future__.log_stream.LogStreams")
    def test_refresh_raises_error_if_log_stream_no_longer_exists(
        self,
        mock_logstreams_class: MagicMock,
        mock_projects_class: MagicMock,
        reset_configuration: None,
        mock_logstream: MagicMock,
        mock_project: MagicMock,
    ) -> None:
        """Test refresh() raises ValueError if log stream no longer exists."""
        mock_projects_class.return_value.get_with_env_fallbacks.return_value = mock_project
        mock_service = MagicMock()
        mock_logstreams_class.return_value = mock_service
        mock_service.get.side_effect = [mock_logstream, None]

        log_stream = LogStream.get(name="Test Stream", project_id="test-project-id")

        with pytest.raises(ValueError, match="no longer exists"):
            log_stream.refresh()

        assert log_stream.sync_state == SyncState.FAILED_SYNC

    @patch("galileo.__future__.log_stream.LogStreams")
    def test_refresh_without_project_id_raises_error(
        self, mock_logstreams_class: MagicMock, reset_configuration: None, mock_logstream: MagicMock
    ) -> None:
        """Test refresh() raises ValueError when project_id is not set."""
        # Manually create instance with id but no project_id
        log_stream = LogStream._create_empty()
        log_stream.id = str(uuid4())
        log_stream.name = "Test Stream"
        log_stream.project_id = None
        log_stream._set_state(SyncState.SYNCED)

        with pytest.raises(ValueError, match="Project ID is not set"):
            log_stream.refresh()


class TestLogStreamQuery:
    """Test suite for LogStream.query() and related methods."""

    @pytest.mark.parametrize(
        "method_name,record_type,limit",
        [
            ("query", RecordType.SPAN, 50),
            ("query", RecordType.TRACE, 30),
            ("query", RecordType.SESSION, 10),
            ("get_spans", RecordType.SPAN, 25),
            ("get_traces", RecordType.TRACE, 30),
            ("get_sessions", RecordType.SESSION, 10),
        ],
    )
    @patch("galileo.__future__.log_stream.Projects")
    @patch("galileo.__future__.log_stream.Search")
    @patch("galileo.__future__.log_stream.LogStreams")
    def test_query_methods(
        self,
        mock_logstreams_class: MagicMock,
        mock_search_class: MagicMock,
        mock_projects_class: MagicMock,
        method_name: str,
        record_type: RecordType,
        limit: int,
        reset_configuration: None,
        mock_logstream: MagicMock,
        mock_project: MagicMock,
    ) -> None:
        mock_projects_class.return_value.get_with_env_fallbacks.return_value = mock_project
        """Test query() and convenience methods (get_spans, get_traces, get_sessions)."""
        mock_logstream_service = MagicMock()
        mock_logstreams_class.return_value = mock_logstream_service
        mock_logstream_service.get.return_value = mock_logstream

        mock_search = MagicMock()
        mock_search_class.return_value = mock_search
        mock_response = MagicMock()
        mock_search.query.return_value = mock_response

        log_stream = LogStream.get(name="Test Stream", project_id="test-project-id")

        # Call the appropriate method
        if method_name == "query":
            result = log_stream.query(record_type=record_type, limit=limit)
        else:
            result = getattr(log_stream, method_name)(limit=limit)

        # Verify Search.query was called with correct parameters
        mock_search.query.assert_called_once_with(
            project_id=mock_logstream.project_id,
            record_type=record_type,
            log_stream_id=mock_logstream.id,
            filters=None,
            sort=None,
            limit=limit,
            starting_token=0,
        )
        # Result should be a QueryResult wrapping the response
        assert isinstance(result, QueryResult)
        assert result._response == mock_response

    def test_query_raises_error_for_local_only(self, reset_configuration: None) -> None:
        """Test query() raises ValueError for local-only log stream."""
        log_stream = LogStream(name="Test Stream", project_id="test-project-id")

        with pytest.raises(ValueError, match="Log stream ID is not set"):
            log_stream.query(record_type=RecordType.SPAN)

    @patch("galileo.__future__.log_stream.LogStreams")
    def test_query_raises_error_without_project_id(
        self, mock_logstreams_class: MagicMock, reset_configuration: None, mock_logstream: MagicMock
    ) -> None:
        """Test query() raises ValueError when project_id is not set."""
        # Manually create instance with id but no project_id
        log_stream = LogStream._create_empty()
        log_stream.id = str(uuid4())
        log_stream.name = "Test Stream"
        log_stream.project_id = None
        log_stream._set_state(SyncState.SYNCED)

        with pytest.raises(ValueError, match="Project ID is not set"):
            log_stream.query(record_type=RecordType.SPAN)


class TestLogStreamExportRecords:
    """Test suite for LogStream.export_records() method."""

    @patch("galileo.__future__.log_stream.Projects")
    @patch("galileo.__future__.log_stream.ExportClient")
    @patch("galileo.__future__.log_stream.LogStreams")
    def test_export_records_with_default_params(
        self,
        mock_logstreams_class: MagicMock,
        mock_export_client_class: MagicMock,
        mock_projects_class: MagicMock,
        reset_configuration: None,
        mock_logstream: MagicMock,
        mock_project: MagicMock,
    ) -> None:
        mock_projects_class.return_value.get_with_env_fallbacks.return_value = mock_project
        """Test export_records() with default parameters."""
        mock_logstream_service = MagicMock()
        mock_logstreams_class.return_value = mock_logstream_service
        mock_logstream_service.get.return_value = mock_logstream

        mock_export_client = MagicMock()
        mock_export_client_class.return_value = mock_export_client
        mock_iterator = iter([{"data": "test"}])
        mock_export_client.records.return_value = mock_iterator

        log_stream = LogStream.get(name="Test Stream", project_id="test-project-id")
        result = log_stream.export_records()

        # Verify ExportClient.records was called with correct parameters
        mock_export_client.records.assert_called_once_with(
            project_id=mock_logstream.project_id,
            root_type=RootType.TRACE,
            filters=None,
            sort=LogRecordsSortClause(column_id="created_at", ascending=False),
            export_format=LLMExportFormat.JSONL,
            log_stream_id=mock_logstream.id,
            column_ids=None,
            redact=True,
        )
        assert result == mock_iterator

    @patch("galileo.__future__.log_stream.Projects")
    @patch("galileo.__future__.log_stream.ExportClient")
    @patch("galileo.__future__.log_stream.LogStreams")
    def test_export_records_with_custom_params(
        self,
        mock_logstreams_class: MagicMock,
        mock_export_client_class: MagicMock,
        mock_projects_class: MagicMock,
        reset_configuration: None,
        mock_logstream: MagicMock,
        mock_project: MagicMock,
    ) -> None:
        mock_projects_class.return_value.get_with_env_fallbacks.return_value = mock_project
        """Test export_records() with custom parameters."""
        mock_logstream_service = MagicMock()
        mock_logstreams_class.return_value = mock_logstream_service
        mock_logstream_service.get.return_value = mock_logstream

        mock_export_client = MagicMock()
        mock_export_client_class.return_value = mock_export_client
        mock_iterator = iter([{"data": "test"}])
        mock_export_client.records.return_value = mock_iterator

        log_stream = LogStream.get(name="Test Stream", project_id="test-project-id")
        custom_sort = LogRecordsSortClause(column_id="updated_at", ascending=True)
        log_stream.export_records(
            record_type=RecordType.SPAN,
            sort=custom_sort,
            export_format=LLMExportFormat.CSV,
            column_ids=["input", "output"],
            redact=False,
        )

        # Verify correct parameters
        mock_export_client.records.assert_called_once_with(
            project_id=mock_logstream.project_id,
            root_type=RootType.SPAN,
            filters=None,
            sort=custom_sort,
            export_format=LLMExportFormat.CSV,
            log_stream_id=mock_logstream.id,
            column_ids=["input", "output"],
            redact=False,
        )

    def test_export_records_raises_error_for_local_only(self, reset_configuration: None) -> None:
        """Test export_records() raises ValueError for local-only log stream."""
        log_stream = LogStream(name="Test Stream", project_id="test-project-id")

        with pytest.raises(ValueError, match="Log stream ID is not set"):
            log_stream.export_records()

    @patch("galileo.__future__.log_stream.LogStreams")
    def test_export_records_raises_error_without_project_id(
        self, mock_logstreams_class: MagicMock, reset_configuration: None
    ) -> None:
        """Test export_records() raises ValueError when project_id is not set."""
        # Manually create instance with id but no project_id
        log_stream = LogStream._create_empty()
        log_stream.id = str(uuid4())
        log_stream.name = "Test Stream"
        log_stream.project_id = None
        log_stream._set_state(SyncState.SYNCED)

        with pytest.raises(ValueError, match="Project ID is not set"):
            log_stream.export_records()


class TestLogStreamContext:
    """Test suite for LogStream.context() method."""

    @patch("galileo.__future__.log_stream.Projects")
    @patch("galileo.__future__.log_stream.galileo_context")
    @patch("galileo.__future__.log_stream.LogStreams")
    def test_context_returns_galileo_context(
        self,
        mock_logstreams_class: MagicMock,
        mock_galileo_context: MagicMock,
        mock_projects_class: MagicMock,
        reset_configuration: None,
        mock_logstream: MagicMock,
        mock_project: MagicMock,
    ) -> None:
        mock_projects_class.return_value.get_with_env_fallbacks.return_value = mock_project
        """Test context() returns a properly configured galileo_context."""
        mock_logstream_service = MagicMock()
        mock_logstreams_class.return_value = mock_logstream_service
        mock_logstream_service.get.return_value = mock_logstream

        mock_context = MagicMock()
        mock_galileo_context.return_value = mock_context

        # Mock the project property
        with patch("galileo.__future__.log_stream.Project") as mock_project_class:
            mock_project = MagicMock()
            mock_project.name = "Test Project"
            mock_project_class.get.return_value = mock_project

            log_stream = LogStream.get(name="Test Stream", project_id="test-project-id")
            result = log_stream.context()

            mock_galileo_context.assert_called_once_with(project="Test Project", log_stream="Test Stream")
            assert result == mock_context


class TestLogStreamProject:
    """Test suite for LogStream.project property."""

    @patch("galileo.__future__.log_stream.Projects")
    @patch("galileo.__future__.log_stream.Project")
    @patch("galileo.__future__.log_stream.LogStreams")
    def test_project_property_returns_project(
        self,
        mock_logstreams_class: MagicMock,
        mock_project_class: MagicMock,
        mock_projects_class: MagicMock,
        reset_configuration: None,
        mock_logstream: MagicMock,
        mock_project: MagicMock,
    ) -> None:
        """Test project property returns the associated project."""
        mock_projects_class.return_value.get_with_env_fallbacks.return_value = mock_project
        mock_logstream_service = MagicMock()
        mock_logstreams_class.return_value = mock_logstream_service
        mock_logstream_service.get.return_value = mock_logstream

        returned_project = MagicMock()
        returned_project.id = mock_logstream.project_id
        returned_project.name = "Test Project"
        mock_project_class.get.return_value = returned_project

        log_stream = LogStream.get(name="Test Stream", project_id="test-project-id")
        project = log_stream.project

        mock_project_class.get.assert_called_once_with(id=mock_logstream.project_id)
        assert project == returned_project


class TestLogStreamColumns:
    """Test suite for LogStream column properties."""

    @pytest.mark.parametrize(
        "property_name,api_func_name,error_msg",
        [
            (
                "span_columns",
                "spans_available_columns_projects_project_id_spans_available_columns_post",
                "Unable to retrieve span columns",
            ),
            (
                "session_columns",
                "sessions_available_columns_projects_project_id_sessions_available_columns_post",
                "Unable to retrieve session columns",
            ),
            (
                "trace_columns",
                "traces_available_columns_projects_project_id_traces_available_columns_post",
                "Unable to retrieve trace columns",
            ),
        ],
    )
    @patch("galileo.__future__.log_stream.Projects")
    @patch("galileo.__future__.log_stream.GalileoPythonConfig")
    @patch("galileo.__future__.log_stream.LogStreams")
    def test_column_properties_return_column_collection(
        self,
        mock_logstreams_class: MagicMock,
        mock_config_class: MagicMock,
        mock_projects_class: MagicMock,
        property_name: str,
        api_func_name: str,
        error_msg: str,
        reset_configuration: None,
        mock_logstream: MagicMock,
        mock_project: MagicMock,
    ) -> None:
        mock_projects_class.return_value.get_with_env_fallbacks.return_value = mock_project
        """Test column properties return ColumnCollection with proper API calls."""
        # Setup LogStreams mock
        mock_logstream_service = MagicMock()
        mock_logstreams_class.return_value = mock_logstream_service
        mock_logstream_service.get.return_value = mock_logstream

        # Setup config mock
        mock_config = MagicMock()
        mock_api_client = MagicMock()
        mock_config.api_client = mock_api_client
        mock_config_class.get.return_value = mock_config

        # Setup API function mock
        mock_column_1 = MagicMock()
        mock_column_1.id = "input"
        mock_column_2 = MagicMock()
        mock_column_2.id = "output"
        mock_response = MagicMock()
        mock_response.columns = [mock_column_1, mock_column_2]

        with patch(f"galileo.__future__.log_stream.{api_func_name}") as mock_api_func:
            mock_api_func.sync.return_value = mock_response

            log_stream = LogStream.get(name="Test Stream", project_id="test-project-id")
            columns = getattr(log_stream, property_name)

            # Verify API function was called correctly
            mock_api_func.sync.assert_called_once_with(
                project_id=mock_logstream.project_id, client=mock_api_client, body=ANY
            )
            # Verify the body parameter has the correct log_stream_id
            call_kwargs = mock_api_func.sync.call_args.kwargs
            assert call_kwargs["body"].log_stream_id == mock_logstream.id

            # Verify result is a ColumnCollection
            assert isinstance(columns, ColumnCollection)
            assert len(columns._columns) == 2

    @pytest.mark.parametrize("property_name", ["span_columns", "session_columns", "trace_columns"])
    def test_column_properties_raise_error_for_local_only(self, property_name: str, reset_configuration: None) -> None:
        """Test column properties raise ValueError for local-only log streams."""
        log_stream = LogStream(name="Test Stream", project_id="test-project-id")

        with pytest.raises(ValueError, match="Log stream ID is not set"):
            getattr(log_stream, property_name)

    @pytest.mark.parametrize(
        "property_name,api_func_name",
        [
            ("span_columns", "spans_available_columns_projects_project_id_spans_available_columns_post"),
            ("session_columns", "sessions_available_columns_projects_project_id_sessions_available_columns_post"),
            ("trace_columns", "traces_available_columns_projects_project_id_traces_available_columns_post"),
        ],
    )
    @patch("galileo.__future__.log_stream.Projects")
    @patch("galileo.__future__.log_stream.GalileoPythonConfig")
    @patch("galileo.__future__.log_stream.LogStreams")
    def test_column_properties_raise_error_on_empty_response(
        self,
        mock_logstreams_class: MagicMock,
        mock_config_class: MagicMock,
        mock_projects_class: MagicMock,
        property_name: str,
        api_func_name: str,
        reset_configuration: None,
        mock_logstream: MagicMock,
        mock_project: MagicMock,
    ) -> None:
        mock_projects_class.return_value.get_with_env_fallbacks.return_value = mock_project
        """Test column properties raise ValueError when API returns empty response."""
        # Setup mocks
        mock_logstream_service = MagicMock()
        mock_logstreams_class.return_value = mock_logstream_service
        mock_logstream_service.get.return_value = mock_logstream

        mock_config = MagicMock()
        mock_config_class.get.return_value = mock_config

        with patch(f"galileo.__future__.log_stream.{api_func_name}") as mock_api_func:
            mock_api_func.sync.return_value = None

            log_stream = LogStream.get(name="Test Stream", project_id="test-project-id")

            with pytest.raises(ValueError, match="Unable to retrieve"):
                getattr(log_stream, property_name)


class TestLogStreamMethods:
    """Test suite for other LogStream methods."""

    def test_str_representation(self, reset_configuration: None) -> None:
        """Test __str__ returns expected format."""
        log_stream = LogStream(name="Test Stream", project_id="test-project-id")
        log_stream.id = "test-id-123"

        assert str(log_stream) == "LogStream(name='Test Stream', id='test-id-123', project_id='test-project-id')"

    def test_repr_representation(self, reset_configuration: None) -> None:
        """Test __repr__ returns expected format with created_at."""
        log_stream = LogStream(name="Test Stream", project_id="test-project-id")
        log_stream.id = "test-id-123"
        log_stream.created_at = "2024-01-01 12:00:00"

        assert "Test Stream" in repr(log_stream)
        assert "test-id-123" in repr(log_stream)
        assert "test-project-id" in repr(log_stream)
        assert "2024-01-01 12:00:00" in repr(log_stream)
