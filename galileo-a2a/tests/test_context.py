"""Tests for trace context injection, extraction, and span link creation."""

from opentelemetry.trace import Link

from galileo_a2a._constants import AGNTCY_OBSERVE_KEY, GALILEO_OBSERVE_KEY
from galileo_a2a._context import create_span_link_from_context, extract_trace_context, inject_trace_context


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
