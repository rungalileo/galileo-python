import json
import logging
import time
from datetime import datetime, timezone
from typing import Any, Optional
from uuid import UUID

from galileo import galileo_context
from galileo.handlers.langchain.handler import GalileoCallback
from galileo.logger import GalileoLogger
from galileo.schema.handlers import LANGCHAIN_NODE_TYPE, Node
from galileo.utils.serialization import EventSerializer, convert_to_string_dict, serialize_to_str

_logger = logging.getLogger(__name__)

try:
    from langchain_core.agents import AgentFinish
    from langchain_core.callbacks.base import AsyncCallbackHandler
    from langchain_core.documents import Document
    from langchain_core.messages import BaseMessage, ToolMessage
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
        is_span_with_children = False
        input_ = node.span_params.get("input", "")
        output = node.span_params.get("output", "")
        name = node.span_params.get("name")
        metadata = node.span_params.get("metadata")
        tags = node.span_params.get("tags")
        created_at = node.span_params.get("created_at")

        # Convert metadata to a dict[str, str]
        if metadata is not None:
            metadata = convert_to_string_dict(metadata)

        step_number = metadata.get("langgraph_step") if metadata else None
        if step_number is not None:
            try:
                step_number = int(step_number)
            except Exception as e:
                _logger.warning(f"Invalid step number: {step_number}, exception raised {e}")
                step_number = None

        # Log the current node based on its type
        if node.node_type == "chain":
            self._galileo_logger.add_workflow_span(
                input=input_,
                output=output,
                name=name,
                duration_ns=node.span_params.get("duration_ns"),
                metadata=metadata,
                tags=tags,
                created_at=created_at,
                step_number=step_number,
            )
            is_span_with_children = True
        elif node.node_type == "agent":
            self._galileo_logger.add_agent_span(
                input=input_,
                output=output,
                name=name,
                duration_ns=node.span_params.get("duration_ns"),
                metadata=metadata,
                tags=tags,
                created_at=created_at,
                step_number=step_number,
            )
            is_span_with_children = True
        elif node.node_type in ("llm", "chat"):
            self._galileo_logger.add_llm_span(
                input=input_,
                output=output,
                model=node.span_params.get("model"),
                temperature=node.span_params.get("temperature"),
                tools=node.span_params.get("tools"),
                name=name,
                duration_ns=node.span_params.get("duration_ns"),
                metadata=metadata,
                tags=tags,
                num_input_tokens=node.span_params.get("num_input_tokens"),
                num_output_tokens=node.span_params.get("num_output_tokens"),
                total_tokens=node.span_params.get("total_tokens"),
                time_to_first_token_ns=node.span_params.get("time_to_first_token_ns"),
                created_at=created_at,
                step_number=step_number,
            )
        elif node.node_type == "retriever":
            self._galileo_logger.add_retriever_span(
                input=input_,
                output=output,
                name=name,
                duration_ns=node.span_params.get("duration_ns"),
                metadata=metadata,
                tags=tags,
                created_at=created_at,
                step_number=step_number,
            )
        elif node.node_type == "tool":
            self._galileo_logger.add_tool_span(
                input=input_,
                output=output,
                name=name,
                duration_ns=node.span_params.get("duration_ns"),
                metadata=metadata,
                tags=tags,
                created_at=created_at,
                step_number=step_number,
                tool_call_id=node.span_params.get("tool_call_id"),
            )
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

        # Conclude parent span. Use the last child's output if necessary
        if is_span_with_children:
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

        # start_time is used to calculate duration_ns
        if "start_time" not in node.span_params:
            node.span_params["start_time"] = time.perf_counter_ns()

        if "created_at" not in node.span_params:
            node.span_params["created_at"] = datetime.now(tz=timezone.utc)

        self._nodes[node_id] = node

        # Set as root node if needed
        if not self._root_node:
            _logger.debug(f"Setting root node to {node_id}")
            self._root_node = node

        # Add to parent's children if parent exists
        if parent_run_id:
            parent = self._nodes.get(parent_node_id)
            if parent:
                if node.node_type == "agent":
                    node.span_params["name"] = parent.span_params["name"] + ":" + node.span_params["name"]
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

        node.span_params["duration_ns"] = time.perf_counter_ns() - node.span_params["start_time"]

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
        # If the node is tagged with `hidden`, don't log it.
        if tags and "langsmith:hidden" in tags:
            return

        node_type = "chain"
        node_name = GalileoCallback._get_node_name(node_type, serialized, kwargs)

        # If the `name` is `LangGraph` or `Agent`, set the node type to `agent`.
        if node_name in ["LangGraph", "Agent"]:
            node_type = "agent"
            node_name = "Agent"

        kwargs["name"] = node_name

        await self._start_node(node_type, parent_run_id, run_id, input=serialize_to_str(inputs), tags=tags, **kwargs)

    async def on_chain_end(
        self, outputs: dict[str, Any], *, run_id: UUID, parent_run_id: Optional[UUID] = None, **kwargs: Any
    ) -> Any:
        """Langchain callback when a chain ends."""
        # The input is sent via kwargs in on_chain_end in async streaming mode
        if "inputs" in kwargs:
            kwargs["input"] = serialize_to_str(kwargs["inputs"])
        await self._end_node(run_id, output=serialize_to_str(outputs), **kwargs)

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
        node_type = "llm"
        node_name = GalileoCallback._get_node_name(node_type, serialized, kwargs)
        invocation_params = kwargs.get("invocation_params", {})
        model = invocation_params.get("model_name", "")
        temperature = invocation_params.get("temperature", 0.0)

        await self._start_node(
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
        node = self._nodes.get(str(run_id))
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
        node_type = "chat"
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

        await self._start_node(
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
        token_usage = response.llm_output.get("token_usage", {}) if response.llm_output else {}

        try:
            flattened_messages = [message for batch in response.generations for message in batch]
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
        node_type = "tool"
        node_name = GalileoCallback._get_node_name(node_type, serialized, kwargs)
        if "inputs" in kwargs and isinstance(kwargs["inputs"], dict):
            input_str = json.dumps(kwargs["inputs"], cls=EventSerializer)
        await self._start_node(
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
        end_node_kwargs = {}
        if (tool_message := GalileoCallback._find_tool_message(output)) is not None:
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
        await self._end_node(run_id, **end_node_kwargs)

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
        node_type = "retriever"
        node_name = GalileoCallback._get_node_name(node_type, serialized, kwargs)
        await self._start_node(
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
        try:
            serialized_response = json.loads(json.dumps(documents, cls=EventSerializer))
        except Exception as e:
            _logger.warning(f"Failed to serialize retriever output: {e}")
            serialized_response = str(documents)

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
