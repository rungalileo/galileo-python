from unittest.mock import Mock, patch
import httpx
from httpx import Response
import datetime
from unittest.mock import Mock, patch

import pytest
from openai import Stream
from openai.types import CompletionUsage
from openai.types.create_embedding_response import Usage
from pytest_mock import MockerFixture

from openai.types.chat import ChatCompletionMessage
from openai.types.chat.chat_completion import ChatCompletion, Choice
from openai.types.chat.chat_completion_chunk import ChatCompletionChunk, ChoiceDelta
from openai.types.chat.chat_completion_chunk import Choice as StreamChoice

from galileo import galileo_context, log
from galileo.openai import OpenAIGalileo, openai
from galileo_core.schemas.shared.traces.trace import LlmSpan, WorkflowSpan
from openai.types.chat import ChatCompletionChunk
from tenacity import retry

from tests.testutils.setup import setup_mock_core_api_client, setup_mock_logstreams_client, setup_mock_projects_client

@patch("openai.resources.chat.Completions.create")
@patch("galileo.logger.LogStreams")
@patch("galileo.logger.Projects")
@patch("galileo.logger.GalileoCoreApiClient")
def test_basic_openai_call(
    mock_core_api_client: Mock, mock_projects_client: Mock, mock_logstreams_client: Mock, openai_create, create_chat_completion
):
    mock_core_api_instance = setup_mock_core_api_client(mock_core_api_client)
    setup_mock_projects_client(mock_projects_client)
    setup_mock_logstreams_client(mock_logstreams_client)
    openai_create.return_value = create_chat_completion

    galileo_context.reset()
    OpenAIGalileo().register_tracing()

    chat_completion = openai.chat.completions.create(
        messages=[{"role": "user", "content": "Say this is a test"}], model="gpt-4o"
    )

    response = chat_completion.choices[0].message.content
    assert response == "The mock is working! ;)"

    galileo_context.flush()
    payload = mock_core_api_instance.ingest_traces_sync.call_args[0][0]

    assert len(payload.traces) == 1
    assert len(payload.traces[0].spans) == 1
    assert isinstance(payload.traces[0].spans[0], LlmSpan)
    assert payload.traces[0].input[0].content == "Say this is a test"
    assert payload.traces[0].spans[0].output.content == "The mock is working! ;)"



def create_stream_chat_completion():
    chunks = ["chunk1", "chunk2", "chunk3", "chunk4"]
    for token in chunks:
        yield ChatCompletionChunk(
            id="foo",
            model="gpt-3.5-turbo",
            object="chat.completion.chunk",
            choices=[
                StreamChoice(
                    index=0,
                    finish_reason=None,
                    delta=ChoiceDelta(
                        content=token,
                        role="assistant",
                    )
                ),
            ],
            created=int(datetime.datetime.now().timestamp()),
        )


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

    openai_create.return_value = Stream(cast_to=object, client=openai.OpenAI(), response=Response(status_code=201, content=create_stream_chat_completion()))

    galileo_context.reset()
    OpenAIGalileo().register_tracing()

    stream = openai.chat.completions.create(
        messages=[{"role": "user", "content": "Say this is a test"}], model="gpt-4o",
        stream=True,
    )

    response = ""
    chunk_count = 0
    for chunk in stream:
        response += (chunk.choices[0].delta.content or "")
        chunk_count += 1
    assert response == ""
    assert chunk_count == 4

    # galileo_context.flush()
    # payload = mock_core_api_instance.ingest_traces_sync.call_args[0][0]
    #
    # assert len(payload.traces) == 1
    # assert len(payload.traces[0].spans) == 1
    # assert isinstance(payload.traces[0].spans[0], LlmSpan)
    # assert payload.traces[0].input[0].content == "Say this is a test"
    # assert payload.traces[0].spans[0].output.content == "The mock is working! ;)"


# @patch("galileo.logger.LogStreams")
# @patch("galileo.logger.Projects")
# @patch("galileo.logger.GalileoCoreApiClient")
# def test_openai_api_calls_as_parent_span(
#     mock_core_api_client: Mock, mock_projects_client: Mock, mock_logstreams_client: Mock, mocker: MockerFixture
# ):
#     mock_core_api_instance = setup_mock_core_api_client(mock_core_api_client)
#     setup_mock_projects_client(mock_projects_client)
#     setup_mock_logstreams_client(mock_logstreams_client)
#
#     mocker.patch("openai.resources.chat.completions.Completions.create", side_effect=MockedCompletion())
#
#     # we want reset context and enable tracing for openai plugin
#     galileo_context.reset()
#     OpenAIGalileo().register_tracing()
#
#     @log()
#     def call_openai():
#         chat_completion = openai.chat.completions.create(
#             messages=[{"role": "user", "content": "Say this is a test"}], model="gpt-4o"
#         )
#         return chat_completion.choices[0].message.content
#
#     assert call_openai() == "This is a mocked message."
#     galileo_context.flush()
#
#     payload = mock_core_api_instance.ingest_traces_sync.call_args[0][0]
#
#     assert len(payload.traces) == 1
#     assert len(payload.traces[0].spans) == 1
#     assert isinstance(payload.traces[0].spans[0], WorkflowSpan)
#     assert payload.traces[0].spans[0].output == "This is a mocked message."
#
#     assert len(payload.traces[0].spans[0].spans) == 1
#     assert isinstance(payload.traces[0].spans[0].spans[0], LlmSpan)
#     assert payload.traces[0].spans[0].spans[0].input[0].content == "Say this is a test"
#     assert payload.traces[0].spans[0].spans[0].model == "test_model"
#     assert payload.traces[0].spans[0].spans[0].parent is not None
