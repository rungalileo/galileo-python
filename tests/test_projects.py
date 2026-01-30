import os
from unittest.mock import ANY, Mock, patch

import httpx
import pytest

from galileo.projects import Projects, ProjectsAPIException, delete_project
from galileo.resources.models.project_type import ProjectType


@pytest.fixture(autouse=True)
def reset_env_vars() -> None:
    os.environ.pop("GALILEO_PROJECT", None)
    os.environ.pop("GALILEO_PROJECT_ID", None)


class TestProjects:
    @patch("galileo.projects.get_all_projects_projects_all_get")
    def test_get_all_projects_projects_all_get_exc(self, get_all_projects_projects_all_get) -> None:
        """Test that list raises ValueError when API call fails."""
        get_all_projects_projects_all_get.sync.side_effect = ValueError("unable to get all projects")

        projects_client = Projects()

        with pytest.raises(ValueError) as exc_info:
            projects_client.list()

        assert "unable to get all projects" in str(exc_info.value)

    def test_get_project_with_no_name_or_id_raises_value_error(self) -> None:
        projects_client = Projects()

        try:
            projects_client.get()
        except ValueError as e:
            assert str(e) == "Exactly one of 'id' or 'name' must be provided."

    def test_get_project_with_name_and_id_raises_value_error(self) -> None:
        projects_client = Projects()

        try:
            projects_client.get(id="123", name="my_project")
        except ValueError as e:
            assert str(e) == "Exactly one of 'id' or 'name' must be provided."

    def test_get_project_with_empty_name_and_id_raises_value_error(self) -> None:
        projects_client = Projects()

        try:
            projects_client.get(id="", name="")
        except ValueError as e:
            assert str(e) == "Exactly one of 'id' or 'name' must be provided."

    @patch("galileo.projects.get_project_projects_project_id_get.sync_detailed")
    def test_get_project_with_id_gets_project_by_id(self, get_project_projects_project_id_get: Mock) -> None:
        # Mock a successful response with parsed project data
        mock_response = Mock()
        mock_response.status_code = httpx.codes.OK
        mock_response.parsed = None  # No project found
        get_project_projects_project_id_get.return_value = mock_response

        result = Projects().get(id="123")
        get_project_projects_project_id_get.assert_called_once_with(project_id="123", client=ANY)
        assert result is None

    @patch("galileo.projects.get_project_projects_project_id_get.sync_detailed")
    def test_get_project_with_id_with_whitespace_env_vars_gets_project_by_id(
        self, get_project_projects_project_id_get: Mock
    ) -> None:
        mock_response = Mock()
        mock_response.status_code = httpx.codes.OK
        mock_response.parsed = None
        get_project_projects_project_id_get.return_value = mock_response

        with patch.dict("os.environ", {"GALILEO_PROJECT": "  "}):
            with patch.dict("os.environ", {"GALILEO_PROJECT_ID": "  "}):
                result = Projects().get_with_env_fallbacks(id="123")
                get_project_projects_project_id_get.assert_called_once_with(project_id="123", client=ANY)
                assert result is None

    @patch("galileo.projects.get_project_projects_project_id_get.sync_detailed")
    def test_get_project_with_id_from_env_var_gets_project_by_id(
        self, get_project_projects_project_id_get: Mock
    ) -> None:
        mock_response = Mock()
        mock_response.status_code = httpx.codes.OK
        mock_response.parsed = None
        get_project_projects_project_id_get.return_value = mock_response

        with patch.dict("os.environ", {"GALILEO_PROJECT_ID": "123"}):
            result = Projects().get_with_env_fallbacks()
            get_project_projects_project_id_get.assert_called_once_with(project_id="123", client=ANY)
            assert result is None

    @patch("galileo.projects.get_projects_projects_get.sync_detailed")
    def test_get_project_with_name_gets_project_by_name(self, get_projects_projects_get: Mock) -> None:
        mock_response = Mock()
        mock_response.status_code = httpx.codes.OK
        mock_response.parsed = []  # No projects found
        get_projects_projects_get.return_value = mock_response

        result = Projects().get(name="my_project")
        get_projects_projects_get.assert_called_once_with(project_name="my_project", client=ANY, type_=ANY)
        assert result is None

    @patch("galileo.projects.get_projects_projects_get.sync_detailed")
    def test_get_project_with_name_with_whitespace_env_vars_gets_project_by_name(
        self, get_projects_projects_get: Mock
    ) -> None:
        mock_response = Mock()
        mock_response.status_code = httpx.codes.OK
        mock_response.parsed = []
        get_projects_projects_get.return_value = mock_response

        with patch.dict("os.environ", {"GALILEO_PROJECT": "  "}):
            with patch.dict("os.environ", {"GALILEO_PROJECT_ID": "  "}):
                result = Projects().get_with_env_fallbacks(name="my_project")
                get_projects_projects_get.assert_called_once_with(project_name="my_project", client=ANY, type_=ANY)
                assert result is None

    @patch("galileo.projects.get_projects_projects_get.sync_detailed")
    def test_get_project_with_name_from_env_var_gets_project_by_name(self, get_projects_projects_get: Mock) -> None:
        os.environ.pop("GALILEO_PROJECT_ID", None)
        mock_response = Mock()
        mock_response.status_code = httpx.codes.OK
        mock_response.parsed = []
        get_projects_projects_get.return_value = mock_response

        with patch.dict("os.environ", {"GALILEO_PROJECT": "my_project"}):
            result = Projects().get_with_env_fallbacks()
            get_projects_projects_get.assert_called_once_with(project_name="my_project", client=ANY, type_=ANY)
            assert result is None

    @patch("galileo.projects.create_user_project_collaborators_projects_project_id_users_post.sync")
    def test_share_project_with_user(self, mock_create_user_project_collaborators):
        mock_create_user_project_collaborators.return_value = [Mock()]
        projects_client = Projects()
        projects_client.share_project_with_user(project_id="123", user_id="456")
        mock_create_user_project_collaborators.assert_called_once_with(project_id="123", client=ANY, body=ANY)

    @patch("galileo.projects.create_user_project_collaborators_projects_project_id_users_post.sync")
    def test_share_project_with_user_error(self, mock_create_user_project_collaborators):
        """Test that share_project_with_user raises ValueError when the API call returns None."""
        mock_create_user_project_collaborators.return_value = None
        projects_client = Projects()

        with pytest.raises(ValueError) as exc_info:
            projects_client.share_project_with_user(project_id="123", user_id="456")

        assert "Failed to share project 123 with user 456" in str(exc_info.value)

    @patch("galileo.projects.delete_user_project_collaborator_projects_project_id_users_user_id_delete.sync")
    def test_unshare_project_with_user(self, mock_delete_user_project_collaborator):
        mock_delete_user_project_collaborator.return_value = True
        projects_client = Projects()
        projects_client.unshare_project_with_user(project_id="123", user_id="456")
        mock_delete_user_project_collaborator.assert_called_once_with(project_id="123", user_id="456", client=ANY)

    @patch("galileo.projects.delete_user_project_collaborator_projects_project_id_users_user_id_delete.sync")
    def test_unshare_project_with_user_error(self, mock_delete_user_project_collaborator):
        """Test that unshare_project_with_user raises ValueError when the API call returns None."""
        mock_delete_user_project_collaborator.return_value = None
        projects_client = Projects()

        with pytest.raises(ValueError) as exc_info:
            projects_client.unshare_project_with_user(project_id="123", user_id="456")

        assert "Failed to unshare project 123 with user 456" in str(exc_info.value)

    @patch("galileo.projects.list_user_project_collaborators_projects_project_id_users_get.sync")
    def test_list_user_project_collaborators(self, mock_list_user_project_collaborators):
        mock_list_user_project_collaborators.side_effect = [
            Mock(collaborators=[Mock()], paginated=True, next_starting_token=1),
            Mock(collaborators=[Mock()], paginated=False, next_starting_token=None),
        ]
        projects_client = Projects()
        collaborators = projects_client.list_user_project_collaborators(project_id="123")
        assert len(collaborators) == 2
        assert mock_list_user_project_collaborators.call_count == 2

    @patch("galileo.projects.list_user_project_collaborators_projects_project_id_users_get.sync")
    def test_list_user_project_collaborators_error(self, mock_list_user_project_collaborators):
        """Test that list_user_project_collaborators raises ValueError when the API call returns None."""
        mock_list_user_project_collaborators.return_value = None
        projects_client = Projects()

        with pytest.raises(ValueError) as exc_info:
            projects_client.list_user_project_collaborators(project_id="123")

        assert "Failed to list collaborators for project 123" in str(exc_info.value)

    @patch("galileo.projects.update_user_project_collaborator_projects_project_id_users_user_id_patch.sync")
    def test_update_user_project_collaborator(self, mock_update_user_project_collaborator):
        projects_client = Projects()
        projects_client.update_user_project_collaborator(project_id="123", user_id="456")
        mock_update_user_project_collaborator.assert_called_once_with(
            project_id="123", user_id="456", client=ANY, body=ANY
        )

    @patch("galileo.projects.update_user_project_collaborator_projects_project_id_users_user_id_patch.sync")
    def test_update_user_project_collaborator_error(self, mock_update_user_project_collaborator):
        """Test that update_user_project_collaborator raises ValueError when the API call returns None."""
        mock_update_user_project_collaborator.return_value = None
        projects_client = Projects()

        with pytest.raises(ValueError) as exc_info:
            projects_client.update_user_project_collaborator(project_id="123", user_id="456")

        assert "Failed to update collaborator for project 123" in str(exc_info.value)

    # Delete Project Tests
    def test_delete_project_with_no_name_or_id_raises_value_error(self) -> None:
        """Test that delete_project raises ValueError when neither id nor name is provided."""
        with pytest.raises(ValueError) as exc_info:
            Projects().delete_project()

        assert "Exactly one of 'id' or 'name' must be provided." in str(exc_info.value)

    def test_delete_project_with_both_name_and_id_raises_value_error(self) -> None:
        """Test that delete_project raises ValueError when both id and name are provided."""
        with pytest.raises(ValueError) as exc_info:
            Projects().delete_project(id="123", name="my_project")

        assert "Exactly one of 'id' or 'name' must be provided." in str(exc_info.value)

    def test_delete_project_with_empty_name_and_id_raises_value_error(self) -> None:
        """Test that delete_project raises ValueError when both id and name are empty strings."""
        with pytest.raises(ValueError) as exc_info:
            Projects().delete_project(id="", name="")

        assert "Exactly one of 'id' or 'name' must be provided." in str(exc_info.value)

    @patch("galileo.projects.delete_project_projects_project_id_delete.sync_detailed")
    @patch("galileo.projects.Projects.get")
    def test_delete_project_with_id_deletes_project_by_id(self, get_mock: Mock, delete_project_mock: Mock) -> None:
        # Mock the get method to return a project with the expected ID
        mock_project = Mock()
        mock_project.id = "123"
        mock_project.type = ProjectType.GEN_AI
        mock_project.name = "test_project"

        get_mock.return_value = mock_project

        # Mock successful deletion response
        mock_response = Mock()
        mock_response.status_code = httpx.codes.OK
        mock_response.parsed = Mock()
        delete_project_mock.return_value = mock_response

        result = Projects().delete_project(id="123")
        delete_project_mock.assert_called_once_with(project_id="123", client=ANY)
        assert result is True

    @patch("galileo.projects.delete_project_projects_project_id_delete.sync_detailed")
    @patch("galileo.projects.Projects.get")
    def test_delete_project_with_name_deletes_project_by_name(self, get_mock: Mock, delete_project_mock: Mock) -> None:
        # Mock the get method to return a project with the expected ID
        mock_project = Mock()
        mock_project.id = "456"
        mock_project.type = ProjectType.GEN_AI
        mock_project.name = "my_project"

        get_mock.return_value = mock_project

        # Mock successful deletion response
        mock_response = Mock()
        mock_response.status_code = httpx.codes.OK
        mock_response.parsed = Mock()
        delete_project_mock.return_value = mock_response

        result = Projects().delete_project(name="my_project")
        delete_project_mock.assert_called_once_with(project_id="456", client=ANY)
        assert result is True

    @patch("galileo.projects.Projects.get")
    def test_delete_project_with_non_genai_project_raises_api_exception(self, get_mock: Mock) -> None:
        """Test that delete_project raises ProjectsAPIException when project is not GEN_AI type."""
        # Mock the get method to return a non-GEN_AI project
        mock_project = Mock()
        mock_project.id = "123"
        mock_project.type = ProjectType.LLM_MONITOR  # Not GEN_AI
        mock_project.name = "test_project"

        get_mock.return_value = mock_project

        with pytest.raises(ProjectsAPIException) as exc_info:
            Projects().delete_project(id="123")

        assert "is not a gen_ai project" in str(exc_info.value)

    @patch("galileo.projects.Projects.get")
    def test_delete_project_with_nonexistent_project_raises_value_error(self, get_mock: Mock) -> None:
        """Test that delete_project raises ValueError when project doesn't exist."""
        # Mock the get method to return None (project not found)
        get_mock.return_value = None

        with pytest.raises(ValueError) as exc_info:
            Projects().delete_project(id="nonexistent-id")

        assert "not found" in str(exc_info.value)


class TestDeleteProjectConvenienceFunction:
    """Tests for the delete_project convenience function that wraps Projects().delete_project()."""

    def test_delete_project_convenience_with_no_name_or_id_raises_value_error(self) -> None:
        """Test that delete_project convenience function raises ValueError when neither id nor name is provided."""
        with pytest.raises(ValueError) as exc_info:
            delete_project(id="", name="")

        assert "Exactly one of 'id' or 'name' must be provided." in str(exc_info.value)

    def test_delete_project_convenience_with_both_name_and_id_raises_value_error(self) -> None:
        """Test that delete_project convenience function raises ValueError when both id and name are provided."""
        with pytest.raises(ValueError) as exc_info:
            delete_project(id="123", name="my_project")

        assert "Exactly one of 'id' or 'name' must be provided." in str(exc_info.value)

    @patch("galileo.projects.Projects.get")
    def test_delete_project_convenience_with_nonexistent_project_raises_value_error(self, get_mock: Mock) -> None:
        """Test that delete_project convenience function raises ValueError when project doesn't exist."""
        # Mock the get method to return None (project not found)
        get_mock.return_value = None

        with pytest.raises(ValueError) as exc_info:
            delete_project(name="nonexistent-project")

        assert "not found" in str(exc_info.value)

    @patch("galileo.projects.delete_project_projects_project_id_delete.sync_detailed")
    @patch("galileo.projects.Projects.get")
    def test_delete_project_convenience_successful_deletion_returns_true(
        self, get_mock: Mock, delete_project_mock: Mock
    ) -> None:
        """Test that delete_project convenience function returns True on successful deletion."""
        # Mock the get method to return a project
        mock_project = Mock()
        mock_project.id = "123"
        mock_project.type = ProjectType.GEN_AI
        mock_project.name = "test_project"

        get_mock.return_value = mock_project

        # Mock successful deletion response
        mock_response = Mock()
        mock_response.status_code = httpx.codes.OK
        mock_response.parsed = Mock()
        delete_project_mock.return_value = mock_response

        result = delete_project(id="123")

        assert result is True
        delete_project_mock.assert_called_once_with(project_id="123", client=ANY)
