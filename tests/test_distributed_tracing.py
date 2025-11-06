"""Tests for distributed tracing functionality."""

import datetime
from unittest.mock import AsyncMock, Mock, patch
from uuid import UUID

import pytest
from starlette.requests import Request
from starlette.responses import Response

from galileo import galileo_context, log
from galileo.middleware.tracing import TracingMiddleware, get_span_id, get_trace_id
from galileo.utils.distributed_tracing import extract_tracing_headers
from tests.testutils.setup import setup_mock_logstreams_client, setup_mock_projects_client, setup_mock_traces_client


@pytest.fixture
def reset_context() -> None:
    """Reset galileo context before each test."""
    galileo_context.reset()


def test_extract_tracing_headers_from_context() -> None:
    """Test extracting trace/span IDs from context variables."""
    # Set context variables (as middleware would)
    from galileo.middleware.tracing import _span_id_context, _trace_id_context

    _trace_id_context.set("test-trace-id-123")
    _span_id_context.set("test-span-id-456")

    trace_id, span_id = extract_tracing_headers()

    assert trace_id == "test-trace-id-123"
    assert span_id == "test-span-id-456"

    # Clean up
    _trace_id_context.set(None)
    _span_id_context.set(None)


def test_extract_tracing_headers_from_fastapi_request() -> None:
    """Test extracting trace/span IDs from FastAPI Request object."""
    # Create a mock request with headers
    mock_request = Mock(spec=Request)
    mock_request.headers = {"X-Trace-ID": "trace-from-request", "X-Span-ID": "span-from-request"}

    trace_id, span_id = extract_tracing_headers(func_args=(mock_request,))

    assert trace_id == "trace-from-request"
    assert span_id == "span-from-request"


def test_extract_tracing_headers_from_fastapi_request_lowercase() -> None:
    """Test extracting trace/span IDs from FastAPI Request with lowercase headers."""
    mock_request = Mock(spec=Request)
    mock_request.headers = {"x-trace-id": "trace-lower", "x-span-id": "span-lower"}

    trace_id, span_id = extract_tracing_headers(func_args=(mock_request,))

    assert trace_id == "trace-lower"
    assert span_id == "span-lower"


def test_extract_tracing_headers_from_flask_request() -> None:
    """Test extracting trace/span IDs from Flask request object."""
    # Create a mock Flask request
    mock_request = Mock()
    mock_request.headers = Mock()
    mock_request.headers.get = Mock(
        side_effect=lambda key, default=None: {"X-Trace-ID": "flask-trace", "X-Span-ID": "flask-span"}.get(key, default)
    )

    trace_id, span_id = extract_tracing_headers(func_args=(mock_request,))

    assert trace_id == "flask-trace"
    assert span_id == "flask-span"


def test_extract_tracing_headers_priority_context_over_request() -> None:
    """Test that context variables take priority over request objects."""
    from galileo.middleware.tracing import _span_id_context, _trace_id_context

    # Set context variables
    _trace_id_context.set("context-trace")
    _span_id_context.set("context-span")

    # Create request with different IDs
    mock_request = Mock(spec=Request)
    mock_request.headers = {"X-Trace-ID": "request-trace", "X-Span-ID": "request-span"}

    trace_id, span_id = extract_tracing_headers(func_args=(mock_request,))

    # Context should take priority
    assert trace_id == "context-trace"
    assert span_id == "context-span"

    # Clean up
    _trace_id_context.set(None)
    _span_id_context.set(None)


def test_extract_tracing_headers_no_headers() -> None:
    """Test extracting when no headers are present."""
    trace_id, span_id = extract_tracing_headers()

    assert trace_id is None
    assert span_id is None


@patch("galileo.logger.logger.LogStreams")
@patch("galileo.logger.logger.Projects")
@patch("galileo.logger.logger.Traces")
def test_tracing_middleware_extracts_headers(
    mock_traces_client: Mock, mock_projects_client: Mock, mock_logstreams_client: Mock
) -> None:
    """Test that TracingMiddleware extracts headers from requests."""
    setup_mock_traces_client(mock_traces_client)
    setup_mock_projects_client(mock_projects_client)
    setup_mock_logstreams_client(mock_logstreams_client)

    middleware = TracingMiddleware(app=None)

    # Create a mock request
    mock_request = Mock(spec=Request)
    mock_request.headers = {"X-Trace-ID": "middleware-trace-123", "X-Span-ID": "middleware-span-456"}

    # Create a mock call_next
    async def mock_call_next(request: Request) -> Response:
        # Verify context was set
        assert get_trace_id() == "middleware-trace-123"
        assert get_span_id() == "middleware-span-456"
        return Response()

    # Run the middleware
    import asyncio

    asyncio.run(middleware.dispatch(mock_request, mock_call_next))

    # Verify context is cleared after request (or still available if needed)
    # Note: Context variables are request-scoped, so they may persist
    # until the next request in the same context


@patch("galileo.logger.logger.LogStreams")
@patch("galileo.logger.logger.Projects")
@patch("galileo.logger.logger.Traces")
def test_decorator_with_distributed_tracing_context(
    mock_traces_client: Mock, mock_projects_client: Mock, mock_logstreams_client: Mock, reset_context
) -> None:
    """Test that @log decorator uses distributed tracing headers from context."""
    mock_traces_client_instance = setup_mock_traces_client(mock_traces_client)
    setup_mock_projects_client(mock_projects_client)
    setup_mock_logstreams_client(mock_logstreams_client)

    # Set up context with distributed tracing IDs (as middleware would)
    from galileo.middleware.tracing import _span_id_context, _trace_id_context

    test_trace_id = "6c4e3f7e-4a9a-4e7e-8c1f-3a9a3a9a3a9d"
    test_span_id = "6c4e3f7e-4a9a-4e7e-8c1f-3a9a3a9a3a9e"

    _trace_id_context.set(test_trace_id)
    _span_id_context.set(test_span_id)

    # Mock get_trace to return an existing trace (for distributed tracing)
    # Note: get_trace is already mocked as AsyncMock in setup_mock_traces_client
    # We just need to update its return value
    mock_traces_client_instance.get_trace = AsyncMock(
        return_value={
            "id": UUID(test_trace_id),
            "name": "distributed-trace",
            "type": "trace",
            "input": "original input",
            "output": None,
            "created_at": datetime.datetime.now(),
            "updated_at": datetime.datetime.now(),
            "user_metadata": {},
            "spans": [],
            "metrics": {},
        }
    )

    # Mock get_span to return an existing span (for distributed tracing)
    # Note: get_span is already mocked as AsyncMock in setup_mock_traces_client
    mock_traces_client_instance.get_span = AsyncMock(
        return_value={
            "id": UUID(test_span_id),
            "name": "distributed-span",
            "type": "workflow",
            "input": "original input",
            "output": None,
            "created_at": datetime.datetime.now(),
            "updated_at": datetime.datetime.now(),
            "user_metadata": {},
            "metrics": {},
            "parent_id": UUID(test_trace_id),
            "trace_id": UUID(test_trace_id),
        }
    )

    # Initialize context in streaming mode (required for distributed tracing)
    galileo_context.init(project="test-project", log_stream="test-stream", mode="streaming")

    @log(span_type="retriever")
    def retrieval_service(query: str) -> str:
        return "retrieved data"

    @log
    def retrieve_endpoint(query: str) -> str:
        return retrieval_service(query=query)

    result = retrieve_endpoint(query="test query")
    galileo_context.flush_all()

    # Verify get_trace was called to load the distributed trace
    # In streaming mode with distributed tracing, get_trace should be called to load the existing trace
    mock_traces_client_instance.get_trace.assert_called()

    # Verify the functions executed successfully
    assert result == "retrieved data"

    # Clean up
    _trace_id_context.set(None)
    _span_id_context.set(None)


@patch("galileo.logger.logger.LogStreams")
@patch("galileo.logger.logger.Projects")
@patch("galileo.logger.logger.Traces")
def test_decorator_with_distributed_tracing_request_object(
    mock_traces_client: Mock, mock_projects_client: Mock, mock_logstreams_client: Mock, reset_context
) -> None:
    """Test that @log decorator extracts headers from Request object in function args."""
    mock_traces_client_instance = setup_mock_traces_client(mock_traces_client)
    setup_mock_projects_client(mock_projects_client)
    setup_mock_logstreams_client(mock_logstreams_client)

    # Mock get_trace for distributed tracing
    test_trace_id = "6c4e3f7e-4a9a-4e7e-8c1f-3a9a3a9a3a9f"
    test_span_id = "6c4e3f7e-4a9a-4e7e-8c1f-3a9a3a9a3a9g"

    # Note: get_trace is already mocked as AsyncMock in setup_mock_traces_client
    # We just need to update its return value
    mock_traces_client_instance.get_trace = AsyncMock(
        return_value={
            "id": UUID(test_trace_id),
            "name": "request-trace",
            "type": "trace",
            "input": "original input",
            "output": None,
            "created_at": datetime.datetime.now(),
            "updated_at": datetime.datetime.now(),
            "user_metadata": {},
            "spans": [],
            "metrics": {},
        }
    )

    galileo_context.init(project="test-project", log_stream="test-stream", mode="streaming")

    # Create a mock request with headers
    mock_request = Mock(spec=Request)
    mock_request.headers = {"X-Trace-ID": test_trace_id, "X-Span-ID": test_span_id}

    @log(span_type="retriever")
    def retrieval_service(query: str) -> str:
        return "retrieved data"

    @log
    def retrieve_endpoint(request: Request, query: str) -> str:
        return retrieval_service(query=query)

    retrieve_endpoint(request=mock_request, query="test query")
    galileo_context.flush_all()

    # Verify get_trace was called to load the distributed trace
    mock_traces_client_instance.get_trace.assert_called()


@patch("galileo.logger.logger.LogStreams")
@patch("galileo.logger.logger.Projects")
@patch("galileo.logger.logger.Traces")
def test_singleton_not_caches_distributed_tracing_loggers(
    mock_traces_client: Mock, mock_projects_client: Mock, mock_logstreams_client: Mock, reset_context
) -> None:
    """Test that singleton does not cache loggers when trace_id/span_id are provided."""
    from galileo.utils.singleton import GalileoLoggerSingleton

    setup_mock_traces_client(mock_traces_client)
    setup_mock_projects_client(mock_projects_client)
    setup_mock_logstreams_client(mock_logstreams_client)

    # Clear any existing loggers
    singleton = GalileoLoggerSingleton()
    singleton.reset()

    galileo_context.init(project="test-project", log_stream="test-stream", mode="streaming")

    # Set up context with distributed tracing IDs
    from galileo.middleware.tracing import _span_id_context, _trace_id_context
    from galileo.utils.distributed_tracing import extract_tracing_headers

    _trace_id_context.set("trace-1")
    _span_id_context.set("span-1")

    # Extract trace_id/span_id and get logger instance with them
    trace_id_1, span_id_1 = extract_tracing_headers()
    logger1 = galileo_context.get_logger_instance(trace_id=trace_id_1, span_id=span_id_1)

    @log
    def func1() -> str:
        return "result1"

    func1()

    # Change trace/span IDs
    _trace_id_context.set("trace-2")
    _span_id_context.set("span-2")

    # Extract new trace_id/span_id and get a new logger instance
    trace_id_2, span_id_2 = extract_tracing_headers()
    logger2 = galileo_context.get_logger_instance(trace_id=trace_id_2, span_id=span_id_2)

    @log
    def func2() -> str:
        return "result2"

    func2()

    # In distributed tracing mode, each request should get a new logger instance
    # (not cached based on trace_id/span_id)
    # The loggers should be different instances
    assert logger1 is not logger2

    # Verify they have different trace_id/span_id
    assert logger1.trace_id == "trace-1"
    assert logger1.span_id == "span-1"
    assert logger2.trace_id == "trace-2"
    assert logger2.span_id == "span-2"

    # Clean up
    _trace_id_context.set(None)
    _span_id_context.set(None)
