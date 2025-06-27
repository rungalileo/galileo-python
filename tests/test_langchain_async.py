import asyncio
import uuid
from unittest.mock import MagicMock, Mock, patch

import pytest
from langchain_core.agents import AgentFinish
from langchain_core.documents import Document
from langchain_core.messages import AIMessage, HumanMessage
from pytest import mark

from galileo import Message, MessageRole
from galileo.handlers.langchain import GalileoAsyncCallback
from galileo.logger.logger import GalileoLogger
from galileo_core.schemas.shared.document import Document as GalileoDocument
from tests.testutils.setup import setup_mock_core_api_client, setup_mock_logstreams_client, setup_mock_projects_client


class TestGalileoAsyncCallback:
    @pytest.fixture
    @patch("galileo.logger.logger.LogStreams")
    @patch("galileo.logger.logger.Projects")
    @patch("galileo.logger.logger.GalileoCoreApiClient")
    def galileo_logger(self, mock_core_api_client: Mock, mock_projects_client: Mock, mock_logstreams_client: Mock):
        """Creates a mock Galileo logger for testing"""
        setup_mock_core_api_client(mock_core_api_client)
        setup_mock_projects_client(mock_projects_client)
        setup_mock_logstreams_client(mock_logstreams_client)
        logger = GalileoLogger(project="my_project", log_stream="my_log_stream")
        return logger

    @pytest.fixture
    def callback(self, galileo_logger: GalileoLogger) -> GalileoAsyncCallback:
        """Creates a GalileoCallback with a mock logger"""
        callback = GalileoAsyncCallback(galileo_logger=galileo_logger, flush_on_chain_end=False)
        # Reset the root node before each test
        callback._root_node = None
        yield callback
        # Clean up after each test
        callback._root_node = None

    @mark.asyncio
    async def test_initialization(self, galileo_logger: GalileoLogger):
        """Test callback initialization with various parameters"""
        # Default initialization
        callback = GalileoAsyncCallback(galileo_logger=galileo_logger)
        assert callback._galileo_logger == galileo_logger
        assert callback._start_new_trace is True
        assert callback._flush_on_chain_end is True
        assert callback._nodes == {}

        # Custom initialization
        callback = GalileoAsyncCallback(galileo_logger=galileo_logger, start_new_trace=False, flush_on_chain_end=False)
        assert callback._start_new_trace is False
        assert callback._flush_on_chain_end is False

    @mark.asyncio
    async def test_start_node(self, callback: GalileoAsyncCallback):
        """Test creating a node and establishing parent-child relationships"""
        # Create a parent node
        parent_id = uuid.uuid4()
        node = await callback._start_node(
            node_type="chain", parent_run_id=None, run_id=parent_id, name="Parent Chain", input={"query": "test"}
        )

        assert node.node_type == "chain"
        assert node.run_id == parent_id
        assert node.parent_run_id is None
        assert "name" in node.span_params
        assert node.span_params["name"] == "Parent Chain"
        assert node.span_params["start_time"] > 0
        assert str(parent_id) in callback._nodes

        # Create a child node
        child_id = uuid.uuid4()
        child_node = await callback._start_node(
            node_type="llm", parent_run_id=parent_id, run_id=child_id, name="Child LLM", input="test prompt"
        )

        assert child_node.node_type == "llm"
        assert child_node.parent_run_id == parent_id
        assert str(child_id) in callback._nodes

        # Verify parent-child relationship was established
        assert str(child_id) in callback._nodes[str(parent_id)].children

        # Verify root node was set properly
        assert callback._root_node.run_id == parent_id

    @mark.asyncio
    async def test_end_node(self, callback: GalileoAsyncCallback, galileo_logger: GalileoLogger):
        """Test ending a node and updating its parameters"""
        # Create a node
        run_id = uuid.uuid4()
        await callback._start_node(
            node_type="chain", parent_run_id=None, run_id=run_id, name="Test Chain", input='{"query": "test"}'
        )

        # End the node and commit the trace
        await callback._end_node(run_id, output='{"result": "test result"}')

        traces = galileo_logger.traces
        assert len(traces) == 1
        assert len(traces[0].spans) == 1
        assert traces[0].spans[0].name == "Test Chain"
        assert traces[0].spans[0].type == "workflow"
        assert traces[0].spans[0].input == '{"query": "test"}'
        assert traces[0].spans[0].output == '{"result": "test result"}'

    @mark.asyncio
    async def test_on_chain_start_end(self, callback: GalileoAsyncCallback, galileo_logger: GalileoLogger):
        """Test chain start and end callbacks"""
        run_id = uuid.uuid4()

        # Start chain
        await callback.on_chain_start(
            serialized={"name": "TestChain"}, inputs='{"query": "test question"}', run_id=run_id
        )

        assert str(run_id) in callback._nodes
        assert callback._nodes[str(run_id)].node_type == "chain"
        assert callback._nodes[str(run_id)].span_params["input"] == '{"query": "test question"}'
        assert callback._nodes[str(run_id)].span_params["start_time"] > 0

        # End chain
        await callback.on_chain_end(outputs='{"result": "test answer"}', run_id=run_id)

        # Verify chain was properly ended
        # assert callback._nodes.get(str(run_id)).span_params["output"] == '{"result": "test answer"}'

        traces = galileo_logger.traces
        assert len(traces) == 1
        assert len(traces[0].spans) == 1
        assert traces[0].spans[0].name == "TestChain"
        assert traces[0].spans[0].type == "workflow"
        assert traces[0].spans[0].input == '{"query": "test question"}'
        assert traces[0].spans[0].output == '{"result": "test answer"}'
        assert traces[0].spans[0].step_number is None

    @mark.asyncio
    async def test_on_chain_start_end_with_input_update(
        self, callback: GalileoAsyncCallback, galileo_logger: GalileoLogger
    ):
        """Test chain start and end callbacks with input update (streaming mode)"""
        run_id = uuid.uuid4()

        # Start chain
        await callback.on_chain_start(serialized={"name": "TestChain"}, inputs="", run_id=run_id)

        assert str(run_id) in callback._nodes
        assert callback._nodes[str(run_id)].node_type == "chain"
        assert callback._nodes[str(run_id)].span_params["input"] == ""

        # End chain
        await callback.on_chain_end(
            outputs='{"result": "test answer"}', run_id=run_id, inputs={"query": "test question"}
        )

        traces = galileo_logger.traces
        assert len(traces) == 1
        assert len(traces[0].spans) == 1
        assert traces[0].spans[0].name == "TestChain"
        assert traces[0].spans[0].type == "workflow"
        assert traces[0].spans[0].input == '{"query": "test question"}'
        assert traces[0].spans[0].output == '{"result": "test answer"}'
        assert traces[0].spans[0].step_number is None

    @mark.asyncio
    async def test_on_agent_chain(self, callback: GalileoAsyncCallback, galileo_logger: GalileoLogger):
        """Test agent chain handling"""
        run_id = uuid.uuid4()

        # Start agent chain
        await callback.on_chain_start(serialized={"name": "agent"}, inputs={"input": "test input"}, run_id=run_id)

        assert callback._nodes[str(run_id)].node_type == "chain"

        # End with agent finish
        finish = AgentFinish(return_values={"output": "test result"}, log="log message")

        await callback.on_agent_finish(finish=finish, run_id=run_id)

        traces = galileo_logger.traces
        assert len(traces) == 1
        assert len(traces[0].spans) == 1
        assert traces[0].spans[0].name == "agent"
        assert traces[0].spans[0].type == "workflow"
        assert traces[0].spans[0].input == '{"input": "test input"}'
        assert traces[0].spans[0].output == '{"return_values": {"output": "test result"}, "log": "log message"}'
        assert traces[0].spans[0].step_number is None

    @mark.asyncio
    async def test_on_llm_start_end(self, callback: GalileoAsyncCallback):
        """Test LLM start and end callbacks"""
        parent_id = uuid.uuid4()
        run_id = uuid.uuid4()

        # Create parent chain
        await callback.on_chain_start(serialized={}, inputs={"query": "test"}, run_id=parent_id)

        # Start LLM
        await callback.on_llm_start(
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
        await callback.on_llm_new_token("AI", run_id=run_id)

        # End LLM
        llm_response = MagicMock()
        llm_response.generations = [[MagicMock()]]
        llm_response.llm_output = {"token_usage": {"prompt_tokens": 10, "completion_tokens": 20, "total_tokens": 30}}

        # Mock dict method on the generation
        llm_response.generations[0][0].dict.return_value = {"text": "AI is a technology..."}

        await callback.on_llm_end(response=llm_response, run_id=run_id, parent_run_id=parent_id)

        # Verify token counts were set
        assert callback._nodes[str(run_id)].span_params["num_input_tokens"] == 10
        assert callback._nodes[str(run_id)].span_params["num_output_tokens"] == 20
        assert callback._nodes[str(run_id)].span_params["total_tokens"] == 30
        assert callback._nodes[str(run_id)].span_params["duration_ns"] > 0

    @mark.asyncio
    async def test_on_chat_model_start(self, callback: GalileoAsyncCallback):
        """Test chat model start callback"""
        parent_id = uuid.uuid4()
        run_id = uuid.uuid4()

        # Create parent chain
        await callback.on_chain_start(serialized={}, inputs={"query": "test"}, run_id=parent_id)

        # Start chat model
        human_message = HumanMessage(content="Tell me about AI")
        ai_message = AIMessage(content="AI is a technology...")
        messages = [[human_message, ai_message]]

        await callback.on_chat_model_start(
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

        # Check that message serialization worked
        input_data = callback._nodes[str(run_id)].span_params["input"]
        assert isinstance(input_data, list)
        assert len(input_data) == 2  # Two messages
        assert input_data[0]["content"] == "Tell me about AI"
        assert input_data[1]["content"] == "AI is a technology..."

    @mark.asyncio
    async def test_on_chat_model_start_end_with_tools(
        self, callback: GalileoAsyncCallback, galileo_logger: GalileoLogger
    ):
        """Test chat model start and end callbacks with tools"""
        run_id = uuid.uuid4()
        chain_id = uuid.uuid4()

        # Start chat model
        human_message = HumanMessage(content="What is the sine of 90 degrees?")
        messages = [[human_message]]

        await callback.on_chat_model_start(
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

        await callback.on_llm_end(response=llm_response, run_id=run_id, parent_run_id=chain_id)

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
        assert traces[0].spans[0].step_number is None

    @mark.asyncio
    async def test_on_tool_start_end_with_string_output(self, callback: GalileoAsyncCallback):
        """Test tool start and end callbacks"""
        parent_id = uuid.uuid4()
        run_id = uuid.uuid4()

        # Create parent chain
        await callback.on_chain_start(serialized={}, inputs={"query": "test"}, run_id=parent_id)

        # Start tool
        await callback.on_tool_start(
            serialized={"name": "calculator"}, input_str="2+2", run_id=run_id, parent_run_id=parent_id
        )

        assert str(run_id) in callback._nodes
        assert callback._nodes[str(run_id)].node_type == "tool"
        assert callback._nodes[str(run_id)].span_params["input"] == "2+2"

        # End tool with a string output
        await callback.on_tool_end(output="4", run_id=run_id, parent_run_id=parent_id)

        assert callback._nodes[str(run_id)].span_params["output"] == "4"

    @mark.asyncio
    async def test_on_tool_start_end_with_object_output(self, callback: GalileoAsyncCallback):
        """Test tool start and end callbacks"""
        parent_id = uuid.uuid4()
        run_id = uuid.uuid4()

        # Create parent chain
        await callback.on_chain_start(serialized={}, inputs={"query": "test"}, run_id=parent_id)

        # Start tool
        await callback.on_tool_start(
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
        await callback.on_tool_end(
            output=ToolResponseWithContent(content="tool response", tool_call_id="1", status="success", role="tool"),
            run_id=run_id,
            parent_run_id=parent_id,
        )

        assert str(run_id) in callback._nodes
        assert callback._nodes[str(run_id)].node_type == "tool"
        assert callback._nodes[str(run_id)].span_params["input"] == "2+2"
        assert callback._nodes[str(run_id)].span_params["output"] == "tool response"

        # Start tool
        await callback.on_tool_start(
            serialized={"name": "calculator"}, input_str="2+2", run_id=run_id, parent_run_id=parent_id
        )

        class ToolResponseWithoutContent:
            def __init__(self, tool_call_id, status, role):
                self.tool_call_id = tool_call_id
                self.status = status
                self.role = role

        # End tool with an object output without a content field
        await callback.on_tool_end(
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

    @mark.asyncio
    async def test_on_tool_start_end_with_dict_output(self, callback: GalileoAsyncCallback):
        """Test tool start and end callbacks"""
        parent_id = uuid.uuid4()
        run_id = uuid.uuid4()

        # Create parent chain
        await callback.on_chain_start(serialized={}, inputs={"query": "test"}, run_id=parent_id)

        # Start tool
        await callback.on_tool_start(
            serialized={"name": "calculator"}, input_str="2+2", run_id=run_id, parent_run_id=parent_id
        )

        assert str(run_id) in callback._nodes
        assert callback._nodes[str(run_id)].node_type == "tool"
        assert callback._nodes[str(run_id)].span_params["input"] == "2+2"

        # End tool with a dict output with a content field
        await callback.on_tool_end(
            output={"content": "tool response", "tool_call_id": "1", "status": "success", "role": "tool"},
            run_id=run_id,
            parent_run_id=parent_id,
        )

        assert str(run_id) in callback._nodes
        assert callback._nodes[str(run_id)].node_type == "tool"
        assert callback._nodes[str(run_id)].span_params["input"] == "2+2"
        assert callback._nodes[str(run_id)].span_params["output"] == "tool response"

        # Start tool
        await callback.on_tool_start(
            serialized={"name": "calculator"}, input_str="2+2", run_id=run_id, parent_run_id=parent_id
        )

        # End tool with an object output without a content field
        await callback.on_tool_end(
            output={"tool_call_id": "1", "status": "success", "role": "tool"}, run_id=run_id, parent_run_id=parent_id
        )

        assert (
            callback._nodes[str(run_id)].span_params["output"]
            == '{"tool_call_id": "1", "status": "success", "role": "tool"}'
        )

    @mark.asyncio
    async def test_on_retriever_start_end(self, callback: GalileoAsyncCallback):
        """Test retriever start and end callbacks"""
        parent_id = uuid.uuid4()
        run_id = uuid.uuid4()

        # Create parent chain
        await callback.on_chain_start(serialized={}, inputs={"query": "test"}, run_id=parent_id)

        # Start retriever
        await callback.on_retriever_start(serialized={}, query="AI development", run_id=run_id, parent_run_id=parent_id)

        assert str(run_id) in callback._nodes
        assert callback._nodes[str(run_id)].node_type == "retriever"
        assert callback._nodes[str(run_id)].span_params["input"] == "AI development"

        # End retriever
        document = Document(page_content="AI is advancing rapidly", metadata={"source": "textbook"})
        await callback.on_retriever_end(documents=[document], run_id=run_id, parent_run_id=parent_id)

        assert isinstance(callback._nodes[str(run_id)].span_params["output"], list)
        assert len(callback._nodes[str(run_id)].span_params["output"]) == 1

    @mark.asyncio
    async def test_complex_execution_flow(self, callback: GalileoAsyncCallback, galileo_logger: GalileoLogger):
        """Test a complex execution flow with multiple component types"""
        # Create UUIDs for different components
        chain_id = uuid.uuid4()
        llm_id = uuid.uuid4()
        tool_id = uuid.uuid4()
        retriever_id = uuid.uuid4()

        # Start main chain
        await callback.on_chain_start(
            serialized={}, inputs={"query": "What can you tell me about the latest AI research?"}, run_id=chain_id
        )

        # Start retriever
        await callback.on_retriever_start(
            serialized={}, query="latest AI research", run_id=retriever_id, parent_run_id=chain_id
        )

        # End retriever
        document = Document(page_content="Recent advances in large language models...", metadata={"source": "paper"})
        await callback.on_retriever_end(documents=[document], run_id=retriever_id, parent_run_id=chain_id)

        # Start LLM
        await callback.on_llm_start(
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

        await callback.on_llm_end(response=llm_response, run_id=llm_id, parent_run_id=chain_id)

        # Start tool
        await callback.on_tool_start(
            serialized={},
            input_str="verify(LLMs have seen significant progress)",
            run_id=tool_id,
            parent_run_id=chain_id,
            metadata={"key": "value", "extras": {"tools": "tool1"}},
        )

        # End tool
        await callback.on_tool_end(
            output="Verification complete: accurate statement", run_id=tool_id, parent_run_id=chain_id
        )

        # End chain
        await callback.on_chain_end(
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
        assert traces[0].spans[0].step_number is None
        assert traces[0].spans[0].spans[0].type == "retriever"
        assert traces[0].spans[0].spans[0].input == "latest AI research"
        assert traces[0].spans[0].spans[0].output == [
            GalileoDocument(content="Recent advances in large language models...", metadata={"source": "paper"})
        ]
        assert traces[0].spans[0].spans[0].step_number is None
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
        assert traces[0].spans[0].spans[1].step_number is None
        assert traces[0].spans[0].spans[2].type == "tool"
        assert traces[0].spans[0].spans[2].input == "verify(LLMs have seen significant progress)"
        assert traces[0].spans[0].spans[2].output == "Verification complete: accurate statement"
        assert traces[0].spans[0].spans[2].user_metadata == {"key": "value", "extras": "{'tools': 'tool1'}"}
        assert traces[0].spans[0].spans[2].step_number is None

    @mark.asyncio
    async def test_missing_parent_node(self, callback: GalileoAsyncCallback):
        """Test handling of missing parent nodes"""
        parent_id = uuid.uuid4()
        child_id = uuid.uuid4()

        # Start child with non-existent parent
        await callback._start_node(
            node_type="llm",
            parent_run_id=parent_id,  # This parent doesn't exist
            run_id=child_id,
            name="Test LLM",
            input="test prompt",
        )

        # Child should still be created
        assert str(child_id) in callback._nodes
        assert callback._nodes[str(child_id)].parent_run_id == parent_id

    @mark.asyncio
    async def test_serialization_error_handling(self, callback: GalileoAsyncCallback):
        """Test handling of serialization errors"""
        run_id = uuid.uuid4()

        # Create a mock object that will cause serialization errors
        class UnserializableObject:
            def __repr__(self):
                return "UnserializableObject()"

        unserializable = UnserializableObject()

        # Test retriever with unserializable response
        await callback.on_chain_start(serialized={}, inputs={"query": "test"}, run_id=run_id)

        retriever_id = uuid.uuid4()
        await callback.on_retriever_start(serialized={}, query="test query", run_id=retriever_id, parent_run_id=run_id)

        # This should be handled gracefully
        with patch("json.dumps", side_effect=TypeError("Cannot serialize")):
            await callback.on_retriever_end(documents=[unserializable], run_id=retriever_id, parent_run_id=run_id)

        # Node should still exist and output should be a string
        assert str(retriever_id) in callback._nodes
        assert isinstance(callback._nodes[str(retriever_id)].span_params["output"], str)

    @mark.asyncio
    async def test_callback_with_active_trace(self, galileo_logger: GalileoLogger):
        """Test that the callback properly handles an active trace."""
        run_id = uuid.uuid4()

        galileo_logger.start_trace(input="test input")

        # Pass the active logger to the callback
        callback = GalileoAsyncCallback(galileo_logger=galileo_logger, start_new_trace=False, flush_on_chain_end=False)

        # Start a chain (creates a workflow span)
        await callback._start_node("chain", None, run_id, name="Test Chain", input='{"query": "test"}')

        # Add a retriever span
        retriever_id = uuid.uuid4()
        await callback.on_retriever_start(serialized={}, query="test query", run_id=retriever_id, parent_run_id=run_id)
        await callback.on_retriever_end(
            documents=[Document(page_content="test document")], run_id=retriever_id, parent_run_id=run_id
        )

        # End the chain (ends the workflow span)
        await callback._end_node(run_id, output='{"result": "test result"}')

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
        assert traces[0].spans[0].step_number is None

    @mark.asyncio
    async def test_node_created_at(self, callback: GalileoAsyncCallback, galileo_logger: GalileoLogger):
        parent_id = uuid.uuid4()
        llm_run_id = uuid.uuid4()
        retriever_run_id = uuid.uuid4()

        # Create parent chain
        await callback.on_chain_start(serialized={}, inputs={"query": "test"}, run_id=parent_id)

        # Start retriever
        await callback.on_retriever_start(
            serialized={}, query="AI development", run_id=retriever_run_id, parent_run_id=parent_id
        )

        # End retriever
        document = Document(page_content="AI is advancing rapidly", metadata={"source": "textbook"})
        await callback.on_retriever_end(documents=[document], run_id=retriever_run_id, parent_run_id=parent_id)

        delay_ms = 500

        await asyncio.sleep(delay_ms / 1000)

        await callback.on_llm_start(
            serialized={},
            prompts=["Tell me about AI"],
            run_id=llm_run_id,
            parent_run_id=parent_id,
            invocation_params={"model_name": "gpt-4", "temperature": 0.7},
        )

        # Add a token to test token timing
        await callback.on_llm_new_token("AI", run_id=llm_run_id)

        # End LLM
        llm_response = MagicMock()
        llm_response.generations = [[MagicMock()]]
        llm_response.llm_output = {"token_usage": {"prompt_tokens": 10, "completion_tokens": 20, "total_tokens": 30}}

        # Mock dict method on the generation
        llm_response.generations[0][0].dict.return_value = {"text": "AI is a technology..."}

        await callback.on_llm_end(response=llm_response, run_id=llm_run_id, parent_run_id=parent_id)

        # End chain
        await callback.on_chain_end(outputs='{"result": "test answer"}', run_id=parent_id)

        traces = galileo_logger.traces
        assert len(traces) == 1
        assert len(traces[0].spans) == 1
        assert len(traces[0].spans[0].spans) == 2

        retriever_span = traces[0].spans[0].spans[0]
        llm_span = traces[0].spans[0].spans[1]

        time_diff_ms = (llm_span.created_at - retriever_span.created_at).total_seconds() * 1000
        assert time_diff_ms >= delay_ms

    @pytest.mark.parametrize(
        "node_type, start_fn, end_fn, input_args, output_args, expected_type",
        [
            (
                "tool",
                "on_tool_start",
                "on_tool_end",
                {"serialized": {"name": "calculator"}, "input_str": "2+2"},
                {"output": "4"},
                "tool",
            ),
            (
                "llm",
                "on_llm_start",
                "on_llm_end",
                {"serialized": {}, "prompts": ["Tell me about AI"], "invocation_params": {"model_name": "gpt-4"}},
                {"response": MagicMock()},
                "llm",
            ),
            (
                "retriever",
                "on_retriever_start",
                "on_retriever_end",
                {"serialized": {}, "query": "AI development"},
                {"documents": [Document(page_content="AI", metadata={})]},
                "retriever",
            ),
            (
                "chain",
                "on_chain_start",
                "on_chain_end",
                {"serialized": {"name": "TestChain"}, "inputs": {"query": "test"}},
                {"outputs": {"result": "answer"}},
                "workflow",
            ),
            (
                "agent",
                "on_chain_start",
                "on_chain_end",
                {"serialized": {"name": "Agent"}, "inputs": {"query": "test"}},
                {"outputs": {"result": "answer"}},
                "workflow",
            ),
        ],
    )
    @mark.asyncio
    async def test_step_number_propagation(
        self,
        callback: GalileoAsyncCallback,
        galileo_logger: GalileoLogger,
        node_type,
        start_fn,
        end_fn,
        input_args,
        output_args,
        expected_type,
    ):
        """Test that step_number is set correctly for all node types when metadata contains langgraph_step"""
        parent_id = uuid.uuid4()
        run_id = uuid.uuid4()
        step_number = 42

        # Create parent chain for non-root nodes
        if node_type not in ("chain", "agent"):
            await callback.on_chain_start(serialized={}, inputs={"query": "test"}, run_id=parent_id)
            parent_arg = {"parent_run_id": parent_id}
        else:
            parent_arg = {}

        input_args.update({"run_id": run_id, **parent_arg, "metadata": {"langgraph_step": str(step_number)}})

        # Call start
        await getattr(callback, start_fn)(**input_args)

        # Prepare and call end
        output_args.update({"run_id": run_id, **parent_arg})
        await getattr(callback, end_fn)(**output_args)

        # End chain to trigger commit for non-root nodes
        if node_type not in ("chain", "agent"):
            await callback.on_chain_end(outputs={"result": "test answer"}, run_id=parent_id)
            traces = galileo_logger.traces
            assert len(traces) == 1
            assert len(traces[0].spans) == 1
            child_span = traces[0].spans[0].spans[0]
            assert child_span.type == expected_type
            assert child_span.step_number == step_number
        else:
            traces = galileo_logger.traces
            assert len(traces) == 1
            assert len(traces[0].spans) == 1
            root_span = traces[0].spans[0]
            assert root_span.type == expected_type
            assert root_span.step_number == step_number
