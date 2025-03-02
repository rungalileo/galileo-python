import contextvars
import json
import logging
import time
from typing import Any, Literal, Optional
from uuid import UUID

from galileo import galileo_context
from galileo.logger import GalileoLogger
from galileo.utils.serialization import EventSerializer, serialize_to_str

_logger = logging.getLogger("galileo.handlers.langchain")

try:
    from langchain.callbacks.base import BaseCallbackHandler
    from langchain.schema import Document
    from langchain.schema.agent import AgentAction
    from langchain.schema.messages import BaseMessage
    from langchain.schema.output import LLMResult
    from langchain_core.agents import AgentFinish
except ImportError:
    _logger.warning("Failed to import langchain, using stubs")
    BaseCallbackHandler = object
    Document = object
    AgentAction = object
    BaseMessage = object
    LLMResult = object
    AgentFinish = object


SPAN_TYPE = Literal["llm", "retriever", "tool", "workflow"]

LANGCHAIN_NODE_TYPE = Literal["agent", "chain", "chat", "llm", "retriever", "tool"]


class Node:
    """
    A node in the Langchain trace.

    Attributes
    ----------
    node_type : LANGCHAIN_NODE_TYPE
        The type of node.
    span_params : Optional[dict[str, str]]
        The parameters for the span that will be created.
    run_id : UUID
        The run ID of the span.
    parent_run_id : Optional[UUID]
        The run ID of the parent span.
    """

    node_type: LANGCHAIN_NODE_TYPE
    span_params: Optional[dict[str, str]]
    run_id: UUID
    parent_run_id: Optional[UUID]

    def __init__(
        self,
        node_type: LANGCHAIN_NODE_TYPE,
        span_params: Optional[dict[str, str]],
        run_id: UUID,
        parent_run_id: Optional[UUID] = None,
    ) -> None:
        self.node_type = node_type
        self.span_params = span_params
        self.run_id = run_id
        self.parent_run_id = parent_run_id


_root_node: contextvars.ContextVar[Optional[Node]] = contextvars.ContextVar("langchain_root_node", default=None)


class GalileoCallback(BaseCallbackHandler):
    """
    Langchain callback handler for logging traces to Galileo.

    Attributes
    ----------
    _galileo_logger : GalileoLogger
        The Galileo logger instance.
    _nodes : dict[UUID, Node]
        A dictionary of nodes, where the key is the run_id and the value is the node.
    _start_new_trace : bool
        Whether to start a new trace when a chain starts.
    _flush_on_chain_end : bool
        Whether to flush the trace when a chain ends.
    """

    _galileo_logger: GalileoLogger
    _nodes: dict[UUID, Node]

    def __init__(
        self,
        galileo_logger: Optional[GalileoLogger] = None,
        start_new_trace: bool = True,
        flush_on_chain_end: bool = True,
    ):
        self._galileo_logger = galileo_logger or galileo_context.get_logger_instance()
        self._start_new_trace = start_new_trace
        self._flush_on_chain_end = flush_on_chain_end
        self._nodes: dict[UUID, Node] = {}

    def _commit(self) -> None:
        """
        Commit the nodes to the trace using the Galileo Logger. Optionally flush the trace.
        """

        if not self._nodes:
            return

        root_node = self._nodes.get(_root_node.get().run_id)

        if root_node is None:
            _logger.warning("Unable to add nodes to trace: Root node does not exist")
            return

        # Create a mapping of parent run IDs to child nodes
        parent_child_mapping: dict[UUID, list[UUID]] = {}
        for _, node in self._nodes.items():
            if node.parent_run_id is not None:
                parent_child_mapping.setdefault(node.parent_run_id, []).append(node)

        def recursive_log(node: Node) -> Node:
            """
            Recursively logs a node and its children as spans in the Galileo Logger.

            Parameters
            ----------
            node : Node
                The node to log.

            Returns
            -------
            Node
                The logged node.
            """
            is_workflow_span = False
            if node.node_type == "agent" or node.node_type == "chain":
                self._galileo_logger.add_workflow_span(
                    input=node.span_params.get("input", ""),
                    output=node.span_params.get("output", ""),
                    name=node.span_params.get("name", None),
                    metadata=node.span_params.get("metadata", None),
                    tags=node.span_params.get("tags", None),
                )
                is_workflow_span = True
            elif node.node_type == "llm" or node.node_type == "chat":
                self._galileo_logger.add_llm_span(
                    input=node.span_params.get("input", ""),
                    output=node.span_params.get("output", ""),
                    model=node.span_params.get("model", None),
                    temperature=node.span_params.get("temperature", None),
                    name=node.span_params.get("name", None),
                    metadata=node.span_params.get("metadata", None),
                    tags=node.span_params.get("tags", None),
                    num_input_tokens=node.span_params.get("num_input_tokens", None),
                    num_output_tokens=node.span_params.get("num_output_tokens", None),
                    total_tokens=node.span_params.get("total_tokens", None),
                    time_to_first_token_ns=node.span_params.get("time_to_first_token_ns", None),
                )
            elif node.node_type == "retriever":
                self._galileo_logger.add_retriever_span(
                    input=node.span_params.get("input", ""),
                    output=node.span_params.get("output", ""),
                    name=node.span_params.get("name", None),
                    metadata=node.span_params.get("metadata", None),
                    tags=node.span_params.get("tags", None),
                )
            elif node.node_type == "tool":
                self._galileo_logger.add_tool_span(
                    input=node.span_params.get("input", ""),
                    output=node.span_params.get("output", ""),
                    name=node.span_params.get("name", None),
                    metadata=node.span_params.get("metadata", None),
                    tags=node.span_params.get("tags", None),
                )
            else:
                _logger.warning(f"Unknown node type: {node.node_type}")

            node = None
            for child in parent_child_mapping.get(node.run_id, []):
                node = recursive_log(child)

            if is_workflow_span:
                self._galileo_logger.conclude(
                    output=serialize_to_str(node.span_params.get("output", "") if node else "")
                )

            return node

        node = recursive_log(root_node)

        # Conclude the trace
        self._galileo_logger.conclude(output=serialize_to_str(node.span_params.get("output", "") if node else ""))

        if self._flush_on_chain_end:
            # Upload the trace to Galileo
            self._galileo_logger.flush()

    def _start_node(self, node_type: LANGCHAIN_NODE_TYPE, parent_run_id: UUID, run_id: UUID, **kwargs: Any) -> Any:
        """Start a new node in the chain."""
        assert run_id not in self._nodes, f"Node already exists for run_id {run_id}"

        node = Node(node_type=node_type, span_params=kwargs, run_id=run_id, parent_run_id=parent_run_id)

        if not _root_node.get():
            _root_node.set(node)

        self._nodes[run_id] = node
        return node

    def _end_node(self, run_id, **kwargs: Any) -> Any:
        """
        End a node in the chain. Commit the nodes to a trace if the run_id matches the root node.
        """

        assert run_id in self._nodes, f"No node exists for run_id {run_id}"
        node = self._nodes.get(run_id, None)
        if node is None:
            return

        node.span_params.update(**kwargs)

        if node.run_id == _root_node.get().run_id:
            self._commit()

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
        node_type = "chain"
        node_name = kwargs.get("name", "Chain")

        # If the `name` is `LangGraph` or `agent`, set the node type to `agent`.
        if node_name in ["LangGraph", "agent"]:
            node_type = "agent"
            node_name = "agent"

        # If the node is tagged with `hidden`, don't log it.
        if tags and "langsmith:hidden" in tags:
            return

        self._start_node(node_type, parent_run_id, run_id, name=node_name, input=inputs, tags=tags, **kwargs)

    def on_chain_end(
        self, outputs: dict[str, Any], *, run_id: UUID, parent_run_id: Optional[UUID] = None, **kwargs: Any
    ) -> Any:
        """Langchain callback when a chain ends."""
        self._end_node(run_id, output=outputs)

    def on_agent_finish(self, finish: AgentFinish, *, run_id: UUID, **kwargs: Any) -> Any:
        """Langchain callback when an agent finishes."""
        self._end_node(run_id, output=serialize_to_str(finish))

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
        """Langchain callback when an LLM node starts."""
        invocation_params = kwargs.get("invocation_params", {})
        model = invocation_params.get("model_name", "")
        temperature = invocation_params.get("temperature", 0.0)
        self._start_node(
            "llm",
            parent_run_id,
            run_id,
            name="LLM",
            input=prompts,
            tags=tags,
            model=model,
            temperature=temperature,
            metadata=metadata,
            start_time=time.perf_counter(),
        )

    def on_llm_new_token(self, token: str, run_id: UUID, **kwargs: Any) -> Any:
        """Langchain callback when an LLM node generates a new token."""
        node = self._nodes.get(run_id, None)
        if node is None:
            return

        if node.span_params["time_to_first_token_ns"] is None and node.span_params["start_time"] is not None:
            node.span_params["time_to_first_token_ns"] = (time.perf_counter() - node.span_params["start_time"]) * 1e9
            self._nodes[run_id] = node

    def on_chat_model_start(
        self,
        serialized: dict[str, Any],
        messages: list[list[BaseMessage]],
        *,
        run_id: UUID,
        parent_run_id: Optional[UUID] = None,
        invocation_params: Optional[dict[str, Any]] = None,
        tags: Optional[list[str]] = None,
        metadata: Optional[dict[str, Any]] = None,
        **kwargs: Any,
    ) -> Any:
        """Langchain callback when a chat model starts."""
        invocation_params = kwargs.get("invocation_params", {})
        model = invocation_params.get("model", invocation_params.get("_type", "undefined-type"))
        temperature = invocation_params.get("temperature", 0.0)
        self._start_node(
            "chat",
            parent_run_id,
            run_id,
            name="Chat Model",
            input=json.loads(json.dumps([[m.dict() for m in batch] for batch in messages], cls=EventSerializer)),
            tags=tags,
            model=model,
            temperature=temperature,
            metadata=metadata,
        )

    def on_llm_end(
        self, response: LLMResult, *, run_id: UUID, parent_run_id: Optional[UUID] = None, **kwargs: Any
    ) -> Any:
        """Langchain callback when an LLM node ends."""
        token_usage = response.llm_output.get("token_usage", {})
        self._end_node(
            run_id,
            output=[[m.dict() for m in batch] for batch in response.generations],
            num_input_tokens=token_usage.get("prompt_tokens", None),
            num_output_tokens=token_usage.get("completion_tokens", None),
            total_tokens=token_usage.get("total_tokens", None),
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
        self._start_node("tool", parent_run_id, run_id, name="Tool", input=input_str, tags=tags, metadata=metadata)

    def on_tool_end(self, output: str, *, run_id: UUID, parent_run_id: Optional[UUID] = None, **kwargs: Any) -> Any:
        """Langchain callback when a tool node ends."""
        self._end_node(run_id, output=serialize_to_str(output))

    def on_retriever_start(
        self, query: str, *, run_id: UUID, parent_run_id: Optional[UUID] = None, **kwargs: Any
    ) -> Any:
        """Langchain callback when a retriever node starts."""
        self._start_node("retriever", parent_run_id, run_id, name="Retriever", input=serialize_to_str(query))

    def on_retriever_end(
        self, response: list[Document], *, run_id: UUID, parent_run_id: Optional[UUID] = None, **kwargs: Any
    ) -> Any:
        """Langchain callback when a retriever node ends."""
        self._end_node(run_id, output=json.loads(json.dumps(response, cls=EventSerializer)))
