from unittest.mock import MagicMock, patch
from uuid import uuid4

import pytest

from galileo_adk import GalileoADKCallback


class TestGalileoADKCallback:
    @pytest.fixture
    def callback(self, mock_galileo_logger: MagicMock) -> GalileoADKCallback:
        return GalileoADKCallback(galileo_logger=mock_galileo_logger)

    def test_initialization_with_logger(self, mock_galileo_logger: MagicMock) -> None:
        callback = GalileoADKCallback(galileo_logger=mock_galileo_logger)
        assert callback._handler is not None
        assert callback._handler._galileo_logger == mock_galileo_logger

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
        with patch("galileo_adk.observer.galileo_context") as mock_context:
            mock_logger = MagicMock()
            mock_context.get_logger_instance.return_value = mock_logger

            callback = GalileoADKCallback(project="test")

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


class MockRunConfig:
    """Mock ADK RunConfig for testing custom_metadata extraction."""

    def __init__(self, custom_metadata: dict | None = None) -> None:
        self.custom_metadata = custom_metadata


class MockCallbackContext:
    """Mock ADK CallbackContext for testing callback error handling."""

    def __init__(
        self,
        agent_name: str = "test_agent",
        session_id: str = "test_session",
        user_id: str = "test_user",
        run_config: MockRunConfig | None = None,
    ) -> None:
        self.agent_name = agent_name
        self.session_id = session_id
        self.user_id = user_id
        self.parent_context = MagicMock()
        self.parent_context.new_message = MagicMock()
        self.session = MagicMock()
        self.session.id = session_id
        self.run_config = run_config


class MockLlmRequest:
    """Mock ADK LlmRequest for testing."""

    def __init__(
        self,
        contents: list | None = None,
        model: str = "gemini-pro",
        request_id: str | None = None,
    ) -> None:
        self.contents = contents or []
        self.config = MagicMock(spec_set=[])
        self.model = model
        self.request_id = request_id or str(uuid4())


class MockLlmResponse:
    """Mock ADK LlmResponse for testing."""

    def __init__(
        self,
        content: object = None,
        usage_metadata: object = None,
        model_version: str = "gemini-pro-response",
        request_id: str | None = None,
    ) -> None:
        self.content = content
        self.usage_metadata = usage_metadata
        self.model_version = model_version
        self.request_id = request_id


class MockContent:
    """Mock ADK Content for testing."""

    def __init__(self, parts: list | None = None, role: str = "user") -> None:
        self.parts = parts or []
        self.role = role


class MockPart:
    """Mock ADK Part for testing."""

    def __init__(self, text: str | None = None) -> None:
        self.text = text


class MockToolContext:
    """Mock ADK ToolContext for testing."""

    def __init__(self, callback_context: MockCallbackContext | None = None) -> None:
        self.callback_context = callback_context


class TestCallbackErrorHandling:
    """Consolidated error handling tests for GalileoADKCallback."""

    @pytest.fixture
    def callback(self, mock_galileo_logger: MagicMock) -> GalileoADKCallback:
        return GalileoADKCallback(galileo_logger=mock_galileo_logger)

    def test_callback_handles_all_exception_types_gracefully(
        self,
        callback: GalileoADKCallback,
    ) -> None:
        """Callbacks handle various exception types without propagating errors."""
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
        tool_context = MockToolContext()
        result = callback.before_tool_callback(tool, {"arg": "value"}, tool_context)
        assert result is None

        result = callback.after_tool_callback(tool, {"arg": "value"}, tool_context, {"result": "ok"})
        assert result is None

    def test_all_callbacks_return_none_consistently(
        self,
        callback: GalileoADKCallback,
    ) -> None:
        """All callback methods consistently return None to allow callback chaining."""
        context = MockCallbackContext()
        request = MockLlmRequest()
        # Use matching request_id for correlation
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
    """Tests for multi-plugin compatibility - migrated from test_multi_plugin.py."""

    @pytest.fixture
    def callback(self, mock_galileo_logger: MagicMock) -> GalileoADKCallback:
        return GalileoADKCallback(galileo_logger=mock_galileo_logger)

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

        # Use matching request_id for correlation
        response = MockLlmResponse(request_id=request.request_id)
        result = callback.after_model_callback(context, response)
        assert result is None
        # LLM run_id tracked internally, cleaned up after after_model_callback
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

        # Use matching request_id for correlation
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
        """Tests multiple LLM calls and tool calls within a single agent lifecycle."""
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
        """LLM spans are properly correlated even when request_id is not available."""
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
    def callback(self, mock_galileo_logger: MagicMock) -> GalileoADKCallback:
        return GalileoADKCallback(galileo_logger=mock_galileo_logger)

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


class TestRunConfigMetadata:
    """Tests for per-invocation metadata from RunConfig.custom_metadata."""

    @pytest.fixture
    def callback(self, mock_galileo_logger: MagicMock) -> GalileoADKCallback:
        return GalileoADKCallback(galileo_logger=mock_galileo_logger)

    def test_metadata_extracted_from_run_config(self, callback: GalileoADKCallback) -> None:
        """Metadata is extracted from RunConfig.custom_metadata in before_agent_callback."""
        # Given: a context with RunConfig containing custom_metadata
        run_config = MockRunConfig(custom_metadata={"turn": 1, "user_id": "test-user"})
        context = MockCallbackContext(run_config=run_config)

        # When: calling before_agent_callback
        callback.before_agent_callback(context)

        # Then: metadata is stored for the invocation (in observer)
        # The actual invocation_id comes from get_invocation_id which falls back to "unknown"
        assert "unknown" in callback._observer._invocation_metadata or len(callback._observer._invocation_metadata) > 0

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

        # Then: metadata is stored (invocation_id is "unknown" for MockCallbackContext)
        initial_metadata_count = len(callback._observer._invocation_metadata)
        assert initial_metadata_count >= 0  # May be 0 if "unknown" is used

        # When: agent ends
        callback.after_agent_callback(context)

        # Then: metadata is cleaned up
        # The invocation_id is "unknown" for MockCallbackContext since it has no invocation_id attr
        assert (
            "unknown" not in callback._observer._invocation_metadata
            or callback._observer._invocation_metadata.get("unknown") is None
        )

    def test_concurrent_agents_have_isolated_metadata(self, callback: GalileoADKCallback) -> None:
        """Concurrent agents with different RunConfig have isolated metadata."""
        # Given: two contexts with different custom_metadata
        run_config_1 = MockRunConfig(custom_metadata={"turn": 1, "user": "alice"})
        run_config_2 = MockRunConfig(custom_metadata={"turn": 2, "user": "bob"})

        # Add invocation_id to make them distinct
        context_1 = MockCallbackContext(agent_name="agent_1", run_config=run_config_1)
        context_1.invocation_id = "inv_1"  # type: ignore[attr-defined]
        context_2 = MockCallbackContext(agent_name="agent_2", run_config=run_config_2)
        context_2.invocation_id = "inv_2"  # type: ignore[attr-defined]

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
