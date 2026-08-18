import asyncio
from typing import NoReturn
from unittest.mock import Mock, patch
from uuid import UUID

import pytest
from pydantic import BaseModel

from galileo import Message, MessageRole, galileo_context, log, start_session
from galileo.decorator import _session_id_context
from galileo.schema.content_blocks import DataContentBlock, TextContentBlock
from galileo_core.schemas.logging.span import AgentSpan, LlmSpan, RetrieverSpan, ToolSpan, WorkflowSpan
from galileo_core.schemas.shared.document import Document
from galileo_core.schemas.shared.multimodal import ContentModality
from tests.testutils.setup import setup_mock_logstreams_client, setup_mock_projects_client, setup_mock_traces_client


@pytest.fixture
def reset_context():
    galileo_context.reset()
    yield
    galileo_context.reset()


@patch("galileo.logger.logger.LogStreams")
@patch("galileo.logger.logger.Projects")
@patch("galileo.logger.logger.Traces")
def test_decorator_context_reset(
    mock_traces_client: Mock, mock_projects_client: Mock, mock_logstreams_client: Mock, reset_context
) -> None:
    setup_mock_traces_client(mock_traces_client)
    setup_mock_projects_client(mock_projects_client)
    setup_mock_logstreams_client(mock_logstreams_client)

    galileo_context.init(project="project-X", log_stream="log-stream-X")

    @log(span_type="llm")
    def llm_call(query: str) -> str:
        return "response"

    assert galileo_context.get_current_trace() is None

    llm_call(query="input")

    assert len(galileo_context.get_logger_instance().traces) == 1
    assert galileo_context.get_current_trace() is not None
    assert galileo_context.get_current_project() == "project-X"
    assert galileo_context.get_current_log_stream() == "log-stream-X"

    galileo_context.reset()

    assert len(galileo_context.get_logger_instance().traces) == 0
    assert galileo_context.get_current_trace() is None
    assert galileo_context.get_current_project() is None
    assert galileo_context.get_current_log_stream() is None


@patch("galileo.logger.logger.LogStreams")
@patch("galileo.logger.logger.Projects")
@patch("galileo.logger.logger.Traces")
def test_decorator_context_init(
    mock_traces_client: Mock, mock_projects_client: Mock, mock_logstreams_client: Mock, reset_context
) -> None:
    setup_mock_traces_client(mock_traces_client)
    setup_mock_projects_client(mock_projects_client)
    setup_mock_logstreams_client(mock_logstreams_client)

    galileo_context.init(project="project-X", log_stream="log-stream-X")

    assert galileo_context.get_current_project() == "project-X"
    assert galileo_context.get_current_log_stream() == "log-stream-X"

    galileo_context.reset()

    assert galileo_context.get_current_project() is None
    assert galileo_context.get_current_log_stream() is None


@patch("galileo.logger.logger.LogStreams")
@patch("galileo.logger.logger.Projects")
@patch("galileo.logger.logger.Traces")
def test_decorator_context_flush(
    mock_traces_client: Mock, mock_projects_client: Mock, mock_logstreams_client: Mock, reset_context
) -> None:
    mock_traces_client_instance = setup_mock_traces_client(mock_traces_client)
    setup_mock_projects_client(mock_projects_client)
    setup_mock_logstreams_client(mock_logstreams_client)

    @log(span_type="llm")
    def llm_call(query: str) -> str:
        return "response"

    assert galileo_context.get_current_trace() is None

    llm_call(query="input")

    assert galileo_context.get_current_trace() is not None

    galileo_context.flush()

    # Check if ingest_traces (async) was called instead of ingest_traces
    if mock_traces_client_instance.ingest_traces.call_args is not None:
        payload = mock_traces_client_instance.ingest_traces.call_args[0][0]
    else:
        payload = mock_traces_client_instance.ingest_traces.call_args[0][0]

    assert len(payload.traces) == 1
    assert len(payload.traces[0].spans) == 1
    assert galileo_context.get_current_trace() is None
    assert galileo_context.get_current_span_stack() == []


@patch("galileo.logger.logger.LogStreams")
@patch("galileo.logger.logger.Projects")
@patch("galileo.logger.logger.Traces")
def test_decorator_context_flush_specific_project_and_log_stream(
    mock_traces_client: Mock, mock_projects_client: Mock, mock_logstreams_client: Mock, reset_context
) -> None:
    mock_traces_client_instance = setup_mock_traces_client(mock_traces_client)
    setup_mock_projects_client(mock_projects_client)
    setup_mock_logstreams_client(mock_logstreams_client)

    galileo_context.init(project="project-X", log_stream="log-stream-X")

    @log(span_type="llm")
    def llm_call(query: str) -> str:
        return "response"

    assert galileo_context.get_current_trace() is None

    llm_call(query="input")

    assert galileo_context.get_current_trace() is not None

    galileo_context.init(project="project-Y", log_stream="log-stream-Y")

    assert galileo_context.get_current_trace() is None

    llm_call(query="input")

    assert galileo_context.get_current_trace() is not None

    galileo_context.flush(project="project-X", log_stream="log-stream-X")

    payload = mock_traces_client_instance.ingest_traces.call_args[0][0]

    assert len(payload.traces) == 1
    assert len(payload.traces[0].spans) == 1

    assert galileo_context.get_current_trace() is not None

    galileo_context.flush(project="project-Y", log_stream="log-stream-Y")

    payload = mock_traces_client_instance.ingest_traces.call_args[0][0]

    assert len(payload.traces) == 1
    assert len(payload.traces[0].spans) == 1

    assert galileo_context.get_current_trace() is None


@patch("galileo.logger.logger.LogStreams")
@patch("galileo.logger.logger.Projects")
@patch("galileo.logger.logger.Traces")
def test_decorator_context_flush_all(
    mock_traces_client: Mock, mock_projects_client: Mock, mock_logstreams_client: Mock, reset_context
) -> None:
    setup_mock_traces_client(mock_traces_client)
    setup_mock_projects_client(mock_projects_client)
    setup_mock_logstreams_client(mock_logstreams_client)

    @log(span_type="llm")
    def llm_call(query: str) -> str:
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

    assert galileo_context.get_current_trace() is None
    assert galileo_context.get_current_span_stack() == []


@patch("galileo.logger.logger.LogStreams")
@patch("galileo.logger.logger.Projects")
@patch("galileo.logger.logger.Traces")
def test_decorator_llm_span(
    mock_traces_client: Mock, mock_projects_client: Mock, mock_logstreams_client: Mock, reset_context
) -> None:
    mock_traces_client_instance = setup_mock_traces_client(mock_traces_client)
    setup_mock_projects_client(mock_projects_client)
    setup_mock_logstreams_client(mock_logstreams_client)

    @log(span_type="llm")
    def llm_call(query: str) -> str:
        return "response"

    llm_call(query="input")
    galileo_context.flush()

    payload = mock_traces_client_instance.ingest_traces.call_args[0][0]

    assert len(payload.traces) == 1
    assert len(payload.traces[0].spans) == 1
    assert isinstance(payload.traces[0].spans[0], LlmSpan)
    assert payload.traces[0].input == '{"query": "input"}'
    assert payload.traces[0].spans[0].input == [Message(content='{"query": "input"}', role=MessageRole.user)]
    assert payload.traces[0].spans[0].output == Message(content="response", role=MessageRole.assistant)


@patch("galileo.logger.logger.LogStreams")
@patch("galileo.logger.logger.Projects")
@patch("galileo.logger.logger.Traces")
def test_decorator_workflow_span_output_int(
    mock_traces_client: Mock, mock_projects_client: Mock, mock_logstreams_client: Mock, reset_context
) -> None:
    mock_traces_client_instance = setup_mock_traces_client(mock_traces_client)
    setup_mock_projects_client(mock_projects_client)
    setup_mock_logstreams_client(mock_logstreams_client)

    @log(span_type="workflow")
    def my_function(arg1, arg2):
        return arg1 + arg2

    my_function(1, 2)
    galileo_context.flush()

    payload = mock_traces_client_instance.ingest_traces.call_args[0][0]

    assert len(payload.traces) == 1
    assert len(payload.traces[0].spans) == 1
    assert isinstance(payload.traces[0].spans[0], WorkflowSpan)
    assert payload.traces[0].input == '{"arg1": 1, "arg2": 2}'
    assert payload.traces[0].spans[0].input == '{"arg1": 1, "arg2": 2}'
    assert payload.traces[0].spans[0].output == "3"


@patch("galileo.logger.logger.LogStreams")
@patch("galileo.logger.logger.Projects")
@patch("galileo.logger.logger.Traces")
def test_decorator_workflow_span_io_object(
    mock_traces_client: Mock, mock_projects_client: Mock, mock_logstreams_client: Mock, reset_context
) -> None:
    mock_traces_client_instance = setup_mock_traces_client(mock_traces_client)
    setup_mock_projects_client(mock_projects_client)
    setup_mock_logstreams_client(mock_logstreams_client)

    @log(span_type="workflow")
    def my_function(system: Message, user: Message):
        return Document(content="response", metadata={"arg1": "val1", "arg2": "val2"})

    my_function(
        Message(content="system prompt", role=MessageRole.system), Message(content="query", role=MessageRole.user)
    )
    galileo_context.flush()

    payload = mock_traces_client_instance.ingest_traces.call_args[0][0]

    assert len(payload.traces) == 1
    assert len(payload.traces[0].spans) == 1
    assert isinstance(payload.traces[0].spans[0], WorkflowSpan)
    assert (
        payload.traces[0].input
        == '{"system": {"content": "system prompt", "role": "system"}, "user": {"content": "query", "role": "user"}}'
    )
    assert (
        payload.traces[0].spans[0].input
        == '{"system": {"content": "system prompt", "role": "system"}, "user": {"content": "query", "role": "user"}}'
    )
    assert payload.traces[0].spans[0].output == '{"content": "response", "metadata": {"arg1": "val1", "arg2": "val2"}}'


@patch("galileo.logger.logger.LogStreams")
@patch("galileo.logger.logger.Projects")
@patch("galileo.logger.logger.Traces")
def test_decorator_tool_span_io_object(
    mock_traces_client: Mock, mock_projects_client: Mock, mock_logstreams_client: Mock, reset_context
) -> None:
    mock_traces_client_instance = setup_mock_traces_client(mock_traces_client)
    setup_mock_projects_client(mock_projects_client)
    setup_mock_logstreams_client(mock_logstreams_client)

    @log(span_type="tool")
    def my_function(system: Message, user: Message):
        return Document(content="response", metadata={"arg1": "val1", "arg2": "val2"})

    my_function(
        Message(content="system prompt", role=MessageRole.system), Message(content="query", role=MessageRole.user)
    )
    galileo_context.flush()

    payload = mock_traces_client_instance.ingest_traces.call_args[0][0]

    assert len(payload.traces) == 1
    assert len(payload.traces[0].spans) == 1
    assert isinstance(payload.traces[0].spans[0], ToolSpan)
    assert (
        payload.traces[0].input
        == '{"system": {"content": "system prompt", "role": "system"}, "user": {"content": "query", "role": "user"}}'
    )
    assert (
        payload.traces[0].spans[0].input
        == '{"system": {"content": "system prompt", "role": "system"}, "user": {"content": "query", "role": "user"}}'
    )
    assert payload.traces[0].spans[0].output == '{"content": "response", "metadata": {"arg1": "val1", "arg2": "val2"}}'


@patch("galileo.logger.logger.LogStreams")
@patch("galileo.logger.logger.Projects")
@patch("galileo.logger.logger.Traces")
def test_decorator_agent_span(
    mock_traces_client: Mock, mock_projects_client: Mock, mock_logstreams_client: Mock, reset_context
) -> None:
    mock_traces_client_instance = setup_mock_traces_client(mock_traces_client)
    setup_mock_projects_client(mock_projects_client)
    setup_mock_logstreams_client(mock_logstreams_client)

    @log(span_type="agent")
    def my_function(arg1: str, arg2: str) -> str:
        return f"{arg1} {arg2}"

    my_function("arg1", "arg2")
    galileo_context.flush()

    payload = mock_traces_client_instance.ingest_traces.call_args[0][0]

    assert len(payload.traces) == 1
    assert len(payload.traces[0].spans) == 1
    assert isinstance(payload.traces[0].spans[0], AgentSpan)
    assert payload.traces[0].input == '{"arg1": "arg1", "arg2": "arg2"}'
    assert payload.traces[0].spans[0].input == '{"arg1": "arg1", "arg2": "arg2"}'
    assert payload.traces[0].spans[0].output == "arg1 arg2"


@patch("galileo.logger.logger.LogStreams")
@patch("galileo.logger.logger.Projects")
@patch("galileo.logger.logger.Traces")
def test_decorator_agent_span_with_agent_type(
    mock_traces_client: Mock, mock_projects_client: Mock, mock_logstreams_client: Mock, reset_context
) -> None:
    mock_traces_client_instance = setup_mock_traces_client(mock_traces_client)
    setup_mock_projects_client(mock_projects_client)
    setup_mock_logstreams_client(mock_logstreams_client)

    @log(span_type="agent", params={"agent_type": "planner"})
    def my_function(arg1: str, arg2: str) -> str:
        return f"{arg1} {arg2}"

    my_function("arg1", "arg2")
    galileo_context.flush()

    payload = mock_traces_client_instance.ingest_traces.call_args[0][0]

    assert len(payload.traces) == 1
    assert len(payload.traces[0].spans) == 1
    assert isinstance(payload.traces[0].spans[0], AgentSpan)
    assert payload.traces[0].input == '{"arg1": "arg1", "arg2": "arg2"}'
    assert payload.traces[0].spans[0].input == '{"arg1": "arg1", "arg2": "arg2"}'
    assert payload.traces[0].spans[0].output == "arg1 arg2"
    assert payload.traces[0].spans[0].agent_type == "planner"


@patch("galileo.logger.logger.LogStreams")
@patch("galileo.logger.logger.Projects")
@patch("galileo.logger.logger.Traces")
def test_decorator_agent_span_with_nested_span(
    mock_traces_client: Mock, mock_projects_client: Mock, mock_logstreams_client: Mock, reset_context
) -> None:
    mock_traces_client_instance = setup_mock_traces_client(mock_traces_client)
    setup_mock_projects_client(mock_projects_client)
    setup_mock_logstreams_client(mock_logstreams_client)

    @log(span_type="tool")
    def my_tool_function(arg1: str) -> str:
        return f"{arg1}"

    @log(span_type="agent", params={"agent_type": "planner"})
    def my_function(arg1: str, arg2: str):
        return my_tool_function(arg1)

    my_function("arg1", "arg2")
    galileo_context.flush()

    payload = mock_traces_client_instance.ingest_traces.call_args[0][0]

    assert len(payload.traces) == 1
    assert len(payload.traces[0].spans) == 1
    assert isinstance(payload.traces[0].spans[0], AgentSpan)
    assert isinstance(payload.traces[0].spans[0].spans[0], ToolSpan)
    assert payload.traces[0].input == '{"arg1": "arg1", "arg2": "arg2"}'
    assert payload.traces[0].spans[0].input == '{"arg1": "arg1", "arg2": "arg2"}'
    assert payload.traces[0].spans[0].output == "arg1"
    assert payload.traces[0].spans[0].agent_type == "planner"
    assert len(payload.traces[0].spans[0].spans) == 1
    assert isinstance(payload.traces[0].spans[0].spans[0], ToolSpan)
    assert payload.traces[0].spans[0].spans[0].input == '{"arg1": "arg1"}'
    assert payload.traces[0].spans[0].spans[0].output == "arg1"


@patch("galileo.logger.logger.LogStreams")
@patch("galileo.logger.logger.Projects")
@patch("galileo.logger.logger.Traces")
def test_decorator_nested_span(
    mock_traces_client: Mock, mock_projects_client: Mock, mock_logstreams_client: Mock, reset_context
) -> None:
    mock_traces_client_instance = setup_mock_traces_client(mock_traces_client)
    setup_mock_projects_client(mock_projects_client)
    setup_mock_logstreams_client(mock_logstreams_client)

    @log(span_type="llm")
    def llm_call(query: str) -> str:
        return "response"

    @log
    def nested_call(nested_query: str):
        return llm_call(query=nested_query)

    output = nested_call(nested_query="input")
    galileo_context.flush()

    payload = mock_traces_client_instance.ingest_traces.call_args[0][0]

    assert len(payload.traces) == 1
    assert len(payload.traces[0].spans) == 1
    assert len(payload.traces[0].spans[0].spans) == 1
    assert isinstance(payload.traces[0].spans[0], WorkflowSpan)
    assert isinstance(payload.traces[0].spans[0].spans[0], LlmSpan)
    assert payload.traces[0].input == '{"nested_query": "input"}'
    assert payload.traces[0].spans[0].input == '{"nested_query": "input"}'
    assert payload.traces[0].spans[0].output == output
    assert payload.traces[0].spans[0].spans[0].input == [Message(content='{"query": "input"}', role=MessageRole.user)]
    assert payload.traces[0].spans[0].spans[0].output == Message(content="response", role=MessageRole.assistant)


@patch("galileo.logger.logger.LogStreams")
@patch("galileo.logger.logger.Projects")
@patch("galileo.logger.logger.Traces")
def test_decorator_multiple_nested_spans(
    mock_traces_client: Mock, mock_projects_client: Mock, mock_logstreams_client: Mock, reset_context
) -> None:
    mock_traces_client_instance = setup_mock_traces_client(mock_traces_client)
    setup_mock_projects_client(mock_projects_client)
    setup_mock_logstreams_client(mock_logstreams_client)

    @log(span_type="llm")
    def llm_call(query: str) -> str:
        return "response"

    @log()
    def nested_call(nested_query: str) -> str:
        llm_call(query=nested_query)
        llm_call(query=nested_query)
        return "new response"

    output = nested_call(nested_query="input")
    galileo_context.flush()

    payload = mock_traces_client_instance.ingest_traces.call_args[0][0]

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


@patch("galileo.logger.logger.LogStreams")
@patch("galileo.logger.logger.Projects")
@patch("galileo.logger.logger.Traces")
def test_decorator_retriever_span_str(
    mock_traces_client: Mock, mock_projects_client: Mock, mock_logstreams_client: Mock, reset_context
) -> None:
    mock_traces_client_instance = setup_mock_traces_client(mock_traces_client)
    setup_mock_projects_client(mock_projects_client)
    setup_mock_logstreams_client(mock_logstreams_client)

    @log(span_type="retriever")
    def retriever_call(query: str) -> str:
        return "response1"

    retriever_call(query="input")
    galileo_context.flush()

    payload = mock_traces_client_instance.ingest_traces.call_args[0][0]

    assert isinstance(payload.traces[0].spans[0], RetrieverSpan)
    assert payload.traces[0].spans[0].input == '{"query": "input"}'
    assert payload.traces[0].spans[0].output == [Document(content="response1", metadata=None)]


@patch("galileo.logger.logger.LogStreams")
@patch("galileo.logger.logger.Projects")
@patch("galileo.logger.logger.Traces")
def test_decorator_retriever_span_list_str(
    mock_traces_client: Mock, mock_projects_client: Mock, mock_logstreams_client: Mock, reset_context
) -> None:
    mock_traces_client_instance = setup_mock_traces_client(mock_traces_client)
    setup_mock_projects_client(mock_projects_client)
    setup_mock_logstreams_client(mock_logstreams_client)

    @log(span_type="retriever")
    def retriever_call(query: str):
        return ["response1", "response2"]

    retriever_call(query="input")
    galileo_context.flush()

    payload = mock_traces_client_instance.ingest_traces.call_args[0][0]

    assert isinstance(payload.traces[0].spans[0], RetrieverSpan)
    assert payload.traces[0].spans[0].input == '{"query": "input"}'
    assert payload.traces[0].spans[0].output == [
        Document(content="response1", metadata=None),
        Document(content="response2", metadata=None),
    ]


@patch("galileo.logger.logger.LogStreams")
@patch("galileo.logger.logger.Projects")
@patch("galileo.logger.logger.Traces")
def test_decorator_retriever_span_list_dict(
    mock_traces_client: Mock, mock_projects_client: Mock, mock_logstreams_client: Mock, reset_context
) -> None:
    mock_traces_client_instance = setup_mock_traces_client(mock_traces_client)
    setup_mock_projects_client(mock_projects_client)
    setup_mock_logstreams_client(mock_logstreams_client)

    @log(span_type="retriever")
    def retriever_call(query: str):
        return [{"content": "response1", "metadata": {"key": "value"}}, {"content": "response2", "metadata": None}]

    retriever_call(query="input")
    galileo_context.flush()

    payload = mock_traces_client_instance.ingest_traces.call_args[0][0]

    assert isinstance(payload.traces[0].spans[0], RetrieverSpan)
    assert payload.traces[0].spans[0].input == '{"query": "input"}'
    assert payload.traces[0].spans[0].output == [
        Document(content="response1", metadata={"key": "value"}),
        Document(content="response2", metadata=None),
    ]


@patch("galileo.logger.logger.LogStreams")
@patch("galileo.logger.logger.Projects")
@patch("galileo.logger.logger.Traces")
def test_decorator_retriever_span_list_document(
    mock_traces_client: Mock, mock_projects_client: Mock, mock_logstreams_client: Mock, reset_context
) -> None:
    mock_traces_client_instance = setup_mock_traces_client(mock_traces_client)
    setup_mock_projects_client(mock_projects_client)
    setup_mock_logstreams_client(mock_logstreams_client)

    @log(span_type="retriever")
    def retriever_call(query: str):
        return [Document(content="response1", metadata={"key": "value"}), Document(content="response2", metadata=None)]

    retriever_call(query="input")
    galileo_context.flush()

    payload = mock_traces_client_instance.ingest_traces.call_args[0][0]

    assert isinstance(payload.traces[0].spans[0], RetrieverSpan)
    assert payload.traces[0].spans[0].input == '{"query": "input"}'
    assert payload.traces[0].spans[0].output == [
        Document(content="response1", metadata={"key": "value"}),
        Document(content="response2", metadata=None),
    ]


@patch("galileo.logger.logger.LogStreams")
@patch("galileo.logger.logger.Projects")
@patch("galileo.logger.logger.Traces")
def test_decorator_we_should_create_trace_but_reraise_exception(
    mock_traces_client: Mock, mock_projects_client: Mock, mock_logstreams_client: Mock, reset_context
) -> None:
    mock_traces_client_instance = setup_mock_traces_client(mock_traces_client)
    setup_mock_projects_client(mock_projects_client)
    setup_mock_logstreams_client(mock_logstreams_client)

    @log()
    def foo() -> NoReturn:
        raise Exception("i'm user exception")

    with pytest.raises(Exception):
        foo()

    galileo_context.flush()

    payload = mock_traces_client_instance.ingest_traces.call_args[0][0]

    assert len(payload.traces) == 1
    assert len(payload.traces[0].spans) == 1


@patch("galileo.logger.logger.LogStreams")
@patch("galileo.logger.logger.Projects")
@patch("galileo.logger.logger.Traces")
def test_decorator_start_session(
    mock_traces_client: Mock, mock_projects_client: Mock, mock_logstreams_client: Mock, reset_context
) -> None:
    mock_traces_client_instance = setup_mock_traces_client(mock_traces_client)
    setup_mock_projects_client(mock_projects_client)
    setup_mock_logstreams_client(mock_logstreams_client)

    @log()
    def foo() -> str:
        return "response"

    foo()
    galileo_context.start_session(
        name="test-session", previous_session_id="6c4e3f7e-4a9a-4e7e-8c1f-3a9a3a9a3a9e", external_id="test"
    )

    logger = galileo_context.get_logger_instance()
    assert logger.session_id == "6c4e3f7e-4a9a-4e7e-8c1f-3a9a3a9a3a9c"

    galileo_context.flush()

    payload = mock_traces_client_instance.ingest_traces.call_args[0][0]

    assert payload.session_id == UUID("6c4e3f7e-4a9a-4e7e-8c1f-3a9a3a9a3a9c")


@patch("galileo.logger.logger.LogStreams")
@patch("galileo.logger.logger.Projects")
@patch("galileo.logger.logger.Traces")
def test_standalone_start_session(
    mock_traces_client: Mock, mock_projects_client: Mock, mock_logstreams_client: Mock, reset_context
) -> None:
    """Test that the standalone start_session function works correctly."""
    mock_traces_client_instance = setup_mock_traces_client(mock_traces_client)
    setup_mock_projects_client(mock_projects_client)
    setup_mock_logstreams_client(mock_logstreams_client)

    @log()
    def foo() -> str:
        return "response"

    foo()
    session_id = start_session(
        name="test-session", previous_session_id="6c4e3f7e-4a9a-4e7e-8c1f-3a9a3a9a3a9e", external_id="test"
    )

    logger = galileo_context.get_logger_instance()
    assert logger.session_id == "6c4e3f7e-4a9a-4e7e-8c1f-3a9a3a9a3a9c"
    assert session_id == "6c4e3f7e-4a9a-4e7e-8c1f-3a9a3a9a3a9c"

    galileo_context.flush()

    payload = mock_traces_client_instance.ingest_traces.call_args[0][0]

    assert payload.session_id == UUID("6c4e3f7e-4a9a-4e7e-8c1f-3a9a3a9a3a9c")


@patch("galileo.logger.logger.LogStreams")
@patch("galileo.logger.logger.Projects")
@patch("galileo.logger.logger.Traces")
def test_decorator_start_session_empty_values(
    mock_traces_client: Mock, mock_projects_client: Mock, mock_logstreams_client: Mock, reset_context
) -> None:
    mock_traces_client_instance = setup_mock_traces_client(mock_traces_client)
    setup_mock_projects_client(mock_projects_client)
    setup_mock_logstreams_client(mock_logstreams_client)

    @log()
    def foo() -> str:
        return "response"

    foo()
    galileo_context.start_session()

    logger = galileo_context.get_logger_instance()
    assert logger.session_id == "6c4e3f7e-4a9a-4e7e-8c1f-3a9a3a9a3a9c"

    galileo_context.flush()

    payload = mock_traces_client_instance.ingest_traces.call_args[0][0]

    assert payload.session_id == UUID("6c4e3f7e-4a9a-4e7e-8c1f-3a9a3a9a3a9c")


@patch("galileo.logger.logger.LogStreams")
@patch("galileo.logger.logger.Projects")
@patch("galileo.logger.logger.Traces")
def test_decorator_clear_session(
    mock_traces_client: Mock, mock_projects_client: Mock, mock_logstreams_client: Mock, reset_context
) -> None:
    mock_traces_client_instance = setup_mock_traces_client(mock_traces_client)
    setup_mock_projects_client(mock_projects_client)
    setup_mock_logstreams_client(mock_logstreams_client)

    @log()
    def foo() -> str:
        return "response"

    foo()
    galileo_context.start_session(name="test-session")

    logger = galileo_context.get_logger_instance()
    assert logger.session_id == "6c4e3f7e-4a9a-4e7e-8c1f-3a9a3a9a3a9c"

    galileo_context.clear_session()

    assert logger.session_id is None

    galileo_context.flush()

    payload = mock_traces_client_instance.ingest_traces.call_args[0][0]

    assert payload.session_id is None


@patch("galileo.logger.logger.LogStreams")
@patch("galileo.logger.logger.Projects")
@patch("galileo.logger.logger.Traces")
def test_decorator_set_session(
    mock_traces_client: Mock, mock_projects_client: Mock, mock_logstreams_client: Mock, reset_context
) -> None:
    mock_traces_client_instance = setup_mock_traces_client(mock_traces_client)
    setup_mock_projects_client(mock_projects_client)
    setup_mock_logstreams_client(mock_logstreams_client)

    @log()
    def foo() -> str:
        return "response"

    foo()
    galileo_context.set_session(session_id="6c4e3f7e-4a9a-4e7e-8c1f-3a9a3a9a3a9c")

    logger = galileo_context.get_logger_instance()
    assert logger.session_id == "6c4e3f7e-4a9a-4e7e-8c1f-3a9a3a9a3a9c"

    galileo_context.flush()

    payload = mock_traces_client_instance.ingest_traces.call_args[0][0]

    assert payload.session_id == UUID("6c4e3f7e-4a9a-4e7e-8c1f-3a9a3a9a3a9c")


class TestPydanticModel(BaseModel):
    """Test Pydantic model for serialization tests."""

    name: str
    value: int
    optional_field: str = "default"


class ComplexPydanticModel(BaseModel):
    """More complex Pydantic model for testing."""

    simple_field: str
    nested_data: dict = {}
    items: list = []


@patch("galileo.logger.logger.LogStreams")
@patch("galileo.logger.logger.Projects")
@patch("galileo.logger.logger.Traces")
def test_decorator_input_serialization_deserialization(
    mock_traces_client: Mock, mock_projects_client: Mock, mock_logstreams_client: Mock, reset_context
) -> None:
    """Test that input is properly serialized and then deserialized back to JSON."""
    mock_traces_client_instance = setup_mock_traces_client(mock_traces_client)
    setup_mock_projects_client(mock_projects_client)
    setup_mock_logstreams_client(mock_logstreams_client)

    @log(span_type="workflow")
    def my_function(complex_input: dict) -> str:
        return "response"

    # Test with complex nested data
    complex_input = {"nested": {"key": "value", "number": 42}, "list": [1, 2, 3], "string": "test"}

    my_function(complex_input=complex_input)
    galileo_context.flush()

    payload = mock_traces_client_instance.ingest_traces.call_args[0][0]
    span = payload.traces[0].spans[0]

    # Input should be properly serialized and deserialized JSON
    assert (
        span.input
        == '{"complex_input": {"nested": {"key": "value", "number": 42}, "list": [1, 2, 3], "string": "test"}}'
    )


@patch("galileo.logger.logger.LogStreams")
@patch("galileo.logger.logger.Projects")
@patch("galileo.logger.logger.Traces")
def test_decorator_llm_span_list_output_serialization(
    mock_traces_client: Mock, mock_projects_client: Mock, mock_logstreams_client: Mock, reset_context
) -> None:
    """Test that LLM spans with list/tuple outputs are converted to string."""
    mock_traces_client_instance = setup_mock_traces_client(mock_traces_client)
    setup_mock_projects_client(mock_projects_client)
    setup_mock_logstreams_client(mock_logstreams_client)

    @log(span_type="llm")
    def llm_call_returning_list(query: str):
        return ["response1", "response2", "response3"]

    llm_call_returning_list(query="input")
    galileo_context.flush()

    payload = mock_traces_client_instance.ingest_traces.call_args[0][0]
    span = payload.traces[0].spans[0]

    # For LLM spans, list outputs should be converted to string within a Message
    assert hasattr(span.output, "content")
    assert span.output.content == '["response1", "response2", "response3"]'


@patch("galileo.logger.logger.LogStreams")
@patch("galileo.logger.logger.Projects")
@patch("galileo.logger.logger.Traces")
def test_decorator_llm_span_tuple_output_serialization(
    mock_traces_client: Mock, mock_projects_client: Mock, mock_logstreams_client: Mock, reset_context
) -> None:
    """Test that LLM spans with tuple outputs are converted to string."""
    mock_traces_client_instance = setup_mock_traces_client(mock_traces_client)
    setup_mock_projects_client(mock_projects_client)
    setup_mock_logstreams_client(mock_logstreams_client)

    @log(span_type="llm")
    def llm_call_returning_tuple(query: str):
        return ("response1", "response2")

    llm_call_returning_tuple(query="input")
    galileo_context.flush()

    payload = mock_traces_client_instance.ingest_traces.call_args[0][0]
    span = payload.traces[0].spans[0]

    # For LLM spans, tuple outputs should be converted to string
    assert hasattr(span.output, "content")
    # Note: Tuples are converted to lists during JSON serialization
    assert span.output.content == '["response1", "response2"]'


@patch("galileo.logger.logger.LogStreams")
@patch("galileo.logger.logger.Projects")
@patch("galileo.logger.logger.Traces")
def test_decorator_llm_span_dict_output_preserved(
    mock_traces_client: Mock, mock_projects_client: Mock, mock_logstreams_client: Mock, reset_context
) -> None:
    """Test that LLM spans with dict outputs are preserved as JSON."""
    mock_traces_client_instance = setup_mock_traces_client(mock_traces_client)
    setup_mock_projects_client(mock_projects_client)
    setup_mock_logstreams_client(mock_logstreams_client)

    @log(span_type="llm")
    def llm_call_returning_dict(query: str):
        return {"response": "value", "number": 42}

    llm_call_returning_dict(query="input")
    galileo_context.flush()

    payload = mock_traces_client_instance.ingest_traces.call_args[0][0]
    span = payload.traces[0].spans[0]

    # For LLM spans, dict outputs should be preserved as Message with JSON serialization
    assert hasattr(span.output, "content")
    # The output should be properly JSON serialized
    assert '"response": "value"' in span.output.content
    assert '"number": 42' in span.output.content


@patch("galileo.logger.logger.LogStreams")
@patch("galileo.logger.logger.Projects")
@patch("galileo.logger.logger.Traces")
def test_decorator_workflow_span_complex_output_serialization(
    mock_traces_client: Mock, mock_projects_client: Mock, mock_logstreams_client: Mock, reset_context
) -> None:
    """Test that workflow spans properly serialize complex outputs."""
    mock_traces_client_instance = setup_mock_traces_client(mock_traces_client)
    setup_mock_projects_client(mock_projects_client)
    setup_mock_logstreams_client(mock_logstreams_client)

    @log(span_type="workflow")
    def workflow_with_complex_output(query: str):
        return {
            "result": ["item1", "item2"],
            "metadata": {"count": 2, "processed": True},
            "nested": {"deep": {"value": "test"}},
        }

    workflow_with_complex_output(query="input")
    galileo_context.flush()

    payload = mock_traces_client_instance.ingest_traces.call_args[0][0]
    span = payload.traces[0].spans[0]

    # Workflow spans should serialize complex outputs to string
    assert isinstance(span.output, str)
    expected_content = '{"result": ["item1", "item2"], "metadata": {"count": 2, "processed": true}, "nested": {"deep": {"value": "test"}}}'
    assert span.output == expected_content


@patch("galileo.logger.logger.LogStreams")
@patch("galileo.logger.logger.Projects")
@patch("galileo.logger.logger.Traces")
def test_decorator_pydantic_model_input_serialization(
    mock_traces_client: Mock, mock_projects_client: Mock, mock_logstreams_client: Mock, reset_context
) -> None:
    """Test that Pydantic model inputs are properly serialized."""
    mock_traces_client_instance = setup_mock_traces_client(mock_traces_client)
    setup_mock_projects_client(mock_projects_client)
    setup_mock_logstreams_client(mock_logstreams_client)

    @log(span_type="workflow")
    def process_model(model: TestPydanticModel) -> str:
        return f"Processed {model.name}"

    test_model = TestPydanticModel(name="test", value=42)
    process_model(model=test_model)
    galileo_context.flush()

    payload = mock_traces_client_instance.ingest_traces.call_args[0][0]
    span = payload.traces[0].spans[0]

    # Pydantic model should be serialized in input
    assert '"name": "test"' in span.input
    assert '"value": 42' in span.input
    # Default values should be excluded from serialization
    assert '"optional_field"' not in span.input


@patch("galileo.logger.logger.LogStreams")
@patch("galileo.logger.logger.Projects")
@patch("galileo.logger.logger.Traces")
def test_decorator_pydantic_model_output_serialization(
    mock_traces_client: Mock, mock_projects_client: Mock, mock_logstreams_client: Mock, reset_context
) -> None:
    """Test that Pydantic model outputs are properly serialized."""
    mock_traces_client_instance = setup_mock_traces_client(mock_traces_client)
    setup_mock_projects_client(mock_projects_client)
    setup_mock_logstreams_client(mock_logstreams_client)

    @log(span_type="workflow")
    def create_model(name: str, value: int):
        return TestPydanticModel(name=name, value=value)

    create_model(name="output_test", value=123)
    galileo_context.flush()

    payload = mock_traces_client_instance.ingest_traces.call_args[0][0]
    span = payload.traces[0].spans[0]

    # Pydantic model output should be serialized to string
    assert isinstance(span.output, str)
    assert '"name": "output_test"' in span.output
    assert '"value": 123' in span.output


@patch("galileo.logger.logger.LogStreams")
@patch("galileo.logger.logger.Projects")
@patch("galileo.logger.logger.Traces")
def test_decorator_null_output_handling(
    mock_traces_client: Mock, mock_projects_client: Mock, mock_logstreams_client: Mock, reset_context
) -> None:
    """Test that None/null outputs are handled properly."""
    mock_traces_client_instance = setup_mock_traces_client(mock_traces_client)
    setup_mock_projects_client(mock_projects_client)
    setup_mock_logstreams_client(mock_logstreams_client)

    @log(span_type="workflow")
    def function_returning_none(query: str) -> None:
        return None

    function_returning_none(query="input")
    galileo_context.flush()

    payload = mock_traces_client_instance.ingest_traces.call_args[0][0]
    span = payload.traces[0].spans[0]

    # None output should be converted to empty string or None (depending on implementation)
    # In this case, the output is None because it wasn't processed through the serialization logic for None values
    assert span.output is None or span.output == ""


@patch("galileo.logger.logger.LogStreams")
@patch("galileo.logger.logger.Projects")
@patch("galileo.logger.logger.Traces")
def test_decorator_tool_span_output_serialization(
    mock_traces_client: Mock, mock_projects_client: Mock, mock_logstreams_client: Mock, reset_context
) -> None:
    """Test that tool spans properly serialize outputs to string."""
    mock_traces_client_instance = setup_mock_traces_client(mock_traces_client)
    setup_mock_projects_client(mock_projects_client)
    setup_mock_logstreams_client(mock_logstreams_client)

    @log(span_type="tool")
    def tool_with_complex_output(input_data: str):
        return {"tool_result": input_data, "status": "success", "items": [1, 2, 3]}

    tool_with_complex_output(input_data="test")
    galileo_context.flush()

    payload = mock_traces_client_instance.ingest_traces.call_args[0][0]
    span = payload.traces[0].spans[0]

    # Tool spans should serialize outputs to string (textual span type)
    assert isinstance(span.output, str)
    assert '"tool_result": "test"' in span.output
    assert '"status": "success"' in span.output
    assert '"items": [1, 2, 3]' in span.output


@patch("galileo.logger.logger.LogStreams")
@patch("galileo.logger.logger.Projects")
@patch("galileo.logger.logger.Traces")
def test_decorator_agent_span_output_serialization(
    mock_traces_client: Mock, mock_projects_client: Mock, mock_logstreams_client: Mock, reset_context
) -> None:
    """Test that agent spans properly serialize outputs to string."""
    mock_traces_client_instance = setup_mock_traces_client(mock_traces_client)
    setup_mock_projects_client(mock_projects_client)
    setup_mock_logstreams_client(mock_logstreams_client)

    @log(span_type="agent")
    def agent_with_complex_output(query: str):
        return {"agent_response": query, "confidence": 0.95, "actions": ["analyze", "respond"]}

    agent_with_complex_output(query="test query")
    galileo_context.flush()

    payload = mock_traces_client_instance.ingest_traces.call_args[0][0]
    span = payload.traces[0].spans[0]

    # Agent spans should serialize outputs to string (textual span type)
    assert isinstance(span.output, str)
    assert '"agent_response": "test query"' in span.output
    assert '"confidence": 0.95' in span.output
    assert '"actions": ["analyze", "respond"]' in span.output


@patch("galileo.logger.logger.LogStreams")
@patch("galileo.logger.logger.Projects")
@patch("galileo.logger.logger.Traces")
def test_decorator_workflow_content_blocks_output_preserved(
    mock_traces_client: Mock, mock_projects_client: Mock, mock_logstreams_client: Mock, reset_context
) -> None:
    """Test that List[ContentBlock] output from a workflow span is preserved, not stringified."""
    mock_traces_client_instance = setup_mock_traces_client(mock_traces_client)
    setup_mock_projects_client(mock_projects_client)
    setup_mock_logstreams_client(mock_logstreams_client)

    blocks = [
        TextContentBlock(text="Analysis complete"),
        DataContentBlock(modality=ContentModality.image, url="https://example.com/chart.png"),
    ]

    @log(span_type="workflow")
    def workflow_returning_content_blocks(query: str):
        return blocks

    # When: the workflow is executed and flushed
    workflow_returning_content_blocks(query="analyze this")
    galileo_context.flush()

    # Then: content blocks are preserved as a list on the trace (not stringified)
    payload = mock_traces_client_instance.ingest_traces.call_args[0][0]
    trace_output = payload.traces[0].output
    assert isinstance(trace_output, list)
    assert isinstance(trace_output[0], TextContentBlock)
    assert trace_output[0].text == "Analysis complete"
    assert isinstance(trace_output[1], DataContentBlock)

    # Then: the workflow span output is also preserved as a list
    span_output = payload.traces[0].spans[0].output
    assert isinstance(span_output, list)


@patch("galileo.logger.logger.LogStreams")
@patch("galileo.logger.logger.Projects")
@patch("galileo.logger.logger.Traces")
def test_decorator_workflow_message_list_output_serialized(
    mock_traces_client: Mock, mock_projects_client: Mock, mock_logstreams_client: Mock, reset_context
) -> None:
    """Test that List[Message] output from a workflow is serialized to string on the trace."""
    mock_traces_client_instance = setup_mock_traces_client(mock_traces_client)
    setup_mock_projects_client(mock_projects_client)
    setup_mock_logstreams_client(mock_logstreams_client)

    @log(span_type="workflow")
    def workflow_returning_messages(query: str):
        return [
            Message(content="Hello", role=MessageRole.user),
            Message(content="Hi there!", role=MessageRole.assistant),
        ]

    # When: the workflow is executed and flushed
    workflow_returning_messages(query="chat")
    galileo_context.flush()

    # Then: messages are serialized to string on the trace (not preserved as list)
    payload = mock_traces_client_instance.ingest_traces.call_args[0][0]
    trace_output = payload.traces[0].output
    assert isinstance(trace_output, str)
    assert "Hello" in trace_output
    assert "Hi there!" in trace_output


# ============================================================================
# Mode Context Tests
# ============================================================================


@patch("galileo.logger.logger.LogStreams")
@patch("galileo.logger.logger.Projects")
@patch("galileo.logger.logger.Traces")
def test_mode_context_init_default(
    mock_traces_client: Mock, mock_projects_client: Mock, mock_logstreams_client: Mock, reset_context
) -> None:
    """Test that mode defaults to 'batch' when not specified."""
    setup_mock_traces_client(mock_traces_client)
    setup_mock_projects_client(mock_projects_client)
    setup_mock_logstreams_client(mock_logstreams_client)

    galileo_context.init(project="project-X", log_stream="log-stream-X")

    assert galileo_context.get_current_mode() == "batch"


@patch("galileo.logger.logger.LogStreams")
@patch("galileo.logger.logger.Projects")
@patch("galileo.logger.logger.Traces")
def test_mode_context_init_explicit(
    mock_traces_client: Mock, mock_projects_client: Mock, mock_logstreams_client: Mock, reset_context
) -> None:
    """Test that mode can be explicitly set during init."""
    setup_mock_traces_client(mock_traces_client)
    setup_mock_projects_client(mock_projects_client)
    setup_mock_logstreams_client(mock_logstreams_client)

    galileo_context.init(project="project-X", log_stream="log-stream-X", mode="distributed")

    assert galileo_context.get_current_mode() == "distributed"


@patch("galileo.logger.logger.LogStreams")
@patch("galileo.logger.logger.Projects")
@patch("galileo.logger.logger.Traces")
def test_mode_context_call_default(
    mock_traces_client: Mock, mock_projects_client: Mock, mock_logstreams_client: Mock, reset_context
) -> None:
    """Test that mode defaults to 'batch' in context manager."""
    setup_mock_traces_client(mock_traces_client)
    setup_mock_projects_client(mock_projects_client)
    setup_mock_logstreams_client(mock_logstreams_client)

    with galileo_context(project="project-X", log_stream="log-stream-X"):
        assert galileo_context.get_current_mode() == "batch"


@patch("galileo.logger.logger.LogStreams")
@patch("galileo.logger.logger.Projects")
@patch("galileo.logger.logger.Traces")
def test_mode_context_call_explicit(
    mock_traces_client: Mock, mock_projects_client: Mock, mock_logstreams_client: Mock, reset_context
) -> None:
    """Test that mode can be explicitly set in context manager."""
    setup_mock_traces_client(mock_traces_client)
    setup_mock_projects_client(mock_projects_client)
    setup_mock_logstreams_client(mock_logstreams_client)

    with galileo_context(project="project-X", log_stream="log-stream-X", mode="distributed"):
        assert galileo_context.get_current_mode() == "distributed"


@patch("galileo.logger.logger.LogStreams")
@patch("galileo.logger.logger.Projects")
@patch("galileo.logger.logger.Traces")
def test_mode_context_nested_push_pop(
    mock_traces_client: Mock, mock_projects_client: Mock, mock_logstreams_client: Mock, reset_context
) -> None:
    """Test that mode is properly pushed and popped with nested contexts."""
    setup_mock_traces_client(mock_traces_client)
    setup_mock_projects_client(mock_projects_client)
    setup_mock_logstreams_client(mock_logstreams_client)

    # Set initial mode
    galileo_context.init(project="project-X", log_stream="log-stream-X", mode="batch")
    assert galileo_context.get_current_mode() == "batch"

    # Enter nested context with different mode
    with galileo_context(project="project-Y", log_stream="log-stream-Y", mode="distributed"):
        assert galileo_context.get_current_mode() == "distributed"

    # After exiting, mode should be restored
    assert galileo_context.get_current_mode() == "batch"


@patch("galileo.logger.logger.LogStreams")
@patch("galileo.logger.logger.Projects")
@patch("galileo.logger.logger.Traces")
def test_mode_context_multiple_nested_levels(
    mock_traces_client: Mock, mock_projects_client: Mock, mock_logstreams_client: Mock, reset_context
) -> None:
    """Test that mode is properly managed across multiple nested context levels."""
    setup_mock_traces_client(mock_traces_client)
    setup_mock_projects_client(mock_projects_client)
    setup_mock_logstreams_client(mock_logstreams_client)

    # Set initial mode
    galileo_context.init(project="project-X", log_stream="log-stream-X", mode="batch")
    assert galileo_context.get_current_mode() == "batch"

    # First nested level
    with galileo_context(project="project-Y", log_stream="log-stream-Y", mode="distributed"):
        assert galileo_context.get_current_mode() == "distributed"

        # Second nested level - defaults back to batch
        with galileo_context(project="project-Z", log_stream="log-stream-Z"):
            assert galileo_context.get_current_mode() == "batch"

        # Back to first nested level
        assert galileo_context.get_current_mode() == "distributed"

    # Back to original
    assert galileo_context.get_current_mode() == "batch"


@patch("galileo.logger.logger.LogStreams")
@patch("galileo.logger.logger.Projects")
@patch("galileo.logger.logger.Traces")
def test_mode_context_reset(
    mock_traces_client: Mock, mock_projects_client: Mock, mock_logstreams_client: Mock, reset_context
) -> None:
    """Test that mode is reset to 'batch' when reset() is called."""
    setup_mock_traces_client(mock_traces_client)
    setup_mock_projects_client(mock_projects_client)
    setup_mock_logstreams_client(mock_logstreams_client)

    galileo_context.init(project="project-X", log_stream="log-stream-X", mode="distributed")
    assert galileo_context.get_current_mode() == "distributed"

    galileo_context.reset()
    assert galileo_context.get_current_mode() == "batch"


@patch("galileo.logger.logger.LogStreams")
@patch("galileo.logger.logger.Projects")
@patch("galileo.logger.logger.Traces")
def test_mode_flush_with_explicit_mode(
    mock_traces_client: Mock, mock_projects_client: Mock, mock_logstreams_client: Mock, reset_context
) -> None:
    """Test that flush can target a specific mode's logger instance."""
    mock_traces_client_instance = setup_mock_traces_client(mock_traces_client)
    setup_mock_projects_client(mock_projects_client)
    setup_mock_logstreams_client(mock_logstreams_client)

    # Initialize with batch mode
    galileo_context.init(project="project-X", log_stream="log-stream-X", mode="batch")

    @log(span_type="llm")
    def llm_call(query: str) -> str:
        return "response"

    llm_call(query="input")
    assert galileo_context.get_current_trace() is not None

    # Flush with explicit mode
    galileo_context.flush(project="project-X", log_stream="log-stream-X", mode="batch")

    payload = mock_traces_client_instance.ingest_traces.call_args[0][0]
    assert len(payload.traces) == 1

    # Trace context should be reset since we flushed the current context
    assert galileo_context.get_current_trace() is None


@patch("galileo.logger.logger.LogStreams")
@patch("galileo.logger.logger.Projects")
@patch("galileo.logger.logger.Traces")
def test_mode_flush_different_mode_no_reset(
    mock_traces_client: Mock, mock_projects_client: Mock, mock_logstreams_client: Mock, reset_context
) -> None:
    """Test that flush with different mode doesn't reset current trace context."""
    setup_mock_traces_client(mock_traces_client)
    setup_mock_projects_client(mock_projects_client)
    setup_mock_logstreams_client(mock_logstreams_client)

    # Initialize with batch mode
    galileo_context.init(project="project-X", log_stream="log-stream-X", mode="batch")

    @log(span_type="llm")
    def llm_call(query: str) -> str:
        return "response"

    llm_call(query="input")
    current_trace = galileo_context.get_current_trace()
    assert current_trace is not None

    # Flush with a different mode shouldn't reset the current trace context
    # Since the logger instances are different
    galileo_context.flush(project="project-X", log_stream="log-stream-X", mode="distributed")

    # Current trace should still exist since we didn't flush the batch mode instance
    assert galileo_context.get_current_trace() is not None
    assert galileo_context.get_current_trace() == current_trace


@patch("galileo.logger.logger.LogStreams")
@patch("galileo.logger.logger.Projects")
@patch("galileo.logger.logger.Traces")
@patch.dict("os.environ", {"GALILEO_MODE": "distributed"})
def test_mode_from_environment_variable(
    mock_traces_client: Mock, mock_projects_client: Mock, mock_logstreams_client: Mock, reset_context
) -> None:
    """Test that mode is read from GALILEO_MODE environment variable."""
    setup_mock_traces_client(mock_traces_client)
    setup_mock_projects_client(mock_projects_client)
    setup_mock_logstreams_client(mock_logstreams_client)

    # When mode is not specified, it should use the environment variable
    galileo_context.init(project="project-X", log_stream="log-stream-X")

    assert galileo_context.get_current_mode() == "distributed"


@patch("galileo.logger.logger.LogStreams")
@patch("galileo.logger.logger.Projects")
@patch("galileo.logger.logger.Traces")
@patch.dict("os.environ", {"GALILEO_MODE": "distributed"})
def test_mode_explicit_overrides_environment(
    mock_traces_client: Mock, mock_projects_client: Mock, mock_logstreams_client: Mock, reset_context
) -> None:
    """Test that explicit mode parameter overrides environment variable."""
    setup_mock_traces_client(mock_traces_client)
    setup_mock_projects_client(mock_projects_client)
    setup_mock_logstreams_client(mock_logstreams_client)

    # Explicit mode should override environment variable
    galileo_context.init(project="project-X", log_stream="log-stream-X", mode="batch")

    assert galileo_context.get_current_mode() == "batch"


@patch("galileo.logger.logger.LogStreams")
@patch("galileo.logger.logger.Projects")
@patch("galileo.logger.logger.Traces")
def test_get_logger_instance_with_explicit_mode(
    mock_traces_client: Mock, mock_projects_client: Mock, mock_logstreams_client: Mock, reset_context
) -> None:
    """Test that get_logger_instance can accept explicit mode parameter."""
    setup_mock_traces_client(mock_traces_client)
    setup_mock_projects_client(mock_projects_client)
    setup_mock_logstreams_client(mock_logstreams_client)

    # Initialize with batch mode
    galileo_context.init(project="project-X", log_stream="log-stream-X", mode="batch")

    # Get logger instance with different mode
    logger_batch = galileo_context.get_logger_instance(project="project-X", log_stream="log-stream-X", mode="batch")
    logger_distributed = galileo_context.get_logger_instance(
        project="project-X", log_stream="log-stream-X", mode="distributed"
    )

    # They should be different instances
    assert logger_batch is not logger_distributed
    assert logger_batch.mode == "batch"
    assert logger_distributed.mode == "distributed"


@patch("galileo.logger.logger.LogStreams")
@patch("galileo.logger.logger.Projects")
@patch("galileo.logger.logger.Traces")
def test_multiple_workflow_calls_create_one_trace_with_multiple_spans(
    mock_traces_client: Mock, mock_projects_client: Mock, mock_logstreams_client: Mock, reset_context
) -> None:
    """
    Test that multiple workflow-level function calls are added as spans to a single trace in batch mode.
    """
    mock_traces_client_instance = setup_mock_traces_client(mock_traces_client)
    setup_mock_projects_client(mock_projects_client)
    setup_mock_logstreams_client(mock_logstreams_client)

    galileo_context.init(project="project-X", log_stream="log-stream-X", mode="batch")

    @log(span_type="workflow")
    def process_query(query: str) -> str:
        return f"Processed: {query}"

    # Call the workflow function 3 times
    result1 = process_query("query 1")
    result2 = process_query("query 2")
    result3 = process_query("query 3")

    # Verify results
    assert result1 == "Processed: query 1"
    assert result2 == "Processed: query 2"
    assert result3 == "Processed: query 3"

    # Before flush, verify only 1 trace was created with 3 workflow spans
    logger = galileo_context.get_logger_instance()
    assert len(logger.traces) == 1, f"Expected 1 trace, got {len(logger.traces)}"

    # Verify the single trace has 3 workflow spans
    trace = logger.traces[0]
    assert len(trace.spans) == 3, f"Expected 3 spans, got {len(trace.spans)}"

    # Verify each span has the correct input
    assert trace.spans[0].input == '{"query": "query 1"}'
    assert trace.spans[1].input == '{"query": "query 2"}'
    assert trace.spans[2].input == '{"query": "query 3"}'

    # Flush the trace
    galileo_context.flush()

    # Verify ingest_traces was called with 1 trace containing 3 spans
    payload = mock_traces_client_instance.ingest_traces.call_args[0][0]
    assert len(payload.traces) == 1
    assert len(payload.traces[0].spans) == 3

    # After flush, trace context should be cleared
    assert galileo_context.get_current_trace() is None
    assert len(logger.traces) == 0


@patch("galileo.logger.logger.LogStreams")
@patch("galileo.logger.logger.Projects")
@patch("galileo.logger.logger.Traces")
def test_session_id_context_manager(
    mock_traces_client: Mock, mock_projects_client: Mock, mock_logstreams_client: Mock, reset_context
) -> None:
    """Test that session_id can be set via context manager and is included in payload."""
    mock_traces_client_instance = setup_mock_traces_client(mock_traces_client)
    setup_mock_projects_client(mock_projects_client)
    setup_mock_logstreams_client(mock_logstreams_client)

    test_session_id = "1c4e3f7e-4a9a-4e7e-8c1f-3a9a3a9a3a9d"

    @log()
    def foo() -> str:
        return "response"

    galileo_context.init(project="test-project", log_stream="test-stream")
    with galileo_context(session_id=test_session_id):
        assert galileo_context.get_logger_instance().session_id == test_session_id
        foo()

    payload = mock_traces_client_instance.ingest_traces.call_args[0][0]
    assert payload.session_id == UUID(test_session_id)


@patch("galileo.logger.logger.LogStreams")
@patch("galileo.logger.logger.Projects")
@patch("galileo.logger.logger.Traces")
def test_session_id_nested_context_stacking(
    mock_traces_client: Mock, mock_projects_client: Mock, mock_logstreams_client: Mock, reset_context
) -> None:
    """Test that session_id is properly stacked and restored in nested contexts."""
    setup_mock_traces_client(mock_traces_client)
    setup_mock_projects_client(mock_projects_client)
    setup_mock_logstreams_client(mock_logstreams_client)

    session_1 = "2c4e3f7e-4a9a-4e7e-8c1f-3a9a3a9a3a9d"
    session_2 = "3c4e3f7e-4a9a-4e7e-8c1f-3a9a3a9a3a9d"

    # No session initially
    assert galileo_context.get_logger_instance().session_id is None

    with galileo_context(project="p1", log_stream="s1", session_id=session_1):
        assert galileo_context.get_logger_instance().session_id == session_1

        with galileo_context(project="p2", log_stream="s2", session_id=session_2):
            assert galileo_context.get_logger_instance().session_id == session_2

        # Restored after nested context exits
        assert galileo_context.get_logger_instance().session_id == session_1

    # Cleared after all contexts exit
    assert galileo_context.get_logger_instance().session_id is None


@patch("galileo.logger.logger.LogStreams")
@patch("galileo.logger.logger.Projects")
@patch("galileo.logger.logger.Traces")
def test_session_id_cleared_on_reset_and_init(
    mock_traces_client: Mock, mock_projects_client: Mock, mock_logstreams_client: Mock, reset_context
) -> None:
    """Test that session_id is cleared when context is reset or re-initialized."""
    setup_mock_traces_client(mock_traces_client)
    setup_mock_projects_client(mock_projects_client)
    setup_mock_logstreams_client(mock_logstreams_client)

    galileo_context.init(project="project-X", log_stream="log-stream-X")
    galileo_context.start_session(name="test-session")
    assert galileo_context.get_logger_instance().session_id == "6c4e3f7e-4a9a-4e7e-8c1f-3a9a3a9a3a9c"

    # Reset clears session
    galileo_context.reset()
    assert galileo_context.get_logger_instance().session_id is None

    # Re-init also clears session
    galileo_context.init(project="project-X", log_stream="log-stream-X")
    galileo_context.start_session(name="test-session")
    galileo_context.init(project="project-Y", log_stream="log-stream-Y")
    assert galileo_context.get_logger_instance().session_id is None


@patch("galileo.logger.logger.LogStreams")
@patch("galileo.logger.logger.Projects")
@patch("galileo.logger.logger.Traces")
def test_start_session_overrides_context_session(
    mock_traces_client: Mock, mock_projects_client: Mock, mock_logstreams_client: Mock, reset_context
) -> None:
    """Test that start_session overrides context manager session and updates context var."""
    setup_mock_traces_client(mock_traces_client)
    setup_mock_projects_client(mock_projects_client)
    setup_mock_logstreams_client(mock_logstreams_client)

    context_session = "6d4e3f7e-4a9a-4e7e-8c1f-3a9a3a9a3a9d"

    with galileo_context(project="test-project", log_stream="test-stream", session_id=context_session):
        assert galileo_context.get_logger_instance().session_id == context_session

        # start_session overrides context session
        new_session_id = galileo_context.start_session(name="new-session")
        assert galileo_context.get_logger_instance().session_id == new_session_id
        assert _session_id_context.get() == new_session_id


@patch("galileo.logger.logger.LogStreams")
@patch("galileo.logger.logger.Projects")
@patch("galileo.logger.logger.Traces")
def test_flush_on_error_called_when_flush_raises(
    mock_traces_client: Mock, mock_projects_client: Mock, mock_logstreams_client: Mock, reset_context
) -> None:
    # Given: the logger's flush raises and an on_error callback is provided
    mock_traces_client_instance = setup_mock_traces_client(mock_traces_client)
    setup_mock_projects_client(mock_projects_client)
    setup_mock_logstreams_client(mock_logstreams_client)
    flush_error = RuntimeError("network error")
    mock_traces_client_instance.ingest_traces.side_effect = flush_error

    on_error = Mock()

    galileo_context.init(project="project-X", log_stream="log-stream-X")

    @log(span_type="llm")
    def llm_call(query: str) -> str:
        return "response"

    llm_call(query="input")

    # When: flush is called with on_error
    galileo_context.flush(on_error=on_error)

    # Then: on_error is invoked with the exception; no warning is raised
    on_error.assert_called_once()
    assert isinstance(on_error.call_args[0][0], Exception)


@patch("galileo.logger.logger.LogStreams")
@patch("galileo.logger.logger.Projects")
@patch("galileo.logger.logger.Traces")
def test_flush_warns_when_flush_raises_without_on_error(
    mock_traces_client: Mock, mock_projects_client: Mock, mock_logstreams_client: Mock, reset_context
) -> None:
    # Given: the logger's flush raises and no on_error callback is provided
    mock_traces_client_instance = setup_mock_traces_client(mock_traces_client)
    setup_mock_projects_client(mock_projects_client)
    setup_mock_logstreams_client(mock_logstreams_client)
    mock_traces_client_instance.ingest_traces.side_effect = RuntimeError("network error")

    galileo_context.init(project="project-X", log_stream="log-stream-X")

    @log(span_type="llm")
    def llm_call(query: str) -> str:
        return "response"

    llm_call(query="input")

    # When/Then: flush does not raise; a warning is logged instead

    with patch("galileo.decorator._logger") as mock_logger:
        galileo_context.flush()
        mock_logger.warning.assert_called_once()
        assert "flush failed" in mock_logger.warning.call_args[0][0]


@patch("galileo.logger.logger.LogStreams")
@patch("galileo.logger.logger.Projects")
@patch("galileo.logger.logger.Traces")
def test_flush_on_error_callback_raises_is_swallowed(
    mock_traces_client: Mock, mock_projects_client: Mock, mock_logstreams_client: Mock, reset_context
) -> None:
    # Given: the logger's flush raises, on_error is provided but also raises
    mock_traces_client_instance = setup_mock_traces_client(mock_traces_client)
    setup_mock_projects_client(mock_projects_client)
    setup_mock_logstreams_client(mock_logstreams_client)
    mock_traces_client_instance.ingest_traces.side_effect = RuntimeError("network error")

    def bad_callback(exc: Exception) -> None:
        raise ValueError("callback failed")

    galileo_context.init(project="project-X", log_stream="log-stream-X")

    @log(span_type="llm")
    def llm_call(query: str) -> str:
        return "response"

    llm_call(query="input")

    # When/Then: flush does not raise even though the callback raises
    with patch("galileo.decorator._logger") as mock_logger:
        galileo_context.flush(on_error=bad_callback)  # must not raise
        mock_logger.warning.assert_called_once()
        assert "on_error callback raised" in mock_logger.warning.call_args[0][0]


@patch("galileo.logger.logger.LogStreams")
@patch("galileo.logger.logger.Projects")
@patch("galileo.logger.logger.Traces")
def test_flush_on_error_logs_at_debug_not_warning(
    mock_traces_client: Mock, mock_projects_client: Mock, mock_logstreams_client: Mock, reset_context
) -> None:
    # Given: the logger's flush raises and an on_error callback is provided
    mock_traces_client_instance = setup_mock_traces_client(mock_traces_client)
    setup_mock_projects_client(mock_projects_client)
    setup_mock_logstreams_client(mock_logstreams_client)
    mock_traces_client_instance.ingest_traces.side_effect = RuntimeError("network error")

    galileo_context.init(project="project-X", log_stream="log-stream-X")

    @log(span_type="llm")
    def llm_call(query: str) -> str:
        return "response"

    llm_call(query="input")

    # When: flush is called with on_error
    with patch("galileo.decorator._logger") as mock_logger:
        galileo_context.flush(on_error=Mock())

        # Then: debug is called, not warning
        mock_logger.debug.assert_called_once()
        mock_logger.warning.assert_not_called()


@pytest.mark.asyncio
@patch("galileo.logger.logger.LogStreams")
@patch("galileo.logger.logger.Projects")
@patch("galileo.logger.logger.Traces")
async def test_concurrent_decorated_coroutines_do_not_flush_each_others_traces(
    mock_traces_client: Mock, mock_projects_client: Mock, mock_logstreams_client: Mock, reset_context
) -> None:
    """A flush must not carry a concurrent task's still-running decorated trace.

    ``@log`` on an async function necessarily holds its trace open across every await inside the
    function, and concurrent tasks under one ``galileo_context`` share a single ``GalileoLogger``
    and therefore a single trace list. Flushing from one task while another is mid-await used to
    send the sibling's trace, which is serialised before the request is awaited and so goes out
    with no output - and, because the batch is detached from the list, the sibling's own flush
    then finds nothing left to send.

    This is the documented usage shape rather than an exotic one: plain ``@log`` plus
    ``asyncio.gather``, and the blocking ``flush()``. No ``async_flush()`` is involved.
    """
    # Given: two decorated coroutines under one context, one held mid-await
    mock_traces_client_instance = setup_mock_traces_client(mock_traces_client)
    setup_mock_projects_client(mock_projects_client)
    setup_mock_logstreams_client(mock_logstreams_client)

    london_started = asyncio.Event()
    london_may_finish = asyncio.Event()
    ingest_payloads: list[list[tuple[str, str | None]]] = []

    def record_payload(request) -> dict:
        # Snapshotted synchronously: the real client serialises before its first await, so a
        # trace sent mid-flight cannot be repaired by a later conclude.
        ingest_payloads.append([(trace.name, trace.output) for trace in request.traces])
        return {}

    mock_traces_client_instance.ingest_traces.side_effect = record_payload

    @log
    async def london_forecast() -> str:
        london_started.set()
        await london_may_finish.wait()
        return "rainy in London"

    @log
    async def new_york_forecast() -> str:
        return "sunny in New York"

    async def london_request() -> None:
        await london_forecast()
        galileo_context.get_logger_instance(project="project-concurrent", log_stream="stream-concurrent").flush()

    with galileo_context(project="project-concurrent", log_stream="stream-concurrent"):
        logger = galileo_context.get_logger_instance(project="project-concurrent", log_stream="stream-concurrent")
        london = asyncio.create_task(london_request())
        await asyncio.wait_for(london_started.wait(), timeout=5)

        # When: the other coroutine finishes and flushes while London is still awaiting
        await new_york_forecast()
        logger.flush()

        # Then: only the finished trace was sent, and London waits for its own flush
        assert ingest_payloads == [[("new_york_forecast", "sunny in New York")]]
        assert [trace.name for trace in logger.traces] == ["london_forecast"]

        # When: London finishes and flushes from its own task
        london_may_finish.set()
        await london

    # Then: London was sent exactly once, carrying its own output
    assert ingest_payloads == [[("new_york_forecast", "sunny in New York")], [("london_forecast", "rainy in London")]]


@pytest.mark.asyncio
@patch("galileo.logger.logger.LogStreams")
@patch("galileo.logger.logger.Projects")
@patch("galileo.logger.logger.Traces")
async def test_context_exit_flush_sends_traces_from_finished_tasks(
    mock_traces_client: Mock, mock_projects_client: Mock, mock_logstreams_client: Mock, reset_context
) -> None:
    """Traces from tasks that finished without flushing must still leave at context exit.

    ``@log`` leaves its trace open on purpose so a later decorated call in the same context can
    reuse it, so "not concluded" cannot mean "still being built" - if it did, tasks that finish
    without flushing would have their traces held back from the exit flush and stranded until the
    process ends. The decorator therefore reports the hand-off when its outermost call returns.

    Nothing flushes per task here: ``galileo_context.__exit__`` is the only flush.
    """
    # Given: three decorated coroutines that run concurrently and never flush themselves
    mock_traces_client_instance = setup_mock_traces_client(mock_traces_client)
    setup_mock_projects_client(mock_projects_client)
    setup_mock_logstreams_client(mock_logstreams_client)

    ingest_payloads: list[list[str]] = []

    def record_payload(request) -> dict:
        ingest_payloads.append([trace.name for trace in request.traces])
        return {}

    mock_traces_client_instance.ingest_traces.side_effect = record_payload

    @log
    async def forecast(city: str) -> str:
        await asyncio.sleep(0)  # yield, so the three tasks genuinely interleave
        return f"{city}: done"

    # When: they all finish inside the context, and only the exit flush runs
    with galileo_context(project="project-exit-flush", log_stream="stream-exit-flush"):
        logger = galileo_context.get_logger_instance(project="project-exit-flush", log_stream="stream-exit-flush")
        await asyncio.gather(*(forecast(city) for city in ("New York", "London", "Tokyo")))
        assert len(logger.traces) == 3
        assert ingest_payloads == []

    # Then: the exit flush carried all three rather than stranding them
    assert ingest_payloads == [["forecast", "forecast", "forecast"]]
    assert logger.traces == []


@pytest.mark.asyncio
@patch("galileo.logger.logger.LogStreams")
@patch("galileo.logger.logger.Projects")
@patch("galileo.logger.logger.Traces")
async def test_reused_trace_is_protected_while_a_second_decorated_call_builds_it(
    mock_traces_client: Mock, mock_projects_client: Mock, mock_logstreams_client: Mock, reset_context
) -> None:
    """A trace reused by a second decorated call is off limits again while that call runs.

    A context that finishes one decorated call releases its trace so any flush can send it, but
    ``_prepare_call`` reuses that same still-open trace for the next decorated call in the context.
    The release therefore has to be re-taken on entry, or the second call's spans are exposed to a
    concurrent task's flush - the original defect, reached through the reuse path.
    """
    # Given: a task that completes one decorated call, then starts a second on the same trace
    mock_traces_client_instance = setup_mock_traces_client(mock_traces_client)
    setup_mock_projects_client(mock_projects_client)
    setup_mock_logstreams_client(mock_logstreams_client)

    second_call_started = asyncio.Event()
    second_call_may_finish = asyncio.Event()
    ingest_payloads: list[list[str]] = []

    def record_payload(request) -> dict:
        ingest_payloads.append([trace.name for trace in request.traces])
        return {}

    mock_traces_client_instance.ingest_traces.side_effect = record_payload

    @log
    async def first_step() -> str:
        return "first step done"

    @log
    async def second_step() -> str:
        second_call_started.set()
        await second_call_may_finish.wait()
        return "second step done"

    @log
    async def new_york_forecast() -> str:
        return "sunny in New York"

    async def two_step_request() -> None:
        await first_step()
        await second_step()

    with galileo_context(project="project-trace-reuse", log_stream="stream-trace-reuse"):
        logger = galileo_context.get_logger_instance(project="project-trace-reuse", log_stream="stream-trace-reuse")
        request = asyncio.create_task(two_step_request())
        await asyncio.wait_for(second_call_started.wait(), timeout=5)

        # When: another task flushes while the second call is still building the reused trace
        await new_york_forecast()
        logger.flush()

        # Then: the reused trace stayed behind
        assert ingest_payloads == [["new_york_forecast"]]
        assert [trace.name for trace in logger.traces] == ["first_step"]

        second_call_may_finish.set()
        await request

    # Then: it left at context exit, once, with both steps' spans on it
    assert ingest_payloads == [["new_york_forecast"], ["first_step"]]


@pytest.mark.asyncio
@patch("galileo.logger.logger.LogStreams")
@patch("galileo.logger.logger.Projects")
@patch("galileo.logger.logger.Traces")
async def test_trace_is_not_stranded_when_span_setup_fails(
    mock_traces_client: Mock, mock_projects_client: Mock, mock_logstreams_client: Mock, reset_context
) -> None:
    """A trace is never marked as being built unless something will release it.

    The wrappers skip ``_finalize_call`` when ``_prepare_call`` raises, and ``_finalize_call`` is
    the only thing that reports the decorator's hand-off. Claiming the trace before the span setup
    that might raise would therefore strand it: held back from every flush, with nothing left to
    release it, until the process exits.

    The failing call runs in its own task and the flush comes from outside it, because a flush in
    the owning context claims its own trace and would mask the leak.
    """
    # Given: a decorated call in another task whose span setup fails after the trace exists
    mock_traces_client_instance = setup_mock_traces_client(mock_traces_client)
    setup_mock_projects_client(mock_projects_client)
    setup_mock_logstreams_client(mock_logstreams_client)

    ingest_payloads: list[list[str]] = []

    def record_payload(request) -> dict:
        ingest_payloads.append([trace.name for trace in request.traces])
        return {}

    mock_traces_client_instance.ingest_traces.side_effect = record_payload

    @log
    async def forecast() -> str:
        return "sunny in New York"

    with galileo_context(project="project-span-setup-fails", log_stream="stream-span-setup-fails"):
        logger = galileo_context.get_logger_instance(
            project="project-span-setup-fails", log_stream="stream-span-setup-fails"
        )

        async def failing_request() -> None:
            with patch.object(type(logger), "add_workflow_span", side_effect=RuntimeError("span setup exploded")):
                await forecast()

        # When: the span setup inside _prepare_call raises, so _finalize_call is skipped
        await asyncio.create_task(failing_request())
        assert len(logger.traces) == 1

        # Then: a flush from outside that task still carries the trace
        logger.flush()

    assert ingest_payloads == [["forecast"]]


@pytest.mark.asyncio
@patch("galileo.logger.logger.LogStreams")
@patch("galileo.logger.logger.Projects")
@patch("galileo.logger.logger.Traces")
async def test_decorated_generator_releases_its_trace_when_the_call_returns(
    mock_traces_client: Mock, mock_projects_client: Mock, mock_logstreams_client: Mock, reset_context
) -> None:
    """A decorated generator must report its hand-off like any other decorated call.

    ``_finalize_call`` wraps a generator result and returns the wrapper, but ``_sync_log`` discards
    that return value and hands back the unwrapped generator, so the wrapper is never iterated and
    ``_handle_call_result`` - the only place the decorator reports it has stopped building the trace
    - never runs. The trace is then held back from every flush.

    The owning task is still alive when the foreign flush happens, so nothing but this hand-off can
    release the trace: an owner-liveness check cannot rescue it, which is what makes this the shape
    that pins the release rather than the backstop.
    """
    # Given: a decorated generator consumed inside a task that then stays alive
    mock_traces_client_instance = setup_mock_traces_client(mock_traces_client)
    setup_mock_projects_client(mock_projects_client)
    setup_mock_logstreams_client(mock_logstreams_client)

    ingest_payloads: list[list[str]] = []

    def record_payload(request) -> dict:
        ingest_payloads.append([trace.name for trace in request.traces])
        return {}

    mock_traces_client_instance.ingest_traces.side_effect = record_payload

    @log
    def stream_forecast():
        yield "sunny "
        yield "in New York"

    generator_consumed = asyncio.Event()
    task_may_finish = asyncio.Event()

    with galileo_context(project="project-decorated-generator", log_stream="stream-decorated-generator"):
        logger = galileo_context.get_logger_instance(
            project="project-decorated-generator", log_stream="stream-decorated-generator"
        )

        async def consuming_task() -> None:
            assert list(stream_forecast()) == ["sunny ", "in New York"]
            generator_consumed.set()
            await task_may_finish.wait()

        consumer = asyncio.create_task(consuming_task())
        await asyncio.wait_for(generator_consumed.wait(), timeout=5)
        assert len(logger.traces) == 1

        # When: a context that does not own the trace flushes while the owning task is still alive
        logger.flush()
        payloads_after_foreign_flush = list(ingest_payloads)

        task_may_finish.set()
        await consumer

    # Then: the flush carried the trace instead of holding it back for an owner that was done
    assert payloads_after_foreign_flush == [["stream_forecast"]]


@pytest.mark.asyncio
@patch("galileo.logger.logger.LogStreams")
@patch("galileo.logger.logger.Projects")
@patch("galileo.logger.logger.Traces")
async def test_decorated_async_generator_releases_its_trace_when_the_call_returns(
    mock_traces_client: Mock, mock_projects_client: Mock, mock_logstreams_client: Mock, reset_context
) -> None:
    """An async generator reaches the same unreleased path as a sync one.

    ``asyncio.iscoroutinefunction`` is False for an async generator function, so ``@log`` routes it
    through ``_sync_log`` too, and its wrapper is discarded the same way.
    """
    # Given: a decorated async generator consumed inside a task that then stays alive
    mock_traces_client_instance = setup_mock_traces_client(mock_traces_client)
    setup_mock_projects_client(mock_projects_client)
    setup_mock_logstreams_client(mock_logstreams_client)

    ingest_payloads: list[list[str]] = []

    def record_payload(request) -> dict:
        ingest_payloads.append([trace.name for trace in request.traces])
        return {}

    mock_traces_client_instance.ingest_traces.side_effect = record_payload

    @log
    async def stream_forecast_async():
        yield "rainy "
        yield "in London"

    generator_consumed = asyncio.Event()
    task_may_finish = asyncio.Event()

    with galileo_context(project="project-decorated-async-generator", log_stream="stream-decorated-async-generator"):
        logger = galileo_context.get_logger_instance(
            project="project-decorated-async-generator", log_stream="stream-decorated-async-generator"
        )

        async def consuming_task() -> None:
            assert [item async for item in stream_forecast_async()] == ["rainy ", "in London"]
            generator_consumed.set()
            await task_may_finish.wait()

        consumer = asyncio.create_task(consuming_task())
        await asyncio.wait_for(generator_consumed.wait(), timeout=5)
        assert len(logger.traces) == 1

        # When: a context that does not own the trace flushes while the owning task is still alive
        logger.flush()
        payloads_after_foreign_flush = list(ingest_payloads)

        task_may_finish.set()
        await consumer

    # Then: the flush carried the trace instead of holding it back for an owner that was done
    assert payloads_after_foreign_flush == [["stream_forecast_async"]]


@pytest.mark.asyncio
@patch("galileo.logger.logger.LogStreams")
@patch("galileo.logger.logger.Projects")
@patch("galileo.logger.logger.Traces")
async def test_nested_decorated_generator_does_not_release_the_outer_trace(
    mock_traces_client: Mock, mock_projects_client: Mock, mock_logstreams_client: Mock, reset_context
) -> None:
    """A nested decorated generator must not report the hand-off on its caller's behalf.

    ``_prepare_call`` pushes a span only for a workflow, agent or untyped call, so a generator
    decorated with a non-concludable span type pushes nothing. Reporting the hand-off whenever the
    span stack holds at most one entry therefore reported it for the *enclosing* call's span, and a
    sibling's flush carried the outer trace away while its body was still running - without its
    output, and detached from the list, so the outer call's own flush had nothing left to send.

    The outer call is parked on an await when the foreign flush happens, so its task is alive and an
    owner-liveness check cannot rescue the trace: only the guard on the stack length can.
    """
    # Given: an outer decorated coroutine that consumes a nested decorated generator, then parks
    mock_traces_client_instance = setup_mock_traces_client(mock_traces_client)
    setup_mock_projects_client(mock_projects_client)
    setup_mock_logstreams_client(mock_logstreams_client)

    ingest_payloads: list[list[tuple[str, str | None]]] = []

    def record_payload(request) -> dict:
        ingest_payloads.append([(trace.name, trace.output) for trace in request.traces])
        return {}

    mock_traces_client_instance.ingest_traces.side_effect = record_payload

    @log(span_type="llm")
    def stream_tokens():
        yield "sunny "
        yield "in New York"

    outer_parked = asyncio.Event()
    outer_may_finish = asyncio.Event()

    @log
    async def outer_forecast() -> str:
        assert list(stream_tokens()) == ["sunny ", "in New York"]
        outer_parked.set()
        await outer_may_finish.wait()
        return "sunny in New York"

    with galileo_context(project="project-nested-generator", log_stream="stream-nested-generator"):
        logger = galileo_context.get_logger_instance(
            project="project-nested-generator", log_stream="stream-nested-generator"
        )

        async def outer_request() -> None:
            await outer_forecast()
            logger.flush()

        owner = asyncio.create_task(outer_request())
        await asyncio.wait_for(outer_parked.wait(), timeout=5)

        # When: a context that does not own the trace flushes while the outer call is mid-await
        logger.flush()

        # Then: the outer trace stayed behind for the task that is still building it
        assert ingest_payloads == []
        assert [trace.name for trace in logger.traces] == ["outer_forecast"]

        outer_may_finish.set()
        await owner

    # Then: it was sent exactly once, by its owner, carrying the output the early release destroyed
    assert ingest_payloads == [[("outer_forecast", "sunny in New York")]]


@pytest.mark.asyncio
@patch("galileo.logger.logger.LogStreams")
@patch("galileo.logger.logger.Projects")
@patch("galileo.logger.logger.Traces")
async def test_nested_decorated_async_generator_does_not_release_the_outer_trace(
    mock_traces_client: Mock, mock_projects_client: Mock, mock_logstreams_client: Mock, reset_context
) -> None:
    """An async generator nested in a decorated call must not release its caller's trace either.

    Both generator kinds route through ``_sync_log``, and neither pushes a span when decorated with a
    non-concludable span type, so the same off-by-one reached them both.
    """
    # Given: an outer decorated coroutine that consumes a nested decorated async generator
    mock_traces_client_instance = setup_mock_traces_client(mock_traces_client)
    setup_mock_projects_client(mock_projects_client)
    setup_mock_logstreams_client(mock_logstreams_client)

    ingest_payloads: list[list[tuple[str, str | None]]] = []

    def record_payload(request) -> dict:
        ingest_payloads.append([(trace.name, trace.output) for trace in request.traces])
        return {}

    mock_traces_client_instance.ingest_traces.side_effect = record_payload

    @log(span_type="tool")
    async def stream_tokens_async():
        yield "rainy "
        yield "in London"

    outer_parked = asyncio.Event()
    outer_may_finish = asyncio.Event()

    @log
    async def outer_forecast_async() -> str:
        assert [token async for token in stream_tokens_async()] == ["rainy ", "in London"]
        outer_parked.set()
        await outer_may_finish.wait()
        return "rainy in London"

    with galileo_context(project="project-nested-async-generator", log_stream="stream-nested-async-generator"):
        logger = galileo_context.get_logger_instance(
            project="project-nested-async-generator", log_stream="stream-nested-async-generator"
        )

        async def outer_request() -> None:
            await outer_forecast_async()
            logger.flush()

        owner = asyncio.create_task(outer_request())
        await asyncio.wait_for(outer_parked.wait(), timeout=5)

        # When: a context that does not own the trace flushes while the outer call is mid-await
        logger.flush()

        # Then: the outer trace stayed behind for the task that is still building it
        assert ingest_payloads == []
        assert [trace.name for trace in logger.traces] == ["outer_forecast_async"]

        outer_may_finish.set()
        await owner

    # Then: it was sent exactly once, by its owner, carrying its output
    assert ingest_payloads == [[("outer_forecast_async", "rainy in London")]]
