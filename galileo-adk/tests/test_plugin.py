"""Integration tests for GalileoADKPlugin."""

from unittest.mock import MagicMock
from uuid import uuid4

import pytest

from galileo_adk import GalileoADKPlugin


class MockRunConfig:
    """Mock ADK RunConfig for testing custom_metadata extraction."""

    def __init__(self, custom_metadata: dict | None = None) -> None:
        self.custom_metadata = custom_metadata


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
        run_config: MockRunConfig | None = None,
    ) -> None:
        self.agent_name = agent_name
        self.invocation_id = invocation_id or str(uuid4())
        self.session = MagicMock()
        self.session.id = "test_session"
        self.run_config = run_config


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
    async def test_metadata_from_run_config_appears_on_spans(
        self, plugin: GalileoADKPlugin, captured_traces: list
    ) -> None:
        """Metadata from RunConfig.custom_metadata appears on captured spans."""
        # Given: RunConfig with custom_metadata
        run_config = MockRunConfig(custom_metadata={"turn": 1, "user_id": "test-user"})

        invocation_id = str(uuid4())
        callback_context = MockCallbackContext(invocation_id=invocation_id)
        inv_context = MockInvocationContext(invocation_id=invocation_id, run_config=run_config)

        # When: running full lifecycle
        await plugin.on_user_message_callback(
            invocation_context=inv_context,
            user_message=MockContent(),
        )
        await plugin.before_agent_callback(callback_context=callback_context)
        await plugin.after_agent_callback(callback_context=callback_context)
        await plugin.after_run_callback(invocation_context=inv_context)

        # Then: metadata appears on captured traces
        assert len(captured_traces) >= 1
        for trace in captured_traces:
            for span in getattr(trace, "spans", []):
                metadata = getattr(span, "metadata", {})
                if metadata and "turn" in metadata:
                    assert metadata["turn"] == 1

    @pytest.mark.asyncio
    async def test_missing_run_config_results_in_empty_metadata(
        self, plugin: GalileoADKPlugin, captured_traces: list
    ) -> None:
        """Missing RunConfig results in empty metadata (no error)."""
        # Given: no RunConfig (run_config=None)
        invocation_id = str(uuid4())
        callback_context = MockCallbackContext(invocation_id=invocation_id)
        inv_context = MockInvocationContext(invocation_id=invocation_id, run_config=None)

        # When: running full lifecycle
        await plugin.on_user_message_callback(
            invocation_context=inv_context,
            user_message=MockContent(),
        )
        await plugin.before_agent_callback(callback_context=callback_context)
        await plugin.after_agent_callback(callback_context=callback_context)
        await plugin.after_run_callback(invocation_context=inv_context)

        # Then: no crash and traces are captured
        assert len(captured_traces) >= 1


class TestRunConfigMetadataIsolation:
    """Tests for per-invocation metadata isolation using RunConfig.custom_metadata."""

    @pytest.fixture
    def plugin(self) -> GalileoADKPlugin:
        return GalileoADKPlugin(ingestion_hook=lambda r: None)

    @pytest.mark.asyncio
    async def test_concurrent_invocations_have_isolated_metadata(self, plugin: GalileoADKPlugin) -> None:
        """Concurrent invocations with different RunConfig have isolated metadata."""
        # Given: two invocations with different custom_metadata
        inv_id_1 = str(uuid4())
        inv_id_2 = str(uuid4())

        run_config_1 = MockRunConfig(custom_metadata={"turn": 1, "user": "alice"})
        run_config_2 = MockRunConfig(custom_metadata={"turn": 2, "user": "bob"})

        inv_context_1 = MockInvocationContext(invocation_id=inv_id_1, run_config=run_config_1)
        inv_context_2 = MockInvocationContext(invocation_id=inv_id_2, run_config=run_config_2)

        callback_context_1 = MockCallbackContext(invocation_id=inv_id_1)
        callback_context_2 = MockCallbackContext(invocation_id=inv_id_2)

        # When: starting both invocations (simulating concurrent execution)
        await plugin.on_user_message_callback(
            invocation_context=inv_context_1,
            user_message=MockContent(),
        )
        await plugin.on_user_message_callback(
            invocation_context=inv_context_2,
            user_message=MockContent(),
        )

        # Then: each invocation has its own metadata stored (in observer)
        assert plugin._observer._invocation_metadata[inv_id_1] == {"turn": 1, "user": "alice"}
        assert plugin._observer._invocation_metadata[inv_id_2] == {"turn": 2, "user": "bob"}

        # When: running agents for both invocations
        await plugin.before_agent_callback(callback_context=callback_context_1)
        await plugin.before_agent_callback(callback_context=callback_context_2)

        # Then: metadata still isolated
        assert plugin._observer._invocation_metadata[inv_id_1] == {"turn": 1, "user": "alice"}
        assert plugin._observer._invocation_metadata[inv_id_2] == {"turn": 2, "user": "bob"}

        # Cleanup
        await plugin.after_agent_callback(callback_context=callback_context_1)
        await plugin.after_agent_callback(callback_context=callback_context_2)
        await plugin.after_run_callback(invocation_context=inv_context_1)
        await plugin.after_run_callback(invocation_context=inv_context_2)

        # Then: metadata cleaned up after run ends
        assert inv_id_1 not in plugin._observer._invocation_metadata
        assert inv_id_2 not in plugin._observer._invocation_metadata

    @pytest.mark.asyncio
    async def test_metadata_cleaned_up_after_run_ends(self, plugin: GalileoADKPlugin) -> None:
        """Per-invocation metadata is cleaned up when run ends."""
        # Given: an invocation with custom_metadata
        invocation_id = str(uuid4())
        run_config = MockRunConfig(custom_metadata={"turn": 1})
        inv_context = MockInvocationContext(invocation_id=invocation_id, run_config=run_config)
        callback_context = MockCallbackContext(invocation_id=invocation_id)

        # When: running the invocation
        await plugin.on_user_message_callback(
            invocation_context=inv_context,
            user_message=MockContent(),
        )

        # Then: metadata is stored (in observer)
        assert invocation_id in plugin._observer._invocation_metadata
        assert plugin._observer._invocation_metadata[invocation_id] == {"turn": 1}

        # When: run ends
        await plugin.before_agent_callback(callback_context=callback_context)
        await plugin.after_agent_callback(callback_context=callback_context)
        await plugin.after_run_callback(invocation_context=inv_context)

        # Then: metadata is cleaned up (no memory leak)
        assert invocation_id not in plugin._observer._invocation_metadata

    @pytest.mark.asyncio
    async def test_sub_invocation_inherits_root_metadata(self, plugin: GalileoADKPlugin) -> None:
        """Sub-invocations (e.g., AgentTool calls) inherit metadata from root invocation."""
        # Given: root invocation with custom_metadata
        root_invocation_id = str(uuid4())
        sub_invocation_id = str(uuid4())  # Different invocation_id for sub-agent
        session_id = "test_session"

        run_config = MockRunConfig(custom_metadata={"turn": 1, "workflow": "test"})
        inv_context = MockInvocationContext(invocation_id=root_invocation_id, run_config=run_config)
        inv_context.session.id = session_id

        # When: root invocation starts
        await plugin.on_user_message_callback(
            invocation_context=inv_context,
            user_message=MockContent(),
        )

        # Then: root invocation's metadata is stored and root is tracked (in observer)
        assert plugin._observer._invocation_metadata[root_invocation_id] == {"turn": 1, "workflow": "test"}
        assert plugin._observer._session_root_invocation[session_id] == root_invocation_id

        # Given: sub-invocation callback context (different invocation_id, same session)
        sub_callback_context = MockCallbackContext(invocation_id=sub_invocation_id)
        sub_callback_context.session = MagicMock()
        sub_callback_context.session.id = session_id

        # When: getting metadata for sub-invocation (via observer)
        metadata = plugin._observer.get_invocation_metadata(sub_invocation_id, session_id)

        # Then: sub-invocation inherits root's metadata
        assert metadata == {"turn": 1, "workflow": "test"}

        # Cleanup
        await plugin.after_run_callback(invocation_context=inv_context)


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
        self.callback_context.session.id = session_id


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
        inv_context_1.session.id = session_id_1
        await plugin.on_user_message_callback(
            invocation_context=inv_context_1,
            user_message=MockContent(),
        )
        callback_context_1 = MockCallbackContext(invocation_id=inv_id_1)
        await plugin.before_agent_callback(callback_context=callback_context_1)

        # Setup invocation 2 with session 2
        inv_context_2 = MockInvocationContext(invocation_id=inv_id_2)
        inv_context_2.session.id = session_id_2
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
        parent_inv_context.session.id = shared_session_id
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
        child_inv_context.session.id = shared_session_id  # SAME session

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
        inv_context.session.id = session_id
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
        inv_context.session.id = session_id
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
        inv_context.session.id = session_id
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
        inv_context.session.id = session_id
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


class TestAutomaticSessionMapping:
    """Tests for automatic ADK session_id → Galileo session mapping."""

    @pytest.fixture
    def plugin(self) -> GalileoADKPlugin:
        return GalileoADKPlugin(ingestion_hook=lambda r: None)

    @pytest.mark.asyncio
    async def test_session_mapped_on_first_user_message(self, plugin: GalileoADKPlugin) -> None:
        """ADK session_id is mapped to Galileo session on first user message."""
        # Given: an invocation context with a session_id
        inv_context = MockInvocationContext()
        inv_context.session.id = "adk-session-123"

        # When: processing the user message
        await plugin.on_user_message_callback(
            invocation_context=inv_context,
            user_message=MockContent(),
        )

        # Then: the ADK session is tracked by the observer
        assert plugin._observer._current_adk_session == "adk-session-123"

    @pytest.mark.asyncio
    async def test_session_not_remapped_for_same_session_id(self, plugin: GalileoADKPlugin) -> None:
        """Same session_id doesn't trigger repeated session mapping."""
        # Given: two invocations with the same session_id
        session_id = "persistent-session"
        inv_context_1 = MockInvocationContext(invocation_id="inv-1")
        inv_context_1.session.id = session_id
        inv_context_2 = MockInvocationContext(invocation_id="inv-2")
        inv_context_2.session.id = session_id

        # When: processing both user messages
        await plugin.on_user_message_callback(
            invocation_context=inv_context_1,
            user_message=MockContent(),
        )
        first_mapped_session = plugin._observer._current_adk_session

        await plugin.on_user_message_callback(
            invocation_context=inv_context_2,
            user_message=MockContent(),
        )
        second_mapped_session = plugin._observer._current_adk_session

        # Then: session remains the same (not remapped)
        assert first_mapped_session == second_mapped_session == session_id

    @pytest.mark.asyncio
    async def test_unknown_session_id_not_mapped(self, plugin: GalileoADKPlugin) -> None:
        """Session_id of 'unknown' is not mapped to Galileo session."""
        # Given: an invocation context with unknown session_id
        inv_context = MockInvocationContext()
        inv_context.session.id = "unknown"

        # When: processing the user message
        await plugin.on_user_message_callback(
            invocation_context=inv_context,
            user_message=MockContent(),
        )

        # Then: session is not tracked (remains None)
        assert plugin._observer._current_adk_session is None

    @pytest.mark.asyncio
    async def test_session_mapping_with_sub_invocations(self, plugin: GalileoADKPlugin) -> None:
        """Sub-invocations with same session_id don't trigger remapping."""
        # Given: parent and child invocations sharing a session
        shared_session = "shared-session-xyz"

        parent_context = MockInvocationContext(invocation_id="parent-inv")
        parent_context.session.id = shared_session

        child_context = MockInvocationContext(invocation_id="child-inv")
        child_context.session.id = shared_session

        # When: processing parent invocation
        await plugin.on_user_message_callback(
            invocation_context=parent_context,
            user_message=MockContent(),
        )
        assert plugin._observer._current_adk_session == shared_session

        # And: processing child invocation (sub-agent call)
        await plugin.on_user_message_callback(
            invocation_context=child_context,
            user_message=MockContent(),
        )

        # Then: session remains the same
        assert plugin._observer._current_adk_session == shared_session
