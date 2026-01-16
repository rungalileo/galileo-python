from typing import Any
from unittest.mock import MagicMock

import pytest

from galileo_adk import GalileoADKCallback


class MockCallbackContext:
    def __init__(
        self, agent_name: str = "test_agent", session_id: str = "test_session", user_id: str = "test_user"
    ) -> None:
        self.agent_name = agent_name
        self.session_id = session_id
        self.user_id = user_id
        self.parent_context = MagicMock()
        self.parent_context.new_message = MagicMock()


class MockLlmRequest:
    def __init__(self, contents: list | None = None, config: Any | None = None, model: str = "gemini-pro") -> None:
        self.contents = contents or []
        self.config = config or MagicMock(spec_set=[])
        self.model = model


class MockLlmResponse:
    def __init__(
        self, content: Any | None = None, usage_metadata: Any | None = None, model_version: str = "gemini-pro-response"
    ) -> None:
        self.content = content
        self.usage_metadata = usage_metadata
        self.model_version = model_version


class MockContent:
    def __init__(self, parts: list | None = None, role: str = "user") -> None:
        self.parts = parts or []
        self.role = role


class MockPart:
    def __init__(self, text: str | None = None) -> None:
        self.text = text


class MockToolContext:
    def __init__(self, callback_context: MockCallbackContext | None = None) -> None:
        self.callback_context = callback_context


class TestMultiPluginCompatibility:
    @pytest.fixture
    def galileo_callback(self, mock_galileo_logger: MagicMock) -> GalileoADKCallback:
        return GalileoADKCallback(galileo_logger=mock_galileo_logger)

    def test_callback_returns_none_agent(self, galileo_callback: GalileoADKCallback) -> None:
        context = MockCallbackContext()

        result = galileo_callback.before_agent_callback(context)
        assert result is None

        result = galileo_callback.after_agent_callback(context)
        assert result is None

    def test_callback_returns_none_model(self, galileo_callback: GalileoADKCallback) -> None:
        context = MockCallbackContext()
        request = MockLlmRequest()
        response = MockLlmResponse()

        result = galileo_callback.before_model_callback(context, request)
        assert result is None

        result = galileo_callback.after_model_callback(context, response)
        assert result is None

    def test_callback_returns_none_tool(self, galileo_callback: GalileoADKCallback) -> None:
        context = MockCallbackContext()
        tool = MagicMock()
        tool.name = "test_tool"
        tool_args = {"arg": "value"}
        tool_context = MockToolContext(callback_context=context)
        result_data = {"output": "result"}

        galileo_callback.before_agent_callback(context)

        result = galileo_callback.before_tool_callback(tool, tool_args, tool_context)
        assert result is None

        result = galileo_callback.after_tool_callback(tool, tool_args, tool_context, result_data)
        assert result is None

    def test_callback_handles_data_modification_gracefully(self, galileo_callback: GalileoADKCallback) -> None:
        context = MockCallbackContext()
        request = MockLlmRequest(contents=[MockContent(parts=[MockPart(text="sensitive data")])])

        galileo_callback.before_model_callback(context, request)

        request.contents[0].parts[0].text = "[REDACTED]"

        response = MockLlmResponse()
        result = galileo_callback.after_model_callback(context, response)
        assert result is None
        assert hasattr(context, "_galileo_llm_run_id")

    def test_namespaced_attributes(self, galileo_callback: GalileoADKCallback) -> None:
        context = MockCallbackContext()
        request = MockLlmRequest()

        galileo_callback.before_model_callback(context, request)

        assert hasattr(context, "_galileo_llm_run_id")
        assert context._galileo_llm_run_id is not None

        context._other_plugin_data = "test"
        assert context._other_plugin_data == "test"
        assert context._galileo_llm_run_id is not None

    def test_read_only_operations(self, galileo_callback: GalileoADKCallback) -> None:
        context = MockCallbackContext()

        original_text = "original message"
        request = MockLlmRequest(contents=[MockContent(parts=[MockPart(text=original_text)])])

        galileo_callback.before_model_callback(context, request)

        assert request.contents[0].parts[0].text == original_text

    def test_missing_context_handling(self, galileo_callback: GalileoADKCallback) -> None:
        context = MockCallbackContext()
        response = MockLlmResponse()

        result = galileo_callback.after_model_callback(context, response)

        assert result is None

    def test_tool_without_parent_agent(self, galileo_callback: GalileoADKCallback) -> None:
        tool = MagicMock()
        tool.name = "test_tool"
        tool_args = {"arg": "value"}
        tool_context = MockToolContext()

        result = galileo_callback.before_tool_callback(tool, tool_args, tool_context)
        assert result is None

        result = galileo_callback.after_tool_callback(tool, tool_args, tool_context, {"result": "ok"})
        assert result is None

    def test_multiple_llm_calls_in_sequence(self, galileo_callback: GalileoADKCallback) -> None:
        context = MockCallbackContext()

        galileo_callback.before_agent_callback(context)

        request1 = MockLlmRequest()
        galileo_callback.before_model_callback(context, request1)
        llm_run_id_1 = context._galileo_llm_run_id

        response1 = MockLlmResponse()
        galileo_callback.after_model_callback(context, response1)

        request2 = MockLlmRequest()
        galileo_callback.before_model_callback(context, request2)
        llm_run_id_2 = context._galileo_llm_run_id

        response2 = MockLlmResponse()
        galileo_callback.after_model_callback(context, response2)

        assert llm_run_id_1 != llm_run_id_2

        galileo_callback.after_agent_callback(context)

        assert len(galileo_callback._handler._nodes) == 0

    def test_tool_call_between_llm_calls(self, galileo_callback: GalileoADKCallback) -> None:
        context = MockCallbackContext()
        tool = MagicMock()
        tool.name = "test_tool"
        tool_context = MockToolContext(callback_context=context)

        galileo_callback.before_agent_callback(context)

        request1 = MockLlmRequest()
        galileo_callback.before_model_callback(context, request1)
        response1 = MockLlmResponse()
        galileo_callback.after_model_callback(context, response1)

        tool_args = {"action": "search"}
        galileo_callback.before_tool_callback(tool, tool_args, tool_context)
        galileo_callback.after_tool_callback(tool, tool_args, tool_context, {"result": "found"})

        request2 = MockLlmRequest()
        galileo_callback.before_model_callback(context, request2)
        response2 = MockLlmResponse()
        galileo_callback.after_model_callback(context, response2)

        galileo_callback.after_agent_callback(context)

        assert len(galileo_callback._handler._nodes) == 0

    def test_error_in_callback_does_not_propagate(self, galileo_callback: GalileoADKCallback) -> None:
        context = MagicMock()
        context.agent_name = property(lambda self: 1 / 0)

        result = galileo_callback.before_agent_callback(context)
        assert result is None

    def test_compatibility_with_other_plugin_attributes(self, galileo_callback: GalileoADKCallback) -> None:
        context = MockCallbackContext()
        request = MockLlmRequest()

        context._redaction_processed = True
        context._cache_key = "abc123"
        context._validation_passed = True

        galileo_callback.before_model_callback(context, request)

        assert context._redaction_processed is True
        assert context._cache_key == "abc123"
        assert context._validation_passed is True
        assert hasattr(context, "_galileo_llm_run_id")

        response = MockLlmResponse()
        galileo_callback.after_model_callback(context, response)

        assert context._redaction_processed is True
        assert context._cache_key == "abc123"
        assert context._validation_passed is True
