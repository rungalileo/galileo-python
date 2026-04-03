# galileo-a2a

[![PyPI version](https://img.shields.io/pypi/v/galileo-a2a.svg)](https://pypi.org/project/galileo-a2a/)
[![Python versions](https://img.shields.io/pypi/pyversions/galileo-a2a.svg)](https://pypi.org/project/galileo-a2a/)
[![License](https://img.shields.io/pypi/l/galileo-a2a.svg)](https://github.com/rungalileo/galileo-python/blob/main/LICENSE)

Galileo observability for [A2A (Agent-to-Agent)](https://github.com/google/A2A) protocol interactions. Automatic tracing of agent-to-agent calls, task lifecycle, and cross-agent correlation via span links.

## Installation

```bash
pip install galileo-a2a
```

**Requirements:** Python 3.10+, a [Galileo API key](https://www.rungalileo.io/), and [a2a-sdk](https://pypi.org/project/a2a-sdk/) 0.3+

## Quick Start

```python
import asyncio

from galileo.otel import GalileoSpanProcessor, add_galileo_span_processor
from galileo_a2a import A2AInstrumentor
from opentelemetry.sdk.trace import TracerProvider

# Set up Galileo tracing
provider = TracerProvider()
processor = GalileoSpanProcessor(project="my-project", logstream="my-agents")
add_galileo_span_processor(provider, processor)

# Instrument A2A — all client and server calls are traced automatically
A2AInstrumentor().instrument(tracer_provider=provider, agent_name="orchestrator")
```

Once instrumented, all `a2a-sdk` client and server interactions produce OTel spans with A2A-specific attributes — no code changes needed in your agent logic.

## Configuration

| Parameter | Description |
|-----------|-------------|
| `tracer_provider` | OTel `TracerProvider` instance. Falls back to the global provider if not specified. |
| `agent_name` | Name of this agent, set on spans as `gen_ai.agent.name`. |

Environment variables for the Galileo exporter:

| Environment Variable | Description |
|---------------------|-------------|
| `GALILEO_API_KEY` | Galileo API key (required) |
| `GALILEO_PROJECT` | Project name (alternative to `GalileoSpanProcessor(project=...)`) |
| `GALILEO_LOG_STREAM` | Log stream name (alternative to `GalileoSpanProcessor(logstream=...)`) |

## Features

### Automatic Client & Server Instrumentation

The instrumentor monkey-patches both sides of the A2A protocol:

**Client-side** (outbound calls):
- `BaseClient.send_message` — traced with streaming event tracking
- `BaseClient.get_task` — traced for task polling
- `BaseClient.cancel_task` — traced for task cancellation
- `BaseClient.get_card` — traced for agent card discovery

**Server-side** (inbound requests):
- `DefaultRequestHandler.on_message_send` — traced with trace context extraction
- `DefaultRequestHandler.on_message_send_stream` — same for streaming responses

```python
from a2a.client import A2AClient

# Client calls are automatically traced — no wrapper needed
client = A2AClient(agent_url="https://research-agent.example.com")
async for event in client.send_message(message):
    print(event)
```

### Cross-Agent Trace Correlation

When Agent A calls Agent B, `galileo-a2a` propagates trace context through A2A message metadata. The receiving agent creates a **span link** back to the caller, connecting both traces in Galileo:

```
Agent A (orchestrator)              Agent B (researcher)
┌─────────────────────┐             ┌─────────────────────┐
│ a2a.client.         │  metadata   │ a2a.server.         │
│   send_message      │────────────>│   on_message_send   │
│                     │  trace ctx  │        ↑             │
└─────────────────────┘             │   span link back    │
                                    │   to Agent A        │
                                    └─────────────────────┘
```

This works automatically — no manual context passing required.

### Session Tracking

A2A's `context_id` is mapped to `session.id`, grouping all interactions within the same conversation into a Galileo session:

```python
from a2a.types import MessageSendParams

# All traces with the same context_id are grouped into one session
params = MessageSendParams(
    message=Message(
        role="user",
        parts=[TextPart(text="Find hotels in Paris")],
        context_id="conversation-abc",  # becomes session.id
    )
)
```

### Task Lifecycle & Error Tracking

A2A task states are tracked on spans automatically. Error states (`failed`, `rejected`, `canceled`) set the span status to ERROR for visibility in Galileo:

```python
# Task state transitions are captured as span attributes:
#   a2a.task.state = "completed" | "failed" | "rejected" | "canceled" | ...
#
# Error states automatically mark the span as ERROR
```

### Multi-Agent Example

```python
import asyncio

from a2a.client import A2AClient
from a2a.types import Message, MessageSendParams, TextPart
from galileo.otel import GalileoSpanProcessor, add_galileo_span_processor
from galileo_a2a import A2AInstrumentor
from opentelemetry.sdk.trace import TracerProvider


def setup_galileo(agent_name: str, logstream: str) -> None:
    """Set up Galileo tracing for an agent."""
    provider = TracerProvider()
    processor = GalileoSpanProcessor(project="multi-agent-app", logstream=logstream)
    add_galileo_span_processor(provider, processor)
    A2AInstrumentor().instrument(tracer_provider=provider, agent_name=agent_name)


# Each agent gets its own logstream in Galileo
setup_galileo("orchestrator", logstream="orchestrator-agent")

# The orchestrator calls other agents — traces are linked automatically
client = A2AClient(agent_url="https://research-agent.example.com")


async def orchestrate(query: str, context_id: str):
    async for event in client.send_message(
        MessageSendParams(
            message=Message(
                role="user",
                parts=[TextPart(text=query)],
                context_id=context_id,
            )
        )
    ):
        print(event)


asyncio.run(orchestrate("Plan a trip to Paris", context_id="session-123"))
```

### Disabling Instrumentation

```python
instrumentor = A2AInstrumentor()
instrumentor.instrument(tracer_provider=provider, agent_name="my-agent")

# Later, restore original a2a-sdk behavior
instrumentor.uninstrument()
```

## Span Attributes

Spans created by this instrumentor include:

| Attribute | Description | Example |
|-----------|-------------|---------|
| `gen_ai.system` | Always `"a2a"` | `a2a` |
| `gen_ai.operation.name` | Operation type | `invoke_agent`, `create_agent` |
| `gen_ai.agent.name` | Agent name | `orchestrator` |
| `a2a.rpc.method` | A2A RPC method | `SendMessage`, `GetTask`, `CancelTask` |
| `a2a.task.id` | Task identifier | `task-abc-123` |
| `a2a.task.state` | Task lifecycle state | `completed`, `failed` |
| `a2a.context_id` | Conversation context | `ctx-conversation-789` |
| `session.id` | Session ID (= context_id) | `ctx-conversation-789` |

## Compatibility

`galileo-a2a` also works alongside the [AGNTCY Observe SDK](https://github.com/agntcy/observe-sdk). When extracting trace context on the server side, it checks both the Galileo metadata key and the AGNTCY `observe` key for interoperability.

## Resources

- [Galileo Documentation](https://docs.rungalileo.io/)
- [A2A Protocol Specification](https://github.com/google/A2A)
- [a2a-sdk Documentation](https://pypi.org/project/a2a-sdk/)

## License

Apache-2.0
