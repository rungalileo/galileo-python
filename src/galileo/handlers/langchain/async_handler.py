import json
import logging
import time
from typing import Any, Optional
from uuid import UUID

from galileo import galileo_context
from galileo.logger import GalileoLogger
from galileo.schema.handlers import LANGCHAIN_NODE_TYPE, Node
from galileo.utils.serialization import EventSerializer, convert_to_string_dict, serialize_to_str

_logger = logging.getLogger(__name__)

try:
    from langchain_core.agents import AgentAction, AgentFinish
    from langchain_core.callbacks.base import AsyncCallbackHandler
    from langchain_core.documents import Document
    from langchain_core.messages import BaseMessage
    from langchain_core.outputs import LLMResult
except ImportError:
    _logger.warning("Failed to import langchain, using stubs")
    AsyncCallbackHandler = object
    Document = object
    AgentAction = object
    BaseMessage = object
    LLMResult = object
    AgentFinish = object


class GalileoAsyncCallback(AsyncCallbackHandler):
    """
    Async Langchain callback handler for logging traces to the Galileo platform.

    Attributes
    ----------
    _galileo_logger : GalileoLogger
        The Galileo logger instance.
    _nodes : dict[UUID, Node]
        A dictionary of nodes, where the key is the run_id and the value is the node.
    _start_new_trace : bool
        Whether to start a new trace when a chain starts. Set this to `False` to continue using the current trace.
    _flush_on_chain_end : bool
        Whether to flush the trace when a chain ends.
    """

    def __init__(
        self,
        galileo_logger: Optional[GalileoLogger] = None,
        start_new_trace: bool = True,
        flush_on_chain_end: bool = True,
    ):
        self._galileo_logger: GalileoLogger = galileo_logger or galileo_context.get_logger_instance()
        self._start_new_trace: bool = start_new_trace
        self._flush_on_chain_end: bool = flush_on_chain_end
        self._nodes: dict[str, Node] = {}
        self._root_node: Optional[Node] = None

    async def _commit(self) -> None:
        """
        Commit the nodes to the trace using the Galileo Logger. Optionally flush the trace.
        """
        if not self._nodes:
            _logger.warning("No nodes to commit")
            return

        root = self._root_node
        if root is None:
            _logger.warning("Unable to add nodes to trace: Root node not set")
            return

        root_node = self._nodes.get(str(root.run_id))
        if root_node is None:
            _logger.warning("Unable to add nodes to trace: Root node does not exist")
            return

        if self._start_new_trace:
            self._galileo_logger.start_trace(input=serialize_to_str(root_node.span_params.get("input", "")))

        await self._log_node_tree(root_node)

        # Conclude the trace with the root node's output
        root_output = root_node.span_params.get("output", "")

        if self._start_new_trace:
            # If we started a new trace, we need to conclude it
            self._galileo_logger.conclude(output=serialize_to_str(root_output))

        if self._flush_on_chain_end:
            # Upload the trace to Galileo
            await self._galileo_logger.async_flush()

        # Clear nodes after successful commit
        self._nodes.clear()
        self._root_node = None

    async def _log_node_tree(self, node: Node) -> None:
        """
        Log a node and its children recursively.

        Parameters
        ----------
        node : Node
            The node to log.
        """
        is_workflow_span = False
        input_ = node.span_params.get("input", "")
        output = node.span_params.get("output", "")
        name = node.span_params.get("name")
        metadata = node.span_params.get("metadata")
        tags = node.span_params.get("tags")

        # Convert metadata to a dict[str, str]
        if metadata is not None:
            metadata = convert_to_string_dict(metadata)

        # Log the current node based on its type
        if node.node_type in ("agent", "chain"):
            self._galileo_logger.add_workflow_span(input=input_, output=output, name=name, metadata=metadata, tags=tags)
            is_workflow_span = True
        elif node.node_type in ("llm", "chat"):
            self._galileo_logger.add_llm_span(
                input=input_,
                output=output,
                model=node.span_params.get("model"),
                temperature=node.span_params.get("temperature"),
                name=name,
                metadata=metadata,
                tags=tags,
                num_input_tokens=node.span_params.get("num_input_tokens"),
                num_output_tokens=node.span_params.get("num_output_tokens"),
                total_tokens=node.span_params.get("total_tokens"),
                time_to_first_token_ns=node.span_params.get("time_to_first_token_ns"),
            )
        elif node.node_type == "retriever":
            self._galileo_logger.add_retriever_span(
                input=input_, output=output, name=name, metadata=metadata, tags=tags
            )
        elif node.node_type == "tool":
            self._galileo_logger.add_tool_span(input=input_, output=output, name=name, metadata=metadata, tags=tags)
        else:
            _logger.warning(f"Unknown node type: {node.node_type}")

        # Process all child nodes
        last_child = None
        for child_id in node.children:
            child_node = self._nodes.get(child_id)
            if child_node:
                await self._log_node_tree(child_node)
                last_child = child_node
            else:
                _logger.warning(f"Child node {child_id} not found")

        # Conclude workflow span. Use the last child's output if necessary
        if is_workflow_span:
            output = output or (last_child.span_params.get("output", "") if last_child else "")
            self._galileo_logger.conclude(output=serialize_to_str(output))

    async def _start_node(
        self, node_type: LANGCHAIN_NODE_TYPE, parent_run_id: Optional[UUID], run_id: UUID, **kwargs: Any
    ) -> Node:
        """
        Start a new node in the chain.

        Parameters
        ----------
        node_type : LANGCHAIN_NODE_TYPE
            The type of node.
        parent_run_id : Optional[UUID]
            The parent run ID.
        run_id : UUID
            The run ID.
        **kwargs : Any
            Additional parameters for the span.

        Returns
        -------
        Node
            The created node.
        """
        node_id = str(run_id)
        parent_node_id = str(parent_run_id) if parent_run_id else None

        if node_id in self._nodes:
            _logger.debug(f"Node already exists for run_id {run_id}, overwriting...")

        # Create new node
        node = Node(node_type=node_type, span_params=kwargs, run_id=run_id, parent_run_id=parent_run_id)
        self._nodes[node_id] = node

        # Set as root node if needed
        if not self._root_node:
            _logger.debug(f"Setting root node to {node_id}")
            self._root_node = node

        # Add to parent's children if parent exists
        if parent_run_id:
            parent = self._nodes.get(parent_node_id)
            if parent:
                parent.children.append(node_id)
            else:
                _logger.debug(f"Parent node {parent_node_id} not found for {node_id}")

        return node

    async def _end_node(self, run_id: UUID, **kwargs: Any) -> None:
        """
        End a node in the chain. Commit the nodes to a trace if the run_id matches the root node.

        Parameters
        ----------
        run_id : UUID
            The run ID.
        **kwargs : Any
            Additional parameters to update the span with.
        """
        node_id = str(run_id)
        node = self._nodes.get(node_id)

        if not node:
            _logger.debug(f"No node exists for run_id {node_id}")
            return

        # Update node parameters
        node.span_params.update(**kwargs)

        # Check if this is the root node and commit if so
        root = self._root_node
        if root and node.run_id == root.run_id:
            await self._commit()

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
        node_type = "chain"
        node_name = serialized.get("name", None) or kwargs.get("name", "Chain")

        # If the `name` is `LangGraph` or `agent`, set the node type to `agent`.
        if node_name in ["LangGraph", "agent"]:
            node_type = "agent"
            node_name = "Agent"

        kwargs["name"] = node_name

        # If the node is tagged with `hidden`, don't log it.
        if tags and "langsmith:hidden" in tags:
            return

        await self._start_node(node_type, parent_run_id, run_id, input=serialize_to_str(inputs), tags=tags, **kwargs)

    async def on_chain_end(
        self, outputs: dict[str, Any], *, run_id: UUID, parent_run_id: Optional[UUID] = None, **kwargs: Any
    ) -> Any:
        """Langchain callback when a chain ends."""
        await self._end_node(run_id, output=serialize_to_str(outputs))

    async def on_agent_finish(self, finish: AgentFinish, *, run_id: UUID, **kwargs: Any) -> Any:
        """Langchain callback when an agent finishes."""
        await self._end_node(run_id, output=serialize_to_str(finish))

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
        invocation_params = kwargs.get("invocation_params", {})
        model = invocation_params.get("model_name", "")
        temperature = invocation_params.get("temperature", 0.0)

        await self._start_node(
            "llm",
            parent_run_id,
            run_id,
            name="LLM",
            input=[{"content": p, "role": "user"} for p in prompts],
            tags=tags,
            model=model,
            temperature=temperature,
            metadata={k: str(v) for k, v in metadata.items()} if metadata else None,
            start_time=time.perf_counter(),
            time_to_first_token_ns=None,
        )

    async def on_llm_new_token(self, token: str, *, run_id: UUID, **kwargs: Any) -> Any:
        """Langchain callback when an LLM node generates a new token."""
        node = self._nodes.get(str(run_id))
        if not node:
            return

        if "time_to_first_token_ns" not in node.span_params or node.span_params["time_to_first_token_ns"] is None:
            start_time = node.span_params.get("start_time")
            if start_time is not None:
                node.span_params["time_to_first_token_ns"] = (time.perf_counter() - start_time) * 1e9

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
        invocation_params = kwargs.get("invocation_params", {})
        model = invocation_params.get("model", invocation_params.get("_type", "undefined-type"))
        temperature = invocation_params.get("temperature", 0.0)

        # Serialize messages safely
        try:
            flattened_messages = [message.dict() for batch in messages for message in batch]
            serialized_messages = json.loads(json.dumps(flattened_messages, cls=EventSerializer))
        except Exception as e:
            _logger.warning(f"Failed to serialize chat messages: {e}")
            serialized_messages = str(messages)

        await self._start_node(
            "chat",
            parent_run_id,
            run_id,
            name="Chat Model",
            input=serialized_messages,
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
        token_usage = response.llm_output.get("token_usage", {}) if response.llm_output else {}

        try:
            flattened_messages = [message.dict() for batch in response.generations for message in batch]
            output = json.loads(json.dumps(flattened_messages[0], cls=EventSerializer))
        except Exception as e:
            _logger.warning(f"Failed to serialize LLM output: {e}")
            output = str(response.generations)

        await self._end_node(
            run_id,
            output=output,
            num_input_tokens=token_usage.get("prompt_tokens"),
            num_output_tokens=token_usage.get("completion_tokens"),
            total_tokens=token_usage.get("total_tokens"),
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
        await self._start_node(
            "tool",
            parent_run_id,
            run_id,
            name="Tool",
            input=input_str,
            tags=tags,
            metadata={k: str(v) for k, v in metadata.items()} if metadata else None,
        )

    async def on_tool_end(
        self, output: str, *, run_id: UUID, parent_run_id: Optional[UUID] = None, **kwargs: Any
    ) -> Any:
        """Langchain callback when a tool node ends."""
        await self._end_node(run_id, output=serialize_to_str(output))

    async def on_retriever_start(
        self, query: str, *, run_id: UUID, parent_run_id: Optional[UUID] = None, **kwargs: Any
    ) -> Any:
        """Langchain callback when a retriever node starts."""
        await self._start_node("retriever", parent_run_id, run_id, name="Retriever", input=serialize_to_str(query))

    async def on_retriever_end(
        self, response: list[Document], *, run_id: UUID, parent_run_id: Optional[UUID] = None, **kwargs: Any
    ) -> Any:
        """Langchain callback when a retriever node ends."""
        try:
            serialized_response = json.loads(json.dumps(response, cls=EventSerializer))
        except Exception as e:
            _logger.warning(f"Failed to serialize retriever output: {e}")
            serialized_response = str(response)

        await self._end_node(run_id, output=serialized_response)

    async def on_chain_error(
        self, error: Exception, *, run_id: UUID, parent_run_id: Optional[UUID] = None, **kwargs: Any
    ) -> Any:
        """Called when a chain errors."""
        await self._end_node(run_id, output=f"Error: {str(error)}")

    async def on_llm_error(
        self, error: Exception, *, run_id: UUID, parent_run_id: Optional[UUID] = None, **kwargs: Any
    ) -> Any:
        """Called when an LLM errors."""
        await self._end_node(run_id, output=f"Error: {str(error)}")

    async def on_tool_error(
        self, error: Exception, *, run_id: UUID, parent_run_id: Optional[UUID] = None, **kwargs: Any
    ) -> Any:
        """Called when a tool errors."""
        await self._end_node(run_id, output=f"Error: {str(error)}")

    async def on_retriever_error(
        self, error: Exception, *, run_id: UUID, parent_run_id: Optional[UUID] = None, **kwargs: Any
    ) -> Any:
        """Called when a retriever errors."""
        await self._end_node(run_id, output=f"Error: {str(error)}")
