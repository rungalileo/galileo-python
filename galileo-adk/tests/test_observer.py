"""Unit tests for GalileoObserver extraction methods."""

from unittest.mock import MagicMock

import pytest

from galileo_adk.observer import GalileoObserver


class MockPart:
    """Mock ADK Content Part."""

    def __init__(self, text: str | None = None) -> None:
        self.text = text


class MockContent:
    """Mock ADK Content."""

    def __init__(self, parts: list[MockPart] | None = None, role: str = "user") -> None:
        self.parts = parts or []
        self.role = role


class MockEvent:
    """Mock ADK Event."""

    def __init__(self, content: MockContent | None = None) -> None:
        self.content = content


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
        # Given: an invocation context with session.events
        context = MagicMock()
        event = MockEvent(content=MockContent(parts=[MockPart(text="The answer is 42")]))
        context.session.events = [event]

        # When: extracting final output
        result = observer._extract_final_output(context)

        # Then: the event content is extracted
        assert result == "The answer is 42"

    def test_handles_missing_session_gracefully(self, observer: GalileoObserver) -> None:
        # Given: an invocation context without session
        context = MagicMock(spec=[])

        # When: extracting final output
        result = observer._extract_final_output(context)

        # Then: empty string is returned
        assert result == ""
