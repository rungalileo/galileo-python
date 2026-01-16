# galileo-adk

Galileo observability integration for Google ADK (Agent Development Kit).

## Installation

```bash
pip install galileo-adk
```

## Two Interfaces

| Interface | Use Case |
|-----------|----------|
| `GalileoADKPlugin` | Runner-level observability |
| `GalileoADKCallback` | Agent-level observability |

## Quick Start

### GalileoADKPlugin (Recommended)

```python
from galileo_adk import GalileoADKPlugin
from google.adk.runners import Runner
from google.adk.agents import LlmAgent

agent = LlmAgent(
    name="my_agent",
    model="gemini-2.0-flash",
    instruction="You are a helpful assistant."
)

plugin = GalileoADKPlugin(
    project="my-project",
    log_stream="production",
)

runner = Runner(agent=agent, plugins=[plugin])

async for event in runner.run_async(user_id="user", session_id="session", new_message=message):
    if event.is_final_response():
        print(event.content.parts[0].text)
```

### GalileoADKCallback

```python
from galileo_adk import GalileoADKCallback
from google.adk.agents import LlmAgent

callback = GalileoADKCallback(
    project="my-project",
    log_stream="production",
)

agent = LlmAgent(
    name="my_agent",
    model="gemini-2.0-flash",
    instruction="You are a helpful assistant.",
    before_agent_callback=callback.before_agent_callback,
    after_agent_callback=callback.after_agent_callback,
    before_model_callback=callback.before_model_callback,
    after_model_callback=callback.after_model_callback,
    before_tool_callback=callback.before_tool_callback,
    after_tool_callback=callback.after_tool_callback,
)
```

## Configuration

Both interfaces accept the same parameters:

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `project` | `str` | `None` | Galileo project (or `GALILEO_PROJECT` env var) |
| `log_stream` | `str` | `None` | Log stream (or `GALILEO_LOG_STREAM` env var) |
| `galileo_logger` | `GalileoLogger` | `None` | Existing logger instance |
| `start_new_trace` | `bool` | `True` | Start new trace per run |
| `flush_on_run_end` / `flush_on_agent_end` | `bool` | `True` | Auto-flush on completion |
| `ingestion_hook` | `Callable` | `None` | Intercept traces (replaces default ingestion) |

### Ingestion Hook

The `ingestion_hook` **replaces** default ingestion. To inspect AND send traces:

```python
callback = GalileoADKCallback()
logger = callback._handler._galileo_logger

def my_hook(request):
    print(f"Intercepted {len(request.traces)} traces")
    logger.ingest_traces(request)  # Required to send to Galileo!

logger._ingestion_hook = my_hook
```

## Multi-Plugin Support

Galileo plugin works with other ADK plugins. Order matters:

```python
# Galileo observes ORIGINAL data
plugins=[galileo_plugin, redaction_plugin]

# Galileo observes REDACTED data
plugins=[redaction_plugin, galileo_plugin]
```

## Development

### Setup

```bash
cd galileo-python/galileo-adk
uv sync
```

### Tests

```bash
uv run pytest -v
```

### Linting

```bash
uv run ruff check .
uv run ruff format .
```

## License

Apache-2.0
