from unittest.mock import MagicMock

import pytest

from galileo.handlers.base_handler import GalileoBaseHandler
from galileo.logger import GalileoLogger


@pytest.fixture
def mock_galileo_logger() -> MagicMock:
    """Create a mock Galileo logger for testing."""
    logger = MagicMock(spec=GalileoLogger)
    logger.current_parent.return_value = None
    logger.has_active_trace.return_value = False
    logger.traces = []
    logger.session_id = None
    return logger


@pytest.fixture
def mock_galileo_handler(mock_galileo_logger: MagicMock) -> MagicMock:
    """Create a mock handler for testing."""
    handler = MagicMock(spec=GalileoBaseHandler)
    handler._galileo_logger = mock_galileo_logger
    handler._nodes = {}
    handler._root_node = None
    return handler


@pytest.fixture
def adk_callback_context() -> MagicMock:
    """Create a mock ADK CallbackContext."""
    context = MagicMock()
    context.agent_name = "test_agent"
    context.session_id = "test_session"
    context.user_id = "test_user"
    return context


@pytest.fixture
def adk_invocation_context() -> MagicMock:
    """Create a mock ADK InvocationContext."""
    context = MagicMock()
    context.invocation_id = "test_invocation_123"
    context.session = MagicMock()
    context.session.session_id = "test_session"
    return context


@pytest.fixture
def adk_llm_request() -> MagicMock:
    """Create a mock ADK LlmRequest."""
    request = MagicMock()
    request.contents = []
    request.config = MagicMock()
    request.model = "gemini-pro"
    return request


@pytest.fixture
def adk_llm_response() -> MagicMock:
    """Create a mock ADK LlmResponse."""
    response = MagicMock()
    response.content = MagicMock()
    response.content.parts = []
    response.usage_metadata = MagicMock()
    response.usage_metadata.input_token_count = 10
    response.usage_metadata.output_token_count = 20
    response.model_version = "gemini-pro-response"
    return response


@pytest.fixture
def adk_tool() -> MagicMock:
    """Create a mock ADK BaseTool."""
    tool = MagicMock()
    tool.name = "test_tool"
    return tool


@pytest.fixture
def adk_tool_context() -> MagicMock:
    """Create a mock ADK ToolContext."""
    return MagicMock()


@pytest.fixture
def adk_user_message() -> MagicMock:
    """Create a mock ADK user message (types.Content)."""
    message = MagicMock()
    message.parts = [MagicMock(text="Hello, world!")]
    return message


@pytest.fixture
def adk_event() -> MagicMock:
    """Create a mock ADK Event."""
    event = MagicMock()
    event.type = "test_event"
    event.id = "event_123"
    return event
