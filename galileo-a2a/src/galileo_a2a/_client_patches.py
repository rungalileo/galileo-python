"""Client-side monkey-patches for a2a-sdk instrumentation."""

from __future__ import annotations

import functools
import json
import logging
from typing import Any

from a2a.client.base_client import BaseClient
from opentelemetry import trace
from opentelemetry.trace import StatusCode, Tracer

from galileo_a2a._constants import (
    A2A_CONTEXT_ID,
    A2A_RPC_METHOD,
    A2A_TASK_ID,
    GALILEO_OBSERVE_KEY,
    GENAI_AGENT_NAME,
    GENAI_INPUT_MESSAGES,
    GENAI_OPERATION_NAME,
    GENAI_OUTPUT_MESSAGES,
    GENAI_SYSTEM,
    GENAI_TOOL_NAME,
    ROLE_ASSISTANT,
    ROLE_USER,
    SESSION_ID,
)
from galileo_a2a._context import inject_trace_context
from galileo_a2a._message_utils import extract_text_from_parts, set_output_on_span, track_task_state

_logger = logging.getLogger(__name__)

# Stashed original methods for uninstrumentation
_originals: dict[str, Any] = {}


def _patch_client(tracer: Tracer, agent_name: str | None = None) -> None:
    """Patch ``BaseClient`` methods to create OTel spans for outbound A2A calls.

    Idempotent — safe to call multiple times. Rolls back partial patches on
    failure to avoid leaving the class in an inconsistent state.
    """
    if _originals:
        _logger.warning("a2a-sdk client already patched, skipping")
        return

    patched_keys: list[str] = []
    try:
        _originals["BaseClient.send_message"] = BaseClient.send_message
        patched_keys.append("BaseClient.send_message")
        BaseClient.send_message = _wrap_send_message(tracer, _originals["BaseClient.send_message"], agent_name)

        _originals["BaseClient.get_task"] = BaseClient.get_task
        patched_keys.append("BaseClient.get_task")
        BaseClient.get_task = _wrap_simple_method(tracer, _originals["BaseClient.get_task"], "GetTask", "execute_tool")

        _originals["BaseClient.cancel_task"] = BaseClient.cancel_task
        patched_keys.append("BaseClient.cancel_task")
        BaseClient.cancel_task = _wrap_simple_method(
            tracer, _originals["BaseClient.cancel_task"], "CancelTask", "execute_tool"
        )

        _originals["BaseClient.get_card"] = BaseClient.get_card
        patched_keys.append("BaseClient.get_card")
        BaseClient.get_card = _wrap_simple_method(tracer, _originals["BaseClient.get_card"], "GetCard", "execute_tool")
    except Exception:
        _logger.error(
            "Failed to patch a2a-sdk client — rolling back. The installed a2a-sdk version may be incompatible.",
            exc_info=True,
        )
        # Roll back any partial patches
        for key in patched_keys:
            if key in _originals:
                setattr(BaseClient, key.split(".")[1], _originals.pop(key))
        return

    _logger.debug("Patched a2a-sdk client methods")


def _unpatch_client() -> None:
    """Restore original a2a-sdk client methods."""
    if "BaseClient.send_message" in _originals:
        BaseClient.send_message = _originals.pop("BaseClient.send_message")
    if "BaseClient.get_task" in _originals:
        BaseClient.get_task = _originals.pop("BaseClient.get_task")
    if "BaseClient.cancel_task" in _originals:
        BaseClient.cancel_task = _originals.pop("BaseClient.cancel_task")
    if "BaseClient.get_card" in _originals:
        BaseClient.get_card = _originals.pop("BaseClient.get_card")

    _logger.debug("Unpatched a2a-sdk client methods")


def _wrap_send_message(tracer: Tracer, original: Any, agent_name: str | None = None) -> Any:
    """Create an instrumented wrapper for BaseClient.send_message."""

    @functools.wraps(original)
    async def wrapper(
        self: Any,
        request: Any,
        *,
        configuration: Any = None,
        context: Any = None,
        request_metadata: dict[str, Any] | None = None,
        extensions: list[str] | None = None,
    ) -> Any:
        span_name = "a2a.client.send_message"
        with tracer.start_as_current_span(span_name) as span:
            _set_client_span_attributes(span, request, "SendMessage", agent_name)
            _set_input_from_message(span, request)

            # Inject trace context into request_metadata for cross-agent correlation
            observe_ctx = inject_trace_context(agent_name=agent_name)
            request_metadata = dict(request_metadata) if request_metadata else {}
            request_metadata[GALILEO_OBSERVE_KEY] = observe_ctx

            try:
                result = original(
                    self,
                    request,
                    configuration=configuration,
                    context=context,
                    request_metadata=request_metadata,
                    extensions=extensions,
                )
                async for event in result:
                    _track_event_state(span, event)
                    yield event
            except Exception as exc:
                span.record_exception(exc)
                span.set_status(StatusCode.ERROR, str(exc))
                raise

    return wrapper


def _wrap_simple_method(tracer: Tracer, original: Any, rpc_method: str, operation: str) -> Any:
    """Create an instrumented wrapper for a non-streaming client method."""

    @functools.wraps(original)
    async def wrapper(self: Any, *args: Any, **kwargs: Any) -> Any:
        span_name = f"a2a.client.{rpc_method.lower()}"
        with tracer.start_as_current_span(span_name) as span:
            span.set_attribute(GENAI_OPERATION_NAME, operation)
            span.set_attribute(GENAI_SYSTEM, "a2a")
            span.set_attribute(A2A_RPC_METHOD, rpc_method)

            if operation == "execute_tool":
                span.set_attribute(GENAI_TOOL_NAME, rpc_method)

            if args:
                try:
                    span.set_attribute(
                        GENAI_INPUT_MESSAGES,
                        json.dumps([{"role": ROLE_USER, "content": str(args[0])}]),
                    )
                except Exception:
                    _logger.debug("Failed to capture input for %s", rpc_method, exc_info=True)

            try:
                result = await original(self, *args, **kwargs)
                _track_event_state(span, result)

                if result is not None:
                    try:
                        if hasattr(result, "model_dump"):
                            output_str = json.dumps(result.model_dump(exclude_none=True), default=str)
                        else:
                            output_str = str(result)
                        span.set_attribute(
                            GENAI_OUTPUT_MESSAGES,
                            json.dumps([{"role": ROLE_ASSISTANT, "content": output_str}]),
                        )
                    except Exception:
                        _logger.debug("Failed to capture output for %s", rpc_method, exc_info=True)

                return result
            except Exception as exc:
                span.record_exception(exc)
                span.set_status(StatusCode.ERROR, str(exc))
                raise

    return wrapper


def _set_client_span_attributes(span: trace.Span, request: Any, rpc_method: str, agent_name: str | None) -> None:
    """Set A2A and GenAI attributes on a client span."""
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


def _set_input_from_message(span: trace.Span, message: Any) -> None:
    """Extract input content from an A2A Message and set gen_ai.input.messages."""
    text = extract_text_from_parts(message)
    if text:
        span.set_attribute(GENAI_INPUT_MESSAGES, json.dumps([{"role": ROLE_USER, "content": text}]))


def _track_event_state(span: trace.Span, event: Any) -> None:
    """Record task state and output content from an A2A response event on *span*.

    Handles both plain objects and ``(task, update)`` tuples emitted by
    streaming ``send_message``.
    """
    if event is None:
        return

    # Streaming send_message yields (task, update) tuples — unpack them.
    if isinstance(event, tuple | list):
        primary = event[0] if len(event) > 0 else None
        secondary = event[1] if len(event) > 1 else None
    else:
        primary = event
        secondary = None

    if primary is not None:
        set_output_on_span(span, primary)
        track_task_state(span, primary)
    if secondary is not None:
        set_output_on_span(span, secondary)
