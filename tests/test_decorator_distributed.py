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
    setup_mock_traces_client(mock_traces_client)
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

    # After the workflow call, the span is updated but the trace stays open
    captured_tasks = capture.get_all_tasks()
    update_span_tasks = [task for task in captured_tasks if task.function_name == "update_span_with_backoff"]

    assert len(update_span_tasks) > 0, "Expected workflow span update to be sent"

    # Verify the span was updated
    span_task = update_span_tasks[0]
    span_request = span_task.request
    assert isinstance(span_request, SpanUpdateRequest)
    assert span_request.output == "output: test input"
    assert span_request.duration_ns is not None
    assert span_request.duration_ns >= 0

    # Now flush to conclude the trace
    logger.flush()

    # After flush, verify trace was concluded
    captured_tasks = capture.get_all_tasks()
    update_trace_tasks = [task for task in captured_tasks if task.function_name == "update_trace_with_backoff"]

    assert len(update_trace_tasks) > 0, "Expected trace update after flush"

    # Find the trace update with is_complete=True (should be the last one)
    complete_trace_tasks = [task for task in update_trace_tasks if task.request.is_complete]
    assert len(complete_trace_tasks) > 0, (
        f"Expected at least one trace update with is_complete=True, but got {len(update_trace_tasks)} updates total"
    )

    trace_task = complete_trace_tasks[0]
    trace_request = trace_task.request
    assert isinstance(trace_request, TraceUpdateRequest)
    assert trace_request.is_complete, "Trace should be marked complete after flush"


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

    # Verify client-side sends span update (trace stays open until flush)
    client_tasks = capture_client.get_all_tasks()
    client_span_tasks = [task for task in client_tasks if task.function_name == "update_span_with_backoff"]

    assert len(client_span_tasks) > 0, "Client side should send span update"
    client_span_request = client_span_tasks[0].request
    assert isinstance(client_span_request, SpanUpdateRequest)
    assert client_span_request.output == "client output: client input"
    assert client_span_request.duration_ns is not None
    assert client_span_request.duration_ns >= 0

    # Flush to conclude the trace
    logger.flush()

    # After flush, verify trace was concluded
    client_tasks = capture_client.get_all_tasks()
    client_trace_tasks = [task for task in client_tasks if task.function_name == "update_trace_with_backoff"]

    assert len(client_trace_tasks) > 0, "Client side should conclude trace on flush"

    # Find the trace update with is_complete=True (should be the last one)
    complete_client_trace_tasks = [task for task in client_trace_tasks if task.request.is_complete]
    assert len(complete_client_trace_tasks) > 0, (
        f"Expected at least one trace update with is_complete=True, but got {len(client_trace_tasks)} updates total"
    )

    client_trace_request = complete_client_trace_tasks[0].request
    assert isinstance(client_trace_request, TraceUpdateRequest)
    assert client_trace_request.is_complete, "Trace should be marked complete"

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

    # After workflow call, only span update is sent (trace stays open)
    captured_tasks = capture.get_all_tasks()
    update_span_tasks = [task for task in captured_tasks if task.function_name == "update_span_with_backoff"]

    assert len(update_span_tasks) > 0, "Expected workflow span update to be sent"

    # Verify workflow span has output
    span_task = update_span_tasks[0]
    span_request = span_task.request

    assert isinstance(span_request, SpanUpdateRequest)
    assert span_request.output == "function output: test input", "Workflow span output should be set"
    assert span_request.duration_ns is not None
    assert span_request.duration_ns >= 0

    # Flush to conclude the trace
    logger.flush()

    # After flush, verify trace was updated
    captured_tasks = capture.get_all_tasks()
    update_trace_tasks = [task for task in captured_tasks if task.function_name == "update_trace_with_backoff"]

    assert len(update_trace_tasks) > 0, "Expected trace update after flush"

    # Find the trace update with is_complete=True (should be the last one)
    complete_trace_tasks = [task for task in update_trace_tasks if task.request.is_complete]
    assert len(complete_trace_tasks) > 0, (
        f"Expected at least one trace update with is_complete=True, but got {len(update_trace_tasks)} updates total"
    )

    trace_task = complete_trace_tasks[0]
    trace_request = trace_task.request
    assert isinstance(trace_request, TraceUpdateRequest)
    assert trace_request.output == "function output: test input", "Trace should inherit span output"
    assert trace_request.is_complete, "Trace should be marked complete after flush"


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


@patch("galileo.logger.logger.LogStreams")
@patch("galileo.logger.logger.Projects")
@patch("galileo.logger.logger.Traces")
def test_decorator_trace_duration_is_set_and_accumulates(
    mock_traces_client: Mock,
    mock_projects_client: Mock,
    mock_logstreams_client: Mock,
    reset_context,
    set_distributed_mode,
):
    """Test that trace duration is set and increases across multiple workflows."""
    setup_mock_traces_client(mock_traces_client)
    setup_mock_projects_client(mock_projects_client)
    setup_mock_logstreams_client(mock_logstreams_client)

    galileo_context.init(project="test-project", log_stream="test-stream")

    logger = galileo_context.get_logger_instance()
    capture = setup_thread_pool_request_capture(logger)

    @log(span_type="workflow")
    def workflow_step_1() -> str:
        return "step 1 complete"

    @log(span_type="workflow")
    def workflow_step_2() -> str:
        return "step 2 complete"

    # Execute first workflow
    result1 = workflow_step_1()
    assert result1 == "step 1 complete"

    tasks_after_first = capture.get_all_tasks()
    trace_updates_1 = [task for task in tasks_after_first if task.function_name == "update_trace_with_backoff"]

    # Should have at least one trace update after first workflow
    assert len(trace_updates_1) > 0, "Expected trace update after first workflow"
    first_trace_update = trace_updates_1[-1].request
    first_duration = first_trace_update.duration_ns

    # Verify duration is set and is a reasonable value (>= 0)
    assert first_duration is not None, "First trace duration should be set"
    assert first_duration > 0, f"First trace duration should be >= 0, got {first_duration}ns"

    # Execute second workflow
    result2 = workflow_step_2()
    assert result2 == "step 2 complete"

    tasks_after_second = capture.get_all_tasks()
    trace_updates_2 = [task for task in tasks_after_second if task.function_name == "update_trace_with_backoff"]

    # Should have more trace updates now
    assert len(trace_updates_2) > len(trace_updates_1), "Expected additional trace update after second workflow"
    second_trace_update = trace_updates_2[-1].request
    second_duration = second_trace_update.duration_ns

    # Verify second duration is set and >= first duration (time has passed or stayed same)
    assert second_duration is not None, "Second trace duration should be set"
    assert second_duration >= first_duration, (
        f"Second trace duration ({second_duration}ns) should be >= first duration ({first_duration}ns)"
    )
