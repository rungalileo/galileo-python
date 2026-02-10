"""Unit tests for SpanTracker."""

import threading
from unittest.mock import MagicMock
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

        assert tracker.pop_llm("inv1", "wrong_call_id") is None
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

        assert tracker.pop_tool("inv1", "wrong_tool_key") is None
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


class TestSpanTrackerObjectCallIds:
    """Tests for identity-based call_id correlation."""

    def test_store_and_get_call_id(self) -> None:
        """Store and retrieve a call_id by object identity."""
        # Given: a tracker and an object with a stored call_id
        tracker = SpanTracker()
        obj = MagicMock()
        tracker.store_call_id(obj, "call-123")

        # When: retrieving the call_id
        result = tracker.get_stored_call_id(obj)

        # Then: the stored call_id is returned
        assert result == "call-123"

    def test_get_stored_call_id_returns_none_for_unknown(self) -> None:
        """get_stored_call_id returns None for untracked objects."""
        tracker = SpanTracker()
        obj = MagicMock()

        assert tracker.get_stored_call_id(obj) is None

    def test_clear_stored_call_id(self) -> None:
        """clear_stored_call_id removes the stored call_id."""
        tracker = SpanTracker()
        obj = MagicMock()
        tracker.store_call_id(obj, "call-456")
        assert tracker.get_stored_call_id(obj) == "call-456"

        tracker.clear_stored_call_id(obj)

        assert tracker.get_stored_call_id(obj) is None

    def test_clear_stored_call_id_noop_for_unknown(self) -> None:
        """clear_stored_call_id is a no-op for untracked objects."""
        tracker = SpanTracker()
        obj = MagicMock()

        # Should not raise
        tracker.clear_stored_call_id(obj)


class TestSpanTrackerResolveLlmCallId:
    """Tests for resolve_llm_call_id multi-strategy resolution."""

    def test_stored_call_id_takes_precedence(self) -> None:
        """Stored call_id (identity-based) is the highest priority."""
        # Given: an object with both a stored call_id and a request_id attribute
        tracker = SpanTracker()
        obj = MagicMock()
        obj.request_id = "request-abc"
        tracker.store_call_id(obj, "stored-xyz")

        # When: resolving the call_id
        result = tracker.resolve_llm_call_id(obj, invocation_id="inv1")

        # Then: the stored call_id wins
        assert result == "stored-xyz"

    def test_request_id_attribute_used_when_no_stored(self) -> None:
        """request_id attribute is used when no stored call_id exists."""
        tracker = SpanTracker()
        obj = MagicMock()
        obj.request_id = "request-abc"

        result = tracker.resolve_llm_call_id(obj)

        assert result == "request-abc"

    def test_current_stack_used_when_no_request_id(self) -> None:
        """Current LLM call_id stack is used when no stored or request_id."""
        tracker = SpanTracker()
        obj = MagicMock(spec=[])  # No attributes
        tracker.set_current_llm_call_id("inv1", "stack-call-1")

        result = tracker.resolve_llm_call_id(obj, invocation_id="inv1")

        assert result == "stack-call-1"

    def test_fallback_to_object_identity(self) -> None:
        """Falls back to object identity when all strategies fail."""
        tracker = SpanTracker()
        obj = MagicMock(spec=[])  # No attributes

        result = tracker.resolve_llm_call_id(obj)

        assert result.startswith("llm_")
        assert str(id(obj)) in result


class TestSpanTrackerMakeToolKey:
    """Tests for make_tool_key static method."""

    def test_generates_key_from_tool_name(self) -> None:
        """Tool key includes the tool's name."""
        tool = MagicMock()
        tool.name = "my_tool"

        key = SpanTracker.make_tool_key(tool)

        assert key.startswith("my_tool_")

    def test_generates_unique_keys_for_different_tool_instances(self) -> None:
        """Different tool instances produce different keys."""
        tool_a = MagicMock()
        tool_a.name = "search"
        tool_b = MagicMock()
        tool_b.name = "search"

        key_a = SpanTracker.make_tool_key(tool_a)
        key_b = SpanTracker.make_tool_key(tool_b)

        assert key_a != key_b

    def test_handles_missing_name_attribute(self) -> None:
        """Falls back to 'unknown' when tool has no name attribute."""
        tool = MagicMock(spec=[])  # No attributes

        key = SpanTracker.make_tool_key(tool)

        assert key.startswith("unknown_")


class TestSpanTrackerClearAllLlmCallIds:
    """Tests for clear_all_llm_call_ids_for_invocation."""

    def test_clears_all_call_ids_for_invocation(self) -> None:
        """All LLM call_ids for an invocation are cleared."""
        tracker = SpanTracker()
        tracker.set_current_llm_call_id("inv1", "call-1")
        tracker.set_current_llm_call_id("inv1", "call-2")
        tracker.set_current_llm_call_id("inv2", "call-3")

        tracker.clear_all_llm_call_ids_for_invocation("inv1")

        assert tracker.get_current_llm_call_id("inv1") is None
        # Other invocations unaffected
        assert tracker.get_current_llm_call_id("inv2") == "call-3"

    def test_noop_for_unknown_invocation(self) -> None:
        """Clearing a non-existent invocation doesn't raise."""
        tracker = SpanTracker()
        tracker.clear_all_llm_call_ids_for_invocation("nonexistent")


class TestSpanTrackerConcurrency:
    """Tests for thread safety of SpanTracker."""

    def test_concurrent_register_and_pop_runs(self) -> None:
        """Multiple threads can register and pop runs concurrently without errors."""
        # Given: a shared tracker
        tracker = SpanTracker()
        num_threads = 20
        iterations_per_thread = 50
        errors: list[Exception] = []

        def worker(thread_id: int) -> None:
            try:
                for i in range(iterations_per_thread):
                    inv_id = f"inv_{thread_id}_{i}"
                    run_id = uuid4()
                    tracker.register_run(inv_id, f"session_{thread_id}", run_id)
                    got = tracker.get_run(inv_id)
                    assert got == run_id, f"Expected {run_id}, got {got}"
                    popped = tracker.pop_run(inv_id)
                    assert popped == run_id, f"Expected {run_id}, popped {popped}"
            except Exception as e:
                errors.append(e)

        # When: running concurrent workers
        threads = [threading.Thread(target=worker, args=(tid,)) for tid in range(num_threads)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        # Then: no errors occurred
        assert errors == [], f"Concurrent errors: {errors}"
        assert tracker.run_count == 0

    def test_concurrent_register_and_pop_agents(self) -> None:
        """Multiple threads can register and pop agents concurrently."""
        tracker = SpanTracker()
        num_threads = 10
        iterations = 30
        errors: list[Exception] = []

        def worker(thread_id: int) -> None:
            try:
                for i in range(iterations):
                    inv_id = f"inv_{thread_id}"
                    agent_name = f"agent_{thread_id}_{i}"
                    run_id = uuid4()
                    tracker.register_agent(inv_id, agent_name, run_id)
                    got = tracker.get_agent(inv_id, agent_name)
                    assert got == run_id
                    popped = tracker.pop_agent(inv_id, agent_name)
                    assert popped == run_id
            except Exception as e:
                errors.append(e)

        threads = [threading.Thread(target=worker, args=(tid,)) for tid in range(num_threads)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        assert errors == [], f"Concurrent errors: {errors}"
        assert tracker.agent_count == 0
