import json
import logging
import typing
from collections.abc import Generator
from contextlib import contextmanager
from contextvars import ContextVar
from typing import Any, NoReturn, Optional, Protocol, cast
from urllib.parse import urljoin

from requests import Session

from galileo.config import GalileoPythonConfig
from galileo.decorator import _experiment_id_context, _log_stream_context, _project_context, _session_id_context
from galileo.utils.env_helpers import _get_log_stream_or_default, _get_project_or_default
from galileo.utils.retrievers import document_adapter
from galileo_core.schemas.logging.span import RetrieverSpan, ToolSpan, WorkflowSpan
from galileo_core.schemas.logging.span import Span as GalileoSpan

logger = logging.getLogger(__name__)

# Context variables for dataset fields (ground truth/reference output)
# These allow setting ground truth data that will be attached to all spans
# created within the context, enabling scorers that require reference output.
_dataset_input_context: ContextVar[Optional[str]] = ContextVar("dataset_input_context", default=None)
_dataset_output_context: ContextVar[Optional[str]] = ContextVar("dataset_output_context", default=None)
_dataset_metadata_context: ContextVar[Optional[dict[str, str]]] = ContextVar("dataset_metadata_context", default=None)

INSTALL_ERR_MSG = (
    "OpenTelemetry packages are not installed. "
    "Install optional OpenTelemetry dependencies with: pip install galileo[otel]"
)


try:
    from opentelemetry import context, trace
    from opentelemetry.exporter.otlp.proto.http.trace_exporter import (
        OTLPSpanExporter,  # pyright: ignore[reportAssignmentType]
    )
    from opentelemetry.sdk.resources import Resource  # pyright: ignore[reportAssignmentType]
    from opentelemetry.sdk.trace import Span, SpanProcessor  # pyright: ignore[reportAssignmentType]
    from opentelemetry.sdk.trace.export import BatchSpanProcessor  # pyright: ignore[reportAssignmentType]
    from opentelemetry.trace import Tracer  # pyright: ignore[reportAssignmentType]

    OTEL_AVAILABLE = True
except ImportError:
    # Create stub classes if OpenTelemetry is not available
    class OTLPSpanExporter:  # type: ignore[no-redef]
        def __init__(self, *args, **kwargs) -> NoReturn:  # type: ignore[no-untyped-def]
            raise ImportError(INSTALL_ERR_MSG)

        def export(self, spans: typing.Sequence[Any]) -> "Any":
            raise ImportError(INSTALL_ERR_MSG)

    class Span:  # type: ignore[no-redef]
        def __init__(self, *args, **kwargs) -> NoReturn:  # type: ignore[no-untyped-def]
            raise ImportError(INSTALL_ERR_MSG)

        def set_attribute(self, *args, **kwargs) -> NoReturn:  # type: ignore[no-untyped-def]
            raise ImportError(INSTALL_ERR_MSG)

    class SpanProcessor:  # type: ignore[no-redef]
        def __init__(self, *args, **kwargs) -> NoReturn:  # type: ignore[no-untyped-def]
            raise ImportError(INSTALL_ERR_MSG)

    class Resource:  # type: ignore[no-redef]
        def __init__(self, *args, **kwargs) -> NoReturn:  # type: ignore[no-untyped-def]
            raise ImportError(INSTALL_ERR_MSG)

    OTEL_AVAILABLE = False


class TracerProvider(Protocol):
    def add_span_processor(self, span_processor: Any) -> None: ...

    def get_tracer(
        self,
        instrumenting_module_name: str,
        instrumenting_library_version: typing.Optional[str] = None,
        schema_url: typing.Optional[str] = None,
        attributes: typing.Optional[Any] = None,
    ) -> "Tracer": ...


_TRACE_PROVIDER_CONTEXT_VAR: ContextVar[Optional[TracerProvider]] = ContextVar("galileo_trace_provider", default=None)


class GalileoOTLPExporter(OTLPSpanExporter):
    """
    OpenTelemetry OTLP span exporter preconfigured for Galileo platform integration.

    This exporter extends the standard OTLPSpanExporter with Galileo-specific
    configuration and authentication. For most applications, consider using
    GalileoSpanProcessor instead, which provides a complete tracing solution.
    """

    _session: Session

    def __init__(self, project: Optional[str] = None, logstream: Optional[str] = None, **kwargs: Any) -> None:
        """
        Initialize the Galileo OTLP exporter with authentication and endpoint configuration.

        Parameters
        ----------
        project : str, optional
            Target Galileo project name. Falls back to GALILEO_PROJECT environment variable.
        logstream : str, optional
            Target logstream for trace organization. Uses default logstream if not specified.
        **kwargs
            Additional configuration options passed to the underlying OTLPSpanExporter.

        Raises
        ------
        ValueError
            When configuration is not properly initialized with required credentials.
        """
        # Get configuration from GalileoPythonConfig
        config = GalileoPythonConfig.get()

        if not config.api_url:
            # This should never happen, but we'll raise an error just in case
            raise ValueError("API URL is required.")

        # Get API URL and construct OTLP endpoint
        base_url = str(config.api_url)
        # Ensure base_url ends with / for proper joining
        if not base_url.endswith("/"):
            base_url += "/"
        endpoint: str = urljoin(base_url, "otel/traces")
        api_key = config.api_key.get_secret_value() if config.api_key else None

        if not api_key:
            raise ValueError("API key is required.")

        # Resolve project and logstream: param first, then context var, then env var with default fallback
        ctx_project = project if project is not None else _project_context.get(None)
        ctx_logstream = logstream if logstream is not None else _log_stream_context.get(None)

        self.project = _get_project_or_default(ctx_project)
        self.logstream = _get_log_stream_or_default(ctx_logstream)

        exporter_headers = {"Galileo-API-Key": api_key, "project": self.project, "logstream": self.logstream}

        super().__init__(endpoint=endpoint, headers=exporter_headers, **kwargs)

    def export(self, spans: typing.Sequence[Any]) -> "Any":
        """Override export to set resource attributes from span attributes before serialization."""
        for span in spans:
            # Read from span attributes (set during on_start when context was available)
            project = span.attributes.get("galileo.project.name")
            logstream = span.attributes.get("galileo.logstream.name")
            session_id = span.attributes.get("galileo.session.id")
            experiment_id = span.attributes.get("galileo.experiment.id")
            dataset_input = span.attributes.get("galileo.dataset.input")
            dataset_output = span.attributes.get("galileo.dataset.output")
            dataset_metadata = span.attributes.get("galileo.dataset.metadata")

            # Build resource attributes dict, filtering out None values
            resource_attrs = {}
            if project:
                resource_attrs["galileo.project.name"] = project
            if logstream:
                resource_attrs["galileo.logstream.name"] = logstream
            if session_id:
                resource_attrs["galileo.session.id"] = session_id
            if experiment_id:
                resource_attrs["galileo.experiment.id"] = experiment_id
            if dataset_input:
                resource_attrs["galileo.dataset.input"] = dataset_input
            if dataset_output:
                resource_attrs["galileo.dataset.output"] = dataset_output
            if dataset_metadata:
                resource_attrs["galileo.dataset.metadata"] = dataset_metadata

            if resource_attrs:
                # Merge new attributes into span's resource
                new_resource = span.resource.merge(Resource(resource_attrs))
                # Mutate the internal _resource (ReadableSpan stores it there)
                span._resource = new_resource

        # for the last span update the headers
        if spans:
            last_span = spans[-1]
            self._session.headers.update(
                {
                    "project": last_span.attributes.get("galileo.project.name"),
                    "logstream": last_span.attributes.get("galileo.logstream.name"),
                }
            )

        return super().export(spans)


class GalileoSpanProcessor(SpanProcessor):
    """
    Complete OpenTelemetry span processor with integrated Galileo export functionality.

    This processor combines span processing and export capabilities into a single
    component that can be directly attached to any OpenTelemetry TracerProvider.
    It handles the complete lifecycle of spans from creation to export to Galileo.

    Examples
    --------
    >>> from opentelemetry.sdk.trace import TracerProvider
    >>> tracer_provider = TracerProvider()
    >>> processor = GalileoSpanProcessor(project="my-project")
    >>> add_galileo_span_processor(tracer_provider, processor)
    """

    def __init__(
        self,
        project: Optional[str] = None,
        logstream: Optional[str] = None,
        SpanProcessor: Optional[type] = None,
        **kwargs: Any,
    ) -> None:
        """
        Initialize the Galileo span processor with export configuration.

        Parameters
        ----------
        project : str, optional
            Target Galileo project for trace data. Falls back to GALILEO_PROJECT environment variable.
        logstream : str, optional
            Target logstream for trace organization. Uses default logstream if not specified.
        SpanProcessor : type, optional
            Custom span processor class. Defaults to BatchSpanProcessor for optimal performance.

        Raises
        ------
        ImportError
            When OpenTelemetry dependencies are not installed.
        """
        if not OTEL_AVAILABLE:
            raise ImportError(
                "OpenTelemetry packages are not installed. "
                "Install optional OpenTelemetry dependencies with: pip install galileo[otel]"
            )

        # Resolve project and logstream: param first, then context var, then env var with default fallback
        ctx_project = project if project is not None else _project_context.get(None)
        ctx_logstream = logstream if logstream is not None else _log_stream_context.get(None)

        self._project = _get_project_or_default(ctx_project)
        self._logstream = _get_log_stream_or_default(ctx_logstream)

        # Create the exporter using the config-based approach
        self._exporter = GalileoOTLPExporter(**kwargs)

        if SpanProcessor is None:
            SpanProcessor = BatchSpanProcessor

        self._processor = SpanProcessor(self._exporter)

    def on_start(self, span: Span, parent_context: Optional[context.Context] = None) -> None:
        """Handle span start events by delegating to the underlying processor."""
        # Set Galileo context attributes on the span
        # Use context var if set and not None, otherwise fall back to instance defaults
        project = _project_context.get(None) or self._project
        log_stream = _log_stream_context.get(None) or self._logstream
        experiment_id = _experiment_id_context.get(None)
        session_id = _session_id_context.get(None)

        if project:
            span.set_attribute("galileo.project.name", project)
        if log_stream:
            span.set_attribute("galileo.logstream.name", log_stream)
        if experiment_id:
            span.set_attribute("galileo.experiment.id", experiment_id)
        if session_id:
            span.set_attribute("galileo.session.id", session_id)

        # Set dataset attributes for ground truth/reference output support
        dataset_input = _dataset_input_context.get(None)
        dataset_output = _dataset_output_context.get(None)
        dataset_metadata = _dataset_metadata_context.get(None)

        if dataset_input is not None:
            span.set_attribute("galileo.dataset.input", dataset_input)
        if dataset_output is not None:
            span.set_attribute("galileo.dataset.output", dataset_output)
        if dataset_metadata is not None:
            span.set_attribute("galileo.dataset.metadata", json.dumps(dataset_metadata))

        self._processor.on_start(span, parent_context)

    def on_end(self, span: Span) -> None:
        """Handle span completion events by delegating to the underlying processor."""
        self._processor.on_end(span)

    def shutdown(self) -> None:
        """Gracefully shutdown the processor and flush any remaining spans."""
        self._processor.shutdown()
        logger.info(
            "Galileo span processor shutdown for project %s and logstream %s",
            self.exporter.project,
            self.exporter.logstream,
        )

    def force_flush(self, timeout_millis: int = 40000) -> None:
        """Force immediate export of all pending spans with specified timeout."""
        return self._processor.force_flush(timeout_millis)

    @property
    def exporter(self) -> GalileoOTLPExporter:
        """Access to the underlying Galileo OTLP exporter instance."""
        return self._exporter

    @property
    def processor(self) -> SpanProcessor:
        """Access to the underlying OpenTelemetry span processor instance."""
        return self._processor


def add_galileo_span_processor(tracer_provider: TracerProvider, processor: GalileoSpanProcessor) -> None:
    """Add the Galileo span processor to the tracer provider."""
    tracer_provider.add_span_processor(processor)
    _TRACE_PROVIDER_CONTEXT_VAR.set(tracer_provider)


def _set_retriever_span_attributes(span: trace.Span, galileo_span: RetrieverSpan) -> None:
    span.set_attribute("db.operation", "search")
    span.set_attribute("gen_ai.input.messages", json.dumps([{"role": "user", "content": galileo_span.input}]))
    span.set_attribute(
        "gen_ai.output.messages",
        json.dumps(
            [
                {
                    "role": "assistant",
                    "content": {"documents": document_adapter.dump_python(galileo_span.output, mode="json")},
                }
            ]
        ),
    )


def _set_tool_span_attributes(span: trace.Span, galileo_span: ToolSpan) -> None:
    span.set_attribute("gen_ai.operation.name", "execute_tool")
    span.set_attribute("gen_ai.tool.name", galileo_span.name)
    span.set_attribute("gen_ai.tool.call.arguments", galileo_span.input)
    span.set_attribute("gen_ai.input.messages", json.dumps([{"role": "tool", "content": galileo_span.input}]))
    if galileo_span.output is not None:
        span.set_attribute("gen_ai.tool.call.result", galileo_span.output)
        span.set_attribute("gen_ai.output.messages", json.dumps([{"role": "tool", "content": galileo_span.output}]))
    if galileo_span.tool_call_id is not None:
        span.set_attribute("gen_ai.tool.call.id", galileo_span.tool_call_id)


def _set_dataset_attributes(span: trace.Span, galileo_span: GalileoSpan) -> None:
    """Set OpenTelemetry attributes for dataset fields (ground truth/reference output).

    These attributes enable scorers that require ground truth data to work
    with OTEL-ingested traces.
    """
    if galileo_span.dataset_input:
        span.set_attribute("galileo.dataset.input", galileo_span.dataset_input)
    if galileo_span.dataset_output:
        span.set_attribute("galileo.dataset.output", galileo_span.dataset_output)
    if galileo_span.dataset_metadata:
        span.set_attribute("galileo.dataset.metadata", json.dumps(galileo_span.dataset_metadata))


def _set_workflow_span_attributes(span: trace.Span, galileo_span: WorkflowSpan) -> None:
    """Set OpenTelemetry attributes for WorkflowSpan."""
    # Handle input - Union[str, Sequence[Message]]
    if isinstance(galileo_span.input, str):
        input_messages = [{"role": "user", "content": galileo_span.input}]
    else:
        # Sequence[Message] - serialize each message
        input_messages = []
        for msg in list(galileo_span.input):
            if hasattr(msg, "model_dump"):
                input_messages.append(msg.model_dump(exclude_none=True))
            else:
                input_messages.append(msg)
    span.set_attribute("gen_ai.input.messages", json.dumps(input_messages))

    # Handle output - Union[str, Message, Sequence[Document], None]
    if galileo_span.output is None:
        return

    output_value = galileo_span.output
    # Type annotation to handle flexible content types (string or dict)
    # Content can be: str (simple output), dict (documents), or dict (Message model_dump)
    output_messages: list[dict[str, Any]] = []

    if isinstance(output_value, str):
        output_messages = [{"role": "assistant", "content": output_value}]
    elif hasattr(output_value, "model_dump"):
        # Single Message
        output_messages = [output_value.model_dump(exclude_none=True)]
    else:
        # Sequence[Document] - wrap in assistant message
        # Use document_adapter for consistency with _set_retriever_span_attributes
        output_messages = [
            {
                "role": "assistant",
                "content": {"documents": document_adapter.dump_python(list(output_value), mode="json")},
            }
        ]

    span.set_attribute("gen_ai.output.messages", json.dumps(output_messages))


@contextmanager
def start_galileo_span(galileo_span: GalileoSpan) -> Generator[trace.Span, Any, None]:
    tracer_provider = _TRACE_PROVIDER_CONTEXT_VAR.get()
    if tracer_provider is None:
        tracer_provider = trace.get_tracer_provider()
        _TRACE_PROVIDER_CONTEXT_VAR.set(cast(TracerProvider, tracer_provider))
    tracer = tracer_provider.get_tracer("galileo-tracer")
    with tracer.start_as_current_span(galileo_span.name) as span:
        yield span
        span.set_attribute("gen_ai.system", "galileo-otel")
        # Set dataset attributes for ground truth/reference output support
        _set_dataset_attributes(span, galileo_span)
        if isinstance(galileo_span, RetrieverSpan):
            _set_retriever_span_attributes(span, galileo_span)
        elif isinstance(galileo_span, ToolSpan):
            _set_tool_span_attributes(span, galileo_span)
        elif isinstance(galileo_span, WorkflowSpan):
            _set_workflow_span_attributes(span, galileo_span)


@contextmanager
def galileo_dataset_context(
    *,
    dataset_input: Optional[str] = None,
    dataset_output: Optional[str] = None,
    dataset_metadata: Optional[dict[str, str]] = None,
) -> Generator[None, None, None]:
    """
    Context manager to set dataset/ground truth information for OTEL spans.

    Use this when working with third-party OTEL instrumentation (e.g., Microsoft Agent Framework,
    LangChain, etc.) where you don't have direct control over span creation but need to attach
    ground truth data for scorers that require reference output.

    Parameters
    ----------
    dataset_input : str, optional
        The expected input from your dataset (ground truth input).
    dataset_output : str, optional
        The expected output/ground truth for scoring (e.g., for BLEU, exact match scorers).
    dataset_metadata : dict[str, str], optional
        Additional metadata from your dataset.

    Examples
    --------
    >>> from galileo.otel import galileo_dataset_context
    >>>
    >>> # Set ground truth for a single agent call
    >>> with galileo_dataset_context(
    ...     dataset_input="What is the capital of France?",
    ...     dataset_output="Paris",
    ...     dataset_metadata={"source": "geography_quiz"}
    ... ):
    ...     response = await agent.run("What is the capital of France?")
    >>>
    >>> # Use with experiment datasets
    >>> for row in dataset:
    ...     with galileo_dataset_context(
    ...         dataset_input=row["input"],
    ...         dataset_output=row["expected_output"],
    ...     ):
    ...         response = await agent.run(row["input"])
    """
    # Set new values and capture tokens for proper restoration
    token_input = _dataset_input_context.set(dataset_input)
    token_output = _dataset_output_context.set(dataset_output)
    token_metadata = _dataset_metadata_context.set(dataset_metadata)

    try:
        yield
    finally:
        # Reset to previous values using tokens (handles nested contexts correctly)
        _dataset_input_context.reset(token_input)
        _dataset_output_context.reset(token_output)
        _dataset_metadata_context.reset(token_metadata)
