"""Tests for OpenAI Agents utility functions."""

from __future__ import annotations

from typing import Any
from unittest.mock import Mock

import pytest
from agents import (
    AgentSpanData,
    CustomSpanData,
    FunctionSpanData,
    GenerationSpanData,
    GuardrailSpanData,
    HandoffSpanData,
    Span,
)
from agents.tracing import ResponseSpanData

from galileo.utils.openai_agents import (
    GalileoCustomSpan,
    _extract_llm_data,
    _extract_tool_data,
    _extract_workflow_data,
    _map_span_name,
    _map_span_type,
    _parse_usage,
)
from galileo_core.schemas.logging.span import ToolSpan, WorkflowSpan


class TestParseUsage:
    """Test _parse_usage function."""

    @pytest.mark.parametrize(
        "usage_data,expected",
        [
            (
                {"input_tokens": 10, "output_tokens": 20, "total_tokens": 30},
                {"input_tokens": 10, "output_tokens": 20, "total_tokens": 30},
            ),
            (
                {"prompt_tokens": 15, "completion_tokens": 25, "total_tokens": 40},
                {"input_tokens": 15, "output_tokens": 25, "total_tokens": 40},
            ),
            (
                {
                    "input_tokens": 10,
                    "prompt_tokens": 999,
                    "output_tokens": 20,
                    "completion_tokens": 888,
                    "total_tokens": 30,
                },
                {"input_tokens": 10, "output_tokens": 20, "total_tokens": 30},
            ),
            ({"input_tokens": 10, "output_tokens": 20}, {"input_tokens": 10, "output_tokens": 20, "total_tokens": 30}),
            (None, {"input_tokens": None, "output_tokens": None, "total_tokens": None}),
            ({"input_tokens": 10}, {"input_tokens": 10, "output_tokens": None, "total_tokens": None}),
        ],
    )
    def test_parse_usage_variations(self, usage_data: dict[str, Any] | None, expected: dict[str, int | None]) -> None:
        """Test various usage data formats."""
        result = _parse_usage(usage_data)
        assert result == expected

    def test_parse_usage_with_model_dump(self) -> None:
        """Test parsing from object with model_dump."""
        mock_usage = Mock()
        mock_usage.model_dump.return_value = {"input_tokens": 5, "output_tokens": 10, "total_tokens": 15}
        result = _parse_usage(mock_usage)
        assert result == {"input_tokens": 5, "output_tokens": 10, "total_tokens": 15}

    def test_parse_usage_with_invalid_values(self) -> None:
        """Test parsing with invalid token values."""
        result = _parse_usage({"input_tokens": "invalid", "output_tokens": 20})
        assert result["output_tokens"] == 20
        assert result["input_tokens"] is None


class TestExtractLlmData:
    """Test _extract_llm_data function."""

    def test_generation_span(self) -> None:
        """Test extracting from GenerationSpanData."""
        span_data = Mock(spec=GenerationSpanData)
        span_data.input = "What is AI?"
        span_data.output = "Artificial Intelligence"
        span_data.model = "gpt-4"
        span_data.usage = {"input_tokens": 5, "output_tokens": 10, "total_tokens": 15}
        span_data.model_config = {"temperature": 0.7}

        result = _extract_llm_data(span_data)

        assert result["model"] == "gpt-4"
        assert result["temperature"] == 0.7
        assert result["num_input_tokens"] == 5
        assert result["num_output_tokens"] == 10
        assert result["status_code"] == 200

    def test_response_span_with_tools(self) -> None:
        """Test extracting from ResponseSpanData with tools."""
        mock_response = Mock()
        mock_response.output = "Response"
        mock_response.model = "gpt-4"
        mock_response.temperature = 0.7
        mock_response.usage = None
        mock_response.tools = [
            Mock(model_dump=Mock(return_value={"name": "search"})),
            Mock(model_dump=Mock(return_value={"name": "calc"})),
        ]
        mock_response.error = None
        mock_response.model_dump.return_value = {"model": "gpt-4", "temperature": 0.7}

        result = _extract_llm_data(ResponseSpanData(input="Query", response=mock_response))

        assert len(result["tools"]) == 2

    def test_response_span_with_error(self) -> None:
        """Test extracting from ResponseSpanData with error."""
        mock_response = Mock()
        mock_response.output = None
        mock_response.model = "gpt-4"
        mock_response.temperature = None
        mock_response.usage = None
        mock_response.tools = None
        mock_response.error = Mock(status_code=503)
        mock_response.model_dump.return_value = {"model": "gpt-4"}

        result = _extract_llm_data(ResponseSpanData(input="Query", response=mock_response))

        assert result["status_code"] == 503
        assert "error_details" in result["metadata"]

    def test_serializes_complex_output(self) -> None:
        """Test that complex output is serialized."""
        span_data = GenerationSpanData(input=[{"text": "Question"}], output=[{"text": "Answer"}], model="gpt-4")
        result = _extract_llm_data(span_data)
        assert isinstance(result["input"], str)
        assert isinstance(result["output"], str)


class TestExtractToolData:
    """Test _extract_tool_data function."""

    def test_function_span(self) -> None:
        """Test extracting from FunctionSpanData."""
        result = _extract_tool_data(FunctionSpanData(name="search", input="input data", output=[{"result": "output"}]))
        assert "input" in result and "output" in result
        assert result["status_code"] == 200

    @pytest.mark.parametrize("triggered,has_warning", [(True, True), (False, False)])
    def test_guardrail_span(self, triggered: bool, has_warning: bool) -> None:
        """Test extracting from GuardrailSpanData."""
        result = _extract_tool_data(GuardrailSpanData(name="guardrail", triggered=triggered))
        assert result["metadata"]["triggered"] is triggered
        assert ("status" in result["metadata"]) == has_warning


class TestExtractWorkflowData:
    """Test _extract_workflow_data function."""

    def test_agent_span(self) -> None:
        """Test extracting from AgentSpanData."""
        result = _extract_workflow_data(
            AgentSpanData(name="Agent", tools=["tool1"], handoffs=["agent1"], output_type="text")
        )
        assert result["metadata"]["tools"] == ["tool1"]
        assert result["metadata"]["handoffs"] == ["agent1"]

    def test_handoff_span(self) -> None:
        """Test extracting from HandoffSpanData."""
        result = _extract_workflow_data(HandoffSpanData(from_agent="agent1", to_agent="agent2"))
        assert result["metadata"]["from_agent"] == "agent1"
        assert result["metadata"]["to_agent"] == "agent2"

    def test_custom_span_filters_none(self) -> None:
        """Test CustomSpanData filters None values from metadata."""
        result = _extract_workflow_data(
            CustomSpanData(name="Test", data={"input": "in", "output": "out", "field1": "val", "field2": None})
        )
        assert "field1" in result["metadata"]
        assert "field2" not in result["metadata"]


class TestMapSpanName:
    """Test _map_span_name function."""

    def test_uses_name_attribute(self) -> None:
        """Test mapping span name from name attribute."""
        mock_span = Mock(spec=Span)
        mock_span_data = Mock()
        mock_span_data.name = "Custom Name"
        mock_span.span_data = mock_span_data
        assert _map_span_name(mock_span) == "Custom Name"

    @pytest.mark.parametrize(
        "span_data,expected_name",
        [
            (GenerationSpanData(input=[{"text": "test"}], output=[{"text": "response"}], model="gpt-4"), "Generation"),
            (ResponseSpanData(input="test", response=Mock(output="response")), "Response"),
            (HandoffSpanData(from_agent="Agent1", to_agent="Agent2"), "Handoff: Agent1 -> Agent2"),
        ],
    )
    def test_span_type_names(self, span_data: Any, expected_name: str) -> None:
        """Test mapping names for different span types."""
        mock_span = Mock(spec=Span)
        mock_span.span_data = span_data
        assert _map_span_name(mock_span) == expected_name

    def test_falls_back_to_type(self) -> None:
        """Test fallback to type attribute."""
        mock_span = Mock(spec=Span)
        mock_span_data = Mock()
        mock_span_data.name = None
        mock_span_data.type = "custom_type"
        mock_span.span_data = mock_span_data
        assert _map_span_name(mock_span) == "Custom_type"

    def test_unknown_span(self) -> None:
        """Test handling of unknown span types."""
        mock_span = Mock(spec=Span)
        mock_span.span_data = Mock(spec=[])
        assert _map_span_name(mock_span) == "Unknown Span"


class TestMapSpanType:
    """Test _map_span_type function."""

    @pytest.mark.parametrize(
        "span_data,expected_type",
        [
            # LLM spans
            (GenerationSpanData(input=[{"text": "test"}], output=[{"text": "response"}], model="gpt-4"), "llm"),
            (ResponseSpanData(input="test", response=Mock()), "llm"),
            # Tool spans
            (FunctionSpanData(name="function", input="input", output=[{"result": "output"}]), "tool"),
            (GuardrailSpanData(name="guardrail", triggered=False), "tool"),
            # Workflow spans
            (AgentSpanData(name="Agent", tools=[], handoffs=[]), "workflow"),
            (HandoffSpanData(from_agent="A", to_agent="B"), "workflow"),
            (CustomSpanData(name="Custom", data={}), "workflow"),
        ],
    )
    def test_span_data_types(self, span_data: Any, expected_type: str) -> None:
        """Test mapping various span data types."""
        assert _map_span_type(span_data) == expected_type

    def test_galileo_custom_span(self) -> None:
        """Test mapping GalileoCustomSpan."""
        galileo_span = WorkflowSpan(name="Test", input="input", output="output", status_code=200)
        assert _map_span_type(GalileoCustomSpan(galileo_span, {})) == "galileo_custom"

    @pytest.mark.parametrize(
        "type_attr,expected_type", [("function", "tool"), ("generation", "llm"), ("agent", "workflow")]
    )
    def test_type_attribute_mapping(self, type_attr: str, expected_type: str) -> None:
        """Test mapping based on type attribute."""
        assert _map_span_type(Mock(type=type_attr)) == expected_type

    def test_unknown_defaults_to_workflow(self) -> None:
        """Test unknown span types default to workflow."""
        assert _map_span_type(Mock(spec=[])) == "workflow"


class TestGalileoCustomSpan:
    """Test GalileoCustomSpan utility."""

    @pytest.mark.parametrize(
        "span",
        [
            ToolSpan(name="Tool", input="i", output="o", status_code=200),
            WorkflowSpan(name="Workflow", input="start", output="end", status_code=200),
        ],
    )
    def test_wraps_span_types(self, span: Any) -> None:
        """Test that GalileoCustomSpan wraps different span types."""
        assert GalileoCustomSpan(span, {}).type == "galileo_custom"

    def test_preserves_underlying_properties(self) -> None:
        """Test accessing underlying span properties."""
        workflow_span = WorkflowSpan(
            name="Test", input="Q", output="A", user_metadata={"v": "1.0"}, tags=["test"], status_code=200
        )
        custom_span = GalileoCustomSpan(workflow_span, workflow_span.user_metadata or {})

        assert custom_span.span.name == "Test"
        assert custom_span.span.input == "Q"
        assert custom_span.span.output == "A"
        assert custom_span.span.tags == ["test"]
        assert custom_span.data == {"v": "1.0"}

    def test_handles_none_user_metadata(self) -> None:
        """Test that None user_metadata is handled correctly."""
        workflow_span = WorkflowSpan(
            name="Test",
            input="Q",
            output="A",
            user_metadata=None,  # pyright: ignore[reportArgumentType]
            tags=["test"],
            status_code=200,
        )
        # WorkflowSpan converts None to {} automatically, but we test the 'or {}' pattern
        custom_span = GalileoCustomSpan(workflow_span, workflow_span.user_metadata or {})

        assert custom_span.span.name == "Test"
        # WorkflowSpan normalizes None to {} internally
        assert custom_span.span.user_metadata == {}
        assert custom_span.data == {}

        # Verify that unpacking with 'or {}' pattern works (which is what our fix uses)
        metadata = custom_span.span.user_metadata or {}
        result = {**metadata, "status_code": custom_span.span.status_code}
        assert result == {"status_code": 200}
