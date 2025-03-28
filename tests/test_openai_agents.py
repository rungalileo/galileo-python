from agents import Agent, InputGuardrail,GuardrailFunctionOutput, InputGuardrailTripwireTriggered, Runner, set_trace_processors
from pydantic import BaseModel
from pytest import MonkeyPatch, mark
import pytest
import vcr
import asyncio
import os

from galileo.agents import GalileoTracingProcessor




class HomeworkOutput(BaseModel):
    is_homework: bool
    reasoning: str


guardrail_agent = Agent(
    name="Guardrail check",
    instructions="Check if the user is asking about homework.",
    output_type=HomeworkOutput,
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
    return GuardrailFunctionOutput(
        output_info=final_output,
        tripwire_triggered=not final_output.is_homework,
    )

triage_agent = Agent(
    name="Triage Agent",
    instructions="You determine which agent to use based on the user's homework question",
    handoffs=[history_tutor_agent, math_tutor_agent],
    input_guardrails=[
        InputGuardrail(guardrail_function=homework_guardrail),
    ],
)

import os
os.environ["OPENAI_API_KEY"] = "sk-test"


@mark.asyncio
@vcr.use_cassette('tests/fixtures/openai_session.yaml', decode_compressed_response=True, record_mode=vcr.mode.NEW_EPISODES)
async def test_openai_agent(monkeypatch:MonkeyPatch) -> None:
    """
    Test the OpenAI agent with a VCR cassette.
    """

    monkeypatch.setenv("OPENAI_API_KEY", "sk-test")
    
    set_trace_processors([GalileoTracingProcessor()])
    # with the following exception InputGuardrailTripwireTriggered
    # catch it with
    with pytest.raises(InputGuardrailTripwireTriggered) as excinfo:    
        result = await Runner.run(triage_agent, "who was the first president of the united states?")
        print(result.final_output)
        result = await Runner.run(triage_agent, "what is life")
        print(result.final_output)

