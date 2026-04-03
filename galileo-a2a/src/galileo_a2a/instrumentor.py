"""A2A auto-instrumentor for the a2a-sdk Python library."""

from __future__ import annotations

import logging
from collections.abc import Collection
from typing import Any

from opentelemetry import trace
from opentelemetry.instrumentation.instrumentor import BaseInstrumentor  # type: ignore[import-untyped]

from galileo_a2a._client_patches import _patch_client, _unpatch_client
from galileo_a2a._constants import INSTRUMENTOR_NAME, INSTRUMENTOR_VERSION
from galileo_a2a._server_patches import _patch_server, _unpatch_server

_logger = logging.getLogger(__name__)


class A2AInstrumentor(BaseInstrumentor):  # type: ignore[misc]
    """Auto-instrumentor for the ``a2a-sdk`` Python library.

    Monkey-patches client and server methods to create OTel spans with
    A2A-specific attributes and cross-agent trace context propagation.

    Client-side patches (outbound A2A calls):
        - ``BaseClient.send_message`` — creates span + injects trace context
        - ``BaseClient.get_task`` — creates span for task status checks
        - ``BaseClient.cancel_task`` — creates span for task cancellation
        - ``BaseClient.get_card`` — creates span for agent card discovery

    Server-side patches (inbound A2A requests):
        - ``DefaultRequestHandler.on_message_send`` — creates span + extracts trace context
        - ``DefaultRequestHandler.on_message_send_stream`` — same for streaming

    Usage
    -----
    >>> from opentelemetry.sdk.trace import TracerProvider
    >>> from galileo.otel import GalileoSpanProcessor, add_galileo_span_processor
    >>> from galileo_a2a import A2AInstrumentor
    >>>
    >>> provider = TracerProvider()
    >>> processor = GalileoSpanProcessor(project="my-app", logstream="my-agent")
    >>> add_galileo_span_processor(provider, processor)
    >>>
    >>> A2AInstrumentor().instrument(tracer_provider=provider, agent_name="my-agent")

    Parameters (passed to instrument())
    ------------------------------------
    tracer_provider : TracerProvider, optional
        OTel tracer provider. Falls back to the global provider if not specified.
    agent_name : str, optional
        Name of this agent, set on spans as ``gen_ai.agent.name``.
    """

    def instrumentation_dependencies(self) -> Collection[str]:
        """Return the a2a-sdk dependency requirement."""
        return ("a2a-sdk>=0.3.0,<1.0.0",)

    def _instrument(self, **kwargs: Any) -> None:
        """Patch a2a-sdk client and server methods."""
        tracer_provider = kwargs.get("tracer_provider")
        agent_name = kwargs.get("agent_name")
        tracer = trace.get_tracer(INSTRUMENTOR_NAME, INSTRUMENTOR_VERSION, tracer_provider=tracer_provider)

        _patch_client(tracer, agent_name=agent_name)
        _patch_server(tracer, agent_name=agent_name)

        _logger.info(
            "A2A instrumentation enabled",
            extra={"agent_name": agent_name},
        )

    def _uninstrument(self, **kwargs: Any) -> None:
        """Restore original a2a-sdk methods."""
        _unpatch_client()
        _unpatch_server()

        _logger.info("A2A instrumentation disabled")
