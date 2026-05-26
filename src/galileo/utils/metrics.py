import builtins
import json
import logging
from typing import Any
from uuid import UUID

from galileo.resources.models.scorer_config import ScorerConfig
from galileo.resources.models.scorer_response import ScorerResponse
from galileo.schema.metrics import GalileoMetrics, LocalMetricConfig, Metric
from galileo.scorers import Scorers, ScorerSettings
from galileo_core.schemas.logging.span import Span, StepWithChildSpans
from galileo_core.schemas.logging.trace import Trace
from galileo_core.schemas.shared.metric import MetricValueType

logger = logging.getLogger(__name__)

# Per-row, per-metric upper bound for serialized scorer metadata. Mirrors the
# server-side cap enforced in the runners sandbox so SDK-side and code-scorer
# scorers are subject to the same constraint.
_MAX_METADATA_SERIALIZED_BYTES = 8 * 1024


def _split_score_and_metadata(result: Any) -> tuple[Any, dict | None]:
    """Split a scorer return value into ``(score, metadata)``.

    A 2-tuple whose second element is a dict is the ``(score, metadata)`` shape:
    we use a tuple (not list) check so a vector-valued score like ``[0.1, 0.2]``
    flows through unchanged, and a dict check so a ``(score1, score2)`` 2-tuple
    isn't mistakenly unpacked as metadata. Anything else passes through with
    ``metadata=None``.
    """
    if isinstance(result, tuple) and len(result) == 2 and isinstance(result[1], dict):
        return result[0], result[1]
    return result, None


def _safe_scorer_metadata(metadata: dict, metric_name: str) -> dict | None:
    """Return ``metadata`` if it is safe to attach to ``step.metrics``, else ``None``.

    Metadata flows into HTTPX ``json=`` during trace upload, so a non-serializable
    value (e.g. a ``set``, a ``datetime``) would blow up far from the scorer with
    no useful context. Oversized payloads also bloat ingest. Both are dropped
    with an error log; the score still flows through so the user keeps the metric.
    """
    try:
        serialized = json.dumps(metadata)
    except (TypeError, ValueError) as exc:
        logger.error("Dropping non-JSON-serializable metadata from local metric '%s': %s", metric_name, exc)
        return None
    if len(serialized.encode("utf-8")) > _MAX_METADATA_SERIALIZED_BYTES:
        logger.error(
            "Dropping metadata from local metric '%s': serialized size exceeds %d bytes",
            metric_name,
            _MAX_METADATA_SERIALIZED_BYTES,
        )
        return None
    return metadata


def populate_local_metrics(step: Trace | Span, local_metrics: list[LocalMetricConfig]) -> None:
    for local_metric in local_metrics:
        _populate_local_metric(step, local_metric, [])


def _populate_local_metric(step: Trace | Span, local_metric: LocalMetricConfig, scores: list[MetricValueType]) -> None:
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
        metric_value, metadata = _split_score_and_metadata(local_metric.scorer_fn(step))
        if metadata is not None:
            safe_metadata = _safe_scorer_metadata(metadata, local_metric.name)
            if safe_metadata is not None:
                setattr(step.metrics, f"{local_metric.name}_metadata", safe_metadata)
        setattr(step.metrics, local_metric.name, metric_value)
        scores.append(metric_value)


def _is_uuid(value: str) -> bool:
    """Check if a string is a valid UUID."""
    try:
        UUID(value)
        return True
    except ValueError:
        return False


def create_metric_configs(
    project_id: str,
    run_id: str | None,  # Can be experiment_id, log_stream_id, or None (for trigger=True flow)
    metrics: builtins.list[GalileoMetrics | Metric | LocalMetricConfig | str],
) -> tuple[builtins.list[ScorerConfig], builtins.list[LocalMetricConfig]]:
    """
    Process metrics and create scorer configurations for experiments or log streams.

    This unified function categorizes metrics into server-side and client-side types,
    validates they exist, and registers server-side metrics with Galileo.

    Metrics can be specified as:
    - GalileoMetrics enum values (human-readable labels like "Correctness")
    - Metric objects with name and optional version
    - UUID strings (scorer IDs for direct lookup)
    - Plain strings (searched by label with name fallback)
    - LocalMetricConfig objects (processed client-side)

    Parameters
    ----------
    project_id : str
        The ID of the project
    run_id : Optional[str]
        The ID of the run (can be experiment ID or log stream ID).
        When None, scorer registration is skipped (trigger=True flow).
    metrics : list
        List of metrics to configure

    Returns
    -------
    tuple[list[ScorerConfig], list[LocalMetricConfig]]
        A tuple containing:
        - List of ScorerConfig objects for server-side metrics configured in Galileo
        - List of LocalMetricConfig objects for client-side metrics to process locally

    Raises
    ------
    ValueError
        If any specified metrics are unknown or don't exist in Galileo
    """
    local_metric_configs: list[LocalMetricConfig] = []
    scorer_ids: list[str] = []
    label_searches: list[tuple[str, int | None]] = []

    # Categorize metrics by type
    for metric in metrics:
        if isinstance(metric, GalileoMetrics):
            label_searches.append((metric.value, None))
        elif isinstance(metric, Metric):
            label_searches.append((metric.name, metric.version))
        elif isinstance(metric, LocalMetricConfig):
            local_metric_configs.append(metric)
        elif isinstance(metric, str):
            if _is_uuid(metric):
                scorer_ids.append(metric)
            else:
                label_searches.append((metric, None))
        else:
            raise ValueError(f"Unknown metric type: {type(metric)}")

    # Process server-side metrics with targeted API calls
    scorers_client = Scorers()
    all_resolved: list[ScorerResponse] = []

    if scorer_ids:
        all_resolved.extend(scorers_client.list_by_ids(scorer_ids))

    if label_searches:
        search_values = list({v for v, _ in label_searches})
        all_resolved.extend(scorers_client.list_by_labels(search_values, strict=False))

    # Build lookup maps by id, name, and label
    by_id: dict[str, ScorerResponse] = {str(s.id): s for s in all_resolved}
    by_name: dict[str, ScorerResponse] = {s.name: s for s in all_resolved}
    by_label: dict[str, ScorerResponse] = {}
    for s in all_resolved:
        label = s.label if not isinstance(s.label, type(None)) else None
        if label:
            by_label[label] = s

    scorers: list[ScorerConfig] = []
    unknown_metrics: list[str] = []

    # Match scorer_ids
    for sid in scorer_ids:
        matched = by_id.get(sid)
        if matched:
            scorers.append(ScorerConfig.from_dict(matched.to_dict()))
        else:
            unknown_metrics.append(sid)

    # Match label searches
    for search_val, version in label_searches:
        # Fall back to name (deprecated) match if label match not found
        matched = by_label.get(search_val) or by_name.get(search_val)
        if matched:
            raw_metric_dict = matched.to_dict()
            if version is not None:
                raw_version = scorers_client.get_scorer_version(scorer_id=raw_metric_dict["id"], version=version)
                raw_metric_dict["scorer_version"] = raw_version.to_dict()
            scorers.append(ScorerConfig.from_dict(raw_metric_dict))
        else:
            unknown_metrics.append(search_val)

    if unknown_metrics:
        raise ValueError(
            "One or more non-existent metrics are specified: " + ", ".join(f"'{metric}'" for metric in unknown_metrics)
        )

    # Register server-side metrics with Galileo.
    # Skip registration when run_id is None (trigger=True flow — API handles it).
    if run_id is not None and scorers:
        ScorerSettings().create(project_id=project_id, run_id=run_id, scorers=scorers)

    return scorers, local_metric_configs
