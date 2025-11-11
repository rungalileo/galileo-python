import os
from unittest.mock import Mock, patch

import httpx
import pytest
import respx
import vcr
from agents import (
    Agent,
    CodeInterpreterTool,
    GuardrailFunctionOutput,
    InputGuardrail,
    InputGuardrailTripwireTriggered,
    Runner,
    set_trace_processors,
)
from pydantic import BaseModel
from pytest import MonkeyPatch, mark

from galileo.handlers.openai_agents import GalileoTracingProcessor
from galileo.logger.logger import GalileoLogger
from galileo_core.schemas.logging.span import LlmSpan, ToolSpan
from tests.testutils.setup import setup_mock_logstreams_client, setup_mock_projects_client, setup_mock_traces_client


class HomeworkOutput(BaseModel):
    is_homework: bool
    reasoning: str


guardrail_agent = Agent(
    name="Guardrail check", instructions="Check if the user is asking about homework.", output_type=HomeworkOutput
)

math_tutor_agent = Agent(
    name="Math Tutor",
    handoff_description="Specialist agent for math questions",
    instructions="You provide help with math problems. Explain your reasoning at each step and include examples",
)

history_tutor_agent = Agent(
    name="History Tutor",
    handoff_description="Specialist agent for historical questions",
    instructions="You provide assistance with historical queries. Explain important events and context clearly.",
)


async def homework_guardrail(ctx, agent, input_data):
    result = await Runner.run(guardrail_agent, input_data, context=ctx.context)
    final_output = result.final_output_as(HomeworkOutput)
    return GuardrailFunctionOutput(output_info=final_output, tripwire_triggered=not final_output.is_homework)


triage_agent = Agent(
    name="Triage Agent",
    instructions="You determine which agent to use based on the user's homework question",
    handoffs=[history_tutor_agent, math_tutor_agent],
    input_guardrails=[InputGuardrail(guardrail_function=homework_guardrail)],
)

os.environ["OPENAI_API_KEY"] = "sk-test"


@pytest.mark.skip("flaky test")
@mark.asyncio
@vcr.use_cassette(
    "tests/fixtures/openai_agents_complex.yaml",
    filter_headers=["authorization"],
    decode_compressed_response=True,
    record_mode=vcr.mode.NEW_EPISODES,
)
@patch("galileo.logger.logger.LogStreams")
@patch("galileo.logger.logger.Projects")
@patch("galileo.logger.logger.Traces")
async def test_complex_agent(
    mock_traces_client: Mock, mock_projects_client: Mock, mock_logstreams_client: Mock, monkeypatch: MonkeyPatch
) -> None:
    setup_mock_traces_client(mock_traces_client)
    setup_mock_projects_client(mock_projects_client)
    setup_mock_logstreams_client(mock_logstreams_client)
    galileo_logger = GalileoLogger(project="test", log_stream="test")
    gp = GalileoTracingProcessor(galileo_logger=galileo_logger, flush_on_trace_end=False)
    set_trace_processors([gp])
    monkeypatch.setenv("OPENAI_API_KEY", "sk-test")

    with pytest.raises(InputGuardrailTripwireTriggered):
        await Runner.run(triage_agent, "who was the first president of the united states?")
        await Runner.run(triage_agent, "what is life")

    traces = galileo_logger.traces
    assert len(traces) == 2
    spans = traces[0].spans
    assert len(spans) == 2


@mark.asyncio
@vcr.use_cassette(
    "tests/fixtures/openai_agents.yaml",
    filter_headers=["authorization"],
    decode_compressed_response=True,
    record_mode=vcr.mode.NEW_EPISODES,
)
@patch("galileo.logger.logger.LogStreams")
@patch("galileo.logger.logger.Projects")
@patch("galileo.logger.logger.Traces")
async def test_simple_agent(
    mock_traces_client: Mock, mock_projects_client: Mock, mock_logstreams_client: Mock, monkeypatch: MonkeyPatch
) -> None:
    mock_traces_client_instance = setup_mock_traces_client(mock_traces_client)
    setup_mock_projects_client(mock_projects_client)
    setup_mock_logstreams_client(mock_logstreams_client)
    galileo_logger = GalileoLogger(project="test", log_stream="test")
    gp = GalileoTracingProcessor(galileo_logger=galileo_logger, flush_on_trace_end=False)
    set_trace_processors([gp])
    monkeypatch.setenv("OPENAI_API_KEY", "sk-test")
    agent = Agent(name="Assistant", instructions="You are the worlds best assistant.")
    result = await Runner.run(agent, "Write a haiku about recursion in programming.")
    assert result
    traces = galileo_logger.traces
    assert len(traces) == 1
    trace = traces[0]
    for span in trace.spans:
        assert span.status_code != 500
        assert span.metrics.duration_ns
        assert span.metrics.duration_ns > 0

    galileo_logger.flush()
    payload = mock_traces_client_instance.ingest_traces.call_args[0][0]
    assert len(payload.traces) == 1
    assert len(payload.traces[0].spans) == 1


def _create_mock_response_with_tools(tool_calls: list[dict]) -> dict:
    """Create a mock OpenAI API response with embedded tool calls."""
    return {
        "id": "resp_test123",
        "object": "response",
        "created_at": 1743431972,
        "status": "completed",
        "error": None,
        "incomplete_details": None,
        "instructions": None,
        "max_output_tokens": None,
        "tools": [],
        "tool_choice": "auto",
        "text": {"format": {"type": "text"}},
        "parallel_tool_calls": True,
        "previous_response_id": None,
        "reasoning": {"effort": None, "summary": None},
        "service_tier": "default",
        "metadata": {},
        "model": "gpt-4.1",
        "temperature": 0.7,
        "top_p": 1.0,
        "truncation": "disabled",
        "usage": {
            "input_tokens": 20,
            "input_tokens_details": {"cached_tokens": 0},
            "output_tokens": 50,
            "output_tokens_details": {"reasoning_tokens": 0},
            "total_tokens": 70,
        },
        "output": [
            *tool_calls,
            {
                "id": "msg_test123",
                "type": "message",
                "role": "assistant",
                "status": "completed",
                "content": [{"type": "output_text", "text": "Task completed.", "annotations": [], "logprobs": []}],
            },
        ],
    }


def _find_llm_spans(spans):
    llm_spans = []
    for span in spans:
        if isinstance(span, LlmSpan):
            llm_spans.append(span)
        if hasattr(span, "spans") and span.spans:
            llm_spans.extend(_find_llm_spans(span.spans))
    return llm_spans


def _find_tool_spans(spans):
    tool_spans = []
    for span in spans:
        if isinstance(span, ToolSpan):
            tool_spans.append(span)
        if hasattr(span, "spans") and span.spans:
            tool_spans.extend(_find_tool_spans(span.spans))
    return tool_spans


@mark.asyncio
@patch("galileo.logger.logger.LogStreams")
@patch("galileo.logger.logger.Projects")
@patch("galileo.logger.logger.Traces")
async def test_pre_built_tools_multiple_types(
    mock_traces_client: Mock, mock_projects_client: Mock, mock_logstreams_client: Mock, monkeypatch: MonkeyPatch
) -> None:
    """
    Test pre-built tools extraction: Multiple tool types (code_interpreter, file_search, web_search).
    """
    mock_traces_client_instance = setup_mock_traces_client(mock_traces_client)
    setup_mock_projects_client(mock_projects_client)
    setup_mock_logstreams_client(mock_logstreams_client)

    galileo_logger = GalileoLogger(project="test", log_stream="test")
    gp = GalileoTracingProcessor(galileo_logger=galileo_logger, flush_on_trace_end=False)
    set_trace_processors([gp])
    monkeypatch.setenv("OPENAI_API_KEY", "sk-test")

    tool_calls = [
        {
            "id": "ci_test123",
            "type": "code_interpreter_call",
            "code": "sum(range(1, 101))",
            "container_id": "cntr_test123",
            "status": "completed",
            "outputs": [{"type": "logs", "logs": "5050"}],
        },
        {
            "id": "fs_test123",
            "type": "file_search_call",
            "queries": ["test query"],
            "status": "completed",
            "results": [{"file_id": "file_123", "score": 0.95}],
        },
        {
            "id": "ws_test123",
            "type": "web_search_call",
            "action": {"type": "search", "query": "Python programming"},
            "status": "completed",
        },
    ]

    mock_response_data = _create_mock_response_with_tools(tool_calls)

    with respx.mock(base_url="https://api.openai.com") as respx_mock:
        respx_mock.post("/v1/responses").mock(return_value=httpx.Response(200, json=mock_response_data))
        agent = Agent(
            name="Assistant",
            instructions="You are a helpful assistant.",
            tools=[CodeInterpreterTool(tool_config={"type": "code_interpreter", "container": {"type": "auto"}})],
        )

        result = await Runner.run(agent, "Test multiple tools.")
        assert result

    traces = galileo_logger.traces
    assert len(traces) == 1

    llm_spans = _find_llm_spans(traces[0].spans)
    assert len(llm_spans) > 0

    spans_with_tools = [span for span in llm_spans if span.tools and len(span.tools) > 0]
    assert len(spans_with_tools) > 0, "Expected at least one LLM span with embedded tools extracted"

    all_tools = []
    for span in spans_with_tools:
        all_tools.extend(span.tools)

    assert len(all_tools) == 3, (
        f"Expected 3 tools, got {len(all_tools)}: {[t.get('tool_call_type') for t in all_tools]}"
    )

    tool_types = {tool.get("tool_call_type") for tool in all_tools}
    assert "code_interpreter_call" in tool_types, f"Missing code_interpreter_call. Found: {tool_types}"
    assert "file_search_call" in tool_types, f"Missing file_search_call. Found: {tool_types}"
    assert "web_search_call" in tool_types, f"Missing web_search_call. Found: {tool_types}"

    tools_by_type = {tool.get("tool_call_type"): tool for tool in all_tools}

    ci_tool = tools_by_type["code_interpreter_call"]
    assert ci_tool["function"]["name"] == "code_interpreter"
    assert ci_tool["tool_call_id"] == "ci_test123"

    fs_tool = tools_by_type["file_search_call"]
    assert fs_tool["function"]["name"] == "file_search"
    assert fs_tool["tool_call_id"] == "fs_test123"

    ws_tool = tools_by_type["web_search_call"]
    assert ws_tool["function"]["name"] == "web_search"
    assert ws_tool["tool_call_id"] == "ws_test123"

    for tool in all_tools:
        assert all(
            key in tool
            for key in ("type", "function", "tool_call_id", "tool_call_input", "tool_call_output", "tool_call_status")
        )

    assert len(spans_with_tools) > 0, "Expected at least one LLM span with tools"

    galileo_logger.flush()
    payload = mock_traces_client_instance.ingest_traces.call_args[0][0]
    assert len(payload.traces) == 1
