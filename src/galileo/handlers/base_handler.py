import logging
import time
from datetime import datetime, timezone
from typing import Any, Callable, Optional
from uuid import UUID

from galileo import galileo_context
from galileo.logger import GalileoLogger
from galileo.schema.handlers import INTEGRATION, NODE_TYPE, Node
from galileo.schema.trace import TracesIngestRequest
from galileo.utils.serialization import convert_to_string_dict, serialize_to_str

_logger = logging.getLogger(__name__)


class GalileoBaseHandler:
    """
    Callback handler for logging traces to the Galileo platform.

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
    _root_node : Optional[Node]
        The root node of the trace, if any.
    _nodes : dict[str, Node]
        A dictionary of nodes, where the key is the run_id as a string and the value is the Node object.
    _integration : INTEGRATION
        The integration type, e.g., "langchain". This is used to identify the source of the trace.
    """

    def __init__(
        self,
        integration: INTEGRATION = "langchain",
        galileo_logger: Optional[GalileoLogger] = None,
        start_new_trace: bool = True,
        flush_on_chain_end: bool = True,
        ingestion_hook: Optional[Callable[[TracesIngestRequest], None]] = None,
    ):
        self._galileo_logger: GalileoLogger = galileo_logger or galileo_context.get_logger_instance()
        if ingestion_hook:
            self._galileo_logger._ingestion_hook = ingestion_hook
        self._start_new_trace: bool = start_new_trace
        self._flush_on_chain_end: bool = flush_on_chain_end
        self._nodes: dict[str, Node] = {}
        self._root_node: Optional[Node] = None
        self._integration: INTEGRATION = integration

    def commit(self) -> None:
        """Commit the nodes to the trace using the Galileo Logger. Optionally flush the trace."""
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
            self._galileo_logger.start_trace(
                input=serialize_to_str(root_node.span_params.get("input", "")), name=root_node.span_params.get("name")
            )

        self.log_node_tree(root_node)

        # Conclude the trace with the root node's output
        root_output = root_node.span_params.get("output", "")

        if self._start_new_trace:
            # If we started a new trace, we need to conclude it
            self._galileo_logger.conclude(
                output=serialize_to_str(root_output), status_code=root_node.span_params.get("status_code")
            )

        if self._flush_on_chain_end:
            self._galileo_logger.flush()

        # Clear nodes after successful commit
        self._nodes.clear()
        self._root_node = None

    def log_node_tree(self, node: Node) -> None:
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
        metadata = node.span_params.get("metadata", {})
        tags = node.span_params.get("tags")
        created_at = node.span_params.get("created_at")

        # Convert metadata to a dict[str, str]
        if metadata is not None:
            metadata = convert_to_string_dict(metadata)

        step_number = None
        if metadata and (metadata_step_number := metadata.get("langgraph_step")):
            try:
                step_number = int(metadata_step_number)
            except Exception as e:
                _logger.warning(f"Invalid step number: {metadata_step_number}, exception raised {e}")

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
                status_code=node.span_params.get("status_code"),
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
                status_code=node.span_params.get("status_code"),
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
                status_code=node.span_params.get("status_code"),
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
            tool_span = self._galileo_logger.add_tool_span(
                input=input_,
                output=output,
                name=name,
                duration_ns=node.span_params.get("duration_ns"),
                metadata=metadata,
                tags=tags,
                created_at=created_at,
                step_number=step_number,
                tool_call_id=node.span_params.get("tool_call_id"),
                status_code=node.span_params.get("status_code"),
            )
            # If tool has children (e.g., agent-as-tool invocations), push it to parent stack
            if node.children and tool_span is not None:
                parent_before_tool = self._galileo_logger.current_parent()
                tool_span._parent = parent_before_tool
                self._galileo_logger._set_current_parent(tool_span)
                is_span_with_children = True
        else:
            _logger.warning(f"Unknown node type: {node.node_type}")

        # Process all child nodes
        last_child = None
        for child_id in node.children:
            child_node = self._nodes.get(child_id)
            if child_node:
                self.log_node_tree(child_node)
                last_child = child_node
            else:
                _logger.warning(f"Child node {child_id} not found")

        # Conclude parent span. Use the last child's output if necessary
        if is_span_with_children:
            output = output or (last_child.span_params.get("output", "") if last_child else "")
            self._galileo_logger.conclude(
                output=serialize_to_str(output), status_code=node.span_params.get("status_code")
            )

    def start_node(self, node_type: NODE_TYPE, parent_run_id: Optional[UUID], run_id: UUID, **kwargs: Any) -> Node:
        """
        Start a new node in the chain.

        Parameters
        ----------
        node_type : NODE_TYPE
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

        found_node = self._nodes.get(node_id)
        if found_node:
            _logger.debug(f"Node already exists for run_id {run_id}, overwriting...")
            self._nodes[node_id].span_params.update(**kwargs)
            self._nodes[node_id].children.extend(node.children)
            return found_node

        self._nodes[node_id] = node

        # Set as root node if needed
        if not self._root_node:
            _logger.debug(f"Setting root node to {node_id}")
            self._root_node = node

        # Add to parent's children if parent exists
        if parent_run_id:
            parent = self._nodes.get(str(parent_run_id))
            if parent:
                parent.children.append(node_id)
            else:
                _logger.debug(f"Parent node {parent_node_id} not found for {node_id}")

        return node

    def end_node(self, run_id: UUID, **kwargs: Any) -> None:
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
            self.commit()

    def get_node(self, run_id: UUID) -> Optional[Node]:
        """
        Get a node by its run ID.

        Parameters
        ----------
        run_id : UUID
            The run ID of the node to retrieve.

        Returns
        -------
        Optional[Node]
            The node if found, otherwise None.
        """
        return self._nodes.get(str(run_id))

    def get_nodes(self) -> dict[str, Node]:
        """
        Get all nodes.

        Returns
        -------
        dict[str, Node]
            A dictionary of all nodes.
        """
        return self._nodes
