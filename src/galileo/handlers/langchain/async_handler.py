import json
import logging
import time
from typing import Any, Callable, Optional
from uuid import UUID

from galileo.handlers.base_async_handler import GalileoAsyncBaseHandler
from galileo.handlers.langchain.handler import GalileoCallback
from galileo.handlers.langchain.utils import get_agent_name, is_agent_node, parse_llm_result, update_root_to_agent
from galileo.logger import GalileoLogger
from galileo.schema.handlers import NODE_TYPE
from galileo.schema.trace import TracesIngestRequest
from galileo.utils.serialization import EventSerializer, serialize_to_str
from galileo.utils.uuid_utils import convert_uuid_if_uuid7

_logger = logging.getLogger(__name__)

try:
    from langchain_core.agents import AgentFinish
    from langchain_core.callbacks.base import AsyncCallbackHandler
    from langchain_core.documents import Document
    from langchain_core.messages import BaseMessage
    from langchain_core.outputs import LLMResult
except ImportError:
    _logger.warning("Failed to import langchain, using stubs")
    AsyncCallbackHandler = object
    Document = object
    BaseMessage = object
    LLMResult = object
    AgentFinish = object
    ToolMessage = object


class GalileoAsyncCallback(AsyncCallbackHandler):
    """
    Async Langchain callback handler for logging traces to the Galileo platform.

    Attributes
    ----------
    _handler : GalileoAsyncBaseHandler
        The async handler for managing the trace.
    """

    def __init__(
        self,
        galileo_logger: Optional[GalileoLogger] = None,
        start_new_trace: bool = True,
        flush_on_chain_end: bool = True,
        ingestion_hook: Optional[Callable[[TracesIngestRequest], None]] = None,
    ):
        self._handler = GalileoAsyncBaseHandler(
            flush_on_chain_end=flush_on_chain_end,
            start_new_trace=start_new_trace,
            galileo_logger=galileo_logger,
            integration="langchain",
            ingestion_hook=ingestion_hook,
        )

    async def on_chain_start(
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

        # Convert UUID7s to UUID4s if needed
        run_id = convert_uuid_if_uuid7(run_id) or run_id
        parent_run_id = convert_uuid_if_uuid7(parent_run_id) if parent_run_id else None

        node_type: NODE_TYPE = "chain"
        node_name = GalileoCallback._get_node_name(node_type, serialized, kwargs)

        # If the `name` is `LangGraph` or `Agent`, set the node type to `agent`.
        if is_agent_node(node_name):
            node_type = "agent"
            node_name = get_agent_name(parent_run_id, "Agent", self._handler.get_nodes())

        update_root_to_agent(
            parent_run_id, kwargs.get("metadata", {}), self._handler.get_node(parent_run_id) if parent_run_id else None
        )

        kwargs["name"] = node_name
        await self._handler.async_start_node(
            node_type, parent_run_id, run_id, input=serialize_to_str(inputs), tags=tags, **kwargs
        )

    async def on_chain_end(
        self, outputs: dict[str, Any], *, run_id: UUID, parent_run_id: Optional[UUID] = None, **kwargs: Any
    ) -> Any:
        """Langchain callback when a chain ends."""
        # Convert UUID7 to UUID4 if needed
        run_id = convert_uuid_if_uuid7(run_id) or run_id

        # The input is sent via kwargs in on_chain_end in async streaming mode
        if "inputs" in kwargs:
            kwargs["input"] = serialize_to_str(kwargs["inputs"])
        await self._handler.async_end_node(run_id, output=serialize_to_str(outputs), status_code=200, **kwargs)

    async def on_agent_finish(self, finish: AgentFinish, *, run_id: UUID, **kwargs: Any) -> Any:
        """Langchain callback when an agent finishes."""
        # Convert UUID7 to UUID4 if needed
        run_id = convert_uuid_if_uuid7(run_id) or run_id
        await self._handler.async_end_node(run_id, output=serialize_to_str(finish), status_code=200)

    async def on_llm_start(
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
        # Convert UUID7s to UUID4s if needed
        run_id = convert_uuid_if_uuid7(run_id) or run_id
        parent_run_id = convert_uuid_if_uuid7(parent_run_id) if parent_run_id else None

        node_type: NODE_TYPE = "llm"
        node_name = GalileoCallback._get_node_name(node_type, serialized, kwargs)
        invocation_params = kwargs.get("invocation_params", {})
        model = invocation_params.get("model_name", "")
        temperature = invocation_params.get("temperature", 0.0)

        await self._handler.async_start_node(
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

    async def on_llm_new_token(self, token: str, *, run_id: UUID, **kwargs: Any) -> Any:
        """Langchain callback when an LLM node generates a new token."""
        # Convert UUID7 to UUID4 if needed
        run_id = convert_uuid_if_uuid7(run_id) or run_id

        node = self._handler.get_node(run_id)
        if not node:
            return

        if "time_to_first_token_ns" not in node.span_params or node.span_params["time_to_first_token_ns"] is None:
            start_time = node.span_params.get("start_time")
            if start_time is not None:
                node.span_params["time_to_first_token_ns"] = time.perf_counter_ns() - start_time

    async def on_chat_model_start(
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
        # Convert UUID7s to UUID4s if needed
        run_id = convert_uuid_if_uuid7(run_id) or run_id
        parent_run_id = convert_uuid_if_uuid7(parent_run_id) if parent_run_id else None

        node_type: NODE_TYPE = "chat"
        node_name = GalileoCallback._get_node_name(node_type, serialized, kwargs)
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

        await self._handler.async_start_node(
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

    async def on_llm_end(
        self, response: LLMResult, *, run_id: UUID, parent_run_id: Optional[UUID] = None, **kwargs: Any
    ) -> Any:
        """Langchain callback when an LLM node ends."""
        # Convert UUID7 to UUID4 if needed
        run_id = convert_uuid_if_uuid7(run_id) or run_id

        result = parse_llm_result(response)
        await self._handler.async_end_node(
            run_id,
            output=result.output,
            num_input_tokens=result.num_input_tokens,
            num_output_tokens=result.num_output_tokens,
            total_tokens=result.total_tokens,
            status_code=200,
        )

    async def on_tool_start(
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
        # Convert UUID7s to UUID4s if needed
        run_id = convert_uuid_if_uuid7(run_id) or run_id
        parent_run_id = convert_uuid_if_uuid7(parent_run_id) if parent_run_id else None

        node_type: NODE_TYPE = "tool"
        node_name = GalileoCallback._get_node_name(node_type, serialized, kwargs)
        if "inputs" in kwargs and isinstance(kwargs["inputs"], dict):
            input_str = json.dumps(kwargs["inputs"], cls=EventSerializer)
        await self._handler.async_start_node(
            node_type,
            parent_run_id,
            run_id,
            name=node_name,
            input=input_str,
            tags=tags,
            metadata={k: str(v) for k, v in metadata.items()} if metadata else None,
        )

    async def on_tool_end(
        self, output: Any, *, run_id: UUID, parent_run_id: Optional[UUID] = None, **kwargs: Any
    ) -> Any:
        """Langchain callback when a tool node ends."""
        # Convert UUID7 to UUID4 if needed
        run_id = convert_uuid_if_uuid7(run_id) or run_id

        end_node_kwargs: dict[str, Any] = {"status_code": 200}
        if (tool_message := GalileoCallback._find_tool_message(output)) is not None:
            end_node_kwargs["output"] = tool_message.content
            end_node_kwargs["tool_call_id"] = tool_message.tool_call_id
        else:
            # Handle tools with response_format="content_and_artifact" returning (content, artifact)
            if isinstance(output, tuple) and len(output) >= 1:
                end_node_kwargs["output"] = output[0]  # Extract content only
            else:
                end_node_kwargs["output"] = output
        # This will pass-through strings like 'blah' without encoding them
        # into '"blah"', but will turn everything else into a JSON string.
        end_node_kwargs["output"] = (
            end_node_kwargs["output"]
            if isinstance(end_node_kwargs["output"], str)
            else json.dumps(end_node_kwargs["output"], cls=EventSerializer)
        )
        await self._handler.async_end_node(run_id, **end_node_kwargs)

    async def on_retriever_start(
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
        # Convert UUID7s to UUID4s if needed
        run_id = convert_uuid_if_uuid7(run_id) or run_id
        parent_run_id = convert_uuid_if_uuid7(parent_run_id) if parent_run_id else None

        node_type: NODE_TYPE = "retriever"
        node_name = GalileoCallback._get_node_name(node_type, serialized, kwargs)
        await self._handler.async_start_node(
            node_type,
            parent_run_id,
            run_id,
            name=node_name,
            input=serialize_to_str(query),
            tags=tags,
            metadata={k: str(v) for k, v in metadata.items()} if metadata else None,
        )

    async def on_retriever_end(
        self, documents: list[Document], *, run_id: UUID, parent_run_id: Optional[UUID] = None, **kwargs: Any
    ) -> Any:
        """Langchain callback when a retriever node ends."""
        # Convert UUID7 to UUID4 if needed
        run_id = convert_uuid_if_uuid7(run_id) or run_id

        try:
            serialized_response = json.loads(json.dumps(documents, cls=EventSerializer))
        except Exception as e:
            _logger.warning(f"Failed to serialize retriever output: {e}")
            serialized_response = str(documents)

        await self._handler.async_end_node(run_id, output=serialized_response, status_code=200)

    async def on_chain_error(
        self, error: Exception, *, run_id: UUID, parent_run_id: Optional[UUID] = None, **kwargs: Any
    ) -> Any:
        """Langchain callback when a chain errors."""
        # Convert UUID7 to UUID4 if needed
        run_id = convert_uuid_if_uuid7(run_id) or run_id
        await self._handler.async_end_node(run_id, output=f"Error: {error!s}", status_code=400)

    async def on_llm_error(
        self, error: Exception, *, run_id: UUID, parent_run_id: Optional[UUID] = None, **kwargs: Any
    ) -> Any:
        """Langchain callback when an LLM errors."""
        # Convert UUID7 to UUID4 if needed
        run_id = convert_uuid_if_uuid7(run_id) or run_id
        await self._handler.async_end_node(run_id, output=f"Error: {error!s}", status_code=400)

    async def on_tool_error(
        self, error: Exception, *, run_id: UUID, parent_run_id: Optional[UUID] = None, **kwargs: Any
    ) -> Any:
        """Langchain callback when a tool errors."""
        # Convert UUID7 to UUID4 if needed
        run_id = convert_uuid_if_uuid7(run_id) or run_id
        await self._handler.async_end_node(run_id, output=f"Error: {error!s}", status_code=400)

    async def on_retriever_error(
        self, error: Exception, *, run_id: UUID, parent_run_id: Optional[UUID] = None, **kwargs: Any
    ) -> Any:
        """Langchain callback when a retriever errors."""
        # Convert UUID7 to UUID4 if needed
        run_id = convert_uuid_if_uuid7(run_id) or run_id
        await self._handler.async_end_node(run_id, output=f"Error: {error!s}", status_code=400)
