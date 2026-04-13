"""Tests for server-side monkey-patching lifecycle and streaming wrappers."""

from types import SimpleNamespace
from unittest.mock import MagicMock, patch

import pytest
from opentelemetry.trace import Span, StatusCode, Tracer

from galileo_a2a._server_patches import _originals, _patch_server, _unpatch_server, _wrap_on_message_send_stream


@patch("galileo_a2a._server_patches.DefaultRequestHandler")
class TestPatchServer:
    def test_patches_all_methods(self, mock_handler):
        # Given: a fresh state
        _originals.clear()
        tracer = MagicMock(spec=Tracer)

        # When: patching
        _patch_server(tracer, agent_name="test")

        # Then: both methods stashed
        assert "DefaultRequestHandler.on_message_send" in _originals
        assert "DefaultRequestHandler.on_message_send_stream" in _originals

        # Cleanup
        _originals.clear()

    def test_idempotent_second_call_is_noop(self, mock_handler):
        # Given: already patched
        _originals.clear()
        tracer = MagicMock(spec=Tracer)
        _patch_server(tracer)

        original_send = mock_handler.on_message_send

        # When: patching again
        _patch_server(tracer)

        # Then: on_message_send not re-wrapped
        assert mock_handler.on_message_send == original_send

        # Cleanup
        _originals.clear()


@patch("galileo_a2a._server_patches.DefaultRequestHandler")
class TestUnpatchServer:
    def test_restores_originals(self, mock_handler):
        # Given: patched state
        _originals.clear()
        tracer = MagicMock(spec=Tracer)
        _patch_server(tracer)

        # When: unpatching
        _unpatch_server()

        # Then: originals dict is empty
        assert len(_originals) == 0

    def test_noop_when_not_patched(self, mock_handler):
        # Given: clean state
        _originals.clear()

        # When: unpatching
        _unpatch_server()

        # Then: no error
        assert len(_originals) == 0


def _make_tracer_and_span():
    """Create a mock Tracer that returns a mock Span from start_span."""
    span = MagicMock(spec=Span)
    tracer = MagicMock(spec=Tracer)
    tracer.start_span.return_value = span
    return tracer, span


def _text_part(text: str) -> SimpleNamespace:
    return SimpleNamespace(root=SimpleNamespace(text=text))


def _message(text: str) -> SimpleNamespace:
    return SimpleNamespace(parts=[_text_part(text)])


def _server_params(text: str = "hello") -> SimpleNamespace:
    return SimpleNamespace(message=_message(text), metadata=None)


async def _fake_on_message_send_stream(self, params, context=None):
    """Simulate DefaultRequestHandler.on_message_send_stream yielding events."""
    for event in [
        SimpleNamespace(parts=[_text_part("event-1")], status=None, id=None),
        SimpleNamespace(parts=[_text_part("event-2")], status=None, id=None),
    ]:
        yield event


async def _failing_stream(self, params, context=None):
    """Simulate on_message_send_stream that raises mid-stream."""
    yield SimpleNamespace(parts=[_text_part("ok")], status=None, id=None)
    raise RuntimeError("server error")


class TestWrapOnMessageSendStreamStreaming:
    @pytest.mark.asyncio
    async def test_yields_all_events(self):
        # Given: a wrapped streaming handler
        tracer, span = _make_tracer_and_span()
        wrapped = _wrap_on_message_send_stream(tracer, _fake_on_message_send_stream, agent_name="test")

        # When: consuming all events
        events = []
        async for event in wrapped(None, _server_params()):
            events.append(event)

        # Then: both events are yielded and span is ended
        assert len(events) == 2
        span.end.assert_called_once()

    @pytest.mark.asyncio
    async def test_span_ended_on_early_termination(self):
        # Given: a wrapped streaming handler
        tracer, span = _make_tracer_and_span()
        wrapped = _wrap_on_message_send_stream(tracer, _fake_on_message_send_stream, agent_name="test")

        # When: consuming one event then closing
        gen = wrapped(None, _server_params()).__aiter__()
        first = await gen.__anext__()
        await gen.aclose()

        # Then: span is still ended cleanly
        assert first is not None
        span.end.assert_called_once()

    @pytest.mark.asyncio
    async def test_no_context_detach_error_on_early_termination(self):
        # Given: a wrapped streaming handler using real OTel tracer
        from opentelemetry.sdk.trace import TracerProvider

        provider = TracerProvider()
        tracer = provider.get_tracer("test")
        wrapped = _wrap_on_message_send_stream(tracer, _fake_on_message_send_stream, agent_name="test")

        # When: consuming one event then closing — must not raise ValueError
        gen = wrapped(None, _server_params()).__aiter__()
        await gen.__anext__()
        await gen.aclose()  # must not raise

    @pytest.mark.asyncio
    async def test_span_is_current_during_inner_execution(self):
        # Given: a wrapped streaming handler with a real tracer
        from opentelemetry import trace as otel_trace
        from opentelemetry.sdk.trace import TracerProvider

        provider = TracerProvider()
        tracer = provider.get_tracer("test")

        captured_parents = []

        async def _capturing_stream(self, params, context=None):
            """Record the current span during inner agent execution."""
            current = otel_trace.get_current_span()
            captured_parents.append(current)
            yield SimpleNamespace(parts=[_text_part("ok")], status=None, id=None)

        wrapped = _wrap_on_message_send_stream(tracer, _capturing_stream, agent_name="test")

        # When: consuming events
        async for _ in wrapped(None, _server_params()):
            pass

        # Then: the inner execution saw our server span as the current span
        assert len(captured_parents) == 1
        parent = captured_parents[0]
        assert parent.get_span_context().is_valid
        assert parent.name == "a2a.server.on_message_send_stream"

    @pytest.mark.asyncio
    async def test_records_exception_on_error(self):
        # Given: a wrapped streaming handler that raises mid-stream
        tracer, span = _make_tracer_and_span()
        wrapped = _wrap_on_message_send_stream(tracer, _failing_stream, agent_name="test")

        # When: consuming events until the error
        events = []
        with pytest.raises(RuntimeError, match="server error"):  # noqa: PT012
            async for event in wrapped(None, _server_params()):
                events.append(event)

        # Then: exception is recorded on span and span is ended
        assert len(events) == 1
        span.record_exception.assert_called_once()
        span.set_status.assert_called_once_with(StatusCode.ERROR, "server error")
        span.end.assert_called_once()
