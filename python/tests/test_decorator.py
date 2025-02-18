from unittest.mock import AsyncMock, Mock, patch

from uuid import UUID

from galileo import log, galileo_context
from galileo.schema.trace import TracesIngestRequest, TracesIngestResponse
from galileo_core.schemas.shared.traces.trace import Trace, LlmSpan, WorkflowSpan


def setup_mock_api_client(mock_api_client: Mock):
    mock_instance = mock_api_client.return_value
    mock_ingest_traces_sync = AsyncMock(return_value={})
    mock_ingest_traces_async = AsyncMock(return_value={})
    mock_instance.get_project_by_name = AsyncMock(return_value={"id": UUID("6c4e3f7e-4a9a-4e7e-8c1f-3a9a3a9a3a9a")})
    mock_instance.get_log_stream_by_name = AsyncMock(return_value={"id": UUID("6c4e3f7e-4a9a-4e7e-8c1f-3a9a3a9a3a9b")})
    mock_instance.ingest_traces_sync = mock_ingest_traces_sync
    mock_instance.ingest_traces = mock_ingest_traces_async
    return mock_instance


@patch("galileo.logger.ApiClient")
def test_decorator_llm_span(mock_api_client: Mock) -> None:
    mock_instance = setup_mock_api_client(mock_api_client)

    @log(span_type="llm")
    def llm_call(query: str):
        return "response"

    output = llm_call(query="input")
    galileo_context.flush()

    payload = mock_instance.ingest_traces_sync.call_args[0][0]

    assert len(payload.traces) == 1
    assert len(payload.traces[0].spans) == 1
    assert type(payload.traces[0].spans[0]) == LlmSpan
    assert payload.traces[0].input == {"args": [], "kwargs": {"query": "input"}}
    assert payload.traces[0].spans[0].input == {"args": [], "kwargs": {"query": "input"}}
    assert payload.traces[0].spans[0].output == output


@patch("galileo.logger.ApiClient")
def test_decorator_nested_span(mock_api_client: Mock) -> None:
    mock_instance = setup_mock_api_client(mock_api_client)

    @log(span_type="llm")
    def llm_call(query: str):
        return "response"

    @log()
    def nested_call(nested_query: str):
        return llm_call(query=nested_query)

    output = nested_call(nested_query="input")
    galileo_context.flush()

    payload = mock_instance.ingest_traces_sync.call_args[0][0]

    assert len(payload.traces) == 1
    assert len(payload.traces[0].spans) == 1
    assert len(payload.traces[0].spans[0].spans) == 1
    assert type(payload.traces[0].spans[0]) == WorkflowSpan
    assert type(payload.traces[0].spans[0].spans[0]) == LlmSpan
    assert payload.traces[0].input == {"args": [], "kwargs": {"nested_query": "input"}}
    assert payload.traces[0].spans[0].spans[0].input == {"args": [], "kwargs": {"query": "input"}}
    assert payload.traces[0].spans[0].output == output
    assert payload.traces[0].spans[0].spans[0].output == output


@patch("galileo.logger.ApiClient")
def test_decorator_multiple_nested_spans(mock_api_client: Mock) -> None:
    mock_instance = setup_mock_api_client(mock_api_client)

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

    payload = mock_instance.ingest_traces_sync.call_args[0][0]

    assert len(payload.traces) == 1
    assert len(payload.traces[0].spans) == 1
    assert len(payload.traces[0].spans[0].spans) == 2
    assert type(payload.traces[0].spans[0]) == WorkflowSpan
    assert type(payload.traces[0].spans[0].spans[0]) == LlmSpan
    assert type(payload.traces[0].spans[0].spans[1]) == LlmSpan
    assert payload.traces[0].input == {"args": [], "kwargs": {"nested_query": "input"}}
    assert payload.traces[0].spans[0].spans[0].input == {"args": [], "kwargs": {"query": "input"}}
    assert payload.traces[0].spans[0].output == output
    assert payload.traces[0].spans[0].spans[0].output == "response"
