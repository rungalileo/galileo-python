from unittest.mock import MagicMock, patch

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

            callback = GalileoADKCallback()

            assert callback._handler._start_new_trace is True
            assert callback._handler._flush_on_chain_end is True
            assert callback._handler._integration == "google_adk"

    def test_before_agent_callback(self, callback: GalileoADKCallback, adk_callback_context: MagicMock) -> None:
        result = callback.before_agent_callback(adk_callback_context)

        assert result is None
        assert hasattr(adk_callback_context, "_galileo_run_id")
        assert adk_callback_context._galileo_run_id is not None
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
        assert hasattr(adk_callback_context, "_galileo_llm_run_id")
        assert adk_callback_context._galileo_llm_run_id is not None
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

        result = callback.after_model_callback(adk_callback_context, adk_llm_response, model_response_event=None)

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
        assert hasattr(adk_tool_context, "_galileo_tool_run_id")
        assert adk_tool_context._galileo_tool_run_id is not None
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
