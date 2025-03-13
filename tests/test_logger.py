import datetime
import logging
from collections import deque
from unittest.mock import AsyncMock, Mock, patch
from uuid import UUID

import pytest

from galileo.logger import GalileoLogger
from galileo.schema.trace import TracesIngestRequest
from galileo_core.schemas.logging.span import RetrieverSpan
from galileo_core.schemas.logging.step import Metrics
from galileo_core.schemas.logging.trace import Trace
from galileo_core.schemas.shared.document import Document
from galileo_core.schemas.shared.workflows.node_type import NodeType
from tests.testutils.setup import (
    setup_mock_core_api_client,
    setup_mock_experiment_client,
    setup_mock_logstreams_client,
    setup_mock_projects_client,
)

LOGGER = logging.getLogger(__name__)


def test_galileo_logger_exceptions() -> None:
    with pytest.raises(Exception) as exc_info:
        GalileoLogger(project="my_project", log_stream="my_log_stream", experiment_id="my_experiment_id")
    assert str(exc_info.value) == "User must provide either experiment_id or log_stream, not both."


@patch("galileo.logger.LogStreams")
@patch("galileo.logger.Projects")
@patch("galileo.logger.GalileoCoreApiClient")
def test_single_span_trace_to_galileo(
    mock_core_api_client: Mock, mock_projects_client: Mock, mock_logstreams_client: Mock
) -> None:
    mock_core_api_instance = setup_mock_core_api_client(mock_core_api_client)
    setup_mock_projects_client(mock_projects_client)
    setup_mock_logstreams_client(mock_logstreams_client)

    created_at = datetime.datetime.now()
    metadata = {"key": "value"}
    logger = GalileoLogger(project="my_project", log_stream="my_log_stream")
    logger.start_trace(
        input="input", name="test-trace", duration_ns=1_000_000, created_at=created_at, metadata=metadata
    )
    span = logger.add_llm_span(
        input="prompt",
        output="response",
        model="gpt4o",
        name="test-span",
        tools=[{"name": "tool1", "args": {"arg1": "val1"}}],
        duration_ns=1_000_000,
        created_at=created_at,
        metadata=metadata,
        temperature=1.0,
        status_code=200,
    )
    logger.conclude("output", status_code=200)
    logger.flush()

    payload = mock_core_api_instance.ingest_traces_sync.call_args[0][0]
    expected_payload = TracesIngestRequest(
        log_stream_id=None,  # TODO: fix this
        experiment_id=None,
        traces=[
            Trace(
                type=NodeType.trace,
                input="input",
                output="output",
                name="test-trace",
                created_at=created_at,
                user_metadata=metadata,
                status_code=200,
                spans=[span],
                metrics=Metrics(duration_ns=1000000),
            )
        ],
    )
    assert payload == expected_payload
    assert logger.traces == list()
    assert logger._parent_stack == deque()


@patch("galileo.experiments.Experiment")
@patch("galileo.logger.Projects")
@patch("galileo.logger.GalileoCoreApiClient")
def test_single_span_trace_to_galileo_experiment_id(
    mock_core_api_client: Mock, mock_projects_client: Mock, mock_experiments_client: Mock
) -> None:
    mock_core_api_instance = setup_mock_core_api_client(mock_core_api_client)
    setup_mock_projects_client(mock_projects_client)
    setup_mock_experiment_client(mock_experiments_client)

    created_at = datetime.datetime.now()
    metadata = {"key": "value"}
    logger = GalileoLogger(project="my_project", experiment_id="6c4e3f7e-4a9a-4e7e-8c1f-3a9a3a9a3a9a")
    logger.start_trace(
        input="input", name="test-trace", duration_ns=1_000_000, created_at=created_at, metadata=metadata
    )
    logger.conclude("output", status_code=200)
    logger.flush()

    payload = mock_core_api_instance.ingest_traces_sync.call_args[0][0]
    expected_payload = TracesIngestRequest(
        log_stream_id=None,
        experiment_id="6c4e3f7e-4a9a-4e7e-8c1f-3a9a3a9a3a9a",
        traces=[
            Trace(
                type=NodeType.trace,
                input="input",
                output="output",
                name="test-trace",
                created_at=created_at,
                user_metadata=metadata,
                status_code=200,
                spans=[],
                metrics=Metrics(duration_ns=1000000),
            )
        ],
    )
    assert payload == expected_payload
    assert logger.traces == list()
    assert logger._parent_stack == deque()


@patch("galileo.logger.LogStreams")
@patch("galileo.logger.Projects")
@patch("galileo.logger.GalileoCoreApiClient")
def test_nested_span_trace_to_galileo(
    mock_core_api_client: Mock, mock_projects_client: Mock, mock_logstreams_client: Mock
) -> None:
    mock_core_api_instance = setup_mock_core_api_client(mock_core_api_client)
    setup_mock_projects_client(mock_projects_client)
    setup_mock_logstreams_client(mock_logstreams_client)

    created_at = datetime.datetime.now()
    metadata = {"key": "value"}
    logger = GalileoLogger(project="my_project", log_stream="my_log_stream")
    trace = logger.start_trace(
        input="input", name="test-trace", duration_ns=1_000_000, created_at=created_at, metadata=metadata
    )
    logger.add_workflow_span(input="prompt", name="test-workflow-span", created_at=created_at, metadata=metadata)

    logger.add_llm_span(
        input="prompt",
        output="response",
        model="gpt4o",
        name="test-span",
        tools=[{"name": "tool1", "args": {"arg1": "val1"}}],
        duration_ns=1_000_000,
        created_at=created_at,
        metadata=metadata,
        temperature=1.0,
        status_code=200,
    )

    logger.conclude(output="response", duration_ns=1_000_000, status_code=200)

    logger.conclude("response", duration_ns=1_000_000, status_code=200)

    assert logger.traces == [trace]

    logger.flush()

    payload = mock_core_api_instance.ingest_traces_sync.call_args[0][0]
    expected_payload = TracesIngestRequest(
        log_stream_id=None,  # TODO: fix this
        experiment_id=None,
        traces=[trace],
    )
    assert payload == expected_payload
    assert logger.traces == list()
    assert logger._parent_stack == deque()


@patch("galileo.logger.LogStreams")
@patch("galileo.logger.Projects")
@patch("galileo.logger.GalileoCoreApiClient")
def test_multi_span_trace_to_galileo(
    mock_core_api_client: Mock, mock_projects_client: Mock, mock_logstreams_client: Mock
) -> None:
    mock_core_api_instance = setup_mock_core_api_client(mock_core_api_client)
    setup_mock_projects_client(mock_projects_client)
    setup_mock_logstreams_client(mock_logstreams_client)

    created_at = datetime.datetime.now()
    metadata = {"key": "value"}
    logger = GalileoLogger(project="my_project", log_stream="my_log_stream")
    logger.start_trace(
        input="input", name="test-trace", duration_ns=1_000_000, created_at=created_at, metadata=metadata
    )
    workflow_span = logger.add_workflow_span(
        input="prompt", name="test-workflow-span", created_at=created_at, metadata=metadata
    )

    logger.add_llm_span(
        input="prompt",
        output="response",
        model="gpt4o",
        name="test-span",
        tools=[{"name": "tool1", "args": {"arg1": "val1"}}],
        duration_ns=1_000_000,
        created_at=created_at,
        metadata=metadata,
        temperature=1.0,
        status_code=200,
    )

    logger.conclude(output="response", duration_ns=1_000_000, status_code=200)

    second_span = logger.add_llm_span(
        input="prompt2",
        output="response2",
        model="gpt4o",
        name="test-span2",
        tools=[{"name": "tool1", "args": {"arg1": "val1"}}],
        duration_ns=1_000_000,
        created_at=created_at,
        metadata=metadata,
        temperature=1.0,
        status_code=200,
    )

    logger.conclude("response2", duration_ns=1_000_000, status_code=200)

    logger.flush()

    payload = mock_core_api_instance.ingest_traces_sync.call_args[0][0]
    expected_payload = TracesIngestRequest(
        log_stream_id=None,  # TODO: fix this
        experiment_id=None,
        traces=[
            Trace(
                type=NodeType.trace,
                input="input",
                output="response2",
                name="test-trace",
                created_at=created_at,
                user_metadata=metadata,
                status_code=200,
                spans=[workflow_span, second_span],
                metrics=Metrics(duration_ns=1000000),
            )
        ],
    )
    assert payload == expected_payload
    assert logger.traces == list()
    assert logger._parent_stack == deque()


@pytest.mark.asyncio
@patch("galileo.logger.LogStreams")
@patch("galileo.logger.Projects")
@patch("galileo.logger.GalileoCoreApiClient")
async def test_single_span_trace_to_galileo_with_async(
    mock_core_api_client: Mock, mock_projects_client: Mock, mock_logstreams_client: Mock
) -> None:
    mock_core_api_instance = setup_mock_core_api_client(mock_core_api_client)
    setup_mock_projects_client(mock_projects_client)
    setup_mock_logstreams_client(mock_logstreams_client)

    created_at = datetime.datetime.now()
    metadata = {"key": "value"}
    logger = GalileoLogger(project="my_project", log_stream="my_log_stream")
    logger.start_trace(
        input="input", name="test-trace", duration_ns=1_000_000, created_at=created_at, metadata=metadata
    )
    span = logger.add_llm_span(
        input="prompt",
        output="response",
        model="gpt4o",
        name="test-span",
        tools=[{"name": "tool1", "args": {"arg1": "val1"}}],
        duration_ns=1_000_000,
        created_at=created_at,
        metadata=metadata,
        temperature=1.0,
        status_code=200,
    )
    logger.conclude("output", status_code=200)
    await logger.async_flush()

    payload = mock_core_api_instance.ingest_traces.call_args[0][0]
    expected_payload = TracesIngestRequest(
        log_stream_id=None,  # TODO: fix this
        experiment_id=None,
        traces=[
            Trace(
                type=NodeType.trace,
                input="input",
                output="output",
                name="test-trace",
                created_at=created_at,
                user_metadata=metadata,
                status_code=200,
                spans=[span],
                metrics=Metrics(duration_ns=1000000),
            )
        ],
    )
    assert payload == expected_payload
    assert logger.traces == list()
    assert logger._parent_stack == deque()


@patch("galileo.logger.LogStreams")
@patch("galileo.logger.Projects")
@patch("galileo.logger.GalileoCoreApiClient")
def test_retriever_span_str_output(
    mock_core_api_client: Mock, mock_projects_client: Mock, mock_logstreams_client: Mock
) -> None:
    mock_core_api_instance = setup_mock_core_api_client(mock_core_api_client)
    setup_mock_projects_client(mock_projects_client)
    setup_mock_logstreams_client(mock_logstreams_client)

    created_at = datetime.datetime.now()
    logger = GalileoLogger(project="my_project", log_stream="my_log_stream")
    logger.start_trace(input="input", name="test-trace", created_at=created_at)
    logger.add_retriever_span(
        input="prompt", output="response", name="test-span", created_at=created_at, status_code=200
    )
    logger.conclude("output", status_code=200)
    logger.flush()

    payload = mock_core_api_instance.ingest_traces_sync.call_args[0][0]

    assert isinstance(payload.traces[0].spans[0], RetrieverSpan)
    assert payload.traces[0].spans[0].input == "prompt"
    assert payload.traces[0].spans[0].output == [Document(content="response", metadata=None)]


@patch("galileo.logger.LogStreams")
@patch("galileo.logger.Projects")
@patch("galileo.logger.GalileoCoreApiClient")
def test_retriever_span_list_str_output(
    mock_core_api_client: Mock, mock_projects_client: Mock, mock_logstreams_client: Mock
) -> None:
    mock_core_api_instance = setup_mock_core_api_client(mock_core_api_client)
    setup_mock_projects_client(mock_projects_client)
    setup_mock_logstreams_client(mock_logstreams_client)

    created_at = datetime.datetime.now()
    logger = GalileoLogger(project="my_project", log_stream="my_log_stream")
    logger.start_trace(input="input", name="test-trace", created_at=created_at)
    logger.add_retriever_span(
        input="prompt", output=["response1", "response2"], name="test-span", created_at=created_at, status_code=200
    )
    logger.conclude("output", status_code=200)
    logger.flush()

    payload = mock_core_api_instance.ingest_traces_sync.call_args[0][0]

    assert isinstance(payload.traces[0].spans[0], RetrieverSpan)
    assert payload.traces[0].spans[0].input == "prompt"
    assert payload.traces[0].spans[0].output == [
        Document(content="response1", metadata=None),
        Document(content="response2", metadata=None),
    ]


@patch("galileo.logger.LogStreams")
@patch("galileo.logger.Projects")
@patch("galileo.logger.GalileoCoreApiClient")
def test_retriever_span_dict_output(
    mock_core_api_client: Mock, mock_projects_client: Mock, mock_logstreams_client: Mock
) -> None:
    mock_core_api_instance = setup_mock_core_api_client(mock_core_api_client)
    setup_mock_projects_client(mock_projects_client)
    setup_mock_logstreams_client(mock_logstreams_client)

    created_at = datetime.datetime.now()
    logger = GalileoLogger(project="my_project", log_stream="my_log_stream")
    logger.start_trace(input="input", name="test-trace", created_at=created_at)
    logger.add_retriever_span(
        input="prompt", output={"response1": "response2"}, name="test-span", created_at=created_at, status_code=200
    )
    logger.add_retriever_span(
        input="prompt",
        output={"content": "response2", "metadata": {"key": "value"}},
        name="test-span",
        created_at=created_at,
        status_code=200,
    )
    logger.conclude("output", status_code=200)
    logger.flush()

    payload = mock_core_api_instance.ingest_traces_sync.call_args[0][0]

    assert isinstance(payload.traces[0].spans[0], RetrieverSpan)
    assert payload.traces[0].spans[0].input == "prompt"
    assert payload.traces[0].spans[0].output == [Document(content='{"response1": "response2"}', metadata=None)]
    assert payload.traces[0].spans[1].input == "prompt"
    assert payload.traces[0].spans[1].output == [Document(content="response2", metadata={"key": "value"})]


@patch("galileo.logger.LogStreams")
@patch("galileo.logger.Projects")
@patch("galileo.logger.GalileoCoreApiClient")
def test_retriever_span_list_dict_output(
    mock_core_api_client: Mock, mock_projects_client: Mock, mock_logstreams_client: Mock
) -> None:
    mock_core_api_instance = setup_mock_core_api_client(mock_core_api_client)
    setup_mock_projects_client(mock_projects_client)
    setup_mock_logstreams_client(mock_logstreams_client)

    created_at = datetime.datetime.now()
    logger = GalileoLogger(project="my_project", log_stream="my_log_stream")
    logger.start_trace(input="input", name="test-trace", created_at=created_at)
    logger.add_retriever_span(
        input="prompt", output=[{"response1": "response2"}], name="test-span", created_at=created_at, status_code=200
    )
    logger.add_retriever_span(
        input="prompt",
        output=[{"content": "response2", "metadata": {"key": "value"}}],
        name="test-span",
        created_at=created_at,
        status_code=200,
    )
    logger.add_retriever_span(
        input="prompt",
        output=[{"content": "response2", "metadata": {"key": "value"}}, {"response1": "response2"}],
        name="test-span",
        created_at=created_at,
        status_code=200,
    )
    logger.conclude("output", status_code=200)
    logger.flush()

    payload = mock_core_api_instance.ingest_traces_sync.call_args[0][0]

    assert isinstance(payload.traces[0].spans[0], RetrieverSpan)
    assert payload.traces[0].spans[0].input == "prompt"
    assert payload.traces[0].spans[0].output == [Document(content='{"response1": "response2"}', metadata=None)]
    assert payload.traces[0].spans[1].input == "prompt"
    assert payload.traces[0].spans[1].output == [Document(content="response2", metadata={"key": "value"})]
    assert payload.traces[0].spans[2].input == "prompt"
    assert payload.traces[0].spans[2].output == [
        Document(content='{"content": "response2", "metadata": {"key": "value"}}', metadata=None),
        Document(content='{"response1": "response2"}', metadata=None),
    ]


@patch("galileo.logger.LogStreams")
@patch("galileo.logger.Projects")
@patch("galileo.logger.GalileoCoreApiClient")
def test_retriever_span_document_output(
    mock_core_api_client: Mock, mock_projects_client: Mock, mock_logstreams_client: Mock
) -> None:
    mock_core_api_instance = setup_mock_core_api_client(mock_core_api_client)
    setup_mock_projects_client(mock_projects_client)
    setup_mock_logstreams_client(mock_logstreams_client)

    created_at = datetime.datetime.now()
    logger = GalileoLogger(project="my_project", log_stream="my_log_stream")
    logger.start_trace(input="input", name="test-trace", created_at=created_at)
    logger.add_retriever_span(
        input="prompt",
        output=Document(content="response", metadata={"key": "value"}),
        name="test-span",
        created_at=created_at,
        status_code=200,
    )
    logger.conclude("output", status_code=200)
    logger.flush()

    payload = mock_core_api_instance.ingest_traces_sync.call_args[0][0]

    assert isinstance(payload.traces[0].spans[0], RetrieverSpan)
    assert payload.traces[0].spans[0].input == "prompt"
    assert payload.traces[0].spans[0].output == [Document(content="response", metadata={"key": "value"})]


@patch("galileo.logger.LogStreams")
@patch("galileo.logger.Projects")
@patch("galileo.logger.GalileoCoreApiClient")
def test_retriever_span_list_document_output(
    mock_core_api_client: Mock, mock_projects_client: Mock, mock_logstreams_client: Mock
) -> None:
    mock_core_api_instance = setup_mock_core_api_client(mock_core_api_client)
    setup_mock_projects_client(mock_projects_client)
    setup_mock_logstreams_client(mock_logstreams_client)

    created_at = datetime.datetime.now()
    logger = GalileoLogger(project="my_project", log_stream="my_log_stream")
    logger.start_trace(input="input", name="test-trace", created_at=created_at)
    logger.add_retriever_span(
        input="prompt",
        output=[Document(content="response1", metadata={"key": "value"}), Document(content="response2", metadata={})],
        name="test-span",
        created_at=created_at,
        status_code=200,
    )
    logger.conclude("output", status_code=200)
    logger.flush()

    payload = mock_core_api_instance.ingest_traces_sync.call_args[0][0]

    assert isinstance(payload.traces[0].spans[0], RetrieverSpan)
    assert payload.traces[0].spans[0].input == "prompt"
    assert payload.traces[0].spans[0].output == [
        Document(content="response1", metadata={"key": "value"}),
        Document(content="response2", metadata={}),
    ]


@patch("galileo.logger.LogStreams")
@patch("galileo.logger.Projects")
@patch("galileo.logger.GalileoCoreApiClient")
def test_retriever_span_none_output(
    mock_core_api_client: Mock, mock_projects_client: Mock, mock_logstreams_client: Mock
) -> None:
    mock_core_api_instance = setup_mock_core_api_client(mock_core_api_client)
    setup_mock_projects_client(mock_projects_client)
    setup_mock_logstreams_client(mock_logstreams_client)

    created_at = datetime.datetime.now()
    logger = GalileoLogger(project="my_project", log_stream="my_log_stream")
    logger.start_trace(input="input", name="test-trace", created_at=created_at)
    logger.add_retriever_span(input="prompt", output=None, name="test-span", created_at=created_at, status_code=200)
    logger.conclude("output", status_code=200)
    logger.flush()

    payload = mock_core_api_instance.ingest_traces_sync.call_args[0][0]

    assert isinstance(payload.traces[0].spans[0], RetrieverSpan)
    assert payload.traces[0].spans[0].input == "prompt"
    assert payload.traces[0].spans[0].output == [Document(content="", metadata={})]


@patch("galileo.logger.LogStreams")
@patch("galileo.logger.Projects")
@patch("galileo.logger.GalileoCoreApiClient")
def test_conclude_all_spans(
    mock_core_api_client: Mock, mock_projects_client: Mock, mock_logstreams_client: Mock
) -> None:
    setup_mock_core_api_client(mock_core_api_client)
    setup_mock_projects_client(mock_projects_client)
    setup_mock_logstreams_client(mock_logstreams_client)

    created_at = datetime.datetime.now()
    metadata = {"key": "value"}
    logger = GalileoLogger(project="my_project", log_stream="my_log_stream")
    logger.start_trace(
        input="input", name="test-trace", duration_ns=1_000_000, created_at=created_at, metadata=metadata
    )
    logger.add_workflow_span(input="prompt", name="test-workflow-span", created_at=created_at, metadata=metadata)

    logger.add_llm_span(
        input="prompt",
        output="response",
        model="gpt4o",
        name="test-span",
        tools=[{"name": "tool1", "args": {"arg1": "val1"}}],
        duration_ns=1_000_000,
        created_at=created_at,
        metadata=metadata,
        temperature=1.0,
        status_code=200,
    )

    logger.conclude(output="response", duration_ns=1_000_000, status_code=200, conclude_all=True)

    assert len(logger.traces) == 1
    assert len(logger.traces[0].spans) == 1
    assert len(logger.traces[0].spans[0].spans) == 1
    assert logger.traces[0].output == "response"
    assert logger.traces[0].spans[0].output == "response"
    assert logger._parent_stack == deque()


@patch("galileo.logger.LogStreams")
@patch("galileo.logger.Projects")
@patch("galileo.logger.GalileoCoreApiClient")
def test_flush_with_conclude_all_spans(
    mock_core_api_client: Mock, mock_projects_client: Mock, mock_logstreams_client: Mock
) -> None:
    mock_core_api_instance = setup_mock_core_api_client(mock_core_api_client)
    setup_mock_projects_client(mock_projects_client)
    setup_mock_logstreams_client(mock_logstreams_client)

    created_at = datetime.datetime.now()
    metadata = {"key": "value"}
    logger = GalileoLogger(project="my_project", log_stream="my_log_stream")
    logger.start_trace(
        input="input", name="test-trace", duration_ns=1_000_000, created_at=created_at, metadata=metadata
    )
    logger.add_workflow_span(input="prompt", name="test-workflow-span", created_at=created_at, metadata=metadata)

    logger.add_llm_span(
        input="prompt",
        output="response",
        model="gpt4o",
        name="test-span",
        tools=[{"name": "tool1", "args": {"arg1": "val1"}}],
        duration_ns=1_000_000,
        created_at=created_at,
        metadata=metadata,
        temperature=1.0,
        status_code=200,
    )

    logger.flush()

    payload = mock_core_api_instance.ingest_traces_sync.call_args[0][0]

    assert len(payload.traces) == 1
    assert len(payload.traces[0].spans) == 1
    assert len(payload.traces[0].spans[0].spans) == 1
    assert payload.traces[0].output is None
    assert payload.traces[0].spans[0].output is None

    assert logger.traces == []
    assert logger._parent_stack == deque()


@patch("galileo.logger.Projects.get")
@patch("galileo.projects.create_project_projects_post")
@patch("galileo.logger.GalileoCoreApiClient")
def test_galileo_logger_failed_creating_project(
    mock_core_api_client: Mock, galileo_resources_api_projects: Mock, mock_projects_get: Mock, caplog
) -> None:
    mock_instance = mock_core_api_client.return_value

    mock_instance.get_project_by_name = AsyncMock(return_value={"id": UUID("6c4e3f7e-4a9a-4e7e-8c1f-3a9a3a9a3a9a")})
    mock_instance.get_log_stream_by_name = AsyncMock(return_value={"id": UUID("6c4e3f7e-4a9a-4e7e-8c1f-3a9a3a9a3a9b")})

    # galileo_resources_api_projects.= MagicMock()
    galileo_resources_api_projects.sync = Mock(side_effect=ValueError("Unable to create project"))
    mock_projects_get.return_value = None

    with caplog.at_level(logging.WARNING):
        GalileoLogger()
        assert "Unable to create project" in caplog.text
