import json
from typing import Any, Optional, cast
from unittest.mock import Mock, patch

import pytest
from langchain.agents.middleware import AgentState
from langchain_core.messages import AIMessage, HumanMessage, ToolMessage
from langgraph.runtime import Runtime

from galileo import galileo_context
from galileo.handlers.langchain.middleware import GalileoMiddleware
from galileo.logger.logger import GalileoLogger
from tests.testutils.setup import setup_mock_logstreams_client, setup_mock_projects_client, setup_mock_traces_client


class MockAgentState(dict):
    """Mock AgentState that behaves like a dict with attribute access."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__dict__ = self


class MockRuntime:
    """Mock Runtime for testing."""

    pass


class MockModel:
    """Mock model object."""

    def __init__(self, model_name: Optional[str] = None):
        self.model_name = model_name


class MockRequest:
    """Mock request object for model/tool calls."""

    def __init__(
        self,
        state: Optional[dict[str, Any]] = None,
        messages: Optional[list] = None,
        system_message: Optional[Any] = None,
        tools: Optional[list] = None,
        model_settings: Optional[dict[str, Any]] = None,
        model: Optional[Any] = None,
        tool_call: Optional[dict[str, Any]] = None,
    ):
        self.state = state
        self.messages = messages or []
        self.system_message = system_message
        self.tools = tools
        self.model_settings = model_settings or {}
        self.model = model
        self.tool_call = tool_call


class MockResponse:
    """Mock response object."""

    def __init__(self, result: Optional[Any] = None):
        self.result = result


class MockStructuredTool:
    """Mock StructuredTool for testing."""

    def __init__(self, name: str, args_schema: Any):
        self.name = name
        self.args_schema = args_schema


class MockArgsSchema:
    """Mock args schema for tools."""

    @staticmethod
    def model_json_schema():
        return {"type": "object", "properties": {"x": {"type": "number"}}}


@pytest.fixture
@patch("galileo.logger.logger.LogStreams")
@patch("galileo.logger.logger.Projects")
@patch("galileo.logger.logger.Traces")
def galileo_logger(mock_traces_client: Mock, mock_projects_client: Mock, mock_logstreams_client: Mock):
    """Creates a mock Galileo logger for testing."""
    setup_mock_traces_client(mock_traces_client)
    setup_mock_projects_client(mock_projects_client)
    setup_mock_logstreams_client(mock_logstreams_client)
    return GalileoLogger(project="my_project", log_stream="my_log_stream")


@pytest.fixture
def middleware(galileo_logger: GalileoLogger) -> GalileoMiddleware:
    """Creates a GalileoMiddleware with a mock logger."""
    return GalileoMiddleware(galileo_logger=galileo_logger, flush_on_chain_end=False)


@pytest.fixture
def runtime() -> MockRuntime:
    """Creates a mock runtime."""
    return MockRuntime()


@pytest.fixture
def sample_messages():
    """Sample messages for testing."""
    return [HumanMessage(content="test")]


@pytest.fixture
def sample_state(sample_messages):
    """Sample agent state with messages."""
    return MockAgentState(messages=sample_messages)


class TestGalileoMiddlewareInitialization:
    def test_default_initialization(self, galileo_logger: GalileoLogger) -> None:
        """Test middleware initialization with default parameters."""
        middleware = GalileoMiddleware(galileo_logger=galileo_logger)

        assert middleware._handler._galileo_logger == galileo_logger
        assert middleware._async_handler._galileo_logger == galileo_logger
        assert middleware._handler._start_new_trace is True
        assert middleware._handler._flush_on_chain_end is True
        assert middleware._root_run_id is None

    def test_custom_initialization(self, galileo_logger: GalileoLogger) -> None:
        """Test middleware initialization with custom parameters."""
        middleware = GalileoMiddleware(galileo_logger=galileo_logger, start_new_trace=False, flush_on_chain_end=False)

        assert middleware._handler._start_new_trace is False
        assert middleware._handler._flush_on_chain_end is False


class TestSerializationHelpers:
    """Tests for middleware serialization helper methods."""

    def test_serialize_messages(self, middleware: GalileoMiddleware) -> None:
        """Test _serialize_messages with various inputs."""
        # Valid messages
        messages = [HumanMessage(content="Hello"), AIMessage(content="Hi")]
        result = middleware._serialize_messages(messages)
        assert isinstance(result, list) and len(result) == 2

        # None input
        assert middleware._serialize_messages(None) is None

    def test_get_state_messages(self, middleware: GalileoMiddleware) -> None:
        """Test _get_state_messages extracts messages correctly."""
        messages = [HumanMessage(content="test")]

        # Dict with messages
        assert middleware._get_state_messages(cast(AgentState, MockAgentState(messages=messages))) == messages

        # Dict without messages / None
        assert middleware._get_state_messages(cast(AgentState, MockAgentState(other="data"))) is None
        assert middleware._get_state_messages(None) is None

    def test_serialize_state(self, middleware: GalileoMiddleware) -> None:
        """Test _serialize_state behavior."""
        # With messages - returns list
        state_with_msgs = AgentState(messages=[HumanMessage(content="test")])
        assert isinstance(middleware._serialize_state(state_with_msgs), list)

        # Without messages - returns string
        assert isinstance(middleware._serialize_state(cast(AgentState, MockAgentState(other="data"))), str)
        assert middleware._serialize_state(None) is not None

    def test_serialize_response(self, middleware: GalileoMiddleware) -> None:
        """Test _serialize_response with different response types."""
        # Response with result attribute
        messages = [AIMessage(content="response")]
        assert isinstance(middleware._serialize_response(MockResponse(result=messages)), list)

        # AIMessage directly
        result = middleware._serialize_response(AIMessage(content="direct"))
        assert isinstance(result, list) and len(result) == 1

        # Dict fallback
        assert isinstance(middleware._serialize_response({"custom": "response"}), str)

    def test_serialize_tools(self, middleware: GalileoMiddleware) -> None:
        """Test _serialize_tools serialization."""
        tool = MockStructuredTool(name="calculator", args_schema=MockArgsSchema())
        result = middleware._serialize_tools([tool])

        assert isinstance(result, list) and len(result) == 1
        assert result[0]["function"]["name"] == "calculator"
        assert middleware._serialize_tools(None) is None

    def test_serialize_tool_response(self, middleware: GalileoMiddleware) -> None:
        """Test _serialize_tool_response with different response types."""
        # ToolMessage directly (GalileoCallback._find_tool_message returns it)
        result = middleware._serialize_tool_response(
            cast(AgentState, ToolMessage(content="result", tool_call_id="123"))
        )
        assert result["output"] == "result"
        assert result["tool_call_id"] == "123"

        # Non-ToolMessage (falls back to serializing the response)
        result = middleware._serialize_tool_response(cast(AgentState, MockAgentState(data="value")))
        assert "output" in result and isinstance(result["output"], str)


class TestModelMetadataExtraction:
    """Tests for model metadata extraction methods."""

    @pytest.mark.parametrize(
        ("request_kwargs", "expected_model", "expected_temp"),
        [
            ({"model_settings": {"model": "gpt-4", "temperature": 0.7}}, "gpt-4", 0.7),
            ({"model": MockModel(model_name="gpt-3.5")}, "gpt-3.5", None),
            ({}, None, None),
        ],
    )
    def test_extract_model_metadata(
        self, middleware: GalileoMiddleware, request_kwargs, expected_model, expected_temp
    ) -> None:
        """Test _extract_model_metadata from various sources."""
        request = MockRequest(**request_kwargs)
        model_name, temperature = middleware._extract_model_metadata(request)
        assert model_name == expected_model
        assert temperature == expected_temp

    @pytest.mark.parametrize(
        ("request_kwargs", "model_name", "expected"),
        [
            ({}, "gpt-4", "gpt-4"),
            ({"model": MockModel(model_name="gpt-3.5")}, None, "gpt-3.5"),
            ({}, None, "ChatModel"),
        ],
    )
    def test_get_model_display_name(self, middleware: GalileoMiddleware, request_kwargs, model_name, expected) -> None:
        """Test _get_model_display_name returns correct display name."""
        request = MockRequest(**request_kwargs)
        assert middleware._get_model_display_name(request, model_name) == expected


class TestParamPreparation:
    """Tests for parameter preparation methods."""

    def test_prepare_model_call_params(self, middleware: GalileoMiddleware) -> None:
        """Test _prepare_model_call_params creates correct params."""
        request = cast(
            AgentState,
            MockRequest(messages=[HumanMessage(content="test")], model_settings={"model": "gpt-4", "temperature": 0.5}),
        )
        params = middleware._prepare_model_call_params(request)

        assert params["model"] == "gpt-4"
        assert params["temperature"] == 0.5
        assert params["name"] == "gpt-4"
        assert "start_time" in params

    def test_prepare_model_call_params_with_system_message(self, middleware: GalileoMiddleware) -> None:
        """Test system message is prepended to input."""
        request = cast(
            AgentState,
            MockRequest(messages=[HumanMessage(content="test")], system_message=HumanMessage(content="system")),
        )
        params = middleware._prepare_model_call_params(request)
        assert len(params["input"]) == 2

    def test_prepare_tool_call_params(self, middleware: GalileoMiddleware) -> None:
        """Test _prepare_tool_call_params extracts tool info."""
        # With tool_call
        request = cast(AgentState, MockRequest(tool_call={"name": "calc", "args": {"x": 5}}))
        name, input_str = middleware._prepare_tool_call_params(request)
        assert name == "calc"
        assert json.loads(input_str) == {"x": 5}

        # Without tool_call
        request = cast(AgentState, MockRequest(tool_call=None))
        name, input_str = middleware._prepare_tool_call_params(request)
        assert name == "tool" and input_str == "{}"


class TestRootNodeManagement:
    """Tests for root node creation and management."""

    def test_ensure_root_node(self, middleware: GalileoMiddleware, sample_state) -> None:
        """Test _ensure_root_node creates and reuses root."""
        assert middleware._root_run_id is None

        # Creates new root
        root_id = middleware._ensure_root_node(sample_state)
        assert middleware._root_run_id == root_id

        # Returns existing root
        assert middleware._ensure_root_node(sample_state) == root_id

    @pytest.mark.asyncio
    async def test_ensure_async_root_node(self, middleware: GalileoMiddleware, sample_state) -> None:
        """Test _ensure_async_root_node creates and reuses root."""
        assert middleware._root_run_id is None

        root_id = await middleware._ensure_async_root_node(sample_state)
        assert middleware._root_run_id == root_id
        assert await middleware._ensure_async_root_node(sample_state) == root_id


class TestAgentLifecycle:
    """Tests for agent lifecycle methods (sync and async)."""

    def test_before_after_agent(self, middleware: GalileoMiddleware, runtime: MockRuntime) -> None:
        """Test before_agent and after_agent lifecycle."""
        state = cast(AgentState, MockAgentState(messages=[HumanMessage(content="test")]))
        rt = cast(Runtime, runtime)

        # before_agent creates root
        assert middleware.before_agent(state, rt) is None
        assert middleware._root_run_id is not None

        # after_agent clears root
        assert middleware.after_agent(state, rt) is None
        assert middleware._root_run_id is None

    def test_after_agent_without_root(self, middleware: GalileoMiddleware, runtime: MockRuntime) -> None:
        """Test after_agent returns None when no root exists."""
        state = cast(AgentState, MockAgentState(messages=[AIMessage(content="response")]))
        assert middleware.after_agent(state, cast(Runtime, runtime)) is None

    @pytest.mark.asyncio
    async def test_abefore_aafter_agent(self, middleware: GalileoMiddleware, runtime: MockRuntime) -> None:
        """Test async agent lifecycle methods."""
        state = cast(AgentState, MockAgentState(messages=[HumanMessage(content="test")]))
        rt = cast(Runtime, runtime)

        assert await middleware.abefore_agent(state, rt) is None
        assert middleware._root_run_id is not None

        assert await middleware.aafter_agent(state, rt) is None
        assert middleware._root_run_id is None

    @pytest.mark.asyncio
    async def test_aafter_agent_without_root(self, middleware: GalileoMiddleware, runtime: MockRuntime) -> None:
        """Test aafter_agent returns None when no root exists."""
        state = cast(AgentState, MockAgentState(messages=[AIMessage(content="response")]))
        assert await middleware.aafter_agent(state, cast(Runtime, runtime)) is None


class TestWrapCalls:
    """Tests for wrap_model_call and wrap_tool_call methods."""

    def test_wrap_model_call(self, middleware: GalileoMiddleware) -> None:
        """Test wrap_model_call wraps handler execution."""
        request = cast(
            AgentState,
            MockRequest(
                state={"messages": [HumanMessage(content="test")]},
                messages=[HumanMessage(content="test")],
                model_settings={"model": "gpt-4"},
            ),
        )
        expected = AIMessage(content="response")
        handler = Mock(return_value=expected)

        result = middleware.wrap_model_call(request, handler)

        assert result == expected
        handler.assert_called_once_with(request)

    def test_wrap_tool_call(self, middleware: GalileoMiddleware) -> None:
        """Test wrap_tool_call wraps handler execution."""
        request = cast(
            AgentState,
            MockRequest(
                state={"messages": [HumanMessage(content="test")]}, tool_call={"name": "calc", "args": {"x": 5}}
            ),
        )
        expected = ToolMessage(content="10", tool_call_id="123")
        handler = Mock(return_value=expected)

        result = middleware.wrap_tool_call(request, handler)

        assert result == expected
        handler.assert_called_once_with(request)

    @pytest.mark.asyncio
    async def test_awrap_model_call(self, middleware: GalileoMiddleware) -> None:
        """Test awrap_model_call wraps async handler."""
        request = cast(
            AgentState,
            MockRequest(
                state={"messages": [HumanMessage(content="test")]},
                messages=[HumanMessage(content="test")],
                model_settings={"model": "gpt-4"},
            ),
        )
        expected = AIMessage(content="response")

        async def async_handler(r):
            return expected

        result = await middleware.awrap_model_call(request, async_handler)
        assert result == expected

    @pytest.mark.asyncio
    async def test_awrap_tool_call(self, middleware: GalileoMiddleware) -> None:
        """Test awrap_tool_call wraps async handler."""
        request = cast(
            AgentState,
            MockRequest(state={"messages": [HumanMessage(content="test")]}, tool_call={"name": "calc", "args": {}}),
        )
        expected = ToolMessage(content="result", tool_call_id="123")

        async def async_handler(r):
            return expected

        result = await middleware.awrap_tool_call(request, async_handler)
        assert result == expected


class TestEdgeCases:
    """Tests for edge cases and error handling."""

    def test_wrap_calls_with_empty_response(self, middleware: GalileoMiddleware) -> None:
        """Test wrap methods handle None/empty responses."""
        request = cast(AgentState, MockRequest(state={"messages": []}, messages=[]))

        assert middleware.wrap_model_call(request, lambda r: None) is None

    @pytest.mark.asyncio
    async def test_awrap_calls_with_empty_response(self, middleware: GalileoMiddleware) -> None:
        """Test async wrap methods handle None/empty responses."""
        request = cast(AgentState, MockRequest(state={"messages": []}, messages=[]))

        async def async_handler(r):
            return None

        result = await middleware.awrap_model_call(request, async_handler)
        assert result is None

    def test_multiple_agent_runs(self, middleware: GalileoMiddleware, runtime: MockRuntime) -> None:
        """Test middleware handles multiple sequential runs."""
        rt = cast(Runtime, runtime)
        for content in ["first", "second"]:
            state = cast(AgentState, MockAgentState(messages=[HumanMessage(content=content)]))
            middleware.before_agent(state, rt)

            end_state = cast(AgentState, MockAgentState(messages=[AIMessage(content=f"{content} response")]))
            middleware.after_agent(end_state, rt)

            assert middleware._root_run_id is None

    @pytest.mark.asyncio
    async def test_multiple_async_agent_runs(self, middleware: GalileoMiddleware, runtime: MockRuntime) -> None:
        """Test async middleware handles multiple sequential runs."""
        rt = cast(Runtime, runtime)
        for content in ["first", "second"]:
            state = cast(AgentState, MockAgentState(messages=[HumanMessage(content=content)]))
            await middleware.abefore_agent(state, rt)

            end_state = cast(AgentState, MockAgentState(messages=[AIMessage(content=f"{content} response")]))
            await middleware.aafter_agent(end_state, rt)

            assert middleware._root_run_id is None


class TestIngestionHook:
    """Tests for ingestion hook functionality."""

    @pytest.fixture(autouse=True)
    def logger_mocks(self):
        with (
            patch("galileo.logger.logger.LogStreams") as mock_logstreams,
            patch("galileo.logger.logger.Projects") as mock_projects,
            patch("galileo.logger.logger.Traces") as mock_traces,
        ):
            setup_mock_traces_client(mock_traces)
            setup_mock_projects_client(mock_projects)
            setup_mock_logstreams_client(mock_logstreams)
            yield

    @pytest.mark.parametrize(
        "middleware_builder",
        [
            lambda hook: GalileoMiddleware(ingestion_hook=hook),
            lambda hook: GalileoMiddleware(galileo_logger=GalileoLogger(), ingestion_hook=hook),
            lambda hook: GalileoMiddleware(galileo_logger=galileo_context.get_logger_instance(), ingestion_hook=hook),
        ],
    )
    def test_ingestion_hook_called(self, middleware_builder) -> None:
        """Test ingestion hook is called during agent flow."""
        mock_hook = Mock()
        middleware = middleware_builder(mock_hook)
        rt = cast(Runtime, MockRuntime())

        middleware.before_agent(cast(AgentState, MockAgentState(messages=[HumanMessage(content="test")])), rt)
        middleware.after_agent(cast(AgentState, MockAgentState(messages=[AIMessage(content="response")])), rt)

        mock_hook.assert_called_once()
