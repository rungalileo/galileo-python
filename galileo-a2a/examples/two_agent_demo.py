"""Two-agent A2A demo with LangGraph + Galileo distributed tracing.

Demonstrates a realistic multi-agent flow:
  - Orchestrator: A LangGraph StateGraph that plans, delegates, and synthesizes.
    Nodes: discover -> plan -> delegate -> synthesize (sequential edges).
  - Researcher: LangChain agent with a search tool, served over A2A protocol.
  - All spans (LangGraph workflow, LLM, tool, A2A) in a single distributed trace
    via opentelemetry-instrumentation-langchain + galileo-a2a.

Architecture:
    Orchestrator (LangGraph StateGraph) ──A2A──> Researcher (LangChain agent + search tool)

Modes:
    --streaming   (default) Uses SSE streaming — exercises send_message + on_message_send_stream
    --polling     Uses non-blocking send + get_task polling — exercises full task lifecycle

Usage:
    # Copy and fill in the .env file:
    cp examples/.env.example examples/.env

    # Install deps (in the galileo-a2a dir):
    uv add --dev "langchain>=1.2.13" "langchain-openai>=1.1.12" "langgraph>=1.1.3" \
        opentelemetry-instrumentation-langchain python-dotenv

    # Streaming mode (default):
    uv run python examples/two_agent_demo.py

    # Polling mode (exercises get_task):
    uv run python examples/two_agent_demo.py --polling
"""

from __future__ import annotations

import argparse
import asyncio
import logging
import os
import uuid
from pathlib import Path
from typing import Any

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
    TaskQueryParams,
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
from opentelemetry.sdk.trace import TracerProvider
from starlette.applications import Starlette
from typing_extensions import TypedDict

from galileo.otel import GalileoSpanProcessor, add_galileo_span_processor
from galileo_a2a import A2AInstrumentor

load_dotenv(Path(__file__).parent / ".env")

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(name)s] %(message)s")
logger = logging.getLogger("a2a-demo")

RESEARCHER_PORT = 9867
RESEARCHER_URL = f"http://localhost:{RESEARCHER_PORT}"
GALILEO_PROJECT = os.environ.get("GALILEO_PROJECT", "a2a-distributed-tracing-demo")
GALILEO_LOG_STREAM = os.environ.get("GALILEO_LOG_STREAM", "dev")

llm = ChatOpenAI(model="gpt-4o-mini")


# =============================================================================
# Tools
# =============================================================================

TRAVEL_KB = {
    "paris": (
        "Paris has 20 arrondissements. The Eiffel Tower is 330m tall and was built in 1889. "
        "The Louvre is the most visited museum in the world with 9.6M visitors/year. "
        "The Paris Metro has 16 lines and 308 stations. Best neighborhoods: Le Marais, "
        "Saint-Germain-des-Prés, Montmartre. Must-try food: croissants, croque-monsieur, "
        "escargot, crème brûlée. Tips: buy a Navigo pass for metro, most museums closed Tuesdays."
    ),
    "tokyo": (
        "Tokyo has 23 special wards. Tokyo Skytree is 634m tall. "
        "Shibuya Crossing sees 3,000 pedestrians per signal change. "
        "The Tokyo Metro carries 8.7M passengers daily."
    ),
}


@tool
def search_travel_kb(query: str) -> str:
    """Search the travel knowledge base for facts about a destination city."""
    query_lower = query.lower()
    for city, facts in TRAVEL_KB.items():
        if city in query_lower:
            return facts
    return f"No results found for: {query}"


# =============================================================================
# Researcher Agent (Server) — LangChain agent with search tool over A2A
# =============================================================================

researcher_agent = create_agent(
    ChatOpenAI(model="gpt-4o-mini"),
    [search_travel_kb],
    system_prompt="You are a travel researcher. Use the search_travel_kb tool to find facts about the destination, then summarize them clearly for a traveler.",
)


class ResearcherExecutor(AgentExecutor):
    """A2A executor that runs the LangChain researcher agent."""

    async def execute(self, context: RequestContext, event_queue: EventQueue) -> None:
        question = context.get_user_input()
        logger.info("Researcher received: %s", question)

        await event_queue.enqueue_event(
            TaskStatusUpdateEvent(
                task_id=context.task_id,
                context_id=context.context_id,
                status=TaskStatus(state=TaskState.working),
                final=False,
            )
        )

        result = await researcher_agent.ainvoke(
            {"messages": [("user", question)]},
        )

        answer = result["messages"][-1].content
        logger.info("Researcher answer: %s", (answer or "")[:120])

        await event_queue.enqueue_event(
            TaskStatusUpdateEvent(
                task_id=context.task_id,
                context_id=context.context_id,
                status=TaskStatus(
                    state=TaskState.completed,
                    message=Message(
                        message_id=str(uuid.uuid4()),
                        role=Role.agent,
                        parts=[TextPart(text=answer or "No answer generated.")],
                        task_id=context.task_id,
                        context_id=context.context_id,
                    ),
                ),
                final=True,
            )
        )

    async def cancel(self, context: RequestContext, event_queue: EventQueue) -> None:
        await event_queue.enqueue_event(
            TaskStatusUpdateEvent(
                task_id=context.task_id,
                context_id=context.context_id,
                status=TaskStatus(state=TaskState.canceled),
                final=True,
            )
        )


# =============================================================================
# Agent Card & Server Setup
# =============================================================================


def build_researcher_agent_card(*, streaming: bool) -> AgentCard:
    return AgentCard(
        name="researcher",
        description="Travel research agent powered by LangChain with knowledge base search.",
        url=RESEARCHER_URL,
        version="1.0.0",
        capabilities=AgentCapabilities(streaming=streaming),
        skills=[
            AgentSkill(
                id="travel-research",
                name="Travel Research",
                description="Research facts about travel destinations using a knowledge base",
                tags=["travel", "research"],
                examples=["Tell me about Paris", "What should I know about Tokyo?"],
            )
        ],
        default_input_modes=["text/plain"],
        default_output_modes=["text/plain"],
    )


def create_researcher_app(*, streaming: bool) -> Starlette:
    agent_card = build_researcher_agent_card(streaming=streaming)
    handler = DefaultRequestHandler(
        agent_executor=ResearcherExecutor(),
        task_store=InMemoryTaskStore(),
        queue_manager=InMemoryQueueManager(),
    )
    a2a_app = A2AStarletteApplication(agent_card=agent_card, http_handler=handler)
    app = Starlette()
    a2a_app.add_routes_to_app(app)
    return app


# =============================================================================
# Galileo Tracing — A2A + LangChain OTel instrumentation
# =============================================================================


def setup_galileo_tracing() -> tuple[A2AInstrumentor, TracerProvider]:
    provider = TracerProvider()
    processor = GalileoSpanProcessor(project=GALILEO_PROJECT, logstream=GALILEO_LOG_STREAM)
    add_galileo_span_processor(provider, processor)

    a2a_instrumentor = A2AInstrumentor()
    a2a_instrumentor.instrument(tracer_provider=provider, agent_name="orchestrator")

    # Lazy import: opentelemetry-instrumentation-langchain is a dev/example dependency,
    # not a requirement of galileo-a2a itself.
    from opentelemetry.instrumentation.langchain import LangchainInstrumentor

    LangchainInstrumentor().instrument(tracer_provider=provider)

    logger.info("Galileo tracing enabled (A2A + LangChain) for project=%s", GALILEO_PROJECT)
    return a2a_instrumentor, provider


# =============================================================================
# Orchestrator — LangGraph StateGraph
# =============================================================================


class OrchestratorState(TypedDict):
    user_query: str
    context_id: str
    streaming: bool
    skills: list[str]
    research_query: str
    researcher_response: str
    travel_plan: str


def _extract_text(parts: list) -> str:
    """Extract text from A2A Part wrappers."""
    for part in parts:
        inner = getattr(part, "root", part)
        if hasattr(inner, "text"):
            return inner.text
    return ""


async def _delegate_streaming(client: Any, message: Message) -> str:
    """Delegate via A2A streaming — exercises send_message + on_message_send_stream."""
    response = ""
    async for event in client.send_message(message):
        if isinstance(event, Message):
            response = _extract_text(event.parts)
        else:
            task, _update = event
            state = task.status.state if task.status else "unknown"
            logger.info("Task %s — state: %s", task.id, state)
            if task.status and task.status.state == TaskState.completed and task.status.message:
                response = _extract_text(task.status.message.parts)
    return response


_POLL_TIMEOUT_SECONDS = 120
_POLL_INTERVAL_SECONDS = 1


async def _delegate_polling(client: Any, message: Message) -> str:
    """Delegate via A2A polling — exercises send_message + get_task lifecycle."""
    task_id = None
    response = ""
    async for event in client.send_message(message):
        if isinstance(event, Message):
            response = _extract_text(event.parts)
        elif isinstance(event, tuple):
            task, _update = event
            task_id = task.id
            state = task.status.state if task.status else "unknown"
            logger.info("Task %s — state: %s", task_id, state)

    # Poll get_task until the researcher completes (with timeout)
    if task_id and not response:
        elapsed_seconds = 0.0
        while elapsed_seconds < _POLL_TIMEOUT_SECONDS:
            await asyncio.sleep(_POLL_INTERVAL_SECONDS)
            elapsed_seconds += _POLL_INTERVAL_SECONDS
            task = await client.get_task(TaskQueryParams(id=task_id))
            state = task.status.state if task.status else TaskState.unknown
            logger.info("Polling task %s — state: %s", task_id, state)

            if state == TaskState.completed:
                if task.status and task.status.message:
                    response = _extract_text(task.status.message.parts)
                break
            if state in (TaskState.failed, TaskState.canceled, TaskState.rejected):
                logger.error("Task %s ended with state: %s", task_id, state)
                break
        else:
            logger.error("Task %s polling timed out after %ss", task_id, _POLL_TIMEOUT_SECONDS)

    return response


def build_orchestrator_graph(client: Any) -> Any:
    """Build a LangGraph StateGraph for the orchestrator workflow.

    The graph has four sequential nodes:
        START -> discover -> plan -> delegate -> synthesize -> END

    ``client`` is captured by closure so the graph nodes can make A2A calls.
    """

    async def discover(state: OrchestratorState) -> dict:
        logger.info("Orchestrator discovering researcher agent...")
        card = await client.get_card()
        skills = [s.name for s in card.skills]
        logger.info("Discovered: %s — skills: %s", card.name, skills)
        return {"skills": skills}

    async def plan(state: OrchestratorState) -> dict:
        planner = create_agent(
            llm,
            system_prompt=(
                "You are a travel planning orchestrator. A user wants trip advice. "
                f"You have a researcher agent with skills: {state['skills']}. "
                "Formulate a clear, specific research question. Reply with ONLY the question."
            ),
        )
        result = await planner.ainvoke({"messages": [("user", state["user_query"])]})
        research_query = result["messages"][-1].content
        logger.info("Planned query: %s", research_query)
        return {"research_query": research_query}

    async def delegate(state: OrchestratorState) -> dict:
        message = Message(
            message_id=str(uuid.uuid4()),
            role=Role.user,
            parts=[TextPart(text=state["research_query"] or "Tell me about Paris")],
            context_id=state["context_id"],
        )

        mode = "streaming" if state["streaming"] else "polling"
        logger.info("Sending A2A request to researcher (%s mode)...", mode)
        if state["streaming"]:
            researcher_response = await _delegate_streaming(client, message)
        else:
            researcher_response = await _delegate_polling(client, message)
        return {"researcher_response": researcher_response}

    async def synthesize(state: OrchestratorState) -> dict:
        synthesizer = create_agent(
            llm,
            system_prompt="You are a travel planning assistant. Create a brief, actionable 3-day itinerary from the research.",
        )
        result = await synthesizer.ainvoke(
            {"messages": [("user", f"Research:\n{state['researcher_response']}\n\nCreate a 3-day Paris itinerary.")]},
        )
        travel_plan = result["messages"][-1].content
        logger.info("Final travel plan:\n%s", travel_plan)
        return {"travel_plan": travel_plan}

    graph = StateGraph(OrchestratorState)
    graph.add_node("discover", discover)
    graph.add_node("plan", plan)
    graph.add_node("delegate", delegate)
    graph.add_node("synthesize", synthesize)
    graph.add_edge(START, "discover")
    graph.add_edge("discover", "plan")
    graph.add_edge("plan", "delegate")
    graph.add_edge("delegate", "synthesize")
    graph.add_edge("synthesize", END)
    return graph.compile()


async def run_orchestrator(context_id: str, *, streaming: bool) -> None:
    agent_card = build_researcher_agent_card(streaming=streaming)
    http_client = httpx.AsyncClient(timeout=httpx.Timeout(120.0))
    factory = ClientFactory(
        config=ClientConfig(
            streaming=streaming,
            polling=not streaming,
            httpx_client=http_client,
        ),
    )
    client = factory.create(agent_card)

    graph = build_orchestrator_graph(client)
    result = await graph.ainvoke(
        {
            "user_query": "I'm planning a week-long trip to Paris. What should I know?",
            "context_id": context_id,
            "streaming": streaming,
            "skills": [],
            "research_query": "",
            "researcher_response": "",
            "travel_plan": "",
        },
    )

    logger.info("Orchestrator finished. Travel plan length: %d chars", len(result.get("travel_plan", "")))


# =============================================================================
# Main
# =============================================================================


async def main(streaming: bool) -> None:
    instrumentor, tracer_provider = setup_galileo_tracing()

    app = create_researcher_app(streaming=streaming)
    config = uvicorn.Config(app, host="0.0.0.0", port=RESEARCHER_PORT, log_level="warning")
    server = uvicorn.Server(config)
    server_task = asyncio.create_task(server.serve())

    async with httpx.AsyncClient() as http_client:
        for _ in range(30):
            try:
                resp = await http_client.get(f"{RESEARCHER_URL}/.well-known/agent-card.json")
                if resp.status_code == 200:
                    logger.info("Researcher server ready at %s", RESEARCHER_URL)
                    break
            except httpx.ConnectError:
                await asyncio.sleep(0.2)
        else:
            logger.error("Researcher server did not start in time")
            server.should_exit = True
            await server_task
            return

    mode = "streaming" if streaming else "polling"
    logger.info("Running demo in %s mode", mode)

    context_id = f"demo-session-{uuid.uuid4().hex[:8]}"
    try:
        await run_orchestrator(context_id, streaming=streaming)
    finally:
        server.should_exit = True
        await server_task
        instrumentor.uninstrument()
        tracer_provider.shutdown()

    logger.info("Done! Check Galileo project '%s' logstream '%s'.", GALILEO_PROJECT, GALILEO_LOG_STREAM)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="A2A two-agent demo with Galileo tracing")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--streaming", action="store_true", default=True, help="Use SSE streaming (default)")
    group.add_argument("--polling", action="store_true", help="Use non-blocking send + get_task polling")
    args = parser.parse_args()

    use_streaming = not args.polling
    asyncio.run(main(streaming=use_streaming))
