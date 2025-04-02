import os
from unittest.mock import Mock, patch

import pytest
import vcr
from agents import (
    Agent,
    GuardrailFunctionOutput,
    InputGuardrail,
    InputGuardrailTripwireTriggered,
    Runner,
    set_trace_processors,
)
from pydantic import BaseModel
from pytest import MonkeyPatch, mark

from galileo.handlers.openai_agents import GalileoTracingProcessor
from galileo.logger import GalileoLogger
from tests.testutils.setup import setup_mock_core_api_client, setup_mock_logstreams_client, setup_mock_projects_client


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


@mark.asyncio
@mark.asyncio
@vcr.use_cassette(
    "tests/fixtures/openai_agents_complex.yaml",
    filter_headers=["authorization"],
    decode_compressed_response=True,
    record_mode=vcr.mode.NEW_EPISODES,
)
@patch("galileo.logger.LogStreams")
@patch("galileo.logger.Projects")
@patch("galileo.logger.GalileoCoreApiClient")
async def test_complex_agent(
    mock_core_api_client: Mock, mock_projects_client: Mock, mock_logstreams_client: Mock, monkeypatch: MonkeyPatch
) -> None:
    setup_mock_core_api_client(mock_core_api_client)
    setup_mock_projects_client(mock_projects_client)
    setup_mock_logstreams_client(mock_logstreams_client)
    # galileo_context.reset()
    galileo_logger = GalileoLogger(project="test", log_stream="test")
    gp = GalileoTracingProcessor(galileo_logger=galileo_logger, flush_on_trace_end=False)
    set_trace_processors([gp])
    monkeypatch.setenv("OPENAI_API_KEY", "sk-test")

    # set_trace_processors([GalileoTracingProcessor()])
    # with the following exception InputGuardrailTripwireTriggered
    # catch it with
    with pytest.raises(InputGuardrailTripwireTriggered):
        result = await Runner.run(triage_agent, "who was the first president of the united states?")
        print(result.final_output)
        result = await Runner.run(triage_agent, "what is life")
        print(result.final_output)

    traces = galileo_logger.traces
    assert len(traces) == 2


@mark.asyncio
@mark.asyncio
@vcr.use_cassette(
    "tests/fixtures/openai_agents.yaml",
    filter_headers=["authorization"],
    decode_compressed_response=True,
    record_mode=vcr.mode.NEW_EPISODES,
)
@patch("galileo.logger.LogStreams")
@patch("galileo.logger.Projects")
@patch("galileo.logger.GalileoCoreApiClient")
async def test_simple_agent(
    mock_core_api_client: Mock, mock_projects_client: Mock, mock_logstreams_client: Mock, monkeypatch: MonkeyPatch
) -> None:
    mock_core_api_instance = setup_mock_core_api_client(mock_core_api_client)
    setup_mock_projects_client(mock_projects_client)
    setup_mock_logstreams_client(mock_logstreams_client)
    # galileo_context.reset()
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
    payload = mock_core_api_instance.ingest_traces_sync.call_args[0][0]
    assert len(payload.traces) == 1
    assert len(payload.traces[0].spans) == 1
