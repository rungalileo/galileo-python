from unittest.mock import AsyncMock, Mock, patch

import httpx
import pytest
from httpx import Request, Response
from openai import Stream
from openai.types.chat import ChatCompletionChunk

from galileo import Message, MessageRole, galileo_context, log
from galileo.openai import OpenAIGalileo, openai
from galileo_core.schemas.logging.span import LlmSpan, WorkflowSpan
from tests.testutils.setup import setup_mock_logstreams_client, setup_mock_projects_client, setup_mock_traces_client
from tests.testutils.streaming import EventStream


@pytest.fixture(autouse=True)
def ensure_openai_api_key(monkeypatch):
    """Ensure OPENAI_API_KEY is set for OpenAI tests."""
    monkeypatch.setenv("OPENAI_API_KEY", "sk-test")


def openai_incorrect_api_key_error() -> bytes:
    return b"{'error': {'message': 'Incorrect API key provided: sk-galil********. You can find your API key at https://platform.openai.com/account/api-keys.', 'type': 'invalid_request_error', 'param': None, 'code': 'invalid_api_key'}}"


@patch("openai.resources.chat.Completions.create")
@patch("galileo.logger.logger.LogStreams")
@patch("galileo.logger.logger.Projects")
@patch("galileo.logger.logger.Traces")
def test_basic_openai_call(
    mock_traces_client: Mock,
    mock_projects_client: Mock,
    mock_logstreams_client: Mock,
    openai_create,
    create_chat_completion,
) -> None:
    mock_traces_client_instance = setup_mock_traces_client(mock_traces_client)
    setup_mock_projects_client(mock_projects_client)
    setup_mock_logstreams_client(mock_logstreams_client)
    openai_create.return_value = create_chat_completion

    galileo_context.reset()
    OpenAIGalileo().register_tracing()

    chat_completion = openai.chat.completions.create(
        messages=[{"role": "user", "content": "Say this is a test"}],
        model="gpt-3.5-turbo",
        tools=[
            {
                "type": "function",
                "function": {
                    "name": "test",
                    "description": "test",
                    "parameters": {"type": "object", "properties": {"name": {"type": "string"}}},
                },
            }
        ],
    )

    response = chat_completion.choices[0].message.content
    assert response == "The mock is working! ;)"

    galileo_context.flush()
    payload = mock_traces_client_instance.ingest_traces.call_args[0][0]

    assert len(payload.traces) == 1
    assert payload.traces[0].status_code == 200
    assert len(payload.traces[0].spans) == 1
    assert isinstance(payload.traces[0].spans[0], LlmSpan)
    assert payload.traces[0].spans[0].status_code == 200
    assert payload.traces[0].input == '[{"role": "user", "content": "Say this is a test"}]'
    assert payload.traces[0].spans[0].input == [Message(content="Say this is a test", role=MessageRole.user)]
    assert payload.traces[0].spans[0].output == Message(content="The mock is working! ;)", role=MessageRole.assistant)
    assert payload.traces[0].spans[0].tools == [
        {
            "type": "function",
            "function": {
                "name": "test",
                "description": "test",
                "parameters": {"type": "object", "properties": {"name": {"type": "string"}}},
            },
        }
    ]


@patch("openai.resources.chat.Completions.create")
@patch("galileo.logger.logger.LogStreams")
@patch("galileo.logger.logger.Projects")
@patch("galileo.logger.logger.Traces")
def test_streamed_openai_call(
    mock_traces_client: Mock, mock_projects_client: Mock, mock_logstreams_client: Mock, openai_create
) -> None:
    mock_traces_client_instance = setup_mock_traces_client(mock_traces_client)
    setup_mock_projects_client(mock_projects_client)
    setup_mock_logstreams_client(mock_logstreams_client)

    openai_create.return_value = Stream(
        cast_to=ChatCompletionChunk, client=openai.OpenAI(), response=Response(status_code=200, content=EventStream())
    )

    galileo_context.reset()
    OpenAIGalileo().register_tracing()

    stream = openai.chat.completions.create(
        messages=[{"role": "user", "content": "Say this is a test"}], model="gpt-3.5-turbo", stream=True
    )

    response = ""
    chunk_count = 0
    for chunk in stream:
        response += chunk.choices[0].delta.content or ""
        chunk_count += 1
    assert response == "Hello"
    assert chunk_count == 3

    galileo_context.flush()
    payload = mock_traces_client_instance.ingest_traces.call_args[0][0]

    assert len(payload.traces) == 1
    assert payload.traces[0].status_code == 200

    assert len(payload.traces[0].spans) == 1
    assert isinstance(payload.traces[0].spans[0], LlmSpan)
    assert payload.traces[0].input == '[{"role": "user", "content": "Say this is a test"}]'
    assert payload.traces[0].output == "Hello"
    assert payload.traces[0].spans[0].status_code == 200
    assert payload.traces[0].spans[0].input == [Message(content="Say this is a test", role=MessageRole.user)]
    assert payload.traces[0].spans[0].output == Message(content="Hello", role=MessageRole.assistant)


@patch("openai.resources.chat.Completions.create")
@patch("galileo.logger.logger.LogStreams")
@patch("galileo.logger.logger.Projects")
@patch("galileo.logger.logger.Traces")
def test_openai_api_calls_as_parent_span(
    mock_traces_client: Mock,
    mock_projects_client: Mock,
    mock_logstreams_client: Mock,
    openai_create,
    create_chat_completion,
) -> None:
    mock_traces_client_instance = setup_mock_traces_client(mock_traces_client)
    setup_mock_projects_client(mock_projects_client)
    setup_mock_logstreams_client(mock_logstreams_client)
    openai_create.return_value = create_chat_completion

    # we want reset context and enable tracing for openai plugin
    galileo_context.reset()
    OpenAIGalileo().register_tracing()

    @log()
    def call_openai(model: str = "gpt-3.5-turbo"):
        chat_completion = openai.chat.completions.create(
            messages=[{"role": "user", "content": "Say this is a test"}], model=model
        )
        return chat_completion.choices[0].message.content

    output = call_openai()
    assert output == "The mock is working! ;)"

    galileo_context.flush()

    payload = mock_traces_client_instance.ingest_traces.call_args[0][0]

    assert len(payload.traces) == 1
    assert len(payload.traces[0].spans) == 1
    assert isinstance(payload.traces[0].spans[0], WorkflowSpan)
    assert payload.traces[0].spans[0].input == '{"model": "gpt-3.5-turbo"}'
    assert payload.traces[0].spans[0].output == "The mock is working! ;)"

    assert len(payload.traces[0].spans[0].spans) == 1
    assert isinstance(payload.traces[0].spans[0].spans[0], LlmSpan)
    assert payload.traces[0].spans[0].spans[0].status_code == 200
    assert payload.traces[0].spans[0].spans[0].input == [Message(content="Say this is a test", role=MessageRole.user)]
    assert payload.traces[0].spans[0].spans[0].output == Message(
        content="The mock is working! ;)", role=MessageRole.assistant
    )
    assert payload.traces[0].spans[0].spans[0].model == "gpt-3.5-turbo"


@patch(
    "openai.resources.chat.Completions.create",
    side_effect=openai.OpenAIError("The api_key client option must be set either"),
)
@patch("galileo.logger.logger.LogStreams")
@patch("galileo.logger.logger.Projects")
@patch("galileo.logger.logger.Traces")
def test_openai_error_trace(
    mock_traces_client: Mock, mock_projects_client: Mock, mock_logstreams_client: Mock, openai_create
) -> None:
    mock_traces_client_instance = setup_mock_traces_client(mock_traces_client)
    setup_mock_projects_client(mock_projects_client)
    setup_mock_logstreams_client(mock_logstreams_client)

    # we want reset context and enable tracing for openai plugin
    galileo_context.reset()
    OpenAIGalileo().register_tracing()

    def call_openai(model: str = "gpt-3.5-turbo"):
        chat_completion = openai.chat.completions.create(
            messages=[{"role": "user", "content": "Say this is a test"}], model=model
        )
        return chat_completion.choices[0].message.content

    with pytest.raises(RuntimeError):
        call_openai()

    galileo_context.flush()

    openai_create.assert_called_once()
    mock_traces_client_instance.ingest_traces.assert_called()
    payload = mock_traces_client_instance.ingest_traces.call_args[0][0]
    assert len(payload.traces) == 1


@patch("openai.resources.chat.Completions.create")
@patch("galileo.logger.logger.LogStreams")
@patch("galileo.logger.logger.Projects")
@patch("galileo.logger.logger.Traces")
def test_openai_error_trace_(
    mock_traces_client: Mock, mock_projects_client: Mock, mock_logstreams_client: Mock, openai_create
) -> None:
    mock_traces_client_instance = setup_mock_traces_client(mock_traces_client)
    setup_mock_projects_client(mock_projects_client)
    setup_mock_logstreams_client(mock_logstreams_client)
    openai_create.side_effect = openai.APIStatusError(
        "error",
        response=Response(status_code=401, content=b"", request=Request("GET", "url")),
        body=openai_incorrect_api_key_error(),
    )

    # we want reset context and enable tracing for openai plugin
    galileo_context.reset()
    OpenAIGalileo().register_tracing()

    def call_openai(model: str = "gpt-3.5-turbo"):
        chat_completion = openai.chat.completions.create(
            messages=[{"role": "user", "content": "Say this is a test"}], model=model
        )
        return chat_completion.choices[0].message.content

    with pytest.raises(RuntimeError):
        call_openai()

    galileo_context.flush()

    openai_create.assert_called_once()
    mock_traces_client_instance.ingest_traces.assert_called()
    payload = mock_traces_client_instance.ingest_traces.call_args[0][0]
    assert len(payload.traces) == 1
    assert payload.traces[0].status_code == 401
    assert payload.traces[0].output == "<NoneType response returned from OpenAI>"


@patch(
    "openai.resources.chat.Completions.create",
    side_effect=openai.OpenAIError("The api_key client option must be set either"),
)
@patch("galileo.logger.logger.LogStreams")
@patch("galileo.logger.logger.Projects")
@patch("galileo.logger.logger.Traces")
def test_client_fails_because_openai_error_trace_no_exp(
    mock_traces_client: Mock, mock_projects_client: Mock, mock_logstreams_client: Mock, openai_create
) -> None:
    mock_traces_client_instance = setup_mock_traces_client(mock_traces_client)
    setup_mock_projects_client(mock_projects_client)
    setup_mock_logstreams_client(mock_logstreams_client)

    # we want reset context and enable tracing for openai plugin
    galileo_context.reset()
    OpenAIGalileo().register_tracing()

    @log
    def call_openai(model: str = "gpt-3.5-turbo"):
        chat_completion = openai.chat.completions.create(
            messages=[{"role": "user", "content": "Say this is a test"}], model=model
        )
        return chat_completion.choices[0].message.content

    with pytest.raises(RuntimeError):
        call_openai()

    galileo_context.flush()

    mock_projects_client.assert_called_once()
    openai_create.assert_called_once()
    mock_traces_client_instance.ingest_traces.assert_called()
    payload = mock_traces_client_instance.ingest_traces.call_args[0][0]

    assert len(payload.traces) == 1
    assert len(payload.traces[0].spans) == 1


@patch("openai.resources.chat.Completions.create")
@patch("galileo.logger.logger.LogStreams", side_effect=Exception("error"))
@patch("galileo.logger.logger.Projects", side_effect=Exception("error"))
@patch("galileo.logger.logger.Traces")
def test_galileo_api_client_transport_error_not_blocking_user_code(
    mock_traces_client: Mock,
    mock_projects_client: Mock,
    mock_logstreams_client: Mock,
    openai_create,
    create_chat_completion,
) -> None:
    m = mock_traces_client.return_value
    m.get_project_by_name = AsyncMock(side_effect=httpx.HTTPError("http error"))
    m.get_log_stream_by_name = AsyncMock(side_effect=httpx.HTTPError("http error"))
    m.ingest_traces = AsyncMock(side_effect=httpx.HTTPError("http error"))
    m.ingest_traces = AsyncMock(side_effect=httpx.HTTPError("http error"))

    setup_mock_projects_client(mock_projects_client)
    setup_mock_logstreams_client(mock_logstreams_client)
    openai_create.return_value = create_chat_completion
    # we want reset context and enable tracing for openai plugin
    galileo_context.reset()
    OpenAIGalileo().register_tracing()

    @log()
    def call_openai(model: str = "gpt-3.5-turbo"):
        chat_completion = openai.chat.completions.create(
            messages=[{"role": "user", "content": "The mock is working! ;)"}], model=model
        )
        return chat_completion.choices[0].message.content

    assert call_openai() == "The mock is working! ;)"
    galileo_context.flush()

    mock_projects_client.assert_called_once()
    openai_create.assert_called_once()


@patch("openai.resources.chat.Completions.create")
@patch("galileo.logger.logger.LogStreams")
@patch("galileo.logger.logger.Projects")
@patch("galileo.logger.logger.Traces")
def test_openai_calls_in_active_trace(
    mock_traces_client: Mock,
    mock_projects_client: Mock,
    mock_logstreams_client: Mock,
    openai_create,
    create_chat_completion,
) -> None:
    mock_traces_client_instance = setup_mock_traces_client(mock_traces_client)
    setup_mock_projects_client(mock_projects_client)
    setup_mock_logstreams_client(mock_logstreams_client)
    openai_create.return_value = create_chat_completion

    galileo_context.reset()
    OpenAIGalileo().register_tracing()

    logger = galileo_context.get_logger_instance()
    logger.start_trace("test trace")

    openai.chat.completions.create(messages=[{"role": "user", "content": "Say this is a test"}], model="gpt-4o-mini")
    openai.chat.completions.create(
        messages=[{"role": "user", "content": "Say this is a second test"}], model="gpt-4o-mini"
    )

    logger.conclude(output="trace completed", duration_ns=1000)
    logger.flush()

    payload = mock_traces_client_instance.ingest_traces.call_args[0][0]

    assert len(payload.traces) == 1
    assert len(payload.traces[0].spans) == 2
    assert payload.traces[0].spans[0].type == "llm"
    assert payload.traces[0].spans[1].type == "llm"
