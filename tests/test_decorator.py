from typing import NoReturn
from unittest.mock import Mock, patch
from uuid import UUID

import pytest
from pydantic import BaseModel

from galileo import Message, MessageRole, galileo_context, log, start_session
from galileo_core.schemas.logging.span import AgentSpan, LlmSpan, RetrieverSpan, ToolSpan, WorkflowSpan
from galileo_core.schemas.shared.document import Document
from tests.testutils.setup import setup_mock_logstreams_client, setup_mock_projects_client, setup_mock_traces_client


@pytest.fixture
def reset_context() -> None:
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
