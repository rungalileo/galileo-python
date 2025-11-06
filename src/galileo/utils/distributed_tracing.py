"""
Utility functions for distributed tracing header detection.

This module provides functions to automatically detect distributed tracing headers
from various web frameworks (FastAPI, Flask, Starlette, etc.) and extract trace/span IDs.

How it works with TracingMiddleware:
1. TracingMiddleware.dispatch() extracts headers from HTTP requests and stores them
   in ContextVar (context variables) using _trace_id_context and _span_id_context
2. extract_tracing_headers() first checks these context variables (via get_trace_id()
   and get_span_id()) - this is the primary path when middleware is used
3. If context variables are empty, it falls back to checking function arguments
   for request objects (useful when middleware isn't used or for Flask/WSGI apps)

This two-tier approach allows the @log decorator to work seamlessly:
- With middleware (FastAPI/Starlette): Headers are automatically extracted and stored
- Without middleware (Flask or manual): Headers are extracted from request objects
  passed as function arguments
"""

import logging
from typing import Any, Optional

from galileo.middleware.tracing import get_span_id, get_trace_id

_logger = logging.getLogger(__name__)


def extract_tracing_headers(
    func_args: tuple = (), func_kwargs: Optional[dict] = None
) -> tuple[Optional[str], Optional[str]]:
    """
    Extract distributed tracing headers from context or function arguments.

    This function first checks context variables (set by TracingMiddleware),
    then falls back to looking for web framework request objects in function arguments.

    Parameters
    ----------
    func_args
        Positional arguments passed to the function
    func_kwargs
        Keyword arguments passed to the function

    Returns
    -------
    Tuple[Optional[str], Optional[str]]
        A tuple of (trace_id, span_id) if found, otherwise (None, None)
    """
    # First, check context variables (set by TracingMiddleware)
    trace_id = get_trace_id()
    span_id = get_span_id()

    if trace_id or span_id:
        return trace_id, span_id

    # Fallback: check function arguments for request objects
    if func_kwargs is None:
        func_kwargs = {}

    # Check all arguments for request objects
    all_args = list(func_args) + list(func_kwargs.values())

    for arg in all_args:
        if arg is None:
            continue

        # Check if it's a web framework request object (FastAPI/Starlette or Flask)
        # Both ASGI (FastAPI) and WSGI (Flask) request objects expose headers similarly
        trace_id, span_id = _extract_from_request_object(arg)
        if trace_id or span_id:
            return trace_id, span_id

    return None, None


def _extract_from_request_object(request_obj: Any) -> tuple[Optional[str], Optional[str]]:
    """
    Extract tracing headers from a web framework request object.

    This function works with both FastAPI/Starlette (ASGI) and Flask (WSGI) request objects.
    Both frameworks expose headers in a similar way, so we can use a unified extraction method.

    Note: While FastAPI/Starlette uses ASGI (async) and Flask uses WSGI (sync), both expose
    request headers via a `headers` attribute with a `.get()` method, making unified extraction possible.

    Parameters
    ----------
    request_obj
        Potential web framework request object (FastAPI/Starlette Request or Flask request)

    Returns
    -------
    Tuple[Optional[str], Optional[str]]
        A tuple of (trace_id, span_id) if found, otherwise (None, None)
    """
    try:
        # Both FastAPI/Starlette and Flask request objects have a headers attribute
        if hasattr(request_obj, "headers"):
            headers = request_obj.headers
            # Both frameworks support .get() method on headers
            if hasattr(headers, "get"):
                # Try both lowercase and uppercase header names (case-insensitive)
                trace_id = headers.get("x-trace-id") or headers.get("X-Trace-ID")
                span_id = headers.get("x-span-id") or headers.get("X-Span-ID")
                return trace_id, span_id
    except Exception as e:
        _logger.debug(f"Failed to extract headers from request object: {e}")

    return None, None
