"""Tests for retriever span detection in GalileoObserver."""

from __future__ import annotations

from unittest.mock import patch
from uuid import UUID

import pytest

from galileo_adk.decorator import galileo_retriever
from galileo_adk.observer import GalileoObserver

from .mocks import MockTool, MockToolContext


class MockBaseRetrievalTool:
    """Fake BaseRetrievalTool for testing isinstance detection."""

    def __init__(self, name: str = "vertex_ai_rag") -> None:
        self.name = name


class MockRetrieverSubclass(MockBaseRetrievalTool):
    """Simulates a tool that extends BaseRetrievalTool."""

    def __init__(self, name: str = "custom_rag") -> None:
        super().__init__(name=name)


class MockFunctionTool:
    """Simulates ADK's FunctionTool which stores the wrapped function as tool.func."""

    def __init__(self, func: object, name: str = "function_tool") -> None:
        self.func = func
        self.name = name


@pytest.fixture
def observer() -> GalileoObserver:
    """Create observer with ingestion hook for testing (no credentials needed)."""
    return GalileoObserver(ingestion_hook=lambda r: None)


class TestGalileoRetrieverDecorator:
    """Tests for the @galileo_retriever decorator."""

    def test_decorator_sets_attribute(self) -> None:
        # Given: a plain function
        def my_search(query: str) -> str:
            return "results"

        # When: decorating with @galileo_retriever
        decorated = galileo_retriever(my_search)

        # Then: the function has _galileo_is_retriever = True
        assert getattr(decorated, "_galileo_is_retriever", False) is True

    def test_decorator_preserves_function(self) -> None:
        # Given: a function with specific behavior
        def my_search(query: str) -> str:
            return f"results for {query}"

        # When: decorating with @galileo_retriever
        decorated = galileo_retriever(my_search)

        # Then: the function still works as expected
        assert decorated("test") == "results for test"
        assert decorated is my_search

    def test_decorator_syntax(self) -> None:
        # Given/When: using decorator syntax
        @galileo_retriever
        def my_search(query: str) -> str:
            return "results"

        # Then: the function is marked as a retriever
        assert getattr(my_search, "_galileo_is_retriever", False) is True


class TestIsRetrieverTool:
    """Tests for _is_retriever_tool detection method."""

    def test_regular_tool_is_not_retriever(self, observer: GalileoObserver) -> None:
        # Given: a regular tool without retriever characteristics
        tool = MockTool(name="calculator")

        # When: checking if it's a retriever
        result = observer._is_retriever_tool(tool)

        # Then: it is not detected as a retriever
        assert result is False

    @patch("galileo_adk.observer._BaseRetrievalTool", MockBaseRetrievalTool)
    def test_base_retrieval_tool_instance_is_detected(self, observer: GalileoObserver) -> None:
        # Given: a tool that is an instance of BaseRetrievalTool
        tool = MockBaseRetrievalTool(name="vertex_ai_rag")

        # When: checking if it's a retriever
        result = observer._is_retriever_tool(tool)

        # Then: it is detected as a retriever
        assert result is True

    @patch("galileo_adk.observer._BaseRetrievalTool", MockBaseRetrievalTool)
    def test_base_retrieval_tool_subclass_is_detected(self, observer: GalileoObserver) -> None:
        # Given: a tool that is a subclass of BaseRetrievalTool
        tool = MockRetrieverSubclass(name="custom_rag")

        # When: checking if it's a retriever
        result = observer._is_retriever_tool(tool)

        # Then: it is detected as a retriever
        assert result is True

    def test_decorated_function_tool_is_detected(self, observer: GalileoObserver) -> None:
        # Given: a function decorated with @galileo_retriever wrapped in FunctionTool
        @galileo_retriever
        def my_search(query: str) -> str:
            return "results"

        tool = MockFunctionTool(func=my_search, name="my_search")

        # When: checking if it's a retriever
        result = observer._is_retriever_tool(tool)

        # Then: it is detected as a retriever
        assert result is True

    def test_undecorated_function_tool_is_not_retriever(self, observer: GalileoObserver) -> None:
        # Given: a function NOT decorated with @galileo_retriever wrapped in FunctionTool
        def my_calculator(expression: str) -> str:
            return "42"

        tool = MockFunctionTool(func=my_calculator, name="my_calculator")

        # When: checking if it's a retriever
        result = observer._is_retriever_tool(tool)

        # Then: it is not detected as a retriever
        assert result is False

    @patch("galileo_adk.observer._BaseRetrievalTool", None)
    def test_isinstance_skipped_when_base_class_unavailable(self, observer: GalileoObserver) -> None:
        # Given: BaseRetrievalTool is not importable (None) and tool has no func attribute
        tool = MockBaseRetrievalTool(name="some_retriever")

        # When: checking if it's a retriever
        result = observer._is_retriever_tool(tool)

        # Then: it is NOT detected (isinstance check is skipped, no func attribute)
        assert result is False

    def test_tool_without_func_attribute_is_not_retriever(self, observer: GalileoObserver) -> None:
        # Given: a tool with no func attribute and not a BaseRetrievalTool
        tool = MockTool(name="any_tool")

        # When: checking if it's a retriever
        result = observer._is_retriever_tool(tool)

        # Then: it is not detected
        assert result is False


class TestOnToolStartRetriever:
    """Tests for on_tool_start retriever span creation."""

    def test_decorated_retriever_creates_retriever_span(self, observer: GalileoObserver) -> None:
        # Given: a function decorated with @galileo_retriever wrapped in FunctionTool
        @galileo_retriever
        def my_search(query: str) -> str:
            return "results"

        tool = MockFunctionTool(func=my_search, name="my_search")
        tool_context = MockToolContext()

        # When: starting a tool span
        with patch.object(observer._span_manager, "start_tool") as mock_start:
            observer.on_tool_start(
                tool=tool,
                tool_args={"query": "What is RAG?"},
                tool_context=tool_context,
                parent_run_id=None,
            )

            # Then: start_tool is called with is_retriever=True
            mock_start.assert_called_once()
            call_kwargs = mock_start.call_args.kwargs
            assert call_kwargs["is_retriever"] is True
            assert call_kwargs["name"] == "my_search"

    def test_retriever_tool_extracts_query_from_tool_args(self, observer: GalileoObserver) -> None:
        # Given: a retriever tool with a "query" key in tool_args
        @galileo_retriever
        def my_search(query: str) -> str:
            return "results"

        tool = MockFunctionTool(func=my_search, name="my_search")
        tool_context = MockToolContext()

        # When: starting a tool span
        with patch.object(observer._span_manager, "start_tool") as mock_start:
            observer.on_tool_start(
                tool=tool,
                tool_args={"query": "What is RAG?", "top_k": 5},
                tool_context=tool_context,
                parent_run_id=None,
            )

            # Then: input_data is the query string, not the full serialized args
            call_kwargs = mock_start.call_args.kwargs
            assert call_kwargs["input_data"] == "What is RAG?"

    def test_retriever_tool_falls_back_when_no_query_key(self, observer: GalileoObserver) -> None:
        # Given: a retriever tool without a "query" key in tool_args
        @galileo_retriever
        def my_search(search_text: str) -> str:
            return "results"

        tool = MockFunctionTool(func=my_search, name="my_search")
        tool_context = MockToolContext()

        # When: starting a tool span
        with patch.object(observer._span_manager, "start_tool") as mock_start:
            observer.on_tool_start(
                tool=tool,
                tool_args={"search_text": "What is RAG?"},
                tool_context=tool_context,
                parent_run_id=None,
            )

            # Then: input_data falls back to serialized tool_args
            call_kwargs = mock_start.call_args.kwargs
            assert "search_text" in call_kwargs["input_data"]

    def test_regular_tool_creates_tool_span(self, observer: GalileoObserver) -> None:
        # Given: a regular tool (not a retriever)
        tool = MockTool(name="calculator")
        tool_context = MockToolContext()

        # When: starting a tool span
        with patch.object(observer._span_manager, "start_tool") as mock_start:
            observer.on_tool_start(
                tool=tool,
                tool_args={"expression": "2+2"},
                tool_context=tool_context,
                parent_run_id=None,
            )

            # Then: start_tool is called with is_retriever=False
            call_kwargs = mock_start.call_args.kwargs
            assert call_kwargs["is_retriever"] is False

    def test_on_tool_start_returns_uuid(self, observer: GalileoObserver) -> None:
        # Given: any tool
        tool = MockTool(name="test_tool")
        tool_context = MockToolContext()

        # When: starting a tool span
        run_id = observer.on_tool_start(
            tool=tool,
            tool_args={},
            tool_context=tool_context,
            parent_run_id=None,
        )

        # Then: a valid UUID is returned
        assert isinstance(run_id, UUID)

    @patch("galileo_adk.observer._BaseRetrievalTool", MockBaseRetrievalTool)
    def test_base_retrieval_tool_creates_retriever_span(self, observer: GalileoObserver) -> None:
        # Given: a tool that is an instance of BaseRetrievalTool
        tool = MockBaseRetrievalTool(name="vertex_ai_rag")
        tool_context = MockToolContext()

        # When: starting a tool span
        with patch.object(observer._span_manager, "start_tool") as mock_start:
            observer.on_tool_start(
                tool=tool,
                tool_args={"query": "search this"},
                tool_context=tool_context,
                parent_run_id=None,
            )

            # Then: start_tool is called with is_retriever=True
            mock_start.assert_called_once()
            call_kwargs = mock_start.call_args.kwargs
            assert call_kwargs["is_retriever"] is True
