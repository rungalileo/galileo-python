from unittest.mock import Mock, patch

from pytest_mock import MockerFixture

from galileo import galileo_context
from galileo_core.schemas.shared.traces.trace import LlmSpan
from tests.conftest import MockedCompletion
from tests.testutils.setup import setup_mock_core_api_client, setup_mock_logstreams_client, setup_mock_projects_client


@patch("galileo.logger.LogStreams")
@patch("galileo.logger.Projects")
@patch("galileo.logger.GalileoCoreApiClient")
def test_basic_openai_call(
    mock_core_api_client: Mock, mock_projects_client: Mock, mock_logstreams_client: Mock, mocker: MockerFixture
):
    mock_core_api_instance = setup_mock_core_api_client(mock_core_api_client)
    setup_mock_projects_client(mock_projects_client)
    setup_mock_logstreams_client(mock_logstreams_client)

    mocker.patch("openai.resources.chat.completions.Completions.create", side_effect=MockedCompletion())

    # It's important to import openai integration, after we mock openai call
    from galileo.openai import openai  # OpenAI integration

    chat_completion = openai.chat.completions.create(
        messages=[{"role": "user", "content": "Say this is a test"}], model="gpt-4o"
    )

    assert chat_completion.choices[0].message.content == "This is a mocked message."

    galileo_context.flush()

    payload = mock_core_api_instance.ingest_traces_sync.call_args[0][0]

    assert len(payload.traces) == 1
    assert len(payload.traces[0].spans) == 1
    assert isinstance(payload.traces[0].spans[0], LlmSpan)
    assert payload.traces[0].input[0].content == "Say this is a test"
    assert payload.traces[0].spans[0].output == {"content": "This is a mocked message.", "role": None}
