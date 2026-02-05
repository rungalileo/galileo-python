"""Unit tests for SpanTracker."""

from uuid import uuid4

from galileo_adk.span_tracker import SpanTracker


class TestSpanTrackerRuns:
    """Tests for run span tracking."""

    def test_register_and_get_run(self) -> None:
        tracker = SpanTracker()
        run_id = uuid4()
        tracker.register_run("inv1", "session1", run_id)

        assert tracker.get_run("inv1") == run_id
        assert tracker.run_count == 1

    def test_pop_run(self) -> None:
        tracker = SpanTracker()
        run_id = uuid4()
        tracker.register_run("inv1", "session1", run_id)

        result = tracker.pop_run("inv1")

        assert result == run_id
        assert tracker.get_run("inv1") is None
        assert tracker.run_count == 0

    def test_pop_nonexistent_run(self) -> None:
        tracker = SpanTracker()
        assert tracker.pop_run("nonexistent") is None


class TestSpanTrackerAgents:
    """Tests for agent span tracking."""

    def test_register_and_get_agent(self) -> None:
        tracker = SpanTracker()
        run_id = uuid4()
        tracker.register_agent("inv1", "agent1", run_id)

        assert tracker.get_agent("inv1", "agent1") == run_id
        assert tracker.agent_count == 1

    def test_multiple_agents_same_invocation(self) -> None:
        tracker = SpanTracker()
        run_id1 = uuid4()
        run_id2 = uuid4()
        tracker.register_agent("inv1", "agent1", run_id1)
        tracker.register_agent("inv1", "agent2", run_id2)

        assert tracker.get_agent("inv1", "agent1") == run_id1
        assert tracker.get_agent("inv1", "agent2") == run_id2
        assert tracker.agent_count == 2

    def test_same_agent_different_invocations(self) -> None:
        tracker = SpanTracker()
        run_id1 = uuid4()
        run_id2 = uuid4()
        tracker.register_agent("inv1", "agent1", run_id1)
        tracker.register_agent("inv2", "agent1", run_id2)

        assert tracker.get_agent("inv1", "agent1") == run_id1
        assert tracker.get_agent("inv2", "agent1") == run_id2
        assert tracker.agent_count == 2

    def test_pop_agent(self) -> None:
        tracker = SpanTracker()
        run_id = uuid4()
        tracker.register_agent("inv1", "agent1", run_id)

        result = tracker.pop_agent("inv1", "agent1")

        assert result == run_id
        assert tracker.get_agent("inv1", "agent1") is None
        assert tracker.agent_count == 0

    def test_pop_agent_cleans_empty_invocation(self) -> None:
        tracker = SpanTracker()
        run_id1 = uuid4()
        run_id2 = uuid4()
        tracker.register_agent("inv1", "agent1", run_id1)
        tracker.register_agent("inv1", "agent2", run_id2)

        tracker.pop_agent("inv1", "agent1")
        assert tracker.agent_count == 1

        tracker.pop_agent("inv1", "agent2")
        assert tracker.agent_count == 0
        # Internal dict should be cleaned up
        assert "inv1" not in tracker._agents

    def test_pop_all_agents_for_invocation(self) -> None:
        tracker = SpanTracker()
        run_id1 = uuid4()
        run_id2 = uuid4()
        run_id3 = uuid4()
        tracker.register_agent("inv1", "agent1", run_id1)
        tracker.register_agent("inv1", "agent2", run_id2)
        tracker.register_agent("inv2", "agent3", run_id3)

        result = tracker.pop_all_agents_for_invocation("inv1")

        assert set(result) == {run_id1, run_id2}
        assert tracker.agent_count == 1
        assert tracker.get_agent("inv2", "agent3") == run_id3


class TestSpanTrackerLlms:
    """Tests for LLM span tracking."""

    def test_register_and_pop_llm(self) -> None:
        tracker = SpanTracker()
        run_id = uuid4()
        tracker.register_llm("inv1", "call1", run_id)

        assert tracker.llm_count == 1
        result = tracker.pop_llm("inv1", "call1")
        assert result == run_id
        assert tracker.llm_count == 0

    def test_multiple_llms_same_prefix(self) -> None:
        tracker = SpanTracker()
        run_id1 = uuid4()
        run_id2 = uuid4()
        tracker.register_llm("inv1", "call1", run_id1)
        tracker.register_llm("inv1", "call2", run_id2)

        assert tracker.llm_count == 2

        # Pop specific call_id returns the exact run_id
        result1 = tracker.pop_llm("inv1", "call1")
        assert result1 == run_id1
        assert tracker.llm_count == 1

        result2 = tracker.pop_llm("inv1", "call2")
        assert result2 == run_id2
        assert tracker.llm_count == 0

    def test_pop_llm_nonexistent(self) -> None:
        tracker = SpanTracker()
        assert tracker.pop_llm("nonexistent", "call1") is None

    def test_pop_llm_wrong_call_id(self) -> None:
        tracker = SpanTracker()
        run_id = uuid4()
        tracker.register_llm("inv1", "call1", run_id)

        # Popping with wrong call_id returns None
        assert tracker.pop_llm("inv1", "wrong_call_id") is None
        # Original entry still exists
        assert tracker.llm_count == 1


class TestSpanTrackerTools:
    """Tests for tool span tracking."""

    def test_register_and_pop_tool(self) -> None:
        tracker = SpanTracker()
        run_id = uuid4()
        tracker.register_tool("inv1", "tool_abc123", run_id)

        assert tracker.tool_count == 1
        result = tracker.pop_tool("inv1", "tool_abc123")
        assert result == run_id
        assert tracker.tool_count == 0

    def test_multiple_tools_same_prefix(self) -> None:
        tracker = SpanTracker()
        run_id1 = uuid4()
        run_id2 = uuid4()
        tracker.register_tool("inv1", "tool1_abc", run_id1)
        tracker.register_tool("inv1", "tool2_def", run_id2)

        assert tracker.tool_count == 2

        # Pop specific tool_key returns the exact run_id
        result1 = tracker.pop_tool("inv1", "tool1_abc")
        assert result1 == run_id1
        assert tracker.tool_count == 1

        result2 = tracker.pop_tool("inv1", "tool2_def")
        assert result2 == run_id2
        assert tracker.tool_count == 0

    def test_pop_tool_nonexistent(self) -> None:
        tracker = SpanTracker()
        assert tracker.pop_tool("nonexistent", "tool_key") is None

    def test_pop_tool_wrong_key(self) -> None:
        tracker = SpanTracker()
        run_id = uuid4()
        tracker.register_tool("inv1", "tool_abc", run_id)

        # Popping with wrong tool_key returns None
        assert tracker.pop_tool("inv1", "wrong_tool_key") is None
        # Original entry still exists
        assert tracker.tool_count == 1


class TestSpanTrackerCounts:
    """Tests for count properties."""

    def test_all_counts_zero_initially(self) -> None:
        tracker = SpanTracker()
        assert tracker.run_count == 0
        assert tracker.agent_count == 0
        assert tracker.llm_count == 0
        assert tracker.tool_count == 0

    def test_counts_after_registrations(self) -> None:
        tracker = SpanTracker()
        tracker.register_run("inv1", "session1", uuid4())
        tracker.register_run("inv2", "session2", uuid4())
        tracker.register_agent("inv1", "a1", uuid4())
        tracker.register_agent("inv1", "a2", uuid4())
        tracker.register_agent("inv2", "a1", uuid4())
        tracker.register_llm("inv1", "c1", uuid4())
        tracker.register_tool("inv1", "t1", uuid4())
        tracker.register_tool("inv2", "t2", uuid4())

        assert tracker.run_count == 2
        assert tracker.agent_count == 3
        assert tracker.llm_count == 1
        assert tracker.tool_count == 2


class TestSpanTrackerActiveTools:
    """Tests for active tool tracking."""

    def test_has_any_active_tools_returns_false_when_empty(self) -> None:
        tracker = SpanTracker()
        assert tracker.has_any_active_tools() is False

    def test_has_any_active_tools_returns_true_when_tool_active(self) -> None:
        tracker = SpanTracker()
        tool_run_id = uuid4()

        tracker.set_active_tool("session1", tool_run_id)

        assert tracker.has_any_active_tools() is True

    def test_has_any_active_tools_returns_false_after_clear(self) -> None:
        tracker = SpanTracker()
        tool_run_id = uuid4()

        tracker.set_active_tool("session1", tool_run_id)
        assert tracker.has_any_active_tools() is True

        tracker.clear_active_tool("session1", tool_run_id)

        assert tracker.has_any_active_tools() is False

    def test_has_any_active_tools_multiple_sessions(self) -> None:
        tracker = SpanTracker()
        tool_a = uuid4()
        tool_b = uuid4()

        tracker.set_active_tool("session1", tool_a)
        tracker.set_active_tool("session2", tool_b)
        assert tracker.has_any_active_tools() is True

        tracker.clear_active_tool("session1", tool_a)
        assert tracker.has_any_active_tools() is True

        tracker.clear_active_tool("session2", tool_b)
        assert tracker.has_any_active_tools() is False

    def test_pop_all_tools_clears_active_tool_by_session_id(self) -> None:
        tracker = SpanTracker()
        run_id = uuid4()
        tool_run_id = uuid4()

        # Given: a run registered with session mapping and an active tool
        tracker.register_run("inv1", "session1", run_id)
        tracker.register_tool("inv1", "tool_key", tool_run_id)
        tracker.set_active_tool("session1", tool_run_id)
        assert tracker.get_active_tool("session1") == tool_run_id

        tracker.pop_all_tools_for_invocation("inv1")

        assert tracker.get_active_tool("session1") is None

    def test_pop_run_clears_invocation_to_session_mapping(self) -> None:
        tracker = SpanTracker()
        run_id = uuid4()

        tracker.register_run("inv1", "session1", run_id)
        assert tracker._invocation_to_session.get("inv1") == "session1"

        tracker.pop_run("inv1")

        assert tracker._invocation_to_session.get("inv1") is None

    def test_active_tool_stack_push_pop_lifo(self) -> None:
        """Active tools use LIFO order."""
        tracker = SpanTracker()
        tool_a = uuid4()
        tool_b = uuid4()
        tool_c = uuid4()

        tracker.set_active_tool("session1", tool_a)
        tracker.set_active_tool("session1", tool_b)
        tracker.set_active_tool("session1", tool_c)
        assert tracker.get_active_tool("session1") == tool_c

        tracker.clear_active_tool("session1", tool_c)
        assert tracker.get_active_tool("session1") == tool_b

        tracker.clear_active_tool("session1", tool_b)
        assert tracker.get_active_tool("session1") == tool_a

        tracker.clear_active_tool("session1", tool_a)
        assert tracker.get_active_tool("session1") is None

    def test_clear_active_tool_only_pops_if_top_matches(self) -> None:
        """clear_active_tool only pops if run_id matches top of stack."""
        tracker = SpanTracker()
        tool_a = uuid4()
        tool_b = uuid4()

        tracker.set_active_tool("session1", tool_a)
        tracker.set_active_tool("session1", tool_b)

        tracker.clear_active_tool("session1", tool_a)
        assert tracker.get_active_tool("session1") == tool_b

        tracker.clear_active_tool("session1", tool_b)
        assert tracker.get_active_tool("session1") == tool_a

    def test_pop_all_tools_clears_entire_stack(self) -> None:
        tracker = SpanTracker()
        run_id = uuid4()
        tool_a = uuid4()
        tool_b = uuid4()

        tracker.register_run("inv1", "session1", run_id)
        tracker.register_tool("inv1", "tool_a", tool_a)
        tracker.register_tool("inv1", "tool_b", tool_b)
        tracker.set_active_tool("session1", tool_a)
        tracker.set_active_tool("session1", tool_b)
        assert tracker.get_active_tool("session1") == tool_b

        tracker.pop_all_tools_for_invocation("inv1")

        assert tracker.get_active_tool("session1") is None
