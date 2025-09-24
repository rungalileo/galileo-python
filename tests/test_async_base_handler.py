import uuid
from collections.abc import Generator
from unittest.mock import Mock, patch

import pytest

from galileo.handlers.base_async_handler import GalileoAsyncBaseHandler
from galileo.logger.logger import GalileoLogger
from tests.testutils.setup import setup_mock_logstreams_client, setup_mock_projects_client, setup_mock_traces_client


class TestGalileoAsyncBaseHandlerCallback:
    @pytest.fixture
    @patch("galileo.logger.logger.LogStreams")
    @patch("galileo.logger.logger.Projects")
    @patch("galileo.logger.logger.Traces")
    def galileo_logger(self, mock_traces_client: Mock, mock_projects_client: Mock, mock_logstreams_client: Mock):
        """Creates a mock Galileo logger for testing"""
        setup_mock_traces_client(mock_traces_client)
        setup_mock_projects_client(mock_projects_client)
        setup_mock_logstreams_client(mock_logstreams_client)
        return GalileoLogger(project="my_project", log_stream="my_log_stream")

    @pytest.fixture
    def handler(self, galileo_logger: GalileoLogger) -> Generator[GalileoAsyncBaseHandler, None, None]:
        """Creates a GalileoCallback with a mock logger"""
        handler = GalileoAsyncBaseHandler(galileo_logger=galileo_logger, flush_on_chain_end=False)
        # Reset the root node before each test
        handler._root_node = None
        yield handler
        # Clean up after each test
        handler._root_node = None

    @pytest.mark.asyncio
    async def test_initialization(self, galileo_logger: GalileoLogger) -> None:
        """Test callback initialization with various parameters"""
        # Default initialization
        callback = GalileoAsyncBaseHandler(galileo_logger=galileo_logger)
        assert callback._galileo_logger == galileo_logger
        assert callback._start_new_trace is True
        assert callback._flush_on_chain_end is True
        assert callback._nodes == {}

        # Custom initialization
        callback = GalileoAsyncBaseHandler(
            galileo_logger=galileo_logger, start_new_trace=False, flush_on_chain_end=False
        )
        assert callback._start_new_trace is False
        assert callback._flush_on_chain_end is False

    @pytest.mark.asyncio
    async def test_start_node(self, handler: GalileoAsyncBaseHandler) -> None:
        """Test creating a node and establishing parent-child relationships"""
        # Create a parent node
        parent_id = uuid.uuid4()
        node = await handler.async_start_node(
            node_type="chain", parent_run_id=None, run_id=parent_id, name="Parent Chain", input={"query": "test"}
        )

        assert node.node_type == "chain"
        assert node.run_id == parent_id
        assert node.parent_run_id is None
        assert "name" in node.span_params
        assert node.span_params["name"] == "Parent Chain"
        assert node.span_params["start_time"] > 0
        assert str(parent_id) in handler._nodes

        # Create a child node
        child_id = uuid.uuid4()
        child_node = await handler.async_start_node(
            node_type="llm", parent_run_id=parent_id, run_id=child_id, name="Child LLM", input="test prompt"
        )

        assert child_node.node_type == "llm"
        assert child_node.parent_run_id == parent_id
        assert str(child_id) in handler._nodes

        # Verify parent-child relationship was established
        assert str(child_id) in handler._nodes[str(parent_id)].children

        # Verify root node was set properly
        assert handler._root_node
        assert handler._root_node.run_id == parent_id

    @pytest.mark.asyncio
    async def test_end_node(self, handler: GalileoAsyncBaseHandler, galileo_logger: GalileoLogger) -> None:
        """Test ending a node and updating its parameters"""
        # Create a node
        run_id = uuid.uuid4()
        await handler.async_start_node(
            node_type="chain", parent_run_id=None, run_id=run_id, name="Test Chain", input='{"query": "test"}'
        )

        # End the node and commit the trace
        await handler.async_end_node(run_id, output='{"result": "test result"}')

        traces = galileo_logger.traces
        assert len(traces) == 1
        assert len(traces[0].spans) == 1
        assert traces[0].spans[0].name == "Test Chain"
        assert traces[0].spans[0].type == "workflow"
        assert traces[0].spans[0].input == '{"query": "test"}'
        assert traces[0].spans[0].output == '{"result": "test result"}'
