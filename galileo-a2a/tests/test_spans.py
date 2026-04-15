"""Tests for span attribute operations."""

import json
from types import SimpleNamespace
from unittest.mock import MagicMock

import pytest
from opentelemetry.trace import Span, StatusCode

from galileo_a2a import _spans
from galileo_a2a._constants import (
    A2A_CONTEXT_ID,
    A2A_RPC_METHOD,
    A2A_TASK_ID,
    A2A_TASK_STATE,
    GENAI_AGENT_NAME,
    GENAI_INPUT_MESSAGES,
    GENAI_OPERATION_NAME,
    GENAI_OUTPUT_MESSAGES,
    GENAI_RESPONSE_FINISH_REASONS,
    GENAI_SYSTEM,
    GENAI_TOOL_NAME,
    SESSION_ID,
)


@pytest.fixture(autouse=True)
def _enable_content_capture():
    """Ensure content capture is enabled for each test."""
    _spans.configure(capture_content=True)
    yield
    _spans.configure(capture_content=True)


@pytest.fixture
def span():
    return MagicMock(spec=Span)


def _text_part(text: str) -> SimpleNamespace:
    return SimpleNamespace(root=SimpleNamespace(text=text))


def _message(text: str) -> SimpleNamespace:
    return SimpleNamespace(parts=[_text_part(text)])


class TestSetClientAttributes:
    def test_sets_standard_attributes(self, span):
        # Given: a request with context_id and task_id
        request = SimpleNamespace(context_id="ctx-1", task_id="task-1")

        # When: setting client attributes
        _spans.set_client_attributes(span, request, "SendMessage", "my-agent")

        # Then: all expected attributes are set
        span.set_attribute.assert_any_call(GENAI_OPERATION_NAME, "invoke_agent")
        span.set_attribute.assert_any_call(GENAI_SYSTEM, "a2a")
        span.set_attribute.assert_any_call(A2A_RPC_METHOD, "SendMessage")
        span.set_attribute.assert_any_call(GENAI_AGENT_NAME, "my-agent")
        span.set_attribute.assert_any_call(A2A_CONTEXT_ID, "ctx-1")
        span.set_attribute.assert_any_call(SESSION_ID, "ctx-1")
        span.set_attribute.assert_any_call(A2A_TASK_ID, "task-1")

    def test_skips_agent_name_when_none(self, span):
        # Given: no agent name
        request = SimpleNamespace()

        # When: setting client attributes
        _spans.set_client_attributes(span, request, "SendMessage", None)

        # Then: agent name not set
        set_keys = [call.args[0] for call in span.set_attribute.call_args_list]
        assert GENAI_AGENT_NAME not in set_keys


class TestSetServerAttributes:
    def test_sets_attributes_from_message(self, span):
        # Given: params with message containing context_id
        params = SimpleNamespace(message=SimpleNamespace(context_id="ctx-2", task_id="task-2"))

        # When: setting server attributes
        _spans.set_server_attributes(span, params, "SendMessage", "server-agent")

        # Then: attributes extracted from message
        span.set_attribute.assert_any_call(A2A_CONTEXT_ID, "ctx-2")
        span.set_attribute.assert_any_call(SESSION_ID, "ctx-2")
        span.set_attribute.assert_any_call(A2A_TASK_ID, "task-2")


class TestSetToolAttributes:
    def test_sets_tool_operation_and_name(self, span):
        # When: setting tool attributes
        _spans.set_tool_attributes(span, "GetCard")

        # Then: operation is execute_tool and tool name is set
        span.set_attribute.assert_any_call(GENAI_OPERATION_NAME, "execute_tool")
        span.set_attribute.assert_any_call(GENAI_TOOL_NAME, "GetCard")


class TestSetInput:
    def test_sets_input_messages_as_json(self, span):
        # Given: a message with text
        msg = _message("hello")

        # When: setting input
        _spans.set_input(span, msg)

        # Then: input messages set as JSON
        call_args = span.set_attribute.call_args
        assert call_args.args[0] == GENAI_INPUT_MESSAGES
        parsed = json.loads(call_args.args[1])
        assert parsed == [{"role": "user", "content": "hello"}]

    def test_skips_when_no_text(self, span):
        # Given: a message with no text parts
        msg = SimpleNamespace(parts=[])

        # When: setting input
        _spans.set_input(span, msg)

        # Then: no attribute set
        span.set_attribute.assert_not_called()

    def test_skips_when_capture_content_disabled(self, span):
        # Given: content capture is disabled
        _spans.configure(capture_content=False)
        msg = _message("secret data")

        # When: setting input
        _spans.set_input(span, msg)

        # Then: no attribute set
        span.set_attribute.assert_not_called()


class TestSetOutput:
    def test_sets_output_from_message(self, span):
        # Given: a direct message response
        event = _message("response text")

        # When: setting output
        _spans.set_output(span, event)

        # Then: output messages set
        call_args = span.set_attribute.call_args
        assert call_args.args[0] == GENAI_OUTPUT_MESSAGES
        parsed = json.loads(call_args.args[1])
        assert parsed == [{"role": "assistant", "content": "response text"}]

    def test_sets_output_from_task_status_message(self, span):
        # Given: a task with status.message containing text
        event = SimpleNamespace(
            parts=None,
            status=SimpleNamespace(message=_message("task result")),
        )

        # When: setting output
        _spans.set_output(span, event)

        # Then: output extracted from status.message
        parsed = json.loads(span.set_attribute.call_args.args[1])
        assert parsed[0]["content"] == "task result"

    def test_skips_when_capture_content_disabled(self, span):
        # Given: content capture disabled
        _spans.configure(capture_content=False)

        # When: setting output
        _spans.set_output(span, _message("secret"))

        # Then: no attribute set
        span.set_attribute.assert_not_called()


class TestTrackTaskState:
    def test_sets_completed_state(self, span):
        # Given: a task with completed status
        obj = SimpleNamespace(status=SimpleNamespace(state=SimpleNamespace(value="completed")), id="t-1")

        # When: tracking state
        _spans.track_task_state(span, obj)

        # Then: state and finish reason set
        span.set_attribute.assert_any_call(A2A_TASK_STATE, "completed")
        span.set_attribute.assert_any_call(GENAI_RESPONSE_FINISH_REASONS, json.dumps(["stop"]))
        span.set_attribute.assert_any_call(A2A_TASK_ID, "t-1")

    @pytest.mark.parametrize("state", ["failed", "rejected", "canceled"])
    def test_sets_error_status(self, span, state):
        # Given: a task with an error state
        obj = SimpleNamespace(status=SimpleNamespace(state=SimpleNamespace(value=state)), id=None)

        # When: tracking state
        _spans.track_task_state(span, obj)

        # Then: span marked as error
        span.set_status.assert_called_once_with(StatusCode.ERROR, f"A2A task {state}")

    def test_noop_for_none(self, span):
        # When: tracking None
        _spans.track_task_state(span, None)

        # Then: nothing set
        span.set_attribute.assert_not_called()


class TestTrackEventState:
    def test_unpacks_tuple_event(self, span):
        # Given: a (task, update) tuple where task has completed status
        task = SimpleNamespace(
            parts=None,
            status=SimpleNamespace(
                state=SimpleNamespace(value="completed"),
                message=_message("done"),
            ),
            id="t-1",
        )
        event = (task, None)

        # When: tracking event state
        _spans.track_event_state(span, event)

        # Then: state extracted from first element
        span.set_attribute.assert_any_call(A2A_TASK_STATE, "completed")

    def test_handles_plain_object(self, span):
        # Given: a plain task object (not a tuple)
        event = SimpleNamespace(
            parts=None,
            status=SimpleNamespace(state=SimpleNamespace(value="working")),
            id="t-2",
        )

        # When: tracking event state
        _spans.track_event_state(span, event)

        # Then: state extracted directly
        span.set_attribute.assert_any_call(A2A_TASK_STATE, "working")

    def test_noop_for_none(self, span):
        # When: tracking None event
        _spans.track_event_state(span, None)

        # Then: nothing set
        span.set_attribute.assert_not_called()


class TestExtractText:
    def test_returns_text_from_single_part(self):
        # Given: a message with one TextPart
        msg = SimpleNamespace(parts=[_text_part("hello")])

        # When/Then: text is returned
        assert _spans.extract_text(msg) == "hello"

    def test_joins_multiple_parts_with_newline(self):
        # Given: a message with two TextParts
        msg = SimpleNamespace(parts=[_text_part("line1"), _text_part("line2")])

        # When/Then: parts are joined
        assert _spans.extract_text(msg) == "line1\nline2"

    def test_skips_non_text_parts(self):
        # Given: a message with a FilePart and a TextPart
        file_part = SimpleNamespace(root=SimpleNamespace(uri="file://data.bin"))
        msg = SimpleNamespace(parts=[file_part, _text_part("hello")])

        # When/Then: only text part is returned
        assert _spans.extract_text(msg) == "hello"

    def test_returns_none_for_empty_parts(self):
        assert _spans.extract_text(SimpleNamespace(parts=[])) is None

    def test_returns_none_for_no_parts_attribute(self):
        assert _spans.extract_text(SimpleNamespace()) is None

    def test_returns_none_for_none_input(self):
        assert _spans.extract_text(None) is None

    def test_handles_part_without_root(self):
        # Given: a part that is not a RootModel (fallback to part itself)
        part = SimpleNamespace(text="direct")
        msg = SimpleNamespace(parts=[part])

        # When/Then: text is extracted from the part directly
        assert _spans.extract_text(msg) == "direct"

    def test_returns_none_when_all_parts_are_non_text(self):
        file_part = SimpleNamespace(root=SimpleNamespace(uri="file://data.bin"))
        msg = SimpleNamespace(parts=[file_part, file_part])

        assert _spans.extract_text(msg) is None
