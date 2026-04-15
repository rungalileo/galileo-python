# galileo-a2a

[![PyPI version](https://img.shields.io/pypi/v/galileo-a2a.svg)](https://pypi.org/project/galileo-a2a/)
[![Python versions](https://img.shields.io/pypi/pyversions/galileo-a2a.svg)](https://pypi.org/project/galileo-a2a/)
[![License](https://img.shields.io/pypi/l/galileo-a2a.svg)](https://github.com/rungalileo/galileo-python/blob/main/LICENSE)

Galileo observability for [A2A (Agent-to-Agent)](https://github.com/google/A2A) protocol interactions. Automatic tracing of agent-to-agent calls, task lifecycle, and cross-agent distributed trace correlation.

## How It Works

```
┌──────────────────────────────────────────────────────────────────────┐
│                        Single Distributed Trace                      │
├──────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  ┌─────────────────────┐    A2A Protocol     ┌────────────────────┐  │
│  │  Orchestrator Agent │    (JSON-RPC)       │  Researcher Agent  │  │
│  │                     │                     │                    │  │
│  │  plan               │  send_message ──>   │  on_message_send   │  │
│  │  delegate ──────────┼──────────────────>  │    invoke LLM      │  │
│  │  synthesize         │  <── stream events  │    call tools      │  │
│  └──────────┬──────────┘                     └─────────┬──────────┘  │
│             │                                          │             │
│             │          OpenTelemetry Spans             │             │
│             └─────────────────┬────────────────────────┘             │
│                               │                                      │
│                    ┌──────────▼──────────┐                           │
│                    │      Galileo        │                           │
│                    │  (Trace Explorer)   │                           │
│                    └─────────────────────┘                           │
└──────────────────────────────────────────────────────────────────────┘
```

`galileo-a2a` instruments both the **client** (outbound calls) and **server** (inbound requests) sides of the A2A protocol. Trace context is propagated through A2A message metadata so all agents appear in a single distributed trace in Galileo.

## Installation

```bash
pip install galileo-a2a
```

**Requirements:** Python 3.10+, a [Galileo API key](https://www.rungalileo.io/), and [a2a-sdk](https://pypi.org/project/a2a-sdk/) 0.3+

## Quick Start

```python
from galileo.otel import GalileoSpanProcessor, add_galileo_span_processor
from galileo_a2a import A2AInstrumentor
from opentelemetry.sdk.trace import TracerProvider

provider = TracerProvider()
add_galileo_span_processor(provider, GalileoSpanProcessor())
A2AInstrumentor().instrument(tracer_provider=provider, agent_name="orchestrator")
```

Once instrumented, all `a2a-sdk` client and server interactions produce OTel spans automatically.

## Configuration

| Parameter | Description |
|-----------|-------------|
| `tracer_provider` | OTel `TracerProvider` instance. Falls back to the global provider if not specified. |
| `agent_name` | Name of this agent, set on spans as `gen_ai.agent.name`. |
| `capture_content` | Set to `False` to disable capturing message content (e.g. for PII compliance). |

Environment variables for the Galileo exporter:

| Environment Variable | Description |
|---------------------|-------------|
| `GALILEO_API_KEY` | Galileo API key (required) |
| `GALILEO_PROJECT` | Project name (alternative to `GalileoSpanProcessor(project=...)`) |
| `GALILEO_LOG_STREAM` | Log stream name (alternative to `GalileoSpanProcessor(logstream=...)`) |

## Features

### Client & Server Instrumentation

The instrumentor patches both sides of the A2A protocol:

**Client-side** (outbound calls): `send_message`, `get_task`, `cancel_task`, `get_card`

**Server-side** (inbound requests): `on_message_send`, `on_message_send_stream`

### Cross-Agent Distributed Tracing

When Agent A calls Agent B, trace context is propagated through A2A message metadata. The receiving agent joins the caller's trace, so both agents appear in a single distributed trace in Galileo.

### Session Tracking

A2A's `context_id` is mapped to `session.id`, grouping all interactions within the same conversation into a Galileo session.

### Disabling Instrumentation

```python
instrumentor = A2AInstrumentor()
instrumentor.instrument(tracer_provider=provider, agent_name="my-agent")

# Restore original a2a-sdk behavior
instrumentor.uninstrument()
```

## Multi-Agent Example

Add distributed tracing to your multi-agent A2A workflow with just 4 lines of code. The rest is your standard agent logic — no changes needed.

```python
import asyncio
import uuid

import httpx
import uvicorn
from a2a.client import ClientConfig, ClientFactory
from a2a.server.agent_execution import AgentExecutor, RequestContext
from a2a.server.apps.jsonrpc.starlette_app import A2AStarletteApplication
from a2a.server.events import EventQueue, InMemoryQueueManager
from a2a.server.request_handlers.default_request_handler import DefaultRequestHandler
from a2a.server.tasks import InMemoryTaskStore
from a2a.types import (
    AgentCapabilities, AgentCard, AgentSkill, Message, Role,
    TaskState, TaskStatus, TaskStatusUpdateEvent, TextPart,
)
from galileo.otel import GalileoSpanProcessor, add_galileo_span_processor
from galileo_a2a import A2AInstrumentor
from langchain.agents import create_agent
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from langgraph.graph import END, START, StateGraph
from opentelemetry.instrumentation.langchain import LangchainInstrumentor
from opentelemetry.sdk.trace import TracerProvider
from starlette.applications import Starlette
from typing_extensions import TypedDict

# ---- Only 4 lines needed for full distributed tracing ----
provider = TracerProvider()
add_galileo_span_processor(provider, GalileoSpanProcessor())
A2AInstrumentor().instrument(tracer_provider=provider, agent_name="orchestrator")
LangchainInstrumentor().instrument(tracer_provider=provider)


# ---- Everything below is your standard agent code ----

llm = ChatOpenAI(model="gpt-4o-mini")

# Researcher agent — standard LangChain agent served over A2A

@tool
def search_kb(query: str) -> str:
    """Search the travel knowledge base."""
    if "paris" in query.lower():
        return "Eiffel Tower 330m, Louvre 9.6M visitors/yr, 20 arrondissements."
    return f"No results for: {query}"

researcher = create_agent(
    llm, [search_kb],
    system_prompt="Use search_kb to find facts, then summarize for a traveler.",
)

CARD = AgentCard(
    name="researcher", description="Travel researcher", url="http://localhost:9867",
    version="1.0.0", capabilities=AgentCapabilities(streaming=True),
    default_input_modes=["text/plain"], default_output_modes=["text/plain"],
    skills=[AgentSkill(id="qa", name="Q&A", description="Answer questions", tags=[])],
)

class ResearcherExecutor(AgentExecutor):
    async def execute(self, ctx: RequestContext, queue: EventQueue) -> None:
        result = await researcher.ainvoke({"messages": [("user", ctx.get_user_input())]})
        await queue.enqueue_event(TaskStatusUpdateEvent(
            task_id=ctx.task_id, context_id=ctx.context_id, final=True,
            status=TaskStatus(state=TaskState.completed, message=Message(
                message_id=str(uuid.uuid4()), role=Role.agent,
                parts=[TextPart(text=result["messages"][-1].content or "")],
            )),
        ))

    async def cancel(self, ctx: RequestContext, queue: EventQueue) -> None:
        await queue.enqueue_event(TaskStatusUpdateEvent(
            task_id=ctx.task_id, context_id=ctx.context_id, final=True,
            status=TaskStatus(state=TaskState.canceled),
        ))

# Orchestrator — standard LangGraph StateGraph

class State(TypedDict):
    user_query: str
    skills: list[str]
    research_query: str
    response: str
    plan: str

def build_orchestrator(client):
    async def discover(state: State) -> dict:
        card = await client.get_card()
        return {"skills": [s.name for s in card.skills]}

    async def plan(state: State) -> dict:
        result = await create_agent(llm,
            system_prompt="Formulate a travel research question. Reply with ONLY the question.",
        ).ainvoke({"messages": [("user", state["user_query"])]})
        return {"research_query": result["messages"][-1].content}

    async def delegate(state: State) -> dict:
        msg = Message(message_id=str(uuid.uuid4()), role=Role.user,
            parts=[TextPart(text=state["research_query"])], context_id="session-1")
        async for event in client.send_message(msg):
            if isinstance(event, tuple):
                task = event[0]
                if task.status and task.status.state == TaskState.completed and task.status.message:
                    return {"response": getattr(task.status.message.parts[0].root, "text", "")}
        return {"response": ""}

    async def synthesize(state: State) -> dict:
        result = await create_agent(llm,
            system_prompt="Create a brief 3-day itinerary from the research.",
        ).ainvoke({"messages": [("user", f"Research:\n{state['response']}\n\nCreate itinerary.")]})
        return {"plan": result["messages"][-1].content}

    graph = StateGraph(State)
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

# Run both agents

async def main():
    app = Starlette()
    A2AStarletteApplication(
        agent_card=CARD,
        http_handler=DefaultRequestHandler(
            agent_executor=ResearcherExecutor(),
            task_store=InMemoryTaskStore(), queue_manager=InMemoryQueueManager(),
        ),
    ).add_routes_to_app(app)
    server = uvicorn.Server(uvicorn.Config(app, port=9867, log_level="warning"))
    server_task = asyncio.create_task(server.serve())
    await asyncio.sleep(1)

    client = ClientFactory(
        config=ClientConfig(streaming=True, httpx_client=httpx.AsyncClient(timeout=httpx.Timeout(120))),
    ).create(CARD)
    result = await build_orchestrator(client).ainvoke(
        {"user_query": "Plan a 3-day trip to Paris", "skills": [], "research_query": "", "response": "", "plan": ""},
    )
    print(result["plan"])

    server.should_exit = True
    await server_task
    provider.shutdown()

if __name__ == "__main__":
    # Set environment variables: GALILEO_API_KEY, OPENAI_API_KEY
    asyncio.run(main())
```

## Resources

- [Galileo Documentation](https://v2docs.galileo.ai)
- [A2A Protocol Specification](https://a2a-protocol.org)
- [a2a-sdk Documentation](https://pypi.org/project/a2a-sdk)

## License

Apache-2.0
