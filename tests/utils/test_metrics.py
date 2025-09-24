import datetime

import pytest

from galileo.schema.metrics import LocalMetricConfig
from galileo.utils.metrics import _populate_local_metric, populate_local_metrics
from galileo_core.schemas.logging.span import LlmSpan, WorkflowSpan
from galileo_core.schemas.logging.step import StepType
from galileo_core.schemas.logging.trace import Trace


# Define simple scorer and aggregator functions for testing
def simple_scorer(step) -> float:
    return 1.0


def simple_aggregator(scores) -> float:
    return sum(scores)


def dict_aggregator(scores) -> dict:
    return {"_mean": sum(scores) / len(scores) if scores else 0, "_sum": sum(scores)}


@pytest.fixture
def simple_metric_config():
    return LocalMetricConfig(name="test_metric", scorer_fn=simple_scorer, scorable_types=[StepType.llm])


@pytest.fixture
def aggregating_metric_config():
    return LocalMetricConfig(
        name="test_metric",
        scorer_fn=simple_scorer,
        aggregator_fn=simple_aggregator,
        scorable_types=[StepType.llm],
        aggregatable_types=[StepType.trace],
    )


@pytest.fixture
def dict_aggregating_metric_config():
    return LocalMetricConfig(
        name="test_metric",
        scorer_fn=simple_scorer,
        aggregator_fn=dict_aggregator,
        scorable_types=[StepType.llm],
        aggregatable_types=[StepType.trace],
    )


@pytest.fixture
def llm_span():
    # Use a string for input and output to avoid validation issues
    return LlmSpan(
        input="test input",
        output="test output",
        name="test-span",
        created_at=datetime.datetime.now(),
        duration_ns=1_000_000,
        status_code=200,
    )


@pytest.fixture
def workflow_span():
    return WorkflowSpan(
        input="test input", name="test-span", created_at=datetime.datetime.now(), duration_ns=1_000_000, status_code=200
    )


@pytest.fixture
def trace_with_spans(llm_span):
    trace = Trace(
        input="test input",
        name="test-trace",
        created_at=datetime.datetime.now(),
        duration_ns=1_000_000,
        status_code=200,
    )
    trace.spans = [llm_span]
    return trace


@pytest.fixture
def nested_trace():
    nested_span = LlmSpan(
        input="test input",
        output="test output",
        name="test-span",
        created_at=datetime.datetime.now(),
        duration_ns=1_000_000,
        status_code=200,
    )
    middle_span = WorkflowSpan(
        input="test input", name="test-span", created_at=datetime.datetime.now(), duration_ns=1_000_000, status_code=200
    )
    middle_span.spans = [nested_span]
    trace = Trace(
        input="test input",
        name="test-trace",
        created_at=datetime.datetime.now(),
        duration_ns=1_000_000,
        status_code=200,
    )
    trace.spans = [middle_span]
    return trace


class TestPopulateLocalMetrics:
    def test_populate_local_metrics_no_metrics(self, trace_with_spans) -> None:
        # Test with empty metrics list
        populate_local_metrics(trace_with_spans, [])
        # No assertions needed, just verifying it doesn't raise exceptions

    def test_populate_local_metrics_with_metrics(self, trace_with_spans, simple_metric_config) -> None:
        # Test with a single metric
        populate_local_metrics(trace_with_spans, [simple_metric_config])

        # Verify metrics were set on the span
        assert hasattr(trace_with_spans.spans[0].metrics, "test_metric")
        assert trace_with_spans.spans[0].metrics.test_metric == 1.0

    def test_populate_local_metrics_with_multiple_metrics(self, trace_with_spans) -> None:
        # Test with multiple metrics
        local_metrics = [
            LocalMetricConfig(name="metric1", scorer_fn=simple_scorer, scorable_types=[StepType.llm]),
            LocalMetricConfig(name="metric2", scorer_fn=simple_scorer, scorable_types=[StepType.llm]),
        ]

        populate_local_metrics(trace_with_spans, local_metrics)

        # Verify both metrics were set on the span
        assert hasattr(trace_with_spans.spans[0].metrics, "metric1")
        assert hasattr(trace_with_spans.spans[0].metrics, "metric2")
        assert trace_with_spans.spans[0].metrics.metric1 == 1.0
        assert trace_with_spans.spans[0].metrics.metric2 == 1.0


class TestPopulateLocalMetric:
    def test_populate_local_metric_scorable_type(self, llm_span, simple_metric_config) -> None:
        # Test with a span that has a scorable type
        scores = []
        _populate_local_metric(llm_span, simple_metric_config, scores)

        # Verify the metric was set on the span
        assert hasattr(llm_span.metrics, "test_metric")
        assert llm_span.metrics.test_metric == 1.0
        assert scores == [1.0]

    def test_populate_local_metric_non_scorable_type(self, workflow_span, simple_metric_config) -> None:
        # Test with a span that doesn't have a scorable type
        scores = []
        _populate_local_metric(workflow_span, simple_metric_config, scores)

        # Verify the metric was not set on the span
        assert not hasattr(workflow_span.metrics, "test_metric")
        assert not scores  # Scores list should still be empty

    def test_populate_local_metric_with_child_spans(self, trace_with_spans, simple_metric_config) -> None:
        # Test with a trace that has child spans
        scores = []
        _populate_local_metric(trace_with_spans, simple_metric_config, scores)

        # Verify metrics were set on child spans but not on the trace
        assert hasattr(trace_with_spans.spans[0].metrics, "test_metric")
        assert not hasattr(trace_with_spans.metrics, "test_metric")
        assert len(scores) == 1
        assert scores == [1.0]

    def test_populate_local_metric_with_aggregation(self, trace_with_spans, aggregating_metric_config) -> None:
        # Test with a trace that has child spans and an aggregator function
        scores = []
        _populate_local_metric(trace_with_spans, aggregating_metric_config, scores)

        # Verify metrics were set on child spans and aggregated on the trace
        assert hasattr(trace_with_spans.spans[0].metrics, "test_metric")
        assert hasattr(trace_with_spans.metrics, "test_metric")
        assert trace_with_spans.metrics.test_metric == 1.0  # Sum of one score
        assert len(scores) == 1

    def test_populate_local_metric_with_dict_aggregation(
        self, trace_with_spans, dict_aggregating_metric_config
    ) -> None:
        # Test with a trace that has child spans and an aggregator function that returns a dict
        scores = []
        _populate_local_metric(trace_with_spans, dict_aggregating_metric_config, scores)

        # Verify metrics were set on child spans and aggregated metrics were set on the trace
        assert hasattr(trace_with_spans.spans[0].metrics, "test_metric")
        assert hasattr(trace_with_spans.metrics, "test_metric_mean")
        assert hasattr(trace_with_spans.metrics, "test_metric_sum")
        assert trace_with_spans.metrics.test_metric_mean == 1.0
        assert trace_with_spans.metrics.test_metric_sum == 1.0
        assert len(scores) == 1

    def test_populate_local_metric_recursive_with_nested_spans(self, nested_trace) -> None:
        # Test with a nested structure of spans
        local_metric = LocalMetricConfig(
            name="test_metric",
            scorer_fn=simple_scorer,
            aggregator_fn=simple_aggregator,
            scorable_types=[StepType.llm],
            aggregatable_types=[StepType.trace, StepType.workflow],
        )

        scores = []
        _populate_local_metric(nested_trace, local_metric, scores)

        # Get the nested span and middle span
        middle_span = nested_trace.spans[0]
        nested_span = middle_span.spans[0]

        # Verify metrics were set correctly at all levels
        assert hasattr(nested_span.metrics, "test_metric")
        assert hasattr(middle_span.metrics, "test_metric")
        assert hasattr(nested_trace.metrics, "test_metric")
        assert len(scores) == 1
