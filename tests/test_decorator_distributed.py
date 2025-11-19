"""Tests for decorator with distributed mode for distributed tracing."""

import os
from unittest.mock import Mock, patch

import pytest

from galileo import galileo_context, log
from galileo.constants.tracing import PARENT_ID_HEADER, TRACE_ID_HEADER
from galileo.decorator import _parent_id_context, _trace_id_context
from tests.testutils.setup import setup_mock_logstreams_client, setup_mock_projects_client, setup_mock_traces_client


@pytest.fixture
def reset_context():
    """Reset the decorator context before each test."""
    galileo_context.reset()
    yield
    galileo_context.reset()


@pytest.fixture
def set_distributed_mode():
    """Set GALILEO_MODE to distributed for tests."""
    original = os.getenv("GALILEO_MODE")
    os.environ["GALILEO_MODE"] = "distributed"
    yield
    if original is None:
        os.environ.pop("GALILEO_MODE", None)
    else:
        os.environ["GALILEO_MODE"] = original


@patch("galileo.logger.logger.LogStreams")
@patch("galileo.logger.logger.Projects")
@patch("galileo.logger.logger.Traces")
def test_decorator_get_tracing_headers(
    mock_traces_client: Mock,
    mock_projects_client: Mock,
    mock_logstreams_client: Mock,
    reset_context,
    set_distributed_mode,
):
    """Test that decorator can get tracing headers for distributed tracing."""
    setup_mock_traces_client(mock_traces_client)
    setup_mock_projects_client(mock_projects_client)
    setup_mock_logstreams_client(mock_logstreams_client)

    galileo_context.init(project="test-project", log_stream="test-stream")

    @log(span_type="workflow")
    def orchestrator(query: str) -> dict:
        # Get headers to propagate to downstream service
        from galileo.tracing import get_tracing_headers

        headers = get_tracing_headers()
        return {"result": query, "headers": headers}

    result = orchestrator("test input")

    assert "headers" in result
    headers = result["headers"]
    assert TRACE_ID_HEADER in headers
    assert PARENT_ID_HEADER in headers

    # Verify the trace ID matches the logger's trace
    logger = galileo_context.get_logger_instance()
    assert headers[TRACE_ID_HEADER] == str(logger.traces[0].id)


@patch("galileo.logger.logger.LogStreams")
@patch("galileo.logger.logger.Projects")
@patch("galileo.logger.logger.Traces")
def test_decorator_with_middleware_context(
    mock_traces_client: Mock,
    mock_projects_client: Mock,
    mock_logstreams_client: Mock,
    reset_context,
    set_distributed_mode,
):
    """Test that decorator respects middleware context (distributed tracing)."""
    setup_mock_traces_client(mock_traces_client)
    setup_mock_projects_client(mock_projects_client)
    setup_mock_logstreams_client(mock_logstreams_client)

    galileo_context.init(project="test-project", log_stream="test-stream")

    # Simulate middleware setting context variables
    trace_id = "12345678-1234-4678-9abc-123456789abc"
    parent_id = "87654321-4321-4876-9cba-987654321cba"

    _trace_id_context.set(trace_id)
    _parent_id_context.set(parent_id)

    @log(span_type="workflow")
    def downstream_service(query: str) -> str:
        return f"processed: {query}"

    result = downstream_service("test input")

    assert result == "processed: test input"

    # Verify logger was created with distributed tracing context
    logger = galileo_context.get_logger_instance()
    assert logger.mode == "distributed"
    assert len(logger.traces) == 1

    # Verify the stub trace was created with correct ID
    assert str(logger.traces[0].id) == trace_id
    assert logger.traces[0].name == "stub_trace"
