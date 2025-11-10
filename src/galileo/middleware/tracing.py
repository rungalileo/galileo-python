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
from typing import Optional

from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response
from starlette.types import ASGIApp

from galileo.constants.tracing import PARENT_ID_HEADER, TRACE_ID_HEADER
from galileo.decorator import _parent_id_context, _trace_id_context
from galileo.logger import GalileoLogger

_logger = logging.getLogger(__name__)


class TracingMiddleware(BaseHTTPMiddleware):
    """
    Middleware that extracts distributed tracing headers from incoming requests.

    This middleware looks for X-Galileo-Trace-ID and X-Galileo-Parent-ID headers
    in incoming HTTP requests and stores them in context variables, making them
    available to request handlers via the `get_request_logger()` function.

    The middleware is compatible with FastAPI and any Starlette-based framework.

    Attributes
    ----------
    project : Optional[str]
        Default project name for loggers created within requests
    log_stream : Optional[str]
        Default log stream name for loggers created within requests
    """

    def __init__(self, app: ASGIApp, project: Optional[str] = None, log_stream: Optional[str] = None) -> None:
        """
        Initialize the tracing middleware.

        Parameters
        ----------
        app : ASGIApp
            The ASGI application
        project : Optional[str]
            Default project name (can be overridden by GALILEO_PROJECT env var)
        log_stream : Optional[str]
            Default log stream name (can be overridden by GALILEO_LOG_STREAM env var)
        """
        super().__init__(app)
        self.project = project
        self.log_stream = log_stream

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


def get_request_logger(project: Optional[str] = None, log_stream: Optional[str] = None) -> GalileoLogger:
    """
    Get a request-scoped GalileoLogger configured with distributed tracing context.

    This function should be called within a request handler after the TracingMiddleware has
    been registered. It creates a new GalileoLogger instance per request that automatically
    continues the distributed trace from the upstream service.

    If no tracing headers were present in the request, a regular logger is returned.

    Note: This creates a new logger per request, unlike the decorator's get_logger_instance()
    which uses a singleton pattern.

    Parameters
    ----------
    project : Optional[str]
        Project name (defaults to GALILEO_PROJECT env var)
    log_stream : Optional[str]
        Log stream name (defaults to GALILEO_LOG_STREAM env var)

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
    return GalileoLogger(
        project=project, log_stream=log_stream, experimental={"mode": "streaming"}, trace_id=trace_id, span_id=parent_id
    )
