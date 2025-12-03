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

from galileo.config import GalileoPythonConfig
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
    from opentelemetry.sdk.trace import Span, SpanProcessor  # pyright: ignore[reportAssignmentType]
    from opentelemetry.sdk.trace.export import BatchSpanProcessor  # pyright: ignore[reportAssignmentType]
    from opentelemetry.trace import Tracer

    OTEL_AVAILABLE = True
except ImportError:
    # Create stub classes if OpenTelemetry is not available
    class OTLPSpanExporter:  # type: ignore[no-redef]
        def __init__(self, *args, **kwargs) -> NoReturn:  # type: ignore[no-untyped-def]
            raise ImportError(INSTALL_ERR_MSG)

    class BatchSpanProcessor:  # type: ignore[no-redef]
        def __init__(self, *args, **kwargs) -> NoReturn:  # type: ignore[no-untyped-def]
            raise ImportError(INSTALL_ERR_MSG)

    class Span:  # type: ignore[no-redef]
        def __init__(self, *args, **kwargs) -> NoReturn:  # type: ignore[no-untyped-def]
            raise ImportError(INSTALL_ERR_MSG)

    class SpanProcessor:  # type: ignore[no-redef]
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

        if not config.api_key:
            raise ValueError("API key is required.")

        # Resolve project and logstream from parameters or environment variables
        self.project = project or os.environ.get("GALILEO_PROJECT")
        self.logstream = logstream or os.environ.get("GALILEO_LOGSTREAM")

        if not self.project:
            self.project = f"project_{uuid.uuid4()}"

        if not self.logstream:
            self.logstream = "default"

        exporter_headers = {
            "Galileo-API-Key": config.api_key.get_secret_value() if config.api_key else None,
            "project": self.project,
            "logstream": self.logstream,
            "X-Use-Otel-New": str(kwargs.pop("use_new_otel", False)).lower(),
        }

        super().__init__(endpoint=endpoint, headers=exporter_headers, **kwargs)


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
        *,
        use_new_otel: bool = True,
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

        # Create the exporter using the config-based approach
        self._exporter = GalileoOTLPExporter(project=project, logstream=logstream, use_new_otel=use_new_otel)

        if SpanProcessor is None:
            SpanProcessor = BatchSpanProcessor

        self._processor = SpanProcessor(self._exporter)

    def on_start(self, span: Span, parent_context: Optional[context.Context] = None) -> None:
        """Handle span start events by delegating to the underlying processor."""
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
