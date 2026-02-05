"""Run ID tracking for span correlation across ADK callbacks."""

from uuid import UUID


class SpanTracker:
    """Tracks run IDs for correlating before/after callbacks.

    Uses nested dicts for O(1) lookup instead of O(n) prefix search.
    Structure: {prefix: {suffix: run_id}}

    Example:
        tracker = SpanTracker()
        tracker.register_agent("inv123", "my_agent", run_id)
        run_id = tracker.pop_agent("inv123", "my_agent")
    """

    def __init__(self) -> None:
        # {invocation_id: run_id}
        self._runs: dict[str, UUID] = {}
        # {invocation_id: {agent_name: run_id}}
        self._agents: dict[str, dict[str, UUID]] = {}
        # {invocation_id: {call_id: run_id}}
        self._llms: dict[str, dict[str, UUID]] = {}
        # {invocation_id: {tool_key: run_id}}
        self._tools: dict[str, dict[str, UUID]] = {}
        # {session_id: [run_id, ...]} - stack of active tools for sub-invocation parenting.
        # Uses session_id (not invocation_id) because sub-invocations have different
        # invocation_ids but share the same session_id with their parent.
        # Stack structure handles concurrent sibling tools correctly.
        self._active_tools: dict[str, list[UUID]] = {}
        # {invocation_id: session_id} - maps invocations to sessions for cleanup
        self._invocation_to_session: dict[str, str] = {}
        # {invocation_id: [call_id, ...]} - stack of LLM call_ids for response correlation
        self._current_llm_call_id: dict[str, list[str]] = {}

    # --- Run spans ---
    def register_run(self, invocation_id: str, session_id: str, run_id: UUID) -> None:
        """Register a run span for an invocation."""
        self._runs[invocation_id] = run_id
        self._invocation_to_session[invocation_id] = session_id

    def pop_run(self, invocation_id: str) -> UUID | None:
        """Pop and return the run_id for an invocation."""
        self._invocation_to_session.pop(invocation_id, None)
        return self._runs.pop(invocation_id, None)

    def get_run(self, invocation_id: str) -> UUID | None:
        """Get the run_id for an invocation without removing it."""
        return self._runs.get(invocation_id)

    # --- Agent spans ---
    def register_agent(self, invocation_id: str, agent_name: str, run_id: UUID) -> None:
        """Register an agent span."""
        if invocation_id not in self._agents:
            self._agents[invocation_id] = {}
        self._agents[invocation_id][agent_name] = run_id

    def pop_agent(self, invocation_id: str, agent_name: str) -> UUID | None:
        """Pop and return the agent run_id."""
        agents = self._agents.get(invocation_id)
        if agents:
            run_id = agents.pop(agent_name, None)
            if not agents:
                del self._agents[invocation_id]
            return run_id
        return None

    def get_agent(self, invocation_id: str, agent_name: str) -> UUID | None:
        """Get the agent run_id without removing it."""
        return self._agents.get(invocation_id, {}).get(agent_name)

    # --- LLM spans ---
    def register_llm(self, prefix: str, call_id: str, run_id: UUID) -> None:
        """Register an LLM span with a unique call_id."""
        if prefix not in self._llms:
            self._llms[prefix] = {}
        self._llms[prefix][call_id] = run_id

    def pop_llm(self, prefix: str, call_id: str) -> UUID | None:
        """Pop and return the LLM run_id for the specific call_id."""
        llms = self._llms.get(prefix)
        if llms:
            run_id = llms.pop(call_id, None)
            if not llms:
                del self._llms[prefix]
            return run_id
        return None

    def set_current_llm_call_id(self, invocation_id: str, call_id: str) -> None:
        """Push an LLM call_id onto the stack for response correlation."""
        if invocation_id not in self._current_llm_call_id:
            self._current_llm_call_id[invocation_id] = []
        self._current_llm_call_id[invocation_id].append(call_id)

    def get_current_llm_call_id(self, invocation_id: str) -> str | None:
        """Get the top LLM call_id from the stack for an invocation."""
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
        stack = self._current_llm_call_id.get(invocation_id)
        if not stack:
            return
        if call_id is None or stack[-1] == call_id:
            stack.pop()
        if not stack:
            del self._current_llm_call_id[invocation_id]

    # --- Tool spans ---
    def register_tool(self, prefix: str, tool_key: str, run_id: UUID) -> None:
        """Register a tool span with a unique tool_key."""
        if prefix not in self._tools:
            self._tools[prefix] = {}
        self._tools[prefix][tool_key] = run_id

    def pop_tool(self, prefix: str, tool_key: str) -> UUID | None:
        """Pop and return the tool run_id for the specific tool_key."""
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
        return any(stack for stack in self._active_tools.values())

    def set_active_tool(self, session_id: str, run_id: UUID) -> None:
        """Push a tool onto the active tool stack for a session."""
        if session_id not in self._active_tools:
            self._active_tools[session_id] = []
        self._active_tools[session_id].append(run_id)

    def get_active_tool(self, session_id: str) -> UUID | None:
        """Get the top active tool run_id for a session (most recently pushed)."""
        stack = self._active_tools.get(session_id)
        if stack:
            return stack[-1]
        return None

    def clear_active_tool(self, session_id: str, run_id: UUID) -> None:
        """Pop the active tool if it matches the given run_id (LIFO order)."""
        stack = self._active_tools.get(session_id)
        if stack and stack[-1] == run_id:
            stack.pop()
            if not stack:
                del self._active_tools[session_id]

    # --- Cleanup helpers ---
    def pop_all_agents_for_invocation(self, invocation_id: str) -> list[UUID]:
        """Pop all agent run_ids for an invocation (for error cleanup)."""
        agents = self._agents.pop(invocation_id, {})
        return list(agents.values())

    def pop_all_llms_for_invocation(self, invocation_id: str) -> list[UUID]:
        """Pop all LLM run_ids for an invocation (for error cleanup)."""
        llms = self._llms.pop(invocation_id, {})
        return list(llms.values())

    def pop_all_tools_for_invocation(self, invocation_id: str) -> list[UUID]:
        """Pop all tool run_ids for an invocation (for error cleanup)."""
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
        return len(self._runs)

    @property
    def agent_count(self) -> int:
        """Number of active agent spans."""
        return sum(len(agents) for agents in self._agents.values())

    @property
    def llm_count(self) -> int:
        """Number of active LLM spans."""
        return sum(len(llms) for llms in self._llms.values())

    @property
    def tool_count(self) -> int:
        """Number of active tool spans."""
        return sum(len(tools) for tools in self._tools.values())
