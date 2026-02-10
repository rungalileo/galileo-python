"""Unit tests for GalileoObserver extraction methods."""

from unittest.mock import MagicMock

import pytest

from galileo_adk.observer import GalileoObserver

from .mocks import MockContent, MockEvent, MockPart


@pytest.fixture
def observer() -> GalileoObserver:
    """Create observer with ingestion hook for testing (no credentials needed)."""
    return GalileoObserver(ingestion_hook=lambda r: None)


class TestExtractInvocationMetadata:
    """Tests for _extract_invocation_metadata method."""

    def test_extracts_invocation_id(self, observer: GalileoObserver) -> None:
        # Given: an invocation context with an invocation_id
        context = MagicMock()
        context.invocation_id = "inv_123"
        del context.session

        # When: extracting metadata
        result = observer._extract_invocation_metadata(context)

        # Then: invocation_id is included
        assert result["invocation_id"] == "inv_123"

    def test_extracts_session_id_from_nested_session(self, observer: GalileoObserver) -> None:
        # Given: an invocation context with a nested session
        context = MagicMock()
        context.invocation_id = "inv_123"
        context.session.id = "sess_456"

        # When: extracting metadata
        result = observer._extract_invocation_metadata(context)

        # Then: both invocation_id and session_id are included
        assert result["invocation_id"] == "inv_123"
        assert result["session_id"] == "sess_456"

    def test_missing_attributes_returns_empty_metadata(self, observer: GalileoObserver) -> None:
        # Given: a context without invocation_id or session
        context = MagicMock(spec=[])  # Empty spec means no attributes

        # When: extracting metadata
        result = observer._extract_invocation_metadata(context)

        # Then: result is an empty dict (or contains only global metadata)
        assert "invocation_id" not in result
        assert "session_id" not in result


class TestExtractAgentInput:
    """Tests for _extract_agent_input method."""

    def test_extracts_from_parent_context_new_message(self, observer: GalileoObserver) -> None:
        # Given: a callback context with parent_context.new_message
        context = MagicMock()
        context.parent_context.new_message.parts = [MockPart(text="Hello, agent!")]

        # When: extracting agent input
        result = observer._extract_agent_input(context)

        # Then: the text is extracted
        assert result == "Hello, agent!"

    def test_fallback_when_no_parent_context(self, observer: GalileoObserver) -> None:
        # Given: a context without parent_context
        context = MagicMock(spec=[])

        # When: extracting agent input
        result = observer._extract_agent_input(context)

        # Then: fallback message is returned
        assert result == "Agent invocation"

    def test_extracts_multiple_parts(self, observer: GalileoObserver) -> None:
        # Given: a callback context with multiple text parts
        context = MagicMock()
        context.parent_context.new_message.parts = [
            MockPart(text="Hello"),
            MockPart(text="World"),
        ]

        # When: extracting agent input
        result = observer._extract_agent_input(context)

        # Then: both parts are joined
        assert "Hello" in result
        assert "World" in result


class TestExtractAgentOutput:
    """Tests for _extract_agent_output method."""

    def test_extracts_from_last_event(self, observer: GalileoObserver) -> None:
        # Given: a context with parent_context.events containing output
        context = MagicMock()
        event1 = MockEvent(content=MockContent(parts=[MockPart(text="Processing...")]))
        event2 = MockEvent(content=MockContent(parts=[MockPart(text="Final answer")]))
        context.parent_context.events = [event1, event2]

        # When: extracting agent output
        result = observer._extract_agent_output(context)

        # Then: the last event's content is extracted
        assert result == "Final answer"

    def test_returns_empty_when_no_events(self, observer: GalileoObserver) -> None:
        # Given: a context without events
        context = MagicMock()
        context.parent_context.events = []

        # When: extracting agent output
        result = observer._extract_agent_output(context)

        # Then: empty string is returned
        assert result == ""


class TestExtractTools:
    """Tests for _extract_tools method."""

    def test_converts_tools_when_present(self, observer: GalileoObserver) -> None:
        # Given: an LLM request with tools in config
        request = MagicMock()
        tool = MagicMock()
        tool.name = "search"
        tool.description = "Search the web"
        tool.parameters_schema = {"type": "object", "properties": {"query": {"type": "string"}}}
        request.config.tools = [tool]

        # When: extracting tools
        result = observer._extract_tools(request)

        # Then: tools are converted to OpenAI format
        assert result is not None
        assert len(result) == 1
        assert result[0]["type"] == "function"
        assert result[0]["function"]["name"] == "search"

    def test_returns_none_when_no_tools(self, observer: GalileoObserver) -> None:
        # Given: an LLM request without tools
        request = MagicMock()
        request.config.tools = None

        # When: extracting tools
        result = observer._extract_tools(request)

        # Then: None is returned
        assert result is None


class TestExtractFinalOutput:
    """Tests for _extract_final_output method."""

    def test_extracts_from_session_events(self, observer: GalileoObserver) -> None:
        # Given: an invocation context with session.events containing a final response
        context = MagicMock()
        event = MockEvent(content=MockContent(parts=[MockPart(text="The answer is 42")]), is_final=True)
        context.session.events = [event]

        # When: extracting final output
        result = observer._extract_final_output(context)

        # Then: the final response content is extracted
        assert result == "The answer is 42"

    def test_finds_final_response_not_at_end(self, observer: GalileoObserver) -> None:
        # Given: session.events where final response is not the last event
        context = MagicMock()
        tool_call = MockEvent(content=MockContent(parts=[MockPart(text="calling tool")]), is_final=False)
        final_response = MockEvent(content=MockContent(parts=[MockPart(text="The answer is 42")]), is_final=True)
        tool_result = MockEvent(content=MockContent(parts=[MockPart(text='{"result": 42}')]), is_final=False)
        context.session.events = [tool_call, final_response, tool_result]

        # When: extracting final output
        result = observer._extract_final_output(context)

        # Then: the final response content is extracted (not the last event)
        assert result == "The answer is 42"

    def test_returns_empty_when_no_final_response(self, observer: GalileoObserver) -> None:
        # Given: session.events with no final response
        context = MagicMock()
        tool_call = MockEvent(content=MockContent(parts=[MockPart(text="calling tool")]), is_final=False)
        tool_result = MockEvent(content=MockContent(parts=[MockPart(text='{"result": 42}')]), is_final=False)
        context.session.events = [tool_call, tool_result]

        # When: extracting final output
        result = observer._extract_final_output(context)

        # Then: empty string is returned (no misleading data)
        assert result == ""

    def test_handles_missing_session_gracefully(self, observer: GalileoObserver) -> None:
        # Given: an invocation context without session
        context = MagicMock(spec=[])

        # When: extracting final output
        result = observer._extract_final_output(context)

        # Then: empty string is returned
        assert result == ""


class TestUpdateSessionIfChanged:
    """Tests for update_session_if_changed method."""

    def test_hook_mode_sets_session_external_id_without_backend_call(self) -> None:
        # Given: an observer in hook mode
        captured_requests: list = []
        observer = GalileoObserver(ingestion_hook=lambda r: captured_requests.append(r))
        logger = observer._handler._galileo_logger

        # When: updating session with an ADK session ID
        observer.update_session_if_changed("adk-session-123")

        # Then: session_external_id is set for correlation
        assert logger._session_external_id == "adk-session-123"
        assert observer._current_adk_session == "adk-session-123"

    def test_hook_mode_updates_external_id_on_session_change(self) -> None:
        # Given: an observer in hook mode with an existing session
        observer = GalileoObserver(ingestion_hook=lambda r: None)
        observer.update_session_if_changed("session-1")
        logger = observer._handler._galileo_logger

        # When: the ADK session changes
        observer.update_session_if_changed("session-2")

        # Then: session_external_id is updated to the new session
        assert logger._session_external_id == "session-2"
        assert observer._current_adk_session == "session-2"

    def test_hook_mode_ignores_unknown_session_id(self) -> None:
        # Given: an observer in hook mode
        observer = GalileoObserver(ingestion_hook=lambda r: None)
        logger = observer._handler._galileo_logger

        # When: updating with "unknown" session ID
        observer.update_session_if_changed("unknown")

        # Then: no session is set
        assert logger._session_external_id is None
        assert observer._current_adk_session is None

    def test_hook_mode_ignores_duplicate_session_id(self) -> None:
        # Given: an observer in hook mode with an existing session
        observer = GalileoObserver(ingestion_hook=lambda r: None)
        observer.update_session_if_changed("session-1")
        logger = observer._handler._galileo_logger
        original_external_id = logger._session_external_id

        # When: updating with the same session ID
        observer.update_session_if_changed("session-1")

        # Then: session_external_id remains unchanged
        assert logger._session_external_id == original_external_id

    def test_hook_mode_preserves_parent_session_for_sub_invocations(self) -> None:
        # Given: an observer in hook mode with an existing parent session
        observer = GalileoObserver(ingestion_hook=lambda r: None)
        observer.update_session_if_changed("parent-session")
        logger = observer._handler._galileo_logger

        # When: a sub-invocation tries to change the session
        observer.update_session_if_changed("sub-invocation-session", is_sub_invocation=True)

        # Then: the parent session is preserved
        assert logger._session_external_id == "parent-session"
        assert observer._current_adk_session == "parent-session"
