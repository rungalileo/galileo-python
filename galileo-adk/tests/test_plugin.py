"""Integration tests for GalileoADKPlugin."""

from unittest.mock import MagicMock
from uuid import uuid4

import pytest

from galileo_adk import GalileoADKPlugin


class MockCallbackContext:
    """Mock ADK CallbackContext for testing."""

    def __init__(
        self,
        agent_name: str = "test_agent",
        invocation_id: str | None = None,
    ) -> None:
        self.agent_name = agent_name
        self.invocation_id = invocation_id or str(uuid4())
        self.parent_context = MagicMock()
        self.parent_context.new_message = MagicMock()
        self.parent_context.new_message.parts = [MagicMock(text="test input")]


class MockInvocationContext:
    """Mock ADK InvocationContext for testing."""

    def __init__(
        self,
        agent_name: str = "test_agent",
        invocation_id: str | None = None,
    ) -> None:
        self.agent_name = agent_name
        self.invocation_id = invocation_id or str(uuid4())
        self.session = MagicMock()
        self.session.session_id = "test_session"


class MockLlmRequest:
    """Mock ADK LlmRequest for testing."""

    def __init__(self, model: str = "gemini-2.0-flash", request_id: str | None = None) -> None:
        self.model = model
        self.config = MagicMock()
        self.config.temperature = 0.7
        self.config.tools = None
        self.contents = []
        self.request_id = request_id or str(uuid4())


class MockLlmResponse:
    """Mock ADK LlmResponse for testing."""

    def __init__(self, text: str = "test response", request_id: str | None = None) -> None:
        self.content = MagicMock()
        self.content.parts = [MagicMock(text=text)]
        self.content.role = "model"
        self.usage_metadata = MagicMock()
        self.usage_metadata.prompt_token_count = 10
        self.usage_metadata.candidates_token_count = 20
        self.usage_metadata.total_token_count = 30
        self.request_id = request_id


class MockContent:
    """Mock ADK Content for testing."""

    def __init__(self, text: str = "test message") -> None:
        self.role = "user"
        self.parts = [MagicMock(text=text)]


class TestGalileoADKPluginInit:
    """Tests for plugin initialization."""

    def test_init_with_ingestion_hook_only(self) -> None:
        """Plugin initializes with only ingestion_hook (no credentials needed)."""
        traces: list = []
        plugin = GalileoADKPlugin(ingestion_hook=lambda r: traces.extend(r.traces))
        assert plugin._observer is not None

    def test_init_requires_project_or_hook(self) -> None:
        """Plugin raises error when neither project nor hook provided."""
        with pytest.raises(ValueError, match="Either 'project' or 'ingestion_hook'"):
            GalileoADKPlugin()

    def test_init_with_external_id(self) -> None:
        """Plugin accepts external_id for session grouping."""
        plugin = GalileoADKPlugin(
            ingestion_hook=lambda r: None,
            external_id="test-session-123",
        )
        assert plugin._observer is not None

    def test_init_with_static_metadata(self) -> None:
        """Plugin accepts static metadata in constructor."""
        plugin = GalileoADKPlugin(
            ingestion_hook=lambda r: None,
            metadata={"env": "test", "version": "1.0"},
        )
        assert plugin.metadata == {"env": "test", "version": "1.0"}


class TestGalileoADKPluginMetadata:
    """Tests for metadata property."""

    def test_metadata_get_set(self) -> None:
        """Metadata property can be get and set."""
        plugin = GalileoADKPlugin(ingestion_hook=lambda r: None)
        plugin.metadata = {"turn": 1, "user": "test"}
        assert plugin.metadata == {"turn": 1, "user": "test"}

    def test_metadata_none_becomes_empty_dict(self) -> None:
        """Setting metadata to None results in empty dict."""
        plugin = GalileoADKPlugin(ingestion_hook=lambda r: None)
        plugin.metadata = {"key": "value"}
        plugin.metadata = None
        assert plugin.metadata == {}

    def test_metadata_update_between_turns(self) -> None:
        """Metadata can be updated between turns."""
        plugin = GalileoADKPlugin(ingestion_hook=lambda r: None)

        plugin.metadata = {"turn": 1}
        assert plugin.metadata["turn"] == 1

        plugin.metadata = {"turn": 2}
        assert plugin.metadata["turn"] == 2


class TestGalileoADKPluginCallbacks:
    """Integration tests for plugin callbacks."""

    @pytest.fixture
    def captured_traces(self) -> list:
        return []

    @pytest.fixture
    def plugin(self, captured_traces: list) -> GalileoADKPlugin:
        return GalileoADKPlugin(ingestion_hook=lambda r: captured_traces.extend(r.traces))

    @pytest.mark.asyncio
    async def test_on_user_message_creates_run_span(self, plugin: GalileoADKPlugin) -> None:
        """on_user_message_callback creates a run span."""
        context = MockInvocationContext()
        message = MockContent("Hello")

        result = await plugin.on_user_message_callback(
            invocation_context=context,
            user_message=message,
        )

        assert result is None
        assert plugin._tracker.get_run(context.invocation_id) is not None

    @pytest.mark.asyncio
    async def test_before_agent_creates_agent_span(self, plugin: GalileoADKPlugin) -> None:
        """before_agent_callback creates an agent span."""
        invocation_id = str(uuid4())
        context = MockCallbackContext(invocation_id=invocation_id)

        # First create run span
        inv_context = MockInvocationContext(invocation_id=invocation_id)
        await plugin.on_user_message_callback(
            invocation_context=inv_context,
            user_message=MockContent(),
        )

        result = await plugin.before_agent_callback(callback_context=context)

        assert result is None
        assert plugin._tracker.agent_count == 1

    @pytest.mark.asyncio
    async def test_before_model_creates_llm_span(self, plugin: GalileoADKPlugin) -> None:
        """before_model_callback creates an LLM span."""
        invocation_id = str(uuid4())
        context = MockCallbackContext(invocation_id=invocation_id)
        request = MockLlmRequest()

        # Setup: create run and agent spans first
        inv_context = MockInvocationContext(invocation_id=invocation_id)
        await plugin.on_user_message_callback(
            invocation_context=inv_context,
            user_message=MockContent(),
        )
        await plugin.before_agent_callback(callback_context=context)

        result = await plugin.before_model_callback(
            callback_context=context,
            llm_request=request,
        )

        assert result is None
        assert plugin._tracker.llm_count == 1

    @pytest.mark.asyncio
    async def test_full_lifecycle_with_trace_capture(self, plugin: GalileoADKPlugin, captured_traces: list) -> None:
        """Full agent lifecycle produces captured traces."""
        invocation_id = str(uuid4())
        callback_context = MockCallbackContext(invocation_id=invocation_id)
        inv_context = MockInvocationContext(invocation_id=invocation_id)

        # Start run
        await plugin.on_user_message_callback(
            invocation_context=inv_context,
            user_message=MockContent("What is 2+2?"),
        )

        # Agent start
        await plugin.before_agent_callback(callback_context=callback_context)

        # LLM call
        await plugin.before_model_callback(
            callback_context=callback_context,
            llm_request=MockLlmRequest(),
        )
        await plugin.after_model_callback(
            callback_context=callback_context,
            llm_response=MockLlmResponse("4"),
        )

        # Agent end
        await plugin.after_agent_callback(callback_context=callback_context)

        # End run
        await plugin.after_run_callback(invocation_context=inv_context)

        # Verify traces were captured
        assert len(captured_traces) >= 1

    @pytest.mark.asyncio
    async def test_metadata_appears_on_spans(self, plugin: GalileoADKPlugin, captured_traces: list) -> None:
        """Metadata set on plugin appears on captured spans."""
        plugin.metadata = {"turn": 1, "user_id": "test-user"}

        invocation_id = str(uuid4())
        callback_context = MockCallbackContext(invocation_id=invocation_id)
        inv_context = MockInvocationContext(invocation_id=invocation_id)

        # Run full lifecycle
        await plugin.on_user_message_callback(
            invocation_context=inv_context,
            user_message=MockContent(),
        )
        await plugin.before_agent_callback(callback_context=callback_context)
        await plugin.after_agent_callback(callback_context=callback_context)
        await plugin.after_run_callback(invocation_context=inv_context)

        # Check metadata on captured traces
        assert len(captured_traces) >= 1
        for trace in captured_traces:
            for span in getattr(trace, "spans", []):
                metadata = getattr(span, "metadata", {})
                if metadata and "turn" in metadata:
                    assert metadata["turn"] == 1


class TestGalileoADKPluginErrorHandling:
    """Tests for error handling in callbacks."""

    @pytest.fixture
    def plugin(self) -> GalileoADKPlugin:
        return GalileoADKPlugin(ingestion_hook=lambda r: None)

    @pytest.mark.asyncio
    async def test_callback_errors_dont_propagate(self, plugin: GalileoADKPlugin) -> None:
        """Errors in callbacks don't propagate to caller."""
        # Pass invalid context - should not raise
        result = await plugin.before_agent_callback(callback_context=None)
        assert result is None

    @pytest.mark.asyncio
    async def test_model_error_callback_extracts_status_code(self, plugin: GalileoADKPlugin) -> None:
        """on_model_error_callback handles errors gracefully."""
        invocation_id = str(uuid4())
        context = MockCallbackContext(invocation_id=invocation_id)

        # Setup spans
        inv_context = MockInvocationContext(invocation_id=invocation_id)
        await plugin.on_user_message_callback(
            invocation_context=inv_context,
            user_message=MockContent(),
        )
        await plugin.before_agent_callback(callback_context=context)

        # Setup LLM span
        llm_request = MockLlmRequest()
        await plugin.before_model_callback(
            callback_context=context,
            llm_request=llm_request,
        )

        # Create error with status code
        error = Exception("Rate limit exceeded")
        error.code = 429  # type: ignore[attr-defined]

        result = await plugin.on_model_error_callback(
            callback_context=context,
            llm_request=llm_request,
            error=error,
        )

        assert result is None  # Error handled gracefully


class MockToolContext:
    """Mock ADK ToolContext for testing."""

    def __init__(self, invocation_id: str, agent_name: str = "test_agent", session_id: str = "test_session") -> None:
        self.invocation_id = invocation_id
        self.callback_context = MagicMock()
        self.callback_context.agent_name = agent_name
        self.callback_context.invocation_id = invocation_id
        self.callback_context.session = MagicMock()
        self.callback_context.session.session_id = session_id


class MockTool:
    """Mock ADK BaseTool for testing."""

    def __init__(self, name: str = "test_tool") -> None:
        self.name = name


class TestInvocationScopedToolTracking:
    """Tests for invocation-scoped tool tracking (ParallelAgent support)."""

    @pytest.fixture
    def plugin(self) -> GalileoADKPlugin:
        return GalileoADKPlugin(ingestion_hook=lambda r: None)

    @pytest.mark.asyncio
    async def test_tool_tracking_isolated_per_session(self, plugin: GalileoADKPlugin) -> None:
        """Tools in different sessions have isolated active tool tracking."""
        inv_id_1 = str(uuid4())
        inv_id_2 = str(uuid4())
        session_id_1 = "session_1"
        session_id_2 = "session_2"

        # Setup invocation 1 with session 1
        inv_context_1 = MockInvocationContext(invocation_id=inv_id_1)
        inv_context_1.session.session_id = session_id_1
        await plugin.on_user_message_callback(
            invocation_context=inv_context_1,
            user_message=MockContent(),
        )
        callback_context_1 = MockCallbackContext(invocation_id=inv_id_1)
        await plugin.before_agent_callback(callback_context=callback_context_1)

        # Setup invocation 2 with session 2
        inv_context_2 = MockInvocationContext(invocation_id=inv_id_2)
        inv_context_2.session.session_id = session_id_2
        await plugin.on_user_message_callback(
            invocation_context=inv_context_2,
            user_message=MockContent(),
        )
        callback_context_2 = MockCallbackContext(invocation_id=inv_id_2)
        await plugin.before_agent_callback(callback_context=callback_context_2)

        # Start tool in invocation 1 (session 1)
        tool_1 = MockTool("tool_A")
        tool_context_1 = MockToolContext(inv_id_1, session_id=session_id_1)
        await plugin.before_tool_callback(
            tool=tool_1,
            tool_args={"arg": "value1"},
            tool_context=tool_context_1,
        )

        # Active tool for session 1 should be set
        assert plugin._tracker.get_active_tool(session_id_1) is not None

        # Active tool for session 2 should NOT be set (sessions are isolated)
        assert plugin._tracker.get_active_tool(session_id_2) is None

    @pytest.mark.asyncio
    async def test_concurrent_tools_different_sessions(self, plugin: GalileoADKPlugin) -> None:
        """Concurrent tools in different sessions track correctly."""
        inv_id_1 = str(uuid4())
        inv_id_2 = str(uuid4())
        session_id_1 = "session_1"
        session_id_2 = "session_2"

        # Setup both invocations with different sessions
        for inv_id, session_id in [(inv_id_1, session_id_1), (inv_id_2, session_id_2)]:
            inv_context = MockInvocationContext(invocation_id=inv_id)
            inv_context.session.session_id = session_id
            await plugin.on_user_message_callback(
                invocation_context=inv_context,
                user_message=MockContent(),
            )
            callback_context = MockCallbackContext(invocation_id=inv_id)
            await plugin.before_agent_callback(callback_context=callback_context)

        # Start tool A in invocation 1 (session 1)
        tool_a = MockTool("tool_A")
        tool_context_a = MockToolContext(inv_id_1, session_id=session_id_1)
        await plugin.before_tool_callback(
            tool=tool_a,
            tool_args={},
            tool_context=tool_context_a,
        )
        active_tool_1 = plugin._tracker.get_active_tool(session_id_1)

        # Start tool B in invocation 2 (session 2)
        tool_b = MockTool("tool_B")
        tool_context_b = MockToolContext(inv_id_2, session_id=session_id_2)
        await plugin.before_tool_callback(
            tool=tool_b,
            tool_args={},
            tool_context=tool_context_b,
        )
        active_tool_2 = plugin._tracker.get_active_tool(session_id_2)

        # Both tools should be tracked independently
        assert active_tool_1 is not None
        assert active_tool_2 is not None
        assert active_tool_1 != active_tool_2

        # End tool A - should only affect session 1
        await plugin.after_tool_callback(
            tool=tool_a,
            tool_args={},
            tool_context=tool_context_a,
            result={"status": "done"},
        )

        # Tool A cleared, Tool B still active
        assert plugin._tracker.get_active_tool(session_id_1) is None
        assert plugin._tracker.get_active_tool(session_id_2) is not None

    @pytest.mark.asyncio
    async def test_sub_invocation_parented_to_tool_via_session(self, plugin: GalileoADKPlugin) -> None:
        """Sub-invocation with different invocation_id but same session_id is parented to tool.

        This tests the key fix: when a tool invokes a sub-agent, the sub-agent gets a NEW
        invocation_id but shares the same session_id. The sub-invocation should find the
        parent tool via session_id and be nested under it in the trace hierarchy.
        """
        parent_inv_id = str(uuid4())
        child_inv_id = str(uuid4())  # Different invocation_id for sub-agent
        shared_session_id = "shared_session_123"  # Same session_id

        # Setup parent invocation
        parent_inv_context = MockInvocationContext(invocation_id=parent_inv_id)
        parent_inv_context.session.session_id = shared_session_id
        await plugin.on_user_message_callback(
            invocation_context=parent_inv_context,
            user_message=MockContent(),
        )
        parent_callback = MockCallbackContext(invocation_id=parent_inv_id)
        await plugin.before_agent_callback(callback_context=parent_callback)

        # Start tool in parent invocation (this tool will invoke a sub-agent)
        tool = MockTool("transfer_to_agent")
        tool_context = MockToolContext(parent_inv_id, session_id=shared_session_id)
        await plugin.before_tool_callback(
            tool=tool,
            tool_args={},
            tool_context=tool_context,
        )
        tool_run_id = plugin._tracker.get_active_tool(shared_session_id)
        assert tool_run_id is not None

        # Sub-invocation with DIFFERENT invocation_id but SAME session_id
        # This simulates what happens when a tool spawns a sub-agent
        child_inv_context = MockInvocationContext(invocation_id=child_inv_id)
        child_inv_context.session.session_id = shared_session_id  # SAME session

        # The sub-invocation should find the parent tool via session_id
        await plugin.on_user_message_callback(
            invocation_context=child_inv_context,
            user_message=MockContent("sub-agent query"),
        )

        # Verify the sub-invocation's run was registered
        sub_run_id = plugin._tracker.get_run(child_inv_id)
        assert sub_run_id is not None

        # The parent tool should still be active (we're inside the tool call)
        assert plugin._tracker.get_active_tool(shared_session_id) == tool_run_id

        # End the sub-invocation
        await plugin.after_run_callback(invocation_context=child_inv_context)

        # End the tool
        await plugin.after_tool_callback(
            tool=tool,
            tool_args={},
            tool_context=tool_context,
            result={"sub_agent_result": "success"},
        )

        # Active tool should now be cleared
        assert plugin._tracker.get_active_tool(shared_session_id) is None

    @pytest.mark.asyncio
    async def test_tool_parent_fallback_to_run_when_no_agent(self, plugin: GalileoADKPlugin) -> None:
        """Tool falls back to invocation run when agent_name is not available."""
        invocation_id = str(uuid4())
        session_id = "test_session"

        # Given: an invocation with a run but NO agent span
        inv_context = MockInvocationContext(invocation_id=invocation_id)
        inv_context.session.session_id = session_id
        await plugin.on_user_message_callback(
            invocation_context=inv_context,
            user_message=MockContent(),
        )
        run_id = plugin._tracker.get_run(invocation_id)
        assert run_id is not None

        # When: starting a tool with no agent_name in context
        tool = MockTool("test_tool")
        tool_context = MockToolContext(invocation_id=invocation_id, session_id=session_id)
        tool_context.callback_context.agent_name = None  # No agent available
        await plugin.before_tool_callback(tool=tool, tool_args={}, tool_context=tool_context)

        # Then: tool should be registered (fallback to run worked)
        assert plugin._tracker.tool_count == 1

    @pytest.mark.asyncio
    async def test_tool_parent_fallback_to_active_tool(self, plugin: GalileoADKPlugin) -> None:
        """Tool falls back to active tool when no agent or run is available."""
        invocation_id = str(uuid4())
        session_id = "test_session"

        # Given: a session with an active tool but no run registered for this invocation
        # (simulates a nested tool call scenario)
        parent_tool_run_id = uuid4()
        plugin._tracker.set_active_tool(session_id, parent_tool_run_id)

        # When: starting a tool with no agent and no run
        tool = MockTool("nested_tool")
        tool_context = MockToolContext(invocation_id=invocation_id, session_id=session_id)
        tool_context.callback_context.agent_name = None  # No agent available
        await plugin.before_tool_callback(tool=tool, tool_args={}, tool_context=tool_context)

        # Then: tool should be registered (fallback to active tool worked)
        assert plugin._tracker.tool_count == 1


class TestGetParentAgentRunId:
    """Tests for _get_parent_agent_run_id helper method."""

    @pytest.fixture
    def plugin(self) -> GalileoADKPlugin:
        return GalileoADKPlugin(ingestion_hook=lambda r: None)

    @pytest.mark.asyncio
    async def test_finds_parent_agent_via_hierarchy(self, plugin: GalileoADKPlugin) -> None:
        """Parent agent run_id found via ADK's parent_agent hierarchy."""
        # Given: a parent agent and child agent setup
        invocation_id = str(uuid4())
        inv_context = MockInvocationContext(invocation_id=invocation_id)
        await plugin.on_user_message_callback(
            invocation_context=inv_context,
            user_message=MockContent(),
        )

        # Register parent agent
        parent_callback = MockCallbackContext(agent_name="parent_agent", invocation_id=invocation_id)
        await plugin.before_agent_callback(callback_context=parent_callback)
        parent_run_id = plugin._tracker.get_agent(invocation_id, "parent_agent")

        # Create child context with parent_agent reference
        child_callback = MagicMock()
        child_callback.agent_name = "child_agent"
        child_callback.invocation_id = invocation_id
        child_callback._invocation_context = MagicMock()
        child_callback._invocation_context.agent = MagicMock()
        child_callback._invocation_context.agent.parent_agent = MagicMock()
        child_callback._invocation_context.agent.parent_agent.name = "parent_agent"

        # When: getting parent agent run_id
        result = plugin._get_parent_agent_run_id(child_callback)

        # Then: parent agent's run_id is returned
        assert result == parent_run_id

    @pytest.mark.asyncio
    async def test_fallback_to_root_invocation(self, plugin: GalileoADKPlugin) -> None:
        """Falls back to root invocation run_id when no parent agent."""
        # Given: a run span without any agents
        invocation_id = str(uuid4())
        inv_context = MockInvocationContext(invocation_id=invocation_id)
        await plugin.on_user_message_callback(
            invocation_context=inv_context,
            user_message=MockContent(),
        )
        run_id = plugin._tracker.get_run(invocation_id)

        # Create context without parent_agent hierarchy
        callback = MockCallbackContext(invocation_id=invocation_id)

        # When: getting parent agent run_id
        result = plugin._get_parent_agent_run_id(callback)

        # Then: root run_id is returned as fallback
        assert result == run_id

    def test_handles_exception_in_hierarchy_traversal(self, plugin: GalileoADKPlugin) -> None:
        """Handles exceptions gracefully when traversing hierarchy."""
        # Given: a context that raises when accessing hierarchy
        callback = MagicMock()
        callback.invocation_id = "test_inv"
        callback._invocation_context = MagicMock()
        callback._invocation_context.agent = property(lambda self: 1 / 0)  # Raises

        # When: getting parent agent run_id
        result = plugin._get_parent_agent_run_id(callback)

        # Then: None is returned (no crash)
        assert result is None


class TestForceCommitPartialTrace:
    """Tests for _force_commit_partial_trace helper method."""

    @pytest.fixture
    def plugin(self) -> GalileoADKPlugin:
        return GalileoADKPlugin(ingestion_hook=lambda r: None)

    @pytest.mark.asyncio
    async def test_closes_all_open_agent_spans(self, plugin: GalileoADKPlugin) -> None:
        """All open agent spans are closed with error status."""
        # Given: an invocation with an open agent span
        invocation_id = str(uuid4())
        inv_context = MockInvocationContext(invocation_id=invocation_id)
        await plugin.on_user_message_callback(
            invocation_context=inv_context,
            user_message=MockContent(),
        )
        callback = MockCallbackContext(invocation_id=invocation_id)
        await plugin.before_agent_callback(callback_context=callback)

        # Verify agent is registered
        assert plugin._tracker.get_agent(invocation_id, "test_agent") is not None

        # When: force committing partial trace
        error = Exception("Fatal error")
        plugin._force_commit_partial_trace(invocation_id, error)

        # Then: agent span is closed (removed from tracker)
        assert plugin._tracker.get_agent(invocation_id, "test_agent") is None

    @pytest.mark.asyncio
    async def test_closes_run_span_with_error_status(self, plugin: GalileoADKPlugin) -> None:
        """Run span is closed with error output and status code."""
        # Given: an invocation with a run span
        invocation_id = str(uuid4())
        inv_context = MockInvocationContext(invocation_id=invocation_id)
        await plugin.on_user_message_callback(
            invocation_context=inv_context,
            user_message=MockContent(),
        )

        # Verify run is registered
        assert plugin._tracker.get_run(invocation_id) is not None

        # When: force committing partial trace
        error = Exception("429 RESOURCE_EXHAUSTED")
        plugin._force_commit_partial_trace(invocation_id, error)

        # Then: run span is closed (removed from tracker)
        assert plugin._tracker.get_run(invocation_id) is None

    @pytest.mark.asyncio
    async def test_status_code_extracted_from_error(self, plugin: GalileoADKPlugin) -> None:
        """Status code is extracted from error for span closure."""
        # Given: an invocation with spans
        invocation_id = str(uuid4())
        inv_context = MockInvocationContext(invocation_id=invocation_id)
        await plugin.on_user_message_callback(
            invocation_context=inv_context,
            user_message=MockContent(),
        )
        callback = MockCallbackContext(invocation_id=invocation_id)
        await plugin.before_agent_callback(callback_context=callback)

        # When: force committing with error that has status_code
        error = Exception("Rate limited")
        error.status_code = 429  # type: ignore[attr-defined]
        plugin._force_commit_partial_trace(invocation_id, error)

        # Then: no crash and spans are cleaned up
        assert plugin._tracker.get_run(invocation_id) is None
        assert plugin._tracker.get_agent(invocation_id, "test_agent") is None

    @pytest.mark.asyncio
    async def test_closes_all_open_tool_spans(self, plugin: GalileoADKPlugin) -> None:
        """All open tool spans are closed with error status."""
        # Given: an invocation with an open tool span
        invocation_id = str(uuid4())
        session_id = "test_session"
        inv_context = MockInvocationContext(invocation_id=invocation_id)
        inv_context.session.session_id = session_id
        await plugin.on_user_message_callback(
            invocation_context=inv_context,
            user_message=MockContent(),
        )
        callback = MockCallbackContext(invocation_id=invocation_id)
        await plugin.before_agent_callback(callback_context=callback)

        tool = MockTool(name="test_tool")
        tool_context = MockToolContext(invocation_id=invocation_id, session_id=session_id)
        await plugin.before_tool_callback(tool=tool, tool_args={}, tool_context=tool_context)

        # Verify tool is registered
        assert plugin._tracker.tool_count == 1

        # When: force committing partial trace
        error = Exception("Fatal error")
        plugin._force_commit_partial_trace(invocation_id, error)

        # Then: tool span is closed (removed from tracker)
        assert plugin._tracker.tool_count == 0

    @pytest.mark.asyncio
    async def test_closes_all_open_llm_spans(self, plugin: GalileoADKPlugin) -> None:
        """All open LLM spans are closed with error status."""
        # Given: an invocation with an open LLM span
        invocation_id = str(uuid4())
        inv_context = MockInvocationContext(invocation_id=invocation_id)
        await plugin.on_user_message_callback(
            invocation_context=inv_context,
            user_message=MockContent(),
        )
        callback = MockCallbackContext(invocation_id=invocation_id)
        await plugin.before_agent_callback(callback_context=callback)
        await plugin.before_model_callback(callback_context=callback, llm_request=MockLlmRequest())

        # Verify LLM is registered
        assert plugin._tracker.llm_count == 1

        # When: force committing partial trace
        error = Exception("Fatal error")
        plugin._force_commit_partial_trace(invocation_id, error)

        # Then: LLM span is closed (removed from tracker)
        assert plugin._tracker.llm_count == 0

    @pytest.mark.asyncio
    async def test_clears_active_tool_on_force_commit(self, plugin: GalileoADKPlugin) -> None:
        """Active tool is cleared when force committing partial trace."""
        # Given: an invocation with an active tool
        invocation_id = str(uuid4())
        session_id = "test_session"
        inv_context = MockInvocationContext(invocation_id=invocation_id)
        inv_context.session.session_id = session_id
        await plugin.on_user_message_callback(
            invocation_context=inv_context,
            user_message=MockContent(),
        )
        callback = MockCallbackContext(invocation_id=invocation_id)
        await plugin.before_agent_callback(callback_context=callback)

        tool = MockTool(name="test_tool")
        tool_context = MockToolContext(invocation_id=invocation_id, session_id=session_id)
        await plugin.before_tool_callback(tool=tool, tool_args={}, tool_context=tool_context)

        # Verify active tool is set
        assert plugin._tracker.get_active_tool(session_id) is not None

        # When: force committing partial trace
        error = Exception("Fatal error")
        plugin._force_commit_partial_trace(invocation_id, error)

        # Then: active tool is cleared
        assert plugin._tracker.get_active_tool(session_id) is None


class TestAfterRunCallbackCleanup:
    """Tests for after_run_callback cleanup of orphaned spans."""

    @pytest.fixture
    def plugin(self) -> GalileoADKPlugin:
        return GalileoADKPlugin(ingestion_hook=lambda r: None)

    @pytest.mark.asyncio
    async def test_cleans_up_orphaned_tools(self, plugin: GalileoADKPlugin) -> None:
        """Orphaned tool spans are closed on after_run_callback."""
        # Given: an invocation with a tool that wasn't closed
        invocation_id = str(uuid4())
        inv_context = MockInvocationContext(invocation_id=invocation_id)
        await plugin.on_user_message_callback(
            invocation_context=inv_context,
            user_message=MockContent(),
        )
        callback = MockCallbackContext(invocation_id=invocation_id)
        await plugin.before_agent_callback(callback_context=callback)

        tool = MockTool("orphan_tool")
        tool_context = MockToolContext(invocation_id)
        await plugin.before_tool_callback(
            tool=tool,
            tool_args={},
            tool_context=tool_context,
        )

        # Verify tool is tracked
        assert plugin._tracker.tool_count > 0

        # When: after_run_callback is called (simulating run end without tool close)
        await plugin.after_agent_callback(callback_context=callback)
        await plugin.after_run_callback(invocation_context=inv_context)

        # Then: tool span is cleaned up
        assert plugin._tracker.tool_count == 0

    @pytest.mark.asyncio
    async def test_cleans_up_orphaned_llms(self, plugin: GalileoADKPlugin) -> None:
        """Orphaned LLM spans are closed on after_run_callback."""
        # Given: an invocation with an LLM that wasn't closed
        invocation_id = str(uuid4())
        inv_context = MockInvocationContext(invocation_id=invocation_id)
        await plugin.on_user_message_callback(
            invocation_context=inv_context,
            user_message=MockContent(),
        )
        callback = MockCallbackContext(invocation_id=invocation_id)
        await plugin.before_agent_callback(callback_context=callback)

        request = MockLlmRequest()
        await plugin.before_model_callback(
            callback_context=callback,
            llm_request=request,
        )

        # Verify LLM is tracked
        assert plugin._tracker.llm_count > 0

        # When: after_run_callback is called (simulating run end without LLM close)
        await plugin.after_agent_callback(callback_context=callback)
        await plugin.after_run_callback(invocation_context=inv_context)

        # Then: LLM span is cleaned up
        assert plugin._tracker.llm_count == 0

    @pytest.mark.asyncio
    async def test_cleans_up_orphaned_agents(self, plugin: GalileoADKPlugin) -> None:
        """Orphaned agent spans are closed on after_run_callback."""
        # Given: an invocation with an agent that wasn't closed
        invocation_id = str(uuid4())
        inv_context = MockInvocationContext(invocation_id=invocation_id)
        await plugin.on_user_message_callback(
            invocation_context=inv_context,
            user_message=MockContent(),
        )
        callback = MockCallbackContext(invocation_id=invocation_id)
        await plugin.before_agent_callback(callback_context=callback)

        # Verify agent is tracked
        assert plugin._tracker.agent_count > 0

        # When: after_run_callback is called without after_agent_callback
        await plugin.after_run_callback(invocation_context=inv_context)

        # Then: agent span is cleaned up
        assert plugin._tracker.agent_count == 0

    @pytest.mark.asyncio
    async def test_tool_error_clears_active_tool(self, plugin: GalileoADKPlugin) -> None:
        """Tool error properly clears the active tool for the session."""
        inv_id = str(uuid4())
        session_id = "test_session_error"

        # Setup invocation
        inv_context = MockInvocationContext(invocation_id=inv_id)
        inv_context.session.session_id = session_id
        await plugin.on_user_message_callback(
            invocation_context=inv_context,
            user_message=MockContent(),
        )
        callback_context = MockCallbackContext(invocation_id=inv_id)
        await plugin.before_agent_callback(callback_context=callback_context)

        # Start tool
        tool = MockTool("failing_tool")
        tool_context = MockToolContext(inv_id, session_id=session_id)
        await plugin.before_tool_callback(
            tool=tool,
            tool_args={},
            tool_context=tool_context,
        )

        assert plugin._tracker.get_active_tool(session_id) is not None

        # Tool errors
        error = Exception("Tool failed")
        await plugin.on_tool_error_callback(
            tool=tool,
            tool_args={},
            tool_context=tool_context,
            error=error,
        )

        # Active tool should be cleared
        assert plugin._tracker.get_active_tool(session_id) is None
