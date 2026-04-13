"""Span attribute operations for A2A telemetry."""

from __future__ import annotations

import json
import logging
from typing import Any

from opentelemetry import trace
from opentelemetry.trace import StatusCode

from galileo_a2a._constants import (
    A2A_CONTEXT_ID,
    A2A_RPC_METHOD,
    A2A_TASK_ID,
    A2A_TASK_STATE,
    ERROR_STATES,
    FINISH_REASON_STOP,
    GENAI_AGENT_NAME,
    GENAI_INPUT_MESSAGES,
    GENAI_OPERATION_NAME,
    GENAI_OUTPUT_MESSAGES,
    GENAI_RESPONSE_FINISH_REASONS,
    GENAI_SYSTEM,
    GENAI_TOOL_NAME,
    ROLE_ASSISTANT,
    ROLE_USER,
    SESSION_ID,
)


def extract_text(obj: Any) -> str | None:
    """Return concatenated text from an A2A Message's parts.

    A2A ``Part`` is a Pydantic ``RootModel``; the inner ``TextPart`` lives at
    ``part.root``.  Non-text parts are skipped.  Returns ``None`` when no text
    content is found.
    """
    parts = getattr(obj, "parts", None)
    if not parts:
        return None

    texts = []
    for part in parts:
        inner = getattr(part, "root", part)
        text = getattr(inner, "text", None)
        if text:
            texts.append(str(text))
    return "\n".join(texts) if texts else None


_logger = logging.getLogger(__name__)

_capture_content: bool = True


def configure(*, capture_content: bool = True) -> None:
    """Set module-level configuration for span content capture."""
    global _capture_content  # noqa: PLW0603
    _capture_content = capture_content


def set_client_attributes(
    span: trace.Span,
    request: Any,
    rpc_method: str,
    agent_name: str | None,
) -> None:
    """Set standard A2A and GenAI attributes on a client span."""
    span.set_attribute(GENAI_OPERATION_NAME, "invoke_agent")
    span.set_attribute(GENAI_SYSTEM, "a2a")
    span.set_attribute(A2A_RPC_METHOD, rpc_method)

    if agent_name:
        span.set_attribute(GENAI_AGENT_NAME, agent_name)

    if hasattr(request, "context_id") and request.context_id:
        span.set_attribute(A2A_CONTEXT_ID, str(request.context_id))
        span.set_attribute(SESSION_ID, str(request.context_id))

    if hasattr(request, "task_id") and request.task_id:
        span.set_attribute(A2A_TASK_ID, str(request.task_id))


def set_server_attributes(
    span: trace.Span,
    params: Any,
    rpc_method: str,
    agent_name: str | None,
) -> None:
    """Set standard A2A and GenAI attributes on a server span."""
    span.set_attribute(GENAI_OPERATION_NAME, "invoke_agent")
    span.set_attribute(GENAI_SYSTEM, "a2a")
    span.set_attribute(A2A_RPC_METHOD, rpc_method)

    if agent_name:
        span.set_attribute(GENAI_AGENT_NAME, agent_name)

    message = getattr(params, "message", None)
    if message:
        context_id = getattr(message, "context_id", None)
        if context_id:
            span.set_attribute(A2A_CONTEXT_ID, str(context_id))
            span.set_attribute(SESSION_ID, str(context_id))

        task_id = getattr(message, "task_id", None)
        if task_id:
            span.set_attribute(A2A_TASK_ID, str(task_id))


def set_tool_attributes(span: trace.Span, rpc_method: str) -> None:
    """Set attributes for tool-like A2A operations (get_task, cancel_task, get_card)."""
    span.set_attribute(GENAI_OPERATION_NAME, "execute_tool")
    span.set_attribute(GENAI_SYSTEM, "a2a")
    span.set_attribute(A2A_RPC_METHOD, rpc_method)
    span.set_attribute(GENAI_TOOL_NAME, rpc_method)


def set_input(span: trace.Span, message: Any) -> None:
    """Set ``gen_ai.input.messages`` from an A2A Message's text parts."""
    if not _capture_content:
        return
    text = extract_text(message)
    if text:
        span.set_attribute(GENAI_INPUT_MESSAGES, json.dumps([{"role": ROLE_USER, "content": text}]))


def set_output(span: trace.Span, event: Any) -> None:
    """Set ``gen_ai.output.messages`` from an A2A response.

    Handles direct ``Message`` responses and ``Task`` responses whose output
    is carried in ``status.message``.
    """
    if not _capture_content:
        return
    try:
        text = extract_text(event)
        if text:
            span.set_attribute(GENAI_OUTPUT_MESSAGES, json.dumps([{"role": ROLE_ASSISTANT, "content": text}]))
            return

        status = getattr(event, "status", None)
        if status is not None:
            status_msg = getattr(status, "message", None)
            if status_msg is not None:
                text = extract_text(status_msg)
                if text:
                    span.set_attribute(
                        GENAI_OUTPUT_MESSAGES,
                        json.dumps([{"role": ROLE_ASSISTANT, "content": text}]),
                    )
    except Exception:
        _logger.debug("Failed to extract output from A2A event", exc_info=True)


def set_simple_output(span: trace.Span, result: Any, rpc_method: str) -> None:
    """Set ``gen_ai.output.messages`` for non-streaming methods (get_task, get_card)."""
    if not _capture_content or result is None:
        return
    try:
        if hasattr(result, "model_dump"):
            output_str = json.dumps(result.model_dump(exclude_none=True), default=str)
        else:
            output_str = str(result)
        span.set_attribute(GENAI_OUTPUT_MESSAGES, json.dumps([{"role": ROLE_ASSISTANT, "content": output_str}]))
    except Exception:
        _logger.debug("Failed to capture output for %s", rpc_method, exc_info=True)


def set_simple_input(span: trace.Span, args: tuple, rpc_method: str) -> None:
    """Set ``gen_ai.input.messages`` for non-streaming methods from positional args."""
    if not _capture_content or not args:
        return
    try:
        span.set_attribute(GENAI_INPUT_MESSAGES, json.dumps([{"role": ROLE_USER, "content": str(args[0])}]))
    except Exception:
        _logger.debug("Failed to capture input for %s", rpc_method, exc_info=True)


def track_task_state(span: trace.Span, obj: Any) -> None:
    """Record A2A task state and ID on *span*.

    Sets ``a2a.task.state``, ``a2a.task.id``, and ``gen_ai.response.finish_reasons``.
    Marks the span as an error when the task enters a terminal error state.
    """
    if obj is None:
        return

    status = getattr(obj, "status", None)
    if status is not None:
        state = getattr(status, "state", None)
        if state is not None:
            state_value = state.value if hasattr(state, "value") else str(state)
            span.set_attribute(A2A_TASK_STATE, state_value)

            if state_value in ERROR_STATES:
                span.set_status(StatusCode.ERROR, f"A2A task {state_value}")
                span.set_attribute(GENAI_RESPONSE_FINISH_REASONS, json.dumps([state_value]))
            elif state_value == "completed":
                span.set_attribute(GENAI_RESPONSE_FINISH_REASONS, json.dumps([FINISH_REASON_STOP]))

    task_id = getattr(obj, "id", None)
    if task_id:
        span.set_attribute(A2A_TASK_ID, str(task_id))


def track_event_state(span: trace.Span, event: Any) -> None:
    """Record task state and output from an A2A response event.

    Handles both plain objects and ``(task, update)`` tuples emitted by
    streaming ``send_message``.
    """
    if event is None:
        return

    if isinstance(event, tuple | list):
        primary = event[0] if len(event) > 0 else None
        secondary = event[1] if len(event) > 1 else None
    else:
        primary = event
        secondary = None

    if primary is not None:
        set_output(span, primary)
        track_task_state(span, primary)
    if secondary is not None:
        set_output(span, secondary)
