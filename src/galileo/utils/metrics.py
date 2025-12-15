import builtins
from typing import Optional, Union

from galileo.resources.models.scorer_config import ScorerConfig
from galileo.schema.metrics import GalileoMetrics, LocalMetricConfig, Metric
from galileo.scorers import Scorers, ScorerSettings
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


def create_metric_configs(
    project_id: str,
    run_id: str,  # Can be experiment_id or log_stream_id
    metrics: builtins.list[Union[GalileoMetrics, Metric, LocalMetricConfig, str]],
) -> tuple[builtins.list[ScorerConfig], builtins.list[LocalMetricConfig]]:
    """
    Process metrics and create scorer configurations for experiments or log streams.

    This unified function categorizes metrics into server-side and client-side types,
    validates they exist, and registers server-side metrics with Galileo.

    Parameters
    ----------
    project_id : str
        The ID of the project
    run_id : str
        The ID of the run (can be experiment ID or log stream ID)
    metrics : builtins.list[Union[GalileoMetrics, Metric, LocalMetricConfig, str]]
        List of metrics to configure

    Returns
    -------
    tuple[builtins.list[ScorerConfig], builtins.list[LocalMetricConfig]]
        A tuple containing:
        - List of ScorerConfig objects for server-side metrics configured in Galileo
        - List of LocalMetricConfig objects for client-side metrics to process locally

    Raises
    ------
    ValueError
        If any specified metrics are unknown or don't exist in Galileo
    """
    local_metric_configs: list[LocalMetricConfig] = []
    scorer_name_versions: list[tuple[str, Optional[int]]] = []

    # Categorize metrics by type
    for metric in metrics:
        if isinstance(metric, GalileoMetrics):
            scorer_name_versions.append((metric.value, None))
        elif isinstance(metric, Metric):
            scorer_name_versions.append((metric.name, metric.version))
        elif isinstance(metric, LocalMetricConfig):
            local_metric_configs.append(metric)
        elif isinstance(metric, str):
            scorer_name_versions.append((metric, None))
        else:
            raise ValueError(f"Unknown metric type: {type(metric)}")

    # Process server-side metrics
    scorers: list[ScorerConfig] = []
    if scorer_name_versions:
        all_scorers = Scorers().list()
        known_metrics = {metric.name: metric for metric in all_scorers}
        unknown_metrics = []

        for scorer_name, scorer_version in scorer_name_versions:
            if scorer_name in known_metrics:
                raw_metric_dict = known_metrics[scorer_name].to_dict()

                # Set the version on the ScorerConfig if provided
                if scorer_version is not None:
                    raw_version = Scorers().get_scorer_version(scorer_id=raw_metric_dict["id"], version=scorer_version)
                    raw_metric_dict["scorer_version"] = raw_version.to_dict()
                scorers.append(ScorerConfig.from_dict(raw_metric_dict))
            else:
                unknown_metrics.append(scorer_name)

        if unknown_metrics:
            raise ValueError(
                "One or more non-existent metrics are specified: "
                + ", ".join(f"'{metric}'" for metric in unknown_metrics)
            )

        # Register server-side metrics with Galileo
        ScorerSettings().create(project_id=project_id, run_id=run_id, scorers=scorers)

    return scorers, local_metric_configs
