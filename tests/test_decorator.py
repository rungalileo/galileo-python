from unittest.mock import Mock, patch

import pytest

from galileo import galileo_context, log
from galileo_core.schemas.logging.llm import Message, MessageRole
from galileo_core.schemas.logging.span import LlmSpan, RetrieverSpan, WorkflowSpan
from galileo_core.schemas.shared.document import Document
from tests.testutils.setup import setup_mock_core_api_client, setup_mock_logstreams_client, setup_mock_projects_client


@pytest.fixture
def reset_context():
    galileo_context.reset()


@patch("galileo.logger.LogStreams")
@patch("galileo.logger.Projects")
@patch("galileo.logger.GalileoCoreApiClient")
def test_decorator_context_reset(
    mock_core_api_client: Mock, mock_projects_client: Mock, mock_logstreams_client: Mock, reset_context
) -> None:
    setup_mock_core_api_client(mock_core_api_client)
    setup_mock_projects_client(mock_projects_client)
    setup_mock_logstreams_client(mock_logstreams_client)

    @log(span_type="llm")
    def llm_call(query: str):
        return "response"

    assert galileo_context.get_current_trace() is None

    llm_call(query="input")

    assert len(galileo_context.get_logger_instance().traces) == 1
    assert galileo_context.get_current_trace() is not None

    galileo_context.reset()

    assert len(galileo_context.get_logger_instance().traces) == 0
    assert galileo_context.get_current_trace() is None


@patch("galileo.logger.LogStreams")
@patch("galileo.logger.Projects")
@patch("galileo.logger.GalileoCoreApiClient")
def test_decorator_context_init(
    mock_core_api_client: Mock, mock_projects_client: Mock, mock_logstreams_client: Mock, reset_context
) -> None:
    setup_mock_core_api_client(mock_core_api_client)
    setup_mock_projects_client(mock_projects_client)
    setup_mock_logstreams_client(mock_logstreams_client)

    galileo_context.init(project="project-X", log_stream="log-stream-X")

    assert galileo_context.get_current_project() == "project-X"
    assert galileo_context.get_current_log_stream() == "log-stream-X"

    galileo_context.reset()

    assert galileo_context.get_current_project() is None
    assert galileo_context.get_current_log_stream() is None


@patch("galileo.logger.LogStreams")
@patch("galileo.logger.Projects")
@patch("galileo.logger.GalileoCoreApiClient")
def test_decorator_context_flush(
    mock_core_api_client: Mock, mock_projects_client: Mock, mock_logstreams_client: Mock, reset_context
) -> None:
    mock_core_api_instance = setup_mock_core_api_client(mock_core_api_client)
    setup_mock_projects_client(mock_projects_client)
    setup_mock_logstreams_client(mock_logstreams_client)

    @log(span_type="llm")
    def llm_call(query: str):
        return "response"

    assert galileo_context.get_current_trace() is None

    llm_call(query="input")

    assert galileo_context.get_current_trace() is not None

    galileo_context.flush()

    payload = mock_core_api_instance.ingest_traces_sync.call_args[0][0]

    assert len(payload.traces) == 1
    assert len(payload.traces[0].spans) == 1


@patch("galileo.logger.LogStreams")
@patch("galileo.logger.Projects")
@patch("galileo.logger.GalileoCoreApiClient")
def test_decorator_context_flush_all(
    mock_core_api_client: Mock, mock_projects_client: Mock, mock_logstreams_client: Mock, reset_context
) -> None:
    setup_mock_core_api_client(mock_core_api_client)
    setup_mock_projects_client(mock_projects_client)
    setup_mock_logstreams_client(mock_logstreams_client)

    @log(span_type="llm")
    def llm_call(query: str):
        return "response"

    galileo_context.init(project="project-X", log_stream="log-stream-X")

    llm_call(query="input_X")

    trace_X = galileo_context.get_current_trace()
    assert trace_X.input == '{"query": "input_X"}'

    logger_X = galileo_context.get_logger_instance(project="project-X", log_stream="log-stream-X")
    assert len(logger_X.traces) == 1

    galileo_context.init(project="project-Y", log_stream="log-stream-Y")

    llm_call(query="input_Y")

    trace_Y = galileo_context.get_current_trace()
    assert trace_Y.input == '{"query": "input_Y"}'

    logger_Y = galileo_context.get_logger_instance(project="project-Y", log_stream="log-stream-Y")
    assert len(logger_Y.traces) == 1

    # Flush both loggers
    galileo_context.flush_all()

    logger_X = galileo_context.get_logger_instance(project="project-X", log_stream="log-stream-X")
    assert len(logger_X.traces) == 0

    logger_Y = galileo_context.get_logger_instance(project="project-Y", log_stream="log-stream-Y")
    assert len(logger_Y.traces) == 0


@patch("galileo.logger.LogStreams")
@patch("galileo.logger.Projects")
@patch("galileo.logger.GalileoCoreApiClient")
def test_decorator_llm_span(
    mock_core_api_client: Mock, mock_projects_client: Mock, mock_logstreams_client: Mock, reset_context
) -> None:
    mock_core_api_instance = setup_mock_core_api_client(mock_core_api_client)
    setup_mock_projects_client(mock_projects_client)
    setup_mock_logstreams_client(mock_logstreams_client)

    @log(span_type="llm")
    def llm_call(query: str):
        return "response"

    llm_call(query="input")
    galileo_context.flush()

    payload = mock_core_api_instance.ingest_traces_sync.call_args[0][0]

    assert len(payload.traces) == 1
    assert len(payload.traces[0].spans) == 1
    assert isinstance(payload.traces[0].spans[0], LlmSpan)
    assert payload.traces[0].input == '{"query": "input"}'
    assert payload.traces[0].spans[0].input == [Message(content='{"query": "input"}', role=MessageRole.user)]
    assert payload.traces[0].spans[0].output == Message(content="response", role=MessageRole.assistant)


@patch("galileo.logger.LogStreams")
@patch("galileo.logger.Projects")
@patch("galileo.logger.GalileoCoreApiClient")
def test_decorator_nested_span(
    mock_core_api_client: Mock, mock_projects_client: Mock, mock_logstreams_client: Mock, reset_context
) -> None:
    mock_core_api_instance = setup_mock_core_api_client(mock_core_api_client)
    setup_mock_projects_client(mock_projects_client)
    setup_mock_logstreams_client(mock_logstreams_client)

    @log(span_type="llm")
    def llm_call(query: str):
        return "response"

    @log()
    def nested_call(nested_query: str):
        return llm_call(query=nested_query)

    output = nested_call(nested_query="input")
    galileo_context.flush()

    payload = mock_core_api_instance.ingest_traces_sync.call_args[0][0]

    assert len(payload.traces) == 1
    assert len(payload.traces[0].spans) == 1
    assert len(payload.traces[0].spans[0].spans) == 1
    assert isinstance(payload.traces[0].spans[0], WorkflowSpan)
    assert isinstance(payload.traces[0].spans[0].spans[0], LlmSpan)
    assert payload.traces[0].input == '{"nested_query": "input"}'
    assert payload.traces[0].spans[0].output == output
    assert payload.traces[0].spans[0].spans[0].input == [Message(content='{"query": "input"}', role=MessageRole.user)]
    assert payload.traces[0].spans[0].spans[0].output == Message(content="response", role=MessageRole.assistant)


@patch("galileo.logger.LogStreams")
@patch("galileo.logger.Projects")
@patch("galileo.logger.GalileoCoreApiClient")
def test_decorator_multiple_nested_spans(
    mock_core_api_client: Mock, mock_projects_client: Mock, mock_logstreams_client: Mock, reset_context
) -> None:
    mock_core_api_instance = setup_mock_core_api_client(mock_core_api_client)
    setup_mock_projects_client(mock_projects_client)
    setup_mock_logstreams_client(mock_logstreams_client)

    @log(span_type="llm")
    def llm_call(query: str):
        return "response"

    @log()
    def nested_call(nested_query: str):
        llm_call(query=nested_query)
        llm_call(query=nested_query)
        return "new response"

    output = nested_call(nested_query="input")
    galileo_context.flush()

    payload = mock_core_api_instance.ingest_traces_sync.call_args[0][0]

    assert len(payload.traces) == 1
    assert len(payload.traces[0].spans) == 1
    assert len(payload.traces[0].spans[0].spans) == 2
    assert isinstance(payload.traces[0].spans[0], WorkflowSpan)
    assert isinstance(payload.traces[0].spans[0].spans[0], LlmSpan)
    assert isinstance(payload.traces[0].spans[0].spans[1], LlmSpan)
    assert payload.traces[0].input == '{"nested_query": "input"}'
    assert payload.traces[0].spans[0].input == '{"nested_query": "input"}'
    assert payload.traces[0].spans[0].output == output
    assert payload.traces[0].spans[0].spans[0].input == [Message(content='{"query": "input"}', role=MessageRole.user)]
    assert payload.traces[0].spans[0].spans[0].output == Message(content="response", role=MessageRole.assistant)


@patch("galileo.logger.LogStreams")
@patch("galileo.logger.Projects")
@patch("galileo.logger.GalileoCoreApiClient")
def test_decorator_retriever_span_str(
    mock_core_api_client: Mock, mock_projects_client: Mock, mock_logstreams_client: Mock, reset_context
) -> None:
    mock_core_api_instance = setup_mock_core_api_client(mock_core_api_client)
    setup_mock_projects_client(mock_projects_client)
    setup_mock_logstreams_client(mock_logstreams_client)

    @log(span_type="retriever")
    def retriever_call(query: str):
        return "response1"

    retriever_call(query="input")
    galileo_context.flush()

    payload = mock_core_api_instance.ingest_traces_sync.call_args[0][0]

    assert isinstance(payload.traces[0].spans[0], RetrieverSpan)
    assert payload.traces[0].spans[0].input == '{"query": "input"}'
    assert payload.traces[0].spans[0].output == [Document(content="response1", metadata=None)]


@patch("galileo.logger.LogStreams")
@patch("galileo.logger.Projects")
@patch("galileo.logger.GalileoCoreApiClient")
def test_decorator_retriever_span_list_str(
    mock_core_api_client: Mock, mock_projects_client: Mock, mock_logstreams_client: Mock, reset_context
) -> None:
    mock_core_api_instance = setup_mock_core_api_client(mock_core_api_client)
    setup_mock_projects_client(mock_projects_client)
    setup_mock_logstreams_client(mock_logstreams_client)

    @log(span_type="retriever")
    def retriever_call(query: str):
        return ["response1", "response2"]

    retriever_call(query="input")
    galileo_context.flush()

    payload = mock_core_api_instance.ingest_traces_sync.call_args[0][0]

    assert isinstance(payload.traces[0].spans[0], RetrieverSpan)
    assert payload.traces[0].spans[0].input == '{"query": "input"}'
    assert payload.traces[0].spans[0].output == [
        Document(content="response1", metadata=None),
        Document(content="response2", metadata=None),
    ]


@patch("galileo.logger.LogStreams")
@patch("galileo.logger.Projects")
@patch("galileo.logger.GalileoCoreApiClient")
def test_decorator_retriever_span_list_dict(
    mock_core_api_client: Mock, mock_projects_client: Mock, mock_logstreams_client: Mock, reset_context
) -> None:
    mock_core_api_instance = setup_mock_core_api_client(mock_core_api_client)
    setup_mock_projects_client(mock_projects_client)
    setup_mock_logstreams_client(mock_logstreams_client)

    @log(span_type="retriever")
    def retriever_call(query: str):
        return [{"content": "response1", "metadata": {"key": "value"}}, {"content": "response2", "metadata": None}]

    retriever_call(query="input")
    galileo_context.flush()

    payload = mock_core_api_instance.ingest_traces_sync.call_args[0][0]

    assert isinstance(payload.traces[0].spans[0], RetrieverSpan)
    assert payload.traces[0].spans[0].input == '{"query": "input"}'
    assert payload.traces[0].spans[0].output == [
        Document(content="response1", metadata={"key": "value"}),
        Document(content="response2", metadata=None),
    ]


@patch("galileo.logger.LogStreams")
@patch("galileo.logger.Projects")
@patch("galileo.logger.GalileoCoreApiClient")
def test_decorator_retriever_span_list_document(
    mock_core_api_client: Mock, mock_projects_client: Mock, mock_logstreams_client: Mock, reset_context
) -> None:
    mock_core_api_instance = setup_mock_core_api_client(mock_core_api_client)
    setup_mock_projects_client(mock_projects_client)
    setup_mock_logstreams_client(mock_logstreams_client)

    @log(span_type="retriever")
    def retriever_call(query: str):
        return [Document(content="response1", metadata={"key": "value"}), Document(content="response2", metadata=None)]

    retriever_call(query="input")
    galileo_context.flush()

    payload = mock_core_api_instance.ingest_traces_sync.call_args[0][0]

    assert isinstance(payload.traces[0].spans[0], RetrieverSpan)
    assert payload.traces[0].spans[0].input == '{"query": "input"}'
    assert payload.traces[0].spans[0].output == [
        Document(content="response1", metadata={"key": "value"}),
        Document(content="response2", metadata=None),
    ]
