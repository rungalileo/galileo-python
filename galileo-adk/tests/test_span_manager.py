"""Tests for SpanManager span lifecycle management."""

from unittest.mock import MagicMock
from uuid import uuid4

import pytest

from galileo_adk.span_manager import INTEGRATION_TAG, SpanManager


class TestSpanManagerRunSpans:
    """Tests for run (invocation) span lifecycle."""

    @pytest.fixture
    def mock_handler(self) -> MagicMock:
        handler = MagicMock()
        handler.start_node = MagicMock()
        handler.end_node = MagicMock()
        return handler

    @pytest.fixture
    def span_manager(self, mock_handler: MagicMock) -> SpanManager:
        return SpanManager(mock_handler)

    def test_start_run_creates_chain_node(self, span_manager: SpanManager, mock_handler: MagicMock) -> None:
        """start_run creates a chain node with correct attributes."""
        run_id = uuid4()
        span_manager.start_run(run_id, "Hello", agent_name="test_agent")

        mock_handler.start_node.assert_called_once()
        call_kwargs = mock_handler.start_node.call_args.kwargs
        assert call_kwargs["node_type"] == "chain"
        assert call_kwargs["name"] == "invocation [test_agent]"
        assert call_kwargs["run_id"] == run_id
        assert call_kwargs["input"] == "Hello"
        assert INTEGRATION_TAG in call_kwargs["tags"]
        assert "invocation" in call_kwargs["tags"]

    def test_start_run_with_metadata(self, span_manager: SpanManager, mock_handler: MagicMock) -> None:
        """start_run passes metadata to handler."""
        run_id = uuid4()
        metadata = {"env": "test", "version": "1.0"}
        span_manager.start_run(run_id, "Hello", metadata=metadata)

        call_kwargs = mock_handler.start_node.call_args.kwargs
        assert call_kwargs["metadata"] == metadata

    def test_start_run_with_parent(self, span_manager: SpanManager, mock_handler: MagicMock) -> None:
        """start_run accepts parent_run_id for nested invocations."""
        run_id = uuid4()
        parent_id = uuid4()
        span_manager.start_run(run_id, "Hello", parent_run_id=parent_id)

        call_kwargs = mock_handler.start_node.call_args.kwargs
        assert call_kwargs["parent_run_id"] == parent_id

    def test_end_run_sets_output(self, span_manager: SpanManager, mock_handler: MagicMock) -> None:
        """end_run sets output correctly."""
        run_id = uuid4()
        span_manager.start_run(run_id, "Hello")
        span_manager.end_run(run_id, "Goodbye")

        call_kwargs = mock_handler.end_node.call_args.kwargs
        assert call_kwargs["output"] == "Goodbye"

    def test_end_run_with_status_code(self, span_manager: SpanManager, mock_handler: MagicMock) -> None:
        """end_run passes status_code to handler."""
        run_id = uuid4()
        span_manager.start_run(run_id, "Hello")
        span_manager.end_run(run_id, "Error", status_code=500)

        call_kwargs = mock_handler.end_node.call_args.kwargs
        assert call_kwargs["status_code"] == 500


class TestSpanManagerAgentSpans:
    """Tests for agent span lifecycle."""

    @pytest.fixture
    def mock_handler(self) -> MagicMock:
        handler = MagicMock()
        handler.start_node = MagicMock()
        handler.end_node = MagicMock()
        return handler

    @pytest.fixture
    def span_manager(self, mock_handler: MagicMock) -> SpanManager:
        return SpanManager(mock_handler)

    def test_start_agent_creates_agent_node(self, span_manager: SpanManager, mock_handler: MagicMock) -> None:
        """start_agent creates an agent node with correct attributes."""
        run_id = uuid4()
        parent_id = uuid4()
        span_manager.start_agent(run_id, parent_id, "test input", name="my_agent")

        mock_handler.start_node.assert_called_once()
        call_kwargs = mock_handler.start_node.call_args.kwargs
        assert call_kwargs["node_type"] == "agent"
        assert call_kwargs["name"] == "agent_run [my_agent]"
        assert call_kwargs["parent_run_id"] == parent_id
        assert "agent:my_agent" in call_kwargs["tags"]

    def test_start_agent_with_metadata(self, span_manager: SpanManager, mock_handler: MagicMock) -> None:
        """start_agent passes metadata to handler."""
        run_id = uuid4()
        metadata = {"turn": 1}
        span_manager.start_agent(run_id, None, "input", name="agent", metadata=metadata)

        call_kwargs = mock_handler.start_node.call_args.kwargs
        assert call_kwargs["metadata"] == metadata

    def test_end_agent_sets_output(self, span_manager: SpanManager, mock_handler: MagicMock) -> None:
        """end_agent sets output and status code."""
        run_id = uuid4()
        span_manager.end_agent(run_id, "agent output")

        call_kwargs = mock_handler.end_node.call_args.kwargs
        assert call_kwargs["output"] == "agent output"
        assert call_kwargs["status_code"] == 200


class TestSpanManagerLlmSpans:
    """Tests for LLM span lifecycle."""

    @pytest.fixture
    def mock_handler(self) -> MagicMock:
        handler = MagicMock()
        handler.start_node = MagicMock()
        handler.end_node = MagicMock()
        return handler

    @pytest.fixture
    def span_manager(self, mock_handler: MagicMock) -> SpanManager:
        return SpanManager(mock_handler)

    def test_start_llm_creates_llm_node(self, span_manager: SpanManager, mock_handler: MagicMock) -> None:
        """start_llm creates an llm node with correct attributes."""
        run_id = uuid4()
        parent_id = uuid4()
        span_manager.start_llm(
            run_id,
            parent_id,
            "prompt messages",
            model="gemini-2.0-flash",
            temperature=0.7,
        )

        mock_handler.start_node.assert_called_once()
        call_kwargs = mock_handler.start_node.call_args.kwargs
        assert call_kwargs["node_type"] == "llm"
        assert call_kwargs["name"] == "call_llm"
        assert call_kwargs["model"] == "gemini-2.0-flash"
        assert call_kwargs["temperature"] == 0.7
        assert "llm" in call_kwargs["tags"]

    def test_start_llm_with_tools(self, span_manager: SpanManager, mock_handler: MagicMock) -> None:
        """start_llm includes tools in node creation."""
        run_id = uuid4()
        tools = [{"type": "function", "function": {"name": "search"}}]
        span_manager.start_llm(run_id, None, "prompt", tools=tools)

        call_kwargs = mock_handler.start_node.call_args.kwargs
        assert call_kwargs["tools"] == tools

    def test_end_llm_includes_token_counts(self, span_manager: SpanManager, mock_handler: MagicMock) -> None:
        """end_llm passes token counts to handler."""
        run_id = uuid4()
        span_manager.end_llm(
            run_id,
            "response",
            num_input_tokens=100,
            num_output_tokens=50,
            total_tokens=150,
        )

        call_kwargs = mock_handler.end_node.call_args.kwargs
        assert call_kwargs["num_input_tokens"] == 100
        assert call_kwargs["num_output_tokens"] == 50
        assert call_kwargs["total_tokens"] == 150

    def test_end_llm_normalizes_empty_list(self, span_manager: SpanManager, mock_handler: MagicMock) -> None:
        """end_llm normalizes empty list output to None."""
        run_id = uuid4()
        span_manager.end_llm(run_id, [])

        call_kwargs = mock_handler.end_node.call_args.kwargs
        assert call_kwargs["output"] is None

    def test_end_llm_unwraps_single_element_list(self, span_manager: SpanManager, mock_handler: MagicMock) -> None:
        """end_llm unwraps single-element list to just the element."""
        run_id = uuid4()
        messages = [{"role": "assistant", "content": "Hello"}]
        span_manager.end_llm(run_id, messages)

        call_kwargs = mock_handler.end_node.call_args.kwargs
        # Single-element list gets unwrapped per span_manager.end_llm docstring
        assert call_kwargs["output"] == {"role": "assistant", "content": "Hello"}


class TestSpanManagerToolSpans:
    """Tests for tool span lifecycle."""

    @pytest.fixture
    def mock_handler(self) -> MagicMock:
        handler = MagicMock()
        handler.start_node = MagicMock()
        handler.end_node = MagicMock()
        return handler

    @pytest.fixture
    def span_manager(self, mock_handler: MagicMock) -> SpanManager:
        return SpanManager(mock_handler)

    def test_start_tool_creates_tool_node(self, span_manager: SpanManager, mock_handler: MagicMock) -> None:
        """start_tool creates a tool node with correct attributes."""
        run_id = uuid4()
        parent_id = uuid4()
        span_manager.start_tool(
            run_id,
            parent_id,
            '{"query": "test"}',
            name="search",
        )

        mock_handler.start_node.assert_called_once()
        call_kwargs = mock_handler.start_node.call_args.kwargs
        assert call_kwargs["node_type"] == "tool"
        assert call_kwargs["name"] == "execute_tool [search]"
        assert "tool" in call_kwargs["tags"]
        assert "tool:search" in call_kwargs["tags"]

    def test_start_tool_with_metadata(self, span_manager: SpanManager, mock_handler: MagicMock) -> None:
        """start_tool passes metadata to handler."""
        run_id = uuid4()
        metadata = {"request_id": "abc123"}
        span_manager.start_tool(run_id, None, "{}", name="calc", metadata=metadata)

        call_kwargs = mock_handler.start_node.call_args.kwargs
        assert call_kwargs["metadata"] == metadata

    def test_end_tool_sets_output(self, span_manager: SpanManager, mock_handler: MagicMock) -> None:
        """end_tool sets output string."""
        run_id = uuid4()
        span_manager.end_tool(run_id, '{"result": 42}')

        call_kwargs = mock_handler.end_node.call_args.kwargs
        assert call_kwargs["output"] == '{"result": 42}'
        assert call_kwargs["status_code"] == 200

    def test_end_tool_with_error_status(self, span_manager: SpanManager, mock_handler: MagicMock) -> None:
        """end_tool can set error status code."""
        run_id = uuid4()
        span_manager.end_tool(run_id, "Error: tool failed", status_code=500)

        call_kwargs = mock_handler.end_node.call_args.kwargs
        assert call_kwargs["status_code"] == 500

    def test_start_tool_as_retriever_creates_retriever_node(
        self, span_manager: SpanManager, mock_handler: MagicMock
    ) -> None:
        """start_tool with is_retriever=True creates a retriever node."""
        # Given: a tool call marked as retriever
        run_id = uuid4()
        parent_id = uuid4()

        # When: starting a tool with is_retriever=True
        span_manager.start_tool(
            run_id,
            parent_id,
            "what is the meaning of life?",
            name="rag_retriever",
            is_retriever=True,
        )

        # Then: the span has retriever node_type, name, and tags
        mock_handler.start_node.assert_called_once()
        call_kwargs = mock_handler.start_node.call_args.kwargs
        assert call_kwargs["node_type"] == "retriever"
        assert call_kwargs["name"] == "retriever [rag_retriever]"
        assert "retriever" in call_kwargs["tags"]
        assert "retriever:rag_retriever" in call_kwargs["tags"]
        assert INTEGRATION_TAG in call_kwargs["tags"]

    def test_start_tool_default_is_not_retriever(self, span_manager: SpanManager, mock_handler: MagicMock) -> None:
        """start_tool defaults to tool node when is_retriever is not specified."""
        # Given: a regular tool call (no is_retriever argument)
        run_id = uuid4()

        # When: starting a tool without is_retriever
        span_manager.start_tool(run_id, None, "{}", name="calculator")

        # Then: the span is a regular tool node
        call_kwargs = mock_handler.start_node.call_args.kwargs
        assert call_kwargs["node_type"] == "tool"
        assert call_kwargs["name"] == "execute_tool [calculator]"
