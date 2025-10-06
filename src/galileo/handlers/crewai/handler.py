import hashlib
import json
import logging
from datetime import datetime
from typing import Any, Optional, Union
from uuid import UUID

from packaging.version import Version

from galileo.handlers.base_handler import GalileoBaseHandler
from galileo.logger import GalileoLogger
from galileo.schema.handlers import NodeType
from galileo.utils.serialization import serialize_to_str

_logger = logging.getLogger(__name__)

try:
    from crewai import __version__ as CREWAI_VERSION

    CREWAI_VERSION = Version(CREWAI_VERSION)
    CREWAI_EVENTS_MODULE_AVAILABLE = Version("0.177.0") <= CREWAI_VERSION
    if CREWAI_EVENTS_MODULE_AVAILABLE:
        from crewai.events.base_event_listener import BaseEventListener
        from crewai.events.types.agent_events import (  # pyright: ignore[reportMissingImports]
            AgentExecutionCompletedEvent,
            AgentExecutionErrorEvent,
            AgentExecutionStartedEvent,
        )
        from crewai.events.types.crew_events import (  # pyright: ignore[reportMissingImports]
            CrewKickoffCompletedEvent,
            CrewKickoffFailedEvent,
            CrewKickoffStartedEvent,
        )
        from crewai.events.types.llm_events import (  # pyright: ignore[reportMissingImports]
            LLMCallCompletedEvent,
            LLMCallFailedEvent,
            LLMCallStartedEvent,
        )
        from crewai.events.types.memory_events import (  # pyright: ignore[reportMissingImports]
            MemoryQueryCompletedEvent,
            MemoryQueryFailedEvent,
            MemoryQueryStartedEvent,
            MemoryRetrievalCompletedEvent,
            MemoryRetrievalStartedEvent,
            MemorySaveCompletedEvent,
            MemorySaveFailedEvent,
            MemorySaveStartedEvent,
        )
        from crewai.events.types.task_events import (  # pyright: ignore[reportMissingImports]
            TaskCompletedEvent,
            TaskFailedEvent,
            TaskStartedEvent,
        )
        from crewai.events.types.tool_usage_events import (  # pyright: ignore[reportMissingImports]
            ToolUsageErrorEvent,
            ToolUsageFinishedEvent,
            ToolUsageStartedEvent,
        )
    else:
        from crewai.utilities.events.agent_events import (  # pyright: ignore[reportMissingImports]
            AgentExecutionCompletedEvent,
            AgentExecutionErrorEvent,
            AgentExecutionStartedEvent,
        )
        from crewai.utilities.events.base_event_listener import BaseEventListener
        from crewai.utilities.events.crew_events import (  # pyright: ignore[reportMissingImports]
            CrewKickoffCompletedEvent,
            CrewKickoffFailedEvent,
            CrewKickoffStartedEvent,
        )
        from crewai.utilities.events.llm_events import (  # pyright: ignore[reportMissingImports]
            LLMCallCompletedEvent,
            LLMCallFailedEvent,
            LLMCallStartedEvent,
        )
        from crewai.utilities.events.memory_events import (  # pyright: ignore[reportMissingImports]
            MemoryQueryCompletedEvent,
            MemoryQueryFailedEvent,
            MemoryQueryStartedEvent,
            MemoryRetrievalCompletedEvent,
            MemoryRetrievalStartedEvent,
            MemorySaveCompletedEvent,
            MemorySaveFailedEvent,
            MemorySaveStartedEvent,
        )
        from crewai.utilities.events.task_events import (  # pyright: ignore[reportMissingImports]
            TaskCompletedEvent,
            TaskFailedEvent,
            TaskStartedEvent,
        )
        from crewai.utilities.events.tool_usage_events import (  # pyright: ignore[reportMissingImports]
            ToolUsageErrorEvent,
            ToolUsageFinishedEvent,
            ToolUsageStartedEvent,
        )

        CREWAI_EVENTS_MODULE_AVAILABLE = False

    CREWAI_AVAILABLE = True

except ImportError:
    _logger.warning("CrewAI not available, using stubs")

    BaseEventListener = object

    CREWAI_AVAILABLE = False
    CREWAI_EVENTS_MODULE_AVAILABLE = False

try:
    import litellm

    LITE_LLM_AVAILABLE = True
except ImportError:
    _logger.warning("LiteLLM not available, using stubs")
    litellm = None
    LITE_LLM_AVAILABLE = False


class CrewAIEventListener(BaseEventListener):  # pyright: ignore[reportGeneralTypeIssues]
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
        flush_on_crew_completed: bool = True,
    ):
        self._handler = GalileoBaseHandler(
            flush_on_chain_end=flush_on_crew_completed,
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
        def on_crew_kickoff_started(source: Any, event: CrewKickoffStartedEvent) -> None:
            self._handle_crew_kickoff_started(source, event)

        @crewai_event_bus.on(CrewKickoffCompletedEvent)
        def on_crew_kickoff_completed(source: Any, event: CrewKickoffCompletedEvent) -> None:
            self._handle_crew_kickoff_completed(source, event)

        @crewai_event_bus.on(CrewKickoffFailedEvent)
        def on_crew_kickoff_failed(source: Any, event: CrewKickoffFailedEvent) -> None:
            self._handle_crew_kickoff_failed(source, event)

        # Agent event handlers
        @crewai_event_bus.on(AgentExecutionStartedEvent)
        def on_agent_execution_started(source: Any, event: AgentExecutionStartedEvent) -> None:
            self._handle_agent_execution_started(source, event)

        @crewai_event_bus.on(AgentExecutionCompletedEvent)
        def on_agent_execution_completed(source: Any, event: AgentExecutionCompletedEvent) -> None:
            self._handle_agent_execution_completed(source, event)

        @crewai_event_bus.on(AgentExecutionErrorEvent)
        def on_agent_execution_error(source: Any, event: AgentExecutionErrorEvent) -> None:
            self._handle_agent_execution_error(source, event)

        # Task event handlers
        @crewai_event_bus.on(TaskStartedEvent)
        def on_task_started(source: Any, event: TaskStartedEvent) -> None:
            self._handle_task_started(source, event)

        @crewai_event_bus.on(TaskCompletedEvent)
        def on_task_completed(source: Any, event: TaskCompletedEvent) -> None:
            self._handle_task_completed(source, event)

        @crewai_event_bus.on(TaskFailedEvent)
        def on_task_failed(source: Any, event: TaskFailedEvent) -> None:
            self._handle_task_failed(source, event)

        # Tool event handlers
        @crewai_event_bus.on(ToolUsageStartedEvent)
        def on_tool_usage_started(source: Any, event: ToolUsageStartedEvent) -> None:
            self._handle_tool_usage_started(source, event)

        @crewai_event_bus.on(ToolUsageFinishedEvent)
        def on_tool_usage_finished(source: Any, event: ToolUsageFinishedEvent) -> None:
            self._handle_tool_usage_finished(source, event)

        @crewai_event_bus.on(ToolUsageErrorEvent)
        def on_tool_usage_error(source: Any, event: ToolUsageErrorEvent) -> None:
            self._handle_tool_usage_error(source, event)

        # LLM event handlers
        @crewai_event_bus.on(LLMCallStartedEvent)
        def on_llm_call_started(source: Any, event: LLMCallStartedEvent) -> None:
            self._handle_llm_call_started(source, event)

        @crewai_event_bus.on(LLMCallCompletedEvent)
        def on_llm_call_completed(source: Any, event: LLMCallCompletedEvent) -> None:
            self._handle_llm_call_completed(source, event)

        @crewai_event_bus.on(LLMCallFailedEvent)
        def on_llm_call_failed(source: Any, event: LLMCallFailedEvent) -> None:
            self._handle_llm_call_failed(source, event)

        # Memory event handlers (only available in CrewAI >= 0.177.0)
        if CREWAI_EVENTS_MODULE_AVAILABLE:

            @crewai_event_bus.on(MemoryQueryStartedEvent)
            def on_memory_query_started(source: Any, event: MemoryQueryStartedEvent) -> None:
                self._handle_memory_query_started(source, event)

            @crewai_event_bus.on(MemoryQueryCompletedEvent)
            def on_memory_query_completed(source: Any, event: MemoryQueryCompletedEvent) -> None:
                self._handle_memory_query_completed(source, event)

            @crewai_event_bus.on(MemoryQueryFailedEvent)
            def on_memory_query_failed(source: Any, event: MemoryQueryFailedEvent) -> None:
                self._handle_memory_query_failed(source, event)

            @crewai_event_bus.on(MemorySaveStartedEvent)
            def on_memory_save_started(source: Any, event: MemorySaveStartedEvent) -> None:
                self._handle_memory_save_started(source, event)

            @crewai_event_bus.on(MemorySaveCompletedEvent)
            def on_memory_save_completed(source: Any, event: MemorySaveCompletedEvent) -> None:
                self._handle_memory_save_completed(source, event)

            @crewai_event_bus.on(MemorySaveFailedEvent)
            def on_memory_save_failed(source: Any, event: MemorySaveFailedEvent) -> None:
                self._handle_memory_save_failed(source, event)

            @crewai_event_bus.on(MemoryRetrievalStartedEvent)
            def on_memory_retrieval_started(source: Any, event: MemoryRetrievalStartedEvent) -> None:
                self._handle_memory_retrieval_started(source, event)

            @crewai_event_bus.on(MemoryRetrievalCompletedEvent)
            def on_memory_retrieval_completed(source: Any, event: MemoryRetrievalCompletedEvent) -> None:
                self._handle_memory_retrieval_completed(source, event)

    def _generate_run_id(self, source: Any, event: Any) -> UUID:
        """Generate a consistent UUID for event tracing."""

        # Memory event specific ID generation
        if hasattr(event, "query"):  # Memory query events
            source_type = event.source_type if hasattr(event, "source_type") else ""
            query_str = f"memory_query_{event.query}_{source_type}_{getattr(event, 'agent_id', '')}_{getattr(event, 'limit', '')}_{getattr(event, 'score_threshold', '')}"
            hash_obj = hashlib.md5(query_str.encode())
            digest = hash_obj.hexdigest()
            return UUID(digest)

        if hasattr(event, "value") and getattr(event, "type", "").startswith("memory_save"):  # Memory save events
            save_str = f"memory_save_{getattr(event, 'agent_id', '')}_{getattr(event, 'task_id', '')}_{getattr(event, 'agent_role', '')}"
            hash_obj = hashlib.md5(save_str.encode())
            digest = hash_obj.hexdigest()
            return UUID(digest)

        if (
            hasattr(event, "memory_content") or getattr(event, "type", "") == "memory_retrieval_started"
        ):  # Memory retrieval events
            # Use consistent fields for all retrieval events (started/completed) - exclude memory_content to ensure same ID
            retrieval_str = f"memory_retrieval_{getattr(event, 'task_id', '')}_{getattr(event, 'agent_id', '')}"
            hash_obj = hashlib.md5(retrieval_str.encode())
            digest = hash_obj.hexdigest()
            return UUID(digest)

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
                tool_args = json.dumps(event.tool_args) if isinstance(event.tool_args, dict) else str(event.tool_args)
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
        metadata["timestamp"] = event.timestamp.isoformat()

        # Add source information
        if hasattr(event, "source_type") and event.source_type:
            metadata["source_type"] = event.source_type

        if hasattr(event, "fingerprint_metadata") and event.fingerprint_metadata:
            metadata.update(event.fingerprint_metadata)

        return metadata

    # Crew event handlers
    def _handle_crew_kickoff_started(self, source: Any, event: "CrewKickoffStartedEvent") -> None:
        """Handle crew execution start."""
        run_id = self._generate_run_id(source, event)
        crew_name = event.crew_name if hasattr(event, "crew_name") else "Crew"

        metadata = self._extract_metadata(event)
        metadata["crew_name"] = crew_name

        input = getattr(event, "inputs", {})

        self._handler.start_node(
            node_type=NodeType.CHAIN.value,
            parent_run_id=None,  # Root node
            run_id=run_id,
            name=crew_name,
            input=serialize_to_str(input) if input else "-",
            metadata=metadata,
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
            tasks = "\n".join(
                [
                    str(node.span_params.get("metadata", {}).get("task_description"))
                    for node in nodes.values()
                    if node.span_params.get("metadata", {}).get("task_description")
                ]
            )
            input = f"Tasks: {tasks}" if tasks else "-"
            root_node.span_params["input"] = input

    def _handle_crew_kickoff_completed(self, source: Any, event: "CrewKickoffCompletedEvent") -> None:
        """Handle crew execution completion."""
        run_id = self._generate_run_id(source, event)
        output = getattr(event, "output", {})
        self._update_crew_input(str(run_id))
        self._handler.end_node(run_id=run_id, output=serialize_to_str(getattr(output, "raw", output)))

    def _handle_crew_kickoff_failed(self, source: Any, event: "CrewKickoffFailedEvent") -> None:
        """Handle crew execution failure."""
        run_id = self._generate_run_id(source, event)
        metadata = self._extract_metadata(event)
        metadata["error"] = event.error

        self._handler.end_node(run_id=run_id, output=f"Error: {event.error}", metadata=metadata)

    # Agent event handlers
    def _handle_agent_execution_started(self, source: Any, event: "AgentExecutionStartedEvent") -> None:
        """Handle agent execution start."""
        run_id = self._generate_run_id(source, event)
        parent_run_id = self._to_uuid(event.task.id)
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
            node_type=NodeType.AGENT.value,
            parent_run_id=parent_run_id,
            run_id=run_id,
            name=role,
            input=serialize_to_str(getattr(event, "task_prompt", "-")),
            metadata=metadata,
        )

    def _handle_agent_execution_completed(self, source: Any, event: "AgentExecutionCompletedEvent") -> None:
        """Handle agent execution completion."""
        run_id = self._generate_run_id(source, event)
        self._handler.end_node(run_id=run_id, output=serialize_to_str(getattr(event, "output", "")))

    def _handle_agent_execution_error(self, source: Any, event: "AgentExecutionErrorEvent") -> None:
        """Handle agent execution error."""
        run_id = self._generate_run_id(source, event)
        metadata = self._extract_metadata(event)
        metadata["error"] = getattr(event, "error", "Unknown error")

        self._handler.end_node(
            run_id=run_id, output=f"Error: {getattr(event, 'error', 'Unknown error')}", metadata=metadata
        )

    # Task event handlers
    def _handle_task_started(self, source: Any, event: "TaskStartedEvent") -> None:
        """Handle task start."""
        run_id = self._generate_run_id(source, event)
        task = event.task if hasattr(event, "task") else None
        parent_run_id = self._to_uuid(task.agent.crew.id) if task else None

        metadata = self._extract_metadata(event)
        if task:
            if hasattr(task, "description"):
                metadata["task_description"] = task.description
            if hasattr(task, "id"):
                metadata["task_id"] = str(task.id)

        task_name = "Unknown Task"
        if task and hasattr(task, "description"):
            # Use first 50 chars of description as name
            task_name = task.description[:50] + "..." if len(task.description) > 50 else task.description

        input = getattr(event, "context", "")
        if not input:
            input = task.description if task and hasattr(task, "description") else ""

        self._handler.start_node(
            node_type=NodeType.CHAIN.value,
            parent_run_id=parent_run_id,
            run_id=run_id,
            name=task_name,
            input=serialize_to_str(input) if input else "-",
            metadata=metadata,
        )

    def _handle_task_completed(self, source: Any, event: "TaskCompletedEvent") -> None:
        """Handle task completion."""
        run_id = self._generate_run_id(source, event)
        output = ""
        if hasattr(event, "output") and event.output:
            output = event.output.raw if hasattr(event.output, "raw") else str(event.output)

        self._handler.end_node(run_id=run_id, output=serialize_to_str(output))

    def _handle_task_failed(self, source: Any, event: "TaskFailedEvent") -> None:
        """Handle task failure."""
        run_id = self._generate_run_id(source, event)
        metadata = self._extract_metadata(event)
        metadata["error"] = event.error

        self._handler.end_node(run_id=run_id, output=f"Error: {event.error}", metadata=metadata)

    # Tool event handlers
    def _handle_tool_usage_started(self, source: Any, event: "ToolUsageStartedEvent") -> None:
        """Handle tool usage start."""
        run_id = self._generate_run_id(source, event)
        parent_run_id = self._to_uuid(event.agent.id) if event.agent else None
        input = getattr(event, "tool_args", {})
        tool_name = getattr(event, "tool_name", "Unknown Tool")

        metadata = self._extract_metadata(event)
        metadata["tool_name"] = tool_name
        if input:
            metadata["tool_args"] = str(input)

        self._handler.start_node(
            node_type=NodeType.TOOL.value,
            parent_run_id=parent_run_id,
            run_id=run_id,
            name=tool_name,
            input=serialize_to_str(input) if input else "-",
            metadata=metadata,
        )

    def _handle_tool_usage_finished(self, source: Any, event: "ToolUsageFinishedEvent") -> None:
        """Handle tool usage completion."""
        run_id = self._generate_run_id(source, event)
        self._handler.end_node(run_id=run_id, output=serialize_to_str(getattr(event, "output", "")))

    def _handle_tool_usage_error(self, source: Any, event: "ToolUsageErrorEvent") -> None:
        """Handle tool usage error."""
        run_id = self._generate_run_id(source, event)
        metadata = self._extract_metadata(event)
        metadata["error"] = getattr(event, "error", "Unknown error")

        self._handler.end_node(
            run_id=run_id, output=f"Error: {getattr(event, 'error', 'Unknown error')}", metadata=metadata
        )

    def _to_uuid(self, id: Union[str, None, UUID]) -> Union[UUID, None]:
        if isinstance(id, UUID):
            return id
        if isinstance(id, str):
            try:
                return UUID(id)
            except ValueError:
                return None
        return None

    # LLM event handlers
    def _handle_llm_call_started(self, source: Any, event: "LLMCallStartedEvent") -> None:
        """Handle LLM call start."""
        run_id = self._generate_run_id(source, event)
        parent_run_id = self._to_uuid(event.agent_id) if hasattr(event, "agent_id") else None
        llm_name = getattr(source, "model", "Unknown Model")

        metadata = self._extract_metadata(event)
        metadata["model"] = llm_name
        if hasattr(source, "temperature"):
            metadata["temperature"] = str(source.temperature)

        self._handler.start_node(
            node_type=NodeType.LLM.value,
            parent_run_id=parent_run_id,
            run_id=run_id,
            name=llm_name,
            input=serialize_to_str(getattr(event, "messages", [])),
            model=llm_name,
            temperature=getattr(source, "temperature", None),
            metadata=metadata,
        )

    def _handle_llm_call_completed(self, source: Any, event: "LLMCallCompletedEvent") -> None:
        """Handle LLM call completion."""
        run_id = self._generate_run_id(source, event)

        self._handler.end_node(run_id=run_id, output=serialize_to_str(getattr(event, "response", "")))

    def _handle_llm_call_failed(self, source: Any, event: "LLMCallFailedEvent") -> None:
        """Handle LLM call failure."""
        run_id = self._generate_run_id(source, event)
        metadata = self._extract_metadata(event)
        metadata["error"] = getattr(event, "error", "Unknown error")

        self._handler.end_node(
            run_id=run_id, output=f"Error: {getattr(event, 'error', 'Unknown error')}", metadata=metadata
        )

    # Memory event handlers
    def _handle_memory_query_started(self, source: Any, event: "MemoryQueryStartedEvent") -> None:
        """Handle memory query start."""
        run_id = self._generate_run_id(source, event)
        parent_run_id = self._to_uuid(getattr(event, "agent_id", None))
        parent_node = self._handler.get_node(parent_run_id) if parent_run_id else None

        if not parent_node and parent_run_id:
            task_id = getattr(event, "task_id", None)
            if task_id:
                task_run_id = self._to_uuid(task_id)
                parent_node = self._handler.get_node(task_run_id) if task_run_id else None
                if parent_node:
                    self._handler.start_node(
                        node_type=NodeType.AGENT.value,
                        parent_run_id=task_run_id,
                        run_id=parent_run_id,
                        name=getattr(event, "agent_role", "Unknown Agent"),
                        input=serialize_to_str(event.query),
                    )

        metadata = self._extract_metadata(event)
        metadata["query"] = event.query
        metadata["limit"] = event.limit
        if event.score_threshold is not None:
            metadata["score_threshold"] = event.score_threshold
        if hasattr(event, "agent_role") and event.agent_role:
            metadata["agent_role"] = event.agent_role

        self._handler.start_node(
            node_type=NodeType.RETRIEVER.value,
            parent_run_id=parent_run_id,
            run_id=run_id,
            name="Memory Query",
            input=serialize_to_str(event.query),
            metadata=metadata,
        )

    def _handle_memory_query_completed(self, source: Any, event: "MemoryQueryCompletedEvent") -> None:
        """Handle memory query completion."""
        run_id = self._generate_run_id(source, event)

        metadata = self._extract_metadata(event)
        metadata["query_time_ms"] = event.query_time_ms
        metadata["results_count"] = len(event.results) if hasattr(event.results, "__len__") else 0

        output = serialize_to_str(event.results) if event.results else "No results found"
        self._handler.end_node(run_id=run_id, output=output, metadata=metadata)

    def _handle_memory_query_failed(self, source: Any, event: "MemoryQueryFailedEvent") -> None:
        """Handle memory query failure."""
        run_id = self._generate_run_id(source, event)

        metadata = self._extract_metadata(event)
        metadata["error"] = event.error

        self._handler.end_node(run_id=run_id, output=f"Memory query failed: {event.error}", metadata=metadata)

    def _handle_memory_save_started(self, source: Any, event: "MemorySaveStartedEvent") -> None:
        """Handle memory save start."""
        run_id = self._generate_run_id(source, event)
        parent_run_id = self._to_uuid(getattr(event, "agent_id", None))

        metadata = self._extract_metadata(event)
        if hasattr(event, "metadata") and event.metadata:
            metadata.update(event.metadata)
        if hasattr(event, "agent_role") and event.agent_role:
            metadata["agent_role"] = event.agent_role

        input_value = event.value if event.value else "Memory content"

        self._handler.start_node(
            node_type=NodeType.CHAIN.value,
            parent_run_id=parent_run_id,
            run_id=run_id,
            name="Memory Save",
            input=serialize_to_str(input_value),
            metadata=metadata,
        )

    def _handle_memory_save_completed(self, source: Any, event: "MemorySaveCompletedEvent") -> None:
        """Handle memory save completion."""
        run_id = self._generate_run_id(source, event)

        metadata = self._extract_metadata(event)
        metadata["save_time_ms"] = event.save_time_ms

        self._handler.end_node(run_id=run_id, output=f"Memory saved successfully: {event.value}", metadata=metadata)

    def _handle_memory_save_failed(self, source: Any, event: "MemorySaveFailedEvent") -> None:
        """Handle memory save failure."""
        run_id = self._generate_run_id(source, event)

        metadata = self._extract_metadata(event)
        metadata["error"] = event.error

        self._handler.end_node(run_id=run_id, output=f"Memory save failed: {event.error}", metadata=metadata)

    def _handle_memory_retrieval_started(self, source: Any, event: "MemoryRetrievalStartedEvent") -> None:
        """Handle memory retrieval start."""
        run_id = self._generate_run_id(source, event)
        parent_run_id = self._to_uuid(getattr(event, "task_id", None))

        metadata = self._extract_metadata(event)
        if hasattr(event, "task_id") and event.task_id:
            metadata["task_id"] = event.task_id

        self._handler.start_node(
            node_type=NodeType.CHAIN.value,
            parent_run_id=parent_run_id,
            run_id=run_id,
            name="Memory Retrieval",
            input="Retrieving relevant memories for task",
            metadata=metadata,
        )

    def _handle_memory_retrieval_completed(self, source: Any, event: "MemoryRetrievalCompletedEvent") -> None:
        """Handle memory retrieval completion."""
        run_id = self._generate_run_id(source, event)

        metadata = self._extract_metadata(event)
        metadata["retrieval_time_ms"] = event.retrieval_time_ms

        self._handler.end_node(run_id=run_id, output=serialize_to_str(event.memory_content), metadata=metadata)

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
