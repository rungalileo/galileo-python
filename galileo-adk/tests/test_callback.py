from collections.abc import Generator
from unittest.mock import MagicMock, patch

import pytest

from galileo_adk import GalileoADKCallback

from .mocks import (
    MockCallbackContext,
    MockContent,
    MockLlmRequest,
    MockLlmResponse,
    MockPart,
    MockRunConfig,
    MockToolContext,
)


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
def adk_user_message() -> Generator[MagicMock, None, None]:
    """Create a mock ADK user message (types.Content)."""
    message = MagicMock()
    message.parts = [MagicMock(text="Hello, world!")]
    return message


class TestGalileoADKCallbackInit:
    """Tests for callback initialization validation."""

    def test_init_requires_project_and_log_stream(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """Callback raises error when neither project/log_stream nor hook provided."""
        # Given: GALILEO_PROJECT and GALILEO_LOG_STREAM env vars are not set
        monkeypatch.delenv("GALILEO_PROJECT", raising=False)
        monkeypatch.delenv("GALILEO_LOG_STREAM", raising=False)

        # When/Then: creating callback without project or log_stream raises an error
        with pytest.raises(ValueError, match="Both 'project' and 'log_stream' must be provided"):
            GalileoADKCallback()

    def test_init_requires_log_stream(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """Callback raises error when project is provided but log_stream is not."""
        # Given: GALILEO_LOG_STREAM env var is not set
        monkeypatch.delenv("GALILEO_LOG_STREAM", raising=False)

        # When/Then: creating callback with project but no log_stream raises an error
        with pytest.raises(ValueError, match="Both 'project' and 'log_stream' must be provided"):
            GalileoADKCallback(project="my-project")

    def test_init_requires_project(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """Callback raises error when log_stream is provided but project is not."""
        # Given: GALILEO_PROJECT env var is not set
        monkeypatch.delenv("GALILEO_PROJECT", raising=False)

        # When/Then: creating callback with log_stream but no project raises an error
        with pytest.raises(ValueError, match="Both 'project' and 'log_stream' must be provided"):
            GalileoADKCallback(log_stream="my-stream")


class TestGalileoADKCallback:
    @pytest.fixture
    def callback(self) -> GalileoADKCallback:
        return GalileoADKCallback(ingestion_hook=lambda r: None)

    def test_initialization_with_ingestion_hook(self) -> None:
        callback = GalileoADKCallback(ingestion_hook=lambda r: None)
        assert callback._handler is not None

    def test_initialization_with_project_and_log_stream(self) -> None:
        with patch("galileo_adk.observer.galileo_context") as mock_context:
            mock_logger = MagicMock()
            mock_context.get_logger_instance.return_value = mock_logger

            callback = GalileoADKCallback(project="test-project", log_stream="test-stream")

            mock_context.get_logger_instance.assert_called_once_with(
                project="test-project",
                log_stream="test-stream",
            )
            assert callback._handler._galileo_logger == mock_logger

    def test_initialization_defaults(self) -> None:
        callback = GalileoADKCallback(ingestion_hook=lambda r: None)

        assert callback._handler._start_new_trace is True
        assert callback._handler._flush_on_chain_end is True
        assert callback._handler._integration == "google_adk"

    def test_before_agent_callback(self, callback: GalileoADKCallback, adk_callback_context: MagicMock) -> None:
        result = callback.before_agent_callback(adk_callback_context)

        assert result is None
        assert callback._tracker.agent_count == 1
        assert len(callback._handler._nodes) == 1

    def test_after_agent_callback(self, callback: GalileoADKCallback, adk_callback_context: MagicMock) -> None:
        callback.before_agent_callback(adk_callback_context)

        result = callback.after_agent_callback(adk_callback_context)

        assert result is None
        assert len(callback._handler._nodes) == 0

    def test_before_model_callback(
        self,
        callback: GalileoADKCallback,
        adk_callback_context: MagicMock,
        adk_llm_request: MagicMock,
    ) -> None:
        callback.before_agent_callback(adk_callback_context)

        result = callback.before_model_callback(adk_callback_context, adk_llm_request)

        assert result is None
        assert callback._tracker.llm_count == 1
        assert len(callback._handler._nodes) == 2

    def test_after_model_callback(
        self,
        callback: GalileoADKCallback,
        adk_callback_context: MagicMock,
        adk_llm_request: MagicMock,
        adk_llm_response: MagicMock,
    ) -> None:
        callback.before_agent_callback(adk_callback_context)
        callback.before_model_callback(adk_callback_context, adk_llm_request)

        result = callback.after_model_callback(adk_callback_context, adk_llm_response)

        assert result is None
        assert len(callback._handler._nodes) == 2

    def test_before_tool_callback(
        self,
        callback: GalileoADKCallback,
        adk_callback_context: MagicMock,
        adk_tool: MagicMock,
        adk_tool_context: MagicMock,
    ) -> None:
        adk_tool_context.callback_context = adk_callback_context
        callback.before_agent_callback(adk_callback_context)

        tool_args = {"arg1": "value1"}
        result = callback.before_tool_callback(adk_tool, tool_args, adk_tool_context)

        assert result is None
        assert callback._tracker.tool_count == 1
        assert len(callback._handler._nodes) == 2

    def test_after_tool_callback(
        self,
        callback: GalileoADKCallback,
        adk_callback_context: MagicMock,
        adk_tool: MagicMock,
        adk_tool_context: MagicMock,
    ) -> None:
        adk_tool_context.callback_context = adk_callback_context
        callback.before_agent_callback(adk_callback_context)

        tool_args = {"arg1": "value1"}
        callback.before_tool_callback(adk_tool, tool_args, adk_tool_context)

        result_data = {"output": "result"}
        result = callback.after_tool_callback(adk_tool, tool_args, adk_tool_context, result_data)

        assert result is None
        assert len(callback._handler._nodes) == 2

    def test_full_trace_lifecycle(
        self,
        callback: GalileoADKCallback,
        adk_callback_context: MagicMock,
        adk_llm_request: MagicMock,
        adk_llm_response: MagicMock,
        adk_tool: MagicMock,
        adk_tool_context: MagicMock,
    ) -> None:
        adk_tool_context.callback_context = adk_callback_context

        callback.before_agent_callback(adk_callback_context)
        assert len(callback._handler._nodes) == 1

        callback.before_model_callback(adk_callback_context, adk_llm_request)
        assert len(callback._handler._nodes) == 2

        callback.after_model_callback(adk_callback_context, adk_llm_response)
        assert len(callback._handler._nodes) == 2

        tool_args = {"query": "test"}
        callback.before_tool_callback(adk_tool, tool_args, adk_tool_context)
        assert len(callback._handler._nodes) == 3

        callback.after_tool_callback(adk_tool, tool_args, adk_tool_context, {"result": "success"})
        assert len(callback._handler._nodes) == 3

        callback.after_agent_callback(adk_callback_context)
        assert len(callback._handler._nodes) == 0

    def test_error_handling_before_agent(self, callback: GalileoADKCallback, adk_callback_context: MagicMock) -> None:
        adk_callback_context.agent_name = property(lambda x: 1 / 0)  # noqa: B017

        result = callback.before_agent_callback(adk_callback_context)
        assert result is None

    def test_error_handling_after_agent_without_run_id(
        self, callback: GalileoADKCallback, adk_callback_context: MagicMock
    ) -> None:
        result = callback.after_agent_callback(adk_callback_context)
        assert result is None

    def test_extract_agent_input(self, callback: GalileoADKCallback, adk_callback_context: MagicMock) -> None:
        parent_context = MagicMock()
        parent_context.new_message = MagicMock()
        parent_context.new_message.parts = [MagicMock(text="Hello")]
        adk_callback_context.parent_context = parent_context

        result = callback._observer._extract_agent_input(adk_callback_context)
        assert result == "Hello"

    def test_extract_agent_input_fallback(self, callback: GalileoADKCallback, adk_callback_context: MagicMock) -> None:
        del adk_callback_context.parent_context

        result = callback._observer._extract_agent_input(adk_callback_context)
        assert result == "Agent invocation"

    def test_extract_llm_input(self, callback: GalileoADKCallback, adk_llm_request: MagicMock) -> None:
        result = callback._observer._extract_llm_input(adk_llm_request)
        assert isinstance(result, list)

    def test_extract_model_name(self, callback: GalileoADKCallback, adk_llm_request: MagicMock) -> None:
        result = callback._observer._extract_model_name(adk_llm_request)
        assert result == "gemini-pro"

    def test_extract_temperature(self, callback: GalileoADKCallback, adk_llm_request: MagicMock) -> None:
        adk_llm_request.config.temperature = 0.7

        result = callback._observer._extract_temperature(adk_llm_request)
        assert result == 0.7

    def test_extract_temperature_none(self, callback: GalileoADKCallback, adk_llm_request: MagicMock) -> None:
        adk_llm_request.config.temperature = None

        result = callback._observer._extract_temperature(adk_llm_request)
        assert result is None

    def test_extract_usage_metadata(self, callback: GalileoADKCallback, adk_llm_response: MagicMock) -> None:
        adk_llm_response.usage_metadata.prompt_token_count = 10
        adk_llm_response.usage_metadata.candidates_token_count = 20
        adk_llm_response.usage_metadata.total_token_count = 30

        result = callback._observer._extract_usage_metadata(adk_llm_response)

        assert result["prompt_tokens"] == 10
        assert result["completion_tokens"] == 20
        assert result["total_tokens"] == 30


class TestCallbackErrorHandling:
    """Consolidated error handling tests for GalileoADKCallback."""

    @pytest.fixture
    def callback(self) -> GalileoADKCallback:
        return GalileoADKCallback(ingestion_hook=lambda r: None)

    def test_callback_handles_all_exception_types_gracefully(
        self,
        callback: GalileoADKCallback,
    ) -> None:
        """Callbacks handle exceptions without propagating errors."""
        # Given: a context that raises when accessing properties
        broken_context = MagicMock()
        broken_context.agent_name = property(lambda self: 1 / 0)

        # When/Then: before_agent_callback handles error gracefully
        result = callback.before_agent_callback(broken_context)
        assert result is None

        # When/Then: after_agent_callback with no run_id handles gracefully
        normal_context = MockCallbackContext()
        result = callback.after_agent_callback(normal_context)
        assert result is None

        # When/Then: after_model_callback without matching before_model handles gracefully
        response = MockLlmResponse()
        result = callback.after_model_callback(normal_context, response)
        assert result is None

        # When/Then: tool callbacks without parent agent handle gracefully
        tool = MagicMock()
        tool.name = "test_tool"
        tool_context = MockToolContext(callback_context=MockCallbackContext())
        result = callback.before_tool_callback(tool, {"arg": "value"}, tool_context)
        assert result is None

        result = callback.after_tool_callback(tool, {"arg": "value"}, tool_context, {"result": "ok"})
        assert result is None

    def test_all_callbacks_return_none_consistently(
        self,
        callback: GalileoADKCallback,
    ) -> None:
        """All callback methods return None."""
        context = MockCallbackContext()
        request = MockLlmRequest()
        response = MockLlmResponse(request_id=request.request_id)
        tool = MagicMock()
        tool.name = "test_tool"
        tool_context = MockToolContext(callback_context=context)

        # Test agent callbacks
        assert callback.before_agent_callback(context) is None
        assert callback.after_agent_callback(context) is None

        # Test model callbacks
        callback.before_agent_callback(context)  # Need parent span
        assert callback.before_model_callback(context, request) is None
        assert callback.after_model_callback(context, response) is None
        callback.after_agent_callback(context)

        # Test tool callbacks
        callback.before_agent_callback(context)
        assert callback.before_tool_callback(tool, {"arg": "value"}, tool_context) is None
        assert callback.after_tool_callback(tool, {"arg": "value"}, tool_context, {"result": "ok"}) is None


class TestCallbackPluginCompatibility:
    """Tests for multi-plugin compatibility."""

    @pytest.fixture
    def callback(self) -> GalileoADKCallback:
        return GalileoADKCallback(ingestion_hook=lambda r: None)

    def test_callback_handles_data_modification_gracefully(
        self,
        callback: GalileoADKCallback,
    ) -> None:
        """Callback handles external data modification between before/after calls."""
        context = MockCallbackContext()
        request = MockLlmRequest(contents=[MockContent(parts=[MockPart(text="sensitive data")])])

        callback.before_agent_callback(context)
        callback.before_model_callback(context, request)

        # External plugin modifies data
        request.contents[0].parts[0].text = "[REDACTED]"

        response = MockLlmResponse(request_id=request.request_id)
        result = callback.after_model_callback(context, response)
        assert result is None
        assert callback._tracker.llm_count == 0

    def test_namespaced_attributes(self, callback: GalileoADKCallback) -> None:
        """Callback tracks spans internally without polluting context."""
        context = MockCallbackContext()
        request = MockLlmRequest()

        callback.before_agent_callback(context)
        callback.before_model_callback(context, request)

        # Spans tracked internally
        assert callback._tracker.llm_count == 1
        assert callback._tracker.agent_count == 1

        # Other plugin attributes on context should not be affected
        context._other_plugin_data = "test"  # type: ignore[attr-defined]
        assert context._other_plugin_data == "test"  # type: ignore[attr-defined]

    def test_read_only_operations(self, callback: GalileoADKCallback) -> None:
        """Callback doesn't modify the original request data."""
        context = MockCallbackContext()
        original_text = "original message"
        request = MockLlmRequest(contents=[MockContent(parts=[MockPart(text=original_text)])])

        callback.before_model_callback(context, request)

        # Original data should be unchanged
        assert request.contents[0].parts[0].text == original_text

    def test_compatibility_with_other_plugin_attributes(
        self,
        callback: GalileoADKCallback,
    ) -> None:
        """Callback is compatible with other plugins setting attributes on context."""
        context = MockCallbackContext()
        request = MockLlmRequest()

        # Other plugins set custom attributes
        context._redaction_processed = True  # type: ignore[attr-defined]
        context._cache_key = "abc123"  # type: ignore[attr-defined]
        context._validation_passed = True  # type: ignore[attr-defined]

        callback.before_agent_callback(context)
        callback.before_model_callback(context, request)

        # Other plugin attributes preserved
        assert context._redaction_processed is True  # type: ignore[attr-defined]
        assert context._cache_key == "abc123"  # type: ignore[attr-defined]
        assert context._validation_passed is True  # type: ignore[attr-defined]
        # Internal tracking unaffected
        assert callback._tracker.llm_count == 1

        response = MockLlmResponse(request_id=request.request_id)
        callback.after_model_callback(context, response)

        # Still preserved after after callback
        assert context._redaction_processed is True  # type: ignore[attr-defined]
        assert context._cache_key == "abc123"  # type: ignore[attr-defined]
        assert context._validation_passed is True  # type: ignore[attr-defined]

    def test_complex_agent_interaction_sequence(
        self,
        callback: GalileoADKCallback,
    ) -> None:
        """Multiple LLM and tool calls within a single agent lifecycle."""
        context = MockCallbackContext()
        tool = MagicMock()
        tool.name = "test_tool"
        tool_context = MockToolContext(callback_context=context)

        callback.before_agent_callback(context)

        # First LLM call
        request1 = MockLlmRequest()
        callback.before_model_callback(context, request1)
        assert callback._tracker.llm_count == 1

        # Use matching request_id for correlation
        response1 = MockLlmResponse(request_id=request1.request_id)
        callback.after_model_callback(context, response1)
        assert callback._tracker.llm_count == 0

        # Tool call between LLM calls
        tool_args = {"action": "search"}
        callback.before_tool_callback(tool, tool_args, tool_context)
        callback.after_tool_callback(tool, tool_args, tool_context, {"result": "found"})

        # Second LLM call
        request2 = MockLlmRequest()
        callback.before_model_callback(context, request2)
        assert callback._tracker.llm_count == 1

        # Use matching request_id for correlation
        response2 = MockLlmResponse(request_id=request2.request_id)
        callback.after_model_callback(context, response2)
        assert callback._tracker.llm_count == 0

        callback.after_agent_callback(context)

        # All spans should be closed
        assert len(callback._handler._nodes) == 0

    def test_llm_correlation_without_request_id(
        self,
        callback: GalileoADKCallback,
    ) -> None:
        """LLM spans correlate without request_id."""
        context = MockCallbackContext()

        callback.before_agent_callback(context)

        # Create request WITHOUT request_id
        request = MockLlmRequest(request_id=None)
        # Clear the auto-generated request_id
        request.request_id = None

        callback.before_model_callback(context, request)
        assert callback._tracker.llm_count == 1

        # Create response WITHOUT request_id (simulates ADK not passing correlation)
        response = MockLlmResponse(request_id=None)

        # This should still work via tracker correlation
        callback.after_model_callback(context, response)
        assert callback._tracker.llm_count == 0

        callback.after_agent_callback(context)


class TestAutomaticSessionMapping:
    """Tests for automatic ADK session_id → Galileo session mapping."""

    @pytest.fixture
    def callback(self) -> GalileoADKCallback:
        return GalileoADKCallback(ingestion_hook=lambda r: None)

    def test_session_mapped_on_before_agent(self, callback: GalileoADKCallback) -> None:
        """ADK session_id is mapped to Galileo session on before_agent_callback."""
        # Given: a callback context with a session_id
        context = MockCallbackContext(session_id="adk-callback-session-123")

        # When: calling before_agent_callback
        callback.before_agent_callback(context)

        # Then: the ADK session is tracked by the observer
        assert callback._observer._current_adk_session == "adk-callback-session-123"

    def test_session_not_remapped_for_same_session_id(self, callback: GalileoADKCallback) -> None:
        """Same session_id doesn't trigger repeated session mapping."""
        # Given: a persistent session
        session_id = "persistent-callback-session"

        context_1 = MockCallbackContext(agent_name="agent_1", session_id=session_id)
        context_2 = MockCallbackContext(agent_name="agent_2", session_id=session_id)

        # When: calling before_agent_callback twice
        callback.before_agent_callback(context_1)
        first_mapped_session = callback._observer._current_adk_session

        callback.after_agent_callback(context_1)
        callback.before_agent_callback(context_2)
        second_mapped_session = callback._observer._current_adk_session

        # Then: session remains the same (not remapped)
        assert first_mapped_session == second_mapped_session == session_id

    def test_unknown_session_id_not_mapped(self, callback: GalileoADKCallback) -> None:
        """Session_id of 'unknown' is not mapped to Galileo session."""
        # Given: a callback context with unknown session_id
        context = MockCallbackContext(session_id="unknown")

        # When: calling before_agent_callback
        callback.before_agent_callback(context)

        # Then: session is not tracked (remains None)
        assert callback._observer._current_adk_session is None

    def test_session_updated_when_different_session_id(self, callback: GalileoADKCallback) -> None:
        """Different session_id triggers session update."""
        # Given: first agent with session-1
        context_1 = MockCallbackContext(agent_name="agent_1", session_id="session-1")
        callback.before_agent_callback(context_1)
        assert callback._observer._current_adk_session == "session-1"
        callback.after_agent_callback(context_1)

        # When: second agent with different session-2
        context_2 = MockCallbackContext(agent_name="agent_2", session_id="session-2")
        callback.before_agent_callback(context_2)

        # Then: session is updated to the new session
        assert callback._observer._current_adk_session == "session-2"


class TestRunConfigMetadata:
    """Tests for per-invocation metadata from RunConfig.custom_metadata."""

    @pytest.fixture
    def callback(self) -> GalileoADKCallback:
        return GalileoADKCallback(ingestion_hook=lambda r: None)

    def test_metadata_extracted_from_run_config(self, callback: GalileoADKCallback) -> None:
        """Metadata is extracted from RunConfig.custom_metadata in before_agent_callback."""
        # Given: a context with RunConfig containing custom_metadata
        run_config = MockRunConfig(custom_metadata={"turn": 1, "user_id": "test-user"})
        context = MockCallbackContext(run_config=run_config)

        # When: calling before_agent_callback
        callback.before_agent_callback(context)

        # Then: metadata is stored for the invocation (in observer)
        assert len(callback._observer._invocation_metadata) > 0

    def test_missing_run_config_results_in_empty_metadata(self, callback: GalileoADKCallback) -> None:
        """Missing RunConfig results in empty metadata (no error)."""
        # Given: a context without RunConfig
        context = MockCallbackContext(run_config=None)

        # When: calling before_agent_callback
        callback.before_agent_callback(context)

        # Then: no crash and agent is tracked
        assert callback._tracker.agent_count == 1

    def test_metadata_cleaned_up_after_agent_ends(self, callback: GalileoADKCallback) -> None:
        """Per-invocation metadata is cleaned up when agent ends."""
        # Given: a context with RunConfig containing custom_metadata
        run_config = MockRunConfig(custom_metadata={"turn": 1})
        context = MockCallbackContext(run_config=run_config)

        # When: running agent lifecycle
        callback.before_agent_callback(context)

        # Then: metadata is stored
        invocation_id = context.invocation_id
        assert invocation_id in callback._observer._invocation_metadata

        # When: agent ends
        callback.after_agent_callback(context)

        # Then: metadata is cleaned up
        assert invocation_id not in callback._observer._invocation_metadata

    def test_concurrent_agents_have_isolated_metadata(self, callback: GalileoADKCallback) -> None:
        """Concurrent agents with different RunConfig have isolated metadata."""
        # Given: two contexts with different custom_metadata
        run_config_1 = MockRunConfig(custom_metadata={"turn": 1, "user": "alice"})
        run_config_2 = MockRunConfig(custom_metadata={"turn": 2, "user": "bob"})

        context_1 = MockCallbackContext(agent_name="agent_1", invocation_id="inv_1", run_config=run_config_1)
        context_2 = MockCallbackContext(agent_name="agent_2", invocation_id="inv_2", run_config=run_config_2)

        # When: starting both agents
        callback.before_agent_callback(context_1)
        callback.before_agent_callback(context_2)

        # Then: each invocation has its own metadata (in observer)
        assert callback._observer._invocation_metadata.get("inv_1") == {"turn": 1, "user": "alice"}
        assert callback._observer._invocation_metadata.get("inv_2") == {"turn": 2, "user": "bob"}

        # Cleanup
        callback.after_agent_callback(context_1)
        callback.after_agent_callback(context_2)

        # Then: metadata is cleaned up
        assert "inv_1" not in callback._observer._invocation_metadata
        assert "inv_2" not in callback._observer._invocation_metadata
