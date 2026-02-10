# galileo-adk

[![PyPI version](https://img.shields.io/pypi/v/galileo-adk.svg)](https://pypi.org/project/galileo-adk/)
[![Python versions](https://img.shields.io/pypi/pyversions/galileo-adk.svg)](https://pypi.org/project/galileo-adk/)
[![License](https://img.shields.io/pypi/l/galileo-adk.svg)](https://github.com/rungalileo/galileo-python/blob/main/LICENSE)

Galileo observability for [Google ADK](https://github.com/google/adk-python) agents. Automatic tracing of agent runs, LLM calls, and tool executions.

## Installation

```bash
pip install galileo-adk
```

**Requirements:** Python 3.10+, a [Galileo API key](https://www.rungalileo.io/), and a [Google AI API key](https://aistudio.google.com/apikey)

## Quick Start

```python
import asyncio
from galileo_adk import GalileoADKPlugin
from google.adk.runners import Runner
from google.adk.agents import LlmAgent
from google.genai import types

async def main():
    plugin = GalileoADKPlugin(project="my-project", log_stream="production")
    agent = LlmAgent(name="assistant", model="gemini-2.0-flash", instruction="You are helpful.")
    runner = Runner(agent=agent, plugins=[plugin])

    message = types.Content(parts=[types.Part(text="Hello! What can you help me with?")])
    async for event in runner.run_async(user_id="user-123", session_id="session-456", new_message=message):
        if event.is_final_response():
            print(event.content.parts[0].text)

if __name__ == "__main__":
    # Set environment variables: GALILEO_API_KEY, GOOGLE_API_KEY
    asyncio.run(main())
```

## Configuration

| Parameter | Environment Variable | Description |
|-----------|---------------------|-------------|
| `project` | `GALILEO_PROJECT` | Project name (required unless `ingestion_hook` provided) |
| `log_stream` | `GALILEO_LOG_STREAM` | Log stream name (required unless `ingestion_hook` provided) |
| `ingestion_hook` | - | Custom callback for trace data (bypasses Galileo backend) |

## Features

### Session Tracking

All traces with the same `session_id` are automatically grouped into a Galileo session, enabling conversation-level tracking:

```python
import asyncio
from galileo_adk import GalileoADKPlugin
from google.adk.runners import Runner
from google.adk.agents import LlmAgent
from google.genai import types

async def main():
    plugin = GalileoADKPlugin(project="my-project", log_stream="production")
    agent = LlmAgent(name="assistant", model="gemini-2.0-flash", instruction="You are helpful.")
    runner = Runner(agent=agent, plugins=[plugin])

    # All traces in this conversation are grouped together
    session_id = "conversation-abc"

    # First message
    message1 = types.Content(parts=[types.Part(text="Hello! What's the capital of France?")])
    async for event in runner.run_async(user_id="user-123", session_id=session_id, new_message=message1):
        if event.is_final_response():
            print(f"Response 1: {event.content.parts[0].text}")

    # Follow-up in same session
    message2 = types.Content(parts=[types.Part(text="What about Germany?")])
    async for event in runner.run_async(user_id="user-123", session_id=session_id, new_message=message2):
        if event.is_final_response():
            print(f"Response 2: {event.content.parts[0].text}")

if __name__ == "__main__":
    # Set environment variables: GALILEO_API_KEY, GOOGLE_API_KEY
    asyncio.run(main())
```

### Custom Metadata

Attach custom metadata to traces using ADK's `RunConfig`. Metadata is propagated to all spans (agent, LLM, tool) within the invocation:

```python
import asyncio
from galileo_adk import GalileoADKPlugin
from google.adk.runners import Runner
from google.adk.agents import LlmAgent
from google.adk.agents.run_config import RunConfig
from google.genai import types

async def main():
    plugin = GalileoADKPlugin(project="my-project", log_stream="production")
    agent = LlmAgent(name="assistant", model="gemini-2.0-flash", instruction="You are helpful.")
    runner = Runner(agent=agent, plugins=[plugin])

    run_config = RunConfig(
        custom_metadata={
            "user_tier": "premium",
            "conversation_id": "conv-abc",
            "turn": 1,
            "experiment_group": "A",
        }
    )

    message = types.Content(parts=[types.Part(text="Hello! Tell me a fun fact.")])
    async for event in runner.run_async(
        user_id="user-123",
        session_id="session-456",
        new_message=message,
        run_config=run_config,
    ):
        if event.is_final_response():
            print(event.content.parts[0].text)

if __name__ == "__main__":
    # Set environment variables: GALILEO_API_KEY, GOOGLE_API_KEY
    asyncio.run(main())
```

### Callback Mode

For granular control over which callbacks to use, attach them directly to your agent instead of using the plugin:

```python
import asyncio
from galileo_adk import GalileoADKCallback
from google.adk.runners import Runner
from google.adk.agents import LlmAgent
from google.genai import types

async def main():
    callback = GalileoADKCallback(project="my-project", log_stream="production")

    agent = LlmAgent(
        name="assistant",
        model="gemini-2.0-flash",
        instruction="You are helpful.",
        before_agent_callback=callback.before_agent_callback,
        after_agent_callback=callback.after_agent_callback,
        before_model_callback=callback.before_model_callback,
        after_model_callback=callback.after_model_callback,
        before_tool_callback=callback.before_tool_callback,
        after_tool_callback=callback.after_tool_callback,
    )
    runner = Runner(agent=agent)

    message = types.Content(parts=[types.Part(text="Hello! How are you?")])
    async for event in runner.run_async(user_id="user-123", session_id="session-456", new_message=message):
        if event.is_final_response():
            print(event.content.parts[0].text)

if __name__ == "__main__":
    # Set environment variables: GALILEO_API_KEY, GOOGLE_API_KEY
    asyncio.run(main())
```

### Ingestion Hook

Intercept traces for custom processing before forwarding to Galileo:

```python
import asyncio
import os
from galileo import GalileoLogger
from galileo_adk import GalileoADKPlugin
from google.adk.runners import Runner
from google.adk.agents import LlmAgent
from google.genai import types

logger = GalileoLogger(
    project=os.getenv("GALILEO_PROJECT", "my-project"),
    log_stream=os.getenv("GALILEO_LOG_STREAM", "dev"),
)

def my_ingestion_hook(request):
    """Hook that captures traces locally and forwards to Galileo with session management."""
    if hasattr(request, "traces") and request.traces:
        print(f"\n[Ingestion Hook] Intercepted {len(request.traces)} trace(s)")
        for trace in request.traces:
            spans = getattr(trace, "spans", []) or []
            span_types = [getattr(s, "type", "unknown") for s in spans]
            print(f"  - Trace with {len(spans)} span(s): {span_types}")

    # Session management: same external_id returns the same Galileo session
    galileo_session_id = logger.start_session(external_id=request.session_external_id)
    request.session_id = galileo_session_id

    # Forward traces to Galileo
    logger.ingest_traces(request)

async def main():
    plugin = GalileoADKPlugin(ingestion_hook=my_ingestion_hook)
    agent = LlmAgent(name="assistant", model="gemini-2.0-flash", instruction="You are helpful.")
    runner = Runner(agent=agent, plugins=[plugin])

    message = types.Content(parts=[types.Part(text="Hello!")])
    async for event in runner.run_async(user_id="user-123", session_id="session-456", new_message=message):
        if event.is_final_response():
            print(event.content.parts[0].text)

if __name__ == "__main__":
    # Set environment variables: GALILEO_API_KEY, GOOGLE_API_KEY
    asyncio.run(main())
```

## Resources

- [Galileo Documentation](https://docs.rungalileo.io/)
- [Google ADK Documentation](https://google.github.io/adk-docs/)

## License

Apache-2.0
