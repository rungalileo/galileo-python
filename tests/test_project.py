from datetime import datetime
from unittest.mock import MagicMock, patch
from uuid import uuid4

import pytest

from galileo.collaborator import Collaborator, CollaboratorRole
from galileo.project import Project
from galileo.shared.base import SyncState
from galileo.shared.exceptions import APIError, ResourceNotFoundError, ValidationError


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

    @patch("galileo.project.Projects")
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

    @patch("galileo.project.Projects")
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
    @patch("galileo.project.Projects")
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

    @patch("galileo.project.Projects")
    def test_get_raises_resource_not_found_by_name(
        self, mock_projects_class: MagicMock, reset_configuration: None
    ) -> None:
        # Given: the service returns None for the lookup
        mock_service = MagicMock()
        mock_projects_class.return_value = mock_service
        mock_service.get.return_value = None

        # When/Then: get() raises ResourceNotFoundError with the name in the message
        with pytest.raises(ResourceNotFoundError) as exc_info:
            Project.get(name="Nonexistent Project")

        assert isinstance(exc_info.value, ResourceNotFoundError)
        assert "name=" in str(exc_info.value)

    @patch("galileo.project.Projects")
    def test_get_raises_resource_not_found_by_id(
        self, mock_projects_class: MagicMock, reset_configuration: None
    ) -> None:
        # Given: the service returns None for the lookup
        mock_service = MagicMock()
        mock_projects_class.return_value = mock_service
        mock_service.get.return_value = None

        # When/Then: get() raises ResourceNotFoundError with the id in the message
        with pytest.raises(ResourceNotFoundError) as exc_info:
            Project.get(id="nonexistent-id-123")

        assert isinstance(exc_info.value, ResourceNotFoundError)
        assert "id=" in str(exc_info.value)

    @patch("galileo.project.Projects")
    def test_get_raises_error_for_api_failure(self, mock_projects_class: MagicMock, reset_configuration: None) -> None:
        """Test get() wraps API errors in APIError."""
        mock_service = MagicMock()
        mock_projects_class.return_value = mock_service
        mock_service.get.side_effect = Exception("API Error")

        with pytest.raises(APIError):
            Project.get(name="Test Project")


class TestProjectList:
    """Test suite for Project.list() class method."""

    @patch("galileo.project.Projects")
    def test_list_returns_all_projects(self, mock_projects_class: MagicMock, reset_configuration: None) -> None:
        """Test list() returns a list of synced project instances."""
        mock_service = MagicMock()
        mock_projects_class.return_value = mock_service

        mock_projects = []
        for i in range(3):
            mock_proj = MagicMock()
            mock_proj.id = str(uuid4())
            mock_proj.name = f"Project {i}"
            mock_proj.created_at = MagicMock()
            mock_proj.created_by = "user-1"
            mock_proj.updated_at = MagicMock()
            mock_proj.bookmark = False
            mock_proj.permissions = []
            mock_proj.type = None
            mock_projects.append(mock_proj)
        mock_service.list.return_value = mock_projects

        projects = Project.list()

        assert len(projects) == 3
        assert all(isinstance(p, Project) for p in projects)
        assert all(p.is_synced() for p in projects)


class TestProjectSave:
    """Test suite for Project.save() method."""

    @patch("galileo.project.Projects")
    def test_save_local_only_delegates_to_create(
        self, mock_projects_class: MagicMock, reset_configuration: None, mock_project: MagicMock
    ) -> None:
        # Given: a local-only project and a mocked create response
        mock_service = MagicMock()
        mock_projects_class.return_value = mock_service
        mock_service.create.return_value = mock_project

        # When: save() is called on a LOCAL_ONLY project
        project = Project(name="Test Project")
        result = project.save()

        # Then: create() is called and the project is synced
        mock_service.create.assert_called_once_with(name="Test Project")
        assert result.id == mock_project.id
        assert result.is_synced()

    @patch("galileo.project.Projects")
    def test_save_synced_is_noop(
        self, mock_projects_class: MagicMock, reset_configuration: None, mock_project: MagicMock
    ) -> None:
        # Given: a synced project
        mock_service = MagicMock()
        mock_projects_class.return_value = mock_service
        mock_service.get.return_value = mock_project

        project = Project.get(id=mock_project.id)
        assert project.is_synced()

        # When: save() is called
        result = project.save()

        # Then: no API update call is made and project remains synced
        mock_service.update.assert_not_called()
        assert result is project
        assert result.is_synced()

    def test_save_deleted_raises_value_error(self, reset_configuration: None) -> None:
        # Given: a project in DELETED state
        project = Project(name="Test Project")
        project.id = str(uuid4())
        project._set_state(SyncState.DELETED)

        # When/Then: save() raises ValueError
        with pytest.raises(ValueError, match="Cannot save a deleted project"):
            project.save()

    def test_save_without_id_raises_value_error(self, reset_configuration: None) -> None:
        # Given: a project in DIRTY state but with no ID
        project = Project(name="Test Project")
        project._set_state(SyncState.DIRTY)

        # When/Then: save() raises ValueError because there is no ID to update
        with pytest.raises(ValueError, match="Project ID is not set"):
            project.save()

    @patch("galileo.project.GalileoPythonConfig")
    @patch("galileo.project.update_project_projects_project_id_put")
    @patch("galileo.project.Projects")
    def test_save_dirty_calls_update_and_syncs_attributes(
        self,
        mock_projects_class: MagicMock,
        mock_update_put: MagicMock,
        mock_config_class: MagicMock,
        reset_configuration: None,
        mock_project: MagicMock,
    ) -> None:
        # Given: a synced project and a mocked API update response with all synced fields
        mock_service = MagicMock()
        mock_projects_class.return_value = mock_service
        mock_service.get.return_value = mock_project

        from galileo.resources.types import UNSET as RESOURCES_UNSET

        updated_at = MagicMock()
        updated_response = MagicMock()
        updated_response.id = mock_project.id
        updated_response.name = "Renamed Project"
        updated_response.created_at = mock_project.created_at
        updated_response.created_by = mock_project.created_by
        updated_response.updated_at = updated_at
        # Use UNSET for fields not returned by the update endpoint
        updated_response.type_ = RESOURCES_UNSET

        mock_detailed = MagicMock()
        mock_detailed.status_code = 200
        mock_detailed.parsed = updated_response
        mock_update_put.sync_detailed.return_value = mock_detailed

        project = Project.get(id=mock_project.id)
        assert project.is_synced()

        # When: the name is changed (triggers SYNCED → DIRTY automatically) and save() is called
        project.name = "Renamed Project"
        assert project.is_dirty(), "name change should transition SYNCED → DIRTY"

        result = project.save()

        # Then: the direct API call is made and synced fields are updated
        mock_update_put.sync_detailed.assert_called_once()
        assert result.name == "Renamed Project"
        assert result.updated_at == updated_at
        assert result.id == mock_project.id
        assert result.is_synced()

        # bookmark and permissions are NOT returned by the update endpoint,
        # so they should retain their values from the initial get()
        assert result.bookmark == mock_project.bookmark
        assert result.permissions == mock_project.permissions

    @patch("galileo.project.Projects")
    def test_save_failed_sync_raises_value_error(
        self, mock_projects_class: MagicMock, reset_configuration: None, mock_project: MagicMock
    ) -> None:
        # Given: a project in FAILED_SYNC state (e.g., from a prior failed operation)
        mock_service = MagicMock()
        mock_projects_class.return_value = mock_service
        mock_service.get.return_value = mock_project

        project = Project.get(id=mock_project.id)
        project._set_state(SyncState.FAILED_SYNC)

        # When/Then: save() raises ValueError directing user to refresh()
        with pytest.raises(ValueError, match="FAILED_SYNC"):
            project.save()

    @patch("galileo.project.GalileoPythonConfig")
    @patch("galileo.project.update_project_projects_project_id_put")
    @patch("galileo.project.Projects")
    def test_save_handles_api_failure(
        self,
        mock_projects_class: MagicMock,
        mock_update_put: MagicMock,
        mock_config_class: MagicMock,
        reset_configuration: None,
        mock_project: MagicMock,
    ) -> None:
        # Given: a synced project that has been dirtied, and an API that raises an error
        mock_service = MagicMock()
        mock_projects_class.return_value = mock_service
        mock_service.get.return_value = mock_project
        mock_update_put.sync_detailed.side_effect = RuntimeError("API error")

        project = Project.get(id=mock_project.id)
        # Trigger DIRTY via real user flow (name assignment)
        project.name = "Trigger Dirty"
        assert project.is_dirty()

        # When/Then: the exception propagates and state is FAILED_SYNC
        with pytest.raises(RuntimeError, match="API error"):
            project.save()

        assert project.sync_state == SyncState.FAILED_SYNC


class TestProjectDirtyTracking:
    """Test suite for Project dirty-tracking via __setattr__."""

    @patch("galileo.project.Projects")
    def test_dirty_tracking_transitions_on_name_change(
        self, mock_projects_class: MagicMock, reset_configuration: None, mock_project: MagicMock
    ) -> None:
        # Given: a synced project
        mock_service = MagicMock()
        mock_projects_class.return_value = mock_service
        mock_service.get.return_value = mock_project

        project = Project.get(id=mock_project.id)
        assert project.is_synced()

        # When: the name is changed to a different value
        project.name = "A Completely New Name"

        # Then: the state transitions to DIRTY
        assert project.is_dirty()
        assert project.name == "A Completely New Name"

    @patch("galileo.project.Projects")
    def test_dirty_tracking_noop_on_same_value(
        self, mock_projects_class: MagicMock, reset_configuration: None, mock_project: MagicMock
    ) -> None:
        # Given: a synced project
        mock_service = MagicMock()
        mock_projects_class.return_value = mock_service
        mock_service.get.return_value = mock_project

        project = Project.get(id=mock_project.id)
        original_name = project.name
        assert project.is_synced()

        # When: the name is assigned the same value
        project.name = original_name

        # Then: the state remains SYNCED (same-value assignment is a no-op)
        assert project.is_synced()


class TestProjectMethods:
    """Test suite for other Project methods."""

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


class TestProjectCollaborators:
    """Test suite for Project collaborator management methods."""

    @patch("galileo.project.Projects")
    def test_add_update_remove_collaborator(
        self,
        mock_projects_class: MagicMock,
        reset_configuration: None,
        mock_project: MagicMock,
        mock_collaborator: MagicMock,
    ) -> None:
        """Test add, update, and remove collaborator return Collaborator instances."""
        mock_service = MagicMock()
        mock_projects_class.return_value = mock_service
        mock_service.get.return_value = mock_project
        mock_service.share_project_with_user.return_value = mock_collaborator
        mock_service.update_user_project_collaborator.return_value = mock_collaborator

        project = Project.get(id=mock_project.id)

        added = project.add_collaborator(user_id=mock_collaborator.user_id)
        assert isinstance(added, Collaborator)

        updated = project.update_collaborator(user_id=mock_collaborator.user_id, role=CollaboratorRole.EDITOR)
        assert isinstance(updated, Collaborator)

        project.remove_collaborator(user_id=mock_collaborator.user_id)
        mock_service.unshare_project_with_user.assert_called_once()

    @patch("galileo.project.Projects")
    def test_collaborators_property_returns_same_as_list_method(
        self,
        mock_projects_class: MagicMock,
        reset_configuration: None,
        mock_project: MagicMock,
        mock_collaborator: MagicMock,
    ) -> None:
        """Test collaborators property returns equivalent results to list_collaborators()."""
        mock_service = MagicMock()
        mock_projects_class.return_value = mock_service
        mock_service.get.return_value = mock_project
        mock_service.list_user_project_collaborators.return_value = [mock_collaborator]

        project = Project.get(id=mock_project.id)

        assert project.collaborators[0] == project.list_collaborators()[0]

    def test_collaborator_methods_require_synced_project(self, reset_configuration: None) -> None:
        """Test collaborator methods raise ValueError for local-only projects."""
        project = Project(name="Test Project")

        with pytest.raises(ValueError, match="Project ID is not set"):
            project.list_collaborators()

        with pytest.raises(ValueError, match="Project ID is not set"):
            project.add_collaborator(user_id="user-123")

        with pytest.raises(ValueError, match="Project ID is not set"):
            project.update_collaborator(user_id="user-123", role=CollaboratorRole.EDITOR)

        with pytest.raises(ValueError, match="Project ID is not set"):
            project.remove_collaborator(user_id="user-123")


class TestProjectRefresh:
    """Test suite for Project.refresh() method."""

    @patch("galileo.project.Projects")
    def test_refresh_raises_resource_not_found_when_project_deleted(
        self, mock_projects_class: MagicMock, reset_configuration: None, mock_project: MagicMock
    ) -> None:
        # Given: a synced project whose remote record has been deleted
        mock_service = MagicMock()
        mock_projects_class.return_value = mock_service
        mock_service.get.return_value = mock_project

        project = Project.get(id=mock_project.id)
        assert project.is_synced()

        # Simulate remote deletion
        mock_service.get.return_value = None

        # When/Then: refresh() raises ResourceNotFoundError and sets FAILED_SYNC
        with pytest.raises(ResourceNotFoundError) as exc_info:
            project.refresh()

        assert isinstance(exc_info.value, ResourceNotFoundError)
        assert "id=" in str(exc_info.value)
        assert project.sync_state == SyncState.FAILED_SYNC


class TestCollaborator:
    """Test suite for Collaborator class methods."""

    def test_collaborator_immutability_setattr(self, reset_configuration: None, mock_collaborator: MagicMock) -> None:
        """Test that Collaborator objects are immutable via __setattr__."""
        collab = Collaborator(
            id=mock_collaborator.id,
            user_id=mock_collaborator.user_id,
            project_id="project-123",
            role=CollaboratorRole.VIEWER,
            email=mock_collaborator.email,
        )

        with pytest.raises(AttributeError, match="Collaborator objects are immutable"):
            collab.role = CollaboratorRole.EDITOR

    def test_collaborator_immutability_delattr(self, reset_configuration: None, mock_collaborator: MagicMock) -> None:
        """Test that Collaborator objects prevent attribute deletion via __delattr__."""
        collab = Collaborator(
            id=mock_collaborator.id,
            user_id=mock_collaborator.user_id,
            project_id="project-123",
            role=CollaboratorRole.VIEWER,
            email=mock_collaborator.email,
        )

        with pytest.raises(AttributeError, match="Collaborator objects are immutable"):
            delattr(collab, "role")

    def test_collaborator_hash(self, reset_configuration: None, mock_collaborator: MagicMock) -> None:
        """Test that Collaborator objects are hashable based on user_id and project_id."""
        collab1 = Collaborator(
            id=mock_collaborator.id,
            user_id=mock_collaborator.user_id,
            project_id="project-123",
            role=CollaboratorRole.VIEWER,
        )

        collab2 = Collaborator(
            id="different-id", user_id=mock_collaborator.user_id, project_id="project-123", role=CollaboratorRole.EDITOR
        )

        collab3 = Collaborator(
            id=mock_collaborator.id, user_id="different-user", project_id="project-123", role=CollaboratorRole.VIEWER
        )

        # Same user_id and project_id should have same hash
        assert hash(collab1) == hash(collab2)

        # Different user_id should have different hash
        assert hash(collab1) != hash(collab3)

        # Can be used in sets
        collaborator_set = {collab1, collab2, collab3}
        assert len(collaborator_set) == 2  # collab1 and collab2 are equal

    def test_collaborator_to_dict(self, reset_configuration: None, mock_collaborator: MagicMock) -> None:
        """Test that to_dict() returns correct dictionary representation."""
        created_at = datetime(2024, 1, 1, 12, 0, 0)
        collab = Collaborator(
            id=mock_collaborator.id,
            user_id=mock_collaborator.user_id,
            project_id="project-123",
            role=CollaboratorRole.EDITOR,
            created_at=created_at,
            email="test@example.com",
            first_name="Test",
            last_name="User",
            permissions=["update", "delete"],
        )

        result = collab.to_dict()

        assert result["id"] == mock_collaborator.id
        assert result["user_id"] == mock_collaborator.user_id
        assert result["project_id"] == "project-123"
        assert result["role"] == CollaboratorRole.EDITOR.value
        assert result["created_at"] == created_at.isoformat()
        assert result["email"] == "test@example.com"
        assert result["first_name"] == "Test"
        assert result["last_name"] == "User"
        assert result["permissions"] == ["update", "delete"]

    def test_collaborator_to_dict_with_none_values(
        self, reset_configuration: None, mock_collaborator: MagicMock
    ) -> None:
        """Test that to_dict() handles None values correctly."""
        collab = Collaborator(
            id=mock_collaborator.id,
            user_id=mock_collaborator.user_id,
            project_id="project-123",
            role=CollaboratorRole.VIEWER,
            created_at=None,
            email=None,
            first_name=None,
            last_name=None,
            permissions=None,
        )

        result = collab.to_dict()

        assert result["created_at"] is None
        assert result["email"] is None
        assert result["first_name"] is None
        assert result["last_name"] is None
        assert result["permissions"] is None

    @patch("galileo.collaborator.Projects")
    def test_collaborator_update_error_path(
        self, mock_projects_class: MagicMock, reset_configuration: None, mock_collaborator: MagicMock
    ) -> None:
        """Test that Collaborator.update() raises exception on API failure."""
        mock_service = MagicMock()
        mock_projects_class.return_value = mock_service
        mock_service.update_user_project_collaborator.side_effect = Exception("API Error")

        collab = Collaborator(
            id=mock_collaborator.id,
            user_id=mock_collaborator.user_id,
            project_id="project-123",
            role=CollaboratorRole.VIEWER,
        )

        with pytest.raises(Exception, match="API Error"):
            collab.update(role=CollaboratorRole.EDITOR)

    @patch("galileo.collaborator.Projects")
    def test_collaborator_remove_error_path(
        self, mock_projects_class: MagicMock, reset_configuration: None, mock_collaborator: MagicMock
    ) -> None:
        """Test that Collaborator.remove() raises exception on API failure."""
        mock_service = MagicMock()
        mock_projects_class.return_value = mock_service
        mock_service.unshare_project_with_user.side_effect = Exception("API Error")

        collab = Collaborator(
            id=mock_collaborator.id,
            user_id=mock_collaborator.user_id,
            project_id="project-123",
            role=CollaboratorRole.VIEWER,
        )

        with pytest.raises(Exception, match="API Error"):
            collab.remove()

    def test_collaborator_equality(self, reset_configuration: None, mock_collaborator: MagicMock) -> None:
        """Test that Collaborator equality is based on user_id and project_id."""
        collab1 = Collaborator(
            id=mock_collaborator.id,
            user_id=mock_collaborator.user_id,
            project_id="project-123",
            role=CollaboratorRole.VIEWER,
        )

        collab2 = Collaborator(
            id="different-id", user_id=mock_collaborator.user_id, project_id="project-123", role=CollaboratorRole.EDITOR
        )

        collab3 = Collaborator(
            id=mock_collaborator.id, user_id="different-user", project_id="project-123", role=CollaboratorRole.VIEWER
        )

        # Same user_id and project_id should be equal
        assert collab1 == collab2

        # Different user_id should not be equal
        assert collab1 != collab3

        # Not equal to non-Collaborator objects
        assert collab1 != "not a collaborator"
        # Test that __eq__ returns False for None (non-Collaborator)
        none_obj = None
        assert collab1 != none_obj

    @pytest.mark.parametrize(
        "input_permissions,expected_permissions,description",
        [
            pytest.param([], None, "empty list becomes None (no permissions data available)", id="empty_list"),
            pytest.param(
                "mock_permission_list",  # Sentinel to create mock permissions in test
                [{"action": "update", "allowed": True, "message": "User can update"}],
                "non-empty permissions converted to list of dicts",
                id="with_data",
            ),
        ],
    )
    def test_from_api_response_permissions_handling(
        self,
        reset_configuration: None,
        mock_collaborator: MagicMock,
        input_permissions: list | str,
        expected_permissions: list | None,
        description: str,
    ) -> None:
        """Test that _from_api_response handles permissions correctly.

        Note: The API model normalizes missing permissions to an empty list,
        so we cannot distinguish between "field omitted" and "explicitly empty".
        Both cases result in permissions=None in the Collaborator object.

        - [] (empty or omitted) -> None
        - [Permission(...)] (non-empty) -> list of dicts
        """
        # Handle the mock_permission_list sentinel
        if input_permissions == "mock_permission_list":
            mock_permission = MagicMock()
            mock_permission.action = "update"
            mock_permission.allowed = True
            mock_permission.message = "User can update"
            input_permissions = [mock_permission]

        mock_response = MagicMock()
        mock_response.id = mock_collaborator.id
        mock_response.user_id = mock_collaborator.user_id
        mock_response.role = CollaboratorRole.VIEWER
        mock_response.email = mock_collaborator.email
        mock_response.created_at = datetime(2024, 1, 1, 12, 0, 0)
        mock_response.first_name = "Test"
        mock_response.last_name = "User"
        mock_response.permissions = input_permissions

        collab = Collaborator._from_api_response(mock_response, project_id="project-123")

        assert collab.permissions == expected_permissions, description
