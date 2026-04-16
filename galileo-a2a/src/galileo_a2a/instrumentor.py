"""OpenTelemetry auto-instrumentor for the a2a-sdk Python library."""

from __future__ import annotations

import logging
from collections.abc import Collection
from typing import Any

from opentelemetry import trace
from opentelemetry.instrumentation.instrumentor import BaseInstrumentor  # type: ignore[import-untyped]

from galileo_a2a import _spans
from galileo_a2a._client_patches import _patch_client, _unpatch_client
from galileo_a2a._constants import INSTRUMENTOR_NAME, INSTRUMENTOR_VERSION
from galileo_a2a._server_patches import _patch_server, _unpatch_server

_logger = logging.getLogger(__name__)


class A2AInstrumentor(BaseInstrumentor):  # type: ignore[misc]
    """Auto-instrumentor for the ``a2a-sdk`` Python library.

    Patches client and server methods to produce OTel spans with A2A-specific
    attributes and cross-agent trace context propagation.

    Client-side patches (outbound calls):
        ``BaseClient.send_message``, ``get_task``, ``cancel_task``, ``get_card``

    Server-side patches (inbound requests):
        ``DefaultRequestHandler.on_message_send``, ``on_message_send_stream``

    Example::

        from opentelemetry.sdk.trace import TracerProvider
        from galileo.otel import GalileoSpanProcessor, add_galileo_span_processor
        from galileo_a2a import A2AInstrumentor

        provider = TracerProvider()
        add_galileo_span_processor(provider, GalileoSpanProcessor())
        A2AInstrumentor().instrument(tracer_provider=provider, agent_name="my-agent")

        # To disable message content capture (e.g. for PII compliance):
        A2AInstrumentor().instrument(tracer_provider=provider, capture_content=False)
    """

    def instrumentation_dependencies(self) -> Collection[str]:
        return ("a2a-sdk>=0.3.0,<1.0.0",)

    def _instrument(self, **kwargs: Any) -> None:
        tracer_provider = kwargs.get("tracer_provider")
        agent_name = kwargs.get("agent_name")
        capture_content = kwargs.get("capture_content", True)
        tracer = trace.get_tracer(INSTRUMENTOR_NAME, INSTRUMENTOR_VERSION, tracer_provider=tracer_provider)

        _spans.configure(capture_content=capture_content)
        _patch_client(tracer, agent_name=agent_name)
        _patch_server(tracer, agent_name=agent_name)

        _logger.info("A2A instrumentation enabled", extra={"agent_name": agent_name})

    def _uninstrument(self, **kwargs: Any) -> None:
        _unpatch_client()
        _unpatch_server()

        _logger.info("A2A instrumentation disabled")
