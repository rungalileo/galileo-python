"""Tests for distributed tracing middleware."""

from unittest.mock import Mock, patch

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from galileo.constants.tracing import PARENT_ID_HEADER, TRACE_ID_HEADER
from galileo.decorator import _parent_id_context, _trace_id_context
from galileo.logger import GalileoLogger
from galileo.middleware import TracingMiddleware, get_request_logger
from tests.testutils.setup import setup_mock_logstreams_client, setup_mock_projects_client, setup_mock_traces_client


@pytest.fixture
def app():
    """Create a test FastAPI app with tracing middleware."""
    app = FastAPI()
    app.add_middleware(TracingMiddleware)

    @app.get("/test")
    async def test_endpoint():
        logger = get_request_logger()
        return {
            "trace_id": logger.trace_id,
            "span_id": logger.span_id,
            "is_logger": isinstance(logger, GalileoLogger),  # Verify logger was created
        }

    @app.get("/test-context")
    async def test_context_endpoint():
        # Direct access to context variables
        return {"trace_id": _trace_id_context.get(), "parent_id": _parent_id_context.get()}

    @app.get("/test-add-span")
    async def test_add_span_endpoint():
        """Endpoint that tries to add a span to test distributed tracing stub creation.

        Note: In distributed tracing (distributed mode), when span_id is provided,
        the logger creates local stub objects in __init__ without fetching from backend.
        """
        try:
            logger = get_request_logger()
            # The validation should have happened during get_request_logger() call above
            # If we get here without exception, validation passed (or didn't run)
            # Try to add a span to confirm logger works
            logger.add_workflow_span(input="test", name="test_span")
            return {
                "error": None,
                "success": True,
                "trace_id": str(logger.trace_id),
                "span_id": str(logger.span_id) if logger.span_id else None,
            }
        except Exception as e:
            return {"error": str(e), "error_type": type(e).__name__, "success": False}

    return app


@pytest.fixture
def client(app):
    """Create a test client."""
    return TestClient(app)


@patch("galileo.logger.logger.LogStreams")
@patch("galileo.logger.logger.Projects")
@patch("galileo.logger.logger.Traces")
def test_middleware_extracts_headers(
    mock_traces_client: Mock, mock_projects_client: Mock, mock_logstreams_client: Mock, client: TestClient
):
    """Test that middleware correctly extracts tracing headers."""
    setup_mock_traces_client(mock_traces_client)
    setup_mock_projects_client(mock_projects_client)
    setup_mock_logstreams_client(mock_logstreams_client)

    # Use valid UUID4 values
    trace_id = "6c4e3f7e-4a9a-4e7e-8c1f-3a9a3a9a3a9d"
    parent_id = "6c4e3f7e-4a9a-4e7e-8c1f-3a9a3a9a3a9e"

    # Override get_span to return a span that belongs to the correct trace
    # Also override get_trace to return a trace with the correct trace_id
    import datetime
    from unittest.mock import AsyncMock
    from uuid import UUID

    now = datetime.datetime.now()
    mock_span = {
        "id": UUID(parent_id),
        "trace_id": UUID(trace_id),  # Same trace as header
        "type": "workflow",
        "name": "test-workflow-span",
        "input": "test-input",
        "output": None,
        "created_at": now,
        "updated_at": now,
        "user_metadata": {},
        "metrics": {},
        "parent_id": None,
    }
    mock_trace = {
        "id": UUID(trace_id),
        "name": "test-trace",
        "type": "trace",
        "input": "test-input",
        "output": None,
        "created_at": now,
        "updated_at": now,
        "user_metadata": {},
        "spans": [],
    }
    mock_instance = mock_traces_client.return_value
    mock_instance.get_span = AsyncMock(return_value=mock_span)
    mock_instance.get_trace = AsyncMock(return_value=mock_trace)

    response = client.get("/test", headers={TRACE_ID_HEADER: trace_id, PARENT_ID_HEADER: parent_id})

    assert response.status_code == 200
    data = response.json()
    assert data["is_logger"] is True
    assert data["trace_id"] == trace_id
    assert data["span_id"] == parent_id


@patch("galileo.logger.logger.LogStreams")
@patch("galileo.logger.logger.Projects")
@patch("galileo.logger.logger.Traces")
def test_middleware_handles_missing_headers(
    mock_traces_client: Mock, mock_projects_client: Mock, mock_logstreams_client: Mock, client: TestClient
):
    """Test that middleware handles requests without tracing headers."""
    setup_mock_traces_client(mock_traces_client)
    setup_mock_projects_client(mock_projects_client)
    setup_mock_logstreams_client(mock_logstreams_client)

    response = client.get("/test")

    assert response.status_code == 200
    data = response.json()
    assert data["is_logger"] is True
    assert data["trace_id"] is None
    assert data["span_id"] is None


@patch("galileo.logger.logger.LogStreams")
@patch("galileo.logger.logger.Projects")
@patch("galileo.logger.logger.Traces")
def test_middleware_handles_partial_headers(
    mock_traces_client: Mock, mock_projects_client: Mock, mock_logstreams_client: Mock, client: TestClient
):
    """Test that middleware handles requests with only trace ID.

    Note: In normal operation, both TRACE_ID_HEADER and PARENT_ID_HEADER should be present.

    However, when only TRACE_ID_HEADER is provided (no PARENT_ID_HEADER), the middleware
    handles this by creating a logger with the trace_id but no span_id,
    allowing the service to start a new root span within the existing trace.
    """
    setup_mock_traces_client(mock_traces_client)
    setup_mock_projects_client(mock_projects_client)
    setup_mock_logstreams_client(mock_logstreams_client)

    trace_id = "12345678-1234-4678-9abc-123456789abc"

    response = client.get("/test", headers={TRACE_ID_HEADER: trace_id})

    assert response.status_code == 200
    data = response.json()
    assert data["is_logger"] is True
    assert data["trace_id"] == trace_id
    assert data["span_id"] is None


@patch("galileo.logger.logger.LogStreams")
@patch("galileo.logger.logger.Projects")
@patch("galileo.logger.logger.Traces")
def test_context_cleanup_after_request(
    mock_traces_client: Mock, mock_projects_client: Mock, mock_logstreams_client: Mock, client: TestClient
):
    """Test that context variables are cleaned up after request."""
    setup_mock_traces_client(mock_traces_client)
    setup_mock_projects_client(mock_projects_client)
    setup_mock_logstreams_client(mock_logstreams_client)

    trace_id = "12345678-1234-4678-9abc-123456789abc"
    parent_id = "87654321-4321-4876-9cba-987654321cba"

    # First request with headers
    response1 = client.get("/test-context", headers={TRACE_ID_HEADER: trace_id, PARENT_ID_HEADER: parent_id})
    assert response1.status_code == 200
    data1 = response1.json()
    assert data1["trace_id"] == trace_id
    assert data1["parent_id"] == parent_id

    # Second request without headers - should not see previous request's context
    response2 = client.get("/test-context")
    assert response2.status_code == 200
    data2 = response2.json()
    assert data2["trace_id"] is None
    assert data2["parent_id"] is None


@patch("galileo.logger.logger.LogStreams")
@patch("galileo.logger.logger.Projects")
@patch("galileo.logger.logger.Traces")
def test_get_request_logger_when_parent_id_equals_trace_id(
    mock_traces_client: Mock, mock_projects_client: Mock, mock_logstreams_client: Mock, client: TestClient
):
    """Test that get_request_logger handles the case when parent_id equals trace_id.

    When upstream services forward headers immediately after start_trace(), both
    X-Galileo-Trace-ID and X-Galileo-Parent-ID are identical (the root trace id).
    In this case, we should pass None as span_id to avoid GalileoLoggerException.
    """
    setup_mock_traces_client(mock_traces_client)
    setup_mock_projects_client(mock_projects_client)
    setup_mock_logstreams_client(mock_logstreams_client)

    trace_id = "12345678-1234-4678-9abc-123456789abc"
    # parent_id equals trace_id (first hop after start_trace)
    parent_id = trace_id

    response = client.get("/test", headers={TRACE_ID_HEADER: trace_id, PARENT_ID_HEADER: parent_id})

    assert response.status_code == 200
    data = response.json()

    # When parent_id equals trace_id, span_id should be None (not the trace_id)
    # This prevents GalileoLogger from trying to look up a span with the trace_id
    assert data["is_logger"] is True
    assert data["trace_id"] == trace_id
    assert data["span_id"] is None


@patch("galileo.logger.logger.LogStreams")
@patch("galileo.logger.logger.Projects")
@patch("galileo.logger.logger.Traces")
def test_mismatched_trace_and_span_ids(
    mock_traces_client: Mock, mock_projects_client: Mock, mock_logstreams_client: Mock, client: TestClient
):
    """Test that get_request_logger creates stubs for distributed tracing.

    In distributed tracing (distributed mode), when trace_id and span_id are provided,
    the logger creates local stub objects instead of fetching from the backend.
    This allows distributed tracing to work without backend validation, with eventual
    consistency handling any mismatches during ingestion retries.
    """
    setup_mock_traces_client(mock_traces_client)
    setup_mock_projects_client(mock_projects_client)
    setup_mock_logstreams_client(mock_logstreams_client)

    trace_id = "12345678-1234-4678-9abc-123456789abc"
    parent_id = "99999999-9999-4999-9999-999999999999"

    response = client.get("/test-add-span", headers={TRACE_ID_HEADER: trace_id, PARENT_ID_HEADER: parent_id})

    assert response.status_code == 200
    data = response.json()

    # With stubs, logger initialization succeeds without backend validation
    # The stub objects are created locally, allowing distributed tracing to work
    # even when the parent span hasn't been ingested yet (eventual consistency)
    assert data["success"] is True, "Expected logger initialization to succeed with stubs"
    assert data["error"] is None
    assert data["trace_id"] == trace_id
    assert data["span_id"] == parent_id
