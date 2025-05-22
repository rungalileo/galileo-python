from typing import Union

from galileo.schema.metrics import LocalMetricConfig
from galileo_core.schemas.logging.span import Span, StepWithChildSpans
from galileo_core.schemas.logging.trace import Trace
from galileo_core.schemas.shared.metric import MetricValueType


def populate_local_metrics(step: Union[Trace, Span], local_metrics: list[LocalMetricConfig]) -> None:
    for local_metric in local_metrics:
        _populate_local_metric(step, local_metric, [])


def _populate_local_metric(
    step: Union[Trace, Span], local_metric: LocalMetricConfig, scores: list[MetricValueType]
) -> None:
    if isinstance(step, StepWithChildSpans):
        for span in step.spans:
            _populate_local_metric(span, local_metric, scores)
        if local_metric.aggregator_fn and scores and step.type in local_metric.aggregatable_types:
            aggregate_metric_result = local_metric.aggregator_fn(scores)
            if isinstance(aggregate_metric_result, dict):
                for suffix, value in aggregate_metric_result.items():
                    setattr(step.metrics, local_metric.name + "_" + suffix.removeprefix("_"), value)
            else:
                setattr(step.metrics, local_metric.name, aggregate_metric_result)
    if step.type in local_metric.scorable_types:
        metric_value = local_metric.scorer_fn(step)
        setattr(step.metrics, local_metric.name, local_metric.scorer_fn(step))
        scores.append(metric_value)
