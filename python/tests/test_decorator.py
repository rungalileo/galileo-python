from json import dumps
from unittest.mock import AsyncMock, Mock, patch

import pytest

from uuid import UUID

from galileo import log, galileo_context
from galileo.schema.trace import TracesIngestRequest, TracesIngestResponse
from galileo_core.schemas.shared.traces.trace import Trace, LlmSpan, WorkflowSpan

from galileo_core.schemas.shared.workflows.node_type import NodeType


def setup_mock_api_client(mock_api_client: Mock):
    mock_instance = mock_api_client.return_value
    mock_ingest_traces_sync = AsyncMock(return_value={})
    mock_ingest_traces_async = AsyncMock(return_value={})
    mock_instance.get_project_by_name = AsyncMock(
        return_value={"id": UUID("6c4e3f7e-4a9a-4e7e-8c1f-3a9a3a9a3a9a")}
    )
    mock_instance.get_log_stream_by_name = AsyncMock(
        return_value={"id": UUID("6c4e3f7e-4a9a-4e7e-8c1f-3a9a3a9a3a9b")}
    )
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
    assert payload.traces[0].input == {"query": "input"}
    assert payload.traces[0].spans[0].input == {"query": "input"}
    assert payload.traces[0].spans[0].output == output


@patch("galileo.logger.ApiClient")
def test_decorator_llm_span_custom_params(mock_api_client: Mock) -> None:
    mock_instance = setup_mock_api_client(mock_api_client)

    @log(
        span_type="llm",
        name="custom-name",
        params={"input": "query", "temperature": lambda x: 1.0},
    )
    def llm_call(query: str, model: str = "model_name"):
        return "response"

    output = llm_call(query="my query")
    galileo_context.flush()

    payload = mock_instance.ingest_traces_sync.call_args[0][0]

    assert len(payload.traces) == 1
    assert len(payload.traces[0].spans) == 1
    assert type(payload.traces[0].spans[0]) == LlmSpan
    assert payload.traces[0].input == "my query"
    assert payload.traces[0].spans[0].input == "my query"
    assert payload.traces[0].spans[0].temperature == 1.0
    assert payload.traces[0].spans[0].model == "model_name"
    assert payload.traces[0].spans[0].output == output
    assert payload.traces[0].spans[0].name == "custom-name"


@patch("galileo.logger.ApiClient")
def test_decorator_nested_span(mock_api_client: Mock) -> None:
    mock_instance = setup_mock_api_client(mock_api_client)

    @log(span_type="llm")
    def llm_call(query: str):
        return "response"

    @log()
    def nested_call(nested_query: str, param_to_ignore: str = "default value"):
        return llm_call(query=nested_query)

    output = nested_call(nested_query="input")
    galileo_context.flush()

    payload = mock_instance.ingest_traces_sync.call_args[0][0]

    assert len(payload.traces) == 1
    assert len(payload.traces[0].spans) == 1
    assert len(payload.traces[0].spans[0].spans) == 1
    assert type(payload.traces[0].spans[0]) == WorkflowSpan
    assert type(payload.traces[0].spans[0].spans[0]) == LlmSpan
    assert payload.traces[0].input == {
        "nested_query": "input",
        "param_to_ignore": "default value",
    }
    assert payload.traces[0].spans[0].input == {
        "nested_query": "input",
        "param_to_ignore": "default value",
    }
    assert payload.traces[0].spans[0].spans[0].input == {"query": "input"}
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
    assert payload.traces[0].input == {"nested_query": "input"}
    assert payload.traces[0].spans[0].spans[0].input == {"query": "input"}
    assert payload.traces[0].spans[0].output == output
    assert payload.traces[0].spans[0].spans[0].output == "response"


@patch("galileo.logger.ApiClient")
def test_context_manager(mock_api_client: Mock) -> None:
    mock_instance = setup_mock_api_client(mock_api_client)

    @log(span_type="llm")
    def llm_call(query: str):
        return "response"

    @log(name="wrapper-span")
    def nested_call(nested_query: str):
        llm_call(query=nested_query)
        llm_call(query=nested_query)
        return "new response"

    with galileo_context():
        output = nested_call(nested_query="input")

    payload = mock_instance.ingest_traces_sync.call_args[0][0]

    assert len(payload.traces) == 1
    assert len(payload.traces[0].spans) == 1
    assert len(payload.traces[0].spans[0].spans) == 2
    assert type(payload.traces[0].spans[0]) == WorkflowSpan
    assert type(payload.traces[0].spans[0].spans[0]) == LlmSpan
    assert type(payload.traces[0].spans[0].spans[1]) == LlmSpan
    assert payload.traces[0].input == {"nested_query": "input"}
    assert payload.traces[0].spans[0].input == {"nested_query": "input"}
    assert payload.traces[0].spans[0].output == "new response"
    assert payload.traces[0].spans[0].spans[0].output == "response"
    assert payload.traces[0].spans[0].spans[0].input == {"query": "input"}


@patch("galileo.logger.ApiClient")
def test_context_manager_model_param(mock_api_client: Mock) -> None:
    mock_instance = setup_mock_api_client(mock_api_client)

    @log(span_type="llm", params={"model": "model_attr"}, name="llm-span")
    def llm_call(query: str, model_attr: str = "gpt4o"):
        return "response"

    @log(span_type="llm", params={"model": "model_attr"})
    def llm_call_2(query: str, model: str = "gpt4o", model_attr: str = "gpt4o"):
        return "response_2"

    @log(name="wrapper-span")
    def nested_call(nested_query: str):
        llm_call(query=nested_query)
        llm_call_2(query=nested_query, model="gpt4o-mini")
        return "new response"

    with galileo_context():
        nested_call(nested_query="input")
        llm_call_2(query="input_2", model_attr="gpt4o-mini")

    payload = mock_instance.ingest_traces_sync.call_args[0][0]

    # nested_call() span
    assert type(payload.traces[0].spans[0]) == WorkflowSpan
    assert payload.traces[0].spans[0].input == {"nested_query": "input"}
    assert payload.traces[0].spans[0].output == "new response"
    assert payload.traces[0].spans[0].name == "wrapper-span"

    # llm_call() span inside nested_call()
    assert type(payload.traces[0].spans[0].spans[0]) == LlmSpan
    assert payload.traces[0].spans[0].spans[0].output == "response"
    assert payload.traces[0].spans[0].spans[0].input == {
        "query": "input",
        "model_attr": "gpt4o",
    }
    assert payload.traces[0].spans[0].spans[0].model == "gpt4o"
    assert payload.traces[0].spans[0].spans[0].name == "llm-span"

    # llm_call_2() span inside nested_call()
    assert type(payload.traces[0].spans[0].spans[1]) == LlmSpan
    assert payload.traces[0].spans[0].spans[1].output == "response_2"
    assert payload.traces[0].spans[0].spans[1].input == {
        "query": "input",
        "model": "gpt4o-mini",
        "model_attr": "gpt4o",
    }
    # `model_attr` default value should override the `model` arg
    assert payload.traces[0].spans[0].spans[1].model == "gpt4o"

    # llm_call_2() span
    assert type(payload.traces[0].spans[1]) == LlmSpan
    assert payload.traces[0].spans[1].output == "response_2"
    assert payload.traces[0].spans[1].input == {
        "query": "input_2",
        "model": "gpt4o",
        "model_attr": "gpt4o-mini",
    }
    # `model_attr` should override the `model` arg
    assert payload.traces[0].spans[1].model == "gpt4o-mini"
