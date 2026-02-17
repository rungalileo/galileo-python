"""Run ID tracking for span correlation across ADK callbacks."""

from __future__ import annotations

import logging
import threading
from typing import Any
from uuid import UUID

_logger = logging.getLogger(__name__)


class SpanTracker:
    """Tracks run IDs for correlating before/after callbacks.

    Uses nested dicts keyed by {prefix: {suffix: run_id}} for O(1) lookup.
    All public methods are thread-safe via threading.Lock.
    """

    def __init__(self) -> None:
        self._lock = threading.Lock()
        # {invocation_id: run_id}
        self._runs: dict[str, UUID] = {}
        # {invocation_id: {agent_name: run_id}}
        self._agents: dict[str, dict[str, UUID]] = {}
        # {invocation_id: {call_id: run_id}}
        self._llms: dict[str, dict[str, UUID]] = {}
        # {invocation_id: {tool_key: run_id}}
        self._tools: dict[str, dict[str, UUID]] = {}
        # {session_id: [run_id, ...]} — keyed by session_id so sub-invocations
        # share the same tool stack as their parent.
        self._active_tools: dict[str, list[UUID]] = {}
        # {invocation_id: session_id}
        self._invocation_to_session: dict[str, str] = {}
        # {invocation_id: [call_id, ...]}
        self._current_llm_call_id: dict[str, list[str]] = {}
        # {id(obj): call_id} — correlates LLM call IDs by object identity
        self._object_call_ids: dict[int, str] = {}

    # --- Run spans ---
    def register_run(self, invocation_id: str, session_id: str, run_id: UUID) -> None:
        """Register a run span for an invocation."""
        with self._lock:
            self._runs[invocation_id] = run_id
            self._invocation_to_session[invocation_id] = session_id

    def pop_run(self, invocation_id: str) -> UUID | None:
        """Pop and return the run_id for an invocation."""
        with self._lock:
            self._invocation_to_session.pop(invocation_id, None)
            return self._runs.pop(invocation_id, None)

    def get_run(self, invocation_id: str) -> UUID | None:
        """Get the run_id for an invocation without removing it."""
        with self._lock:
            return self._runs.get(invocation_id)

    # --- Agent spans ---
    def register_agent(self, invocation_id: str, agent_name: str, run_id: UUID) -> None:
        """Register an agent span."""
        with self._lock:
            if invocation_id not in self._agents:
                self._agents[invocation_id] = {}
            self._agents[invocation_id][agent_name] = run_id

    def pop_agent(self, invocation_id: str, agent_name: str) -> UUID | None:
        """Pop and return the agent run_id."""
        with self._lock:
            agents = self._agents.get(invocation_id)
            if agents:
                run_id = agents.pop(agent_name, None)
                if not agents:
                    del self._agents[invocation_id]
                return run_id
            return None

    def get_agent(self, invocation_id: str, agent_name: str) -> UUID | None:
        """Get the agent run_id without removing it."""
        with self._lock:
            return self._agents.get(invocation_id, {}).get(agent_name)

    # --- LLM spans ---
    def register_llm(self, prefix: str, call_id: str, run_id: UUID) -> None:
        """Register an LLM span with a unique call_id."""
        with self._lock:
            if prefix not in self._llms:
                self._llms[prefix] = {}
            self._llms[prefix][call_id] = run_id

    def pop_llm(self, prefix: str, call_id: str) -> UUID | None:
        """Pop and return the LLM run_id for the specific call_id."""
        with self._lock:
            llms = self._llms.get(prefix)
            if llms:
                run_id = llms.pop(call_id, None)
                if not llms:
                    del self._llms[prefix]
                return run_id
            return None

    def set_current_llm_call_id(self, invocation_id: str, call_id: str) -> None:
        """Push an LLM call_id onto the stack for response correlation."""
        with self._lock:
            if invocation_id not in self._current_llm_call_id:
                self._current_llm_call_id[invocation_id] = []
            self._current_llm_call_id[invocation_id].append(call_id)

    def get_current_llm_call_id(self, invocation_id: str) -> str | None:
        """Get the top LLM call_id from the stack for an invocation."""
        with self._lock:
            stack = self._current_llm_call_id.get(invocation_id)
            if stack:
                return stack[-1]
            return None

    def clear_current_llm_call_id(self, invocation_id: str, call_id: str | None = None) -> None:
        """Pop the LLM call_id from the stack.

        If call_id is provided and matches the top, pop it.
        If call_id is None, pop the top unconditionally.
        Removes the invocation key when the stack is empty.
        """
        with self._lock:
            stack = self._current_llm_call_id.get(invocation_id)
            if not stack:
                return
            if call_id is None or stack[-1] == call_id:
                stack.pop()
            if not stack:
                del self._current_llm_call_id[invocation_id]

    def clear_all_llm_call_ids_for_invocation(self, invocation_id: str) -> None:
        """Remove all LLM call_id entries for an invocation."""
        with self._lock:
            self._current_llm_call_id.pop(invocation_id, None)

    # --- Tool spans ---
    def register_tool(self, prefix: str, tool_key: str, run_id: UUID) -> None:
        """Register a tool span with a unique tool_key."""
        with self._lock:
            if prefix not in self._tools:
                self._tools[prefix] = {}
            self._tools[prefix][tool_key] = run_id

    def pop_tool(self, prefix: str, tool_key: str) -> UUID | None:
        """Pop and return the tool run_id for the specific tool_key."""
        with self._lock:
            tools = self._tools.get(prefix)
            if tools:
                run_id = tools.pop(tool_key, None)
                if not tools:
                    del self._tools[prefix]
                return run_id
            return None

    # --- Active tool tracking (for sub-invocation parenting) ---
    def has_any_active_tools(self) -> bool:
        """Check if any session has active tools (indicates sub-invocation)."""
        with self._lock:
            return any(stack for stack in self._active_tools.values())

    def set_active_tool(self, session_id: str, run_id: UUID) -> None:
        """Push a tool onto the active tool stack for a session."""
        with self._lock:
            if session_id not in self._active_tools:
                self._active_tools[session_id] = []
            self._active_tools[session_id].append(run_id)

    def get_active_tool(self, session_id: str) -> UUID | None:
        """Get the top active tool run_id for a session (most recently pushed)."""
        with self._lock:
            stack = self._active_tools.get(session_id)
            if stack:
                return stack[-1]
            return None

    def clear_active_tool(self, session_id: str, run_id: UUID) -> None:
        """Pop the active tool if it matches the given run_id (LIFO order)."""
        with self._lock:
            stack = self._active_tools.get(session_id)
            if stack and stack[-1] == run_id:
                stack.pop()
                if not stack:
                    del self._active_tools[session_id]

    # --- Object-based call_id correlation ---
    def store_call_id(self, obj: Any, call_id: str) -> None:
        """Store a call_id associated with an object's identity."""
        with self._lock:
            self._object_call_ids[id(obj)] = call_id

    def get_stored_call_id(self, obj: Any) -> str | None:
        """Get the call_id stored for an object's identity."""
        with self._lock:
            return self._object_call_ids.get(id(obj))

    def clear_stored_call_id(self, obj: Any) -> None:
        """Remove the call_id stored for an object's identity."""
        with self._lock:
            self._object_call_ids.pop(id(obj), None)

    # --- Shared helpers ---
    def resolve_llm_call_id(self, obj: Any, invocation_id: str | None = None) -> str:
        """Resolve the LLM call_id for an object using multiple strategies.

        Order: stored call_id → request_id attribute → current stack → object identity fallback.
        """
        with self._lock:
            stored = self._object_call_ids.get(id(obj))
            if stored:
                return stored
        request_id = getattr(obj, "request_id", None)
        if request_id:
            return str(request_id)
        if invocation_id:
            with self._lock:
                stack = self._current_llm_call_id.get(invocation_id)
                if stack:
                    return stack[-1]
        _logger.debug("LLM correlation: falling back to object identity for %s", type(obj).__name__)
        return f"llm_{id(obj)}"

    @staticmethod
    def make_tool_key(tool: Any) -> str:
        """Generate a stable tool key from the tool object."""
        tool_name = getattr(tool, "name", "unknown")
        return f"{tool_name}_{id(tool)}"

    # --- Cleanup helpers ---
    def pop_all_agents_for_invocation(self, invocation_id: str) -> list[UUID]:
        """Pop all agent run_ids for an invocation (for error cleanup)."""
        with self._lock:
            agents = self._agents.pop(invocation_id, {})
            return list(agents.values())

    def pop_all_llms_for_invocation(self, invocation_id: str) -> list[UUID]:
        """Pop all LLM run_ids for an invocation (for error cleanup)."""
        with self._lock:
            llms = self._llms.pop(invocation_id, {})
            return list(llms.values())

    def pop_all_tools_for_invocation(self, invocation_id: str) -> list[UUID]:
        """Pop all tool run_ids for an invocation (for error cleanup)."""
        with self._lock:
            tools = self._tools.pop(invocation_id, {})
            # Look up the session_id for this invocation and clear entire active tool stack
            session_id = self._invocation_to_session.get(invocation_id)
            if session_id:
                self._active_tools.pop(session_id, None)
            return list(tools.values())

    # --- Count properties for testing ---
    @property
    def run_count(self) -> int:
        """Number of active run spans."""
        with self._lock:
            return len(self._runs)

    @property
    def agent_count(self) -> int:
        """Number of active agent spans."""
        with self._lock:
            return sum(len(agents) for agents in self._agents.values())

    @property
    def llm_count(self) -> int:
        """Number of active LLM spans."""
        with self._lock:
            return sum(len(llms) for llms in self._llms.values())

    @property
    def tool_count(self) -> int:
        """Number of active tool spans."""
        with self._lock:
            return sum(len(tools) for tools in self._tools.values())
