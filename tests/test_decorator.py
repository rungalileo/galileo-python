from unittest.mock import MagicMock, Mock, patch

from galileo import galileo_context, log
from galileo_core.schemas.shared.traces.trace import LlmSpan, WorkflowSpan
from tests.testutils.setup import setup_mock_core_api_client, setup_mock_logstreams_client, setup_mock_projects_client


@patch("galileo.logger.LogStreams")
@patch("galileo.logger.Projects")
@patch("galileo.logger.GalileoCoreApiClient")
def test_decorator_llm_span(
    mock_core_api_client: Mock, mock_projects_client: Mock, mock_logstreams_client: Mock
) -> None:
    mock_core_api_instance = setup_mock_core_api_client(mock_core_api_client)
    setup_mock_projects_client(mock_projects_client)
    setup_mock_logstreams_client(mock_logstreams_client)

    @log(span_type="llm")
    def llm_call(query: str):
        return "response"

    output = llm_call(query="input")
    galileo_context.flush()

    payload = mock_core_api_instance.ingest_traces_sync.call_args[0][0]

    assert len(payload.traces) == 1
    assert len(payload.traces[0].spans) == 1
    assert isinstance(payload.traces[0].spans[0], LlmSpan)
    assert payload.traces[0].input == {"query": "input"}
    assert payload.traces[0].spans[0].input == {"query": "input"}
    assert payload.traces[0].spans[0].output == output


@patch("galileo.logger.LogStreams")
@patch("galileo.logger.Projects")
@patch("galileo.logger.GalileoCoreApiClient")
def test_decorator_nested_span(
    mock_core_api_client: Mock, mock_projects_client: Mock, mock_logstreams_client: Mock
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
    assert payload.traces[0].input == {"nested_query": "input"}
    assert payload.traces[0].spans[0].spans[0].input == {"query": "input"}
    assert payload.traces[0].spans[0].output == output
    assert payload.traces[0].spans[0].spans[0].output == output


@patch("galileo.logger.LogStreams")
@patch("galileo.logger.Projects")
@patch("galileo.logger.GalileoCoreApiClient")
def test_decorator_multiple_nested_spans(
    mock_core_api_client: Mock, mock_projects_client: Mock, mock_logstreams_client: Mock
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
    assert payload.traces[0].input == {"nested_query": "input"}
    assert payload.traces[0].spans[0].spans[0].input == {"query": "input"}
    assert payload.traces[0].spans[0].output == output
    assert payload.traces[0].spans[0].spans[0].output == "response"
