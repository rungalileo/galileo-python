"""
Distributed tracing middleware for Starlette-based applications.

This middleware automatically extracts distributed tracing headers from incoming HTTP requests
and makes them available to the Galileo logger within request handlers.

Works with any ASGI framework built on Starlette:
- FastAPI
- Starlette
- Any other Starlette-based framework

Example usage with FastAPI:
    ```python
    from fastapi import FastAPI
    from galileo.middleware import TracingMiddleware, get_request_logger

    app = FastAPI()
    app.add_middleware(TracingMiddleware)

    @app.post("/process")
    async def process_request(data: dict):
        # Logger automatically continues the distributed trace
        logger = get_request_logger()
        logger.add_workflow_span(input=str(data), name="process_workflow")
        # ... process request ...
        logger.conclude(output="done")
        return {"status": "success"}
    ```

Example usage with Starlette:
    ```python
    from starlette.applications import Starlette
    from starlette.routing import Route
    from galileo.middleware import TracingMiddleware, get_request_logger

    async def homepage(request):
        logger = get_request_logger()
        logger.add_workflow_span(input="homepage", name="homepage_handler")
        logger.conclude(output="success")
        return {"status": "ok"}

    app = Starlette(
        routes=[Route("/", homepage)],
        middleware=[TracingMiddleware]
    )
    ```
"""

import logging
from typing import Any, NoReturn

from galileo.constants.tracing import PARENT_ID_HEADER, TRACE_ID_HEADER
from galileo.decorator import _parent_id_context, _trace_id_context
from galileo.logger import GalileoLogger

_logger = logging.getLogger(__name__)

INSTALL_ERR_MSG = (
    "Starlette is not installed. Install optional middleware dependencies with: pip install galileo[middleware]"
)

try:
    from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
    from starlette.requests import Request
    from starlette.responses import Response
    from starlette.types import ASGIApp
except ImportError:
    # Create stub classes if Starlette is not available
    class BaseHTTPMiddleware:  # type: ignore[no-redef]
        def __init__(self, *args: Any, **kwargs: Any) -> NoReturn:
            raise ImportError(INSTALL_ERR_MSG)

    class Request:  # type: ignore[no-redef]
        pass

    class Response:  # type: ignore[no-redef]
        pass

    class RequestResponseEndpoint:  # type: ignore[no-redef]
        pass

    class ASGIApp:  # type: ignore[no-redef]
        pass


class TracingMiddleware(BaseHTTPMiddleware):
    """
    Middleware that extracts distributed tracing headers from incoming requests.

    This middleware looks for the following headers in incoming HTTP requests:
    - X-Galileo-Trace-ID: The root trace ID
    - X-Galileo-Parent-ID: The parent span/trace ID to attach to

    These values are stored in context variables, making them available to request
    handlers via the `get_request_logger()` function.

    The middleware is compatible with FastAPI and any Starlette-based framework.

    Note: Project and log_stream are configured per service via environment variables
    (GALILEO_PROJECT and GALILEO_LOG_STREAM). They are not propagated via headers,
    following standard distributed tracing patterns.
    """

    def __init__(self, app: ASGIApp) -> None:
        """
        Initialize the tracing middleware.

        Parameters
        ----------
        app : ASGIApp
            The ASGI application
        """
        super().__init__(app)

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        """
        Process the request and extract tracing headers.

        Parameters
        ----------
        request : Request
            The incoming HTTP request
        call_next : RequestResponseEndpoint
            The next middleware or route handler

        Returns
        -------
        Response
            The HTTP response
        """
        # Extract tracing headers from request
        trace_id = request.headers.get(TRACE_ID_HEADER)
        parent_id = request.headers.get(PARENT_ID_HEADER)

        # Store in context variables (thread-safe for async)
        trace_id_token = _trace_id_context.set(trace_id)
        parent_id_token = _parent_id_context.set(parent_id)

        try:
            # Process the request
            return await call_next(request)
        finally:
            # Clean up context variables
            _trace_id_context.reset(trace_id_token)
            _parent_id_context.reset(parent_id_token)


def get_request_logger() -> GalileoLogger:
    """
    Get a request-scoped GalileoLogger configured for distributed mode.

    Note: Distributed mode enables distributed tracing across services by propagating
    trace context and sending updates immediately to the backend.

    This function should be called within a request handler after the TracingMiddleware has
    been registered. It creates a new GalileoLogger instance per request that automatically
    continues the distributed trace from the upstream service.

    The logger is configured using trace context extracted by the middleware:
    - X-Galileo-Trace-ID: Root trace ID
    - X-Galileo-Parent-ID: Parent span/trace ID to attach to

    Project and log_stream are configured per service via environment variables
    (GALILEO_PROJECT and GALILEO_LOG_STREAM), not propagated via headers, following
    standard distributed tracing patterns.

    If no tracing headers were present in the request, a regular logger is returned
    (using GALILEO_PROJECT and GALILEO_LOG_STREAM env vars).

    Note: This creates a new logger per request, unlike the decorator's get_logger_instance()
    which uses a singleton pattern.

    Returns
    -------
    GalileoLogger
        A logger instance configured for the current request's trace context

    Examples
    --------
    ```python
    @app.post("/process")
    async def process_request(data: dict):
        logger = get_request_logger()

        # This span will be attached to the distributed trace
        logger.add_workflow_span(input=str(data), name="process_workflow")
        result = await process(data)
        logger.conclude(output=str(result))

        logger.flush()
        logger.terminate()

        return {"result": result}
    ```

    ```python
    @app.post("/retrieve")
    async def retrieve_endpoint(query: str):
        # Get logger with trace context from upstream service
        logger = get_request_logger()

        # If trace context exists, this creates a workflow span
        # Otherwise, it starts a new trace
        if logger.trace_id:
            logger.add_workflow_span(input=query, name="retrieval_service")
        else:
            logger.start_trace(input=query, name="retrieval_service")

        results = retrieve(query, logger)

        logger.conclude(output=str(results))
        logger.flush()
        logger.terminate()

        return {"results": results}
    ```
    """
    # Get trace context from middleware
    trace_id = _trace_id_context.get()
    parent_id = _parent_id_context.get()

    # Create logger with trace context
    # Project and log_stream come from env vars (GALILEO_PROJECT, GALILEO_LOG_STREAM)
    # If parent_id equals trace_id, it means the parent is the root trace itself,
    # not a span. In this case, we should pass None as span_id to avoid
    # GalileoLoggerException when it tries to look up a span with the trace_id.
    return GalileoLogger(mode="distributed", trace_id=trace_id, span_id=parent_id if parent_id != trace_id else None)
