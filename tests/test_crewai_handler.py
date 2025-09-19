import uuid
from datetime import datetime
from typing import Any
from unittest.mock import Mock, patch

import pytest

from galileo.handlers.crewai.handler import CrewAIEventListener
from galileo.schema.handlers import NodeType
from tests.testutils.setup import setup_mock_logstreams_client, setup_mock_projects_client, setup_mock_traces_client


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

        logger = GalileoLogger(project="test_project", log_stream="test_log_stream")
        return logger


@pytest.fixture
def crewai_callback(mock_galileo_logger):
    """Creates a CrewAIEventListener instance for testing."""
    with (
        patch("galileo.handlers.crewai.handler.CREWAI_AVAILABLE", False),
        patch("galileo.handlers.crewai.handler.LITE_LLM_AVAILABLE", False),
    ):
        from galileo.handlers.crewai.handler import CrewAIEventListener

        callback = CrewAIEventListener(
            galileo_logger=mock_galileo_logger, start_new_trace=True, flush_on_crew_completed=False
        )
        return callback


def test_initialization_with_crewai_available(mock_galileo_logger):
    """Test CrewAIEventListener initialization when CrewAI is available."""
    with (
        patch("galileo.handlers.crewai.handler.CREWAI_AVAILABLE", True),
        patch("galileo.handlers.crewai.handler.LITE_LLM_AVAILABLE", True),
        patch("galileo.handlers.crewai.handler.BaseEventListener"),
    ):
        from galileo.handlers.crewai.handler import CrewAIEventListener

        callback = CrewAIEventListener(
            galileo_logger=mock_galileo_logger, start_new_trace=False, flush_on_crew_completed=True
        )

        assert callback._handler._galileo_logger == mock_galileo_logger
        assert callback._handler._start_new_trace is False
        assert callback._handler._flush_on_chain_end is True


def test_initialization_with_crewai_unavailable(mock_galileo_logger):
    """Test CrewAIEventListener initialization when CrewAI is unavailable."""
    with (
        patch("galileo.handlers.crewai.handler.CREWAI_AVAILABLE", False),
        patch("galileo.handlers.crewai.handler.LITE_LLM_AVAILABLE", False),
    ):
        from galileo.handlers.crewai.handler import CrewAIEventListener

        callback = CrewAIEventListener(galileo_logger=mock_galileo_logger)

        assert callback._handler._galileo_logger == mock_galileo_logger


def test_generate_run_id_with_source_id(crewai_callback):
    """Test UUID generation when source has an ID."""
    source_id = uuid.uuid4()
    source = MockSource(id=source_id)
    event = MockEvent()

    result = crewai_callback._generate_run_id(source, event)
    assert result == source_id


def test_generate_run_id_with_messages(crewai_callback):
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


def test_generate_run_id_with_tool_args_dict(crewai_callback):
    """Test UUID generation from tool args as dict."""
    tool_args = {"arg1": "value1", "arg2": "value2"}
    event = MockEvent(tool_args=tool_args)
    source = MockSource()

    result = crewai_callback._generate_run_id(source, event)
    assert isinstance(result, uuid.UUID)


def test_generate_run_id_with_tool_args_string(crewai_callback):
    """Test UUID generation from tool args as string."""
    tool_args = '{"arg1": "value1"}'
    event = MockEvent(tool_args=tool_args)
    source = MockSource()

    result = crewai_callback._generate_run_id(source, event)
    assert isinstance(result, uuid.UUID)


def test_generate_run_id_fallback(crewai_callback):
    """Test UUID generation fallback method."""
    event = MockEvent(crew_name="test_crew", agent="test_agent", task="test_task")
    source = MockSource()

    result = crewai_callback._generate_run_id(source, event)
    assert isinstance(result, uuid.UUID)


def test_extract_metadata(crewai_callback):
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
def test_crew_kickoff_started(crewai_callback, generated_id):
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
def test_crew_kickoff_started_empty_inputs(crewai_callback, generated_id):
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
def test_crew_kickoff_completed(crewai_callback, generated_id):
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
def test_crew_kickoff_failed(crewai_callback, generated_id):
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
def test_agent_execution_started(crewai_callback, generated_id):
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
def test_agent_execution_started_no_input(crewai_callback, generated_id):
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
def test_agent_execution_completed(crewai_callback, generated_id):
    """Test agent execution completed event handling."""
    agent_id = generated_id()
    source = MockSource(id=agent_id)
    event = MockEvent(output="Agent task completed")

    with patch.object(crewai_callback._handler, "end_node") as mock_end_node:
        crewai_callback._handle_agent_execution_completed(source, event)

        mock_end_node.assert_called_once_with(run_id=agent_id, output="Agent task completed")


@pytest.mark.parametrize("generated_id", [lambda: uuid.uuid4(), lambda: str(uuid.uuid4())])
def test_agent_execution_error(crewai_callback, generated_id):
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
def test_task_started(crewai_callback, generated_id):
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
def test_task_started_no_context(crewai_callback, generated_id):
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
def test_task_started_no_description(crewai_callback, generated_id):
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
def test_task_completed(crewai_callback, generated_id):
    """Test task completed event handling."""
    task_id = generated_id()
    source = MockSource(id=task_id)
    output = MockOutput(raw="Task completed successfully")
    event = MockEvent(output=output)

    with patch.object(crewai_callback._handler, "end_node") as mock_end_node:
        crewai_callback._handle_task_completed(source, event)

        mock_end_node.assert_called_once_with(run_id=task_id, output="Task completed successfully")


@pytest.mark.parametrize("generated_id", [lambda: uuid.uuid4(), lambda: str(uuid.uuid4())])
def test_task_failed(crewai_callback, generated_id):
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
def test_tool_usage_started(crewai_callback, generated_id):
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
def test_tool_usage_started_no_input(crewai_callback, generated_id):
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
def test_tool_usage_finished(crewai_callback, generated_id):
    """Test tool usage finished event handling."""
    tool_id = generated_id()
    source = MockSource(id=tool_id)
    event = MockEvent(output="Tool execution completed")

    with patch.object(crewai_callback._handler, "end_node") as mock_end_node:
        crewai_callback._handle_tool_usage_finished(source, event)

        mock_end_node.assert_called_once_with(run_id=tool_id, output="Tool execution completed")


@pytest.mark.parametrize("generated_id", [lambda: uuid.uuid4(), lambda: str(uuid.uuid4())])
def test_tool_usage_error(crewai_callback, generated_id):
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
def test_llm_call_started(crewai_callback, generated_id):
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
def test_llm_call_completed(crewai_callback, generated_id):
    """Test LLM call completed event handling."""
    llm_id = generated_id()
    source = MockSource(id=llm_id)
    event = MockEvent(response="Hello! How can I help you?")

    with patch.object(crewai_callback._handler, "end_node") as mock_end_node:
        crewai_callback._handle_llm_call_completed(source, event)

        mock_end_node.assert_called_once_with(run_id=llm_id, output="Hello! How can I help you?")


@pytest.mark.parametrize("generated_id", [lambda: uuid.uuid4(), lambda: str(uuid.uuid4())])
def test_llm_call_failed(crewai_callback, generated_id):
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


def test_setup_listeners_crewai_unavailable(crewai_callback: CrewAIEventListener):
    """Test setup_listeners when CrewAI is unavailable."""
    mock_event_bus = Mock()

    with patch("galileo.handlers.crewai.handler.CREWAI_AVAILABLE", False):
        crewai_callback.setup_listeners(mock_event_bus)

        # Verify that no event listeners were registered
        mock_event_bus.on.assert_not_called()


def test_update_crew_input(crewai_callback: CrewAIEventListener):
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


def test_lite_llm_usage_callback(crewai_callback: CrewAIEventListener):
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


def test_lite_llm_usage_callback_no_node(crewai_callback):
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
