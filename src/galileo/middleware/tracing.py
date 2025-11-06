"""
Tracing middleware for FastAPI/Starlette applications.

This middleware automatically extracts distributed tracing headers from incoming
HTTP requests and stores them in a context variable, making them available to
the @log decorator throughout the request lifecycle.

How it works:
1. The `dispatch` method intercepts incoming HTTP requests
2. Extracts X-Trace-ID and X-Span-ID headers from the request
3. Stores them in ContextVar (thread-local context variables)
4. The @log decorator (via extract_tracing_headers in distributed_tracing.py)
   reads these context variables to automatically configure distributed tracing

This middleware is only for ASGI frameworks (FastAPI/Starlette). For Flask (WSGI),
users can manually pass request objects to decorated functions, and the decorator
will extract headers from the request object directly.
"""

import logging
from collections.abc import Awaitable, Callable
from contextvars import ContextVar
from typing import Optional

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

_logger = logging.getLogger(__name__)

# Context variables to store trace and span IDs
_trace_id_context: ContextVar[Optional[str]] = ContextVar("trace_id_context", default=None)
_span_id_context: ContextVar[Optional[str]] = ContextVar("span_id_context", default=None)


def get_trace_id() -> Optional[str]:
    """Get the current trace ID from context."""
    return _trace_id_context.get()


def get_span_id() -> Optional[str]:
    """Get the current span ID from context."""
    return _span_id_context.get()


class TracingMiddleware(BaseHTTPMiddleware):
    """
    Middleware that extracts distributed tracing headers from HTTP requests.

    This middleware automatically extracts X-Trace-ID and X-Span-ID headers
    from incoming requests and stores them in context variables. The @log decorator
    can then read these values to automatically configure distributed tracing.

    Usage:
        from fastapi import FastAPI
        from galileo.middleware import TracingMiddleware

        app = FastAPI()
        app.add_middleware(TracingMiddleware)

    Note: This requires starlette to be installed. Install it with:
        pip install galileo[starlette]
        # or
        pip install starlette
        # or
        pip install fastapi  # (which includes starlette)
    """

    async def dispatch(self, request: Request, call_next: Callable[[Request], Awaitable[Response]]) -> Response:
        """
        Extract tracing headers from incoming request and store in context.

        This method:
        1. Extracts X-Trace-ID and X-Span-ID headers from the HTTP request
        2. Stores them in ContextVar (context variables) that are automatically
           available throughout the async request lifecycle
        3. The @log decorator (via extract_tracing_headers in distributed_tracing.py)
           reads these context variables using get_trace_id() and get_span_id()

        The context variables are thread-local and async-safe, so they work correctly
        with FastAPI/Starlette's async request handling.

        Parameters
        ----------
        request
            The incoming HTTP request
        call_next
            The next middleware or route handler in the chain

        Returns
        -------
        Response
            The HTTP response from the next handler
        """
        # Extract X-Trace-ID and X-Span-ID headers (case-insensitive)
        trace_id = request.headers.get("x-trace-id") or request.headers.get("X-Trace-ID")
        span_id = request.headers.get("x-span-id") or request.headers.get("X-Span-ID")

        # Store in context variables for @log decorator to use
        # These context variables are automatically available to extract_tracing_headers()
        # via get_trace_id() and get_span_id() throughout the request lifecycle
        if trace_id:
            _trace_id_context.set(trace_id)
        if span_id:
            _span_id_context.set(span_id)

        # Call the next middleware/route handler
        return await call_next(request)
