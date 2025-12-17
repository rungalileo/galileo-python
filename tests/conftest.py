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

_os.environ["GALILEO_CONSOLE_URL"] = "http://localtest:8088"
_os.environ["GALILEO_API_KEY"] = "api-1234567890"
_os.environ["GALILEO_PROJECT"] = "test-project"
_os.environ["GALILEO_LOG_STREAM"] = "test-log-stream"
_os.environ["OPENAI_API_KEY"] = "sk-test"
del _os  # Clean up temporary import
# fmt: on

import datetime  # noqa: E402
import logging  # noqa: E402
from collections.abc import Generator  # noqa: E402
from typing import Callable  # noqa: E402
from unittest.mock import MagicMock, patch  # noqa: E402
from uuid import uuid4  # noqa: E402

import pytest  # noqa: E402
from openai.types import CompletionUsage  # noqa: E402
from openai.types.chat import ChatCompletionMessage  # noqa: E402
from openai.types.chat.chat_completion import ChatCompletion, Choice  # noqa: E402

from galileo.config import GalileoPythonConfig  # noqa: E402
from galileo.resources.models import DatasetContent, DatasetRow, DatasetRowValuesDict  # noqa: E402
from galileo_core.constants.request_method import RequestMethod  # noqa: E402
from galileo_core.constants.routes import Routes as CoreRoutes  # noqa: E402
from galileo_core.schemas.core.user import User  # noqa: E402
from galileo_core.schemas.core.user_role import UserRole  # noqa: E402
from galileo_core.schemas.protect.rule import Rule, RuleOperator  # noqa: E402
from galileo_core.schemas.protect.ruleset import Ruleset  # noqa: E402
from galileo_core.schemas.shared.traces_logger import _current_parent_var  # noqa: E402
from tests.testutils.setup import setup_thread_pool_request_capture  # noqa: E402

# Note: The mock_request fixture is automatically provided by galileo_core[testing] extras


@pytest.fixture(autouse=True)
def reset_traces_logger_state() -> Generator[None, None, None]:
    """Reset TracesLogger ContextVar state before and after each test.

    This ensures tests don't leak state via the module-level ContextVar.
    """
    _current_parent_var.set(None)
    yield
    _current_parent_var.set(None)


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
