"""Experimental A2A (Agent-to-Agent) tracing support for Galileo.

This module provides OpenTelemetry-based tracing for A2A protocol endpoints,
creating spans with gen_ai semantic convention attributes compatible with
Galileo's trace viewer.

Usage::

    from galileo.__future__.a2a import A2ASpanMiddleware, inject_trace_context

    # Server side: add middleware to capture A2A request/response data
    app.add_middleware(A2ASpanMiddleware)

    # Client side: propagate trace context across A2A service boundaries
    httpx_client = httpx.AsyncClient(
        event_hooks={"request": [inject_trace_context]}
    )
"""

from galileo.__future__.a2a.asgi_middleware import A2ASpanMiddleware
from galileo.__future__.a2a.propagation import inject_trace_context

__all__ = ["A2ASpanMiddleware", "inject_trace_context"]
