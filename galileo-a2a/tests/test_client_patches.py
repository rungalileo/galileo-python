"""Tests for client-side monkey-patching lifecycle and streaming wrappers."""

from types import SimpleNamespace
from unittest.mock import MagicMock, patch

import pytest
from opentelemetry.trace import Span, StatusCode, Tracer

from galileo_a2a._client_patches import _originals, _patch_client, _unpatch_client, _wrap_send_message


@patch("galileo_a2a._client_patches.BaseClient")
class TestPatchClient:
    def test_patches_all_methods(self, mock_base_client):
        # Given: a fresh state
        _originals.clear()
        tracer = MagicMock(spec=Tracer)

        # When: patching
        _patch_client(tracer, agent_name="test")

        # Then: all 4 methods stashed
        assert "BaseClient.send_message" in _originals
        assert "BaseClient.get_task" in _originals
        assert "BaseClient.cancel_task" in _originals
        assert "BaseClient.get_card" in _originals

        # Cleanup
        _originals.clear()

    def test_idempotent_second_call_is_noop(self, mock_base_client):
        # Given: already patched
        _originals.clear()
        tracer = MagicMock(spec=Tracer)
        _patch_client(tracer)

        original_send = mock_base_client.send_message

        # When: patching again
        _patch_client(tracer)

        # Then: send_message not re-wrapped
        assert mock_base_client.send_message == original_send

        # Cleanup
        _originals.clear()

    @patch("galileo_a2a._client_patches._wrap_simple_method")
    def test_rollback_on_failure(self, mock_wrap, mock_base_client):
        # Given: _wrap_simple_method raises on the third call (get_card)
        _originals.clear()
        tracer = MagicMock(spec=Tracer)
        mock_wrap.side_effect = [MagicMock(), MagicMock(), RuntimeError("boom")]

        # When: patching fails partway
        _patch_client(tracer)

        # Then: originals dict is empty (rolled back)
        assert len(_originals) == 0


@patch("galileo_a2a._client_patches.BaseClient")
class TestUnpatchClient:
    def test_restores_originals(self, mock_base_client):
        # Given: patched state
        _originals.clear()
        tracer = MagicMock(spec=Tracer)
        _patch_client(tracer)

        # When: unpatching
        _unpatch_client()

        # Then: originals dict is empty
        assert len(_originals) == 0

    def test_noop_when_not_patched(self, mock_base_client):
        # Given: clean state
        _originals.clear()

        # When: unpatching
        _unpatch_client()

        # Then: no error
        assert len(_originals) == 0


def _make_tracer_and_span():
    """Create a mock Tracer whose start_span returns a Span with a valid SpanContext."""
    from opentelemetry.trace import SpanContext, TraceFlags

    span = MagicMock(spec=Span)
    span.get_span_context.return_value = SpanContext(
        trace_id=0xAABB00112233445566778899AABBCCDD,
        span_id=0x1122334455667788,
        is_remote=False,
        trace_flags=TraceFlags(TraceFlags.SAMPLED),
    )
    tracer = MagicMock(spec=Tracer)
    tracer.start_span.return_value = span
    return tracer, span


def _text_part(text: str) -> SimpleNamespace:
    return SimpleNamespace(root=SimpleNamespace(text=text))


async def _fake_send_message(
    self, request, *, configuration=None, context=None, request_metadata=None, extensions=None
):
    """Simulate BaseClient.send_message yielding events."""
    for event in [SimpleNamespace(parts=[_text_part("hi")]), SimpleNamespace(parts=[_text_part("bye")])]:
        yield event


async def _failing_send_message(
    self, request, *, configuration=None, context=None, request_metadata=None, extensions=None
):
    """Simulate BaseClient.send_message that raises mid-stream."""
    yield SimpleNamespace(parts=[_text_part("first")])
    raise RuntimeError("stream broken")


class TestWrapSendMessageStreaming:
    @pytest.mark.asyncio
    async def test_yields_all_events(self):
        # Given: a wrapped send_message that yields two events
        tracer, span = _make_tracer_and_span()
        wrapped = _wrap_send_message(tracer, _fake_send_message, agent_name="test")

        # When: consuming all events
        events = []
        async for event in wrapped(None, SimpleNamespace(parts=[_text_part("hello")])):
            events.append(event)

        # Then: both events are yielded and span is ended
        assert len(events) == 2
        span.end.assert_called_once()

    @pytest.mark.asyncio
    async def test_span_ended_on_early_termination(self):
        # Given: a wrapped send_message
        tracer, span = _make_tracer_and_span()
        wrapped = _wrap_send_message(tracer, _fake_send_message, agent_name="test")

        # When: consuming only the first event then closing (simulating GeneratorExit)
        gen = wrapped(None, SimpleNamespace(parts=[_text_part("hello")])).__aiter__()
        first = await gen.__anext__()
        await gen.aclose()

        # Then: span is still ended cleanly
        assert first is not None
        span.end.assert_called_once()

    @pytest.mark.asyncio
    async def test_no_context_detach_error_on_early_termination(self):
        # Given: a wrapped send_message using real OTel tracer (not mock)
        from opentelemetry.sdk.trace import TracerProvider

        provider = TracerProvider()
        tracer = provider.get_tracer("test")
        wrapped = _wrap_send_message(tracer, _fake_send_message, agent_name="test")

        # When: consuming one event then closing — this previously raised
        # ValueError: <Token> was created in a different Context
        gen = wrapped(None, SimpleNamespace(parts=[_text_part("hello")])).__aiter__()
        await gen.__anext__()
        await gen.aclose()  # must not raise

    @pytest.mark.asyncio
    async def test_span_is_current_during_iteration(self):
        # Given: a wrapped send_message with a real tracer
        from opentelemetry import trace as otel_trace
        from opentelemetry.sdk.trace import TracerProvider

        provider = TracerProvider()
        tracer = provider.get_tracer("test")

        captured_parents = []

        async def _capturing_send_message(
            self,
            request,
            *,
            configuration=None,
            context=None,
            request_metadata=None,
            extensions=None,
        ):
            """Record the current span during inner execution."""
            current = otel_trace.get_current_span()
            captured_parents.append(current)
            yield SimpleNamespace(parts=[_text_part("ok")])

        wrapped = _wrap_send_message(tracer, _capturing_send_message, agent_name="test")

        # When: consuming events
        async for _ in wrapped(None, SimpleNamespace(parts=[_text_part("hello")])):
            pass

        # Then: the inner execution saw our client span as the current span
        assert len(captured_parents) == 1
        parent = captured_parents[0]
        assert parent.get_span_context().is_valid
        assert parent.name == "a2a.client.send_message"

    @pytest.mark.asyncio
    async def test_records_exception_on_error(self):
        # Given: a wrapped send_message that raises mid-stream
        tracer, span = _make_tracer_and_span()
        wrapped = _wrap_send_message(tracer, _failing_send_message, agent_name="test")

        # When: consuming events until the error
        events = []
        with pytest.raises(RuntimeError, match="stream broken"):  # noqa: PT012
            async for event in wrapped(None, SimpleNamespace(parts=[_text_part("hello")])):
                events.append(event)

        # Then: exception is recorded on span and span is ended
        assert len(events) == 1
        span.record_exception.assert_called_once()
        span.set_status.assert_called_once_with(StatusCode.ERROR, "stream broken")
        span.end.assert_called_once()
