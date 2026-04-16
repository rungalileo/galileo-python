"""Trace context injection and extraction for cross-agent A2A correlation."""

from __future__ import annotations

import logging
from typing import Any

from opentelemetry import context as otel_context
from opentelemetry import trace
from opentelemetry.propagate import inject as otel_inject
from opentelemetry.trace import Link, NonRecordingSpan, SpanContext, TraceFlags

from galileo_a2a._constants import (
    AGNTCY_OBSERVE_KEY,
    GALILEO_OBSERVE_KEY,
    LINK_FROM_AGENT,
    LINK_TYPE,
    LINK_TYPE_AGENT_HANDOFF,
)

_logger = logging.getLogger(__name__)


def inject_trace_context(agent_name: str | None = None) -> dict[str, str]:
    """Build a metadata dict from the current OTel span context for propagation.

    The returned dict is added to A2A ``MessageSendParams.metadata`` so the
    receiving agent can reconstruct the caller's trace context.
    """
    carrier: dict[str, str] = {}
    otel_inject(carrier)

    span = trace.get_current_span()
    span_ctx = span.get_span_context()

    if span_ctx and span_ctx.is_valid:
        carrier["agent_trace_id"] = format(span_ctx.trace_id, "032x")
        carrier["agent_span_id"] = format(span_ctx.span_id, "016x")

    if agent_name:
        carrier["agent_name"] = agent_name

    return carrier


def extract_trace_context(metadata: dict[str, Any] | None) -> dict[str, str] | None:
    """Extract trace context from A2A request metadata.

    Checks the Galileo key first, then falls back to the AGNTCY key for
    interoperability with the AGNTCY Observe SDK.  Returns ``None`` when
    no trace context is present.
    """
    if not metadata or not isinstance(metadata, dict):
        return None

    ctx = metadata.get(GALILEO_OBSERVE_KEY)
    if ctx and isinstance(ctx, dict):
        return {str(k): str(v) for k, v in ctx.items()}

    ctx = metadata.get(AGNTCY_OBSERVE_KEY)
    if ctx and isinstance(ctx, dict):
        return {str(k): str(v) for k, v in ctx.items()}

    return None


def create_span_link_from_context(trace_context: dict[str, str]) -> Link | None:
    """Create an OTel ``Link`` pointing to the calling agent's span.

    The link carries ``link.type = "agent_handoff"`` and, when available,
    ``link.from_agent``.  Returns ``None`` when the context cannot be parsed.
    """
    ids = _parse_ids(trace_context)
    if ids is None:
        return None

    trace_id, span_id = ids

    attrs: dict[str, str] = {LINK_TYPE: LINK_TYPE_AGENT_HANDOFF}
    agent_name = trace_context.get("agent_name")
    if agent_name:
        attrs[LINK_FROM_AGENT] = agent_name

    return Link(
        context=SpanContext(
            trace_id=trace_id,
            span_id=span_id,
            is_remote=True,
            trace_flags=TraceFlags(TraceFlags.SAMPLED),
        ),
        attributes=attrs,
    )


def create_parent_context_from_trace(trace_context: dict[str, str]) -> otel_context.Context | None:
    """Create an OTel parent context so the server span joins the caller's trace.

    Returns ``None`` when the context cannot be parsed.
    """
    ids = _parse_ids(trace_context)
    if ids is None:
        return None

    trace_id, span_id = ids

    parent_span_context = SpanContext(
        trace_id=trace_id,
        span_id=span_id,
        is_remote=True,
        trace_flags=TraceFlags(TraceFlags.SAMPLED),
    )
    return trace.set_span_in_context(NonRecordingSpan(parent_span_context))


async def iter_with_context(ctx: otel_context.Context, async_iterable: Any) -> Any:
    """Iterate *async_iterable* with *ctx* attached for each ``__anext__`` call.

    Attaches *ctx* before each iteration step and detaches immediately after,
    so no context token is held across yield boundaries.  This is required
    for instrumenting async generators because ``start_as_current_span()``
    cannot be used when the span must survive across ``yield`` points.

    The inner async iterator is closed on any exit path including
    ``GeneratorExit`` from early stream termination.
    """
    aiter = async_iterable.__aiter__()
    try:
        while True:
            token = otel_context.attach(ctx)
            try:
                event = await aiter.__anext__()
            except StopAsyncIteration:
                break
            finally:
                otel_context.detach(token)
            yield event
    finally:
        aclose = getattr(aiter, "aclose", None)
        if aclose is not None:
            await aclose()


def _parse_ids(trace_context: dict[str, str]) -> tuple[int, int] | None:
    """Parse trace and span IDs from ``agent_trace_id``/``agent_span_id`` or ``traceparent``."""
    trace_id_hex = trace_context.get("agent_trace_id")
    span_id_hex = trace_context.get("agent_span_id")

    if not trace_id_hex or not span_id_hex:
        traceparent = trace_context.get("traceparent")
        if not traceparent:
            return None
        parts = traceparent.split("-")
        if len(parts) < 4:
            return None
        trace_id_hex = parts[1]
        span_id_hex = parts[2]

    try:
        trace_id = int(trace_id_hex, 16)
        span_id = int(span_id_hex, 16)
    except (ValueError, TypeError):
        _logger.debug("Failed to parse trace/span IDs from A2A context", exc_info=True)
        return None

    if trace_id == 0 or span_id == 0:
        return None

    return trace_id, span_id
