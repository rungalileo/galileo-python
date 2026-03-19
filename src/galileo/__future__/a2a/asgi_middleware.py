"""ASGI middleware for tracing A2A protocol endpoints with OpenTelemetry.

Creates spans with gen_ai semantic convention attributes
(``gen_ai.input.messages``, ``gen_ai.output.messages``, ``gen_ai.tool.*``)
compatible with Galileo's trace viewer.

The middleware handles three types of A2A endpoints:

- **Agent card** (``/.well-known/agent-card.json``): traced as ``execute_tool`` spans
- **Message send/stream** (``/message:send``, ``/message:stream``): traced with
  ``gen_ai.input.messages`` / ``gen_ai.output.messages``
- **Task operations** (``/tasks:get``, ``/tasks:cancel``): traced as ``execute_tool`` spans
"""

from __future__ import annotations

import json
import logging
from typing import Any, Callable

logger = logging.getLogger(__name__)

_OTEL_ERR_MSG = (
    "OpenTelemetry packages are required for A2A tracing middleware. Install with: pip install galileo[otel]"
)

try:
    from opentelemetry import context, trace
    from opentelemetry.propagate import extract

    _tracer = trace.get_tracer("galileo.a2a")
    _OTEL_AVAILABLE = True
except ImportError:
    _OTEL_AVAILABLE = False
    _tracer = None


class A2ASpanMiddleware:
    """ASGI middleware that creates OpenTelemetry spans for A2A endpoints.

    This middleware intercepts A2A JSON-RPC requests and responses, creating
    enriched spans with gen_ai semantic convention attributes that Galileo
    reads natively.

    It replaces ``FastAPIInstrumentor`` for A2A endpoints — creating its own
    spans gives full control over the lifecycle and allows setting attributes
    before the span ends.

    Parameters
    ----------
    app : ASGI application
        The ASGI application to wrap.

    Examples
    --------
    With FastAPI/Starlette::

        from galileo.__future__.a2a import A2ASpanMiddleware

        app = FastAPI()
        app.add_middleware(A2ASpanMiddleware)

    With Agno AgentOS::

        from agno.os import AgentOS
        from galileo.__future__.a2a import A2ASpanMiddleware

        agent_os = AgentOS(agents=[agent], a2a_interface=True)
        app = agent_os.get_app()
        app.add_middleware(A2ASpanMiddleware)
    """

    def __init__(self, app: Any) -> None:
        if not _OTEL_AVAILABLE:
            raise ImportError(_OTEL_ERR_MSG)
        self.app = app

    async def __call__(self, scope: dict, receive: Callable, send: Callable) -> None:
        if scope["type"] != "http":
            return await self.app(scope, receive, send)

        path: str = scope.get("path", "")
        method: str = scope.get("method", "")
        ctx = _extract_context(scope)

        if ".well-known/agent-card.json" in path:
            return await self._handle_agent_card(scope, receive, send, path, ctx)
        if "message:" in path:
            return await self._handle_message(scope, receive, send, method, path, ctx)
        if "tasks:" in path:
            return await self._handle_task(scope, receive, send, method, path, ctx)

        return await self.app(scope, receive, send)

    async def _handle_agent_card(self, scope: dict, receive: Callable, send: Callable, path: str, ctx: Any) -> None:
        response_body, status_code, send_wrapper = _wrap_send(send)

        with _tracer.start_as_current_span("A2A fetch_agent_card", context=ctx, kind=trace.SpanKind.SERVER) as span:
            await self.app(scope, receive, send_wrapper)

            _set_tool_attrs(span, "fetch_agent_card", status_code())
            span.set_attribute("gen_ai.tool.call.arguments", json.dumps({"url": path}))
            span.set_attribute(
                "gen_ai.input.messages", json.dumps([{"role": "tool", "content": json.dumps({"url": path})}])
            )

            card = _parse_json(response_body())
            if card:
                if name := card.get("name"):
                    span.set_attribute("a2a.agent.name", name)
                if desc := card.get("description"):
                    span.set_attribute("a2a.agent.description", desc)
                card_str = json.dumps(card)
                span.set_attribute("gen_ai.tool.call.result", card_str)
                span.set_attribute("gen_ai.output.messages", json.dumps([{"role": "tool", "content": card_str}]))

    async def _handle_message(
        self, scope: dict, receive: Callable, send: Callable, method: str, path: str, ctx: Any
    ) -> None:
        request_body, receive_wrapper = _wrap_receive(receive)
        response_body, status_code, send_wrapper = _wrap_send(send)

        with _tracer.start_as_current_span("A2A message", context=ctx, kind=trace.SpanKind.SERVER) as span:
            span.set_attribute("http.method", method)
            span.set_attribute("http.target", path)

            token = context.attach(trace.set_span_in_context(span))
            try:
                await self.app(scope, receive_wrapper, send_wrapper)
            finally:
                context.detach(token)

            span.set_attribute("http.status_code", status_code())

            req = _parse_json(request_body())
            resp = _parse_json(response_body())

            if input_text := _get_user_text(req):
                span.set_attribute("gen_ai.input.messages", json.dumps([{"role": "user", "content": input_text}]))
            if output_text := _get_agent_text(resp):
                span.set_attribute(
                    "gen_ai.output.messages", json.dumps([{"role": "assistant", "content": output_text}])
                )
            if req and (rpc_method := req.get("method")):
                span.set_attribute("a2a.rpc.method", rpc_method)
            if resp:
                result = resp.get("result", {})
                if state := result.get("status", {}).get("state"):
                    span.set_attribute("a2a.task.state", state)
                if task_id := result.get("id"):
                    span.set_attribute("a2a.task.id", task_id)

    async def _handle_task(
        self, scope: dict, receive: Callable, send: Callable, method: str, path: str, ctx: Any
    ) -> None:
        request_body, receive_wrapper = _wrap_receive(receive)
        response_body, status_code, send_wrapper = _wrap_send(send)

        tool_name = _derive_task_tool_name(path)

        with _tracer.start_as_current_span(f"A2A {tool_name}", context=ctx, kind=trace.SpanKind.SERVER) as span:
            _set_tool_attrs(span, tool_name, None)
            span.set_attribute("http.method", method)

            token = context.attach(trace.set_span_in_context(span))
            try:
                await self.app(scope, receive_wrapper, send_wrapper)
            finally:
                context.detach(token)

            span.set_attribute("http.status_code", status_code())

            req = _parse_json(request_body())
            if req:
                task_id = req.get("params", {}).get("id")
                if task_id:
                    span.set_attribute("a2a.task.id", task_id)
                    args = json.dumps({"task_id": task_id})
                    span.set_attribute("gen_ai.tool.call.arguments", args)
                    span.set_attribute("gen_ai.input.messages", json.dumps([{"role": "tool", "content": args}]))

            resp = _parse_json(response_body())
            if resp:
                result = resp.get("result", {})
                result_str = json.dumps(result)
                span.set_attribute("gen_ai.tool.call.result", result_str)
                span.set_attribute("gen_ai.output.messages", json.dumps([{"role": "tool", "content": result_str}]))
                if state := result.get("status", {}).get("state"):
                    span.set_attribute("a2a.task.state", state)
            if status_code() >= 400:
                span.set_attribute("error.type", str(status_code()))


# ---------------------------------------------------------------------------
# ASGI wrappers
# ---------------------------------------------------------------------------


def _wrap_receive(receive: Callable) -> tuple[Callable[[], bytes], Callable]:
    """Wrap ASGI ``receive`` to capture request body while passing it through."""
    body_parts: list[bytes] = []

    async def wrapper() -> dict:
        message = await receive()
        if message["type"] == "http.request":
            body_parts.append(message.get("body", b""))
        return message

    return lambda: b"".join(body_parts), wrapper


def _wrap_send(send: Callable) -> tuple[Callable[[], bytes], Callable[[], int], Callable]:
    """Wrap ASGI ``send`` to capture response body and status code."""
    body_parts: list[bytes] = []
    code: list[int] = [200]

    async def wrapper(message: dict) -> None:
        if message["type"] == "http.response.start":
            code[0] = message.get("status", 200)
        elif message["type"] == "http.response.body":
            body_parts.append(message.get("body", b""))
        return await send(message)

    return lambda: b"".join(body_parts), lambda: code[0], wrapper


def _extract_context(scope: dict) -> Any:
    """Extract W3C trace context from ASGI scope headers."""
    headers = dict(scope.get("headers", []))
    carrier = {k.decode("utf-8"): v.decode("utf-8") for k, v in headers.items()}
    return extract(carrier)


# ---------------------------------------------------------------------------
# Span helpers
# ---------------------------------------------------------------------------


def _derive_task_tool_name(path: str) -> str:
    """Derive tool name from A2A task path (e.g. ``/tasks:get`` → ``get_task``)."""
    for segment in path.split("/"):
        if segment.startswith("tasks:"):
            operation = segment.split(":", 1)[1]
            return f"{operation}_task"
    return "task_operation"


def _set_tool_attrs(span: Any, tool_name: str, status_code: int | None) -> None:
    """Set ``gen_ai.tool.*`` semantic convention attributes on a span."""
    span.set_attribute("gen_ai.operation.name", "execute_tool")
    span.set_attribute("gen_ai.tool.name", tool_name)
    span.set_attribute("gen_ai.tool.type", "function")
    if status_code is not None:
        span.set_attribute("http.status_code", status_code)


# ---------------------------------------------------------------------------
# JSON extraction helpers
# ---------------------------------------------------------------------------


def _parse_json(body: bytes) -> dict[str, Any] | None:
    """Parse JSON from bytes, returning ``None`` on failure."""
    try:
        return json.loads(body)
    except (json.JSONDecodeError, ValueError):
        return None


def _get_user_text(data: dict[str, Any] | None) -> str | None:
    """Extract user message text from an A2A JSON-RPC request body."""
    if not data:
        return None
    message = data.get("params", {}).get("message", {})
    texts: list[str] = []
    for part in message.get("parts", []):
        root = part.get("root", part)
        if "text" in root:
            texts.append(root["text"])
    return " ".join(texts) if texts else None


def _get_agent_text(data: dict[str, Any] | None) -> str | None:
    """Extract the last agent response text from an A2A JSON-RPC response body."""
    if not data:
        return None
    last_agent_text: str | None = None
    for msg in data.get("result", {}).get("history", []):
        if msg.get("role") == "agent":
            texts: list[str] = []
            for part in msg.get("parts", []):
                root = part.get("root", part)
                if "text" in root:
                    texts.append(root["text"])
            if texts:
                last_agent_text = " ".join(texts)
    return last_agent_text
