from unittest.mock import AsyncMock, Mock, patch

import httpx
import pytest
from httpx import Request, Response
from openai import Stream
from openai.types.chat import ChatCompletionChunk
from openai.types.responses import ResponseCompletedEvent

from galileo import Message, MessageRole, galileo_context, log
from galileo.openai import OpenAIGalileo, openai
from galileo_core.schemas.logging.span import LlmSpan, WorkflowSpan
from tests.testutils.setup import setup_mock_logstreams_client, setup_mock_projects_client, setup_mock_traces_client
from tests.testutils.streaming import EventStream, ResponsesEventStream


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
    assert payload.traces[0].input == '{"messages": [{"content": "Say this is a test", "role": "user"}]}'
    assert (
        payload.traces[0].output
        == '{"messages": [{"content": "Say this is a test", "role": "user"}, {"content": "The mock is working! ;)", "role": "assistant"}]}'
    )
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
    assert payload.traces[0].input == '{"messages": [{"content": "Say this is a test", "role": "user"}]}'
    assert (
        payload.traces[0].output
        == '{"messages": [{"content": "Say this is a test", "role": "user"}, {"content": "Hello", "role": "assistant"}]}'
    )
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
    assert (
        payload.traces[0].output
        == '{"messages": [{"content": "Say this is a test", "role": "user"}, {"content": "<NoneType response returned from OpenAI>", "role": "assistant"}]}'
    )


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


@patch("openai.resources.chat.Completions.create")
@patch("galileo.logger.logger.LogStreams")
@patch("galileo.logger.logger.Projects")
@patch("galileo.logger.logger.Traces")
def test_chat_completions_multiple_messages(
    mock_traces_client: Mock,
    mock_projects_client: Mock,
    mock_logstreams_client: Mock,
    openai_create,
    create_chat_completion,
) -> None:
    """Test Chat Completions API with multiple messages in conversation."""
    mock_traces_client_instance = setup_mock_traces_client(mock_traces_client)
    setup_mock_projects_client(mock_projects_client)
    setup_mock_logstreams_client(mock_logstreams_client)
    openai_create.return_value = create_chat_completion

    galileo_context.reset()
    OpenAIGalileo().register_tracing()

    input_messages = [
        {"role": "user", "content": "What's the weather like today?"},
        {
            "role": "assistant",
            "content": "I'd be happy to help you with the weather! However, I don't have access to real-time weather data.",
        },
        {"role": "user", "content": "Can you check the weather for New York?"},
    ]

    response = openai.chat.completions.create(messages=input_messages, model="gpt-4o")

    response_text = response.choices[0].message.content
    assert response_text == "The mock is working! ;)"

    galileo_context.flush()
    payload = mock_traces_client_instance.ingest_traces.call_args[0][0]

    assert len(payload.traces) == 1
    assert payload.traces[0].status_code == 200
    assert len(payload.traces[0].spans) == 1
    assert isinstance(payload.traces[0].spans[0], LlmSpan)
    assert payload.traces[0].spans[0].status_code == 200

    expected_input = '{"messages": [{"content": "What\'s the weather like today?", "role": "user"}, {"content": "I\'d be happy to help you with the weather! However, I don\'t have access to real-time weather data.", "role": "assistant"}, {"content": "Can you check the weather for New York?", "role": "user"}]}'
    assert payload.traces[0].input == expected_input

    expected_output = '{"messages": [{"content": "What\'s the weather like today?", "role": "user"}, {"content": "I\'d be happy to help you with the weather! However, I don\'t have access to real-time weather data.", "role": "assistant"}, {"content": "Can you check the weather for New York?", "role": "user"}, {"content": "The mock is working! ;)", "role": "assistant"}]}'
    assert payload.traces[0].output == expected_output

    expected_span_input = [
        Message(content="What's the weather like today?", role=MessageRole.user),
        Message(
            content="I'd be happy to help you with the weather! However, I don't have access to real-time weather data.",
            role=MessageRole.assistant,
        ),
        Message(content="Can you check the weather for New York?", role=MessageRole.user),
    ]
    assert payload.traces[0].spans[0].input == expected_span_input
    assert payload.traces[0].spans[0].output == Message(content="The mock is working! ;)", role=MessageRole.assistant)


@patch("openai.resources.responses.Responses.create")
@patch("galileo.logger.logger.LogStreams")
@patch("galileo.logger.logger.Projects")
@patch("galileo.logger.logger.Traces")
def test_basic_responses_api_call(
    mock_traces_client: Mock,
    mock_projects_client: Mock,
    mock_logstreams_client: Mock,
    openai_create,
    create_responses_response,
) -> None:
    mock_traces_client_instance = setup_mock_traces_client(mock_traces_client)
    setup_mock_projects_client(mock_projects_client)
    setup_mock_logstreams_client(mock_logstreams_client)
    openai_create.return_value = create_responses_response

    galileo_context.reset()
    OpenAIGalileo().register_tracing()

    response = openai.responses.create(input="Say this is a test", model="gpt-4o")

    response_text = response.output_text
    assert response_text == "This is a test response"

    galileo_context.flush()
    payload = mock_traces_client_instance.ingest_traces.call_args[0][0]

    assert len(payload.traces) == 1
    assert payload.traces[0].status_code == 200
    assert len(payload.traces[0].spans) == 1
    assert isinstance(payload.traces[0].spans[0], LlmSpan)
    assert payload.traces[0].spans[0].status_code == 200
    assert payload.traces[0].input == '{"messages": [{"content": "Say this is a test", "role": "user"}]}'
    assert (
        payload.traces[0].output
        == '{"messages": [{"content": "Say this is a test", "role": "user"}, {"content": "This is a test response", "role": "assistant"}]}'
    )
    assert payload.traces[0].spans[0].input == [Message(content="Say this is a test", role=MessageRole.user)]
    assert payload.traces[0].spans[0].output == Message(content="This is a test response", role=MessageRole.assistant)


@patch("openai.resources.responses.Responses.create")
@patch("galileo.logger.logger.LogStreams")
@patch("galileo.logger.logger.Projects")
@patch("galileo.logger.logger.Traces")
def test_responses_api_with_tools(
    mock_traces_client: Mock,
    mock_projects_client: Mock,
    mock_logstreams_client: Mock,
    openai_create,
    create_responses_response_with_tools,
) -> None:
    mock_traces_client_instance = setup_mock_traces_client(mock_traces_client)
    setup_mock_projects_client(mock_projects_client)
    setup_mock_logstreams_client(mock_logstreams_client)
    openai_create.return_value = create_responses_response_with_tools

    galileo_context.reset()
    OpenAIGalileo().register_tracing()

    openai.responses.create(
        input="What's the weather like?",
        model="gpt-4o",
        tools=[
            {
                "type": "function",
                "name": "get_weather",
                "description": "Get the current weather",
                "parameters": {
                    "type": "object",
                    "properties": {"location": {"type": "string"}},
                    "required": ["location"],
                },
            }
        ],
    )

    galileo_context.flush()
    payload = mock_traces_client_instance.ingest_traces.call_args[0][0]

    assert len(payload.traces) == 1
    assert payload.traces[0].status_code == 200
    assert len(payload.traces[0].spans) == 1
    assert isinstance(payload.traces[0].spans[0], LlmSpan)
    assert payload.traces[0].spans[0].tools == [
        {
            "type": "function",
            "name": "get_weather",
            "description": "Get the current weather",
            "parameters": {"type": "object", "properties": {"location": {"type": "string"}}, "required": ["location"]},
        }
    ]

    assert payload.traces[0].spans[0].output.tool_calls is not None
    assert len(payload.traces[0].spans[0].output.tool_calls) == 1
    assert payload.traces[0].spans[0].output.tool_calls[0].function.name == "get_weather"
    assert payload.traces[0].spans[0].output.tool_calls[0].function.arguments == '{"location": "San Francisco"}'
    assert payload.traces[0].spans[0].output.tool_calls[0].id == "fc_test456"


@patch("openai.resources.responses.Responses.create")
@patch("galileo.logger.logger.LogStreams")
@patch("galileo.logger.logger.Projects")
@patch("galileo.logger.logger.Traces")
def test_responses_api_multiple_messages(
    mock_traces_client: Mock,
    mock_projects_client: Mock,
    mock_logstreams_client: Mock,
    openai_create,
    create_responses_response,
) -> None:
    """Test Responses API with multiple messages in conversation."""
    mock_traces_client_instance = setup_mock_traces_client(mock_traces_client)
    setup_mock_projects_client(mock_projects_client)
    setup_mock_logstreams_client(mock_logstreams_client)
    openai_create.return_value = create_responses_response

    galileo_context.reset()
    OpenAIGalileo().register_tracing()

    input_messages = [
        {"role": "user", "content": "What's the weather like today?"},
        {
            "role": "assistant",
            "content": "I'd be happy to help you with the weather! However, I don't have access to real-time weather data.",
        },
        {"role": "user", "content": "Can you check the weather for New York?"},
    ]

    response = openai.responses.create(input=input_messages, model="gpt-4o")

    assert response.output is not None
    assert len(response.output) == 1
    assert response.output[0].role == "assistant"

    galileo_context.flush()
    payload = mock_traces_client_instance.ingest_traces.call_args[0][0]

    assert len(payload.traces) == 1
    assert payload.traces[0].status_code == 200
    assert len(payload.traces[0].spans) == 1
    assert isinstance(payload.traces[0].spans[0], LlmSpan)
    assert payload.traces[0].spans[0].status_code == 200

    expected_input = '{"messages": [{"content": "What\'s the weather like today?", "role": "user"}, {"content": "I\'d be happy to help you with the weather! However, I don\'t have access to real-time weather data.", "role": "assistant"}, {"content": "Can you check the weather for New York?", "role": "user"}]}'
    assert payload.traces[0].input == expected_input

    expected_output = '{"messages": [{"content": "What\'s the weather like today?", "role": "user"}, {"content": "I\'d be happy to help you with the weather! However, I don\'t have access to real-time weather data.", "role": "assistant"}, {"content": "Can you check the weather for New York?", "role": "user"}, {"content": "This is a test response", "role": "assistant"}]}'
    assert payload.traces[0].output == expected_output

    expected_span_input = [
        Message(content="What's the weather like today?", role=MessageRole.user),
        Message(
            content="I'd be happy to help you with the weather! However, I don't have access to real-time weather data.",
            role=MessageRole.assistant,
        ),
        Message(content="Can you check the weather for New York?", role=MessageRole.user),
    ]
    assert payload.traces[0].spans[0].input == expected_span_input
    assert payload.traces[0].spans[0].output == Message(content="This is a test response", role=MessageRole.assistant)


@patch("openai.resources.responses.Responses.create")
@patch("galileo.logger.logger.LogStreams")
@patch("galileo.logger.logger.Projects")
@patch("galileo.logger.logger.Traces")
def test_responses_api_streaming(
    mock_traces_client: Mock, mock_projects_client: Mock, mock_logstreams_client: Mock, openai_create
) -> None:
    """Test Responses API with streaming events."""
    mock_traces_client_instance = setup_mock_traces_client(mock_traces_client)
    setup_mock_projects_client(mock_projects_client)
    setup_mock_logstreams_client(mock_logstreams_client)

    openai_create.return_value = Stream(
        cast_to=ResponseCompletedEvent,
        client=openai.OpenAI(),
        response=Response(status_code=200, content=ResponsesEventStream()),
    )

    galileo_context.reset()
    OpenAIGalileo().register_tracing()

    stream = openai.responses.create(input="Say hello", model="gpt-4o", stream=True)

    event_count = 0
    completed_event = None
    for event in stream:
        event_count += 1
        if hasattr(event, "type") and event.type == "response.completed":
            completed_event = event

    assert event_count >= 1
    assert completed_event is not None
    assert completed_event.response.status == "completed"

    galileo_context.flush()
    payload = mock_traces_client_instance.ingest_traces.call_args[0][0]

    assert len(payload.traces) == 1
    assert payload.traces[0].status_code == 200
    assert len(payload.traces[0].spans) == 1
    assert isinstance(payload.traces[0].spans[0], LlmSpan)
    assert payload.traces[0].spans[0].status_code == 200

    assert payload.traces[0].input == '{"messages": [{"content": "Say hello", "role": "user"}]}'
    assert (
        payload.traces[0].output
        == '{"messages": [{"content": "Say hello", "role": "user"}, {"content": "This is a test response", "role": "assistant"}]}'
    )

    assert payload.traces[0].spans[0].input == [Message(content="Say hello", role=MessageRole.user)]
    assert payload.traces[0].spans[0].output == Message(content="This is a test response", role=MessageRole.assistant)
