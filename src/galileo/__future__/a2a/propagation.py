"""Trace context propagation for A2A client calls.

Provides an httpx event hook that injects the W3C traceparent header into
outgoing requests, enabling distributed tracing across A2A service boundaries.
"""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import httpx

logger = logging.getLogger(__name__)

_INJECT_ERR_MSG = (
    "OpenTelemetry packages are required for trace context propagation. Install with: pip install galileo[otel]"
)


async def inject_trace_context(request: httpx.Request) -> None:
    """Inject W3C trace context headers into an outgoing httpx request.

    Use as an httpx event hook to propagate trace context (``traceparent``)
    across A2A service boundaries without creating additional HTTPX spans::

        httpx_client = httpx.AsyncClient(
            event_hooks={"request": [inject_trace_context]}
        )

    If OpenTelemetry is not installed, a warning is logged and the request
    is left unchanged.

    Parameters
    ----------
    request : httpx.Request
        The outgoing httpx request to inject headers into.
    """
    try:
        from opentelemetry.propagate import inject
    except ImportError:
        logger.warning(_INJECT_ERR_MSG)
        return

    inject(request.headers)
