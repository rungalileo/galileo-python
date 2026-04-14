"""Two-agent A2A demo with LangGraph orchestrator and Galileo distributed tracing.

Architecture:
    Orchestrator (LangGraph) ──A2A──> Researcher (LangChain agent + search tool)

Both agents appear in a single distributed trace in Galileo.

Usage:
    # Copy and fill in the .env file:
    cp examples/.env.example examples/.env

    # Install example dependencies:
    uv sync --group examples

    # Run:
    uv run python examples/two_agent_demo.py
"""

from __future__ import annotations

import asyncio
import uuid
from pathlib import Path

import httpx
import uvicorn
from a2a.client import ClientConfig, ClientFactory
from a2a.server.agent_execution import AgentExecutor, RequestContext
from a2a.server.apps.jsonrpc.starlette_app import A2AStarletteApplication
from a2a.server.events import EventQueue, InMemoryQueueManager
from a2a.server.request_handlers.default_request_handler import DefaultRequestHandler
from a2a.server.tasks import InMemoryTaskStore
from a2a.types import (
    AgentCapabilities,
    AgentCard,
    AgentSkill,
    Message,
    Role,
    TaskState,
    TaskStatus,
    TaskStatusUpdateEvent,
    TextPart,
)
from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from langgraph.graph import END, START, StateGraph
from opentelemetry.instrumentation.langchain import LangchainInstrumentor
from opentelemetry.sdk.trace import TracerProvider
from starlette.applications import Starlette
from typing_extensions import TypedDict

from galileo.otel import GalileoSpanProcessor, add_galileo_span_processor
from galileo_a2a import A2AInstrumentor

load_dotenv(Path(__file__).parent / ".env")

# ---------------------------------------------------------------------------
# Galileo tracing setup
# ---------------------------------------------------------------------------

provider = TracerProvider()
add_galileo_span_processor(provider, GalileoSpanProcessor())
A2AInstrumentor().instrument(tracer_provider=provider, agent_name="orchestrator")
LangchainInstrumentor().instrument(tracer_provider=provider)

llm = ChatOpenAI(model="gpt-4o-mini")

# ---------------------------------------------------------------------------
# Researcher agent (LangChain, served over A2A)
# ---------------------------------------------------------------------------


@tool
def search_kb(query: str) -> str:
    """Search the travel knowledge base."""
    if "paris" in query.lower():
        return "Eiffel Tower 330m, Louvre 9.6M visitors/yr, 20 arrondissements."
    return f"No results for: {query}"


researcher = create_agent(
    llm,
    [search_kb],
    system_prompt="Use search_kb to find facts, then summarize for a traveler.",
)

CARD = AgentCard(
    name="researcher",
    description="Travel researcher with tool use",
    url="http://localhost:9867",
    version="1.0.0",
    capabilities=AgentCapabilities(streaming=True),
    default_input_modes=["text/plain"],
    default_output_modes=["text/plain"],
    skills=[AgentSkill(id="qa", name="Q&A", description="Answer questions", tags=[])],
)


class ResearcherExecutor(AgentExecutor):
    async def execute(self, ctx: RequestContext, queue: EventQueue) -> None:
        result = await researcher.ainvoke({"messages": [("user", ctx.get_user_input())]})
        await queue.enqueue_event(
            TaskStatusUpdateEvent(
                task_id=ctx.task_id,
                context_id=ctx.context_id,
                final=True,
                status=TaskStatus(
                    state=TaskState.completed,
                    message=Message(
                        message_id=str(uuid.uuid4()),
                        role=Role.agent,
                        parts=[TextPart(text=result["messages"][-1].content or "")],
                    ),
                ),
            )
        )

    async def cancel(self, ctx: RequestContext, queue: EventQueue) -> None:
        await queue.enqueue_event(
            TaskStatusUpdateEvent(
                task_id=ctx.task_id,
                context_id=ctx.context_id,
                final=True,
                status=TaskStatus(state=TaskState.canceled),
            )
        )


# ---------------------------------------------------------------------------
# Orchestrator (LangGraph StateGraph)
# ---------------------------------------------------------------------------


class OrchestratorState(TypedDict):
    user_query: str
    research_query: str
    response: str
    plan: str


def build_orchestrator(client):
    async def plan(state: OrchestratorState) -> dict:
        result = await create_agent(
            llm,
            system_prompt="Formulate a travel research question. Reply with ONLY the question.",
        ).ainvoke({"messages": [("user", state["user_query"])]})
        return {"research_query": result["messages"][-1].content}

    async def delegate(state: OrchestratorState) -> dict:
        msg = Message(
            message_id=str(uuid.uuid4()),
            role=Role.user,
            parts=[TextPart(text=state["research_query"])],
            context_id="session-1",
        )
        async for event in client.send_message(msg):
            if isinstance(event, tuple):
                task = event[0]
                if task.status and task.status.state == TaskState.completed and task.status.message:
                    return {"response": getattr(task.status.message.parts[0].root, "text", "")}
        return {"response": ""}

    async def synthesize(state: OrchestratorState) -> dict:
        result = await create_agent(
            llm,
            system_prompt="Create a brief 3-day itinerary from the research.",
        ).ainvoke({"messages": [("user", f"Research:\n{state['response']}\n\nCreate itinerary.")]})
        return {"plan": result["messages"][-1].content}

    graph = StateGraph(OrchestratorState)
    graph.add_node("plan", plan)
    graph.add_node("delegate", delegate)
    graph.add_node("synthesize", synthesize)
    graph.add_edge(START, "plan")
    graph.add_edge("plan", "delegate")
    graph.add_edge("delegate", "synthesize")
    graph.add_edge("synthesize", END)
    return graph.compile()


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


async def main():
    # Start researcher A2A server
    app = Starlette()
    A2AStarletteApplication(
        agent_card=CARD,
        http_handler=DefaultRequestHandler(
            agent_executor=ResearcherExecutor(),
            task_store=InMemoryTaskStore(),
            queue_manager=InMemoryQueueManager(),
        ),
    ).add_routes_to_app(app)
    server = uvicorn.Server(uvicorn.Config(app, port=9867, log_level="warning"))
    server_task = asyncio.create_task(server.serve())
    await asyncio.sleep(1)

    # Run orchestrator
    client = ClientFactory(
        config=ClientConfig(streaming=True, httpx_client=httpx.AsyncClient(timeout=httpx.Timeout(120))),
    ).create(CARD)
    result = await build_orchestrator(client).ainvoke(
        {"user_query": "Plan a 3-day trip to Paris", "research_query": "", "response": "", "plan": ""},
    )
    print(result["plan"])

    server.should_exit = True
    await server_task
    provider.shutdown()


if __name__ == "__main__":
    asyncio.run(main())
