import hashlib
import json
import logging
from datetime import datetime
from typing import Any, Optional
from uuid import UUID

from galileo.handlers.base_handler import GalileoBaseHandler
from galileo.logger import GalileoLogger
from galileo.schema.handlers import NODE_TYPE
from galileo.utils.serialization import serialize_to_str

_logger = logging.getLogger(__name__)

try:
    from crewai.utilities.events.agent_events import (
        AgentExecutionCompletedEvent,
        AgentExecutionErrorEvent,
        AgentExecutionStartedEvent,
    )
    from crewai.utilities.events.base_event_listener import BaseEventListener
    from crewai.utilities.events.crew_events import (
        CrewKickoffCompletedEvent,
        CrewKickoffFailedEvent,
        CrewKickoffStartedEvent,
    )
    from crewai.utilities.events.llm_events import LLMCallCompletedEvent, LLMCallFailedEvent, LLMCallStartedEvent
    from crewai.utilities.events.task_events import TaskCompletedEvent, TaskFailedEvent, TaskStartedEvent
    from crewai.utilities.events.tool_usage_events import (
        ToolUsageErrorEvent,
        ToolUsageFinishedEvent,
        ToolUsageStartedEvent,
    )

    CREWAI_AVAILABLE = True
except ImportError:
    _logger.warning("CrewAI not available, using stubs")
    BaseEventListener = object
    CrewKickoffStartedEvent = object
    CrewKickoffCompletedEvent = object
    CrewKickoffFailedEvent = object
    AgentExecutionStartedEvent = object
    AgentExecutionCompletedEvent = object
    AgentExecutionErrorEvent = object
    TaskStartedEvent = object
    TaskCompletedEvent = object
    TaskFailedEvent = object
    ToolUsageStartedEvent = object
    ToolUsageFinishedEvent = object
    ToolUsageErrorEvent = object
    LLMCallStartedEvent = object
    LLMCallCompletedEvent = object
    LLMCallFailedEvent = object

    CREWAI_AVAILABLE = False

try:
    import litellm

    LITE_LLM_AVAILABLE = True
except ImportError:
    _logger.warning("LiteLLM not available, using stubs")
    litellm = None
    LITE_LLM_AVAILABLE = False


class CrewAICallback(BaseEventListener):
    """
    CrewAI event listener for logging traces to the Galileo platform.

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
            integration="crewai",
        )

        # Only call super().__init__() if CrewAI is available
        if CREWAI_AVAILABLE:
            super().__init__()

        if LITE_LLM_AVAILABLE and litellm is not None:
            if not litellm.success_callback:
                litellm.success_callback = []
            litellm.success_callback.append(self.lite_llm_usage_callback)

    def setup_listeners(self, crewai_event_bus: Any) -> None:
        """Setup event listeners for CrewAI events."""
        if not CREWAI_AVAILABLE:
            _logger.warning("CrewAI not available, skipping event listener setup")
            return

        # Crew event handlers
        @crewai_event_bus.on(CrewKickoffStartedEvent)
        def on_crew_kickoff_started(source: Any, event: Any) -> None:
            self._handle_crew_kickoff_started(source, event)

        @crewai_event_bus.on(CrewKickoffCompletedEvent)
        def on_crew_kickoff_completed(source: Any, event: Any) -> None:
            self._handle_crew_kickoff_completed(source, event)

        @crewai_event_bus.on(CrewKickoffFailedEvent)
        def on_crew_kickoff_failed(source: Any, event: Any) -> None:
            self._handle_crew_kickoff_failed(source, event)

        # Agent event handlers
        @crewai_event_bus.on(AgentExecutionStartedEvent)
        def on_agent_execution_started(source: Any, event: Any) -> None:
            self._handle_agent_execution_started(source, event)

        @crewai_event_bus.on(AgentExecutionCompletedEvent)
        def on_agent_execution_completed(source: Any, event: Any) -> None:
            self._handle_agent_execution_completed(source, event)

        @crewai_event_bus.on(AgentExecutionErrorEvent)
        def on_agent_execution_error(source: Any, event: Any) -> None:
            self._handle_agent_execution_error(source, event)

        # Task event handlers
        @crewai_event_bus.on(TaskStartedEvent)
        def on_task_started(source: Any, event: Any) -> None:
            self._handle_task_started(source, event)

        @crewai_event_bus.on(TaskCompletedEvent)
        def on_task_completed(source: Any, event: Any) -> None:
            self._handle_task_completed(source, event)

        @crewai_event_bus.on(TaskFailedEvent)
        def on_task_failed(source: Any, event: Any) -> None:
            self._handle_task_failed(source, event)

        # Tool event handlers
        @crewai_event_bus.on(ToolUsageStartedEvent)
        def on_tool_usage_started(source: Any, event: Any) -> None:
            self._handle_tool_usage_started(source, event)

        @crewai_event_bus.on(ToolUsageFinishedEvent)
        def on_tool_usage_finished(source: Any, event: Any) -> None:
            self._handle_tool_usage_finished(source, event)

        @crewai_event_bus.on(ToolUsageErrorEvent)
        def on_tool_usage_error(source: Any, event: Any) -> None:
            self._handle_tool_usage_error(source, event)

        # LLM event handlers
        @crewai_event_bus.on(LLMCallStartedEvent)
        def on_llm_call_started(source: Any, event: Any) -> None:
            self._handle_llm_call_started(source, event)

        @crewai_event_bus.on(LLMCallCompletedEvent)
        def on_llm_call_completed(source: Any, event: Any) -> None:
            self._handle_llm_call_completed(source, event)

        @crewai_event_bus.on(LLMCallFailedEvent)
        def on_llm_call_failed(source: Any, event: Any) -> None:
            self._handle_llm_call_failed(source, event)

    def _generate_run_id(self, source: Any, event: Any) -> UUID:
        """Generate a consistent UUID for event tracing."""
        if hasattr(source, "id") and source.id:
            return source.id

        if hasattr(event, "messages"):
            messages = json.dumps(event.to_json().get("messages", []))
            hash_obj = hashlib.md5(messages.encode())
            digest = hash_obj.hexdigest()
            return UUID(digest)

        if hasattr(event, "tool_args"):
            # tool_args might be a dict or JSON string
            if isinstance(event.tool_args, str):
                tool_args = event.tool_args
            else:
                # Convert dict to JSON string
                if isinstance(event.tool_args, dict):
                    tool_args = json.dumps(event.tool_args)
                else:
                    tool_args = str(event.tool_args)
            hash_obj = hashlib.md5(tool_args.encode())
            digest = hash_obj.hexdigest()
            return UUID(digest)

        if isinstance(event, dict) and "messages" in event:
            # If event is a string, use it directly
            messages = json.dumps(event["messages"])
            hash_obj = hashlib.md5(messages.encode())
            digest = hash_obj.hexdigest()
            return UUID(digest)

        # Fallback to generating a UUID based on event properties
        source_str = f"{getattr(event, 'crew_name', '')}_{getattr(event, 'agent', '')}_{getattr(event, 'task', '')}"
        hash_obj = hashlib.md5(source_str.encode())
        digest = hash_obj.hexdigest()
        return UUID(digest)

    def _extract_metadata(self, event: Any) -> dict:
        """Extract metadata from event for span attributes."""
        metadata = {}

        # Add timestamp
        metadata["timestamp"] = event.timestamp.isoformat()
        metadata["event_type"] = event.type

        # Add source information
        if hasattr(event, "source_type") and event.source_type:
            metadata["source_type"] = event.source_type

        if hasattr(event, "fingerprint_metadata") and event.fingerprint_metadata:
            metadata.update(event.fingerprint_metadata)

        return metadata

    # Crew event handlers
    def _handle_crew_kickoff_started(self, source: Any, event: Any) -> None:
        """Handle crew execution start."""
        run_id = self._generate_run_id(source, event)
        node_type: NODE_TYPE = "chain"
        crew_name = event.crew_name if hasattr(event, "crew_name") else "Crew"

        metadata = self._extract_metadata(event)
        metadata["crew_name"] = crew_name

        input = getattr(event, "inputs", {})

        self._handler.start_node(
            node_type=node_type,
            parent_run_id=None,  # Root node
            run_id=run_id,
            name=crew_name,
            input=serialize_to_str(input) if input else "-",
            metadata=metadata,
            event_type=event.type,
        )

    def _update_crew_input(self, run_id: str) -> None:
        """Update crew input with task descriptions. if input is not set."""
        nodes = self._handler.get_nodes()
        root_node = nodes.get(str(run_id))
        if not root_node:
            return

        input = root_node.span_params.get("input", "-")
        tasks = ""

        if not input or input == "-":
            tasks = ", ".join(
                [
                    str(node.span_params.get("metadata", {}).get("task_description"))
                    for node in nodes.values()
                    if node.span_params.get("metadata", {}).get("task_description")
                ]
            )
            input = f"Tasks: {tasks}" if tasks else "-"
            root_node.span_params["input"] = input

    def _handle_crew_kickoff_completed(self, source: Any, event: Any) -> None:
        """Handle crew execution completion."""
        run_id = self._generate_run_id(source, event)
        output = getattr(event, "output", {})
        self._update_crew_input(str(run_id))
        self._handler.end_node(
            run_id=run_id, output=serialize_to_str(getattr(output, "raw", output)), event_type=event.type
        )

    def _handle_crew_kickoff_failed(self, source: Any, event: Any) -> None:
        """Handle crew execution failure."""
        run_id = self._generate_run_id(source, event)
        metadata = self._extract_metadata(event)
        metadata["error"] = event.error

        self._handler.end_node(run_id=run_id, output=f"Error: {event.error}", metadata=metadata, event_type=event.type)

    # Agent event handlers
    def _handle_agent_execution_started(self, source: Any, event: Any) -> None:
        """Handle agent execution start."""
        run_id = self._generate_run_id(source, event)
        parent_run_id = event.task.id
        node_type: NODE_TYPE = "agent"
        role = "Unknown Agent"
        metadata = self._extract_metadata(event)

        if hasattr(event, "agent") and event.agent:
            if hasattr(event.agent, "role"):
                role = event.agent.role
                metadata["agent_role"] = role
            if hasattr(event.agent, "id"):
                metadata["agent_id"] = str(event.agent.id)

        if hasattr(event, "tools") and event.tools:
            metadata["available_tools"] = [str(getattr(tool, "name", tool)) for tool in event.tools]

        self._handler.start_node(
            node_type=node_type,
            parent_run_id=parent_run_id,
            run_id=run_id,
            name=role,
            input=serialize_to_str(getattr(event, "task_prompt", "-")),
            metadata=metadata,
            event_type=event.type,
        )

    def _handle_agent_execution_completed(self, source: Any, event: Any) -> None:
        """Handle agent execution completion."""
        run_id = self._generate_run_id(source, event)
        self._handler.end_node(
            run_id=run_id, output=serialize_to_str(getattr(event, "output", "")), event_type=event.type
        )

    def _handle_agent_execution_error(self, source: Any, event: Any) -> None:
        """Handle agent execution error."""
        run_id = self._generate_run_id(source, event)
        metadata = self._extract_metadata(event)
        metadata["error"] = getattr(event, "error", "Unknown error")

        self._handler.end_node(
            run_id=run_id,
            output=f"Error: {getattr(event, 'error', 'Unknown error')}",
            metadata=metadata,
            event_type=event.type,
        )

    # Task event handlers
    def _handle_task_started(self, source: Any, event: Any) -> None:
        """Handle task start."""
        run_id = self._generate_run_id(source, event)
        parent_run_id = event.task.agent.crew.id
        node_type: NODE_TYPE = "chain"

        metadata = self._extract_metadata(event)
        if hasattr(event, "task") and event.task:
            if hasattr(event.task, "description"):
                metadata["task_description"] = event.task.description
            if hasattr(event.task, "id"):
                metadata["task_id"] = str(event.task.id)

        task_name = "Unknown Task"
        if hasattr(event, "task") and event.task and hasattr(event.task, "description"):
            # Use first 50 chars of description as name
            task_name = (
                event.task.description[:50] + "..." if len(event.task.description) > 50 else event.task.description
            )

        input = getattr(event, "context", "")
        if not input:
            input = event.task.description if hasattr(event.task, "description") else ""

        self._handler.start_node(
            node_type=node_type,
            parent_run_id=parent_run_id,
            run_id=run_id,
            name=task_name,
            input=serialize_to_str(input) if input else "-",
            metadata=metadata,
            event_type=event.type,
        )

    def _handle_task_completed(self, source: Any, event: Any) -> None:
        """Handle task completion."""
        run_id = self._generate_run_id(source, event)
        output = ""
        if hasattr(event, "output") and event.output:
            if hasattr(event.output, "raw"):
                output = event.output.raw
            else:
                output = str(event.output)

        self._handler.end_node(run_id=run_id, output=serialize_to_str(output), event_type=event.type)

    def _handle_task_failed(self, source: Any, event: Any) -> None:
        """Handle task failure."""
        run_id = self._generate_run_id(source, event)
        metadata = self._extract_metadata(event)
        metadata["error"] = event.error

        self._handler.end_node(run_id=run_id, output=f"Error: {event.error}", metadata=metadata, event_type=event.type)

    # Tool event handlers
    def _handle_tool_usage_started(self, source: Any, event: Any) -> None:
        """Handle tool usage start."""
        run_id = self._generate_run_id(source, event)
        parent_run_id = event.agent.id
        node_type: NODE_TYPE = "tool"
        input = getattr(event, "tool_args", {})
        tool_name = getattr(event, "tool_name", "Unknown Tool")

        metadata = self._extract_metadata(event)
        metadata["tool_name"] = tool_name
        if input:
            metadata["tool_args"] = str(input)

        self._handler.start_node(
            node_type=node_type,
            parent_run_id=parent_run_id,
            run_id=run_id,
            name=tool_name,
            input=serialize_to_str(input) if input else "-",
            metadata=metadata,
            event_type=event.type,
        )

    def _handle_tool_usage_finished(self, source: Any, event: Any) -> None:
        """Handle tool usage completion."""
        run_id = self._generate_run_id(source, event)
        self._handler.end_node(
            run_id=run_id, output=serialize_to_str(getattr(event, "output", "")), event_type=event.type
        )

    def _handle_tool_usage_error(self, source: Any, event: Any) -> None:
        """Handle tool usage error."""
        run_id = self._generate_run_id(source, event)
        metadata = self._extract_metadata(event)
        metadata["error"] = getattr(event, "error", "Unknown error")

        self._handler.end_node(
            run_id=run_id,
            output=f"Error: {getattr(event, 'error', 'Unknown error')}",
            metadata=metadata,
            event_type=event.type,
        )

    # LLM event handlers
    def _handle_llm_call_started(self, source: Any, event: Any) -> None:
        """Handle LLM call start."""
        run_id = self._generate_run_id(source, event)
        parent_run_id = event.agent_id if hasattr(event, "agent_id") else None
        node_type: NODE_TYPE = "llm"
        llm_name = getattr(source, "model", "Unknown Model")

        metadata = self._extract_metadata(event)
        metadata["model"] = llm_name
        if hasattr(source, "temperature"):
            metadata["temperature"] = str(source.temperature)

        self._handler.start_node(
            node_type=node_type,
            parent_run_id=parent_run_id,
            run_id=run_id,
            name=llm_name,
            input=serialize_to_str(getattr(event, "messages", [])),
            model=llm_name,
            temperature=getattr(source, "temperature", None),
            metadata=metadata,
            event_type=event.type,
        )

    def _handle_llm_call_completed(self, source: Any, event: Any) -> None:
        """Handle LLM call completion."""
        run_id = self._generate_run_id(source, event)

        self._handler.end_node(
            run_id=run_id, output=serialize_to_str(getattr(event, "response", "")), event_type=event.type
        )

    def _handle_llm_call_failed(self, source: Any, event: Any) -> None:
        """Handle LLM call failure."""
        run_id = self._generate_run_id(source, event)
        metadata = self._extract_metadata(event)
        metadata["error"] = getattr(event, "error", "Unknown error")

        self._handler.end_node(
            run_id=run_id,
            output=f"Error: {getattr(event, 'error', 'Unknown error')}",
            metadata=metadata,
            event_type=event.type,
        )

    def lite_llm_usage_callback(
        self,
        kwargs: dict,  # kwargs to completion
        completion_response: Any,  # response from completion
        start_time: datetime,
        end_time: datetime,
    ) -> None:
        node_id = self._generate_run_id(kwargs, kwargs)

        node = self._handler.get_node(node_id)
        if not node:
            _logger.debug(f"No node exists for run_id {node_id}")
            return
        usage = completion_response.model_extra["usage"]
        node.span_params["usage"] = usage.model_dump() if hasattr(usage, "model_dump") else usage
        node.span_params["num_input_tokens"] = getattr(usage, "prompt_tokens", 0)
        node.span_params["num_output_tokens"] = getattr(usage, "completion_tokens", 0)
        node.span_params["total_tokens"] = getattr(usage, "total_tokens", 0)
