"""
Tests for explicit parent_id functionality in GalileoLogger.

This test suite verifies that spans can be added using explicit parent_id
instead of the stack-based approach.
"""

import pytest
from unittest.mock import Mock, patch
from uuid import uuid4

from galileo.logger import GalileoLogger
from galileo_core.schemas.logging.span import LlmSpan, WorkflowSpan, AgentSpan
from galileo_core.schemas.shared.document import Document
from tests.testutils.setup import setup_mock_projects_client, setup_mock_logstreams_client, setup_mock_traces_client


@patch("galileo.logger.logger.LogStreams")
@patch("galileo.logger.logger.Projects")
@patch("galileo.logger.logger.Traces")
def test_add_llm_span_with_explicit_parent_id(
    mock_traces_client: Mock, mock_projects_client: Mock, mock_logstreams_client: Mock
) -> None:
    """Test adding LLM span using explicit parent_id."""
    setup_mock_traces_client(mock_traces_client)
    setup_mock_projects_client(mock_projects_client)
    setup_mock_logstreams_client(mock_logstreams_client)

    logger = GalileoLogger(project="my_project", log_stream="my_log_stream")

    # Create trace
    trace = logger.start_trace(input="test input")

    # Add LLM span directly to trace using parent_id
    llm_span = logger.add_llm_span(
        input="llm input",
        output="llm output",
        model="gpt-4",
        parent_id=trace.id,
    )

    # Verify span was added to trace
    assert len(trace.spans) == 1
    assert trace.spans[0] == llm_span
    assert llm_span.parent_id == trace.id

    # Verify dataset fields were inherited
    assert llm_span.dataset_input == trace.dataset_input
    assert llm_span.dataset_output == trace.dataset_output
    assert llm_span.dataset_metadata == trace.dataset_metadata


@patch("galileo.logger.logger.LogStreams")
@patch("galileo.logger.logger.Projects")
@patch("galileo.logger.logger.Traces")
def test_add_workflow_span_with_explicit_parent_id(
    mock_traces_client: Mock, mock_projects_client: Mock, mock_logstreams_client: Mock
) -> None:
    """Test adding workflow span using explicit parent_id doesn't affect stack."""
    setup_mock_traces_client(mock_traces_client)
    setup_mock_projects_client(mock_projects_client)
    setup_mock_logstreams_client(mock_logstreams_client)

    logger = GalileoLogger(project="my_project", log_stream="my_log_stream")

    # Create trace
    trace = logger.start_trace(input="test input")

    # Add workflow span using parent_id (should NOT push to stack)
    workflow_span = logger.add_workflow_span(
        input="workflow input",
        parent_id=trace.id,
    )

    # Verify span was added to trace
    assert len(trace.spans) == 1
    assert trace.spans[0] == workflow_span
    assert workflow_span.parent_id == trace.id

    # Verify it was NOT added to stack (current parent should still be trace)
    assert logger.current_parent() == trace


@patch("galileo.logger.logger.LogStreams")
@patch("galileo.logger.logger.Projects")
@patch("galileo.logger.logger.Traces")
def test_nested_spans_with_explicit_parent_id(
    mock_traces_client: Mock, mock_projects_client: Mock, mock_logstreams_client: Mock
) -> None:
    """Test creating nested spans using explicit parent_id."""
    setup_mock_traces_client(mock_traces_client)
    setup_mock_projects_client(mock_projects_client)
    setup_mock_logstreams_client(mock_logstreams_client)

    logger = GalileoLogger(project="my_project", log_stream="my_log_stream")

    # Create trace
    trace = logger.start_trace(input="test input")

    # Add workflow span to trace
    workflow = logger.add_workflow_span(
        input="workflow input",
        parent_id=trace.id,
    )

    # Add LLM span to workflow span
    llm_span = logger.add_llm_span(
        input="llm input",
        output="llm output",
        model="gpt-4",
        parent_id=workflow.id,
    )

    # Verify hierarchy
    assert len(trace.spans) == 1
    assert trace.spans[0] == workflow
    assert len(workflow.spans) == 1
    assert workflow.spans[0] == llm_span
    assert llm_span.parent_id == workflow.id


@patch("galileo.logger.logger.LogStreams")
@patch("galileo.logger.logger.Projects")
@patch("galileo.logger.logger.Traces")
def test_mixing_explicit_and_stack_modes(
    mock_traces_client: Mock, mock_projects_client: Mock, mock_logstreams_client: Mock
) -> None:
    """Test that explicit and stack modes can be used together."""
    setup_mock_traces_client(mock_traces_client)
    setup_mock_projects_client(mock_projects_client)
    setup_mock_logstreams_client(mock_logstreams_client)

    logger = GalileoLogger(project="my_project", log_stream="my_log_stream")

    # Create trace using stack mode
    trace = logger.start_trace(input="test input")

    # Add workflow using stack mode (pushes to stack)
    workflow1 = logger.add_workflow_span(input="workflow1 input")

    # Current parent should be workflow1
    assert logger.current_parent() == workflow1

    # Add LLM span using stack mode (uses workflow1 as parent)
    llm1 = logger.add_llm_span(
        input="llm1 input",
        output="llm1 output",
        model="gpt-4",
    )

    # Add another workflow using explicit parent_id pointing to trace
    # This should NOT affect the stack
    workflow2 = logger.add_workflow_span(
        input="workflow2 input",
        parent_id=trace.id,
    )

    # Current parent should still be workflow1 (not workflow2)
    assert logger.current_parent() == workflow1

    # Add LLM span to workflow2 using explicit parent_id
    llm2 = logger.add_llm_span(
        input="llm2 input",
        output="llm2 output",
        model="gpt-4",
        parent_id=workflow2.id,
    )

    # Verify hierarchy
    assert len(trace.spans) == 2  # workflow1 and workflow2
    assert workflow1 in trace.spans
    assert workflow2 in trace.spans
    assert len(workflow1.spans) == 1
    assert workflow1.spans[0] == llm1
    assert len(workflow2.spans) == 1
    assert workflow2.spans[0] == llm2

    # Verify parent_id is set
    assert llm2.parent_id == workflow2.id


@patch("galileo.logger.logger.LogStreams")
@patch("galileo.logger.logger.Projects")
@patch("galileo.logger.logger.Traces")
def test_all_span_types_with_explicit_parent_id(
    mock_traces_client: Mock, mock_projects_client: Mock, mock_logstreams_client: Mock
) -> None:
    """Test that all span types support explicit parent_id."""
    setup_mock_traces_client(mock_traces_client)
    setup_mock_projects_client(mock_projects_client)
    setup_mock_logstreams_client(mock_logstreams_client)

    logger = GalileoLogger(project="my_project", log_stream="my_log_stream")

    trace = logger.start_trace(input="test input")

    # Test all span types
    llm = logger.add_llm_span(
        input="i", output="o", model="m", parent_id=trace.id
    )
    retriever = logger.add_retriever_span(
        input="i", output=[Document(content="c")], parent_id=trace.id
    )
    tool = logger.add_tool_span(
        input="i", output="o", parent_id=trace.id
    )
    workflow = logger.add_workflow_span(
        input="i", parent_id=trace.id
    )
    agent = logger.add_agent_span(
        input="i", parent_id=trace.id
    )

    # All should be direct children of trace
    assert len(trace.spans) == 5
    assert llm in trace.spans
    assert retriever in trace.spans
    assert tool in trace.spans
    assert workflow in trace.spans
    assert agent in trace.spans
