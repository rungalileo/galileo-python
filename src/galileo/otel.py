import contextvars
import json
import logging
import os
import typing
import uuid
from _contextvars import ContextVar
from collections.abc import Generator
from contextlib import contextmanager
from typing import Any, NoReturn, Optional, Protocol, cast
from urllib.parse import urljoin

from requests import Session

from galileo.config import GalileoPythonConfig
from galileo.decorator import _experiment_id_context, _log_stream_context, _project_context, _session_id_context
from galileo.utils.retrievers import document_adapter
from galileo_core.schemas.logging.span import RetrieverSpan
from galileo_core.schemas.logging.span import Span as GalileoSpan

logger = logging.getLogger(__name__)

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


_TRACE_PROVIDER_CONTEXT_VAR: ContextVar[Optional[TracerProvider]] = contextvars.ContextVar(
    "galileo_trace_provider", default=None
)


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

        if project is not None:
            _project_context.set(project)
        if logstream is not None:
            _log_stream_context.set(logstream)

        # Resolve project and logstream from parameters, context, or environment variables
        # Check context first, then environment, then generate/use defaults
        ctx_project = _project_context.get(None)
        ctx_logstream = _log_stream_context.get(None)

        if ctx_project is not None:
            self.project = ctx_project
        elif "GALILEO_PROJECT" in os.environ:
            self.project = os.environ["GALILEO_PROJECT"]
        else:
            self.project = f"project_{uuid.uuid4()}"

        if ctx_logstream is not None:
            self.logstream = ctx_logstream
        elif "GALILEO_LOG_STREAM" in os.environ:
            self.logstream = os.environ["GALILEO_LOG_STREAM"]
        else:
            self.logstream = "default"

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
        if project is not None:
            _project_context.set(project)
        if logstream is not None:
            _log_stream_context.set(logstream)

        self._project = _project_context.get()
        self._logstream = _log_stream_context.get()

        # Create the exporter using the config-based approach
        self._exporter = GalileoOTLPExporter(**kwargs)

        if SpanProcessor is None:
            SpanProcessor = BatchSpanProcessor

        self._processor = SpanProcessor(self._exporter)

    def on_start(self, span: Span, parent_context: Optional[context.Context] = None) -> None:
        """Handle span start events by delegating to the underlying processor."""
        # Set Galileo context attributes on the span
        project = _project_context.get(self._project)
        log_stream = _log_stream_context.get(self._logstream)
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
        if isinstance(galileo_span, RetrieverSpan):
            _set_retriever_span_attributes(span, galileo_span)
