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
    """Build a galileo_observe metadata dict from the current OTel span context.

    This dict is injected into A2A ``MessageSendParams.metadata`` so that the
    receiving agent can link its trace back to the caller.

    Parameters
    ----------
    agent_name : str, optional
        Name of the calling agent, included for display purposes.

    Returns
    -------
    dict[str, str]
        Metadata dict containing traceparent, agent info, and span/trace IDs.
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

    Checks for Galileo's key first, then falls back to AGNTCY's key
    for compatibility with the AGNTCY Observe SDK.

    Parameters
    ----------
    metadata : dict or None
        The ``MessageSendParams.metadata`` from the A2A request.

    Returns
    -------
    dict[str, str] or None
        Extracted trace context, or None if not present.
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


def _parse_trace_and_span_ids(trace_context: dict[str, str]) -> tuple[int, int] | None:
    """Parse trace_id and span_id from a trace context dict.

    Tries ``agent_trace_id``/``agent_span_id`` first, then falls back
    to parsing the W3C ``traceparent`` header.

    Returns
    -------
    tuple[int, int] or None
        (trace_id, span_id) as integers, or None if parsing fails.
    """
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
        _logger.debug("Failed to parse trace/span IDs from A2A trace context", exc_info=True)
        return None

    if trace_id == 0 or span_id == 0:
        return None

    return trace_id, span_id


def create_span_link_from_context(trace_context: dict[str, str]) -> Link | None:
    """Create an OTel span Link from extracted trace context.

    Parses the ``traceparent`` header (or ``agent_trace_id`` / ``agent_span_id``)
    and creates a Link with ``link.type = "agent_handoff"`` attributes.

    Parameters
    ----------
    trace_context : dict[str, str]
        Trace context dict (from ``extract_trace_context``).

    Returns
    -------
    Link or None
        An OTel Link pointing to the calling agent's span, or None if
        the context cannot be parsed.
    """
    ids = _parse_trace_and_span_ids(trace_context)
    if ids is None:
        return None

    trace_id, span_id = ids

    link_attributes: dict[str, str] = {LINK_TYPE: LINK_TYPE_AGENT_HANDOFF}
    agent_name = trace_context.get("agent_name")
    if agent_name:
        link_attributes[LINK_FROM_AGENT] = agent_name

    return Link(
        context=SpanContext(
            trace_id=trace_id,
            span_id=span_id,
            is_remote=True,
            trace_flags=TraceFlags(TraceFlags.SAMPLED),
        ),
        attributes=link_attributes,
    )


def create_parent_context_from_trace(trace_context: dict[str, str]) -> otel_context.Context | None:
    """Create an OTel parent context from extracted trace context.

    This allows the server-side span to be a **child** of the client span
    (same trace ID), so both appear in a single distributed trace in Galileo.

    Parameters
    ----------
    trace_context : dict[str, str]
        Trace context dict (from ``extract_trace_context``).

    Returns
    -------
    Context or None
        An OTel Context with the caller's span as parent, or None if
        the context cannot be parsed.
    """
    ids = _parse_trace_and_span_ids(trace_context)
    if ids is None:
        return None

    trace_id, span_id = ids

    parent_span_context = SpanContext(
        trace_id=trace_id,
        span_id=span_id,
        is_remote=True,
        trace_flags=TraceFlags(TraceFlags.SAMPLED),
    )
    parent_span = NonRecordingSpan(parent_span_context)
    return trace.set_span_in_context(parent_span)
