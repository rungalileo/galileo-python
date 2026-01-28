## Project Overview

Galileo Python SDK (`galileo` on PyPI) - the official Python client library for the Galileo AI platform. It enables logging and tracing of LLM calls, experiments, datasets, prompt management, and more.

**Key characteristics:**
- Public SDK published to PyPI (external contributors welcome)
- Depends on `galileo-core` for shared schemas and infrastructure (see Known Issues)
- Uses auto-generated API client from OpenAPI specification
- Supports multiple LLM frameworks: OpenAI, LangChain, CrewAI, OpenAI Agents SDK

## Build & Development Commands

```bash
# Install dependencies (requires poetry)
poetry install --all-extras --no-root

# Full setup (install + pre-commit hooks)
inv setup

# Run all tests (parallel by default)
poetry run pytest

# Run single test file
poetry run pytest tests/test_decorator.py

# Run single test
poetry run pytest tests/test_decorator.py::test_function_name -v

# Run tests with coverage
inv test

# Type checking
inv type-check

# Linting (via pre-commit)
poetry run ruff check --fix src/
poetry run ruff format src/
```

## Architecture

### Package Structure

```
src/galileo/
├── __future__/              # New object-centric API (WIP)
│   ├── project.py           # Project domain object
│   ├── dataset.py           # Dataset domain object
│   ├── experiment.py        # Experiment domain object
│   ├── prompt.py            # Prompt domain object
│   ├── log_stream.py        # LogStream domain object
│   ├── configuration.py     # Configuration management
│   └── shared/              # Shared utilities (filters, sorting, base classes)
├── logger/                  # Core logging functionality
│   └── logger.py            # GalileoLogger - central trace/span management
├── handlers/                # Framework-specific integrations
│   ├── langchain/           # LangChain callback handler (GalileoCallback)
│   ├── crewai/              # CrewAI event listener
│   └── openai_agents/       # OpenAI Agents SDK integration
├── openai/                  # Drop-in OpenAI client wrapper (auto-logging)
├── resources/               # Auto-generated API client (DO NOT EDIT)
├── schema/                  # Pydantic models for SDK-specific types
├── utils/                   # Utility functions and helpers
├── datasets.py              # Dataset service (current API)
├── experiments.py           # Experiment service (current API)
├── prompts.py               # Prompt service (current API)
├── projects.py              # Project service (current API)
├── log_streams.py           # LogStream service (current API)
├── decorator.py             # @log decorator and galileo_context
└── config.py                # GalileoPythonConfig configuration
```

### Core Components

**GalileoLogger** (`src/galileo/logger/logger.py`): Central class for uploading traces to Galileo. Supports batch and streaming modes. Manages traces, spans (LLM, retriever, tool, workflow, agent), and sessions.

**Decorators** (`src/galileo/decorator.py`): The `@log` decorator and `galileo_context` context manager for automatic function tracing. Uses ContextVars for thread-safe nested span tracking.

**Handlers** (`src/galileo/handlers/`): Framework-specific integrations:
- `langchain/` - LangChain callback handler (`GalileoCallback`)
- `crewai/` - CrewAI handler (uses lazy imports to avoid side effects)
- `openai_agents/` - OpenAI Agents SDK integration

**OpenAI Wrapper** (`src/galileo/openai/`): Drop-in replacement for OpenAI client that auto-logs calls.

**`__future__` Package** (`src/galileo/__future__/`): New object-centric API implementing the "Golden Flow" patterns. Provides intuitive, Pythonic interfaces for domain objects (Project, Dataset, Prompt, Experiment, LogStream). Released incrementally as stable.

### Auto-Generated Code

**Resources** (`src/galileo/resources/`): Auto-generated API client from OpenAPI spec. **Excluded from linting/type-checking.** Never edit manually.

```bash
# Regenerate API client
./scripts/import-openapi-yaml.sh https://api.galileo.ai/client
./scripts/auto-generate-api-client.sh
```

**Important:** The OpenAPI spec comes from the **Client API** (`/client`), not the main API (`/docs`). The Client API is a curated subset designed specifically for SDK consumption.

### Dependency on galileo-core

The SDK depends on `galileo-core` for shared schemas, helpers, and base classes:
- `galileo_core.schemas.logging.*` - Span types (LlmSpan, ToolSpan, etc.), Trace, Session
- `galileo_core.helpers.*` - API key management, execution utilities
- `galileo_core.schemas.protect.*` - Protection/guardrails schemas

**Note:** There is ongoing work to reduce/eliminate this dependency. See Known Issues section.

## Key Patterns

### Object-Centric Design (`__future__` package)

Domain objects follow consistent patterns:

```python
from galileo.__future__ import Project, Dataset

# Factory methods (class-level)
project = Project.get(name="my-project")      # Retrieve existing
projects = Project.list()                      # List all

# Instance creation with lifecycle
project = Project(name="new-project")          # LOCAL_ONLY state
project.create()                               # → SYNCED state

# Fluent creation
project = Project(name="new-project").create() # 2-in-1

# Relationship methods
log_streams = project.list_log_streams()
dataset = project.create_dataset(name="test-data", content=[...])

# Child → Parent navigation
dataset.project  # Returns parent Project object
```

### State Management

Objects have explicit sync states: `LOCAL_ONLY`, `SYNCED`, `DIRTY`, `FAILED_SYNC`, `DELETED`

```python
project = Project(name="test")     # LOCAL_ONLY
project.create()                    # → SYNCED
project.name = "renamed"            # → DIRTY
project.save()                      # → SYNCED
project.delete()                    # → DELETED
```

### Service Layer (Current API)

Services provide functional interfaces for those who prefer procedural style:

```python
from galileo.datasets import create_dataset, get_dataset, list_datasets
from galileo.experiments import run_experiment

dataset = create_dataset(name="test", content=[...])
results = run_experiment(
    experiment_name="eval-1",
    dataset=dataset,
    prompt_template=get_prompt(name="my-prompt"),
    metrics=["correctness"],
    project="my-project"
)
```

### Logging with Decorators

```python
from galileo import log, galileo_context

# Auto-trace function calls
@log
def my_workflow():
    call_llm()
    call_llm()

# Explicit span types
@log(span_type="retriever")
def retrieve_docs(query: str):
    return ["doc1", "doc2"]

# Context manager for explicit control
with galileo_context(project="my-project", log_stream="prod"):
    my_workflow()
```

### Handler Integrations

```python
# LangChain
from galileo.handlers.langchain import GalileoCallback
callback = GalileoCallback()
llm = ChatOpenAI(callbacks=[callback])

# CrewAI
from galileo.handlers.crewai import CrewAIEventListener
listener = CrewAIEventListener(project="my-project")
# Listener auto-registers; use auto_setup_listeners=False in tests

# OpenAI (drop-in wrapper)
from galileo.openai import openai
client = openai.OpenAI()  # Auto-logs all calls
```

## Testing

Tests use pytest with these key fixtures from `tests/conftest.py`:
- `mock_request` - HTTP request mocking (from `galileo_core[testing]`)
- `mock_healthcheck`, `mock_login_api_key`, `mock_get_current_user` - Common API mocks

### Test Environment

Environment variables are set in `conftest.py` for pytest-xdist compatibility:
```python
GALILEO_CONSOLE_URL=http://localtest:8088
GALILEO_API_KEY=api-1234567890
GALILEO_PROJECT=test-project
GALILEO_LOG_STREAM=test-log-stream
```

Tests run with `--disable-socket` to prevent real network calls.

### Testing Guidelines

```python
def test_example(mock_request, mock_healthcheck, mock_login_api_key):
    # Mock API responses
    mock_request.post("/datasets").respond(json={"id": "123", "name": "test"})

    # Test SDK functionality
    dataset = create_dataset(name="test", content=[...])
    assert dataset.id == "123"
```

### Handler Testing (CrewAI)

CrewAI imports have global side effects. Use lazy imports and `auto_setup_listeners=False`:

```python
def test_crewai_handler():
    # Import inside test, not at module level
    from galileo.handlers.crewai import CrewAIEventListener

    listener = CrewAIEventListener(
        project="test",
        auto_setup_listeners=False  # Prevents import side effects
    )
```

### Given/When/Then Testing Style

Use behavioral testing comments to structure tests clearly. Add inline comments before each section:

- `# Given: <description>` - Before setup/arrangement code. Describe the preconditions.
- `# When: <description>` - Before the action being tested. Describe what action is performed.
- `# Then: <description>` - Before assertions. Describe the expected outcome.

**Important rules:**

- Comments must include a human-readable description after the colon - never leave them empty
- Use sentence case for descriptions (e.g., "a user with admin permissions", not "A User With Admin Permissions")
- Keep descriptions concise but meaningful
- For tests where the action raises an exception, use `# When/Then: <description>` combined

```python
def test_create_project_success(mock_request, mock_healthcheck, mock_login_api_key):
    # Given: a valid project name and mocked API response
    mock_request.post("/projects").respond(json={"id": "123", "name": "test"})

    # When: creating a new project
    project = Project(name="test").create()

    # Then: the project is created with the expected ID
    assert project.id == "123"
    assert project.name == "test"
```

## Code Style & Conventions

- **Line length:** 120 characters
- **Linting:** ruff (replaces flake8, isort, etc.)
- **Type annotations:** Required for public functions (mypy)
- **Docstrings:** numpy convention
- **Pre-commit hooks:** Run ruff and mypy on commit

### Required Practices

- Use standard Python logging: `import logging; logger = logging.getLogger(__name__)`
- Duration variables must be suffixed with units: `timeout_seconds`, `delay_ms`
- Commit messages: `type(scope): description` (conventional commits)
- **Imports at top of file**: Always place imports at the module level, not inside functions
- Exception: Lazy imports for optional dependencies (e.g., crewai) - document why
- Use `from __future__ import annotations` for forward references

### Error Handling Architecture

The SDK distinguishes between two types of operations with different error handling needs:

**Resource Management Operations** (raise exceptions):
- Operations where users explicitly request an action and expect feedback
- Examples: `create_project()`, `get_dataset()`, `delete_log_stream()`, `list_projects()`
- These operations should raise exceptions on failure for clear user feedback

**Telemetry/Ingestion Operations** (resilient):
- Background operations that observe user code without interfering
- Examples: `ingest_traces()`, `ingest_spans()`, `flush()`
- These operations swallow infrastructure errors gracefully
- Principle: Observability code should observe, not interfere

```
┌─────────────────────────────────────────────────────────────────┐
│                     User Application                            │
└─────────────────────────────────────────────────────────────────┘
                              │
        ┌─────────────────────┴─────────────────────┐
        │                                           │
        ▼                                           ▼
┌───────────────────┐                   ┌───────────────────────┐
│ Resource Mgmt     │                   │ Telemetry/Ingestion   │
│ (Raises on Error) │                   │ (Resilient)           │
├───────────────────┤                   ├───────────────────────┤
│ Projects          │                   │ Traces.ingest_*()     │
│ Datasets          │                   │ Traces.update_*()     │
│ LogStreams        │                   │ Logger streaming      │
│ Stages            │                   │ @warn_catch_exception │
└───────────────────┘                   └───────────────────────┘
        │                                           │
        ▼                                           ▼
┌─────────────────────────────────────────────────────────────────┐
│              Generated API Client                               │
│              (Always raises HTTP exceptions)                    │
└─────────────────────────────────────────────────────────────────┘
```

**HTTP-Specific Exceptions:**

| Status Code | Exception | Meaning |
|-------------|-----------|---------|
| 400 | `BadRequestError` | Invalid request parameters |
| 401 | `AuthenticationError` | Invalid or expired API key |
| 403 | `ForbiddenError` | Insufficient permissions |
| 404 | `NotFoundError` | Resource doesn't exist |
| 409 | `ConflictError` | Resource already exists |
| 422 | `HTTPValidationError` | Request body/params failed Pydantic validation |
| 429 | `RateLimitError` | Too many requests |
| 5xx | `ServerError` | Server-side error |

**Infrastructure Exceptions** (caught only in telemetry operations):
```python
INFRASTRUCTURE_EXCEPTIONS = (
    httpx.HTTPError,
    httpx.TimeoutException,
    httpx.ConnectError,
    ConnectionError,
    TimeoutError,
    OSError,
)
```

User errors like `TypeError`, `ValueError`, and `ValidationError` are never caught - they propagate immediately.

### Logging Convention

```python
import logging
logger = logging.getLogger(__name__)

# Log lifecycle events with context
logger.info("Project.create: name=%s – started", name)
logger.info("Project.create: id=%s – completed", project_id)
logger.error("Project.update: id=%s – failed: %s", project_id, error)

# Never log sensitive data (tokens, API keys, PII)
```

**When to Add Logging:**
- Service methods that perform writes (create, update, delete)
- Error conditions with full context when catching exceptions
- Long-running operations (start/completion with duration)

**What NOT to Log:**
- Sensitive data: Passwords, API keys, tokens, PII
- Large payloads: Don't log entire request/response bodies
- High-frequency loops: Use sampling or aggregate metrics

## Known Issues and Architectural Decisions

### 1. galileo-core Dependency

The SDK has a deep dependency on `galileo-core` (private repository). This creates:
- Contributor friction (requires private repo access)
- Contract split between core and SDK
- Inheritance of internal complexity

**Mitigation in progress:** Gradual migration to OpenAPI-generated types and SDK-owned abstractions.

### 2. Configuration State Management

Configuration exists in three places:
- `Configuration` class attributes (new `__future__` API)
- `os.environ` (synced by Configuration)
- `GalileoPythonConfig._instance` (actual authenticated state from core)

**Known issue:** `connect()` must be called explicitly; lazy initialization is incomplete.

### 3. Prompt Version Management

`Prompt.create_version()` creates a NEW prompt (name with timestamp suffix), not a new version of the same template. True version management requires API alignment.

### 4. Dataset Version Indexing

API uses **1-based** version indexing, not 0-based:
```python
# Correct: first version is index 1
version_content = dataset.get_version(index=1)

# Wrong: index 0 doesn't exist
version_content = dataset.get_version(index=0)  # Returns None
```

### 5. Experiment-Playground Conflation

The SDK's `Experiment` class conflates two distinct API concepts:
- **Playground**: Interactive workspace for prompt iteration
- **Experiment**: Immutable logged run with recorded results

Version specification for datasets and prompts is implicit (uses "current" version).

### 6. Metadata Type Handling

SDK converts all metadata values to strings. API behavior varies:
- Trace API: Skips `None` values and non-primitives
- Dataset API: Keeps `None` as null, JSON-encodes nested dicts

## Release Process

Releases use python-semantic-release with conventional commits:

```bash
# Patch release triggers
fix:, perf:, chore:, docs:, style:, refactor:

# Version is managed in:
# - src/galileo/__init__.py:__version__
# - pyproject.toml:project.version
```

## Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `GALILEO_CONSOLE_URL` | Yes* | Galileo console URL (default: app.galileo.ai) |
| `GALILEO_API_KEY` | Yes | API key for authentication |
| `GALILEO_PROJECT` | No | Default project name |
| `GALILEO_LOG_STREAM` | No | Default log stream name |
| `GALILEO_LOGGING_DISABLED` | No | Disable trace collection |

*Required for non-production environments

## References

- **PyPI:** https://pypi.org/project/galileo/
- **GitHub:** https://github.com/rungalileo/galileo-python
- **API Docs:** https://docs.galileo.ai
- **OpenAPI Spec:** `openapi.yaml` (generated from Client API)
