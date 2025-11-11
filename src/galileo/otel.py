import logging
import os
import uuid
from typing import Any, NoReturn, Optional
from urllib.parse import urljoin

logger = logging.getLogger(__name__)

INSTALL_ERR_MSG = (
    "OpenTelemetry packages are not installed. "
    "Install optional OpenTelemetry dependencies with: pip install galileo[otel]"
)

try:
    from opentelemetry import context
    from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
    from opentelemetry.sdk.trace import Span, SpanProcessor
    from opentelemetry.sdk.trace.export import BatchSpanProcessor

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


class GalileoOTLPExporter(OTLPSpanExporter):
    """
    OpenTelemetry OTLP span exporter preconfigured for Galileo platform integration.

    This exporter extends the standard OTLPSpanExporter with Galileo-specific
    configuration and authentication. For most applications, consider using
    GalileoSpanProcessor instead, which provides a complete tracing solution.

    Supported Environment Variables:
        GALILEO_API_KEY: Authentication key for Galileo platform access
        GALILEO_CONSOLE_URL: Galileo Console base URL (default: https://api.galileo.ai)
        GALILEO_PROJECT: Target project name for trace data
        GALILEO_LOGSTREAM: Target logstream name for trace organization
    """

    def __init__(
        self,
        project: Optional[str] = None,
        logstream: Optional[str] = None,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        **kwargs: Any,
    ) -> None:
        """
        Initialize the Galileo OTLP exporter with authentication and endpoint configuration.

        Parameters
        ----------
        project : str, optional
            Target Galileo project name. Falls back to GALILEO_PROJECT environment variable.
        logstream : str, optional
            Target logstream for trace organization. Uses default logstream if not specified.
        base_url : str, optional
            Base URL for OTLP endpoint. Constructs {base_url}/otel/traces as the final endpoint.
        api_key : str, optional
            Galileo platform API key. Falls back to GALILEO_API_KEY environment variable.
        **kwargs
            Additional configuration options passed to the underlying OTLPSpanExporter.

        Raises
        ------
        ValueError
            When no API key is provided via parameter or environment variable.
        """
        processed_base_url = str(base_url or os.environ.get("GALILEO_CONSOLE_URL", "https://api.galileo.ai"))
        # Ensure base_url ends with / for proper joining
        if not processed_base_url.endswith("/"):
            processed_base_url += "/"
        endpoint: str = urljoin(processed_base_url, "/otel/traces")
        api_key = api_key or os.environ.get("GALILEO_API_KEY")

        # Resolve project and logstream from parameters or environment variables
        self.project = project or os.environ.get("GALILEO_PROJECT")
        self.logstream = logstream or os.environ.get("GALILEO_LOGSTREAM")

        if not self.project:
            self.project = f"project_{uuid.uuid4()}"

        if not self.logstream:
            self.logstream = "default"

        if not api_key:
            raise ValueError(
                "API key is required. Provide it via api_key parameter or GALILEO_API_KEY environment variable."
            )

        exporter_headers = {"Galileo-API-Key": api_key, "project": self.project, "logstream": self.logstream}

        super().__init__(endpoint=endpoint, headers=exporter_headers, **kwargs)


class GalileoSpanProcessor(SpanProcessor):
    """
    Complete OpenTelemetry span processor with integrated Galileo export functionality.

    This processor combines span processing and export capabilities into a single
    component that can be directly attached to any OpenTelemetry TracerProvider.
    It handles the complete lifecycle of spans from creation to export to Galileo.

    Usage Example:
        >>> processor = GalileoSpanProcessor(project="my-project")
        >>> tracer_provider.add_span_processor(processor)
    """

    def __init__(
        self,
        project: Optional[str] = None,
        logstream: Optional[str] = None,
        api_key: Optional[str] = None,
        api_url: Optional[str] = None,
        SpanProcessor: Optional[type] = None,
    ) -> None:
        """
        Initialize the Galileo span processor with export configuration.

        Parameters
        ----------
        project : str, optional
            Target Galileo project for trace data. Falls back to GALILEO_PROJECT environment variable.
        logstream : str, optional
            Target logstream for trace organization. Uses default logstream if not specified.
        api_key : str, optional
            Galileo platform API key. Falls back to GALILEO_API_KEY environment variable.
        api_url : str, optional
            Base URL for Galileo API endpoints. Falls back to GALILEO_API_URL environment variable.
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

        # Create the exporter
        # Convert api_url to the full endpoint URL that GalileoOTLPExporter expects
        self._exporter = GalileoOTLPExporter(base_url=api_url, api_key=api_key, project=project, logstream=logstream)

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
