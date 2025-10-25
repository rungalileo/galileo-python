from unittest.mock import MagicMock, patch
from uuid import uuid4

import pytest

from galileo.__future__ import LogStream
from galileo.__future__.base import SyncState
from galileo.__future__.exceptions import ValidationError
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

    def test_init_without_project_raises_validation_error(self, reset_configuration: None) -> None:
        """Test initializing a log stream without project info raises ValidationError."""
        with pytest.raises(ValidationError):
            LogStream(name="Test Stream")

    def test_init_with_both_project_id_and_name_raises_validation_error(self, reset_configuration: None) -> None:
        """Test initializing a log stream with both project_id and project_name raises ValidationError."""
        with pytest.raises(ValidationError):
            LogStream(name="Test Stream", project_id="test-id", project_name="Test Project")


class TestLogStreamCreate:
    """Test suite for LogStream.create() method."""

    @pytest.mark.parametrize(
        "project_kwarg,expected_call",
        [
            ({"project_id": "test-project-id"}, {"project_id": "test-project-id", "project_name": None}),
            ({"project_name": "Test Project"}, {"project_id": None, "project_name": "Test Project"}),
        ],
    )
    @patch("galileo.__future__.log_stream.LogStreams")
    def test_create_persists_log_stream_to_api(
        self,
        mock_logstreams_class: MagicMock,
        project_kwarg: dict,
        expected_call: dict,
        reset_configuration: None,
        mock_logstream: MagicMock,
    ) -> None:
        """Test create() persists the log stream to the API and updates attributes."""
        mock_service = MagicMock()
        mock_logstreams_class.return_value = mock_service
        mock_service.create.return_value = mock_logstream

        log_stream = LogStream(name="Test Stream", **project_kwarg).create()

        mock_service.create.assert_called_once_with(name="Test Stream", **expected_call)
        assert log_stream.id == mock_logstream.id
        assert log_stream.is_synced()

    @patch("galileo.__future__.log_stream.LogStreams")
    def test_create_handles_api_failure(self, mock_logstreams_class: MagicMock, reset_configuration: None) -> None:
        """Test create() handles API failures and sets state correctly."""
        mock_service = MagicMock()
        mock_logstreams_class.return_value = mock_service
        mock_service.create.side_effect = Exception("API Error")

        log_stream = LogStream(name="Test Stream", project_id="test-project-id")

        with pytest.raises(Exception, match="API Error"):
            log_stream.create()

        assert log_stream.sync_state == SyncState.FAILED_SYNC

    @patch("galileo.__future__.log_stream.LogStreams")
    def test_create_without_project_info_raises_error(
        self, mock_logstreams_class: MagicMock, reset_configuration: None
    ) -> None:
        """Test create() raises ValueError when project information is missing."""
        # Manually create instance to bypass __init__ validation
        log_stream = LogStream._create_empty()
        log_stream.name = "Test Stream"
        log_stream.project_id = None
        log_stream.project_name = None
        log_stream._set_state(SyncState.LOCAL_ONLY)

        with pytest.raises(ValueError, match="Project information is not set"):
            log_stream.create()


class TestLogStreamGet:
    """Test suite for LogStream.get() class method."""

    @pytest.mark.parametrize(
        "project_kwarg,expected_call",
        [
            ({"project_id": "test-project-id"}, {"project_id": "test-project-id", "project_name": None}),
            ({"project_name": "Test Project"}, {"project_id": None, "project_name": "Test Project"}),
        ],
    )
    @patch("galileo.__future__.log_stream.LogStreams")
    def test_get_returns_log_stream(
        self,
        mock_logstreams_class: MagicMock,
        project_kwarg: dict,
        expected_call: dict,
        reset_configuration: None,
        mock_logstream: MagicMock,
    ) -> None:
        """Test get() with project_id or project_name returns a synced log stream instance."""
        mock_service = MagicMock()
        mock_logstreams_class.return_value = mock_service
        mock_service.get.return_value = mock_logstream

        log_stream = LogStream.get(name="Test Stream", **project_kwarg)

        assert log_stream is not None
        assert log_stream.is_synced()
        mock_service.get.assert_called_once_with(name="Test Stream", **expected_call)

    @patch("galileo.__future__.log_stream.LogStreams")
    def test_get_returns_none_when_not_found(self, mock_logstreams_class: MagicMock, reset_configuration: None) -> None:
        """Test get() returns None when log stream is not found.
        # TODO: we need to change the response to raise an error"""
        mock_service = MagicMock()
        mock_logstreams_class.return_value = mock_service
        mock_service.get.return_value = None

        log_stream = LogStream.get(name="Nonexistent Stream", project_id="test-project-id")

        assert log_stream is None

    def test_get_raises_error_without_project_info(self, reset_configuration: None) -> None:
        """Test get() raises ValidationError when neither project_id nor project_name is provided."""
        with pytest.raises(ValidationError):
            LogStream.get(name="Test Stream")

    def test_get_raises_error_with_both_project_id_and_name(self, reset_configuration: None) -> None:
        """Test get() raises ValidationError when both project_id and project_name are provided."""
        with pytest.raises(ValidationError):
            LogStream.get(name="Test Stream", project_id="test-id", project_name="Test Project")

    @patch("galileo.__future__.log_stream.LogStreams")
    def test_get_preserves_project_name_when_provided(
        self, mock_logstreams_class: MagicMock, reset_configuration: None, mock_logstream: MagicMock
    ) -> None:
        """Test get() preserves project_name when provided (API doesn't return it).
        # TODO: we need to change the response to return the project_name"""
        mock_service = MagicMock()
        mock_logstreams_class.return_value = mock_service
        mock_logstream.project_name = None  # API doesn't return this
        mock_service.get.return_value = mock_logstream

        log_stream = LogStream.get(name="Test Stream", project_name="Test Project")

        assert log_stream.project_name == "Test Project"


class TestLogStreamList:
    """Test suite for LogStream.list() class method."""

    @pytest.mark.parametrize(
        "project_kwarg,expected_call",
        [
            ({"project_id": "test-project-id"}, {"project_id": "test-project-id", "project_name": None}),
            ({"project_name": "Test Project"}, {"project_id": None, "project_name": "Test Project"}),
        ],
    )
    @patch("galileo.__future__.log_stream.LogStreams")
    def test_list_returns_all_log_streams(
        self, mock_logstreams_class: MagicMock, project_kwarg: dict, expected_call: dict, reset_configuration: None
    ) -> None:
        """Test list() returns a list of synced log stream instances."""
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

        log_streams = LogStream.list(**project_kwarg)

        assert len(log_streams) == 3
        assert all(isinstance(ls, LogStream) for ls in log_streams)
        assert all(ls.is_synced() for ls in log_streams)
        mock_service.list.assert_called_once_with(**expected_call)

    @patch("galileo.__future__.log_stream.LogStreams")
    def test_list_preserves_project_name_when_provided(
        self, mock_logstreams_class: MagicMock, reset_configuration: None
    ) -> None:
        """Test list() preserves project_name in all returned instances."""
        mock_service = MagicMock()
        mock_logstreams_class.return_value = mock_service

        mock_ls = MagicMock()
        mock_ls.id = str(uuid4())
        mock_ls.name = "Stream 1"
        mock_ls.project_id = "test-project-id"
        mock_ls.created_at = MagicMock()
        mock_ls.created_by = str(uuid4())
        mock_ls.updated_at = MagicMock()
        mock_ls.additional_properties = {}
        mock_service.list.return_value = [mock_ls]

        log_streams = LogStream.list(project_name="Test Project")

        assert all(ls.project_name == "Test Project" for ls in log_streams)

    def test_list_raises_error_without_project_info(self, reset_configuration: None) -> None:
        """Test list() raises ValidationError when neither project_id nor project_name is provided."""
        with pytest.raises(ValidationError):
            LogStream.list()


class TestLogStreamRefresh:
    """Test suite for LogStream.refresh() method."""

    @patch("galileo.__future__.log_stream.LogStreams")
    def test_refresh_updates_attributes_from_api(
        self, mock_logstreams_class: MagicMock, reset_configuration: None
    ) -> None:
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

    @patch("galileo.__future__.log_stream.LogStreams")
    def test_refresh_raises_error_if_log_stream_no_longer_exists(
        self, mock_logstreams_class: MagicMock, reset_configuration: None, mock_logstream: MagicMock
    ) -> None:
        """Test refresh() raises ValueError if log stream no longer exists."""
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
    @patch("galileo.__future__.log_stream.Search")
    @patch("galileo.__future__.log_stream.LogStreams")
    def test_query_methods(
        self,
        mock_logstreams_class: MagicMock,
        mock_search_class: MagicMock,
        method_name: str,
        record_type: RecordType,
        limit: int,
        reset_configuration: None,
        mock_logstream: MagicMock,
    ) -> None:
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
        assert result == mock_response

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

    @patch("galileo.__future__.log_stream.ExportClient")
    @patch("galileo.__future__.log_stream.LogStreams")
    def test_export_records_with_default_params(
        self,
        mock_logstreams_class: MagicMock,
        mock_export_client_class: MagicMock,
        reset_configuration: None,
        mock_logstream: MagicMock,
    ) -> None:
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

    @patch("galileo.__future__.log_stream.ExportClient")
    @patch("galileo.__future__.log_stream.LogStreams")
    def test_export_records_with_custom_params(
        self,
        mock_logstreams_class: MagicMock,
        mock_export_client_class: MagicMock,
        reset_configuration: None,
        mock_logstream: MagicMock,
    ) -> None:
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

    @patch("galileo.__future__.log_stream.galileo_context")
    @patch("galileo.__future__.log_stream.LogStreams")
    def test_context_returns_galileo_context(
        self,
        mock_logstreams_class: MagicMock,
        mock_galileo_context: MagicMock,
        reset_configuration: None,
        mock_logstream: MagicMock,
    ) -> None:
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

    @patch("galileo.__future__.log_stream.Project")
    @patch("galileo.__future__.log_stream.LogStreams")
    def test_project_property_returns_project(
        self,
        mock_logstreams_class: MagicMock,
        mock_project_class: MagicMock,
        reset_configuration: None,
        mock_logstream: MagicMock,
    ) -> None:
        """Test project property returns the associated project."""
        mock_logstream_service = MagicMock()
        mock_logstreams_class.return_value = mock_logstream_service
        mock_logstream_service.get.return_value = mock_logstream

        mock_project = MagicMock()
        mock_project.id = mock_logstream.project_id
        mock_project.name = "Test Project"
        mock_project_class.get.return_value = mock_project

        log_stream = LogStream.get(name="Test Stream", project_id="test-project-id")
        project = log_stream.project

        mock_project_class.get.assert_called_once_with(id=mock_logstream.project_id)
        assert project == mock_project


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
