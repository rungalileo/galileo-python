"""
Conftest for __future__ tests.

This file provides fixtures for Configuration tests with proper mocking
to prevent interactive prompts and properly isolate Configuration tests.

These tests are completely isolated from the parent conftest.py fixtures.
"""

# fmt: off
# CRITICAL: Set test environment variables BEFORE any other imports.
# This MUST be at the absolute top of conftest.py before any import statements.
# Required for pytest-xdist compatibility on Python 3.14+.
import os as _os

_os.environ.setdefault("GALILEO_CONSOLE_URL", "http://localtest:8088")
_os.environ.setdefault("GALILEO_API_KEY", "api-1234567890")
_os.environ.setdefault("GALILEO_PROJECT", "test-project")
_os.environ.setdefault("GALILEO_LOG_STREAM", "test-log-stream")
_os.environ.setdefault("OPENAI_API_KEY", "sk-test")
del _os  # Clean up temporary import
# fmt: on

import logging  # noqa: E402
from collections.abc import Generator  # noqa: E402
from io import StringIO  # noqa: E402
from pathlib import Path  # noqa: E402
from unittest.mock import AsyncMock, MagicMock, patch  # noqa: E402
from uuid import uuid4  # noqa: E402

import pytest  # noqa: E402
from httpx import Request, Response  # noqa: E402

from galileo.__future__ import Configuration  # noqa: E402
from galileo.__future__.configuration import _CONFIGURATION_KEYS  # noqa: E402
from galileo.config import GalileoPythonConfig  # noqa: E402
from galileo.resources.models.messages_list_item import MessagesListItem  # noqa: E402
from galileo_core.schemas.core.user import User  # noqa: E402
from galileo_core.schemas.core.user_role import UserRole  # noqa: E402


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


@pytest.fixture
def clean_env(monkeypatch: pytest.MonkeyPatch) -> Generator[None, None, None]:
    """Clean environment fixture that removes all Galileo-related env vars."""
    for key in _CONFIGURATION_KEYS:
        monkeypatch.delenv(key.env_var, raising=False)
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

    mock_version = MagicMock()
    mock_version.template = [MessagesListItem(role="user", content="{{input}}")]
    mock_version.version = 1

    mock_pmt = MagicMock()
    mock_pmt.id = str(uuid4())
    mock_pmt.name = "Test Prompt"
    mock_pmt.created_at = MagicMock()
    mock_pmt.updated_at = MagicMock()
    mock_pmt.selected_version = mock_version
    return mock_pmt


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
