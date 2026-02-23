import sys
import uuid
from datetime import datetime
from typing import Any
from unittest.mock import Mock, patch

import pytest

# Skip all tests in this module on Python 3.14+ (crewai doesn't support it yet)
pytestmark = pytest.mark.skipif(sys.version_info >= (3, 14), reason="crewai does not support Python 3.14+")

from galileo.handlers.crewai.handler import CrewAIEventListener  # noqa: E402
from galileo.schema.handlers import NodeType  # noqa: E402
from tests.testutils.setup import (  # noqa: E402
    setup_mock_logstreams_client,
    setup_mock_projects_client,
    setup_mock_traces_client,
)


class MockEvent:
    """Mock CrewAI event for testing."""

    def __init__(self, **kwargs):
        self.timestamp = datetime.now()
        for key, value in kwargs.items():
            setattr(self, key, value)

    def to_json(self) -> dict[str, Any]:
        """Convert event to JSON format."""
        result = {}
        for key, value in self.__dict__.items():
            if key != "timestamp":
                result[key] = value
        return result


class MockSource:
    """Mock source object for CrewAI events."""

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)


class MockTask:
    """Mock CrewAI task."""

    def __init__(self, task_id=None, description="Test task", agent=None):
        self.id = task_id or uuid.uuid4()
        self.description = description
        self.agent = agent


class MockAgent:
    """Mock CrewAI agent."""

    def __init__(self, agent_id=None, role="Test Agent", crew=None):
        self.id = agent_id or uuid.uuid4()
        self.role = role
        self.crew = crew


class MockCrew:
    """Mock CrewAI crew."""

    def __init__(self, crew_id=None, name="Test Crew"):
        self.id = crew_id or uuid.uuid4()
        self.name = name


class MockOutput:
    """Mock CrewAI output."""

    def __init__(self, raw="Test output"):
        self.raw = raw


@pytest.fixture
def mock_galileo_logger():
    """Creates a mock Galileo logger for testing."""
    with (
        patch("galileo.logger.logger.LogStreams") as mock_logstreams,
        patch("galileo.logger.logger.Projects") as mock_projects,
        patch("galileo.logger.logger.Traces") as mock_traces_client,
    ):
        setup_mock_traces_client(mock_traces_client)
        setup_mock_projects_client(mock_projects)
        setup_mock_logstreams_client(mock_logstreams)

        from galileo.logger.logger import GalileoLogger

        return GalileoLogger(project="test_project", log_stream="test_log_stream")


@pytest.fixture
def crewai_callback(mock_galileo_logger):
    """Creates a CrewAIEventListener instance for testing."""
    with (
        patch("galileo.handlers.crewai.handler._crewai_imports_resolved", True),
        patch("galileo.handlers.crewai.handler.CREWAI_AVAILABLE", False),
        patch("galileo.handlers.crewai.handler.LITE_LLM_AVAILABLE", False),
    ):
        from galileo.handlers.crewai.handler import CrewAIEventListener

        return CrewAIEventListener(
            galileo_logger=mock_galileo_logger, start_new_trace=True, flush_on_crew_completed=False
        )


def test_initialization_with_crewai_available(mock_galileo_logger) -> None:
    """Test CrewAIEventListener initialization when CrewAI is available."""
    with (
        patch("galileo.handlers.crewai.handler._crewai_imports_resolved", True),
        patch("galileo.handlers.crewai.handler.CREWAI_AVAILABLE", True),
        patch("galileo.handlers.crewai.handler.LITE_LLM_AVAILABLE", True),
    ):
        from galileo.handlers.crewai.handler import CrewAIEventListener

        callback = CrewAIEventListener(
            galileo_logger=mock_galileo_logger, start_new_trace=False, flush_on_crew_completed=True
        )

        assert callback._handler._galileo_logger == mock_galileo_logger
        assert callback._handler._start_new_trace is False
        assert callback._handler._flush_on_chain_end is True


def test_initialization_with_crewai_unavailable(mock_galileo_logger) -> None:
    """Test CrewAIEventListener initialization when CrewAI is unavailable."""
    with (
        patch("galileo.handlers.crewai.handler._crewai_imports_resolved", True),
        patch("galileo.handlers.crewai.handler.CREWAI_AVAILABLE", False),
        patch("galileo.handlers.crewai.handler.LITE_LLM_AVAILABLE", False),
    ):
        from galileo.handlers.crewai.handler import CrewAIEventListener

        callback = CrewAIEventListener(galileo_logger=mock_galileo_logger)

        assert callback._handler._galileo_logger == mock_galileo_logger


def test_generate_run_id_with_source_id(crewai_callback) -> None:
    """Test UUID generation when source has an ID."""
    source_id = uuid.uuid4()
    source = MockSource(id=source_id)
    event = MockEvent()

    result = crewai_callback._generate_run_id(source, event)
    assert result == source_id


def test_generate_run_id_with_messages(crewai_callback) -> None:
    """Test UUID generation from event messages."""
    messages = [{"role": "user", "content": "test"}]
    event = MockEvent(messages=messages)
    source = MockSource()

    result = crewai_callback._generate_run_id(source, event)

    # Verify it's a valid UUID
    assert isinstance(result, uuid.UUID)

    # Verify consistency - same input should produce same UUID
    result2 = crewai_callback._generate_run_id(source, event)
    assert result == result2


def test_generate_run_id_with_tool_args_dict(crewai_callback) -> None:
    """Test UUID generation from tool args as dict."""
    tool_args = {"arg1": "value1", "arg2": "value2"}
    event = MockEvent(tool_args=tool_args)
    source = MockSource()

    result = crewai_callback._generate_run_id(source, event)
    assert isinstance(result, uuid.UUID)


def test_generate_run_id_with_tool_args_string(crewai_callback) -> None:
    """Test UUID generation from tool args as string."""
    tool_args = '{"arg1": "value1"}'
    event = MockEvent(tool_args=tool_args)
    source = MockSource()

    result = crewai_callback._generate_run_id(source, event)
    assert isinstance(result, uuid.UUID)


def test_generate_run_id_fallback(crewai_callback) -> None:
    """Test UUID generation fallback method."""
    event = MockEvent(crew_name="test_crew", agent="test_agent", task="test_task")
    source = MockSource()

    result = crewai_callback._generate_run_id(source, event)
    assert isinstance(result, uuid.UUID)


def test_extract_metadata(crewai_callback) -> None:
    """Test metadata extraction from event."""
    timestamp = datetime.now()
    event = MockEvent(
        timestamp=timestamp, source_type="test_source", fingerprint_metadata={"key1": "value1", "key2": "value2"}
    )

    metadata = crewai_callback._extract_metadata(event)

    assert metadata["timestamp"] == timestamp.isoformat()
    assert metadata["source_type"] == "test_source"
    assert metadata["key1"] == "value1"
    assert metadata["key2"] == "value2"


@pytest.mark.parametrize("generated_id", [lambda: uuid.uuid4(), lambda: str(uuid.uuid4())])
def test_crew_kickoff_started(crewai_callback, generated_id) -> None:
    """Test crew kickoff started event handling."""
    crew_id = generated_id()
    source = MockSource(id=crew_id)
    event = MockEvent(crew_name="Test Crew", inputs={"input1": "value1"})

    with patch.object(crewai_callback._handler, "start_node") as mock_start_node:
        crewai_callback._handle_crew_kickoff_started(source, event)

        mock_start_node.assert_called_once()
        call_args = mock_start_node.call_args
        assert call_args[1]["node_type"] == NodeType.CHAIN.value
        assert call_args[1]["parent_run_id"] is None
        assert call_args[1]["run_id"] == crew_id
        assert call_args[1]["name"] == "Test Crew"


@pytest.mark.parametrize("generated_id", [lambda: uuid.uuid4(), lambda: str(uuid.uuid4())])
def test_crew_kickoff_started_empty_inputs(crewai_callback, generated_id) -> None:
    """Test crew kickoff started event handling."""
    crew_id = generated_id()
    source = MockSource(id=crew_id)
    event = MockEvent(crew_name="Test Crew")

    with patch.object(crewai_callback._handler, "start_node") as mock_start_node:
        crewai_callback._handle_crew_kickoff_started(source, event)

        mock_start_node.assert_called_once()
        call_args = mock_start_node.call_args
        assert call_args[1]["node_type"] == NodeType.CHAIN.value
        assert call_args[1]["parent_run_id"] is None
        assert call_args[1]["run_id"] == crew_id
        assert call_args[1]["name"] == "Test Crew"
        assert call_args[1]["input"] == "-"


@pytest.mark.parametrize("generated_id", [lambda: uuid.uuid4(), lambda: str(uuid.uuid4())])
def test_crew_kickoff_completed(crewai_callback, generated_id) -> None:
    """Test crew kickoff completed event handling."""
    crew_id = generated_id()
    source = MockSource(id=crew_id)
    output = MockOutput(raw="Crew completed successfully")
    event = MockEvent(output=output)

    with (
        patch.object(crewai_callback._handler, "end_node") as mock_end_node,
        patch.object(crewai_callback, "_update_crew_input") as mock_update_input,
    ):
        crewai_callback._handle_crew_kickoff_completed(source, event)

        mock_update_input.assert_called_once_with(str(crew_id))
        mock_end_node.assert_called_once_with(run_id=crew_id, output="Crew completed successfully")


@pytest.mark.parametrize("generated_id", [lambda: uuid.uuid4(), lambda: str(uuid.uuid4())])
def test_crew_kickoff_failed(crewai_callback, generated_id) -> None:
    """Test crew kickoff failed event handling."""
    crew_id = generated_id()
    source = MockSource(id=crew_id)
    event = MockEvent(error="Something went wrong")

    with patch.object(crewai_callback._handler, "end_node") as mock_end_node:
        crewai_callback._handle_crew_kickoff_failed(source, event)

        mock_end_node.assert_called_once()
        call_args = mock_end_node.call_args
        assert call_args[1]["run_id"] == crew_id
        assert call_args[1]["output"] == "Error: Something went wrong"
        assert call_args[1]["metadata"]["error"] == "Something went wrong"


@pytest.mark.parametrize("generated_id", [lambda: uuid.uuid4(), lambda: str(uuid.uuid4())])
def test_agent_execution_started(crewai_callback, generated_id) -> None:
    """Test agent execution started event handling."""
    agent_id = generated_id()
    task_id = generated_id()
    crew = MockCrew()
    agent = MockAgent(agent_id=agent_id, role="Research Agent", crew=crew)
    task = MockTask(task_id=task_id, agent=agent)
    source = MockSource(id=agent_id)
    event = MockEvent(agent=agent, task=task, task_prompt="Research the topic", tools=["search_tool", "analysis_tool"])

    with patch.object(crewai_callback._handler, "start_node") as mock_start_node:
        crewai_callback._handle_agent_execution_started(source, event)

        mock_start_node.assert_called_once()
        call_args = mock_start_node.call_args
        assert call_args[1]["node_type"] == NodeType.AGENT.value
        assert str(call_args[1]["parent_run_id"]) == str(task_id)
        assert call_args[1]["run_id"] == agent_id
        assert call_args[1]["name"] == "Research Agent"
        assert call_args[1]["input"] == "Research the topic"


@pytest.mark.parametrize("generated_id", [lambda: uuid.uuid4(), lambda: str(uuid.uuid4())])
def test_agent_execution_started_no_input(crewai_callback, generated_id) -> None:
    """Test agent execution started event handling."""
    agent_id = generated_id()
    task_id = generated_id()
    crew = MockCrew()
    agent = MockAgent(agent_id=agent_id, role="Research Agent", crew=crew)
    task = MockTask(task_id=task_id, agent=agent)
    source = MockSource(id=agent_id)
    event = MockEvent(agent=agent, task=task, tools=["search_tool", "analysis_tool"])

    with patch.object(crewai_callback._handler, "start_node") as mock_start_node:
        crewai_callback._handle_agent_execution_started(source, event)

        mock_start_node.assert_called_once()
        call_args = mock_start_node.call_args
        assert call_args[1]["node_type"] == NodeType.AGENT.value
        assert str(call_args[1]["parent_run_id"]) == str(task_id)
        assert call_args[1]["run_id"] == agent_id
        assert call_args[1]["name"] == "Research Agent"
        assert call_args[1]["input"] == "-"


@pytest.mark.parametrize("generated_id", [lambda: uuid.uuid4(), lambda: str(uuid.uuid4())])
def test_agent_execution_completed(crewai_callback, generated_id) -> None:
    """Test agent execution completed event handling."""
    agent_id = generated_id()
    source = MockSource(id=agent_id)
    event = MockEvent(output="Agent task completed")

    with patch.object(crewai_callback._handler, "end_node") as mock_end_node:
        crewai_callback._handle_agent_execution_completed(source, event)

        mock_end_node.assert_called_once_with(run_id=agent_id, output="Agent task completed")


@pytest.mark.parametrize("generated_id", [lambda: uuid.uuid4(), lambda: str(uuid.uuid4())])
def test_agent_execution_error(crewai_callback, generated_id) -> None:
    """Test agent execution error event handling."""
    agent_id = generated_id()
    source = MockSource(id=agent_id)
    event = MockEvent(error="Agent failed")

    with patch.object(crewai_callback._handler, "end_node") as mock_end_node:
        crewai_callback._handle_agent_execution_error(source, event)

        mock_end_node.assert_called_once()
        call_args = mock_end_node.call_args
        assert call_args[1]["run_id"] == agent_id
        assert call_args[1]["output"] == "Error: Agent failed"
        assert call_args[1]["metadata"]["error"] == "Agent failed"


@pytest.mark.parametrize("generated_id", [lambda: uuid.uuid4(), lambda: str(uuid.uuid4())])
def test_task_started(crewai_callback, generated_id) -> None:
    """Test task started event handling."""
    task_id = generated_id()
    crew_id = generated_id()
    crew = MockCrew(crew_id=crew_id)
    agent = MockAgent(crew=crew)
    task = MockTask(task_id=task_id, description="Research market trends", agent=agent)
    source = MockSource(id=task_id)
    event = MockEvent(task=task, context="Previous research context")

    with patch.object(crewai_callback._handler, "start_node") as mock_start_node:
        crewai_callback._handle_task_started(source, event)

        mock_start_node.assert_called_once()
        call_args = mock_start_node.call_args
        assert call_args[1]["node_type"] == NodeType.CHAIN.value
        assert str(call_args[1]["parent_run_id"]) == str(crew_id)
        assert call_args[1]["run_id"] == task_id
        assert call_args[1]["name"] == "Research market trends"
        assert call_args[1]["input"] == "Previous research context"


@pytest.mark.parametrize("generated_id", [lambda: uuid.uuid4(), lambda: str(uuid.uuid4())])
def test_task_started_no_context(crewai_callback, generated_id) -> None:
    """Test task started event handling."""
    task_id = generated_id()
    crew_id = generated_id()
    crew = MockCrew(crew_id=crew_id)
    agent = MockAgent(crew=crew)
    task = MockTask(task_id=task_id, description="Research market trends", agent=agent)
    source = MockSource(id=task_id)
    event = MockEvent(task=task)

    with patch.object(crewai_callback._handler, "start_node") as mock_start_node:
        crewai_callback._handle_task_started(source, event)

        mock_start_node.assert_called_once()
        call_args = mock_start_node.call_args
        assert call_args[1]["node_type"] == NodeType.CHAIN.value
        assert str(call_args[1]["parent_run_id"]) == str(crew_id)
        assert call_args[1]["run_id"] == task_id
        assert call_args[1]["name"] == "Research market trends"
        assert call_args[1]["input"] == task.description


@pytest.mark.parametrize("generated_id", [lambda: uuid.uuid4(), lambda: str(uuid.uuid4())])
def test_task_started_no_description(crewai_callback, generated_id) -> None:
    """Test task started event handling."""
    task_id = generated_id()
    crew_id = generated_id()
    crew = MockCrew(crew_id=crew_id)
    agent = MockAgent(crew=crew)
    task = MockTask(task_id=task_id, description="", agent=agent)
    source = MockSource(id=task_id)
    event = MockEvent(task=task)

    with patch.object(crewai_callback._handler, "start_node") as mock_start_node:
        crewai_callback._handle_task_started(source, event)

        mock_start_node.assert_called_once()
        call_args = mock_start_node.call_args
        assert call_args[1]["node_type"] == NodeType.CHAIN.value
        assert str(call_args[1]["parent_run_id"]) == str(crew_id)
        assert call_args[1]["run_id"] == task_id
        assert call_args[1]["name"] == ""
        assert call_args[1]["input"] == "-"


@pytest.mark.parametrize("generated_id", [lambda: uuid.uuid4(), lambda: str(uuid.uuid4())])
def test_task_completed(crewai_callback, generated_id) -> None:
    """Test task completed event handling."""
    task_id = generated_id()
    source = MockSource(id=task_id)
    output = MockOutput(raw="Task completed successfully")
    event = MockEvent(output=output)

    with patch.object(crewai_callback._handler, "end_node") as mock_end_node:
        crewai_callback._handle_task_completed(source, event)

        mock_end_node.assert_called_once_with(run_id=task_id, output="Task completed successfully")


@pytest.mark.parametrize("generated_id", [lambda: uuid.uuid4(), lambda: str(uuid.uuid4())])
def test_task_failed(crewai_callback, generated_id) -> None:
    """Test task failed event handling."""
    task_id = generated_id()
    source = MockSource(id=task_id)
    event = MockEvent(error="Task execution failed")

    with patch.object(crewai_callback._handler, "end_node") as mock_end_node:
        crewai_callback._handle_task_failed(source, event)
        mock_end_node.assert_called_once()
        call_args = mock_end_node.call_args
        assert call_args[1]["run_id"] == task_id
        assert call_args[1]["output"] == "Error: Task execution failed"
        assert call_args[1]["metadata"]["error"] == "Task execution failed"


@pytest.mark.parametrize("generated_id", [lambda: uuid.uuid4(), lambda: str(uuid.uuid4())])
def test_tool_usage_started(crewai_callback, generated_id) -> None:
    """Test tool usage started event handling."""
    tool_id = generated_id()
    agent_id = generated_id()
    agent = MockAgent(agent_id=agent_id)
    source = MockSource(id=tool_id)
    event = MockEvent(agent=agent, tool_name="search_tool", tool_args={"query": "market research"})

    with patch.object(crewai_callback._handler, "start_node") as mock_start_node:
        crewai_callback._handle_tool_usage_started(source, event)

        mock_start_node.assert_called_once()
        call_args = mock_start_node.call_args
        assert call_args[1]["node_type"] == NodeType.TOOL.value
        assert str(call_args[1]["parent_run_id"]) == str(agent_id)
        assert call_args[1]["run_id"] == tool_id
        assert call_args[1]["name"] == "search_tool"


@pytest.mark.parametrize("generated_id", [lambda: uuid.uuid4(), lambda: str(uuid.uuid4())])
def test_tool_usage_started_no_input(crewai_callback, generated_id) -> None:
    """Test tool usage started event handling."""
    tool_id = generated_id()
    agent_id = generated_id()
    agent = MockAgent(agent_id=agent_id)

    source = MockSource(id=tool_id)
    event = MockEvent(agent=agent, tool_name="search_tool")

    with patch.object(crewai_callback._handler, "start_node") as mock_start_node:
        crewai_callback._handle_tool_usage_started(source, event)

        mock_start_node.assert_called_once()
        call_args = mock_start_node.call_args
        assert call_args[1]["node_type"] == NodeType.TOOL.value
        assert str(call_args[1]["parent_run_id"]) == str(agent_id)
        assert call_args[1]["run_id"] == tool_id
        assert call_args[1]["name"] == "search_tool"
        assert call_args[1]["input"] == "-"


@pytest.mark.parametrize("generated_id", [lambda: uuid.uuid4(), lambda: str(uuid.uuid4())])
def test_tool_usage_finished(crewai_callback, generated_id) -> None:
    """Test tool usage finished event handling."""
    tool_id = generated_id()
    source = MockSource(id=tool_id)
    event = MockEvent(output="Tool execution completed")

    with patch.object(crewai_callback._handler, "end_node") as mock_end_node:
        crewai_callback._handle_tool_usage_finished(source, event)

        mock_end_node.assert_called_once_with(run_id=tool_id, output="Tool execution completed")


@pytest.mark.parametrize("generated_id", [lambda: uuid.uuid4(), lambda: str(uuid.uuid4())])
def test_tool_usage_error(crewai_callback, generated_id) -> None:
    """Test tool usage error event handling."""
    tool_id = generated_id()
    source = MockSource(id=tool_id)
    event = MockEvent(error="Tool execution failed")

    with patch.object(crewai_callback._handler, "end_node") as mock_end_node:
        crewai_callback._handle_tool_usage_error(source, event)

        mock_end_node.assert_called_once()
        call_args = mock_end_node.call_args
        assert call_args[1]["run_id"] == tool_id
        assert call_args[1]["output"] == "Error: Tool execution failed"
        assert call_args[1]["metadata"]["error"] == "Tool execution failed"


@pytest.mark.parametrize("generated_id", [lambda: uuid.uuid4(), lambda: str(uuid.uuid4())])
def test_llm_call_started(crewai_callback, generated_id) -> None:
    """Test LLM call started event handling."""
    llm_id = generated_id()
    source = MockSource(id=llm_id, model="gpt-4", temperature=0.7)
    event = MockEvent(agent_id=generated_id(), messages=[{"role": "user", "content": "Hello"}])

    with patch.object(crewai_callback._handler, "start_node") as mock_start_node:
        crewai_callback._handle_llm_call_started(source, event)

        mock_start_node.assert_called_once()
        call_args = mock_start_node.call_args
        assert call_args[1]["node_type"] == NodeType.LLM.value
        assert call_args[1]["run_id"] == llm_id
        assert call_args[1]["name"] == "gpt-4"
        assert call_args[1]["model"] == "gpt-4"
        assert call_args[1]["temperature"] == 0.7


@pytest.mark.parametrize("generated_id", [lambda: uuid.uuid4(), lambda: str(uuid.uuid4())])
def test_llm_call_completed(crewai_callback, generated_id) -> None:
    """Test LLM call completed event handling."""
    llm_id = generated_id()
    source = MockSource(id=llm_id)
    event = MockEvent(response="Hello! How can I help you?")

    with patch.object(crewai_callback._handler, "end_node") as mock_end_node:
        crewai_callback._handle_llm_call_completed(source, event)

        mock_end_node.assert_called_once_with(run_id=llm_id, output="Hello! How can I help you?")


@pytest.mark.parametrize("generated_id", [lambda: uuid.uuid4(), lambda: str(uuid.uuid4())])
def test_llm_call_failed(crewai_callback, generated_id) -> None:
    """Test LLM call failed event handling."""
    llm_id = generated_id()
    source = MockSource(id=llm_id)
    event = MockEvent(error="Rate limit exceeded")

    with patch.object(crewai_callback._handler, "end_node") as mock_end_node:
        crewai_callback._handle_llm_call_failed(source, event)

        mock_end_node.assert_called_once()
        call_args = mock_end_node.call_args
        assert call_args[1]["run_id"] == llm_id
        assert call_args[1]["output"] == "Error: Rate limit exceeded"
        assert call_args[1]["metadata"]["error"] == "Rate limit exceeded"


def test_setup_listeners_crewai_unavailable(crewai_callback: CrewAIEventListener) -> None:
    """Test setup_listeners when CrewAI is unavailable."""
    mock_event_bus = Mock()

    with patch("galileo.handlers.crewai.handler.CREWAI_AVAILABLE", False):
        crewai_callback.setup_listeners(mock_event_bus)

        # Verify that no event listeners were registered
        mock_event_bus.on.assert_not_called()


def test_update_crew_input(crewai_callback: CrewAIEventListener) -> None:
    """Test crew input update functionality."""
    crew_id = uuid.uuid4()

    # Mock nodes with task descriptions
    mock_root_node = Mock()
    mock_root_node.span_params = {"input": "-"}

    mock_task_node = Mock()
    mock_task_node.span_params = {"metadata": {"task_description": "Research market trends"}}

    mock_nodes = {str(crew_id): mock_root_node, "task1": mock_task_node}

    with patch.object(crewai_callback._handler, "get_nodes", return_value=mock_nodes):
        crewai_callback._update_crew_input(str(crew_id))

        # Verify input was updated with task descriptions
        assert "Research market trends" in mock_root_node.span_params["input"]


def test_lite_llm_usage_callback(crewai_callback: CrewAIEventListener) -> None:
    """Test LiteLLM usage callback."""
    node_id = uuid.uuid4()

    # Mock node
    mock_node = Mock()
    mock_node.span_params = {}

    # Mock completion response with usage
    mock_usage = Mock()
    mock_usage.model_dump.return_value = {"prompt_tokens": 100, "completion_tokens": 50, "total_tokens": 150}
    mock_usage.prompt_tokens = 100
    mock_usage.completion_tokens = 50
    mock_usage.total_tokens = 150

    mock_response = Mock()
    mock_response.model_extra = {"usage": mock_usage}

    kwargs = {"messages": [{"role": "user", "content": "test"}]}

    with (
        patch.object(crewai_callback._handler, "get_node", return_value=mock_node),
        patch.object(crewai_callback, "_generate_run_id", return_value=node_id),
    ):
        crewai_callback.lite_llm_usage_callback(
            kwargs=kwargs, completion_response=mock_response, start_time=datetime.now(), end_time=datetime.now()
        )

        # Verify usage was recorded
        assert mock_node.span_params["num_input_tokens"] == 100
        assert mock_node.span_params["num_output_tokens"] == 50
        assert mock_node.span_params["total_tokens"] == 150


def test_lite_llm_usage_callback_no_node(crewai_callback) -> None:
    """Test LiteLLM usage callback when node doesn't exist."""
    kwargs = {"messages": [{"role": "user", "content": "test"}]}
    mock_response = Mock()

    with (
        patch.object(crewai_callback._handler, "get_node", return_value=None),
        patch.object(crewai_callback, "_generate_run_id", return_value=uuid.uuid4()),
    ):
        # Should not raise an exception
        crewai_callback.lite_llm_usage_callback(
            kwargs=kwargs, completion_response=mock_response, start_time=datetime.now(), end_time=datetime.now()
        )


# Memory event tests (for CrewAI >= 0.177.0)


@pytest.mark.parametrize("generated_id", [lambda: uuid.uuid4(), lambda: str(uuid.uuid4())])
def test_memory_query_started(crewai_callback, generated_id) -> None:
    """Test memory query started event handling."""
    query_id = generated_id()
    agent_id = generated_id()
    source = MockSource(id=query_id)
    event = MockEvent(
        query="What are the market trends?",
        limit=10,
        score_threshold=0.8,
        agent_id=agent_id,
        agent_role="Research Agent",
    )

    with patch.object(crewai_callback._handler, "start_node") as mock_start_node:
        crewai_callback._handle_memory_query_started(source, event)

        mock_start_node.assert_called_once()
        call_args = mock_start_node.call_args
        assert call_args[1]["node_type"] == NodeType.RETRIEVER.value
        assert str(call_args[1]["parent_run_id"]) == str(agent_id)
        expected_run_id = crewai_callback._generate_run_id(source, event)
        assert call_args[1]["run_id"] == expected_run_id

        assert call_args[1]["name"] == "Memory Query"
        assert call_args[1]["input"] == "What are the market trends?"
        assert call_args[1]["metadata"]["query"] == "What are the market trends?"
        assert call_args[1]["metadata"]["limit"] == 10
        assert call_args[1]["metadata"]["score_threshold"] == 0.8
        assert call_args[1]["metadata"]["agent_role"] == "Research Agent"


@pytest.mark.parametrize("generated_id", [lambda: uuid.uuid4(), lambda: str(uuid.uuid4())])
def test_memory_query_completed(crewai_callback, generated_id) -> None:
    """Test memory query completed event handling."""
    query_id = generated_id()
    source = MockSource(id=query_id)
    results = [{"content": "Market trend 1"}, {"content": "Market trend 2"}]
    event = MockEvent(query="What are the market trends?", results=results, limit=10, query_time_ms=150.5)

    with patch.object(crewai_callback._handler, "end_node") as mock_end_node:
        crewai_callback._handle_memory_query_completed(source, event)

        mock_end_node.assert_called_once()
        call_args = mock_end_node.call_args
        expected_run_id = crewai_callback._generate_run_id(source, event)
        assert call_args[1]["run_id"] == expected_run_id
        assert call_args[1]["metadata"]["query_time_ms"] == 150.5
        assert call_args[1]["metadata"]["results_count"] == 2


@pytest.mark.parametrize("generated_id", [lambda: uuid.uuid4(), lambda: str(uuid.uuid4())])
def test_memory_query_failed(crewai_callback, generated_id) -> None:
    """Test memory query failed event handling."""
    query_id = generated_id()
    source = MockSource(id=query_id)
    event = MockEvent(query="What are the market trends?", limit=10, error="Connection timeout")

    with patch.object(crewai_callback._handler, "end_node") as mock_end_node:
        crewai_callback._handle_memory_query_failed(source, event)

        mock_end_node.assert_called_once()
        call_args = mock_end_node.call_args
        expected_run_id = crewai_callback._generate_run_id(source, event)
        assert call_args[1]["run_id"] == expected_run_id
        assert call_args[1]["output"] == "Memory query failed: Connection timeout"
        assert call_args[1]["metadata"]["error"] == "Connection timeout"


@pytest.mark.parametrize("generated_id", [lambda: uuid.uuid4(), lambda: str(uuid.uuid4())])
def test_memory_save_started(crewai_callback, generated_id) -> None:
    """Test memory save started event handling."""
    save_id = generated_id()
    agent_id = generated_id()
    source = MockSource(id=save_id)
    event = MockEvent(
        value="Important market insight",
        metadata={"source": "research", "confidence": 0.9},
        agent_id=agent_id,
        agent_role="Research Agent",
    )

    with patch.object(crewai_callback._handler, "start_node") as mock_start_node:
        crewai_callback._handle_memory_save_started(source, event)

        mock_start_node.assert_called_once()
        call_args = mock_start_node.call_args
        assert call_args[1]["node_type"] == NodeType.CHAIN.value
        assert str(call_args[1]["parent_run_id"]) == str(agent_id)
        assert call_args[1]["run_id"] == save_id
        assert call_args[1]["name"] == "Memory Save"
        assert call_args[1]["input"] == "Important market insight"
        assert call_args[1]["metadata"]["source"] == "research"
        assert call_args[1]["metadata"]["confidence"] == 0.9
        assert call_args[1]["metadata"]["agent_role"] == "Research Agent"


@pytest.mark.parametrize("generated_id", [lambda: uuid.uuid4(), lambda: str(uuid.uuid4())])
def test_memory_save_started_no_value(crewai_callback, generated_id) -> None:
    """Test memory save started event handling with no value."""
    save_id = generated_id()
    source = MockSource(id=save_id)
    event = MockEvent(value=None, metadata=None)

    with patch.object(crewai_callback._handler, "start_node") as mock_start_node:
        crewai_callback._handle_memory_save_started(source, event)

        mock_start_node.assert_called_once()
        call_args = mock_start_node.call_args
        assert call_args[1]["input"] == "Memory content"


@pytest.mark.parametrize("generated_id", [lambda: uuid.uuid4(), lambda: str(uuid.uuid4())])
def test_memory_save_completed(crewai_callback, generated_id) -> None:
    """Test memory save completed event handling."""
    save_id = generated_id()
    source = MockSource(id=save_id)
    event = MockEvent(value="Important market insight", save_time_ms=75.2)

    with patch.object(crewai_callback._handler, "end_node") as mock_end_node:
        crewai_callback._handle_memory_save_completed(source, event)

        mock_end_node.assert_called_once()
        call_args = mock_end_node.call_args
        assert call_args[1]["run_id"] == save_id
        assert call_args[1]["output"] == "Memory saved successfully: Important market insight"
        assert call_args[1]["metadata"]["save_time_ms"] == 75.2


@pytest.mark.parametrize("generated_id", [lambda: uuid.uuid4(), lambda: str(uuid.uuid4())])
def test_memory_save_failed(crewai_callback, generated_id) -> None:
    """Test memory save failed event handling."""
    save_id = generated_id()
    source = MockSource(id=save_id)
    event = MockEvent(value="Important market insight", error="Storage full")

    with patch.object(crewai_callback._handler, "end_node") as mock_end_node:
        crewai_callback._handle_memory_save_failed(source, event)

        mock_end_node.assert_called_once()
        call_args = mock_end_node.call_args
        assert call_args[1]["run_id"] == save_id
        assert call_args[1]["output"] == "Memory save failed: Storage full"
        assert call_args[1]["metadata"]["error"] == "Storage full"


@pytest.mark.parametrize("generated_id", [lambda: uuid.uuid4(), lambda: str(uuid.uuid4())])
def test_memory_retrieval_started(crewai_callback, generated_id) -> None:
    """Test memory retrieval started event handling."""
    retrieval_id = generated_id()
    task_id = generated_id()
    source = MockSource(id=retrieval_id)
    event = MockEvent(task_id=task_id)

    with patch.object(crewai_callback._handler, "start_node") as mock_start_node:
        crewai_callback._handle_memory_retrieval_started(source, event)

        mock_start_node.assert_called_once()
        call_args = mock_start_node.call_args

        assert call_args[1]["node_type"] == NodeType.CHAIN.value
        assert str(call_args[1]["parent_run_id"]) == str(task_id)
        expected_run_id = crewai_callback._generate_run_id(source, event)
        assert call_args[1]["run_id"] == expected_run_id
        assert call_args[1]["name"] == "Memory Retrieval"
        assert call_args[1]["input"] == "Retrieving relevant memories for task"
        assert call_args[1]["metadata"]["task_id"] == task_id


@pytest.mark.parametrize("generated_id", [lambda: uuid.uuid4(), lambda: str(uuid.uuid4())])
def test_memory_retrieval_completed(crewai_callback, generated_id) -> None:
    """Test memory retrieval completed event handling."""
    retrieval_id = generated_id()
    source = MockSource(id=retrieval_id)
    event = MockEvent(
        task_id=generated_id(), memory_content="Retrieved relevant market insights and trends", retrieval_time_ms=120.8
    )

    with patch.object(crewai_callback._handler, "end_node") as mock_end_node:
        crewai_callback._handle_memory_retrieval_completed(source, event)

        mock_end_node.assert_called_once()
        call_args = mock_end_node.call_args
        expected_run_id = crewai_callback._generate_run_id(source, event)
        assert call_args[1]["run_id"] == expected_run_id
        assert call_args[1]["output"] == "Retrieved relevant market insights and trends"
        assert call_args[1]["metadata"]["retrieval_time_ms"] == 120.8


# crewAI >= 1.0 compatibility tests


def test_generate_run_id_with_call_id(crewai_callback) -> None:
    """Test that call_id correlates start and end events for LLM calls in crewAI >= 1.0."""
    # Given: start and end events with the same call_id but no source.id
    source_start = MockSource()  # No .id — crewAI 1.x BaseLLM source
    source_end = MockSource()
    call_id = "abc-123"
    start_event = MockEvent(call_id=call_id, messages=[{"role": "user", "content": "hi"}])
    end_event = MockEvent(call_id=call_id, response="hello")

    # When: generating run_ids for both events
    run_id_start = crewai_callback._generate_run_id(source_start, start_event)
    run_id_end = crewai_callback._generate_run_id(source_end, end_event)

    # Then: both produce the same UUID
    assert run_id_start == run_id_end
    assert isinstance(run_id_start, uuid.UUID)


def test_generate_run_id_agent_event_no_source_id(crewai_callback) -> None:
    """Test agent events use event.agent.id when source has no .id (crewAI >= 1.0)."""
    # Given: an event with agent.id but source without .id
    agent_id = uuid.uuid4()
    agent = MockAgent(agent_id=agent_id)
    source = MockSource()  # No .id — crewAI 1.x Adapter source
    event = MockEvent(agent=agent)

    # When: generating run_id
    result = crewai_callback._generate_run_id(source, event)

    # Then: it uses agent.id from the event
    assert result == agent_id


def test_llm_call_lifecycle_crewai_v1(crewai_callback) -> None:
    """Test full LLM start/complete lifecycle with call_id (crewAI >= 1.0)."""
    # Given: a source without .id and events with call_id
    source = MockSource()  # No .id — crewAI 1.x BaseLLM
    call_id = "llm-call-456"
    start_event = MockEvent(
        call_id=call_id, model="gpt-4o", agent_id=str(uuid.uuid4()), messages=[{"role": "user", "content": "test"}]
    )
    end_event = MockEvent(call_id=call_id, response="LLM response")

    with (
        patch.object(crewai_callback._handler, "start_node") as mock_start,
        patch.object(crewai_callback._handler, "end_node") as mock_end,
    ):
        # When: handling start and complete
        crewai_callback._handle_llm_call_started(source, start_event)
        crewai_callback._handle_llm_call_completed(source, end_event)

        # Then: both use the same run_id
        start_run_id = mock_start.call_args[1]["run_id"]
        end_run_id = mock_end.call_args[1]["run_id"]
        assert start_run_id == end_run_id


def test_llm_call_started_prefers_event_model(crewai_callback) -> None:
    """Test that event.model is preferred over source.model for LLM name."""
    # Given: source with one model and event with a different model
    source = MockSource(id=uuid.uuid4(), model="old-model", temperature=0.5)
    event = MockEvent(model="gpt-4o", agent_id=str(uuid.uuid4()), messages=[{"role": "user", "content": "hi"}])

    with patch.object(crewai_callback._handler, "start_node") as mock_start_node:
        # When: handling the event
        crewai_callback._handle_llm_call_started(source, event)

        # Then: event.model wins
        call_args = mock_start_node.call_args[1]
        assert call_args["name"] == "gpt-4o"
        assert call_args["model"] == "gpt-4o"
        assert call_args["metadata"]["model"] == "gpt-4o"


def test_memory_retrieval_failed(crewai_callback) -> None:
    """Test memory retrieval failed event handling."""
    # Given: a memory retrieval failed event
    source = MockSource()
    event = MockEvent(
        type="memory_retrieval_failed",
        task_id=str(uuid.uuid4()),
        agent_id=str(uuid.uuid4()),
        error="Memory store unavailable",
    )

    with patch.object(crewai_callback._handler, "end_node") as mock_end_node:
        # When: handling the failure
        crewai_callback._handle_memory_retrieval_failed(source, event)

        # Then: error is recorded properly
        mock_end_node.assert_called_once()
        call_args = mock_end_node.call_args[1]
        assert call_args["output"] == "Memory retrieval failed: Memory store unavailable"
        assert call_args["metadata"]["error"] == "Memory store unavailable"


def test_agent_execution_started_no_task_id(crewai_callback) -> None:
    """Test agent execution started when event.task has no .id (crewAI >= 1.0)."""
    # Given: an event where task object lacks .id
    agent_id = uuid.uuid4()
    agent = MockAgent(agent_id=agent_id, role="Analyst")
    task = MockSource(description="Analyze data")  # No .id attribute
    source = MockSource(id=agent_id)
    event = MockEvent(agent=agent, task=task, task_prompt="Analyze the data")

    with patch.object(crewai_callback._handler, "start_node") as mock_start_node:
        # When: handling the event
        crewai_callback._handle_agent_execution_started(source, event)

        # Then: parent_run_id is None (graceful degradation)
        call_args = mock_start_node.call_args[1]
        assert call_args["parent_run_id"] is None
        assert call_args["name"] == "Analyst"


def test_task_started_no_agent_on_task(crewai_callback) -> None:
    """Test task started when task has no agent attribute (crewAI >= 1.0)."""
    # Given: a task without .agent
    task_id = uuid.uuid4()
    task = MockSource(id=task_id, description="Research market trends")
    source = MockSource(id=task_id)
    event = MockEvent(task=task)

    with patch.object(crewai_callback._handler, "start_node") as mock_start_node:
        # When: handling the event
        crewai_callback._handle_task_started(source, event)

        # Then: parent_run_id is None, rest works fine
        call_args = mock_start_node.call_args[1]
        assert call_args["parent_run_id"] is None
        assert call_args["name"] == "Research market trends"


def test_tool_usage_started_no_agent_id(crewai_callback) -> None:
    """Test tool usage started when event.agent has no .id (crewAI >= 1.0)."""
    # Given: an event where agent lacks .id
    agent = MockSource(role="Researcher")  # No .id
    source = MockSource()
    event = MockEvent(agent=agent, tool_name="web_search", tool_args={"query": "test"})

    with patch.object(crewai_callback._handler, "start_node") as mock_start_node:
        # When: handling the event
        crewai_callback._handle_tool_usage_started(source, event)

        # Then: parent_run_id is None, tool node still created
        call_args = mock_start_node.call_args[1]
        assert call_args["parent_run_id"] is None
        assert call_args["name"] == "web_search"


def test_tool_lifecycle_crewai_v1(crewai_callback) -> None:
    """Test tool start/end correlation via event_id/started_event_id (crewAI >= 1.0).

    In crewAI 1.x, the event bus sets started_event_id on scope-ending events
    to match the event_id of the corresponding start event. This provides
    reliable correlation regardless of thread pool execution order.
    """
    # Given: a ToolUsage-like source (no .id) with event_id/started_event_id
    source = MockSource()  # No .id — crewAI 1.x ToolUsage source
    start_event_id = str(uuid.uuid4())

    # Start event has event_id (set by crewAI's BaseEvent)
    start_event = MockEvent(
        tool_name="SearchTool", tool_args='{"query": "market research"}', agent_key="agent_1", event_id=start_event_id
    )
    # End event has started_event_id pointing to the start event's event_id
    end_event = MockEvent(
        tool_name="search_tool",
        tool_args={"query": "market research"},
        output="search results",
        agent_key="agent_1",
        started_event_id=start_event_id,
    )

    # When: generating run_ids for both events
    run_id_start = crewai_callback._generate_run_id(source, start_event)
    run_id_end = crewai_callback._generate_run_id(source, end_event)

    # Then: both produce the same UUID via event scope tracking
    assert run_id_start == run_id_end
    assert isinstance(run_id_start, uuid.UUID)


def test_tool_lifecycle_crewai_v1_different_sources(crewai_callback) -> None:
    """Test tool correlation works even with different source instances (thread pool race).

    The event bus may deliver start/end handlers to different thread pool workers.
    Using event_id/started_event_id ensures correlation is independent of source identity.
    """
    # Given: different source instances (simulating thread pool race or GC reuse)
    source_start = MockSource()
    source_end = MockSource()  # Different instance!
    start_event_id = str(uuid.uuid4())

    start_event = MockEvent(tool_name="SearchTool", tool_args='{"query": "test"}', event_id=start_event_id)
    end_event = MockEvent(
        tool_name="search_tool", tool_args={"query": "test"}, output="results", started_event_id=start_event_id
    )

    # When: generating run_ids with different sources
    run_id_start = crewai_callback._generate_run_id(source_start, start_event)
    run_id_end = crewai_callback._generate_run_id(source_end, end_event)

    # Then: still produces the same UUID
    assert run_id_start == run_id_end


def test_tool_lifecycle_crewai_v1_full(crewai_callback) -> None:
    """Test full tool start/finish lifecycle with crewAI 1.x event scope tracking."""
    # Given: source without .id, events with event_id/started_event_id
    source = MockSource()
    agent_id = uuid.uuid4()
    agent = MockAgent(agent_id=agent_id)
    start_event_id = str(uuid.uuid4())

    start_event = MockEvent(agent=agent, tool_name="WebSearch", tool_args='{"query": "test"}', event_id=start_event_id)
    end_event = MockEvent(
        tool_name="web_search", tool_args={"query": "test"}, output="Results found", started_event_id=start_event_id
    )

    with (
        patch.object(crewai_callback._handler, "start_node") as mock_start,
        patch.object(crewai_callback._handler, "end_node") as mock_end,
    ):
        # When: handling start and finish
        crewai_callback._handle_tool_usage_started(source, start_event)
        crewai_callback._handle_tool_usage_finished(source, end_event)

        # Then: both use the same run_id
        start_run_id = mock_start.call_args[1]["run_id"]
        end_run_id = mock_end.call_args[1]["run_id"]
        assert start_run_id == end_run_id


def test_tool_lifecycle_crewai_v1_with_error(crewai_callback) -> None:
    """Test tool start/error correlation via event scope tracking (crewAI >= 1.0)."""
    # Given: a tool that fails — error event also gets started_event_id
    source = MockSource()
    agent_id = uuid.uuid4()
    agent = MockAgent(agent_id=agent_id)
    start_event_id = str(uuid.uuid4())

    start_event = MockEvent(agent=agent, tool_name="WebSearch", tool_args='{"query": "test"}', event_id=start_event_id)
    error_event = MockEvent(
        tool_name="web_search", tool_args={"query": "test"}, error="Connection timeout", started_event_id=start_event_id
    )

    with (
        patch.object(crewai_callback._handler, "start_node") as mock_start,
        patch.object(crewai_callback._handler, "end_node") as mock_end,
    ):
        # When: handling start and error
        crewai_callback._handle_tool_usage_started(source, start_event)
        crewai_callback._handle_tool_usage_error(source, error_event)

        # Then: both use the same run_id
        start_run_id = mock_start.call_args[1]["run_id"]
        end_run_id = mock_end.call_args[1]["run_id"]
        assert start_run_id == end_run_id


def test_tool_lifecycle_crewai_v1_retry_gets_unique_ids(crewai_callback) -> None:
    """Test that retried tool calls get unique run_ids (crewAI >= 1.0).

    Each retry emits a new start event with a new event_id, so each attempt
    gets its own span in the trace.
    """
    # Given: two attempts on the same ToolUsage instance
    source = MockSource()
    first_event_id = str(uuid.uuid4())
    second_event_id = str(uuid.uuid4())

    first_start = MockEvent(tool_name="SearchTool", tool_args="query", event_id=first_event_id)
    first_error = MockEvent(tool_name="search_tool", tool_args={}, error="fail", started_event_id=first_event_id)
    second_start = MockEvent(tool_name="SearchTool", tool_args="query", event_id=second_event_id)
    second_finish = MockEvent(tool_name="search_tool", tool_args={}, output="ok", started_event_id=second_event_id)

    # When: generating run_ids for both attempts
    rid_1_start = crewai_callback._generate_run_id(source, first_start)
    rid_1_error = crewai_callback._generate_run_id(source, first_error)
    rid_2_start = crewai_callback._generate_run_id(source, second_start)
    rid_2_finish = crewai_callback._generate_run_id(source, second_finish)

    # Then: each attempt correlates correctly and is distinct from the other
    assert rid_1_start == rid_1_error
    assert rid_2_start == rid_2_finish
    assert rid_1_start != rid_2_start


def test_tool_lifecycle_previous_event_id(crewai_callback) -> None:
    """Test tool start/end correlation via previous_event_id (crewAI >= 1.0).

    Newer crewAI versions use previous_event_id instead of started_event_id
    to link finish/error events back to the corresponding start event.
    """
    # Given: a source without .id and events using previous_event_id
    source = MockSource()
    start_event_id = str(uuid.uuid4())

    start_event = MockEvent(
        tool_name="duck_duck_go_search", tool_args={"query": "latest advancements in AI"}, event_id=start_event_id
    )
    # Finish event uses previous_event_id (not started_event_id)
    end_event = MockEvent(
        tool_name="duck_duck_go_search",
        tool_args={"query": "latest advancements in AI"},
        output="No good DuckDuckGo Search Result was found",
        event_id=str(uuid.uuid4()),
        previous_event_id=start_event_id,
    )

    # When: generating run_ids for both events
    run_id_start = crewai_callback._generate_run_id(source, start_event)
    run_id_end = crewai_callback._generate_run_id(source, end_event)

    # Then: both produce the same UUID
    assert run_id_start == run_id_end
    assert isinstance(run_id_start, uuid.UUID)


def test_tool_lifecycle_previous_event_id_full(crewai_callback) -> None:
    """Test full tool start/finish lifecycle with previous_event_id (crewAI >= 1.0)."""
    # Given: events matching real crewAI output (agent as null, agent_id as string)
    source = MockSource()
    agent_id = str(uuid.uuid4())
    start_event_id = str(uuid.uuid4())

    start_event = MockEvent(
        agent=None,
        agent_id=agent_id,
        tool_name="duck_duck_go_search",
        tool_args={"query": "test"},
        event_id=start_event_id,
    )
    end_event = MockEvent(
        agent=None,
        agent_id=agent_id,
        tool_name="duck_duck_go_search",
        tool_args={"query": "test"},
        output="search results",
        event_id=str(uuid.uuid4()),
        previous_event_id=start_event_id,
    )

    with (
        patch.object(crewai_callback._handler, "start_node") as mock_start,
        patch.object(crewai_callback._handler, "end_node") as mock_end,
    ):
        # When: handling start and finish
        crewai_callback._handle_tool_usage_started(source, start_event)
        crewai_callback._handle_tool_usage_finished(source, end_event)

        # Then: both use the same run_id and parent is resolved from agent_id
        start_run_id = mock_start.call_args[1]["run_id"]
        end_run_id = mock_end.call_args[1]["run_id"]
        assert start_run_id == end_run_id
        assert str(mock_start.call_args[1]["parent_run_id"]) == agent_id


def test_tool_usage_started_agent_id_fallback(crewai_callback) -> None:
    """Test tool usage started resolves parent from event.agent_id when event.agent is None."""
    # Given: an event with agent=None but agent_id as a top-level string (crewAI >= 1.0)
    source = MockSource()
    agent_id = str(uuid.uuid4())
    event = MockEvent(
        agent=None, agent_id=agent_id, tool_name="web_search", tool_args={"query": "test"}, event_id=str(uuid.uuid4())
    )

    with patch.object(crewai_callback._handler, "start_node") as mock_start_node:
        # When: handling the event
        crewai_callback._handle_tool_usage_started(source, event)

        # Then: parent_run_id is resolved from the top-level agent_id
        call_args = mock_start_node.call_args[1]
        assert str(call_args["parent_run_id"]) == agent_id
        assert call_args["name"] == "web_search"


def test_tool_lifecycle_previous_event_id_with_error(crewai_callback) -> None:
    """Test tool start/error correlation via previous_event_id (crewAI >= 1.0)."""
    # Given: a tool that fails, error event uses previous_event_id
    source = MockSource()
    agent_id = str(uuid.uuid4())
    start_event_id = str(uuid.uuid4())

    start_event = MockEvent(
        agent=None, agent_id=agent_id, tool_name="web_search", tool_args={"query": "test"}, event_id=start_event_id
    )
    error_event = MockEvent(
        tool_name="web_search",
        tool_args={"query": "test"},
        error="Connection timeout",
        event_id=str(uuid.uuid4()),
        previous_event_id=start_event_id,
    )

    with (
        patch.object(crewai_callback._handler, "start_node") as mock_start,
        patch.object(crewai_callback._handler, "end_node") as mock_end,
    ):
        # When: handling start and error
        crewai_callback._handle_tool_usage_started(source, start_event)
        crewai_callback._handle_tool_usage_error(source, error_event)

        # Then: both use the same run_id
        start_run_id = mock_start.call_args[1]["run_id"]
        end_run_id = mock_end.call_args[1]["run_id"]
        assert start_run_id == end_run_id
