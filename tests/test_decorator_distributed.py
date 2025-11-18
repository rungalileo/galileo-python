"""Tests for decorator with distributed mode for distributed tracing."""

import asyncio
import os
from unittest.mock import Mock, patch

import pytest

from galileo import galileo_context, log
from galileo.constants.tracing import PARENT_ID_HEADER, TRACE_ID_HEADER
from galileo.decorator import _parent_id_context, _trace_id_context
from galileo.schema.trace import SpanUpdateRequest, TraceUpdateRequest
from tests.testutils.setup import (
    setup_mock_logstreams_client,
    setup_mock_projects_client,
    setup_mock_traces_client,
    setup_thread_pool_request_capture,
)


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


@patch("galileo.logger.logger.LogStreams")
@patch("galileo.logger.logger.Projects")
@patch("galileo.logger.logger.Traces")
def test_decorator_updates_trace_with_output_and_duration(
    mock_traces_client: Mock,
    mock_projects_client: Mock,
    mock_logstreams_client: Mock,
    reset_context,
    set_distributed_mode,
):
    """Test that decorator calls update_trace with output and duration when it starts a trace."""
    mock_traces_client_instance = setup_mock_traces_client(mock_traces_client)
    setup_mock_projects_client(mock_projects_client)
    setup_mock_logstreams_client(mock_logstreams_client)

    galileo_context.init(project="test-project", log_stream="test-stream")

    logger = galileo_context.get_logger_instance()
    capture = setup_thread_pool_request_capture(logger)

    @log(span_type="workflow")
    def my_function(input_value: str) -> str:
        return f"output: {input_value}"

    result = my_function("test input")

    assert result == "output: test input"

    # Verify that update_trace_with_backoff was called
    captured_tasks = capture.get_all_tasks()
    update_trace_tasks = [task for task in captured_tasks if task.function_name == "update_trace_with_backoff"]

    assert len(update_trace_tasks) > 0, "Expected update_trace_with_backoff to be called"

    # Get the update trace task
    update_task = update_trace_tasks[0]
    request = update_task.request
    assert isinstance(request, TraceUpdateRequest)

    # Verify the request has output and duration
    assert request.output == "output: test input"
    assert request.duration_ns is not None, "Expected duration_ns to be set"
    assert request.duration_ns > 0, "Expected duration_ns to be positive"
    assert request.is_complete

    # Verify it was called with the correct request
    asyncio.run(update_task.task_func())
    mock_traces_client_instance.update_trace.assert_called()


@patch("galileo.logger.logger.LogStreams")
@patch("galileo.logger.logger.Projects")
@patch("galileo.logger.logger.Traces")
def test_decorator_server_side_does_not_conclude_trace(
    mock_traces_client: Mock,
    mock_projects_client: Mock,
    mock_logstreams_client: Mock,
    reset_context,
    set_distributed_mode,
):
    """Test that decorator does NOT conclude trace when receiving distributed tracing headers (server side)."""
    setup_mock_traces_client(mock_traces_client)
    setup_mock_projects_client(mock_projects_client)
    setup_mock_logstreams_client(mock_logstreams_client)

    galileo_context.init(project="test-project", log_stream="test-stream")

    # Simulate middleware setting context variables (server receiving trace_id/span_id)
    trace_id = "12345678-1234-4678-9abc-123456789abc"
    parent_id = "87654321-4321-4876-9cba-987654321cba"

    _trace_id_context.set(trace_id)
    _parent_id_context.set(parent_id)

    logger = galileo_context.get_logger_instance()
    capture = setup_thread_pool_request_capture(logger)

    @log(span_type="workflow")
    def downstream_service(query: str) -> str:
        return f"processed: {query}"

    result = downstream_service("test input")

    assert result == "processed: test input"

    # Verify that update_trace_with_backoff was NOT called (we don't conclude traces we didn't start)
    captured_tasks = capture.get_all_tasks()
    update_trace_tasks = [task for task in captured_tasks if task.function_name == "update_trace_with_backoff"]

    # Should have NO trace updates - we didn't start this trace
    assert len(update_trace_tasks) == 0, "Expected NO update_trace calls when receiving distributed tracing headers"

    # Verify the stub trace was created
    assert len(logger.traces) == 1
    assert str(logger.traces[0].id) == trace_id
    assert logger.traces[0].name == "stub_trace"


@patch("galileo.logger.logger.LogStreams")
@patch("galileo.logger.logger.Projects")
@patch("galileo.logger.logger.Traces")
def test_decorator_client_and_server_side_behavior(
    mock_traces_client: Mock,
    mock_projects_client: Mock,
    mock_logstreams_client: Mock,
    reset_context,
    set_distributed_mode,
):
    """Test both client-side (starting trace) and server-side (receiving trace) behavior."""
    setup_mock_traces_client(mock_traces_client)
    setup_mock_projects_client(mock_projects_client)
    setup_mock_logstreams_client(mock_logstreams_client)

    galileo_context.init(project="test-project", log_stream="test-stream")

    # CLIENT SIDE: Start a new trace
    logger = galileo_context.get_logger_instance()
    capture_client = setup_thread_pool_request_capture(logger)

    @log(span_type="workflow")
    def client_function(query: str) -> str:
        return f"client output: {query}"

    result_client = client_function("client input")
    assert result_client == "client output: client input"

    # Verify client-side concludes the trace with output and duration
    client_tasks = capture_client.get_all_tasks()
    client_update_tasks = [task for task in client_tasks if task.function_name == "update_trace_with_backoff"]

    assert len(client_update_tasks) > 0, "Client side should conclude trace"
    client_request = client_update_tasks[0].request
    assert isinstance(client_request, TraceUpdateRequest)
    assert client_request.output == "client output: client input"
    assert client_request.duration_ns is not None
    assert client_request.duration_ns > 0

    # Reset context for server-side test
    galileo_context.reset()
    galileo_context.init(project="test-project", log_stream="test-stream")

    # SERVER SIDE: Receive distributed tracing headers
    trace_id = "aaaaaaaa-aaaa-4aaa-aaaa-aaaaaaaaaaaa"
    parent_id = "bbbbbbbb-bbbb-4bbb-bbbb-bbbbbbbbbbbb"

    _trace_id_context.set(trace_id)
    _parent_id_context.set(parent_id)

    logger_server = galileo_context.get_logger_instance()
    capture_server = setup_thread_pool_request_capture(logger_server)

    @log(span_type="workflow")
    def server_function(query: str) -> str:
        return f"server output: {query}"

    result_server = server_function("server input")
    assert result_server == "server output: server input"

    # Verify server-side does NOT conclude the trace (didn't start it)
    server_tasks = capture_server.get_all_tasks()
    server_update_tasks = [task for task in server_tasks if task.function_name == "update_trace_with_backoff"]

    assert len(server_update_tasks) == 0, "Server side should NOT conclude trace it didn't start"

    # Verify stub trace was created with the received trace_id
    assert len(logger_server.traces) == 1
    assert str(logger_server.traces[0].id) == trace_id
    assert logger_server.traces[0].name == "stub_trace"


@patch("galileo.logger.logger.LogStreams")
@patch("galileo.logger.logger.Projects")
@patch("galileo.logger.logger.Traces")
def test_decorator_workflow_span_output_is_set(
    mock_traces_client: Mock,
    mock_projects_client: Mock,
    mock_logstreams_client: Mock,
    reset_context,
    set_distributed_mode,
):
    """Test that workflow span output is properly set when concluded via decorator."""
    mock_traces_client_instance = setup_mock_traces_client(mock_traces_client)
    setup_mock_projects_client(mock_projects_client)
    setup_mock_logstreams_client(mock_logstreams_client)

    galileo_context.init(project="test-project", log_stream="test-stream")

    logger = galileo_context.get_logger_instance()
    capture = setup_thread_pool_request_capture(logger)

    @log(span_type="workflow")
    def my_workflow(input_value: str) -> str:
        return f"workflow output: {input_value}"

    result = my_workflow("test input")

    assert result == "workflow output: test input"

    # Verify that update_span_with_backoff was called for the workflow span
    captured_tasks = capture.get_all_tasks()
    update_span_tasks = [task for task in captured_tasks if task.function_name == "update_span_with_backoff"]

    assert len(update_span_tasks) > 0, "Expected update_span_with_backoff to be called for workflow span"

    # Get the update span task
    update_task = update_span_tasks[0]
    request = update_task.request

    assert isinstance(request, SpanUpdateRequest)

    # Verify the request has output
    assert request.output == "workflow output: test input", "Workflow span output should be set"
    assert request.duration_ns is not None, "Expected duration_ns to be set"
    assert request.duration_ns >= 0, "Expected duration_ns to be non-negative"

    # Verify it was called with the correct request
    asyncio.run(update_task.task_func())
    mock_traces_client_instance.update_span.assert_called()


@patch("galileo.logger.logger.LogStreams")
@patch("galileo.logger.logger.Projects")
@patch("galileo.logger.logger.Traces")
def test_decorator_both_trace_and_workflow_span_have_output(
    mock_traces_client: Mock,
    mock_projects_client: Mock,
    mock_logstreams_client: Mock,
    reset_context,
    set_distributed_mode,
):
    """Test that both trace and workflow span have output when using @log without span_type."""
    setup_mock_traces_client(mock_traces_client)
    setup_mock_projects_client(mock_projects_client)
    setup_mock_logstreams_client(mock_logstreams_client)

    galileo_context.init(project="test-project", log_stream="test-stream")

    logger = galileo_context.get_logger_instance()
    capture = setup_thread_pool_request_capture(logger)

    # @log without span_type creates a workflow span, and starts a trace if needed
    @log
    def my_function(input_value: str) -> str:
        return f"function output: {input_value}"

    result = my_function("test input")

    assert result == "function output: test input"

    # Verify both trace and span updates were sent
    captured_tasks = capture.get_all_tasks()
    update_trace_tasks = [task for task in captured_tasks if task.function_name == "update_trace_with_backoff"]
    update_span_tasks = [task for task in captured_tasks if task.function_name == "update_span_with_backoff"]

    # Should have both trace and span updates
    assert len(update_trace_tasks) > 0, "Expected update_trace_with_backoff to be called"
    assert len(update_span_tasks) > 0, "Expected update_span_with_backoff to be called"

    # Verify trace has output
    trace_task = update_trace_tasks[0]
    trace_request = trace_task.request
    assert isinstance(trace_request, TraceUpdateRequest)
    assert trace_request.output == "function output: test input", "Trace output should be set"
    assert trace_request.duration_ns is not None
    assert trace_request.duration_ns > 0

    # Verify workflow span has output
    span_task = update_span_tasks[0]
    span_request = span_task.request

    assert isinstance(span_request, SpanUpdateRequest)
    assert span_request.output == "function output: test input", "Workflow span output should be set"
    assert span_request.duration_ns is not None
    assert span_request.duration_ns >= 0


@patch("galileo.logger.logger.LogStreams")
@patch("galileo.logger.logger.Projects")
@patch("galileo.logger.logger.Traces")
def test_decorator_workflow_span_empty_string_output_is_set(
    mock_traces_client: Mock,
    mock_projects_client: Mock,
    mock_logstreams_client: Mock,
    reset_context,
    set_distributed_mode,
):
    """Test that workflow span output is set even when it's an empty string."""
    setup_mock_traces_client(mock_traces_client)
    setup_mock_projects_client(mock_projects_client)
    setup_mock_logstreams_client(mock_logstreams_client)

    galileo_context.init(project="test-project", log_stream="test-stream")

    logger = galileo_context.get_logger_instance()
    capture = setup_thread_pool_request_capture(logger)

    @log(span_type="workflow")
    def my_workflow(input_value: str) -> str:
        return ""  # Return empty string

    result = my_workflow("test input")

    assert result == ""

    # Verify that update_span_with_backoff was called
    captured_tasks = capture.get_all_tasks()
    update_span_tasks = [task for task in captured_tasks if task.function_name == "update_span_with_backoff"]

    assert len(update_span_tasks) > 0, "Expected update_span_with_backoff to be called"

    # Get the update span task
    update_task = update_span_tasks[0]
    request = update_task.request

    assert isinstance(request, SpanUpdateRequest)

    # Verify the request has empty string output (not None)
    assert request.output == "", "Workflow span output should be set to empty string, not None"
