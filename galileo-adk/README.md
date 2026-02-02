# galileo-adk

Galileo observability integration for Google ADK (Agent Development Kit).

## Installation

```bash
pip install galileo-adk
```

## Architecture

```
┌──────────────────────────────────────────────────────────────────────────┐
│                           Google ADK                                     │
│                                                                          │
│  ┌─────────────────────────┐          ┌─────────────────────────┐        │
│  │    GalileoADKPlugin     │          │   GalileoADKCallback    │        │
│  │    (Runner plugins)     │          │   (Agent callbacks)     │        │
│  │                         │          │                         │        │
│  │  on_user_msg            │          │  before/after_agent     │        │
│  │  before/after_agent     │          │  before/after_model     │        │
│  │  before/after_model     │          │  before/after_tool      │        │
│  │  before/after_tool      │          │                         │        │
│  │  on_error               │          │                         │        │
│  └───────────┬─────────────┘          └───────────┬─────────────┘        │
│              │                                    │                      │
│              └──────────────┬─────────────────────┘                      │
│                             ▼                                            │
│                  ┌────────────────────┐                                  │
│                  │   SpanTracker      │  ← Run ID correlation            │
│                  └─────────┬──────────┘                                  │
│                            ▼                                             │
│                  ┌────────────────────┐                                  │
│                  │  GalileoObserver   │  ← Shared logic                  │
│                  └─────────┬──────────┘                                  │
│                            ▼                                             │
│                  ┌────────────────────┐                                  │
│                  │    SpanManager     │  ← Trace hierarchy               │
│                  └─────────┬──────────┘                                  │
│                            ▼                                             │
│                  ┌────────────────────┐                                  │
│                  │ GalileoBaseHandler │  ← From galileo lib              │
│                  └─────────┬──────────┘                                  │
└────────────────────────────┼─────────────────────────────────────────────┘
                             ▼
                ┌────────────────────────┐
                │    Galileo Backend     │
                │   (or ingestion_hook)  │
                └────────────────────────┘

Trace Hierarchy (Plugin mode):
──────────────────────────────
invocation [agent_name]           ← Run span (workflow wrapper)
└── agent_run [agent_name]        ← Agent span
    ├── call_llm                  ← LLM span (with tool_calls)
    └── execute_tool [tool_name]  ← Tool span
        └── (nested invocation)   ← Sub-agent if tool invokes agent
```

## Quick Start

### Plugin (Recommended)

```python
from galileo_adk import GalileoADKPlugin
from google.adk.runners import Runner
from google.adk.agents import LlmAgent

plugin = GalileoADKPlugin(project="my-project", log_stream="production")
agent = LlmAgent(name="assistant", model="gemini-2.0-flash", instruction="...")
runner = Runner(agent=agent, plugins=[plugin])

async for event in runner.run_async(user_id="user", session_id="sess", new_message=msg):
    if event.is_final_response():
        print(event.content.parts[0].text)
```

### Callback

```python
from galileo_adk import GalileoADKCallback

callback = GalileoADKCallback(project="my-project", log_stream="production")

agent = LlmAgent(
    name="assistant",
    model="gemini-2.0-flash",
    before_agent_callback=callback.before_agent_callback,
    after_agent_callback=callback.after_agent_callback,
    before_model_callback=callback.before_model_callback,
    after_model_callback=callback.after_model_callback,
    before_tool_callback=callback.before_tool_callback,
    after_tool_callback=callback.after_tool_callback,
)
```

## Configuration

| Parameter | Type | Description |
|-----------|------|-------------|
| `project` | `str` | Galileo project (or `GALILEO_PROJECT` env) |
| `log_stream` | `str` | Log stream (or `GALILEO_LOG_STREAM` env) |
| `ingestion_hook` | `Callable` | Custom trace handler (enables hook-only mode) |
| `external_id` | `str` | Groups traces under same session |
| `metadata` | `dict` |  Metadata for all spans |

## Metadata

### Static (same for all turns)

```python
plugin = GalileoADKPlugin(
    project="my-project",
    metadata={"env": "prod", "version": "1.0"}
)
```

### Per-Turn (updated before each turn)

```python
plugin = GalileoADKPlugin(project="my-project")
plugin.metadata = {"turn": 1, "user_id": "abc"}
await runner.run_async(...)

plugin.metadata = {"turn": 2, "user_id": "abc"}
await runner.run_async(...)
```

## Advanced

### Ingestion Hook Mode

No credentials required at the time of plugin instantiation when using `ingestion_hook`:

```python
def my_handler(request):
    for trace in request.traces:
        pre_process(trace)
        flush_trace_to_galileo(trace)

plugin = GalileoADKPlugin(ingestion_hook=my_handler)
```

### Multi-Plugin Ordering

```python
# Galileo sees original data
plugins = [galileo_plugin, redaction_plugin]

# Galileo sees redacted data
plugins = [redaction_plugin, galileo_plugin]
```

## Development

### Project Structure

```
galileo-python/
├── .venv/              ← Poetry (invoke setup) - for pre-commit hooks
├── src/galileo/        ← Main SDK source (shared via editable install)
└── galileo-adk/
    ├── .venv/          ← UV (uv sync) - for ADK development
    └── src/galileo_adk/
```

### Setup

```bash
cd galileo-adk
uv sync
```

This installs `galileo` in **editable mode** from `../src/galileo/`. Changes to either package are immediately available without reinstalling.

### Testing

```bash
source .venv/bin/activate
pytest tests -v
ruff check src/
```

### Publishing

The `[tool.uv].sources` override is **dev-only** and ignored when building wheels. Published packages use the standard `dependencies` from `pyproject.toml`.

**Release sequence (when both packages change):**

1. Merge changes to `galileo` (main SDK)
2. Wait for `galileo` to publish to PyPI
3. Update `galileo-adk/pyproject.toml` version constraint if needed:
   ```toml
   dependencies = [
       "galileo>=1.40.0,<2.0.0",  # bump minimum version
   ]
   ```
4. Merge and publish `galileo-adk`


## License

Apache-2.0
