import json
import logging
import time
from typing import Any, Optional
from uuid import UUID

from galileo.handlers.base_handler import GalileoBaseHandler
from galileo.handlers.langchain.utils import get_agent_name, is_agent_node
from galileo.logger import GalileoLogger
from galileo.schema.handlers import LANGCHAIN_NODE_TYPE, NODE_TYPE
from galileo.utils.serialization import EventSerializer, serialize_to_str

_logger = logging.getLogger(__name__)

try:
    from langchain_core.agents import AgentFinish
    from langchain_core.callbacks.base import BaseCallbackHandler
    from langchain_core.documents import Document
    from langchain_core.messages import BaseMessage, ToolMessage
    from langchain_core.outputs import LLMResult
except ImportError:
    _logger.warning("Failed to import langchain, using stubs")
    BaseCallbackHandler = object
    Document = object
    BaseMessage = object
    LLMResult = object
    AgentFinish = object
    ToolMessage = object


class GalileoCallback(BaseCallbackHandler):
    """
    Langchain callback handler for logging traces to the Galileo platform.

    Attributes
    ----------
    _handler : GalileoBaseHandler
        The handler for managing the trace.
    """

    def __init__(
        self,
        galileo_logger: Optional[GalileoLogger] = None,
        start_new_trace: bool = True,
        flush_on_chain_end: bool = True,
    ):
        self._handler = GalileoBaseHandler(
            flush_on_chain_end=flush_on_chain_end,
            start_new_trace=start_new_trace,
            galileo_logger=galileo_logger,
            integration="langchain",
        )

    @staticmethod
    def _get_node_name(
        node_type: LANGCHAIN_NODE_TYPE,
        serialized: Optional[dict[str, Any]] = None,
        kwargs: Optional[dict[str, Any]] = None,
    ) -> str:
        try:
            node_name = None
            node_class_reference = None
            # Langchain can pass None or non-dict objects as serialized
            if serialized is not None and isinstance(serialized, dict):
                node_name = serialized.get("name")
                node_class_reference = serialized.get("id")

            if node_name:
                return node_name
            elif node_class_reference and isinstance(node_class_reference, list):
                return node_class_reference[-1]
            elif isinstance(kwargs, dict):
                if kwargs_name := kwargs.get("name"):
                    return kwargs_name
                if "metadata" in kwargs and isinstance(kwargs["metadata"], dict):
                    if metadata_name := kwargs["metadata"].get("name"):
                        return metadata_name
            return node_type.capitalize()
        except Exception as e:
            _logger.error(f"Failed to get node name: {e}")
            return node_type.capitalize()

    def on_chain_start(
        self,
        serialized: dict[str, Any],
        inputs: dict[str, Any],
        *,
        run_id: UUID,
        parent_run_id: Optional[UUID] = None,
        tags: Optional[list[str]] = None,
        **kwargs: Any,
    ) -> Any:
        """Langchain callback when a chain starts."""
        # If the node is tagged with `hidden`, don't log it.
        if tags and "langsmith:hidden" in tags:
            return

        node_type: NODE_TYPE = "chain"
        node_name = self._get_node_name(node_type, serialized, kwargs)

        # If the `name` is `LangGraph` or `Agent`, set the node type to `agent`.
        if is_agent_node(node_name):
            node_type = "agent"
            node_name = get_agent_name(parent_run_id, "Agent", self._handler.get_nodes())
        kwargs["name"] = node_name
        self._handler.start_node(node_type, parent_run_id, run_id, input=serialize_to_str(inputs), tags=tags, **kwargs)

    def on_chain_end(
        self, outputs: dict[str, Any], *, run_id: UUID, parent_run_id: Optional[UUID] = None, **kwargs: Any
    ) -> Any:
        """Langchain callback when a chain ends."""
        self._handler.end_node(run_id, output=serialize_to_str(outputs))

    def on_agent_finish(self, finish: AgentFinish, *, run_id: UUID, **kwargs: Any) -> Any:
        """Langchain callback when an agent finishes."""
        self._handler.end_node(run_id, output=serialize_to_str(finish))

    def on_llm_start(
        self,
        serialized: dict[str, Any],
        prompts: list[str],
        *,
        run_id: UUID,
        parent_run_id: Optional[UUID] = None,
        tags: Optional[list[str]] = None,
        metadata: Optional[dict[str, Any]] = None,
        **kwargs: Any,
    ) -> Any:
        """
        Langchain callback when an LLM node starts.

        Note: This callback is only used for non-chat models.
        """
        node_type: NODE_TYPE = "llm"
        node_name = self._get_node_name(node_type, serialized, kwargs)
        invocation_params = kwargs.get("invocation_params", {})
        model = invocation_params.get("model_name", "")
        temperature = invocation_params.get("temperature", 0.0)

        self._handler.start_node(
            node_type,
            parent_run_id,
            run_id,
            name=node_name,
            input=[{"content": p, "role": "user"} for p in prompts],
            tags=tags,
            model=model,
            temperature=temperature,
            metadata={k: str(v) for k, v in metadata.items()} if metadata else None,
            start_time=time.perf_counter_ns(),
            time_to_first_token_ns=None,
        )

    def on_llm_new_token(self, token: str, *, run_id: UUID, **kwargs: Any) -> Any:
        """Langchain callback when an LLM node generates a new token."""
        node = self._handler.get_node(run_id)
        if not node:
            return

        if "time_to_first_token_ns" not in node.span_params or node.span_params["time_to_first_token_ns"] is None:
            start_time = node.span_params.get("start_time")
            if start_time is not None:
                node.span_params["time_to_first_token_ns"] = time.perf_counter_ns() - start_time

    def on_chat_model_start(
        self,
        serialized: dict[str, Any],
        messages: list[list[BaseMessage]],
        *,
        run_id: UUID,
        parent_run_id: Optional[UUID] = None,
        tags: Optional[list[str]] = None,
        metadata: Optional[dict[str, Any]] = None,
        **kwargs: Any,
    ) -> Any:
        """Langchain callback when a chat model starts."""
        node_type: NODE_TYPE = "chat"
        node_name = self._get_node_name(node_type, serialized, kwargs)
        invocation_params = kwargs.get("invocation_params", {})
        model = invocation_params.get("model", invocation_params.get("_type", "undefined-type"))
        temperature = invocation_params.get("temperature", 0.0)
        tools = invocation_params.get("tools")

        # Serialize messages safely
        try:
            flattened_messages = [message for batch in messages for message in batch]
            serialized_messages = json.loads(json.dumps(flattened_messages, cls=EventSerializer))
        except Exception as e:
            _logger.warning(f"Failed to serialize chat messages: {e}")
            serialized_messages = str(messages)

        self._handler.start_node(
            node_type,
            parent_run_id,
            run_id,
            name=node_name,
            input=serialized_messages,
            tools=json.loads(json.dumps(tools, cls=EventSerializer)) if tools else None,
            tags=tags,
            model=model,
            temperature=temperature,
            metadata={k: str(v) for k, v in metadata.items()} if metadata else None,
            time_to_first_token_ns=None,
        )

    def on_llm_end(
        self, response: LLMResult, *, run_id: UUID, parent_run_id: Optional[UUID] = None, **kwargs: Any
    ) -> Any:
        """Langchain callback when an LLM node ends."""
        token_usage = response.llm_output.get("token_usage", {}) if response.llm_output else {}

        try:
            flattened_messages = [message for batch in response.generations for message in batch]
            output = json.loads(json.dumps(flattened_messages[0], cls=EventSerializer))
        except Exception as e:
            _logger.warning(f"Failed to serialize LLM output: {e}")
            output = str(response.generations)

        self._handler.end_node(
            run_id,
            output=output,
            num_input_tokens=token_usage.get("prompt_tokens"),
            num_output_tokens=token_usage.get("completion_tokens"),
            total_tokens=token_usage.get("total_tokens"),
        )

    def on_tool_start(
        self,
        serialized: dict[str, Any],
        input_str: str,
        *,
        run_id: UUID,
        parent_run_id: Optional[UUID] = None,
        tags: Optional[list[str]] = None,
        metadata: Optional[dict[str, Any]] = None,
        **kwargs: Any,
    ) -> Any:
        """Langchain callback when a tool node starts."""
        node_type: NODE_TYPE = "tool"
        node_name = self._get_node_name(node_type, serialized, kwargs)
        if "inputs" in kwargs and isinstance(kwargs["inputs"], dict):
            input_str = json.dumps(kwargs["inputs"], cls=EventSerializer)
        self._handler.start_node(
            node_type,
            parent_run_id,
            run_id,
            name=node_name,
            input=input_str,
            tags=tags,
            metadata={k: str(v) for k, v in metadata.items()} if metadata else None,
        )

    @staticmethod
    def _find_tool_message(obj: Any) -> Optional[ToolMessage]:
        """
        Look for a ToolMessage in the output passed to langchain's on_tool_end callback.
        If found, return the ToolMessage. Otherwise, return None.

        Can return a ToolMessage in two cases:
        1. The output is already a ToolMessage.
        2. The output is a Command object with a ToolMessage in its update list.

        As of this writing, Command and ToolMessage are the only Langchain/Langgraph
        classes inheriting from ToolOutputMixin. And Langchain is supposed to convert
        any tool output **not** inheriting from ToolOutputMixin to a ToolMessage.

        So this should cover all cases. Either:

        - the output is a Command (converted to ToolMessage here),
        - or Langchain will force it to be a ToolMessage before passing it to us.
        """
        if isinstance(obj, ToolMessage):
            return obj
        if hasattr(obj, "update") and isinstance(obj.update, dict) and "messages" in obj.update:
            update_messages = obj.update["messages"]
            if (
                isinstance(update_messages, list)
                and len(update_messages) > 0
                and isinstance(update_messages[-1], ToolMessage)
            ):
                return update_messages[-1]
        return None

    def on_tool_end(self, output: Any, *, run_id: UUID, parent_run_id: Optional[UUID] = None, **kwargs: Any) -> Any:
        """Langchain callback when a tool node ends."""
        end_node_kwargs = {}
        if (tool_message := self._find_tool_message(output)) is not None:
            end_node_kwargs["output"] = tool_message.content
            end_node_kwargs["tool_call_id"] = tool_message.tool_call_id
        else:
            end_node_kwargs["output"] = output
        # This will pass-through strings like 'blah' without encoding them
        # into '"blah"', but will turn everything else into a JSON string.
        end_node_kwargs["output"] = (
            end_node_kwargs["output"]
            if isinstance(end_node_kwargs["output"], str)
            else json.dumps(end_node_kwargs["output"], cls=EventSerializer)
        )
        self._handler.end_node(run_id, **end_node_kwargs)

    def on_retriever_start(
        self,
        serialized: dict[str, Any],
        query: str,
        *,
        run_id: UUID,
        parent_run_id: Optional[UUID] = None,
        tags: Optional[list[str]] = None,
        metadata: Optional[dict[str, Any]] = None,
        **kwargs: Any,
    ) -> Any:
        """Langchain callback when a retriever node starts."""
        node_type: NODE_TYPE = "retriever"
        node_name = self._get_node_name(node_type, serialized, kwargs)
        self._handler.start_node(
            node_type,
            parent_run_id,
            run_id,
            name=node_name,
            input=serialize_to_str(query),
            tags=tags,
            metadata={k: str(v) for k, v in metadata.items()} if metadata else None,
        )

    def on_retriever_end(
        self, documents: list[Document], *, run_id: UUID, parent_run_id: Optional[UUID] = None, **kwargs: Any
    ) -> Any:
        """Langchain callback when a retriever node ends."""
        try:
            serialized_response = json.loads(json.dumps(documents, cls=EventSerializer))
        except Exception as e:
            _logger.warning(f"Failed to serialize retriever output: {e}")
            serialized_response = str(documents)

        self._handler.end_node(run_id, output=serialized_response)

    def _get_agent_name(self, parent_run_id: Optional[UUID], node_name: str) -> str:
        if parent_run_id is not None:
            parent = self._handler.get_node(parent_run_id)
            if parent:
                return parent.span_params["name"] + ":" + node_name
        return node_name
