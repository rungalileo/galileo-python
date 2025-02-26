from unittest.mock import Mock, patch

from httpx import Response
from openai import Stream
from openai.types.chat import ChatCompletionChunk

from galileo import galileo_context, log
from galileo.openai import OpenAIGalileo, openai
from galileo_core.schemas.logging.llm import Message, MessageRole
from galileo_core.schemas.logging.span import LlmSpan, WorkflowSpan
from tests.testutils.setup import setup_mock_core_api_client, setup_mock_logstreams_client, setup_mock_projects_client
from tests.testutils.streaming import EventStream


@patch("openai.resources.chat.Completions.create")
@patch("galileo.logger.LogStreams")
@patch("galileo.logger.Projects")
@patch("galileo.logger.GalileoCoreApiClient")
def test_basic_openai_call(
    mock_core_api_client: Mock,
    mock_projects_client: Mock,
    mock_logstreams_client: Mock,
    openai_create,
    create_chat_completion,
):
    mock_core_api_instance = setup_mock_core_api_client(mock_core_api_client)
    setup_mock_projects_client(mock_projects_client)
    setup_mock_logstreams_client(mock_logstreams_client)
    openai_create.return_value = create_chat_completion

    galileo_context.reset()
    OpenAIGalileo().register_tracing()

    chat_completion = openai.chat.completions.create(
        messages=[{"role": "user", "content": "Say this is a test"}], model="gpt-3.5-turbo"
    )

    response = chat_completion.choices[0].message.content
    assert response == "The mock is working! ;)"

    galileo_context.flush()
    payload = mock_core_api_instance.ingest_traces_sync.call_args[0][0]

    assert len(payload.traces) == 1
    assert len(payload.traces[0].spans) == 1
    assert isinstance(payload.traces[0].spans[0], LlmSpan)
    assert payload.traces[0].input == '[{"role": "user", "content": "Say this is a test"}]'
    assert payload.traces[0].spans[0].input == [Message(content="Say this is a test", role=MessageRole.user)]
    assert payload.traces[0].spans[0].output == Message(content="The mock is working! ;)", role=MessageRole.assistant)


@patch("openai.resources.chat.Completions.create")
@patch("galileo.logger.LogStreams")
@patch("galileo.logger.Projects")
@patch("galileo.logger.GalileoCoreApiClient")
def test_streamed_openai_call(
    mock_core_api_client: Mock, mock_projects_client: Mock, mock_logstreams_client: Mock, openai_create
):
    mock_core_api_instance = setup_mock_core_api_client(mock_core_api_client)
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
    payload = mock_core_api_instance.ingest_traces_sync.call_args[0][0]

    assert len(payload.traces) == 1
    assert len(payload.traces[0].spans) == 1
    assert isinstance(payload.traces[0].spans[0], LlmSpan)
    assert payload.traces[0].input[0].content == "Say this is a test"
    assert payload.traces[0].spans[0].output == "Hello"


@patch("openai.resources.chat.Completions.create")
@patch("galileo.logger.LogStreams")
@patch("galileo.logger.Projects")
@patch("galileo.logger.GalileoCoreApiClient")
def test_openai_api_calls_as_parent_span(
    mock_core_api_client: Mock,
    mock_projects_client: Mock,
    mock_logstreams_client: Mock,
    openai_create,
    create_chat_completion,
):
    mock_core_api_instance = setup_mock_core_api_client(mock_core_api_client)
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

    payload = mock_core_api_instance.ingest_traces_sync.call_args[0][0]

    assert len(payload.traces) == 1
    assert len(payload.traces[0].spans) == 1
    assert isinstance(payload.traces[0].spans[0], WorkflowSpan)
    assert payload.traces[0].spans[0].input == '{"model": "gpt-3.5-turbo"}'
    assert payload.traces[0].spans[0].output == "The mock is working! ;)"

    assert len(payload.traces[0].spans[0].spans) == 1
    assert isinstance(payload.traces[0].spans[0].spans[0], LlmSpan)
    assert payload.traces[0].spans[0].spans[0].input == [Message(content="Say this is a test", role=MessageRole.user)]
    assert payload.traces[0].spans[0].spans[0].output == Message(
        content="The mock is working! ;)", role=MessageRole.assistant
    )
    assert payload.traces[0].spans[0].spans[0].model == "gpt-3.5-turbo"
