import re
from collections.abc import Callable, Generator
from unittest.mock import MagicMock, patch
from uuid import uuid4

import pytest
from galileo_core.constants.request_method import RequestMethod
from galileo_core.constants.routes import Routes as CoreRoutes
from galileo_core.schemas.core.user import User
from galileo_core.schemas.core.user_role import UserRole

from galileo.config import GalileoPythonConfig
from galileo.utils.singleton import GalileoLoggerSingleton

# Note: The mock_request fixture is automatically provided by galileo_core[testing] extras


@pytest.fixture
def mock_healthcheck(mock_request: Callable) -> Generator[None, None, None]:
    """Mock the healthcheck endpoint."""
    mock_request(method=RequestMethod.GET, path=CoreRoutes.healthcheck)
    return


@pytest.fixture
def mock_get_current_user(mock_request: Callable) -> Generator[None, None, None]:
    """Mock the get current user endpoint."""
    mock_request(
        RequestMethod.GET,
        CoreRoutes.current_user,
        json=User.model_validate({"id": uuid4(), "email": "user@example.com", "role": UserRole.user}).model_dump(
            mode="json"
        ),
    )
    return


@pytest.fixture
def mock_login_api_key(mock_request: Callable) -> Generator[None, None, None]:
    """Mock the API key login endpoint."""
    mock_request(RequestMethod.POST, CoreRoutes.api_key_login, json={"access_token": "secret_jwt_token"})
    return


@pytest.fixture
def mock_decode_jwt() -> Generator[MagicMock, None, None]:
    with patch("galileo_core.schemas.base_config.jwt_decode") as _fixture:
        _fixture.return_value = {"exp": float("inf")}
        yield _fixture


@pytest.fixture
def mock_projects(mock_request: Callable) -> Generator[None, None, None]:
    """Mock the projects endpoint used by galileo_context.get_logger_instance().

    ProjectDB schema requires:
    - id, created_by, created_by_user (UserInfo), runs, created_at, updated_at
    """
    project_id = str(uuid4())
    user_id = str(uuid4())
    mock_request(
        RequestMethod.GET,
        "/projects",
        json=[
            {
                "id": project_id,
                "name": "test-project",
                "type": "gen_ai",
                "created_at": "2024-01-01T00:00:00Z",
                "updated_at": "2024-01-01T00:00:00Z",
                "created_by": user_id,
                "created_by_user": {
                    "id": user_id,
                    "email": "test@example.com",
                },
                "runs": [],
            }
        ],
    )
    return


@pytest.fixture
def mock_log_streams(mock_request: Callable) -> Generator[None, None, None]:
    """Mock the log streams endpoints.

    LogStreamResponse schema requires:
    - id, created_at, updated_at, name, project_id

    Endpoints:
    - GET /projects/{project_id}/log_streams - list log streams
    - POST /projects/{project_id}/log_streams - create log stream
    """
    log_stream_id = str(uuid4())
    project_id = str(uuid4())
    user_id = str(uuid4())
    log_stream_response = {
        "id": log_stream_id,
        "name": "test-log-stream",
        "project_id": project_id,
        "created_at": "2024-01-01T00:00:00Z",
        "updated_at": "2024-01-01T00:00:00Z",
        "created_by": user_id,
        "created_by_user": {
            "id": user_id,
            "email": "test@example.com",
        },
    }
    # Mock GET - list log streams
    mock_request(
        RequestMethod.GET,
        re.compile(r"/projects/[^/]+/log_streams"),
        json=[log_stream_response],
    )
    # Mock POST - create log stream
    mock_request(
        RequestMethod.POST,
        re.compile(r"/projects/[^/]+/log_streams"),
        json=log_stream_response,
    )
    return


@pytest.fixture
def mock_sessions(mock_request: Callable) -> Generator[None, None, None]:
    """Mock the sessions endpoints used by GalileoLogger.start_session().

    Endpoints:
    - POST /projects/{project_id}/sessions/search - search sessions
    - POST /projects/{project_id}/sessions - create session
    """
    session_id = str(uuid4())
    session_response = {
        "id": session_id,
        "name": "test-session",
        "created_at": "2024-01-01T00:00:00Z",
        "updated_at": "2024-01-01T00:00:00Z",
    }
    # Mock POST - search sessions (returns empty list - no existing session)
    mock_request(
        RequestMethod.POST,
        re.compile(r"/projects/[^/]+/sessions/search"),
        json={"records": [], "total": 0},
    )
    # Mock POST - create session
    mock_request(
        RequestMethod.POST,
        re.compile(r"/projects/[^/]+/sessions$"),
        json=session_response,
    )
    return


@pytest.fixture(autouse=True)
def set_validated_config(
    mock_healthcheck: None,
    mock_login_api_key: None,
    mock_get_current_user: None,
    mock_decode_jwt: MagicMock,
    mock_projects: None,
    mock_log_streams: None,
    mock_sessions: None,
) -> Generator[None, None, None]:
    """Automatically set up validated config for tests."""
    # Reset any existing config state
    if GalileoPythonConfig._instance is not None:
        GalileoPythonConfig._instance.reset()
    # Reset any cached loggers from previous tests
    GalileoLoggerSingleton().reset_all()

    config = GalileoPythonConfig.get(console_url="http://localtest:8088", api_key="api-1234567890")
    yield
    # Clean up after test
    GalileoLoggerSingleton().reset_all()
    config.reset()
