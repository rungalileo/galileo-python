"""Shared utilities for extracting content from A2A messages and tracking task state."""

from __future__ import annotations

import json
import logging
from typing import Any

from opentelemetry import trace
from opentelemetry.trace import StatusCode

from galileo_a2a._constants import (
    A2A_TASK_ID,
    A2A_TASK_STATE,
    ERROR_STATES,
    FINISH_REASON_STOP,
    GENAI_OUTPUT_MESSAGES,
    GENAI_RESPONSE_FINISH_REASONS,
    ROLE_ASSISTANT,
)

_logger = logging.getLogger(__name__)


def extract_text_from_parts(obj: Any) -> str | None:
    """Return concatenated text content from an A2A Message's parts.

    A2A ``Part`` objects are Pydantic ``RootModel`` wrappers — the actual
    ``TextPart`` is at ``part.root``, not ``part`` directly. Non-text parts
    (``FilePart``, ``DataPart``) are skipped.

    Returns ``None`` if no text content is found.
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


def set_output_on_span(span: trace.Span, event: Any) -> None:
    """Set ``gen_ai.output.messages`` on *span* from an A2A response event.

    Accepts two response shapes:

    * A ``Message`` with ``.parts`` containing text.
    * A ``Task`` whose ``status.message`` carries the response.
    """
    try:
        text = extract_text_from_parts(event)
        if text:
            span.set_attribute(GENAI_OUTPUT_MESSAGES, json.dumps([{"role": ROLE_ASSISTANT, "content": text}]))
            return

        status = getattr(event, "status", None)
        if status is not None:
            status_msg = getattr(status, "message", None)
            if status_msg is not None:
                text = extract_text_from_parts(status_msg)
                if text:
                    span.set_attribute(GENAI_OUTPUT_MESSAGES, json.dumps([{"role": ROLE_ASSISTANT, "content": text}]))
    except Exception:
        _logger.debug("Failed to extract output from A2A event", exc_info=True)


def track_task_state(span: trace.Span, obj: Any) -> None:
    """Extract ``status.state`` and ``id`` from an A2A response and set span attributes.

    Sets ``a2a.task.state``, ``a2a.task.id``, ``gen_ai.response.finish_reasons``,
    and marks the span as error when the task enters an error state.
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
