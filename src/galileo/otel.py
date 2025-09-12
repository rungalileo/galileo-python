"""Galileo OpenTelemetry Tracing Helpers
========================

This module gives you everything you need to start exporting **OpenTelemetry** traces
from your Python code to **Galileo**.

Quick start
-----------
```python
from galileo.otel import enable_tracing

# One‑liner to bootstrap tracing
enable_tracing(
    api_key="<YOUR_API_KEY>",
    project_name="my‑project",
    log_stream="my_log_stream"
)


Environment variables (optional)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
If you'd rather use **env‑vars** instead of parameters you can set:
* ``GALILEO_API_KEY`` – API key
* ``GALILEO_PROJECT`` – default project
* ``GALILEO_LOG_STREAM`` – default log‑stream

The helper will also populate the OTLP variables (``OTEL_EXPORTER_OTLP_*``) so *other* OTLP aware
code you might run in the same process will automatically reuse the same exporter.

Documentation
~~~~~~~~~~~~~
See https://v2docs.galileo.ai for a deep‑dive into spans, traces and how Galileo models Gen‑AI
workflows.
"""

from __future__ import annotations

import importlib
import logging
import os
import urllib.parse
from uuid import UUID

from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor

from galileo.api_client import GalileoApiClient
from galileo.constants import DEFAULT_API_URL, DEFAULT_APP_URL

logger = logging.getLogger(__name__)


def _set_destination(console_url: str) -> str:
    """
    Parse the console_url and return the destination for the OpenTelemetry traces.
    """
    destination = console_url or GalileoApiClient.get_console_url()
    destination = destination.replace("console.", "api.")
    parsed_url = urllib.parse.urlparse(destination)
    if parsed_url.netloc in [
        urllib.parse.urlparse(DEFAULT_APP_URL).netloc,
        urllib.parse.urlparse(DEFAULT_API_URL).netloc,
    ]:
        return f"{DEFAULT_APP_URL}api/galileo/otel/traces"

    return f"{parsed_url.scheme}://{parsed_url.netloc}/otel/traces"


def enable_tracing(
    *,
    api_key: str | None = None,
    project_name: str | None = None,
    log_stream: str | None = None,
    session_id: str | UUID | None = None,
    console_url: str = "",
    auto_instrument: bool = True,
) -> None:
    """Configure OpenTelemetry to export spans to **Galileo**.

    Parameters
    ----------
    api_key
        Your Galileo API key. If *None*, we fall back to ``GALILEO_API_KEY``.
    project_name
        Name of the Galileo project. Falls back to ``GALILEO_PROJECT``.
    log_stream
        Run / log‑stream name shown in Galileo. Falls back to ``GALILEO_LOG_STREAM``.
    session_id
        A unique identifier for a session. If provided, all traces will be associated
        with this session. Can be a ``str`` or a ``uuid.UUID`` object. Falls back to
        ``GALILEO_SESSION_ID``.
    console_url
        Full console_url. Leave as default unless you run in a self hosted environment.
    auto_instrument
        Automatically call ``*.instrument()`` on supported Gen‑AI instrumentors – skipped
        gracefully if libraries are missing.
    """

    endpoint = _set_destination(console_url)
    exporter = OTLPSpanExporter(endpoint=endpoint)

    # Compose Galileo auth / routing headers
    session_id = session_id or os.getenv("GALILEO_SESSION_ID")
    api_key = api_key or os.getenv("GALILEO_API_KEY")
    project_name = project_name or os.getenv("GALILEO_PROJECT")
    log_stream = log_stream or os.getenv("GALILEO_LOG_STREAM")

    if not api_key:
        raise ValueError("Galileo API key missing – provide `api_key=` or set GALILEO_API_KEY env‑var")
    if not project_name:
        raise ValueError("Galileo project name missing – provide `project_name=` or set GALILEO_PROJECT env‑var")
    if not log_stream:
        raise ValueError("Galileo log_stream name missing – provide `log_stream=` or set GALILEO_LOG_STREAM env‑var")

    galileo_headers = {"Galileo-API-Key": api_key, "project": project_name, "logstream": log_stream}

    if session_id:
        galileo_headers["session_id"] = str(session_id)

    # Make headers discoverable for *other* OTLP aware libs
    os.environ["OTEL_EXPORTER_OTLP_TRACES_HEADERS"] = ",".join(f"{k}={v}" for k, v in galileo_headers.items())

    # Spin up a TracerProvider with **Batch** processor
    provider = TracerProvider()
    provider.add_span_processor(BatchSpanProcessor(exporter))
    trace.set_tracer_provider(provider)

    # (Optional) auto‑instrument popular Gen‑AI libs
    if auto_instrument:
        _safe_instrument("openinference.instrumentation.openai", "OpenAIInstrumentor")
        _safe_instrument("openinference.instrumentation.litellm", "LiteLLMInstrumentor")
        _safe_instrument("openinference.instrumentation.langchain", "LangchainInstrumentor")
        _safe_instrument("openinference.instrumentation.crewai", "CrewAIInstrumentor")
        _safe_instrument("openinference.instrumentation.google_genai", "GoogleGenAIInstrumentor")
        _safe_instrument("openinference.instrumentation.vertexai", "VertexAIInstrumentor")
        _safe_instrument("openinference.instrumentation.llama_index", "LlamaIndexInstrumentor")

    logger.info("Galileo tracing enabled – exporting to %s", endpoint)


def _safe_instrument(module_path: str, class_name: str) -> None:
    """Import *module_path* and call ``ClassName().instrument()`` if available."""
    try:
        module = importlib.import_module(module_path)
        cls = getattr(module, class_name)
        instrumentor = cls()
        if not getattr(instrumentor, "is_instrumented", lambda: False)():
            instrumentor.instrument()
    except ModuleNotFoundError:
        # Totally fine – user just doesn't have that lib installed.
        logger.debug("%s not installed – skipping instrumentation", module_path)
    except Exception as exc:  # pylint: disable=broad-except
        logger.warning("Failed to auto-instrument %s: %s", module_path, exc)
