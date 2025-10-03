import logging
import os
from unittest.mock import ANY, Mock, patch

import pytest

from galileo.projects import Projects


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
        # it doesn't trough exception, because we catch all and log
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
