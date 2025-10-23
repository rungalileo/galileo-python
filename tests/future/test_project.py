from unittest.mock import MagicMock, patch
from uuid import uuid4

import pytest

from galileo.__future__ import Project
from galileo.__future__.base import SyncState
from galileo.__future__.exceptions import APIError, ValidationError


class TestProjectInitialization:
    """Test suite for Project initialization."""

    def test_init_with_name_creates_local_only_project(self, reset_configuration: None) -> None:
        """Test initializing a project with a name creates a local-only instance."""
        project = Project(name="Test Project")

        assert project.name == "Test Project"
        assert project.id is None
        assert project.sync_state == SyncState.LOCAL_ONLY

    def test_init_without_name_raises_validation_error(self, reset_configuration: None) -> None:
        """Test initializing a project without a name raises ValidationError."""
        with pytest.raises(ValidationError, match="'name' must be provided"):
            Project(name=None)


class TestProjectCreate:
    """Test suite for Project.create() method."""

    @patch("galileo.__future__.project.Projects")
    def test_create_persists_project_to_api(
        self, mock_projects_class: MagicMock, reset_configuration: None, mock_project: MagicMock
    ) -> None:
        """Test create() persists the project to the API and updates attributes."""
        mock_service = MagicMock()
        mock_projects_class.return_value = mock_service
        mock_service.create.return_value = mock_project

        project = Project(name="Test Project").create()

        mock_service.create.assert_called_once_with(name="Test Project")
        assert project.id == mock_project.id
        assert project.is_synced()

    @patch("galileo.__future__.project.Projects")
    def test_create_handles_api_failure(self, mock_projects_class: MagicMock, reset_configuration: None) -> None:
        """Test create() handles API failures and sets state correctly."""
        mock_service = MagicMock()
        mock_projects_class.return_value = mock_service
        mock_service.create.side_effect = Exception("API Error")

        project = Project(name="Test Project")

        with pytest.raises(Exception, match="API Error"):
            project.create()

        assert project.sync_state == SyncState.FAILED_SYNC


class TestProjectGet:
    """Test suite for Project.get() class method."""

    @pytest.mark.parametrize("lookup_key,lookup_value", [("name", "Test Project"), ("id", "test-project-id-123")])
    @patch("galileo.__future__.project.Projects")
    def test_get_returns_project(
        self,
        mock_projects_class: MagicMock,
        lookup_key: str,
        lookup_value: str,
        reset_configuration: None,
        mock_project: MagicMock,
    ) -> None:
        """Test get() with name or id returns a synced project instance."""
        mock_service = MagicMock()
        mock_projects_class.return_value = mock_service
        mock_project.id = lookup_value if lookup_key == "id" else mock_project.id
        mock_project.name = lookup_value if lookup_key == "name" else mock_project.name
        mock_service.get.return_value = mock_project

        project = Project.get(**{lookup_key: lookup_value})

        assert project is not None
        assert project.is_synced()

    @patch("galileo.__future__.project.Projects")
    def test_get_returns_none_when_not_found(self, mock_projects_class: MagicMock, reset_configuration: None) -> None:
        """Test get() returns None when project is not found."""
        mock_service = MagicMock()
        mock_projects_class.return_value = mock_service
        mock_service.get.return_value = None

        project = Project.get(name="Nonexistent Project")

        assert project is None

    @patch("galileo.__future__.project.Projects")
    def test_get_handles_api_error(self, mock_projects_class: MagicMock, reset_configuration: None) -> None:
        """Test get() wraps API errors in APIError."""
        mock_service = MagicMock()
        mock_projects_class.return_value = mock_service
        mock_service.get.side_effect = Exception("API Error")

        with pytest.raises(APIError, match="Failed to retrieve project"):
            Project.get(name="Test Project")


class TestProjectList:
    """Test suite for Project.list() class method."""

    @patch("galileo.__future__.project.Projects")
    def test_list_returns_all_projects(self, mock_projects_class: MagicMock, reset_configuration: None) -> None:
        """Test list() returns a list of synced project instances."""
        mock_service = MagicMock()
        mock_projects_class.return_value = mock_service

        # Create 3 mock projects
        mock_projects = []
        for i in range(3):
            mock_proj = MagicMock()
            mock_proj.id = str(uuid4())
            mock_proj.name = f"Project {i}"
            mock_proj.created_at = MagicMock()
            mock_proj.created_by = str(uuid4())
            mock_proj.updated_at = MagicMock()
            mock_proj.bookmark = None
            mock_proj.permissions = None
            mock_proj.type = None
            mock_projects.append(mock_proj)
        mock_service.list.return_value = mock_projects

        projects = Project.list()

        assert len(projects) == 3
        assert all(isinstance(p, Project) for p in projects)
        assert all(p.is_synced() for p in projects)


class TestProjectLogStreams:
    """Test suite for project log stream management."""

    @patch("galileo.__future__.log_stream.LogStreams")
    @patch("galileo.__future__.project.Projects")
    def test_create_log_stream(
        self,
        mock_projects_class: MagicMock,
        mock_logstreams_class: MagicMock,
        reset_configuration: None,
        mock_project: MagicMock,
        mock_logstream: MagicMock,
    ) -> None:
        """Test create_log_stream() creates a log stream and returns it."""
        mock_project_service = MagicMock()
        mock_projects_class.return_value = mock_project_service
        mock_project_service.get.return_value = mock_project

        mock_logstream_service = MagicMock()
        mock_logstreams_class.return_value = mock_logstream_service
        mock_logstream.project_id = mock_project.id
        mock_logstream_service.create.return_value = mock_logstream

        project = Project.get(id=mock_project.id)
        log_stream = project.create_log_stream(name="Test Stream")

        mock_logstream_service.create.assert_called_once_with(
            name="Test Stream", project_id=mock_project.id, project_name=None
        )
        assert log_stream.name == "Test Stream"
        assert log_stream.project_id == mock_project.id

    def test_create_log_stream_raises_error_for_local_only_project(self, reset_configuration: None) -> None:
        """Test create_log_stream() raises ValueError for local-only project."""
        project = Project(name="Test Project")

        with pytest.raises(ValueError, match="Project ID is not set"):
            project.create_log_stream(name="Test Stream")

    @patch("galileo.__future__.log_stream.LogStreams")
    @patch("galileo.__future__.project.Projects")
    def test_list_log_streams(
        self,
        mock_projects_class: MagicMock,
        mock_logstreams_class: MagicMock,
        reset_configuration: None,
        mock_project: MagicMock,
    ) -> None:
        """Test list_log_streams() returns all log streams for the project."""
        mock_project_service = MagicMock()
        mock_projects_class.return_value = mock_project_service
        mock_project_service.get.return_value = mock_project

        mock_logstream_service = MagicMock()
        mock_logstreams_class.return_value = mock_logstream_service
        mock_logstreams = []
        for i in range(3):
            mock_ls = MagicMock()
            mock_ls.id = str(uuid4())
            mock_ls.name = f"Stream {i}"
            mock_ls.project_id = mock_project.id
            mock_ls.created_at = MagicMock()
            mock_ls.created_by = str(uuid4())
            mock_ls.updated_at = MagicMock()
            mock_ls.additional_properties = {}
            mock_logstreams.append(mock_ls)
        mock_logstream_service.list.return_value = mock_logstreams

        project = Project.get(id=mock_project.id)
        log_streams = project.list_log_streams()

        assert len(log_streams) == 3
        assert all(ls.project_id == mock_project.id for ls in log_streams)


class TestProjectRefresh:
    """Test suite for Project.refresh() method."""

    @patch("galileo.__future__.project.Projects")
    def test_refresh_updates_attributes_from_api(
        self, mock_projects_class: MagicMock, reset_configuration: None
    ) -> None:
        """Test refresh() updates all attributes from the API."""
        mock_service = MagicMock()
        mock_projects_class.return_value = mock_service

        project_id = str(uuid4())
        initial_project = MagicMock()
        initial_project.id = project_id
        initial_project.name = "Old Name"
        initial_project.created_at = MagicMock()
        initial_project.created_by = str(uuid4())
        initial_project.updated_at = MagicMock()
        initial_project.bookmark = None
        initial_project.permissions = None
        initial_project.type = None

        updated_project = MagicMock()
        updated_project.id = project_id
        updated_project.name = "New Name"
        updated_project.created_at = initial_project.created_at
        updated_project.created_by = initial_project.created_by
        updated_project.updated_at = MagicMock()
        updated_project.bookmark = None
        updated_project.permissions = None
        updated_project.type = None

        mock_service.get.side_effect = [initial_project, updated_project]

        project = Project.get(id=project_id)
        assert project.name == "Old Name"

        project.refresh()

        assert project.name == "New Name"
        assert project.is_synced()

    def test_refresh_raises_error_for_local_only_project(self, reset_configuration: None) -> None:
        """Test refresh() raises ValueError for local-only project."""
        project = Project(name="Test Project")

        with pytest.raises(ValueError, match="Project ID is not set"):
            project.refresh()

    @patch("galileo.__future__.project.Projects")
    def test_refresh_raises_error_if_project_no_longer_exists(
        self, mock_projects_class: MagicMock, reset_configuration: None, mock_project: MagicMock
    ) -> None:
        """Test refresh() raises ValueError if project no longer exists."""
        mock_service = MagicMock()
        mock_projects_class.return_value = mock_service
        mock_service.get.side_effect = [mock_project, None]

        project = Project.get(id=mock_project.id)

        with pytest.raises(ValueError, match="no longer exists"):
            project.refresh()

        assert project.sync_state == SyncState.FAILED_SYNC


class TestProjectMethods:
    """Test suite for other Project methods."""

    def test_save_raises_not_implemented_error(self, reset_configuration: None) -> None:
        """Test save() raises NotImplementedError."""
        project = Project(name="Test Project")

        with pytest.raises(NotImplementedError, match="not yet implemented"):
            project.save()

    def test_str_representation(self, reset_configuration: None) -> None:
        """Test __str__ returns expected format."""
        project = Project(name="Test Project")
        project.id = "test-id-123"

        assert str(project) == "Project(name='Test Project', id='test-id-123')"

    def test_repr_representation(self, reset_configuration: None) -> None:
        """Test __repr__ returns expected format with created_at."""
        project = Project(name="Test Project")
        project.id = "test-id-123"
        project.created_at = "2024-01-01 12:00:00"

        assert "Test Project" in repr(project)
        assert "test-id-123" in repr(project)
