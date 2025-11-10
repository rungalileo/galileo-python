"""Tests for distributed tracing middleware."""

from unittest.mock import Mock, patch

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from galileo.constants.tracing import PARENT_ID_HEADER, TRACE_ID_HEADER
from galileo.decorator import _parent_id_context, _trace_id_context
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
        return {"trace_id": logger.trace_id, "span_id": logger.span_id}

    @app.get("/test-context")
    async def test_context_endpoint():
        # Direct access to context variables
        return {"trace_id": _trace_id_context.get(), "parent_id": _parent_id_context.get()}

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

    trace_id = "00000000-0000-0000-0000-000000000001"
    parent_id = "00000000-0000-0000-0000-000000000002"

    response = client.get("/test", headers={TRACE_ID_HEADER: trace_id, PARENT_ID_HEADER: parent_id})

    assert response.status_code == 200
    data = response.json()
    assert data["trace_id"] == trace_id
    assert data["span_id"] == parent_id


@patch("galileo.logger.logger.LogStreams")
@patch("galileo.logger.logger.Projects")
@patch("galileo.logger.logger.Traces")
def test_middleware_sets_context_variables(
    mock_traces_client: Mock, mock_projects_client: Mock, mock_logstreams_client: Mock, client: TestClient
):
    """Test that middleware sets context variables correctly."""
    setup_mock_traces_client(mock_traces_client)
    setup_mock_projects_client(mock_projects_client)
    setup_mock_logstreams_client(mock_logstreams_client)

    trace_id = "00000000-0000-0000-0000-000000000001"
    parent_id = "00000000-0000-0000-0000-000000000002"

    response = client.get("/test-context", headers={TRACE_ID_HEADER: trace_id, PARENT_ID_HEADER: parent_id})

    assert response.status_code == 200
    data = response.json()
    assert data["trace_id"] == trace_id
    assert data["parent_id"] == parent_id


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
    assert data["trace_id"] is None
    assert data["span_id"] is None


@patch("galileo.logger.logger.LogStreams")
@patch("galileo.logger.logger.Projects")
@patch("galileo.logger.logger.Traces")
def test_middleware_handles_partial_headers(
    mock_traces_client: Mock, mock_projects_client: Mock, mock_logstreams_client: Mock, client: TestClient
):
    """Test that middleware handles requests with only trace ID."""
    setup_mock_traces_client(mock_traces_client)
    setup_mock_projects_client(mock_projects_client)
    setup_mock_logstreams_client(mock_logstreams_client)

    trace_id = "00000000-0000-0000-0000-000000000001"

    response = client.get("/test", headers={TRACE_ID_HEADER: trace_id})

    assert response.status_code == 200
    data = response.json()
    assert data["trace_id"] == trace_id
    assert data["span_id"] is None


@patch("galileo.logger.logger.LogStreams")
@patch("galileo.logger.logger.Projects")
@patch("galileo.logger.logger.Traces")
def test_get_request_logger_with_headers(
    mock_traces_client: Mock, mock_projects_client: Mock, mock_logstreams_client: Mock, client: TestClient
):
    """Test that get_request_logger returns a properly configured logger."""
    setup_mock_traces_client(mock_traces_client)
    setup_mock_projects_client(mock_projects_client)
    setup_mock_logstreams_client(mock_logstreams_client)

    trace_id = "00000000-0000-0000-0000-000000000001"
    parent_id = "00000000-0000-0000-0000-000000000002"

    response = client.get("/test", headers={TRACE_ID_HEADER: trace_id, PARENT_ID_HEADER: parent_id})

    assert response.status_code == 200
    data = response.json()

    # Verify the logger was created with the correct IDs
    assert data["trace_id"] == trace_id
    assert data["span_id"] == parent_id


@patch("galileo.logger.logger.LogStreams")
@patch("galileo.logger.logger.Projects")
@patch("galileo.logger.logger.Traces")
def test_get_request_logger_without_headers(
    mock_traces_client: Mock, mock_projects_client: Mock, mock_logstreams_client: Mock, client: TestClient
):
    """Test that get_request_logger works without tracing headers."""
    setup_mock_traces_client(mock_traces_client)
    setup_mock_projects_client(mock_projects_client)
    setup_mock_logstreams_client(mock_logstreams_client)

    response = client.get("/test")

    assert response.status_code == 200
    data = response.json()

    # Without headers, logger should still be created but without trace context
    assert data["trace_id"] is None
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

    trace_id = "00000000-0000-0000-0000-000000000001"
    parent_id = "00000000-0000-0000-0000-000000000002"

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
