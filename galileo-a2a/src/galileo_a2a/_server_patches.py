"""Server-side monkey-patches for a2a-sdk instrumentation."""

from __future__ import annotations

import functools
import json
import logging
from typing import Any

from a2a.server.request_handlers.default_request_handler import DefaultRequestHandler
from opentelemetry import trace
from opentelemetry.trace import StatusCode, Tracer

from galileo_a2a._constants import (
    A2A_CONTEXT_ID,
    A2A_RPC_METHOD,
    A2A_TASK_ID,
    GENAI_AGENT_NAME,
    GENAI_INPUT_MESSAGES,
    GENAI_OPERATION_NAME,
    GENAI_SYSTEM,
    ROLE_USER,
    SESSION_ID,
)
from galileo_a2a._context import (
    create_parent_context_from_trace,
    create_span_link_from_context,
    extract_trace_context,
)
from galileo_a2a._message_utils import extract_text_from_parts, set_output_on_span, track_task_state

_logger = logging.getLogger(__name__)

# Stashed original methods for uninstrumentation
_originals: dict[str, Any] = {}


def _patch_server(tracer: Tracer, agent_name: str | None = None) -> None:
    """Patch ``DefaultRequestHandler`` methods to create OTel spans for inbound A2A requests.

    Idempotent — safe to call multiple times. Rolls back partial patches on
    failure to avoid leaving the class in an inconsistent state.
    """
    if _originals:
        _logger.warning("a2a-sdk server already patched, skipping")
        return

    patched_keys: list[str] = []
    try:
        _originals["DefaultRequestHandler.on_message_send"] = DefaultRequestHandler.on_message_send
        patched_keys.append("DefaultRequestHandler.on_message_send")
        DefaultRequestHandler.on_message_send = _wrap_on_message_send(
            tracer, _originals["DefaultRequestHandler.on_message_send"], agent_name
        )

        _originals["DefaultRequestHandler.on_message_send_stream"] = DefaultRequestHandler.on_message_send_stream
        patched_keys.append("DefaultRequestHandler.on_message_send_stream")
        DefaultRequestHandler.on_message_send_stream = _wrap_on_message_send_stream(
            tracer, _originals["DefaultRequestHandler.on_message_send_stream"], agent_name
        )
    except Exception:
        _logger.error(
            "Failed to patch a2a-sdk server — rolling back. The installed a2a-sdk version may be incompatible.",
            exc_info=True,
        )
        for key in patched_keys:
            if key in _originals:
                setattr(DefaultRequestHandler, key.split(".")[1], _originals.pop(key))
        return

    _logger.debug("Patched a2a-sdk server handler methods")


def _unpatch_server() -> None:
    """Restore original a2a-sdk server handler methods."""
    if "DefaultRequestHandler.on_message_send" in _originals:
        DefaultRequestHandler.on_message_send = _originals.pop("DefaultRequestHandler.on_message_send")
    if "DefaultRequestHandler.on_message_send_stream" in _originals:
        DefaultRequestHandler.on_message_send_stream = _originals.pop("DefaultRequestHandler.on_message_send_stream")

    _logger.debug("Unpatched a2a-sdk server handler methods")


def _build_server_span_context(params: Any) -> tuple[list[Any], Any]:
    """Extract cross-agent trace context from A2A request metadata.

    Returns ``(links, parent_ctx)`` for use with ``tracer.start_as_current_span``.
    """
    metadata = getattr(params, "metadata", None) or {}
    trace_ctx = extract_trace_context(metadata)

    links: list[Any] = []
    parent_ctx = None
    if trace_ctx:
        link = create_span_link_from_context(trace_ctx)
        if link:
            links.append(link)
        parent_ctx = create_parent_context_from_trace(trace_ctx)
    return links, parent_ctx


def _wrap_on_message_send(tracer: Tracer, original: Any, agent_name: str | None = None) -> Any:
    """Create an instrumented wrapper for DefaultRequestHandler.on_message_send."""

    @functools.wraps(original)
    async def wrapper(self: Any, params: Any, context: Any = None) -> Any:
        links, parent_ctx = _build_server_span_context(params)

        with tracer.start_as_current_span("a2a.server.on_message_send", links=links, context=parent_ctx) as span:
            _set_server_span_attributes(span, params, "SendMessage", agent_name)
            _set_input_from_params(span, params)

            try:
                result = await original(self, params, context)
                set_output_on_span(span, result)
                track_task_state(span, result)
                return result
            except Exception as exc:
                span.record_exception(exc)
                span.set_status(StatusCode.ERROR, str(exc))
                raise

    return wrapper


def _wrap_on_message_send_stream(tracer: Tracer, original: Any, agent_name: str | None = None) -> Any:
    """Create an instrumented wrapper for DefaultRequestHandler.on_message_send_stream."""

    @functools.wraps(original)
    async def wrapper(self: Any, params: Any, context: Any = None) -> Any:
        links, parent_ctx = _build_server_span_context(params)

        with tracer.start_as_current_span("a2a.server.on_message_send_stream", links=links, context=parent_ctx) as span:
            _set_server_span_attributes(span, params, "SendStreamingMessage", agent_name)
            _set_input_from_params(span, params)

            try:
                result = original(self, params, context)
                async for event in result:
                    set_output_on_span(span, event)
                    track_task_state(span, event)
                    yield event
            except Exception as exc:
                span.record_exception(exc)
                span.set_status(StatusCode.ERROR, str(exc))
                raise

    return wrapper


def _set_server_span_attributes(span: trace.Span, params: Any, rpc_method: str, agent_name: str | None) -> None:
    """Set A2A and GenAI attributes on a server span."""
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


def _set_input_from_params(span: trace.Span, params: Any) -> None:
    """Extract input content from A2A MessageSendParams and set gen_ai.input.messages."""
    message = getattr(params, "message", None)
    if not message:
        return

    text = extract_text_from_parts(message)
    if text:
        span.set_attribute(GENAI_INPUT_MESSAGES, json.dumps([{"role": ROLE_USER, "content": text}]))
