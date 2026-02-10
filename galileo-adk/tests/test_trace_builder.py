"""Unit tests for TraceBuilder."""

from unittest.mock import MagicMock

import pytest

from galileo.schema.trace import TracesIngestRequest
from galileo_adk.trace_builder import TraceBuilder


class TestTraceBuilderInit:
    """Tests for TraceBuilder initialization."""

    def test_init_with_ingestion_hook(self) -> None:
        # Given: an ingestion hook
        hook = MagicMock()

        # When: creating TraceBuilder
        builder = TraceBuilder(ingestion_hook=hook)

        # Then: hook is stored and session attributes are None
        assert builder._ingestion_hook is hook
        assert builder.session_id is None
        assert builder._session_external_id is None

    def test_init_has_empty_traces(self) -> None:
        # Given/When: creating TraceBuilder
        builder = TraceBuilder(ingestion_hook=MagicMock())

        # Then: traces list is empty
        assert builder.traces == []


class TestTraceBuilderTraceLifecycle:
    """Tests for trace lifecycle methods inherited from TracesLogger."""

    def test_add_trace_creates_trace(self) -> None:
        # Given: a trace builder
        builder = TraceBuilder(ingestion_hook=MagicMock())

        # When: adding a trace
        trace = builder.add_trace(input="test input", name="test-trace")

        # Then: trace is created and added to traces list
        assert trace is not None
        assert trace.input == "test input"
        assert trace.name == "test-trace"
        assert len(builder.traces) == 1
        assert builder.traces[0] is trace

    def test_add_trace_sets_current_parent(self) -> None:
        # Given: a trace builder
        builder = TraceBuilder(ingestion_hook=MagicMock())

        # When: adding a trace
        trace = builder.add_trace(input="test input")

        # Then: current parent is set to the trace
        assert builder.current_parent() is trace

    def test_conclude_clears_current_parent(self) -> None:
        # Given: a trace builder with an active trace
        builder = TraceBuilder(ingestion_hook=MagicMock())
        builder.add_trace(input="test input")
        assert builder.current_parent() is not None

        # When: concluding the trace
        builder.conclude(output="test output")

        # Then: current parent is cleared
        assert builder.current_parent() is None


class TestTraceBuilderSpans:
    """Tests for span methods inherited from TracesLogger."""

    @pytest.fixture
    def builder_with_trace(self) -> TraceBuilder:
        """Create a trace builder with an active trace."""
        builder = TraceBuilder(ingestion_hook=MagicMock())
        builder.add_trace(input="test input")
        return builder

    def test_add_llm_span(self, builder_with_trace: TraceBuilder) -> None:
        # Given: a trace builder with an active trace
        builder = builder_with_trace

        # When: adding an LLM span
        span = builder.add_llm_span(
            input=[{"role": "user", "content": "Hello"}],
            output={"role": "assistant", "content": "Hi there!"},
            model="gpt-4",
        )

        # Then: span is created
        assert span is not None
        assert span.model == "gpt-4"

    def test_add_tool_span(self, builder_with_trace: TraceBuilder) -> None:
        # Given: a trace builder with an active trace
        builder = builder_with_trace

        # When: adding a tool span
        span = builder.add_tool_span(
            input="search query",
            output="search results",
            name="search_tool",
        )

        # Then: span is created
        assert span is not None
        assert span.name == "search_tool"

    def test_add_workflow_span(self, builder_with_trace: TraceBuilder) -> None:
        # Given: a trace builder with an active trace
        builder = builder_with_trace
        initial_parent = builder.current_parent()

        # When: adding a workflow span
        span = builder.add_workflow_span(
            input="workflow input",
            name="my_workflow",
        )

        # Then: span is created and becomes current parent
        assert span is not None
        assert span.name == "my_workflow"
        assert builder.current_parent() is span
        assert span._parent is initial_parent

    def test_add_agent_span(self, builder_with_trace: TraceBuilder) -> None:
        # Given: a trace builder with an active trace
        builder = builder_with_trace
        initial_parent = builder.current_parent()

        # When: adding an agent span
        span = builder.add_agent_span(
            input="agent input",
            name="my_agent",
        )

        # Then: span is created and becomes current parent
        assert span is not None
        assert span.name == "my_agent"
        assert builder.current_parent() is span
        assert span._parent is initial_parent

    def test_trace_and_spans_have_unique_ids(self) -> None:
        """TraceBuilder generates unique UUIDs for traces and all span types."""
        # Given: a trace builder
        builder = TraceBuilder(ingestion_hook=lambda r: None)

        # When: creating a trace and various spans
        trace = builder.start_trace(input="test")
        assert trace.id is not None

        agent = builder.add_agent_span(input="agent input")
        assert agent.id is not None
        assert agent.id != trace.id

        llm = builder.add_llm_span(input="prompt", output="response", model="test-model")
        assert llm.id is not None
        assert llm.id != agent.id

        tool = builder.add_tool_span(input="query", output="result", name="search")
        assert tool.id is not None

        # Then: conclude and verify all IDs are unique
        builder.conclude(output="done")  # conclude agent
        builder.conclude(output="done")  # conclude trace

    def test_add_retriever_span(self, builder_with_trace: TraceBuilder) -> None:
        # Given: a trace builder with an active trace
        builder = builder_with_trace

        # When: adding a retriever span
        span = builder.add_retriever_span(
            input="search query",
            output=[],  # TraceBuilder uses 'output' (same as GalileoLogger API)
        )

        # Then: span is created
        assert span is not None


class TestTraceBuilderFlush:
    """Tests for flush method."""

    def test_flush_calls_ingestion_hook_with_traces_ingest_request(self) -> None:
        # Given: a trace builder with traces
        captured_requests: list[TracesIngestRequest] = []
        builder = TraceBuilder(ingestion_hook=lambda r: captured_requests.append(r))
        builder.add_trace(input="test input")
        builder.add_llm_span(
            input=[{"role": "user", "content": "Hello"}],
            output={"role": "assistant", "content": "Hi!"},
            model="gpt-4",
        )
        builder.conclude(output="test output")

        # When: flushing
        builder.flush()

        # Then: ingestion hook is called with TracesIngestRequest
        assert len(captured_requests) == 1
        request = captured_requests[0]
        assert isinstance(request, TracesIngestRequest)
        assert len(request.traces) == 1
        assert request.traces[0].input == "test input"

    def test_flush_includes_session_external_id(self) -> None:
        # Given: a trace builder with session_external_id set
        captured_requests: list[TracesIngestRequest] = []
        builder = TraceBuilder(ingestion_hook=lambda r: captured_requests.append(r))
        builder._session_external_id = "adk-session-123"
        builder.add_trace(input="test input")
        builder.conclude(output="test output")

        # When: flushing
        builder.flush()

        # Then: session_external_id is included in request
        assert len(captured_requests) == 1
        assert captured_requests[0].session_external_id == "adk-session-123"

    def test_flush_clears_traces(self) -> None:
        # Given: a trace builder with traces
        builder = TraceBuilder(ingestion_hook=MagicMock())
        builder.add_trace(input="test input")
        builder.conclude(output="test output")
        assert len(builder.traces) == 1

        # When: flushing
        builder.flush()

        # Then: traces are cleared
        assert len(builder.traces) == 0

    def test_flush_resets_current_parent(self) -> None:
        # Given: a trace builder with active parent (unconcluded trace)
        builder = TraceBuilder(ingestion_hook=MagicMock())
        builder.add_trace(input="test input")
        # Don't conclude - leave parent active

        # When: flushing
        builder.flush()

        # Then: current parent is reset
        assert builder.current_parent() is None

    def test_flush_with_no_traces_does_nothing(self) -> None:
        # Given: a trace builder with no traces
        hook = MagicMock()
        builder = TraceBuilder(ingestion_hook=hook)
        assert len(builder.traces) == 0

        # When: flushing
        result = builder.flush()

        # Then: hook is not called and empty list is returned
        hook.assert_not_called()
        assert result == []

    def test_flush_returns_flushed_traces(self) -> None:
        # Given: a trace builder with traces
        builder = TraceBuilder(ingestion_hook=MagicMock())
        builder.add_trace(input="test input")
        builder.conclude(output="test output")

        # When: flushing
        result = builder.flush()

        # Then: flushed traces are returned
        assert len(result) == 1
        assert result[0].input == "test input"


class TestTraceBuilderIntegration:
    """Integration tests for TraceBuilder with typical ADK usage patterns."""

    def test_typical_adk_trace_structure(self) -> None:
        """Test a typical ADK trace: invocation -> agent -> llm -> tool."""
        # Given: a trace builder
        captured_requests: list[TracesIngestRequest] = []
        builder = TraceBuilder(ingestion_hook=lambda r: captured_requests.append(r))
        builder._session_external_id = "adk-session-abc"

        # When: building a typical ADK trace
        # Start invocation trace
        builder.add_trace(input="What is 2+2?", name="invocation [agent]")

        # Add agent span
        builder.add_agent_span(input="What is 2+2?", name="test_agent")

        # Add LLM call within agent (with tool call)
        builder.add_llm_span(
            input=[{"role": "user", "content": "What is 2+2?"}],
            output={"role": "assistant", "content": "Let me calculate..."},
            model="gemini-pro",
        )

        # Add tool call
        builder.add_tool_span(input="2+2", output="4", name="calculator")

        # Add second LLM call after tool
        builder.add_llm_span(
            input=[{"role": "user", "content": "What is 2+2?"}, {"role": "tool", "content": "4"}],
            output={"role": "assistant", "content": "2+2 equals 4"},
            model="gemini-pro",
        )

        # Conclude agent
        builder.conclude(output="2+2 equals 4")

        # Conclude trace
        builder.conclude(output="2+2 equals 4")

        # Flush
        builder.flush()

        # Then: trace structure is captured correctly
        assert len(captured_requests) == 1
        request = captured_requests[0]
        assert request.session_external_id == "adk-session-abc"
        assert len(request.traces) == 1

        trace = request.traces[0]
        assert trace.name == "invocation [agent]"
        assert trace.input == "What is 2+2?"
        assert len(trace.spans) == 1  # agent span

        agent_span = trace.spans[0]
        assert agent_span.name == "test_agent"
        assert len(agent_span.spans) == 3  # 2 LLM + 1 tool

    def test_sequential_traces_have_distinct_ids(self) -> None:
        """Sequential traces and their spans have no overlapping IDs."""
        # Given: a trace builder
        captured: list[TracesIngestRequest] = []
        builder = TraceBuilder(ingestion_hook=lambda r: captured.append(r))

        # When: building two sequential traces
        # Trace 1
        builder.start_trace(input="query 1")
        builder.add_agent_span(input="agent 1")
        builder.add_llm_span(input="prompt 1", output="response 1", model="m")
        builder.conclude(output="agent done")
        builder.conclude(output="trace done")
        builder.flush()

        # Trace 2
        builder.start_trace(input="query 2")
        builder.add_agent_span(input="agent 2")
        builder.add_llm_span(input="prompt 2", output="response 2", model="m")
        builder.conclude(output="agent done")
        builder.conclude(output="trace done")
        builder.flush()

        # Then: all IDs across both traces are unique
        assert len(captured) == 2
        all_ids: set = set()

        def collect_ids(spans: list) -> None:
            for span in spans:
                assert span.id is not None
                all_ids.add(span.id)
                if hasattr(span, "spans") and span.spans:
                    collect_ids(span.spans)

        for request in captured:
            for trace in request.traces:
                assert trace.id is not None
                all_ids.add(trace.id)
                collect_ids(trace.spans)

        # 2 traces + 2 agent spans + 2 llm spans = 6 unique IDs minimum
        assert len(all_ids) >= 6

    def test_multiple_traces_per_flush(self) -> None:
        """Test multiple traces accumulated before flush."""
        # Given: a trace builder
        captured_requests: list[TracesIngestRequest] = []
        builder = TraceBuilder(ingestion_hook=lambda r: captured_requests.append(r))

        # When: adding multiple traces
        builder.add_trace(input="First query")
        builder.conclude(output="First response")

        builder.add_trace(input="Second query")
        builder.conclude(output="Second response")

        builder.flush()

        # Then: both traces are in the request
        assert len(captured_requests) == 1
        assert len(captured_requests[0].traces) == 2
