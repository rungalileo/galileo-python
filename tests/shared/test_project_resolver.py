"""Unit tests for ``galileo.shared.project_resolver._resolve_project``.

The resolver is the single canonical entry point used by every ``__future__``
domain object (LogStream, Experiment, …) to turn explicit kwargs / env vars
into a concrete project. These tests pin its contract so future callers
behave consistently.
"""

from unittest.mock import MagicMock, patch

import pytest

from galileo.exceptions import NotFoundError
from galileo.projects import ProjectNotFoundError
from galileo.shared.exceptions import ResourceNotFoundError
from galileo.shared.project_resolver import _resolve_project


class TestResolveProject:
    """Behavioral tests for the shared ``_resolve_project`` helper."""

    @patch("galileo.shared.project_resolver.Projects")
    def test_returns_project_when_get_with_env_fallbacks_succeeds(self, mock_projects_class: MagicMock) -> None:
        # Given: an explicit project_id that resolves to a known project
        mock_project = MagicMock()
        mock_project.id = "p-1"
        mock_project.name = "P One"
        mock_service = MagicMock()
        mock_projects_class.return_value = mock_service
        mock_service.get_with_env_fallbacks.return_value = mock_project

        # When: resolving with that project_id
        resolved = _resolve_project(project_id="p-1", project_name=None)

        # Then: the project is returned and get_with_env_fallbacks was called once
        assert resolved is mock_project
        mock_service.get_with_env_fallbacks.assert_called_once_with(id="p-1", name=None)

    @patch("galileo.shared.project_resolver.Projects")
    def test_short_circuits_when_no_identifier_anywhere(
        self, mock_projects_class: MagicMock, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """No id, no name, no env vars must raise without touching the API client."""
        # Given: env vars are unset
        monkeypatch.delenv("GALILEO_PROJECT", raising=False)
        monkeypatch.delenv("GALILEO_PROJECT_ID", raising=False)

        # When/Then: resolving raises NotFoundError without instantiating Projects
        with pytest.raises(NotFoundError, match="No project specified"):
            _resolve_project(project_id=None, project_name=None)
        mock_projects_class.assert_not_called()

    @patch("galileo.shared.project_resolver.Projects")
    def test_returns_resource_not_found_subclass(
        self, mock_projects_class: MagicMock, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """Backward-compat: the raised error is also a ResourceNotFoundError."""
        # Given: no identifier anywhere
        monkeypatch.delenv("GALILEO_PROJECT", raising=False)
        monkeypatch.delenv("GALILEO_PROJECT_ID", raising=False)

        # When/Then: the raised exception is BOTH a NotFoundError and a ResourceNotFoundError
        with pytest.raises(NotFoundError) as exc_info:
            _resolve_project(project_id=None, project_name=None)
        assert isinstance(exc_info.value, ResourceNotFoundError)

    @patch("galileo.shared.project_resolver.Projects")
    def test_converts_project_not_found_error_to_not_found_error(self, mock_projects_class: MagicMock) -> None:
        # Given: an explicit id that the API reports as not found
        mock_service = MagicMock()
        mock_projects_class.return_value = mock_service
        mock_service.get_with_env_fallbacks.side_effect = ProjectNotFoundError("not found")

        # When/Then: the project-not-found error is rewritten with actionable context
        with pytest.raises(NotFoundError, match='Project with id "missing-id" not found'):
            _resolve_project(project_id="missing-id", project_name=None)

    @patch("galileo.shared.project_resolver.Projects")
    def test_does_not_swallow_unrelated_value_error(self, mock_projects_class: MagicMock) -> None:
        """Unrelated ValueErrors from the API client surface unchanged."""
        # Given: the API client raises a generic ValueError (e.g. deserialization)
        mock_service = MagicMock()
        mock_projects_class.return_value = mock_service
        mock_service.get_with_env_fallbacks.side_effect = ValueError("response decode failed")

        # When/Then: the ValueError propagates instead of being rewritten as NotFoundError
        with pytest.raises(ValueError, match="response decode failed"):
            _resolve_project(project_id="some-id", project_name=None)

    @patch("galileo.shared.project_resolver.Projects")
    def test_raises_not_found_when_get_with_env_fallbacks_returns_none(self, mock_projects_class: MagicMock) -> None:
        # Given: get_with_env_fallbacks returns None (project not found, no exception)
        mock_service = MagicMock()
        mock_projects_class.return_value = mock_service
        mock_service.get_with_env_fallbacks.return_value = None

        # When/Then: a NotFoundError naming the requested project is raised
        with pytest.raises(NotFoundError, match='Project "Missing"'):
            _resolve_project(project_id=None, project_name="Missing")
