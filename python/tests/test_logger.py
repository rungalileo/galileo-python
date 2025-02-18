from uuid import UUID
from unittest.mock import AsyncMock, Mock, patch

import pytest

from galileo.logger import GalileoLogger
from galileo.schema.trace import TracesIngestRequest
from galileo_core.schemas.shared.traces.trace import Trace

from galileo_core.schemas.shared.workflows.node_type import NodeType


def setup_mock_api_client(mock_api_client: Mock):
    mock_instance = mock_api_client.return_value
    mock_ingest_traces_sync = AsyncMock(return_value={})
    mock_ingest_traces_async = AsyncMock(return_value={})
    mock_instance.get_project_by_name = AsyncMock(return_value={"id": UUID("6c4e3f7e-4a9a-4e7e-8c1f-3a9a3a9a3a9a")})
    mock_instance.get_log_stream_by_name = AsyncMock(return_value={"id": UUID("6c4e3f7e-4a9a-4e7e-8c1f-3a9a3a9a3a9b")})
    mock_instance.ingest_traces_sync = mock_ingest_traces_sync
    mock_instance.ingest_traces = mock_ingest_traces_async
    return mock_instance


@patch("galileo.logger.ApiClient")
def test_single_span_trace_to_galileo(mock_api_client: Mock) -> None:
    mock_instance = setup_mock_api_client(mock_api_client)

    created_time_ns = 0
    metadata = {"key": "value"}
    logger = GalileoLogger(project="my_project", log_stream="my_log_stream")
    logger.start_trace(
        input="input", name="test-trace", duration_ns=1_000_000, created_at_ns=created_time_ns, metadata=metadata
    )
    span = logger.add_llm_span(
        input="prompt",
        output="response",
        model="gpt4o",
        name="test-span",
        tools=[{"name": "tool1", "args": {"arg1": "val1"}}],
        duration_ns=1_000_000,
        created_at_ns=created_time_ns,
        metadata=metadata,
        temperature=1.0,
        status_code=200,
    )
    logger.conclude("output", status_code=200)
    logger.flush()

    payload = mock_instance.ingest_traces_sync.call_args[0][0]
    expected_payload = TracesIngestRequest(
        log_stream_id=None,  # TODO: fix this
        experiment_id=None,
        traces=[
            Trace(
                type=NodeType.trace,
                input="input",
                output="output",
                name="test-trace",
                created_at_ns=created_time_ns,
                duration_ns=1_000_000,
                metadata=metadata,
                status_code=200,
                ground_truth=None,
                spans=[span],
            )
        ],
    )
    assert payload == expected_payload
    assert logger.traces == list()
    assert logger.current_parent is None


@patch("galileo.logger.ApiClient")
def test_nested_span_trace_to_galileo(mock_api_client: Mock) -> None:
    mock_instance = setup_mock_api_client(mock_api_client)

    created_time_ns = 0
    metadata = {"key": "value"}
    logger = GalileoLogger(project="my_project", log_stream="my_log_stream")
    trace = logger.start_trace(
        input="input", name="test-trace", duration_ns=1_000_000, created_at_ns=created_time_ns, metadata=metadata
    )
    workflow_span = logger.add_workflow_span(
        input="prompt", name="test-workflow-span", created_at_ns=created_time_ns, metadata=metadata
    )

    workflow_span.add_llm_span(
        input="prompt",
        output="response",
        model="gpt4o",
        name="test-span",
        tools=[{"name": "tool1", "args": {"arg1": "val1"}}],
        duration_ns=1_000_000,
        created_at_ns=created_time_ns,
        metadata=metadata,
        temperature=1.0,
        status_code=200,
    )

    workflow_span.conclude(output="response", duration_ns=1_000_000, status_code=200)

    trace.conclude("response", duration_ns=1_000_000, status_code=200)

    assert logger.traces == [trace]

    logger.flush()

    payload = mock_instance.ingest_traces_sync.call_args[0][0]
    expected_payload = TracesIngestRequest(
        log_stream_id=None,  # TODO: fix this
        experiment_id=None,
        traces=[trace],
    )
    assert payload == expected_payload
    assert logger.traces == list()
    assert logger.current_parent is None


@patch("galileo.logger.ApiClient")
def test_multi_span_trace_to_galileo(mock_api_client: Mock) -> None:
    mock_instance = setup_mock_api_client(mock_api_client)

    created_time_ns = 0
    metadata = {"key": "value"}
    logger = GalileoLogger(project="my_project", log_stream="my_log_stream")
    trace = logger.start_trace(
        input="input", name="test-trace", duration_ns=1_000_000, created_at_ns=created_time_ns, metadata=metadata
    )
    workflow_span = logger.add_workflow_span(
        input="prompt", name="test-workflow-span", created_at_ns=created_time_ns, metadata=metadata
    )

    workflow_span.add_llm_span(
        input="prompt",
        output="response",
        model="gpt4o",
        name="test-span",
        tools=[{"name": "tool1", "args": {"arg1": "val1"}}],
        duration_ns=1_000_000,
        created_at_ns=created_time_ns,
        metadata=metadata,
        temperature=1.0,
        status_code=200,
    )

    workflow_span.conclude(output="response", duration_ns=1_000_000, status_code=200)

    second_span = trace.add_llm_span(
        input="prompt2",
        output="response2",
        model="gpt4o",
        name="test-span2",
        tools=[{"name": "tool1", "args": {"arg1": "val1"}}],
        duration_ns=1_000_000,
        created_at_ns=created_time_ns,
        metadata=metadata,
        temperature=1.0,
        status_code=200,
    )

    trace.conclude("response2", duration_ns=1_000_000, status_code=200)

    logger.flush()

    payload = mock_instance.ingest_traces_sync.call_args[0][0]
    expected_payload = TracesIngestRequest(
        log_stream_id=None,  # TODO: fix this
        experiment_id=None,
        traces=[
            Trace(
                type=NodeType.trace,
                input="input",
                output="response2",
                name="test-trace",
                created_at_ns=created_time_ns,
                duration_ns=1_000_000,
                metadata=metadata,
                status_code=200,
                ground_truth=None,
                spans=[workflow_span, second_span],
            )
        ],
    )
    assert payload == expected_payload
    assert logger.traces == list()
    assert logger.current_parent is None


@pytest.mark.asyncio
@patch("galileo.logger.ApiClient")
async def test_single_span_trace_to_galileo_with_async(mock_api_client: Mock) -> None:
    mock_instance = setup_mock_api_client(mock_api_client)

    created_time_ns = 0
    metadata = {"key": "value"}
    logger = GalileoLogger(project="my_project", log_stream="my_log_stream")
    logger.start_trace(
        input="input", name="test-trace", duration_ns=1_000_000, created_at_ns=created_time_ns, metadata=metadata
    )
    span = logger.add_llm_span(
        input="prompt",
        output="response",
        model="gpt4o",
        name="test-span",
        tools=[{"name": "tool1", "args": {"arg1": "val1"}}],
        duration_ns=1_000_000,
        created_at_ns=created_time_ns,
        metadata=metadata,
        temperature=1.0,
        status_code=200,
    )
    logger.conclude("output", status_code=200)
    await logger.async_flush()

    payload = mock_instance.ingest_traces.call_args[0][0]
    expected_payload = TracesIngestRequest(
        log_stream_id=None,  # TODO: fix this
        experiment_id=None,
        traces=[
            Trace(
                type=NodeType.trace,
                input="input",
                output="output",
                name="test-trace",
                created_at_ns=created_time_ns,
                duration_ns=1_000_000,
                metadata=metadata,
                status_code=200,
                ground_truth=None,
                spans=[span],
            )
        ],
    )
    assert payload == expected_payload
    assert logger.traces == list()
    assert logger.current_parent is None
