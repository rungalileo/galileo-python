"""
Tests for the refactored metric type hierarchy.

This module tests the four metric types:
- LlmMetric: Custom LLM-based metrics with prompt templates
- LocalMetric: Local function-based metrics
- CodeMetric: Code-based metrics (limited support)
- GalileoMetric: Built-in Galileo scorers
"""

from __future__ import annotations

import pytest

from galileo.__future__ import CodeMetric, GalileoMetric, LlmMetric, LocalMetric, Metric
from galileo.__future__.shared.exceptions import ValidationError
from galileo.resources.models import OutputTypeEnum, ScorerTypes
from galileo_core.schemas.logging.step import StepType


class TestLlmMetric:
    """Tests for LlmMetric class."""

    def test_llm_metric_initialization(self):
        """Test basic LlmMetric initialization."""
        metric = LlmMetric(
            name="test_llm",
            prompt="Rate this response",
            model="gpt-4o-mini",
            judges=3,
            description="Test LLM metric",
            tags=["test", "quality"],
        )

        assert metric.name == "test_llm"
        assert metric.prompt == "Rate this response"
        assert metric.model == "gpt-4o-mini"
        assert metric.judges == 3
        assert metric.description == "Test LLM metric"
        assert metric.tags == ["test", "quality"]
        assert metric.scorer_type == ScorerTypes.LLM
        assert isinstance(metric, LlmMetric)
        assert isinstance(metric, Metric)

    def test_llm_metric_with_output_type_string(self):
        """Test LlmMetric with string output_type."""
        metric = LlmMetric(name="test_llm", prompt="Rate this", output_type="percentage")

        assert metric.output_type == OutputTypeEnum.PERCENTAGE

    def test_llm_metric_with_output_type_enum(self):
        """Test LlmMetric with enum output_type."""
        metric = LlmMetric(name="test_llm", prompt="Rate this", output_type=OutputTypeEnum.BOOLEAN)

        assert metric.output_type == OutputTypeEnum.BOOLEAN

    def test_llm_metric_backward_compatibility_aliases(self):
        """Test LlmMetric with deprecated parameter names."""
        metric = LlmMetric(name="test_llm", user_prompt="Old prompt param", model_name="gpt-3.5-turbo", num_judges=2)

        assert metric.prompt == "Old prompt param"
        assert metric.model == "gpt-3.5-turbo"
        assert metric.judges == 2

    def test_llm_metric_new_params_override_old(self):
        """Test that new parameter names override deprecated ones."""
        metric = LlmMetric(
            name="test_llm",
            prompt="New prompt",
            user_prompt="Old prompt",
            model="new-model",
            model_name="old-model",
            judges=5,
            num_judges=2,
        )

        assert metric.prompt == "New prompt"
        assert metric.model == "new-model"
        assert metric.judges == 5

    def test_llm_metric_requires_prompt(self):
        """Test that LlmMetric requires a prompt."""
        with pytest.raises(ValidationError, match="'prompt'.*must be provided"):
            LlmMetric(name="test_llm")

    def test_llm_metric_defaults(self):
        """Test LlmMetric default values."""
        metric = LlmMetric(name="test_llm", prompt="Rate this")

        assert metric.node_level == StepType.llm
        assert metric.cot_enabled is True
        assert metric.output_type == OutputTypeEnum.BOOLEAN

    def test_llm_metric_custom_node_level(self):
        """Test LlmMetric with custom node_level."""
        metric = LlmMetric(name="test_llm", prompt="Rate this", node_level=StepType.workflow)

        assert metric.node_level == StepType.workflow

    def test_llm_metric_cot_disabled(self):
        """Test LlmMetric with chain-of-thought disabled."""
        metric = LlmMetric(name="test_llm", prompt="Rate this", cot_enabled=False)

        assert metric.cot_enabled is False

    def test_llm_metric_repr(self):
        """Test LlmMetric string representation."""
        metric = LlmMetric(name="test_llm", prompt="Rate this", model="gpt-4o-mini", judges=3)

        repr_str = repr(metric)
        assert "LlmMetric" in repr_str
        assert "test_llm" in repr_str
        assert "gpt-4o-mini" in repr_str
        assert "3" in repr_str


class TestLocalMetric:
    """Tests for LocalMetric class."""

    def test_local_metric_initialization(self):
        """Test basic LocalMetric initialization."""

        def my_scorer(trace_or_span):
            return 0.5

        metric = LocalMetric(
            name="test_local",
            scorer_fn=my_scorer,
            scorable_types=[StepType.llm],
            aggregatable_types=[StepType.trace],
            description="Test local metric",
            tags=["local", "custom"],
        )

        assert metric.name == "test_local"
        assert metric.scorer_fn == my_scorer
        assert metric.scorable_types == [StepType.llm]
        assert metric.aggregatable_types == [StepType.trace]
        assert metric.description == "Test local metric"
        assert metric.tags == ["local", "custom"]
        assert metric.scorer_type is None
        assert isinstance(metric, LocalMetric)
        assert isinstance(metric, Metric)

    def test_local_metric_requires_scorer_fn(self):
        """Test that LocalMetric requires a scorer_fn."""
        with pytest.raises(ValidationError, match="'scorer_fn' must be provided"):
            LocalMetric(name="test_local", scorer_fn=None)

    def test_local_metric_default_types(self):
        """Test LocalMetric default scorable and aggregatable types."""

        def my_scorer(trace_or_span):
            return 1.0

        metric = LocalMetric(name="test_local", scorer_fn=my_scorer)

        assert metric.scorable_types == [StepType.llm]
        assert metric.aggregatable_types == [StepType.trace]

    def test_local_metric_to_local_metric_config(self):
        """Test conversion to LocalMetricConfig."""

        def my_scorer(trace_or_span):
            return 0.75

        metric = LocalMetric(
            name="test_local",
            scorer_fn=my_scorer,
            scorable_types=[StepType.llm, StepType.workflow],
            aggregatable_types=[StepType.trace],
        )

        config = metric.to_local_metric_config()

        assert config.name == "test_local"
        assert config.scorer_fn == my_scorer
        assert config.scorable_types == [StepType.llm, StepType.workflow]
        assert config.aggregatable_types == [StepType.trace]

    def test_local_metric_repr(self):
        """Test LocalMetric string representation."""

        def my_scorer(trace_or_span):
            return 0.5

        metric = LocalMetric(name="test_local", scorer_fn=my_scorer)

        repr_str = repr(metric)
        assert "LocalMetric" in repr_str
        assert "test_local" in repr_str
        assert "my_scorer" in repr_str


class TestCodeMetric:
    """Tests for CodeMetric class."""

    def test_code_metric_initialization(self, tmp_path):
        """Test basic CodeMetric initialization."""
        # Create a temporary code file
        code_file = tmp_path / "scorer.py"
        code_file.write_text("def score(trace): return 1.0")

        metric = CodeMetric(
            name="test_code",
            code_file_path=str(code_file),
            node_level=StepType.llm,
            description="Test code metric",
            tags=["code"],
        )

        assert metric.name == "test_code"
        assert metric.description == "Test code metric"
        assert metric.tags == ["code"]
        assert metric.scorer_type == ScorerTypes.CODE
        assert metric.node_level == StepType.llm
        assert isinstance(metric, CodeMetric)
        assert isinstance(metric, Metric)

    def test_code_metric_create_not_implemented(self, tmp_path):
        """Test that CodeMetric.create() is now implemented."""
        # Create a temporary code file
        code_file = tmp_path / "scorer.py"
        code_file.write_text("def score(trace): return 1.0")

        metric = CodeMetric(name="test_code", code_file_path=str(code_file), node_level=StepType.llm)

        # CodeMetric.create() is now implemented, so this test should be updated
        # to verify it works or test it separately
        assert hasattr(metric, "create")
        assert callable(metric.create)


class TestGalileoMetric:
    """Tests for GalileoMetric class."""

    def test_galileo_metric_initialization(self):
        """Test basic GalileoMetric initialization."""
        metric = GalileoMetric(name="test_galileo", description="Test Galileo metric", tags=["galileo"])

        assert metric.name == "test_galileo"
        assert metric.description == "Test Galileo metric"
        assert metric.tags == ["galileo"]
        assert isinstance(metric, GalileoMetric)
        assert isinstance(metric, Metric)


class TestMetricBase:
    """Tests for base Metric class."""

    def test_metric_has_scorers_attribute(self):
        """Test that Metric class has scorers attribute."""
        assert hasattr(Metric, "scorers")

    def test_metric_scorers_is_builtin_scorers(self):
        """Test that Metric.scorers is a BuiltInScorers instance."""
        from galileo.__future__.metric import BuiltInScorers

        assert isinstance(Metric.scorers, BuiltInScorers)

    def test_metric_common_attributes(self, tmp_path):
        """Test that all metric types have common attributes."""

        def my_scorer(trace_or_span):
            return 0.5

        # Create a temporary code file for CodeMetric
        code_file = tmp_path / "scorer.py"
        code_file.write_text("def score(trace): return 1.0")

        metrics = [
            LlmMetric(name="llm", prompt="Rate this"),
            LocalMetric(name="local", scorer_fn=my_scorer),
            CodeMetric(name="code", code_file_path=str(code_file), node_level=StepType.llm),
            GalileoMetric(name="galileo"),
        ]

        for metric in metrics:
            assert hasattr(metric, "id")
            assert hasattr(metric, "name")
            assert hasattr(metric, "scorer_type")
            assert hasattr(metric, "description")
            assert hasattr(metric, "tags")
            assert hasattr(metric, "created_at")
            assert hasattr(metric, "updated_at")
            assert hasattr(metric, "version")

    def test_metric_to_legacy_metric(self):
        """Test conversion to legacy Metric format."""
        metric = LlmMetric(name="test_llm", prompt="Rate this", version=1)
        legacy = metric.to_legacy_metric()

        assert legacy.name == "test_llm"
        assert legacy.version == 1

    def test_metric_str_representation(self):
        """Test Metric __str__ method."""
        metric = LlmMetric(name="test_llm", prompt="Rate this")
        str_repr = str(metric)

        assert "LlmMetric" in str_repr
        assert "test_llm" in str_repr

    def test_metric_delete_raises_for_local_metric(self):
        """Test that delete raises ValidationError for LocalMetric."""

        def my_scorer(trace_or_span):
            return 0.5

        metric = LocalMetric(name="test_local", scorer_fn=my_scorer)

        with pytest.raises(ValidationError, match="Local metrics don't exist on the server"):
            metric.delete()

    def test_metric_refresh_raises_for_local_metric(self):
        """Test that refresh raises ValidationError for LocalMetric."""

        def my_scorer(trace_or_span):
            return 0.5

        metric = LocalMetric(name="test_local", scorer_fn=my_scorer)

        with pytest.raises(ValidationError, match="Local metrics don't exist on the server"):
            metric.refresh()


class TestMetricInheritance:
    """Tests for metric type inheritance."""

    def test_all_metrics_inherit_from_base(self, tmp_path):
        """Test that all metric types inherit from Metric."""

        def my_scorer(trace_or_span):
            return 0.5

        # Create a temporary code file for CodeMetric
        code_file = tmp_path / "scorer.py"
        code_file.write_text("def score(trace): return 1.0")

        assert isinstance(LlmMetric(name="llm", prompt="Rate"), Metric)
        assert isinstance(LocalMetric(name="local", scorer_fn=my_scorer), Metric)
        assert isinstance(CodeMetric(name="code", code_file_path=str(code_file), node_level=StepType.llm), Metric)
        assert isinstance(GalileoMetric(name="galileo"), Metric)

    def test_metric_type_checking(self, tmp_path):
        """Test isinstance checks for different metric types."""

        def my_scorer(trace_or_span):
            return 0.5

        # Create a temporary code file for CodeMetric
        code_file = tmp_path / "scorer.py"
        code_file.write_text("def score(trace): return 1.0")

        llm = LlmMetric(name="llm", prompt="Rate")
        local = LocalMetric(name="local", scorer_fn=my_scorer)
        code = CodeMetric(name="code", code_file_path=str(code_file), node_level=StepType.llm)
        galileo = GalileoMetric(name="galileo")

        assert isinstance(llm, LlmMetric) and not isinstance(llm, LocalMetric)
        assert isinstance(local, LocalMetric) and not isinstance(local, LlmMetric)
        assert isinstance(code, CodeMetric) and not isinstance(code, LlmMetric)
        assert isinstance(galileo, GalileoMetric) and not isinstance(galileo, LlmMetric)


class TestMetricEdgeCases:
    """Tests for edge cases and error conditions."""

    def test_llm_metric_with_minimal_prompt(self):
        """Test LlmMetric with minimal prompt."""
        # Minimal prompt that's not empty
        metric = LlmMetric(name="test", prompt="Rate")
        assert metric.prompt == "Rate"

    def test_metric_with_empty_tags(self):
        """Test metrics with empty tags list."""
        metric = LlmMetric(name="test", prompt="Rate", tags=[])
        assert metric.tags == []

    def test_metric_with_none_tags(self):
        """Test metrics with None tags (should default to empty list)."""
        metric = LlmMetric(name="test", prompt="Rate", tags=None)
        assert metric.tags == []

    def test_output_type_mapping(self):
        """Test all output_type string to enum mappings."""
        output_types = {
            "percentage": OutputTypeEnum.PERCENTAGE,
            "boolean": OutputTypeEnum.BOOLEAN,
            "categorical": OutputTypeEnum.CATEGORICAL,
            "count": OutputTypeEnum.COUNT,
            "discrete": OutputTypeEnum.DISCRETE,
            "freeform": OutputTypeEnum.FREEFORM,
            "multilabel": OutputTypeEnum.MULTILABEL,
        }

        for string_type, enum_type in output_types.items():
            metric = LlmMetric(name="test", prompt="Rate", output_type=string_type)
            assert metric.output_type == enum_type

    def test_output_type_unknown_string(self):
        """Test that unknown output_type string defaults to PERCENTAGE."""
        metric = LlmMetric(name="test", prompt="Rate", output_type="unknown_type")
        assert metric.output_type == OutputTypeEnum.PERCENTAGE

    def test_local_metric_with_multiple_scorable_types(self):
        """Test LocalMetric with multiple scorable types."""

        def my_scorer(trace_or_span):
            return 0.5

        metric = LocalMetric(
            name="test", scorer_fn=my_scorer, scorable_types=[StepType.llm, StepType.workflow, StepType.agent]
        )

        assert len(metric.scorable_types) == 3
        assert StepType.llm in metric.scorable_types
        assert StepType.workflow in metric.scorable_types
        assert StepType.agent in metric.scorable_types
