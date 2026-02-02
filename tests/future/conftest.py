"""
Conftest for __future__ tests.

This file provides fixtures for Configuration tests with proper mocking
to prevent interactive prompts and properly isolate Configuration tests.

These tests are completely isolated from the parent conftest.py fixtures.

NOTE: Unlike the main tests/conftest.py, we do NOT set default env vars here
because future tests need to test "missing env var" scenarios (e.g.,
test_connect_fails_without_console_url, test_connect_fails_without_api_key).
"""

import logging
from collections.abc import Generator
from io import StringIO
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock, patch
from uuid import uuid4

import pytest
from httpx import Request, Response

from galileo.__future__ import Configuration
from galileo.__future__.collaborator import CollaboratorRole
from galileo.__future__.configuration import _CONFIGURATION_KEYS
from galileo.config import GalileoPythonConfig
from galileo.resources.models.messages_list_item import MessagesListItem
from galileo_core.schemas.core.user import User
from galileo_core.schemas.core.user_role import UserRole


# Override parent autouse fixture to prevent it from running for future tests
@pytest.fixture(autouse=True)
def set_validated_config() -> Generator[None, None, None]:
    """
    Override the parent set_validated_config to be a no-op for future tests.

    Future tests handle their own configuration and don't need the automatic
    config setup from the parent conftest.py.
    """
    yield
    # Clean up any config that might have been created
    # Only reset if already initialized to avoid triggering config initialization
    # with potentially wrong values (no mocks available during teardown)
    if GalileoPythonConfig._instance is not None:
        GalileoPythonConfig._instance.reset()


@pytest.fixture(autouse=True)
def clean_env(monkeypatch: pytest.MonkeyPatch) -> Generator[None, None, None]:
    """Clean environment fixture that removes all Galileo-related env vars.

    This is autouse=True to ensure future tests start with a clean environment,
    especially important because the parent tests/conftest.py sets env vars at
    import time for pytest-xdist compatibility. Future tests need to test
    scenarios like "missing console URL" which require these vars to be absent.
    """
    for key in _CONFIGURATION_KEYS:
        monkeypatch.delenv(key.env_var, raising=False)
    # Also clear OPENAI_API_KEY which parent conftest sets
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    yield


@pytest.fixture
def reset_configuration() -> Generator[None, None, None]:
    """Reset Configuration state before and after each test."""
    Configuration.reset()
    yield
    Configuration.reset()


@pytest.fixture
def mock_env_file(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    """Create a temporary .env file for testing."""
    env_file = tmp_path / ".env"
    monkeypatch.chdir(tmp_path)
    return env_file


@pytest.fixture
def capture_logs() -> Generator[tuple[logging.Logger, StringIO], None, None]:
    """Capture log messages for validation."""
    logger = logging.getLogger("galileo")
    original_level = logger.level
    original_handlers = logger.handlers[:]
    original_propagate = logger.propagate

    # Set up string capture
    log_stream = StringIO()
    handler = logging.StreamHandler(log_stream)
    handler.setFormatter(logging.Formatter("%(levelname)s - %(name)s - %(message)s"))

    logger.handlers = [handler]
    logger.setLevel(logging.DEBUG)
    logger.propagate = False

    try:
        yield logger, log_stream
    finally:
        # Restore original configuration
        logger.handlers = original_handlers
        logger.setLevel(original_level)
        logger.propagate = original_propagate


@pytest.fixture
def mock_api_endpoints() -> Generator[MagicMock, None, None]:
    """
    Mock all API endpoints needed for Configuration.connect() by patching httpx.

    This fixture mocks:
    - Healthcheck endpoint
    - API key login endpoint
    - Current user endpoint
    - JWT token validation
    """
    # Create user data for the /current_user endpoint
    user_data = User.model_validate(
        {"id": str(uuid4()), "email": "user@example.com", "role": UserRole.user}
    ).model_dump(mode="json")

    async def mock_request(method, url, **kwargs):
        """Mock httpx request method based on URL patterns."""
        url_str = str(url)

        # Create a request object to attach to the response
        request = Request(method, url)

        # Mock healthcheck endpoint
        if "/healthcheck" in url_str:
            return Response(200, json={"status": "ok"}, request=request)

        # Mock API key login endpoint
        if "/login/api_key" in url_str:
            return Response(200, json={"access_token": "secret_jwt_token"}, request=request)

        # Mock current user endpoint
        if "/current_user" in url_str:
            return Response(200, json=user_data, request=request)

        # Default response for any other endpoints
        return Response(200, json={}, request=request)

    # Mock JWT decode to avoid token validation issues
    with patch("galileo_core.schemas.base_config.jwt_decode") as mock_jwt:
        mock_jwt.return_value = {"exp": float("inf")}

        # Mock httpx AsyncClient.request method
        with patch("httpx.AsyncClient.request", new=AsyncMock(side_effect=mock_request)):
            yield mock_jwt


@pytest.fixture
def mock_project() -> MagicMock:
    """Create a mock project object for testing."""
    mock_proj = MagicMock()
    mock_proj.id = str(uuid4())
    mock_proj.name = "Test Project"
    mock_proj.created_at = MagicMock()
    mock_proj.created_by = str(uuid4())
    mock_proj.updated_at = MagicMock()
    mock_proj.bookmark = None
    mock_proj.permissions = None
    mock_proj.type = None
    return mock_proj


@pytest.fixture
def mock_dataset() -> MagicMock:
    """Create a mock dataset object for testing."""
    mock_ds = MagicMock()
    mock_ds.id = str(uuid4())
    mock_ds.name = "Test Dataset"
    mock_ds.created_at = MagicMock()
    mock_ds.updated_at = MagicMock()
    mock_ds.num_rows = 10
    mock_ds.column_names = ["input", "output"]
    mock_ds.draft = False
    return mock_ds


@pytest.fixture
def mock_prompt() -> MagicMock:
    """Create a mock prompt object for testing."""
    version_id = str(uuid4())

    mock_version = MagicMock()
    mock_version.template = [MessagesListItem(role="user", content="{{input}}")]
    mock_version.version = 1
    mock_version.id = version_id

    mock_pmt = MagicMock()
    mock_pmt.id = str(uuid4())
    mock_pmt.name = "Test Prompt"
    mock_pmt.created_at = MagicMock()
    mock_pmt.updated_at = MagicMock()
    mock_pmt.selected_version = mock_version
    mock_pmt.selected_version_id = version_id
    mock_pmt.total_versions = 1
    mock_pmt.all_available_versions = [1]
    mock_pmt.max_version = 1
    return mock_pmt


@pytest.fixture
def mock_prompt_version() -> MagicMock:
    """Create a mock prompt version object for testing."""
    mock_version = MagicMock()
    mock_version.id = str(uuid4())
    mock_version.version = 1
    mock_version.template = [MessagesListItem(role="user", content="{{input}}")]
    mock_version.settings = MagicMock()
    mock_version.created_at = MagicMock()
    mock_version.updated_at = MagicMock()
    return mock_version


@pytest.fixture
def mock_logstream() -> MagicMock:
    """Create a mock log stream object for testing."""
    mock_ls = MagicMock()
    mock_ls.id = str(uuid4())
    mock_ls.name = "Test Stream"
    mock_ls.project_id = str(uuid4())
    mock_ls.created_at = MagicMock()
    mock_ls.created_by = str(uuid4())
    mock_ls.updated_at = MagicMock()
    mock_ls.additional_properties = {}
    return mock_ls


@pytest.fixture
def mock_integration() -> MagicMock:
    """Create a mock integration object for testing."""
    mock_int = MagicMock()
    mock_int.id = str(uuid4())
    mock_int.name = "openai"
    mock_int.created_at = MagicMock()
    mock_int.updated_at = MagicMock()
    mock_int.created_by = str(uuid4())
    mock_int.is_selected = True
    mock_int.permissions = ["read", "update"]
    return mock_int


@pytest.fixture
def mock_collaborator() -> MagicMock:
    """Create a mock collaborator object for testing."""
    mock_collab = MagicMock()
    mock_collab.id = str(uuid4())
    mock_collab.user_id = str(uuid4())
    mock_collab.role = CollaboratorRole.VIEWER
    mock_collab.created_at = None
    mock_collab.email = "collaborator@test.com"
    mock_collab.first_name = "Test"
    mock_collab.last_name = "Collaborator"
    mock_collab.permissions = []
    return mock_collab
