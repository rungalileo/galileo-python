import json
import logging
import time
from typing import Any, Callable, Optional
from uuid import UUID, uuid4

from langchain_core.messages import AnyMessage
from pydantic import BaseModel

from galileo.handlers.base_async_handler import GalileoAsyncBaseHandler
from galileo.handlers.base_handler import GalileoBaseHandler
from galileo.handlers.langchain.handler import GalileoCallback
from galileo.logger import GalileoLogger
from galileo.schema.trace import TracesIngestRequest
from galileo.utils.serialization import EventSerializer, serialize_to_str
from galileo_core.schemas.logging.llm import Message, MessageRole

try:
    from langchain_core.messages import AIMessage, BaseMessage
    from langchain_core.tools import StructuredTool
    from langgraph.runtime import Runtime

    from langchain.agents.middleware import AgentMiddleware, AgentState  # type: ignore[attr-defined]

    HAS_LANGCHAIN = True
except ImportError:
    logging.getLogger(__name__).warning("Failed to import langchain, using stubs")
    HAS_LANGCHAIN = False

    class AgentMiddleware:
        def __init__(self, *args, **kwargs):
            raise ImportError("langchain is not installed or is not compatible with the expected version.")


_logger = logging.getLogger(__name__)


class GalileoMiddleware(AgentMiddleware):
    def __init__(
        self,
        galileo_logger: Optional[GalileoLogger] = None,
        start_new_trace: bool = True,
        flush_on_chain_end: bool = True,
        ingestion_hook: Optional[Callable[[TracesIngestRequest], None]] = None,
    ) -> None:
        if not HAS_LANGCHAIN:
            raise ImportError("langchain is not installed or is not compatible with the expected version.")
        super().__init__()
        self._handler = GalileoBaseHandler(
            flush_on_chain_end=flush_on_chain_end,
            start_new_trace=start_new_trace,
            galileo_logger=galileo_logger,
            integration="langchain",
            ingestion_hook=ingestion_hook,
        )
        self._async_handler = GalileoAsyncBaseHandler(
            flush_on_chain_end=flush_on_chain_end,
            start_new_trace=start_new_trace,
            galileo_logger=galileo_logger,
            integration="langchain",
            ingestion_hook=ingestion_hook,
        )
        self._root_run_id: Optional[UUID] = None

    @staticmethod
    def _serialize_messages(messages: Optional[list["AnyMessage"]]) -> Any:
        if messages is None:
            return None
        try:
            return json.loads(json.dumps(messages, cls=EventSerializer))
        except Exception as exc:
            _logger.warning(f"Failed to serialize messages: {exc}")
            return str(messages)

    @staticmethod
    def _get_state_messages(state: Optional["AgentState"]) -> Optional[list["AnyMessage"]]:
        if isinstance(state, dict) and "messages" in state:
            return state.get("messages")
        return None

    def _serialize_state(self, state: Optional["AgentState"]) -> Any:
        """Serialize state, preferring messages if available."""
        messages = self._get_state_messages(state)
        return self._serialize_messages(messages) if messages else serialize_to_str(state)

    @staticmethod
    def _extract_model_metadata(request: Any) -> tuple[Optional[str], Optional[float]]:
        model_settings = getattr(request, "model_settings", {}) or {}
        model_name = model_settings.get("model") or model_settings.get("model_name")
        if not model_name:
            model = getattr(request, "model", None)
            model_name = getattr(model, "model_name", None) or getattr(model, "model", None)
        return model_name, model_settings.get("temperature")

    @staticmethod
    def _get_model_display_name(request: Any, model_name: Optional[str]) -> str:
        if model_name:
            return model_name
        model = getattr(request, "model", None)
        if model is None:
            return "ChatModel"
        return getattr(model, "model_name", None) or model.__class__.__name__

    def _serialize_response(self, response: Any) -> Any:
        """Serialize model response to appropriate output format."""
        if hasattr(response, "result"):
            return self._serialize_messages(getattr(response, "result", None))
        if HAS_LANGCHAIN and isinstance(response, (AIMessage, BaseMessage)):
            return self._serialize_messages([response])
        return serialize_to_str(response)

    def _serialize_tools(self, tools: Optional[list[StructuredTool]]) -> Any:
        if tools is None:
            return None
        tools_list = []
        for tool in tools:
            tools_list.append(
                {
                    "function": {
                        "name": tool.name,
                        "arguments": json.dumps(
                            tool.args_schema.model_json_schema()
                            if isinstance(tool.args_schema, BaseModel)
                            else tool.args_schema,
                            cls=EventSerializer,
                        ),
                    }
                }
            )
        return tools_list

    def _prepare_model_call_params(self, request: "AgentState") -> dict[str, Any]:
        """Prepare common parameters for model call nodes."""
        model_name, temperature = self._extract_model_metadata(request)
        messages = list(getattr(request, "messages", []) or [])
        system_message = getattr(request, "system_message", None)
        if system_message:
            messages = [system_message, *messages]

        tools = getattr(request, "tools", None)
        if tools is None:
            state = getattr(request, "state", {}) or {}
            if isinstance(state, dict):
                tools = state.get("tools")
        return {
            "name": self._get_model_display_name(request, model_name),
            "input": self._serialize_messages(messages),
            "tools": self._serialize_tools(tools),
            "model": model_name,
            "temperature": temperature,
            "time_to_first_token_ns": None,
            "start_time": time.perf_counter_ns(),
        }

    def _prepare_tool_call_params(self, request: "AgentState") -> tuple[str, str]:
        """Extract tool name and serialized args from request."""
        tool_call = getattr(request, "tool_call", {}) or {}
        return tool_call.get("name", "tool"), json.dumps(tool_call.get("args", {}), cls=EventSerializer)

    def _serialize_tool_response(self, response: "AgentState") -> dict[str, Any]:
        """Serialize tool response to end_node kwargs."""
        kwargs: dict[str, Any] = {}
        tool_message = GalileoCallback._find_tool_message(response)
        if tool_message is not None:
            kwargs["output"] = tool_message.content
            kwargs["tool_call_id"] = tool_message.tool_call_id
        else:
            kwargs["output"] = response

        if not isinstance(kwargs["output"], str):
            kwargs["output"] = json.dumps(kwargs["output"], cls=EventSerializer)
        return kwargs

    def _ensure_root_node(self, state: Optional["AgentState"]) -> UUID:
        if self._root_run_id is None:
            self._root_run_id = uuid4()
            self._handler.start_node("agent", None, self._root_run_id, name="Agent", input=self._serialize_state(state))
        return self._root_run_id

    async def _ensure_async_root_node(self, state: Optional["AgentState"]) -> UUID:
        if self._root_run_id is None:
            self._root_run_id = uuid4()
            await self._async_handler.async_start_node(
                "agent", None, self._root_run_id, name="Agent", input=self._serialize_state(state)
            )
        return self._root_run_id

    def before_agent(self, state: "AgentState", runtime: "Runtime") -> Optional[dict[str, Any]]:
        self._ensure_root_node(state)
        return None

    def after_agent(self, state: "AgentState", runtime: "Runtime") -> Optional[dict[str, Any]]:
        if self._root_run_id is None:
            return None
        messages = self._serialize_state(state)
        if isinstance(messages, list) and len(messages) > 0:
            messages = messages[-1]
        self._handler.end_node(self._root_run_id, output=messages)
        self._root_run_id = None
        return None

    async def abefore_agent(self, state: "AgentState", runtime: "Runtime") -> Optional[dict[str, Any]]:
        await self._ensure_async_root_node(state)
        return None

    async def aafter_agent(self, state: "AgentState", runtime: "Runtime") -> Optional[dict[str, Any]]:
        if self._root_run_id is None:
            return None
        await self._async_handler.async_end_node(self._root_run_id, output=self._serialize_state(state))
        self._root_run_id = None
        return None

    def wrap_model_call(self, request: "AgentState", handler: Callable[[Any], Any]) -> Any:
        root_run_id = self._ensure_root_node(getattr(request, "state", None))
        run_id = uuid4()

        self._handler.start_node("llm", root_run_id, run_id, **self._prepare_model_call_params(request))

        response = handler(request)
        messages = self._serialize_response(response)
        if isinstance(messages, list) and len(messages) > 0:
            message = messages[-1]
        else:
            message = messages if messages else Message(content="", role=MessageRole.assistant)

        # Ensure message is a Message instance
        if not isinstance(message, Message):
            message = Message(content=str(message), role=MessageRole.assistant)

        self._handler.end_node(run_id, output=message)
        return response

    async def awrap_model_call(self, request: "AgentState", handler: Callable[[Any], Any]) -> Any:
        root_run_id = await self._ensure_async_root_node(getattr(request, "state", None))
        run_id = uuid4()
        await self._async_handler.async_start_node(
            "llm", root_run_id, run_id, **self._prepare_model_call_params(request)
        )

        response = await handler(request)

        messages = self._serialize_response(response)
        if isinstance(messages, list) and len(messages) > 0:
            message = messages[-1]
        else:
            message = messages if messages else Message(content="", role=MessageRole.assistant)

        # Ensure message is a Message instance
        if not isinstance(message, Message):
            message = Message(content=str(message), role=MessageRole.assistant)

        await self._async_handler.async_end_node(run_id, output=message)
        return response

    def wrap_tool_call(self, request: "AgentState", handler: Callable[[Any], Any]) -> Any:
        root_run_id = self._ensure_root_node(getattr(request, "state", None))
        run_id = uuid4()
        tool_name, tool_input = self._prepare_tool_call_params(request)
        self._handler.start_node("tool", root_run_id, run_id, name=tool_name, input=tool_input)

        response = handler(request)
        self._handler.end_node(run_id, **self._serialize_tool_response(response))
        return response

    async def awrap_tool_call(self, request: "AgentState", handler: Callable[[Any], Any]) -> Any:
        root_run_id = await self._ensure_async_root_node(getattr(request, "state", None))
        run_id = uuid4()
        tool_name, tool_input = self._prepare_tool_call_params(request)
        await self._async_handler.async_start_node("tool", root_run_id, run_id, name=tool_name, input=tool_input)

        response = await handler(request)
        await self._async_handler.async_end_node(run_id, **self._serialize_tool_response(response))
        return response
