import uuid
from unittest.mock import MagicMock, Mock, patch

import pytest
from langchain_core.agents import AgentFinish
from langchain_core.documents import Document
from langchain_core.messages import AIMessage, HumanMessage

from galileo import Message, MessageRole
from galileo.handlers.langchain import GalileoCallback
from galileo.handlers.langchain.handler import _root_node
from galileo.logger import GalileoLogger
from galileo_core.schemas.shared.document import Document as GalileoDocument
from tests.testutils.setup import setup_mock_core_api_client, setup_mock_logstreams_client, setup_mock_projects_client


class TestGalileoCallback:
    @pytest.fixture
    @patch("galileo.logger.LogStreams")
    @patch("galileo.logger.Projects")
    @patch("galileo.logger.GalileoCoreApiClient")
    def galileo_logger(self, mock_core_api_client: Mock, mock_projects_client: Mock, mock_logstreams_client: Mock):
        """Creates a mock Galileo logger for testing"""
        setup_mock_core_api_client(mock_core_api_client)
        setup_mock_projects_client(mock_projects_client)
        setup_mock_logstreams_client(mock_logstreams_client)
        logger = GalileoLogger(project="my_project", log_stream="my_log_stream")
        return logger

    @pytest.fixture
    def callback(self, galileo_logger: GalileoLogger) -> GalileoCallback:
        """Creates a GalileoCallback with a mock logger"""
        callback = GalileoCallback(galileo_logger=galileo_logger, flush_on_chain_end=False)
        # Reset the root node before each test
        _root_node.set(None)
        yield callback
        # Clean up after each test
        _root_node.set(None)

    def test_initialization(self, galileo_logger: GalileoLogger):
        """Test callback initialization with various parameters"""
        # Default initialization
        callback = GalileoCallback(galileo_logger=galileo_logger)
        assert callback._galileo_logger == galileo_logger
        assert callback._start_new_trace is True
        assert callback._flush_on_chain_end is True
        assert callback._nodes == {}

        # Custom initialization
        callback = GalileoCallback(galileo_logger=galileo_logger, start_new_trace=False, flush_on_chain_end=False)
        assert callback._start_new_trace is False
        assert callback._flush_on_chain_end is False

    def test_start_node(self, callback: GalileoCallback):
        """Test creating a node and establishing parent-child relationships"""
        # Create a parent node
        parent_id = uuid.uuid4()
        node = callback._start_node(
            node_type="chain", parent_run_id=None, run_id=parent_id, name="Parent Chain", input={"query": "test"}
        )

        assert node.node_type == "chain"
        assert node.run_id == parent_id
        assert node.parent_run_id is None
        assert "name" in node.span_params
        assert node.span_params["name"] == "Parent Chain"
        assert str(parent_id) in callback._nodes
        assert "start_time" in node.span_params

        # Create a child node
        child_id = uuid.uuid4()
        child_node = callback._start_node(
            node_type="llm", parent_run_id=parent_id, run_id=child_id, name="Child LLM", input="test prompt"
        )

        assert child_node.node_type == "llm"
        assert child_node.parent_run_id == parent_id
        assert str(child_id) in callback._nodes

        # Verify parent-child relationship was established
        assert str(child_id) in callback._nodes[str(parent_id)].children

        # Verify root node was set properly
        assert _root_node.get().run_id == parent_id

    def test_end_node(self, callback: GalileoCallback, galileo_logger: GalileoLogger):
        """Test ending a node and updating its parameters"""
        # Create a node
        run_id = uuid.uuid4()
        callback._start_node(
            node_type="chain", parent_run_id=None, run_id=run_id, name="Test Chain", input='{"query": "test"}'
        )

        # End the node and commit the trace
        callback._end_node(run_id, output='{"result": "test result"}')

        traces = galileo_logger.traces
        assert len(traces) == 1
        assert len(traces[0].spans) == 1
        assert traces[0].spans[0].name == "Test Chain"
        assert traces[0].spans[0].type == "workflow"
        assert traces[0].spans[0].input == '{"query": "test"}'
        assert traces[0].spans[0].output == '{"result": "test result"}'

    def test_on_chain_start_end(self, callback: GalileoCallback, galileo_logger: GalileoLogger):
        """Test chain start and end callbacks"""
        run_id = uuid.uuid4()

        # Start chain
        callback.on_chain_start(serialized={"name": "TestChain"}, inputs='{"query": "test question"}', run_id=run_id)

        assert str(run_id) in callback._nodes
        assert callback._nodes[str(run_id)].node_type == "chain"
        assert callback._nodes[str(run_id)].span_params["input"] == '{"query": "test question"}'
        assert callback._nodes[str(run_id)].span_params["start_time"] > 0

        # End chain
        callback.on_chain_end(outputs='{"result": "test answer"}', run_id=run_id)

        # Verify chain was properly ended
        # assert callback._nodes.get(str(run_id)).span_params["output"] == '{"result": "test answer"}'

        traces = galileo_logger.traces
        assert len(traces) == 1
        assert len(traces[0].spans) == 1
        assert traces[0].spans[0].name == "TestChain"
        assert traces[0].spans[0].type == "workflow"
        assert traces[0].spans[0].input == '{"query": "test question"}'
        assert traces[0].spans[0].output == '{"result": "test answer"}'

    def test_on_chain_start_with_kwargs_serialised_none(self, callback: GalileoCallback, galileo_logger: GalileoLogger):
        run_id = uuid.uuid4()

        # Start chain
        callback.on_chain_start(
            serialized=None,
            inputs={
                "messages": [
                    HumanMessage(
                        content="What does Lilian Weng say about the types of agent memory?",
                        additional_kwargs={},
                        response_metadata={},
                    )
                ]
            },
            run_id=run_id,
            name="LangGraph",
        )

        assert str(run_id) in callback._nodes
        assert callback._nodes[str(run_id)].node_type == "agent"
        assert (
            callback._nodes[str(run_id)].span_params["input"]
            == '{"messages": [{"content": "What does Lilian Weng say about the types of agent memory?"}]}'
        )

        # End chain
        callback.on_chain_end(outputs='{"result": "test answer"}', run_id=run_id)

        traces = galileo_logger.traces
        assert len(traces) == 1
        assert len(traces[0].spans) == 1
        assert traces[0].spans[0].name == "Agent"
        assert traces[0].spans[0].type == "workflow"
        assert (
            traces[0].spans[0].input
            == '{"messages": [{"content": "What does Lilian Weng say about the types of agent memory?"}]}'
        )
        assert traces[0].spans[0].output == '{"result": "test answer"}'

    def test_on_agent_chain(self, callback: GalileoCallback, galileo_logger: GalileoLogger):
        """Test agent chain handling"""
        run_id = uuid.uuid4()

        # Start agent chain
        callback.on_chain_start(serialized={"name": "Agent"}, inputs={"input": "test input"}, run_id=run_id)

        assert callback._nodes[str(run_id)].node_type == "agent"

        # End with agent finish
        finish = AgentFinish(return_values={"output": "test result"}, log="log message")

        callback.on_agent_finish(finish=finish, run_id=run_id)

        traces = galileo_logger.traces
        assert len(traces) == 1
        assert len(traces[0].spans) == 1
        assert traces[0].spans[0].name == "Agent"
        assert traces[0].spans[0].type == "workflow"
        assert traces[0].spans[0].input == '{"input": "test input"}'
        assert traces[0].spans[0].output == '{"return_values": {"output": "test result"}, "log": "log message"}'

    def test_on_llm_start_end(self, callback: GalileoCallback):
        """Test LLM start and end callbacks"""
        parent_id = uuid.uuid4()
        run_id = uuid.uuid4()

        # Create parent chain
        callback.on_chain_start(serialized={}, inputs={"query": "test"}, run_id=parent_id)

        # Start LLM
        callback.on_llm_start(
            serialized={},
            prompts=["Tell me about AI"],
            run_id=run_id,
            parent_run_id=parent_id,
            invocation_params={"model_name": "gpt-4", "temperature": 0.7},
        )

        assert str(run_id) in callback._nodes
        assert callback._nodes[str(run_id)].node_type == "llm"
        assert callback._nodes[str(run_id)].span_params["model"] == "gpt-4"
        assert callback._nodes[str(run_id)].span_params["temperature"] == 0.7
        assert callback._nodes[str(run_id)].span_params["input"] == [{"content": "Tell me about AI", "role": "user"}]

        # Add a token to test token timing
        callback.on_llm_new_token("AI", run_id=run_id)

        # End LLM
        llm_response = MagicMock()
        llm_response.generations = [[MagicMock()]]
        llm_response.llm_output = {"token_usage": {"prompt_tokens": 10, "completion_tokens": 20, "total_tokens": 30}}

        # Mock dict method on the generation
        llm_response.generations[0][0].dict.return_value = {"text": "AI is a technology..."}

        callback.on_llm_end(response=llm_response, run_id=run_id, parent_run_id=parent_id)

        # Verify token counts were set
        assert callback._nodes[str(run_id)].span_params["num_input_tokens"] == 10
        assert callback._nodes[str(run_id)].span_params["num_output_tokens"] == 20
        assert callback._nodes[str(run_id)].span_params["total_tokens"] == 30
        assert callback._nodes[str(run_id)].span_params["duration_ns"] > 0

    def test_on_chat_model_start(self, callback: GalileoCallback):
        """Test chat model start callback"""
        parent_id = uuid.uuid4()
        run_id = uuid.uuid4()

        # Create parent chain
        callback.on_chain_start(serialized={}, inputs={"query": "test"}, run_id=parent_id)

        # Start chat model (llm)
        human_message = HumanMessage(content="Tell me about AI")
        ai_message = AIMessage(content="AI is a technology...")
        messages = [[human_message, ai_message]]

        callback.on_chat_model_start(
            serialized={},
            messages=messages,
            run_id=run_id,
            parent_run_id=parent_id,
            invocation_params={"model": "gpt-4o", "temperature": 0.7},
        )

        assert str(run_id) in callback._nodes
        assert callback._nodes[str(run_id)].node_type == "chat"
        assert callback._nodes[str(run_id)].span_params["model"] == "gpt-4o"
        assert callback._nodes[str(run_id)].span_params["temperature"] == 0.7
        assert callback._nodes[str(run_id)].span_params["start_time"] > 0

        # Check that message serialization worked
        input_data = callback._nodes[str(run_id)].span_params["input"]
        assert isinstance(input_data, list)
        assert len(input_data) == 2  # Two messages
        assert input_data[0]["content"] == "Tell me about AI"
        assert input_data[1]["content"] == "AI is a technology..."

    def test_on_chat_model_start_end_with_tools(self, callback: GalileoCallback, galileo_logger: GalileoLogger):
        """Test chat model start and end callbacks with tools"""
        run_id = uuid.uuid4()
        chain_id = uuid.uuid4()

        # Start chat model
        human_message = HumanMessage(content="What is the sine of 90 degrees?")
        messages = [[human_message]]

        callback.on_chat_model_start(
            serialized={},
            messages=messages,
            run_id=run_id,
            parent_run_id=chain_id,
            invocation_params={
                "model": "gpt-4o",
                "temperature": 0.7,
                "tools": [
                    {
                        "type": "function",
                        "function": {
                            "name": "sin",
                            "description": "Calculate the sine of a number.",
                            "parameters": {
                                "properties": {"x": {"type": "number"}},
                                "required": ["x"],
                                "type": "object",
                            },
                        },
                    }
                ],
            },
        )

        assert str(run_id) in callback._nodes
        assert callback._nodes[str(run_id)].node_type == "chat"
        assert callback._nodes[str(run_id)].span_params["model"] == "gpt-4o"
        assert callback._nodes[str(run_id)].span_params["temperature"] == 0.7
        assert callback._nodes[str(run_id)].span_params["tools"] == [
            {
                "type": "function",
                "function": {
                    "name": "sin",
                    "description": "Calculate the sine of a number.",
                    "parameters": {"properties": {"x": {"type": "number"}}, "required": ["x"], "type": "object"},
                },
            }
        ]

        # End chat model (llm)
        llm_response = MagicMock()
        llm_response.generations = [[MagicMock()]]
        llm_response.llm_output = {"token_usage": {"total_tokens": 100}}
        llm_response.generations[0][0].dict.return_value = "The sine of 90 degrees is 0.9999999999999999"

        callback.on_llm_end(response=llm_response, run_id=run_id, parent_run_id=chain_id)

        traces = galileo_logger.traces
        assert len(traces) == 1
        assert len(traces[0].spans) == 1
        assert traces[0].spans[0].name == "Chat"
        assert traces[0].spans[0].type == "llm"
        assert traces[0].spans[0].tools == [
            {
                "type": "function",
                "function": {
                    "name": "sin",
                    "description": "Calculate the sine of a number.",
                    "parameters": {"properties": {"x": {"type": "number"}}, "required": ["x"], "type": "object"},
                },
            }
        ]

    def test_on_tool_start_end_with_string_output(self, callback: GalileoCallback):
        """Test tool start and end callbacks"""
        parent_id = uuid.uuid4()
        run_id = uuid.uuid4()

        # Create parent chain
        callback.on_chain_start(serialized={}, inputs={"query": "test"}, run_id=parent_id)

        # Start tool
        callback.on_tool_start(
            serialized={"name": "calculator"}, input_str="2+2", run_id=run_id, parent_run_id=parent_id
        )

        assert str(run_id) in callback._nodes
        assert callback._nodes[str(run_id)].node_type == "tool"
        assert callback._nodes[str(run_id)].span_params["input"] == "2+2"

        # End tool with a string output
        callback.on_tool_end(output="4", run_id=run_id, parent_run_id=parent_id)

        assert callback._nodes[str(run_id)].span_params["duration_ns"] > 0
        assert callback._nodes[str(run_id)].span_params["output"] == "4"

    def test_on_tool_start_end_with_object_output(self, callback: GalileoCallback):
        """Test tool start and end callbacks"""
        parent_id = uuid.uuid4()
        run_id = uuid.uuid4()

        # Create parent chain
        callback.on_chain_start(serialized={}, inputs={"query": "test"}, run_id=parent_id)

        # Start tool
        callback.on_tool_start(
            serialized={"name": "calculator"}, input_str="2+2", run_id=run_id, parent_run_id=parent_id
        )

        assert str(run_id) in callback._nodes
        assert callback._nodes[str(run_id)].node_type == "tool"
        assert callback._nodes[str(run_id)].span_params["input"] == "2+2"

        class ToolResponseWithContent:
            def __init__(self, content, tool_call_id, status, role):
                self.content = content
                self.tool_call_id = tool_call_id
                self.status = status
                self.role = role

        # End tool with an object output with a content field
        callback.on_tool_end(
            output=ToolResponseWithContent(content="tool response", tool_call_id="1", status="success", role="tool"),
            run_id=run_id,
            parent_run_id=parent_id,
        )

        assert str(run_id) in callback._nodes
        assert callback._nodes[str(run_id)].node_type == "tool"
        assert callback._nodes[str(run_id)].span_params["input"] == "2+2"
        assert callback._nodes[str(run_id)].span_params["output"] == "tool response"

        # Start tool
        callback.on_tool_start(
            serialized={"name": "calculator"}, input_str="2+2", run_id=run_id, parent_run_id=parent_id
        )

        class ToolResponseWithoutContent:
            def __init__(self, tool_call_id, status, role):
                self.tool_call_id = tool_call_id
                self.status = status
                self.role = role

        # End tool with an object output without a content field
        callback.on_tool_end(
            output=ToolResponseWithoutContent(tool_call_id="1", status="success", role="tool"),
            run_id=run_id,
            parent_run_id=parent_id,
        )

        assert str(run_id) in callback._nodes
        assert callback._nodes[str(run_id)].node_type == "tool"
        assert callback._nodes[str(run_id)].span_params["input"] == "2+2"
        assert (
            callback._nodes[str(run_id)].span_params["output"]
            == '{"tool_call_id": "1", "status": "success", "role": "tool"}'
        )

    def test_on_tool_start_end_with_dict_output(self, callback: GalileoCallback):
        """Test tool start and end callbacks"""
        parent_id = uuid.uuid4()
        run_id = uuid.uuid4()

        # Create parent chain
        callback.on_chain_start(serialized={}, inputs={"query": "test"}, run_id=parent_id)

        # Start tool
        callback.on_tool_start(
            serialized={"name": "calculator"}, input_str="2+2", run_id=run_id, parent_run_id=parent_id
        )

        assert str(run_id) in callback._nodes
        assert callback._nodes[str(run_id)].node_type == "tool"
        assert callback._nodes[str(run_id)].span_params["input"] == "2+2"

        # End tool with a dict output with a content field
        callback.on_tool_end(
            output={"content": "tool response", "tool_call_id": "1", "status": "success", "role": "tool"},
            run_id=run_id,
            parent_run_id=parent_id,
        )

        assert str(run_id) in callback._nodes
        assert callback._nodes[str(run_id)].node_type == "tool"
        assert callback._nodes[str(run_id)].span_params["input"] == "2+2"
        assert callback._nodes[str(run_id)].span_params["output"] == "tool response"

        # Start tool
        callback.on_tool_start(
            serialized={"name": "calculator"}, input_str="2+2", run_id=run_id, parent_run_id=parent_id
        )

        # End tool with an object output without a content field
        callback.on_tool_end(
            output={"tool_call_id": "1", "status": "success", "role": "tool"}, run_id=run_id, parent_run_id=parent_id
        )

        assert (
            callback._nodes[str(run_id)].span_params["output"]
            == '{"tool_call_id": "1", "status": "success", "role": "tool"}'
        )

    def test_on_retriever_start_end(self, callback: GalileoCallback):
        """Test retriever start and end callbacks"""
        parent_id = uuid.uuid4()
        run_id = uuid.uuid4()

        # Create parent chain
        callback.on_chain_start(serialized={}, inputs={"query": "test"}, run_id=parent_id)

        # Start retriever
        callback.on_retriever_start(serialized={}, query="AI development", run_id=run_id, parent_run_id=parent_id)

        assert str(run_id) in callback._nodes
        assert callback._nodes[str(run_id)].node_type == "retriever"
        assert callback._nodes[str(run_id)].span_params["input"] == "AI development"

        # End retriever
        document = Document(page_content="AI is advancing rapidly", metadata={"source": "textbook"})
        callback.on_retriever_end(documents=[document], run_id=run_id, parent_run_id=parent_id)

        assert isinstance(callback._nodes[str(run_id)].span_params["output"], list)
        assert len(callback._nodes[str(run_id)].span_params["output"]) == 1

    def test_complex_execution_flow(self, callback: GalileoCallback, galileo_logger: GalileoLogger):
        """Test a complex execution flow with multiple component types"""
        # Create UUIDs for different components
        chain_id = uuid.uuid4()
        llm_id = uuid.uuid4()
        tool_id = uuid.uuid4()
        retriever_id = uuid.uuid4()

        # Start main chain
        callback.on_chain_start(
            serialized={}, inputs={"query": "What can you tell me about the latest AI research?"}, run_id=chain_id
        )

        # Start retriever
        callback.on_retriever_start(
            serialized={}, query="latest AI research", run_id=retriever_id, parent_run_id=chain_id
        )

        # End retriever
        document = Document(page_content="Recent advances in large language models...", metadata={"source": "paper"})
        callback.on_retriever_end(documents=[document], run_id=retriever_id, parent_run_id=chain_id)

        # Start LLM
        callback.on_llm_start(
            serialized={},
            prompts=["Summarize this research: Recent advances in large language models..."],
            run_id=llm_id,
            parent_run_id=chain_id,
            invocation_params={"model_name": "gpt-4"},
            metadata={"extras": {"source": "paper"}},
        )

        # End LLM
        llm_response = MagicMock()
        llm_response.generations = [[MagicMock()]]
        llm_response.llm_output = {"token_usage": {"total_tokens": 100}}
        llm_response.generations[0][0].dict.return_value = {"text": "LLMs have seen significant progress..."}

        callback.on_llm_end(response=llm_response, run_id=llm_id, parent_run_id=chain_id)

        # Start tool
        callback.on_tool_start(
            serialized={},
            input_str="verify(LLMs have seen significant progress)",
            run_id=tool_id,
            parent_run_id=chain_id,
            metadata={"key": "value", "extras": {"tools": "tool1"}},
        )

        # End tool
        callback.on_tool_end(output="Verification complete: accurate statement", run_id=tool_id, parent_run_id=chain_id)

        # End chain
        callback.on_chain_end(
            outputs={"result": "Recent AI research has focused on LLMs which have seen significant progress..."},
            run_id=chain_id,
        )

        traces = galileo_logger.traces
        assert len(traces) == 1
        assert len(traces[0].spans) == 1  # 1 workflow span
        assert len(traces[0].spans[0].spans) == 3  # 3 child spans
        assert traces[0].spans[0].name == "Chain"
        assert traces[0].spans[0].type == "workflow"
        assert traces[0].spans[0].input == '{"query": "What can you tell me about the latest AI research?"}'
        assert (
            traces[0].spans[0].output
            == '{"result": "Recent AI research has focused on LLMs which have seen significant progress..."}'
        )
        assert traces[0].spans[0].spans[0].type == "retriever"
        assert traces[0].spans[0].spans[0].input == "latest AI research"
        assert traces[0].spans[0].spans[0].output == [
            GalileoDocument(content="Recent advances in large language models...", metadata={"source": "paper"})
        ]
        assert traces[0].spans[0].spans[1].type == "llm"
        assert traces[0].spans[0].spans[1].input == [
            Message(
                content="Summarize this research: Recent advances in large language models...", role=MessageRole.user
            )
        ]
        assert traces[0].spans[0].spans[1].output == Message(
            content='{"text": "LLMs have seen significant progress..."}',
            role=MessageRole.assistant,
            tool_call_id=None,
            tool_calls=None,
        )
        assert traces[0].spans[0].spans[1].user_metadata == {"extras": "{'source': 'paper'}"}
        assert traces[0].spans[0].spans[2].type == "tool"
        assert traces[0].spans[0].spans[2].input == "verify(LLMs have seen significant progress)"
        assert traces[0].spans[0].spans[2].output == "Verification complete: accurate statement"
        assert traces[0].spans[0].spans[2].user_metadata == {"key": "value", "extras": "{'tools': 'tool1'}"}

    def test_missing_parent_node(self, callback: GalileoCallback):
        """Test handling of missing parent nodes"""
        parent_id = uuid.uuid4()
        child_id = uuid.uuid4()

        # Start child with non-existent parent
        callback._start_node(
            node_type="llm",
            parent_run_id=parent_id,  # This parent doesn't exist
            run_id=child_id,
            name="Test LLM",
            input="test prompt",
        )

        # Child should still be created
        assert str(child_id) in callback._nodes
        assert callback._nodes[str(child_id)].parent_run_id == parent_id

    def test_serialization_error_handling(self, callback: GalileoCallback):
        """Test handling of serialization errors"""
        run_id = uuid.uuid4()

        # Create a mock object that will cause serialization errors
        class UnserializableObject:
            def __repr__(self):
                return "UnserializableObject()"

        unserializable = UnserializableObject()

        # Test retriever with unserializable response
        callback.on_chain_start(serialized={}, inputs={"query": "test"}, run_id=run_id)

        retriever_id = uuid.uuid4()
        callback.on_retriever_start(serialized={}, query="test query", run_id=retriever_id, parent_run_id=run_id)

        # This should be handled gracefully
        with patch("json.dumps", side_effect=TypeError("Cannot serialize")):
            callback.on_retriever_end(documents=[unserializable], run_id=retriever_id, parent_run_id=run_id)

        # Node should still exist and output should be a string
        assert str(retriever_id) in callback._nodes
        assert isinstance(callback._nodes[str(retriever_id)].span_params["output"], str)

    def test_get_node_name(self, callback: GalileoCallback):
        """Test the _get_node_name method to ensure it correctly extracts names from serialized data"""
        # Case 1: Serialized has a name key
        serialized = {"name": "CustomNodeName", "other_key": "value"}
        result = callback._get_node_name("chain", serialized)
        assert result == "CustomNodeName"

        # Case 2: Serialized has no name key but has an id key with a list value
        serialized = {"id": ["module", "class", "method_name"], "other_key": "value"}
        result = callback._get_node_name("llm", serialized)
        assert result == "method_name"

        # Case 3: Serialized has both name and id, name should be used first
        serialized = {"name": "NamedNode", "id": ["module", "class", "method_name"], "other_key": "value"}
        result = callback._get_node_name("tool", serialized)
        assert result == "NamedNode"

        # Case 4: Serialized has neither name nor id keys
        serialized = {"other_key": "value"}
        result = callback._get_node_name("retriever", serialized)
        assert result == "Retriever"  # Should capitalize the node_type

        # Case 5: Serialized is None
        result = callback._get_node_name("agent", None)
        assert result == "Agent"  # Should capitalize the node_type

        # Case 6: Exception occurs (providing a non-dictionary serialized)
        result = callback._get_node_name("chain", "not_a_dict")
        assert result == "Chain"  # Should capitalize the node_type

    def test_callback_with_active_trace(self, galileo_logger: GalileoLogger):
        """Test that the callback properly handles an active trace."""
        run_id = uuid.uuid4()

        galileo_logger.start_trace(input="test input")

        # Pass the active logger to the callback
        callback = GalileoCallback(galileo_logger=galileo_logger, start_new_trace=False, flush_on_chain_end=False)

        # Start a chain (creates a workflow span)
        callback._start_node("chain", None, run_id, name="Test Chain", input='{"query": "test"}')

        # Add a retriever span
        retriever_id = uuid.uuid4()
        callback.on_retriever_start(serialized={}, query="test query", run_id=retriever_id, parent_run_id=run_id)
        callback.on_retriever_end(
            documents=[Document(page_content="test document")], run_id=retriever_id, parent_run_id=run_id
        )

        # End the chain (ends the workflow span)
        callback._end_node(run_id, output='{"result": "test result"}')

        galileo_logger.conclude(output="test output", status_code=200)

        traces = galileo_logger.traces

        assert len(traces) == 1
        assert len(traces[0].spans) == 1
        assert traces[0].spans[0].type == "workflow"
        assert traces[0].spans[0].input == '{"query": "test"}'
        assert traces[0].spans[0].output == '{"result": "test result"}'
        assert traces[0].spans[0].spans[0].name == "Retriever"
        assert traces[0].spans[0].spans[0].type == "retriever"
        assert traces[0].spans[0].spans[0].input == "test query"
        assert traces[0].spans[0].spans[0].output == [GalileoDocument(content="test document", metadata={})]
