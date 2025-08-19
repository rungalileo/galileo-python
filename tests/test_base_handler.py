import uuid
from collections.abc import Generator
from unittest.mock import Mock, patch

import pytest

from galileo.handlers.base_handler import GalileoBaseHandler
from galileo.logger.logger import GalileoLogger
from tests.testutils.setup import setup_mock_logstreams_client, setup_mock_projects_client, setup_mock_traces_client


class TestGalileoBaseHandler:
    @pytest.fixture
    @patch("galileo.logger.logger.LogStreams")
    @patch("galileo.logger.logger.Projects")
    @patch("galileo.logger.logger.Traces")
    def galileo_logger(self, mock_traces_client: Mock, mock_projects_client: Mock, mock_logstreams_client: Mock):
        """Creates a mock Galileo logger for testing"""
        setup_mock_traces_client(mock_traces_client)
        setup_mock_projects_client(mock_projects_client)
        setup_mock_logstreams_client(mock_logstreams_client)
        logger = GalileoLogger(project="my_project", log_stream="my_log_stream")
        return logger

    @pytest.fixture
    def handler(self, galileo_logger: GalileoLogger) -> Generator[GalileoBaseHandler, None, None]:
        """Creates a GalileoBaseHandler with a mock logger"""
        callback = GalileoBaseHandler(galileo_logger=galileo_logger, flush_on_chain_end=False)
        # Reset the root node before each test
        yield callback
        # Clean up after each test

    def test_initialization(self, galileo_logger: GalileoLogger):
        """Test callback initialization with various parameters"""
        # Default initialization
        handler = GalileoBaseHandler(galileo_logger=galileo_logger)
        assert handler._galileo_logger == galileo_logger
        assert handler._start_new_trace is True
        assert handler._flush_on_chain_end is True
        assert handler._nodes == {}

        # Custom initialization
        handler = GalileoBaseHandler(galileo_logger=galileo_logger, start_new_trace=False, flush_on_chain_end=False)
        assert handler._start_new_trace is False
        assert handler._flush_on_chain_end is False

    def test_start_node(self, handler: GalileoBaseHandler):
        """Test creating a node and establishing parent-child relationships"""
        # Create a parent node
        parent_id = uuid.uuid4()
        node = handler.start_node(
            node_type="chain", parent_run_id=None, run_id=parent_id, name="Parent Chain", input={"query": "test"}
        )

        assert node.node_type == "chain"
        assert node.run_id == parent_id
        assert node.parent_run_id is None
        assert "name" in node.span_params
        assert node.span_params["name"] == "Parent Chain"
        assert str(parent_id) in handler._nodes
        assert "start_time" in node.span_params

        # Create a child node
        child_id = uuid.uuid4()
        child_node = handler.start_node(
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

    def test_end_node(self, handler: GalileoBaseHandler, galileo_logger: GalileoLogger):
        """Test ending a node and updating its parameters"""
        # Create a node
        run_id = uuid.uuid4()
        handler.start_node(
            node_type="chain", parent_run_id=None, run_id=run_id, name="Test Chain", input='{"query": "test"}'
        )

        # End the node and commit the trace
        handler.end_node(run_id, output='{"result": "test result"}')

        traces = galileo_logger.traces
        assert len(traces) == 1
        assert len(traces[0].spans) == 1
        assert traces[0].spans[0].name == "Test Chain"
        assert traces[0].spans[0].type == "workflow"
        assert traces[0].spans[0].input == '{"query": "test"}'
        assert traces[0].spans[0].output == '{"result": "test result"}'
