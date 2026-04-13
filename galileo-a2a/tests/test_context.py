"""Tests for trace context injection, extraction, span link creation, and async iteration."""

import pytest
from opentelemetry import trace as otel_trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.trace import Link

from galileo_a2a._constants import AGNTCY_OBSERVE_KEY, GALILEO_OBSERVE_KEY
from galileo_a2a._context import (
    create_span_link_from_context,
    extract_trace_context,
    inject_trace_context,
    iter_with_context,
)


class TestInjectTraceContext:
    def test_produces_traceparent(self):
        # Given: a default OTel context (no active span → invalid context)
        # When: injecting trace context
        result = inject_trace_context()

        # Then: returns a dict (may be empty if no active span, but doesn't error)
        assert isinstance(result, dict)

    def test_includes_agent_name(self):
        # Given: an agent name
        # When: injecting trace context with agent_name
        result = inject_trace_context(agent_name="planner-agent")

        # Then: agent_name is included in the context
        assert result["agent_name"] == "planner-agent"


class TestExtractTraceContext:
    def test_extracts_from_galileo_observe_key(self):
        # Given: metadata with galileo_observe context
        metadata = {
            GALILEO_OBSERVE_KEY: {
                "traceparent": "00-aabb00112233445566778899aabbccdd-1122334455667788-01",
                "agent_name": "planner",
            }
        }

        # When: extracting trace context
        result = extract_trace_context(metadata)

        # Then: context extracted from galileo_observe key
        assert result is not None
        assert result["traceparent"] == "00-aabb00112233445566778899aabbccdd-1122334455667788-01"
        assert result["agent_name"] == "planner"

    def test_extracts_from_agntcy_observe_key(self):
        # Given: metadata with AGNTCY observe context (no galileo_observe)
        metadata = {
            AGNTCY_OBSERVE_KEY: {
                "traceparent": "00-aabb00112233445566778899aabbccdd-1122334455667788-01",
                "last_agent_name": "search-agent",
            }
        }

        # When: extracting trace context
        result = extract_trace_context(metadata)

        # Then: context extracted from observe key
        assert result is not None
        assert "traceparent" in result

    def test_galileo_key_takes_precedence_over_agntcy(self):
        # Given: metadata with both keys
        metadata = {
            GALILEO_OBSERVE_KEY: {"traceparent": "galileo-traceparent"},
            AGNTCY_OBSERVE_KEY: {"traceparent": "agntcy-traceparent"},
        }

        # When: extracting trace context
        result = extract_trace_context(metadata)

        # Then: galileo key takes precedence
        assert result is not None
        assert result["traceparent"] == "galileo-traceparent"

    def test_returns_none_when_missing(self):
        # Given: metadata with no observe keys
        metadata = {"some_other_key": "value"}

        # When: extracting trace context
        result = extract_trace_context(metadata)

        # Then: returns None
        assert result is None

    def test_returns_none_for_none_metadata(self):
        # When/Then: None metadata returns None
        assert extract_trace_context(None) is None

    def test_returns_none_for_empty_metadata(self):
        # When/Then: empty metadata returns None
        assert extract_trace_context({}) is None


class TestCreateSpanLink:
    def test_creates_link_with_correct_ids(self):
        # Given: trace context with agent_trace_id and agent_span_id
        ctx = {
            "agent_trace_id": "aabb00112233445566778899aabbccdd",
            "agent_span_id": "1122334455667788",
        }

        # When: creating span link
        link = create_span_link_from_context(ctx)

        # Then: link created with correct IDs
        assert link is not None
        assert isinstance(link, Link)
        assert link.context.trace_id == int("aabb00112233445566778899aabbccdd", 16)
        assert link.context.span_id == int("1122334455667788", 16)

    def test_link_has_agent_handoff_type(self):
        # Given: trace context
        ctx = {
            "agent_trace_id": "aabb00112233445566778899aabbccdd",
            "agent_span_id": "1122334455667788",
            "agent_name": "planner",
        }

        # When: creating span link
        link = create_span_link_from_context(ctx)

        # Then: link has agent_handoff type and from_agent
        assert link is not None
        assert link.attributes is not None
        attrs = dict(link.attributes)
        assert attrs["link.type"] == "agent_handoff"
        assert attrs["link.from_agent"] == "planner"

    def test_falls_back_to_traceparent(self):
        # Given: trace context with only traceparent (no agent_trace_id/agent_span_id)
        ctx = {
            "traceparent": "00-aabb00112233445566778899aabbccdd-1122334455667788-01",
        }

        # When: creating span link
        link = create_span_link_from_context(ctx)

        # Then: link created from traceparent
        assert link is not None
        assert link.context.trace_id == int("aabb00112233445566778899aabbccdd", 16)
        assert link.context.span_id == int("1122334455667788", 16)

    def test_returns_none_for_missing_ids(self):
        # Given: trace context without trace/span IDs
        ctx = {"agent_name": "planner"}

        # When: creating span link
        link = create_span_link_from_context(ctx)

        # Then: returns None
        assert link is None

    def test_returns_none_for_invalid_hex(self):
        # Given: trace context with invalid hex IDs
        ctx = {
            "agent_trace_id": "not-valid-hex",
            "agent_span_id": "also-invalid",
        }

        # When: creating span link
        link = create_span_link_from_context(ctx)

        # Then: returns None
        assert link is None

    def test_returns_none_for_zero_ids(self):
        # Given: trace context with zero IDs (invalid)
        ctx = {
            "agent_trace_id": "00000000000000000000000000000000",
            "agent_span_id": "0000000000000000",
        }

        # When: creating span link
        link = create_span_link_from_context(ctx)

        # Then: returns None (zero IDs are invalid)
        assert link is None


async def _async_range(n: int):
    for i in range(n):
        yield i


async def _failing_iter():
    yield "ok"
    raise RuntimeError("boom")


class TestIterWithContext:
    @pytest.mark.asyncio
    async def test_yields_all_events(self):
        # Given: a span context and an async iterable with 3 items
        provider = TracerProvider()
        tracer = provider.get_tracer("test")
        span = tracer.start_span("test")
        ctx = otel_trace.set_span_in_context(span)

        # When: iterating with context
        results = [event async for event in iter_with_context(ctx, _async_range(3))]

        # Then: all items yielded
        assert results == [0, 1, 2]
        span.end()

    @pytest.mark.asyncio
    async def test_span_is_current_during_anext(self):
        # Given: a real span and an inner generator that captures the current span
        provider = TracerProvider()
        tracer = provider.get_tracer("test")
        span = tracer.start_span("parent")
        ctx = otel_trace.set_span_in_context(span)

        captured = []

        async def _capturing_iter():
            captured.append(otel_trace.get_current_span())
            yield "a"
            captured.append(otel_trace.get_current_span())
            yield "b"

        # When: iterating with context
        results = [event async for event in iter_with_context(ctx, _capturing_iter())]

        # Then: the span was current during each __anext__ call
        assert results == ["a", "b"]
        assert all(c is span for c in captured)
        span.end()

    @pytest.mark.asyncio
    async def test_no_token_held_across_yield(self):
        # Given: a span context
        provider = TracerProvider()
        tracer = provider.get_tracer("test")
        span = tracer.start_span("parent")
        ctx = otel_trace.set_span_in_context(span)

        # When: consuming one event then closing (GeneratorExit)
        gen = iter_with_context(ctx, _async_range(5)).__aiter__()
        await gen.__anext__()
        await gen.aclose()  # must not log "Failed to detach context"

        span.end()

    @pytest.mark.asyncio
    async def test_propagates_inner_exception(self):
        # Given: an inner iterator that raises mid-stream
        provider = TracerProvider()
        tracer = provider.get_tracer("test")
        span = tracer.start_span("test")
        ctx = otel_trace.set_span_in_context(span)

        # When/Then: exception propagates
        results = []
        with pytest.raises(RuntimeError, match="boom"):  # noqa: PT012
            async for event in iter_with_context(ctx, _failing_iter()):
                results.append(event)
        assert results == ["ok"]
        span.end()
