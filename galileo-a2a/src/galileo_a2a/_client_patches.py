"""Monkey-patches for outbound A2A client calls."""

from __future__ import annotations

import functools
import logging
from typing import Any

from a2a.client.base_client import BaseClient
from opentelemetry import context as otel_context
from opentelemetry import trace
from opentelemetry.trace import StatusCode, Tracer

from galileo_a2a._constants import GALILEO_OBSERVE_KEY
from galileo_a2a._context import inject_trace_context, iter_with_context
from galileo_a2a._spans import (
    set_client_attributes,
    set_input,
    set_simple_input,
    set_simple_output,
    set_tool_attributes,
    track_event_state,
)

_logger = logging.getLogger(__name__)

_originals: dict[str, Any] = {}


def _patch_client(tracer: Tracer, agent_name: str | None = None) -> None:
    """Replace ``BaseClient`` methods with instrumented versions.

    Idempotent.  Rolls back partial patches on failure.
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
        BaseClient.get_task = _wrap_simple_method(tracer, _originals["BaseClient.get_task"], "GetTask")

        _originals["BaseClient.cancel_task"] = BaseClient.cancel_task
        patched_keys.append("BaseClient.cancel_task")
        BaseClient.cancel_task = _wrap_simple_method(tracer, _originals["BaseClient.cancel_task"], "CancelTask")

        _originals["BaseClient.get_card"] = BaseClient.get_card
        patched_keys.append("BaseClient.get_card")
        BaseClient.get_card = _wrap_simple_method(tracer, _originals["BaseClient.get_card"], "GetCard")
    except Exception:
        _logger.error(
            "Failed to patch a2a-sdk client — rolling back. The installed a2a-sdk version may be incompatible.",
            exc_info=True,
        )
        for key in patched_keys:
            if key in _originals:
                setattr(BaseClient, key.split(".")[1], _originals.pop(key))
        return

    _logger.debug("Patched a2a-sdk client methods")


def _unpatch_client() -> None:
    """Restore original ``BaseClient`` methods."""
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
    """Return an instrumented replacement for ``BaseClient.send_message``."""

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
        # Manual span lifecycle — see iter_with_context for rationale.
        span = tracer.start_span("a2a.client.send_message")
        span_ctx = trace.set_span_in_context(span)

        try:
            token = otel_context.attach(span_ctx)
            try:
                set_client_attributes(span, request, "SendMessage", agent_name)
                set_input(span, request)
                observe_ctx = inject_trace_context(agent_name=agent_name)
            finally:
                otel_context.detach(token)

            request_metadata = dict(request_metadata) if request_metadata else {}
            request_metadata[GALILEO_OBSERVE_KEY] = observe_ctx

            result = original(
                self,
                request,
                configuration=configuration,
                context=context,
                request_metadata=request_metadata,
                extensions=extensions,
            )
            async for event in iter_with_context(span_ctx, result):
                track_event_state(span, event)
                yield event
        except Exception as exc:
            span.record_exception(exc)
            span.set_status(StatusCode.ERROR, str(exc))
            raise
        finally:
            span.end()

    return wrapper


def _wrap_simple_method(tracer: Tracer, original: Any, rpc_method: str) -> Any:
    """Return an instrumented replacement for a non-streaming client method."""

    @functools.wraps(original)
    async def wrapper(self: Any, *args: Any, **kwargs: Any) -> Any:
        with tracer.start_as_current_span(f"a2a.client.{rpc_method.lower()}") as span:
            set_tool_attributes(span, rpc_method)
            set_simple_input(span, args, rpc_method)

            try:
                result = await original(self, *args, **kwargs)
                track_event_state(span, result)
                set_simple_output(span, result, rpc_method)
                return result
            except Exception as exc:
                span.record_exception(exc)
                span.set_status(StatusCode.ERROR, str(exc))
                raise

    return wrapper
