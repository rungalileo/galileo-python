import logging
import os
from unittest.mock import ANY, Mock, patch

import httpx
import pytest

from galileo.projects import Projects, delete_project
from galileo.resources.models.project_type import ProjectType


@pytest.fixture(autouse=True)
def reset_env_vars() -> None:
    os.environ.pop("GALILEO_PROJECT", None)
    os.environ.pop("GALILEO_PROJECT_ID", None)


class TestProjects:
    @patch("galileo.projects.get_all_projects_projects_all_get")
    def test_get_all_projects_projects_all_get_exc(
        self, get_all_projects_projects_all_get, caplog, enable_galileo_logging
    ) -> None:
        get_all_projects_projects_all_get.sync.side_effect = ValueError("unable to get all projects")

        projects_client = Projects()
        # It doesn't throw exception because we catch all and log
        projects_client.list()

        with caplog.at_level(logging.WARNING):
            projects_client.list()
            assert "Error occurred during execution: list: unable to get all projects" in caplog.text

    def test_get_project_with_no_name_or_id_raises_value_error(self) -> None:
        projects_client = Projects()

        try:
            projects_client.get()
        except ValueError as e:
            assert str(e) == "Exactly one of 'id' or 'name' must be provided"

    def test_get_project_with_name_and_id_raises_value_error(self) -> None:
        projects_client = Projects()

        try:
            projects_client.get(id="123", name="my_project")
        except ValueError as e:
            assert str(e) == "Exactly one of 'id' or 'name' must be provided"

    def test_get_project_with_empty_name_and_id_raises_value_error(self) -> None:
        projects_client = Projects()

        try:
            projects_client.get(id="", name="")
        except ValueError as e:
            assert str(e) == "Exactly one of 'id' or 'name' must be provided"

    @patch("galileo.projects.get_project_projects_project_id_get.sync_detailed", return_value=None)
    def test_get_project_with_id_gets_project_by_id(self, get_project_projects_project_id_get: Mock) -> None:
        Projects().get(id="123")
        get_project_projects_project_id_get.assert_called_once_with(project_id="123", client=ANY)

    @patch("galileo.projects.get_project_projects_project_id_get.sync_detailed", return_value=None)
    def test_get_project_with_id_with_whitespace_env_vars_gets_project_by_id(
        self, get_project_projects_project_id_get: Mock
    ) -> None:
        with patch.dict("os.environ", {"GALILEO_PROJECT": "  "}):
            with patch.dict("os.environ", {"GALILEO_PROJECT_ID": "  "}):
                Projects().get_with_env_fallbacks(id="123")
                get_project_projects_project_id_get.assert_called_once_with(project_id="123", client=ANY)

    @patch("galileo.projects.get_project_projects_project_id_get.sync_detailed", return_value=None)
    def test_get_project_with_id_from_env_var_gets_project_by_id(
        self, get_project_projects_project_id_get: Mock
    ) -> None:
        with patch.dict("os.environ", {"GALILEO_PROJECT_ID": "123"}):
            Projects().get_with_env_fallbacks()
            get_project_projects_project_id_get.assert_called_once_with(project_id="123", client=ANY)

    @patch("galileo.projects.get_projects_projects_get.sync_detailed", return_value=None)
    def test_get_project_with_name_gets_project_by_name(self, get_projects_projects_get: Mock) -> None:
        Projects().get(name="my_project")
        get_projects_projects_get.assert_called_once_with(project_name="my_project", client=ANY, type_=ANY)

    @patch("galileo.projects.get_projects_projects_get.sync_detailed", return_value=None)
    def test_get_project_with_name_with_whitespace_env_vars_gets_project_by_name(
        self, get_projects_projects_get: Mock
    ) -> None:
        with patch.dict("os.environ", {"GALILEO_PROJECT": "  "}):
            with patch.dict("os.environ", {"GALILEO_PROJECT_ID": "  "}):
                Projects().get_with_env_fallbacks(name="my_project")
                get_projects_projects_get.assert_called_once_with(project_name="my_project", client=ANY, type_=ANY)

    @patch("galileo.projects.get_projects_projects_get.sync_detailed", return_value=None)
    def test_get_project_with_name_from_env_var_gets_project_by_name(self, get_projects_projects_get: Mock) -> None:
        os.environ.pop("GALILEO_PROJECT_ID", None)

        with patch.dict("os.environ", {"GALILEO_PROJECT": "my_project"}):
            Projects().get_with_env_fallbacks()
            get_projects_projects_get.assert_called_once_with(project_name="my_project", client=ANY, type_=ANY)

    @patch("galileo.projects.create_user_project_collaborators_projects_project_id_users_post.sync")
    def test_share_project_with_user(self, mock_create_user_project_collaborators):
        mock_create_user_project_collaborators.return_value = [Mock()]
        projects_client = Projects()
        projects_client.share_project_with_user(project_id="123", user_id="456")
        mock_create_user_project_collaborators.assert_called_once_with(project_id="123", client=ANY, body=ANY)

    @patch("galileo.projects.create_user_project_collaborators_projects_project_id_users_post.sync")
    def test_share_project_with_user_error(
        self, mock_create_user_project_collaborators, caplog, enable_galileo_logging
    ):
        mock_create_user_project_collaborators.return_value = None
        projects_client = Projects()
        with caplog.at_level(logging.WARNING):
            projects_client.share_project_with_user(project_id="123", user_id="456")
            assert (
                "Error occurred during execution: share_project_with_user: Failed to share project 123 with user 456"
                in caplog.text
            )

    @patch("galileo.projects.delete_user_project_collaborator_projects_project_id_users_user_id_delete.sync")
    def test_unshare_project_with_user(self, mock_delete_user_project_collaborator):
        mock_delete_user_project_collaborator.return_value = True
        projects_client = Projects()
        projects_client.unshare_project_with_user(project_id="123", user_id="456")
        mock_delete_user_project_collaborator.assert_called_once_with(project_id="123", user_id="456", client=ANY)

    @patch("galileo.projects.delete_user_project_collaborator_projects_project_id_users_user_id_delete.sync")
    def test_unshare_project_with_user_error(
        self, mock_delete_user_project_collaborator, caplog, enable_galileo_logging
    ):
        mock_delete_user_project_collaborator.return_value = None
        projects_client = Projects()
        with caplog.at_level(logging.WARNING):
            projects_client.unshare_project_with_user(project_id="123", user_id="456")
            assert (
                "Error occurred during execution: unshare_project_with_user: Failed to unshare project 123 with user 456"
                in caplog.text
            )

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
    def test_list_user_project_collaborators_error(
        self, mock_list_user_project_collaborators, caplog, enable_galileo_logging
    ):
        mock_list_user_project_collaborators.return_value = None
        projects_client = Projects()
        with caplog.at_level(logging.WARNING):
            projects_client.list_user_project_collaborators(project_id="123")
            assert (
                "Error occurred during execution: list_user_project_collaborators: Failed to list collaborators for project 123"
                in caplog.text
            )

    @patch("galileo.projects.update_user_project_collaborator_projects_project_id_users_user_id_patch.sync")
    def test_update_user_project_collaborator(self, mock_update_user_project_collaborator):
        projects_client = Projects()
        projects_client.update_user_project_collaborator(project_id="123", user_id="456")
        mock_update_user_project_collaborator.assert_called_once_with(
            project_id="123", user_id="456", client=ANY, body=ANY
        )

    @patch("galileo.projects.update_user_project_collaborator_projects_project_id_users_user_id_patch.sync")
    def test_update_user_project_collaborator_error(
        self, mock_update_user_project_collaborator, caplog, enable_galileo_logging
    ):
        mock_update_user_project_collaborator.return_value = None
        projects_client = Projects()
        with caplog.at_level(logging.WARNING):
            projects_client.update_user_project_collaborator(project_id="123", user_id="456")
            assert (
                "Error occurred during execution: update_user_project_collaborator: Failed to update collaborator for project 123"
                in caplog.text
            )

    # Delete Project Tests
    def test_delete_project_with_no_name_or_id_logs_warning_and_returns_none(
        self, caplog, enable_galileo_logging
    ) -> None:
        """Test that delete_project logs warning and returns None when neither id nor name is provided."""
        with caplog.at_level(logging.WARNING):
            result = Projects().delete_project()

        assert result is None
        assert "Error occurred during execution: delete_project:" in caplog.text
        assert "Exactly one of 'id' or 'name' must be provided" in caplog.text

    def test_delete_project_with_both_name_and_id_logs_warning_and_returns_none(
        self, caplog, enable_galileo_logging
    ) -> None:
        """Test that delete_project logs warning and returns None when both id and name are provided."""
        with caplog.at_level(logging.WARNING):
            result = Projects().delete_project(id="123", name="my_project")

        assert result is None
        assert "Error occurred during execution: delete_project:" in caplog.text
        assert "Exactly one of 'id' or 'name' must be provided" in caplog.text

    def test_delete_project_with_empty_name_and_id_logs_warning_and_returns_none(
        self, caplog, enable_galileo_logging
    ) -> None:
        """Test that delete_project logs warning and returns None when both id and name are empty strings."""
        with caplog.at_level(logging.WARNING):
            result = Projects().delete_project(id="", name="")

        assert result is None
        assert "Error occurred during execution: delete_project:" in caplog.text
        assert "Exactly one of 'id' or 'name' must be provided" in caplog.text

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
    def test_delete_project_with_non_genai_project_logs_warning_and_returns_none(
        self, get_mock: Mock, caplog, enable_galileo_logging
    ) -> None:
        """Test that delete_project logs warning and returns None when project is not GEN_AI type."""
        # Mock the get method to return a non-GEN_AI project
        mock_project = Mock()
        mock_project.id = "123"
        mock_project.type = ProjectType.LLM_MONITOR  # Not GEN_AI
        mock_project.name = "test_project"

        get_mock.return_value = mock_project

        # The DecorateAllMethods decorator catches ProjectsAPIException and logs it
        with caplog.at_level(logging.WARNING):
            result = Projects().delete_project(id="123")

        assert result is None
        assert "Error occurred during execution: delete_project:" in caplog.text
        assert "is not a gen_ai project" in caplog.text

    @patch("galileo.projects.Projects.get")
    def test_delete_project_with_nonexistent_project_logs_warning_and_returns_none(
        self, get_mock: Mock, caplog, enable_galileo_logging
    ) -> None:
        """Test that delete_project logs warning and returns None when project doesn't exist."""
        # Mock the get method to return None (project not found)
        get_mock.return_value = None

        # The DecorateAllMethods decorator catches ValueError and logs it
        with caplog.at_level(logging.WARNING):
            result = Projects().delete_project(id="nonexistent-id")

        assert result is None
        assert "Error occurred during execution: delete_project:" in caplog.text
        assert "not found" in caplog.text


class TestDeleteProjectConvenienceFunction:
    """Tests for the delete_project convenience function that wraps Projects().delete_project()."""

    def test_delete_project_convenience_with_no_name_or_id_returns_false(self, caplog, enable_galileo_logging) -> None:
        """Test that delete_project convenience function returns False when neither id nor name is provided."""
        with caplog.at_level(logging.WARNING):
            result = delete_project(id="", name="")

        assert result is False
        assert "Error occurred during execution: delete_project:" in caplog.text
        assert "Exactly one of 'id' or 'name' must be provided" in caplog.text

    def test_delete_project_convenience_with_both_name_and_id_returns_false(
        self, caplog, enable_galileo_logging
    ) -> None:
        """Test that delete_project convenience function returns False when both id and name are provided."""
        with caplog.at_level(logging.WARNING):
            result = delete_project(id="123", name="my_project")

        assert result is False
        assert "Error occurred during execution: delete_project:" in caplog.text
        assert "Exactly one of 'id' or 'name' must be provided" in caplog.text

    @patch("galileo.projects.Projects.get")
    def test_delete_project_convenience_with_nonexistent_project_returns_false(
        self, get_mock: Mock, caplog, enable_galileo_logging
    ) -> None:
        """Test that delete_project convenience function returns False when project doesn't exist."""
        # Mock the get method to return None (project not found)
        get_mock.return_value = None

        with caplog.at_level(logging.WARNING):
            result = delete_project(name="nonexistent-project")

        assert result is False
        assert "Error occurred during execution: delete_project:" in caplog.text
        assert "not found" in caplog.text

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
