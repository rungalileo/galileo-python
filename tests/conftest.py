# fmt: off
# CRITICAL: Set test environment variables BEFORE any other imports.
# This MUST be at the absolute top of conftest.py before any import statements.
# Required for pytest-xdist compatibility on Python 3.14+.
#
# NOTE: We unconditionally override these vars (not setdefault) to ensure:
# 1. Tests never accidentally use real credentials from developer's environment
# 2. Test isolation - all tests see the same predictable values
# 3. Security - prevents real API keys from leaking into test logs
import os as _os

import pytest
from openai.types import CompletionUsage
from openai.types.chat import ChatCompletionMessage
from openai.types.chat.chat_completion import ChatCompletion, Choice
from openai.types.responses import (
    Response,
    ResponseFunctionToolCall,
    ResponseOutputMessage,
    ResponseOutputText,
    ResponseUsage,
)
from openai.types.responses.response_usage import InputTokensDetails, OutputTokensDetails

_os.environ["GALILEO_CONSOLE_URL"] = "http://localtest:8088"
_os.environ["GALILEO_API_KEY"] = "api-1234567890"
_os.environ["GALILEO_PROJECT"] = "test-project"
_os.environ["GALILEO_LOG_STREAM"] = "test-log-stream"
_os.environ["OPENAI_API_KEY"] = "sk-test"
# SC-60512: Bound GalileoLogger.terminate() shutdown wait. The default of 90s
# turns into a busy-poll when --disable-socket leaves background tasks pending,
# which is the root cause of pytest workers hanging at exit. Keep this small.
_os.environ.setdefault("GALILEO_LOGGER_SHUTDOWN_TIMEOUT_SECONDS", "2")
del _os  # Clean up temporary import
# fmt: on

import datetime  # noqa: E402
import logging  # noqa: E402
from collections.abc import Callable, Generator  # noqa: E402
from io import StringIO  # noqa: E402
from pathlib import Path  # noqa: E402
from unittest.mock import AsyncMock, MagicMock, patch  # noqa: E402
from uuid import uuid4  # noqa: E402

from httpx import Request  # noqa: E402
from httpx import Response as HttpxResponse  # noqa: E402

from galileo.collaborator import CollaboratorRole  # noqa: E402
from galileo.config import GalileoPythonConfig  # noqa: E402
from galileo.configuration import _CONFIGURATION_KEYS, Configuration  # noqa: E402
from galileo.resources.models import DatasetContent, DatasetRow, DatasetRowValuesDict  # noqa: E402
from galileo.resources.models.messages_list_item import MessagesListItem  # noqa: E402
from galileo_core.constants.request_method import RequestMethod  # noqa: E402
from galileo_core.constants.routes import Routes as CoreRoutes  # noqa: E402
from galileo_core.schemas.core.user import User  # noqa: E402
from galileo_core.schemas.core.user_role import UserRole  # noqa: E402
from galileo_core.schemas.protect.rule import Rule, RuleOperator  # noqa: E402
from galileo_core.schemas.protect.ruleset import Ruleset  # noqa: E402
from tests.testutils.setup import setup_thread_pool_request_capture  # noqa: E402

# Note: The mock_request fixture is automatically provided by galileo_core[testing] extras


@pytest.fixture
def mock_healthcheck(mock_request: Callable) -> Generator[None, None, None]:
    """Mock the healthcheck endpoint. Assertions removed as not all tests call this."""
    mock_request(method=RequestMethod.GET, path=CoreRoutes.healthcheck)
    yield


@pytest.fixture
def mock_get_current_user(mock_request: Callable) -> Generator[None, None, None]:
    """Mock the get current user endpoint. Assertions removed as not all tests call this."""
    mock_request(
        RequestMethod.GET,
        CoreRoutes.current_user,
        json=User.model_validate({"id": uuid4(), "email": "user@example.com", "role": UserRole.user}).model_dump(
            mode="json"
        ),
    )
    yield


@pytest.fixture
def mock_login_api_key(mock_request: Callable) -> Generator[None, None, None]:
    """Mock the API key login endpoint. Assertions removed as not all tests call this."""
    mock_request(RequestMethod.POST, CoreRoutes.api_key_login, json={"access_token": "secret_jwt_token"})
    yield


@pytest.fixture
def mock_decode_jwt() -> Generator[MagicMock, None, None]:
    with patch("galileo_core.schemas.base_config.jwt_decode") as _fixture:
        _fixture.return_value = {"exp": float("inf")}
        yield _fixture


@pytest.fixture(autouse=True)
def set_validated_config(
    mock_healthcheck: None, mock_login_api_key: None, mock_get_current_user: None, mock_decode_jwt: MagicMock
) -> Generator[None, None, None]:
    """Automatically set up validated config for tests."""
    # Reset any existing config to ensure fresh initialization
    # This is needed for pytest-xdist compatibility on Python 3.14+
    if GalileoPythonConfig._instance is not None:
        GalileoPythonConfig._instance.reset()
    # Initialize config with EXPLICIT values to avoid env var timing issues with pytest-xdist
    # This ensures correct config even if env vars weren't set before module imports
    config = GalileoPythonConfig.get(console_url="http://localtest:8088", api_key="api-1234567890")
    yield
    config.reset()


@pytest.fixture
def create_chat_completion() -> ChatCompletion:
    return ChatCompletion(
        id="foo",
        model="gpt-3.5-turbo",
        object="chat.completion",
        choices=[
            Choice(
                finish_reason="stop",
                index=0,
                message=ChatCompletionMessage(content="The mock is working! ;)", role="assistant"),
            )
        ],
        created=int(datetime.datetime.now().timestamp()),
        usage=CompletionUsage(completion_tokens=13, prompt_tokens=12, total_tokens=25),
    )


@pytest.fixture
def create_responses_response():
    """Mock Responses API response for basic text generation."""

    return Response(
        id="resp_test123",
        created_at=1758822441.0,
        model="gpt-4o",
        object="response",
        output=[
            ResponseOutputMessage(
                id="msg_test123",
                content=[
                    ResponseOutputText(text="This is a test response", type="output_text", annotations=[], logprobs=[])
                ],
                role="assistant",
                status="completed",
                type="message",
            )
        ],
        parallel_tool_calls=True,
        tool_choice="auto",
        tools=[],
        usage=ResponseUsage(
            input_tokens=10,
            input_tokens_details=InputTokensDetails(cached_tokens=0),
            output_tokens=5,
            output_tokens_details=OutputTokensDetails(reasoning_tokens=0),
            total_tokens=15,
        ),
        status="completed",
    )


@pytest.fixture
def create_responses_response_with_tools():
    """Mock Responses API response with tool calls."""

    return Response(
        id="resp_test456",
        created_at=1758822441.0,
        model="gpt-4o",
        object="response",
        output=[
            ResponseFunctionToolCall(
                id="fc_test456",
                name="get_weather",
                arguments='{"location": "San Francisco"}',
                type="function_call",
                call_id="call_test456",
                status="completed",
            )
        ],
        parallel_tool_calls=True,
        tool_choice="auto",
        tools=[],
        usage=ResponseUsage(
            input_tokens=20,
            input_tokens_details=InputTokensDetails(cached_tokens=0),
            output_tokens=10,
            output_tokens_details=OutputTokensDetails(reasoning_tokens=0),
            total_tokens=30,
        ),
        status="completed",
    )


@pytest.fixture
def test_dataset_row_id() -> None:
    str(uuid4())


@pytest.fixture
def dataset_content(test_dataset_row_id: str):
    row = DatasetRow(
        index=0,
        values=["Which continent is Spain in?", "Europe", '{"meta": "data"}'],
        values_dict=DatasetRowValuesDict.from_dict(
            {"input": "Which continent is Spain in?", "output": "Europe", "metadata": '{"meta": "data"}'}
        ),
        row_id=test_dataset_row_id,
        metadata=None,
    )

    column_names = ["input", "output", "metadata"]
    return DatasetContent(column_names=column_names, rows=[row])


@pytest.fixture
def dataset_content_with_question():
    row = DatasetRow(
        index=0,
        values=['{"question": "Which continent is Spain in?", "expected": "Europe"}', None, None],
        values_dict=DatasetRowValuesDict.from_dict(
            {
                "input": {"question": "Which continent is Spain in?", "expected": "Europe"},
                "output": None,
                "metadata": None,
            }
        ),
        row_id="",
        metadata=None,
    )

    column_names = ["input", "output", "metadata"]
    return DatasetContent(column_names=column_names, rows=[row])


@pytest.fixture
def local_dataset():
    return [
        {"input": "Which continent is Spain in?", "output": "Europe"},
        {"input": "Which continent is Japan in?", "output": "Asia"},
    ]


@pytest.fixture
def dataset_content_150_rows():
    """Dataset content with 15 rows for testing dataset_limit functionality."""
    rows = [
        DatasetRow(
            index=i,
            row_id=f"row{i}",
            values=[f"Question {i}", f"Answer {i}", f'{{"meta": "data{i}"}}'],
            values_dict=DatasetRowValuesDict.from_dict(
                {"input": f"Question {i}", "output": f"Answer {i}", "metadata": f'{{"meta": "data{i}"}}'}
            ),
            metadata=None,
        )
        for i in range(150)
    ]
    return DatasetContent(rows=rows)


@pytest.fixture
def thread_pool_capture():
    """
    Pytest fixture that provides a function to capture thread pool requests from distributed tracing methods.

    Usage:
        def test_distributed_method(thread_pool_capture):
            logger = GalileoLogger(project="test", log_stream="test", mode="distributed")
            capture = thread_pool_capture(logger)

            logger._ingest_trace_streaming(trace)

            capture.mock_pool.assert_called_once()
            request = capture.get_latest_request()
            assert isinstance(request, TracesIngestRequest)
    """

    def _capture_factory(logger):
        return setup_thread_pool_request_capture(logger)

    return _capture_factory


@pytest.fixture(
    params=[
        # Single ruleset with a single rule.
        [Ruleset(rules=[Rule(metric="toxicity", operator=RuleOperator.gt, target_value=0.5)])],
        # Single ruleset with multiple rules.
        [
            Ruleset(
                rules=[
                    Rule(metric="toxicity", operator=RuleOperator.gt, target_value=0.5),
                    Rule(metric="tone", operator=RuleOperator.lt, target_value=0.8),
                ]
            )
        ],
        # Single ruleset with an unknown metric.
        [Ruleset(rules=[Rule(metric="unknown", operator=RuleOperator.gt, target_value=0.5)])],
        # Multiple rulesets with a single rule each.
        [
            Ruleset(rules=[Rule(metric="toxicity", operator=RuleOperator.gt, target_value=0.5)]),
            Ruleset(rules=[Rule(metric="toxicity", operator=RuleOperator.lt, target_value=0.8)]),
        ],
    ]
)
def rulesets(request: pytest.FixtureRequest) -> list[Ruleset]:
    return request.param


@pytest.fixture
def enable_galileo_logging():
    """Temporarily enable galileo logging for tests that need to capture log output."""
    galileo_logger = logging.getLogger("galileo")
    original_level = galileo_logger.level
    original_propagate = galileo_logger.propagate

    # Enable logging at appropriate levels for different test types
    galileo_logger.setLevel(logging.DEBUG)  # Most permissive for test flexibility
    galileo_logger.propagate = True

    try:
        yield
    finally:
        # Restore original settings
        galileo_logger.setLevel(original_level)
        galileo_logger.propagate = original_propagate


# ---------------------------------------------------------------------------
# Fixtures migrated from tests/future/conftest.py
# ---------------------------------------------------------------------------


@pytest.fixture
def clean_env(monkeypatch: pytest.MonkeyPatch) -> Generator[None, None, None]:
    """Remove all Galileo-related env vars for tests that need a clean environment.

    autouse=False — declare this fixture explicitly in tests that require it.
    Useful for tests that verify behaviour when config keys are absent, e.g.
    test_connect_fails_without_api_key.
    """
    for key in _CONFIGURATION_KEYS:
        monkeypatch.delenv(key.env_var, raising=False)
    # Also clear OPENAI_API_KEY which root conftest sets at import time
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
    """Create a temporary directory and return a .env file path inside it.

    The working directory is changed to ``tmp_path`` so that Configuration's
    env-file discovery finds the file automatically.
    """
    env_file = tmp_path / ".env"
    monkeypatch.chdir(tmp_path)
    return env_file


@pytest.fixture
def capture_logs() -> Generator[tuple[logging.Logger, StringIO], None, None]:
    """Capture log messages emitted by the galileo logger for assertion."""
    logger = logging.getLogger("galileo")
    original_level = logger.level
    original_handlers = logger.handlers[:]
    original_propagate = logger.propagate

    log_stream = StringIO()
    handler = logging.StreamHandler(log_stream)
    handler.setFormatter(logging.Formatter("%(levelname)s - %(name)s - %(message)s"))

    logger.handlers = [handler]
    logger.setLevel(logging.DEBUG)
    logger.propagate = False

    try:
        yield logger, log_stream
    finally:
        logger.handlers = original_handlers
        logger.setLevel(original_level)
        logger.propagate = original_propagate


@pytest.fixture
def mock_api_endpoints() -> Generator[MagicMock, None, None]:
    """Mock all API endpoints needed for Configuration.connect() by patching httpx.

    Mocks:
    - Healthcheck endpoint
    - API key login endpoint
    - Current user endpoint
    - JWT token validation
    """
    user_data = User.model_validate(
        {"id": str(uuid4()), "email": "user@example.com", "role": UserRole.user}
    ).model_dump(mode="json")

    async def _mock_request(method, url, **kwargs):
        url_str = str(url)
        request = Request(method, url)

        if "/healthcheck" in url_str:
            return HttpxResponse(200, json={"status": "ok"}, request=request)
        if "/login/api_key" in url_str:
            return HttpxResponse(200, json={"access_token": "secret_jwt_token"}, request=request)
        if "/current_user" in url_str:
            return HttpxResponse(200, json=user_data, request=request)
        return HttpxResponse(200, json={}, request=request)

    with patch("galileo_core.schemas.base_config.jwt_decode") as mock_jwt:
        mock_jwt.return_value = {"exp": float("inf")}
        with patch("httpx.AsyncClient.request", new=AsyncMock(side_effect=_mock_request)):
            yield mock_jwt


@pytest.fixture
def mock_project() -> MagicMock:
    """Create a mock project API response object for testing."""
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
    """Create a mock dataset API response object for testing."""
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
    """Create a mock prompt API response object for testing."""
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
    """Create a mock prompt version API response object for testing."""
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
    """Create a mock log stream API response object for testing."""
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
    """Create a mock integration API response object for testing."""
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
    """Create a mock collaborator API response object for testing."""
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
