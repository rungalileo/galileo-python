"""Tests for galileo.__future__.a2a - A2A tracing middleware and propagation."""

from __future__ import annotations

import json
from unittest.mock import AsyncMock, MagicMock, patch

import httpx
import pytest
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import SimpleSpanProcessor
from opentelemetry.sdk.trace.export.in_memory_span_exporter import InMemorySpanExporter

import galileo.__future__.a2a.asgi_middleware as _a2a_mw
from galileo.__future__.a2a.asgi_middleware import (
    A2ASpanMiddleware,
    _get_agent_text,
    _get_user_text,
    _parse_json,
    _set_tool_attrs,
    _wrap_receive,
    _wrap_send,
)
from galileo.__future__.a2a.propagation import inject_trace_context

# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture()
def _otel_provider():
    """Create an isolated TracerProvider that does not touch the global singleton.

    ``trace.set_tracer_provider()`` can only be called once per process; subsequent
    calls are silently ignored.  Using a local provider avoids conflicts when
    multiple test files run in the same CI worker.
    """
    exporter = InMemorySpanExporter()
    provider = TracerProvider()
    provider.add_span_processor(SimpleSpanProcessor(exporter))
    _a2a_mw._tracer = provider.get_tracer("galileo.a2a")
    yield provider, exporter
    exporter.shutdown()
    provider.shutdown()


@pytest.fixture()
def span_exporter(_otel_provider):
    """Convenience fixture that yields only the exporter."""
    _, exporter = _otel_provider
    return exporter


@pytest.fixture()
def otel_provider(_otel_provider):
    """Convenience fixture that yields only the provider."""
    provider, _ = _otel_provider
    return provider


@pytest.fixture()
def echo_app():
    """A minimal ASGI app that echoes back the request body as the response."""

    async def app(scope, receive, send):
        body = b""
        while True:
            msg = await receive()
            body += msg.get("body", b"")
            if not msg.get("more_body", False):
                break
        await send({"type": "http.response.start", "status": 200, "headers": []})
        await send({"type": "http.response.body", "body": body})

    return app


@pytest.fixture()
def make_scope():
    """Factory to create ASGI HTTP scopes."""

    def _make(path: str, method: str = "POST", headers: list[tuple[bytes, bytes]] | None = None):
        return {"type": "http", "path": path, "method": method, "headers": headers or []}

    return _make


def _make_receive(body: bytes):
    """Create a simple ASGI receive callable that yields a single body message."""

    async def receive():
        return {"type": "http.request", "body": body, "more_body": False}

    return receive


def _make_send():
    """Create an ASGI send callable that records all messages."""
    messages: list[dict] = []

    async def send(message: dict):
        messages.append(message)

    send.messages = messages  # type: ignore[attr-defined]
    return send


# ---------------------------------------------------------------------------
# Unit tests: JSON extraction helpers
# ---------------------------------------------------------------------------


class TestParseJson:
    def test_valid_json(self):
        # Given: valid JSON bytes
        data = b'{"key": "value"}'

        # When: parsing JSON
        result = _parse_json(data)

        # Then: the parsed dict is returned
        assert result == {"key": "value"}

    def test_invalid_json(self):
        # Given: invalid JSON bytes
        data = b"not json"

        # When: parsing JSON
        result = _parse_json(data)

        # Then: None is returned
        assert result is None

    def test_empty_bytes(self):
        # Given: empty bytes
        data = b""

        # When: parsing JSON
        result = _parse_json(data)

        # Then: None is returned
        assert result is None


class TestGetUserText:
    def test_extracts_text_from_parts(self):
        # Given: an A2A request with text parts
        data = {"params": {"message": {"parts": [{"text": "Hello"}, {"text": "world"}]}}}

        # When: extracting user text
        result = _get_user_text(data)

        # Then: texts are joined with spaces
        assert result == "Hello world"

    def test_extracts_text_from_root_key(self):
        # Given: an A2A request with text nested under root
        data = {"params": {"message": {"parts": [{"root": {"text": "nested text"}}]}}}

        # When: extracting user text
        result = _get_user_text(data)

        # Then: the nested text is extracted
        assert result == "nested text"

    def test_returns_none_for_no_text_parts(self):
        # Given: an A2A request with non-text parts
        data = {"params": {"message": {"parts": [{"data": "binary"}]}}}

        # When: extracting user text
        result = _get_user_text(data)

        # Then: None is returned
        assert result is None

    def test_returns_none_for_none_input(self):
        # When/Then: None input returns None
        assert _get_user_text(None) is None

    def test_returns_none_for_empty_dict(self):
        # When/Then: empty dict returns None
        assert _get_user_text({}) is None


class TestGetAgentText:
    def test_extracts_agent_response_text(self):
        # Given: an A2A response with agent message in history
        data = {"result": {"history": [{"role": "agent", "parts": [{"text": "I can help"}]}]}}

        # When: extracting agent text
        result = _get_agent_text(data)

        # Then: the agent text is returned
        assert result == "I can help"

    def test_extracts_from_root_key(self):
        # Given: agent text nested under root
        data = {"result": {"history": [{"role": "agent", "parts": [{"root": {"text": "nested agent"}}]}]}}

        # When: extracting agent text
        result = _get_agent_text(data)

        # Then: the nested text is extracted
        assert result == "nested agent"

    def test_skips_non_agent_roles(self):
        # Given: a response with only user messages
        data = {"result": {"history": [{"role": "user", "parts": [{"text": "user message"}]}]}}

        # When: extracting agent text
        result = _get_agent_text(data)

        # Then: None is returned since no agent role found
        assert result is None

    def test_returns_none_for_none_input(self):
        # When/Then: None input returns None
        assert _get_agent_text(None) is None

    def test_returns_none_for_empty_history(self):
        # Given: response with empty history
        data = {"result": {"history": []}}

        # When/Then: returns None
        assert _get_agent_text(data) is None

    def test_returns_last_agent_message(self):
        # Given: a response with multiple agent messages in history
        data = {
            "result": {
                "history": [
                    {"role": "agent", "parts": [{"text": "first reply"}]},
                    {"role": "user", "parts": [{"text": "follow-up question"}]},
                    {"role": "agent", "parts": [{"text": "final reply"}]},
                ]
            }
        }

        # When: extracting agent text
        result = _get_agent_text(data)

        # Then: the last agent message is returned
        assert result == "final reply"


# ---------------------------------------------------------------------------
# Unit tests: ASGI wrappers
# ---------------------------------------------------------------------------


class TestWrapReceive:
    @pytest.mark.asyncio
    async def test_captures_request_body(self):
        # Given: a receive callable that returns a request body
        original_receive = _make_receive(b'{"hello": "world"}')
        get_body, wrapped = _wrap_receive(original_receive)

        # When: calling the wrapped receive
        message = await wrapped()

        # Then: the body is captured and the message is passed through
        assert message["type"] == "http.request"
        assert get_body() == b'{"hello": "world"}'

    @pytest.mark.asyncio
    async def test_non_request_messages_pass_through(self):
        # Given: a receive that returns a non-request message
        async def receive():
            return {"type": "http.disconnect"}

        get_body, wrapped = _wrap_receive(receive)

        # When: calling the wrapped receive
        await wrapped()

        # Then: body remains empty since it wasn't a request message
        assert get_body() == b""


class TestWrapSend:
    @pytest.mark.asyncio
    async def test_captures_response_body_and_status(self):
        # Given: a no-op send callable
        original_send = AsyncMock()
        get_body, get_status, wrapped = _wrap_send(original_send)

        # When: sending response start and body
        await wrapped({"type": "http.response.start", "status": 201})
        await wrapped({"type": "http.response.body", "body": b'{"ok": true}'})

        # Then: status and body are captured
        assert get_status() == 201
        assert get_body() == b'{"ok": true}'
        assert original_send.call_count == 2

    @pytest.mark.asyncio
    async def test_default_status_is_200(self):
        # Given: a no-op send callable
        original_send = AsyncMock()
        _, get_status, _ = _wrap_send(original_send)

        # When/Then: default status is 200 before any messages
        assert get_status() == 200

    @pytest.mark.asyncio
    async def test_captures_multi_part_body(self):
        # Given: a no-op send callable
        original_send = AsyncMock()
        get_body, _, wrapped = _wrap_send(original_send)

        # When: sending multiple body chunks
        await wrapped({"type": "http.response.body", "body": b"chunk1"})
        await wrapped({"type": "http.response.body", "body": b"chunk2"})

        # Then: all chunks are concatenated
        assert get_body() == b"chunk1chunk2"


# ---------------------------------------------------------------------------
# Unit tests: _set_tool_attrs
# ---------------------------------------------------------------------------


class TestSetToolAttrs:
    def test_sets_all_tool_attributes(self):
        # Given: a mock span
        span = MagicMock()

        # When: setting tool attributes with a status code
        _set_tool_attrs(span, "fetch_agent_card", 200)

        # Then: all gen_ai.tool attributes are set
        span.set_attribute.assert_any_call("gen_ai.operation.name", "execute_tool")
        span.set_attribute.assert_any_call("gen_ai.tool.name", "fetch_agent_card")
        span.set_attribute.assert_any_call("gen_ai.tool.type", "function")
        span.set_attribute.assert_any_call("http.response.status_code", 200)

    def test_skips_status_code_when_none(self):
        # Given: a mock span
        span = MagicMock()

        # When: setting tool attributes without a status code
        _set_tool_attrs(span, "get_task", None)

        # Then: http.response.status_code is not set
        calls = [c for c in span.set_attribute.call_args_list if c[0][0] == "http.response.status_code"]
        assert len(calls) == 0


# ---------------------------------------------------------------------------
# Integration tests: A2ASpanMiddleware
# ---------------------------------------------------------------------------


class TestA2ASpanMiddlewareInit:
    def test_raises_import_error_when_otel_unavailable(self):
        # Given: OpenTelemetry is not available
        with patch("galileo.__future__.a2a.asgi_middleware._OTEL_AVAILABLE", False):
            # When/Then: creating the middleware raises ImportError
            with pytest.raises(ImportError, match="OpenTelemetry packages are required"):
                A2ASpanMiddleware(app=AsyncMock())


class TestA2ASpanMiddlewareNonHttp:
    @pytest.mark.asyncio
    async def test_passes_through_non_http_scopes(self):
        # Given: a middleware wrapping a no-op app and a websocket scope
        inner_app = AsyncMock()
        middleware = A2ASpanMiddleware(inner_app)
        scope = {"type": "websocket", "path": "/ws"}
        receive = AsyncMock()
        send = AsyncMock()

        # When: calling with a non-http scope
        await middleware(scope, receive, send)

        # Then: the underlying app is called directly (no tracing)
        inner_app.assert_awaited_once_with(scope, receive, send)


class TestA2ASpanMiddlewareUnmatchedPath:
    @pytest.mark.asyncio
    async def test_passes_through_unmatched_paths(self, echo_app, make_scope, span_exporter):
        # Given: a middleware and a request to a non-A2A path
        middleware = A2ASpanMiddleware(echo_app)
        scope = make_scope("/health")
        receive = _make_receive(b"")
        send = _make_send()

        # When: calling with a non-A2A path
        await middleware(scope, receive, send)

        # Then: the app is called but no A2A spans are created
        spans = span_exporter.get_finished_spans()
        assert len(spans) == 0


class TestA2ASpanMiddlewareAgentCard:
    @pytest.mark.asyncio
    async def test_traces_agent_card_fetch(self, make_scope, span_exporter):
        # Given: an app that returns an agent card JSON
        agent_card = {"name": "TestAgent", "description": "A test agent", "url": "http://localhost"}

        async def card_app(scope, receive, send):
            await send({"type": "http.response.start", "status": 200, "headers": []})
            await send({"type": "http.response.body", "body": json.dumps(agent_card).encode()})

        middleware = A2ASpanMiddleware(card_app)
        scope = make_scope("/.well-known/agent-card.json", method="GET")
        receive = _make_receive(b"")
        send = _make_send()

        # When: fetching the agent card
        await middleware(scope, receive, send)

        # Then: a span is created with agent card attributes
        spans = span_exporter.get_finished_spans()
        assert len(spans) == 1
        span = spans[0]
        assert span.name == "A2A fetch_agent_card"
        attrs = dict(span.attributes)
        assert attrs["gen_ai.operation.name"] == "execute_tool"
        assert attrs["gen_ai.tool.name"] == "fetch_agent_card"
        assert attrs["a2a.agent.name"] == "TestAgent"
        assert attrs["a2a.agent.description"] == "A test agent"
        assert "gen_ai.tool.call.result" in attrs
        assert "gen_ai.output.messages" in attrs

    @pytest.mark.asyncio
    async def test_handles_non_json_agent_card_response(self, make_scope, span_exporter):
        # Given: an app that returns non-JSON for the agent card
        async def bad_card_app(scope, receive, send):
            await send({"type": "http.response.start", "status": 500, "headers": []})
            await send({"type": "http.response.body", "body": b"Internal Error"})

        middleware = A2ASpanMiddleware(bad_card_app)
        scope = make_scope("/.well-known/agent-card.json", method="GET")
        receive = _make_receive(b"")
        send = _make_send()

        # When: fetching returns non-JSON
        await middleware(scope, receive, send)

        # Then: a span is still created, just without card-specific attributes
        spans = span_exporter.get_finished_spans()
        assert len(spans) == 1
        attrs = dict(spans[0].attributes)
        assert attrs["gen_ai.tool.name"] == "fetch_agent_card"
        assert "a2a.agent.name" not in attrs


class TestA2ASpanMiddlewareMessage:
    @pytest.mark.asyncio
    async def test_traces_message_send(self, make_scope, span_exporter):
        # Given: an A2A message:send request and response
        request_body = {
            "jsonrpc": "2.0",
            "method": "message/send",
            "params": {"message": {"parts": [{"text": "What is 2+2?"}]}},
        }
        response_body = {
            "jsonrpc": "2.0",
            "result": {
                "id": "task-123",
                "status": {"state": "completed"},
                "history": [{"role": "agent", "parts": [{"text": "4"}]}],
            },
        }

        async def message_app(scope, receive, send):
            # consume the request body
            await receive()
            await send({"type": "http.response.start", "status": 200, "headers": []})
            await send({"type": "http.response.body", "body": json.dumps(response_body).encode()})

        middleware = A2ASpanMiddleware(message_app)
        scope = make_scope("/message:send")
        receive = _make_receive(json.dumps(request_body).encode())
        send = _make_send()

        # When: sending a message
        await middleware(scope, receive, send)

        # Then: a span is created with input/output message attributes
        spans = span_exporter.get_finished_spans()
        assert len(spans) == 1
        span = spans[0]
        assert span.name == "A2A message"
        attrs = dict(span.attributes)
        assert attrs["http.request.method"] == "POST"
        assert attrs["http.response.status_code"] == 200
        assert attrs["a2a.rpc.method"] == "message/send"
        assert attrs["a2a.task.state"] == "completed"
        assert attrs["a2a.task.id"] == "task-123"

        input_msgs = json.loads(attrs["gen_ai.input.messages"])
        assert input_msgs[0]["role"] == "user"
        assert input_msgs[0]["content"] == "What is 2+2?"

        output_msgs = json.loads(attrs["gen_ai.output.messages"])
        assert output_msgs[0]["role"] == "assistant"
        assert output_msgs[0]["content"] == "4"

    @pytest.mark.asyncio
    async def test_traces_message_stream(self, make_scope, span_exporter):
        # Given: an A2A message:stream request
        request_body = {
            "jsonrpc": "2.0",
            "method": "message/stream",
            "params": {"message": {"parts": [{"text": "Stream this"}]}},
        }

        async def stream_app(scope, receive, send):
            await receive()
            await send({"type": "http.response.start", "status": 200, "headers": []})
            await send({"type": "http.response.body", "body": b"{}"})

        middleware = A2ASpanMiddleware(stream_app)
        scope = make_scope("/message:stream")
        receive = _make_receive(json.dumps(request_body).encode())
        send = _make_send()

        # When: streaming a message
        await middleware(scope, receive, send)

        # Then: a span is created for the stream endpoint
        spans = span_exporter.get_finished_spans()
        assert len(spans) == 1
        assert spans[0].name == "A2A message"


class TestA2ASpanMiddlewareTask:
    @pytest.mark.asyncio
    async def test_traces_task_get(self, make_scope, span_exporter):
        # Given: a tasks:get request
        request_body = {"jsonrpc": "2.0", "method": "tasks/get", "params": {"id": "task-abc"}}
        response_body = {
            "jsonrpc": "2.0",
            "result": {"id": "task-abc", "status": {"state": "completed"}, "artifacts": []},
        }

        async def task_app(scope, receive, send):
            await receive()
            await send({"type": "http.response.start", "status": 200, "headers": []})
            await send({"type": "http.response.body", "body": json.dumps(response_body).encode()})

        middleware = A2ASpanMiddleware(task_app)
        scope = make_scope("/tasks:get")
        receive = _make_receive(json.dumps(request_body).encode())
        send = _make_send()

        # When: getting a task
        await middleware(scope, receive, send)

        # Then: a span is created with task tool attributes
        spans = span_exporter.get_finished_spans()
        assert len(spans) == 1
        span = spans[0]
        assert span.name == "A2A get_task"
        attrs = dict(span.attributes)
        assert attrs["gen_ai.tool.name"] == "get_task"
        assert attrs["a2a.task.id"] == "task-abc"
        assert attrs["a2a.task.state"] == "completed"
        assert "gen_ai.tool.call.arguments" in attrs
        assert "gen_ai.tool.call.result" in attrs

    @pytest.mark.asyncio
    async def test_traces_task_cancel(self, make_scope, span_exporter):
        # Given: a tasks:cancel request
        request_body = {"jsonrpc": "2.0", "method": "tasks/cancel", "params": {"id": "task-xyz"}}

        async def cancel_app(scope, receive, send):
            await receive()
            await send({"type": "http.response.start", "status": 200, "headers": []})
            await send({"type": "http.response.body", "body": b'{"result": {}}'})

        middleware = A2ASpanMiddleware(cancel_app)
        scope = make_scope("/tasks:cancel")
        receive = _make_receive(json.dumps(request_body).encode())
        send = _make_send()

        # When: cancelling a task
        await middleware(scope, receive, send)

        # Then: the span uses cancel_task as tool name
        spans = span_exporter.get_finished_spans()
        assert len(spans) == 1
        assert spans[0].name == "A2A cancel_task"
        assert dict(spans[0].attributes)["gen_ai.tool.name"] == "cancel_task"

    @pytest.mark.asyncio
    async def test_sets_error_type_on_failure(self, make_scope, span_exporter):
        # Given: a tasks:get request that returns 500
        request_body = {"jsonrpc": "2.0", "method": "tasks/get", "params": {"id": "task-fail"}}

        async def error_app(scope, receive, send):
            await receive()
            await send({"type": "http.response.start", "status": 500, "headers": []})
            await send({"type": "http.response.body", "body": b"server error"})

        middleware = A2ASpanMiddleware(error_app)
        scope = make_scope("/tasks:get")
        receive = _make_receive(json.dumps(request_body).encode())
        send = _make_send()

        # When: the task endpoint returns an error
        await middleware(scope, receive, send)

        # Then: error.type is set on the span
        spans = span_exporter.get_finished_spans()
        assert len(spans) == 1
        attrs = dict(spans[0].attributes)
        assert attrs["error.type"] == "500"
        assert attrs["http.response.status_code"] == 500

    @pytest.mark.asyncio
    async def test_sets_error_type_on_json_error_response(self, make_scope, span_exporter):
        # Given: a tasks:get request that returns 500 with a JSON error body
        request_body = {"jsonrpc": "2.0", "method": "tasks/get", "params": {"id": "task-fail"}}
        error_response = {"jsonrpc": "2.0", "error": {"code": -32000, "message": "Internal error"}}

        async def error_app(scope, receive, send):
            await receive()
            await send({"type": "http.response.start", "status": 500, "headers": []})
            await send({"type": "http.response.body", "body": json.dumps(error_response).encode()})

        middleware = A2ASpanMiddleware(error_app)
        scope = make_scope("/tasks:get")
        receive = _make_receive(json.dumps(request_body).encode())
        send = _make_send()

        # When: the task endpoint returns a JSON error response
        await middleware(scope, receive, send)

        # Then: error.type is set even though response body is valid JSON
        spans = span_exporter.get_finished_spans()
        assert len(spans) == 1
        attrs = dict(spans[0].attributes)
        assert attrs["error.type"] == "500"
        assert attrs["http.response.status_code"] == 500

    @pytest.mark.asyncio
    async def test_traces_task_subscribe(self, make_scope, span_exporter):
        # Given: a tasks:subscribe request (not get or cancel)
        request_body = {"jsonrpc": "2.0", "method": "tasks/subscribe", "params": {"id": "task-sub"}}

        async def subscribe_app(scope, receive, send):
            await receive()
            await send({"type": "http.response.start", "status": 200, "headers": []})
            await send({"type": "http.response.body", "body": b'{"result": {}}'})

        middleware = A2ASpanMiddleware(subscribe_app)
        scope = make_scope("/tasks:subscribe")
        receive = _make_receive(json.dumps(request_body).encode())
        send = _make_send()

        # When: subscribing to a task
        await middleware(scope, receive, send)

        # Then: the span uses subscribe_task as tool name (not cancel_task)
        spans = span_exporter.get_finished_spans()
        assert len(spans) == 1
        assert spans[0].name == "A2A subscribe_task"
        assert dict(spans[0].attributes)["gen_ai.tool.name"] == "subscribe_task"


# ---------------------------------------------------------------------------
# Tests: trace context propagation
# ---------------------------------------------------------------------------


class TestA2ASpanMiddlewareContextPropagation:
    @pytest.mark.asyncio
    async def test_extracts_traceparent_from_headers(self, make_scope, span_exporter):
        # Given: a request with a traceparent header
        trace_id = "0af7651916cd43dd8448eb211c80319c"
        parent_span_id = "b7ad6b7169203331"
        traceparent = f"00-{trace_id}-{parent_span_id}-01"
        scope = make_scope(
            "/.well-known/agent-card.json", method="GET", headers=[(b"traceparent", traceparent.encode())]
        )

        async def card_app(scope, receive, send):
            await send({"type": "http.response.start", "status": 200, "headers": []})
            await send({"type": "http.response.body", "body": b'{"name": "Agent"}'})

        middleware = A2ASpanMiddleware(card_app)
        receive = _make_receive(b"")
        send = _make_send()

        # When: the middleware processes the request
        await middleware(scope, receive, send)

        # Then: the span has the parent trace context
        spans = span_exporter.get_finished_spans()
        assert len(spans) == 1
        span = spans[0]
        assert span.context.trace_id == int(trace_id, 16)
        assert span.parent.span_id == int(parent_span_id, 16)


class TestInjectTraceContext:
    @pytest.mark.asyncio
    async def test_injects_traceparent_header(self, otel_provider):
        # Given: an active span from the local provider and an httpx request
        tracer = otel_provider.get_tracer("test")
        with tracer.start_as_current_span("test-parent"):
            request = httpx.Request("POST", "http://example.com/message:send")

            # When: injecting trace context
            await inject_trace_context(request)

            # Then: traceparent header is added
            assert "traceparent" in request.headers

    @pytest.mark.asyncio
    async def test_warns_when_otel_unavailable(self):
        # Given: OpenTelemetry is not importable
        with patch("galileo.__future__.a2a.propagation.inject_trace_context", new=inject_trace_context):
            with patch.dict("sys.modules", {"opentelemetry.propagate": None}):
                # Re-import to trigger the ImportError path
                # Since the import is inside the function, we patch builtins
                original_import = __builtins__.__import__ if hasattr(__builtins__, "__import__") else __import__

                def mock_import(name, *args, **kwargs):
                    if name == "opentelemetry.propagate":
                        raise ImportError("mocked")
                    return original_import(name, *args, **kwargs)

                request = httpx.Request("POST", "http://example.com/message:send")
                with patch("builtins.__import__", side_effect=mock_import):
                    # When: calling inject without otel available
                    await inject_trace_context(request)

                # Then: no traceparent header is set (graceful degradation)
                assert "traceparent" not in request.headers


# ---------------------------------------------------------------------------
# Tests: public API (__init__.py exports)
# ---------------------------------------------------------------------------


class TestPublicAPI:
    def test_exports_middleware(self):
        # When/Then: A2ASpanMiddleware is importable from the package
        from galileo.__future__.a2a import A2ASpanMiddleware as Middleware

        assert Middleware is not None

    def test_exports_inject_trace_context(self):
        # When/Then: inject_trace_context is importable from the package
        from galileo.__future__.a2a import inject_trace_context as inject

        assert inject is not None
