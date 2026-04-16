"""Monkey-patches for inbound A2A server request handlers."""

from __future__ import annotations

import functools
import logging
from typing import Any

from a2a.server.request_handlers.default_request_handler import DefaultRequestHandler
from opentelemetry import trace
from opentelemetry.trace import StatusCode, Tracer

from galileo_a2a._context import (
    create_parent_context_from_trace,
    create_span_link_from_context,
    extract_trace_context,
    iter_with_context,
)
from galileo_a2a._spans import set_input, set_output, set_server_attributes, track_task_state

_logger = logging.getLogger(__name__)

_originals: dict[str, Any] = {}


def _patch_server(tracer: Tracer, agent_name: str | None = None) -> None:
    """Replace ``DefaultRequestHandler`` methods with instrumented versions.

    Idempotent.  Rolls back partial patches on failure.
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
    """Restore original ``DefaultRequestHandler`` methods."""
    if "DefaultRequestHandler.on_message_send" in _originals:
        DefaultRequestHandler.on_message_send = _originals.pop("DefaultRequestHandler.on_message_send")
    if "DefaultRequestHandler.on_message_send_stream" in _originals:
        DefaultRequestHandler.on_message_send_stream = _originals.pop("DefaultRequestHandler.on_message_send_stream")

    _logger.debug("Unpatched a2a-sdk server handler methods")


def _build_span_context(params: Any) -> tuple[list[Any], Any]:
    """Extract caller trace context from A2A metadata.

    Returns ``(links, parent_ctx)`` for use when starting a server span.
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
    """Return an instrumented replacement for ``on_message_send``."""

    @functools.wraps(original)
    async def wrapper(self: Any, params: Any, context: Any = None) -> Any:
        links, parent_ctx = _build_span_context(params)

        with tracer.start_as_current_span("a2a.server.on_message_send", links=links, context=parent_ctx) as span:
            set_server_attributes(span, params, "SendMessage", agent_name)
            set_input(span, getattr(params, "message", None))

            try:
                result = await original(self, params, context)
                set_output(span, result)
                track_task_state(span, result)
                return result
            except Exception as exc:
                span.record_exception(exc)
                span.set_status(StatusCode.ERROR, str(exc))
                raise

    return wrapper


def _wrap_on_message_send_stream(tracer: Tracer, original: Any, agent_name: str | None = None) -> Any:
    """Return an instrumented replacement for ``on_message_send_stream``."""

    @functools.wraps(original)
    async def wrapper(self: Any, params: Any, context: Any = None) -> Any:
        links, parent_ctx = _build_span_context(params)

        # Manual span lifecycle — see iter_with_context for rationale.
        span = tracer.start_span("a2a.server.on_message_send_stream", links=links, context=parent_ctx)
        span_ctx = trace.set_span_in_context(span)

        try:
            set_server_attributes(span, params, "SendStreamingMessage", agent_name)
            set_input(span, getattr(params, "message", None))

            result = original(self, params, context)
            async for event in iter_with_context(span_ctx, result):
                set_output(span, event)
                track_task_state(span, event)
                yield event
        except Exception as exc:
            span.record_exception(exc)
            span.set_status(StatusCode.ERROR, str(exc))
            raise
        finally:
            span.end()

    return wrapper
