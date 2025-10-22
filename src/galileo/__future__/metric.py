from __future__ import annotations

import builtins
import logging
from datetime import datetime
from typing import Any, Callable

from galileo.__future__.base import BusinessObjectMixin, SyncState
from galileo.__future__.exceptions import ValidationError
from galileo.metrics import Metrics
from galileo.resources.models import OutputTypeEnum, ScorerTypes
from galileo.resources.types import Unset
from galileo.schema.metrics import GalileoScorers, LocalMetricConfig
from galileo.schema.metrics import Metric as LegacyMetric
from galileo.scorers import Scorers
from galileo_core.schemas.logging.span import Span
from galileo_core.schemas.logging.step import StepType
from galileo_core.schemas.logging.trace import Trace
from galileo_core.schemas.shared.metric import MetricValueType

logger = logging.getLogger(__name__)


class BuiltInScorers:
    """
    Provides convenient access to built-in Galileo scorers.

    Examples
    --------
        from galileo.__future__ import Metric

        # Access built-in scorers
        Metric.scorers.correctness
        Metric.scorers.completeness
        Metric.scorers.toxicity
    """

    def __getattr__(self, name: str) -> GalileoScorers:
        """Allow attribute-style access to built-in scorers."""
        # Try to find the scorer by name
        for scorer in GalileoScorers:
            # Match against both enum name (UI-visible) and internal value
            if scorer.name == name or scorer.value.lstrip("_") == name:
                return scorer
        raise AttributeError(
            f"Built-in scorer '{name}' not found. Available: {[s.name for s in GalileoScorers]}"
        )

    def __dir__(self) -> list[str]:
        """Return list of available scorer names for autocomplete."""
        return [scorer.name for scorer in GalileoScorers]


class Metric(BusinessObjectMixin):
    """
    Unified, object-centric interface for Galileo metrics.

    This class provides three ways to work with metrics:

    1. **Built-in Galileo Scorers** - Access via `Metric.scorers.correctness`
    2. **Custom LLM Metrics** - Create with prompt templates and judge models
    3. **Local Function Metrics** - Define custom scoring functions

    Attributes
    ----------
        id (str | None): The unique metric identifier (UUID).
        name (str): The metric name.
        scorer_type (ScorerTypes | None): The type of scorer (LLM, CODE, LOCAL, etc.).
        description (str): Description of the metric.
        tags (list[str]): Tags associated with the metric.
        prompt (str | None): Prompt template for LLM-based scorers (alias for user_prompt).
        model (str | None): Model name used for the scorer (alias for model_name).
        judges (int | None): Number of judges for the metric (alias for num_judges).
        cot_enabled (bool | None): Whether chain-of-thought is enabled.
        node_level (StepType | None): Node level for the metric.
        output_type (str | OutputTypeEnum | None): Output type for the metric.
        scorer_fn (Callable | None): Scoring function for local metrics.
        scorable_types (list[StepType] | None): Types that can be scored (for local metrics).
        aggregatable_types (list[StepType] | None): Types that can be aggregated (for local metrics).
        created_at (datetime | None): When the metric was created.
        updated_at (datetime | None): When the metric was last updated.

    Class Attributes
    ----------------
        scorers (BuiltInScorers): Access built-in Galileo scorers.

    Examples
    --------
        # 1. Use built-in scorers
        from galileo.__future__ import Metric, LogStream

        log_stream = LogStream.get(name="my-stream", project_name="my-project")
        log_stream.set_metrics([
            Metric.scorers.correctness,
            Metric.scorers.completeness,
            "context_relevance",  # String names also work
        ])

        # 2. Create custom LLM metric
        custom_metric = Metric(
            name="response_quality",
            prompt='''
            Rate the quality of this response on a scale of 1-10.

            Question: {input}
            Answer: {output}

            Return only the numerical score (1-10).
            ''',
            model="gpt-4o-mini",
            judges=3,
            node_level=StepType.llm,
            description="Rates response quality",
            tags=["quality", "custom"],
            output_type="percentage",
            cot_enabled=True,
        ).create()

        # 3. Create local function-based metric
        def response_length_scorer(trace_or_span):
            if hasattr(trace_or_span, "output") and trace_or_span.output:
                return min(len(trace_or_span.output) / 100.0, 1.0)
            return 0.0

        local_metric = Metric(
            name="response_length",
            scorer_fn=response_length_scorer,
            scorable_types=[StepType.llm],
            aggregatable_types=[StepType.trace],
        )

        # Use all together
        log_stream.set_metrics([
            Metric.scorers.correctness,
            custom_metric,
            local_metric,
        ])

        # Get existing metric
        metric = Metric.get(name="response_quality")

        # List all metrics
        metrics = Metric.list()

        # Delete a metric
        metric.delete()
    """

    # Class attribute for built-in scorers
    scorers = BuiltInScorers()

    # Type annotations for instance attributes
    id: str | None
    name: str
    scorer_type: ScorerTypes | None
    description: str
    tags: list[str]
    prompt: str | None  # Alias for user_prompt
    model: str | None  # Alias for model_name
    judges: int | None  # Alias for num_judges
    cot_enabled: bool | None
    node_level: StepType | None
    output_type: str | OutputTypeEnum | None
    scorer_fn: Callable[[Trace | Span], MetricValueType] | None
    scorable_types: list[StepType] | None
    aggregatable_types: list[StepType] | None
    created_at: datetime | None
    updated_at: datetime | None
    version: int | None

    def __init__(
        self,
        name: str | None = None,
        *,
        # LLM metric parameters (improved API)
        prompt: str | None = None,
        model: str | None = None,
        judges: int | None = None,
        # Backward compatibility aliases
        user_prompt: str | None = None,
        model_name: str | None = None,
        num_judges: int | None = None,
        # Local metric parameters
        scorer_fn: Callable[[Trace | Span], MetricValueType] | None = None,
        scorable_types: list[StepType] | None = None,
        aggregatable_types: list[StepType] | None = None,
        # Common parameters
        scorer_type: ScorerTypes | None = None,
        node_level: StepType | None = None,
        cot_enabled: bool | None = None,
        description: str = "",
        tags: list[str] | None = None,
        output_type: str | OutputTypeEnum | None = None,
        version: int | None = None,
    ) -> None:
        """
        Initialize a Metric instance.

        Creates a local metric object that can be:
        1. A reference to an existing metric (if only name provided)
        2. A new LLM metric to be created (if prompt provided)
        3. A local function-based metric (if scorer_fn provided)

        Args:
            name: The name of the metric.
            prompt: Prompt template for LLM scorers (preferred over user_prompt).
            model: Model name to use (preferred over model_name). Defaults to "gpt-4.1-mini".
            judges: Number of judges (preferred over num_judges). Defaults to 3.
            user_prompt: [Deprecated] Use 'prompt' instead.
            model_name: [Deprecated] Use 'model' instead.
            num_judges: [Deprecated] Use 'judges' instead.
            scorer_fn: Scoring function for local metrics.
            scorable_types: Step types that can be scored (for local metrics).
            aggregatable_types: Step types for aggregation (for local metrics).
            scorer_type: Type of scorer. Auto-detected if not provided.
            node_level: Node level for the metric. Defaults to StepType.llm.
            cot_enabled: Whether chain-of-thought is enabled. Defaults to True.
            description: Description of the metric.
            tags: Tags associated with the metric.
            output_type: Output type ("percentage", "boolean", etc.).
            version: Specific version to reference (for existing metrics).

        Raises
        ------
            ValidationError: If parameters are invalid or contradictory.
        """
        super().__init__()

        if name is None:
            raise ValidationError("'name' must be provided. Use Metric.get() to retrieve an existing metric by ID.")

        # Handle parameter aliases (new names preferred)
        final_prompt = prompt or user_prompt
        final_model = model or model_name or "gpt-4.1-mini"
        final_judges = judges if judges is not None else (num_judges if num_judges is not None else 3)

        # Auto-detect scorer type
        if scorer_type is None:
            if scorer_fn is not None:
                scorer_type = None  # Local metrics don't have a scorer_type
            elif final_prompt is not None:
                scorer_type = ScorerTypes.LLM
            else:
                # Just a reference to existing metric
                scorer_type = None

        # Validate LLM metrics
        if scorer_type == ScorerTypes.LLM and final_prompt is None and scorer_fn is None:
            raise ValidationError("'prompt' (or 'user_prompt') must be provided for LLM-based metrics.")

        # Validate local metrics
        if scorer_fn is not None and final_prompt is not None:
            raise ValidationError("Cannot specify both 'scorer_fn' (local metric) and 'prompt' (LLM metric).")

        # Initialize attributes
        self.name = name
        self.scorer_type = scorer_type
        self.prompt = final_prompt
        self.model = final_model
        self.judges = final_judges
        self.scorer_fn = scorer_fn
        self.scorable_types = scorable_types or [StepType.llm] if scorer_fn else None
        self.aggregatable_types = aggregatable_types or [StepType.trace] if scorer_fn else None
        self.node_level = node_level or StepType.llm
        self.cot_enabled = cot_enabled if cot_enabled is not None else True
        self.description = description
        self.tags = tags if tags is not None else []
        self.version = version

        # Handle output_type (accept string or enum)
        if isinstance(output_type, str):
            # Map common string values to enum
            output_type_map = {
                "percentage": OutputTypeEnum.PERCENTAGE,
                "boolean": OutputTypeEnum.BOOLEAN,
                "categorical": OutputTypeEnum.CATEGORICAL,
                "count": OutputTypeEnum.COUNT,
                "discrete": OutputTypeEnum.DISCRETE,
                "freeform": OutputTypeEnum.FREEFORM,
                "multilabel": OutputTypeEnum.MULTILABEL,
            }
            self.output_type = output_type_map.get(output_type.lower(), OutputTypeEnum.PERCENTAGE)
        else:
            self.output_type = output_type or OutputTypeEnum.BOOLEAN

        # Set defaults for uninitialized attributes
        self.id = None
        self.created_at = None
        self.updated_at = None

        # Set initial state
        self._set_state(SyncState.LOCAL_ONLY)

    def create(self) -> Metric:
        """
        Persist this metric to the API.

        Only works for LLM metrics. Local metrics (with scorer_fn) don't need
        to be created on the server.

        Returns
        -------
            Metric: This metric instance with updated attributes from the API.

        Raises
        ------
            ValidationError: If this is a local metric or invalid configuration.
            NotImplementedError: If scorer_type is not LLM.
            Exception: If the API call fails.

        Examples
        --------
            metric = Metric(
                name="quality_check",
                prompt="Rate the quality...",
                model="gpt-4o-mini"
            ).create()
            assert metric.is_synced()
        """
        if self.scorer_fn is not None:
            raise ValidationError(
                "Local metrics (with scorer_fn) don't need to be created on the server. "
                "Use them directly with log_stream.set_metrics()."
            )

        if self.scorer_type is None:
            raise ValidationError("Cannot create a metric reference. Use Metric.get() to retrieve existing metrics.")

        try:
            logger.info(f"Metric.create: name='{self.name}' type='{self.scorer_type}' - started")

            if self.scorer_type != ScorerTypes.LLM:
                raise NotImplementedError(
                    f"Creating {self.scorer_type} scorers is not yet supported. Only LLM scorers are supported."
                )

            metrics_service = Metrics()
            created_version = metrics_service.create_custom_llm_metric(
                name=self.name,
                user_prompt=self.prompt or "",
                node_level=self.node_level or StepType.llm,
                cot_enabled=self.cot_enabled or True,
                model_name=self.model or "gpt-4.1-mini",
                num_judges=self.judges or 3,
                description=self.description,
                tags=self.tags,
                output_type=self.output_type
                if isinstance(self.output_type, OutputTypeEnum)
                else OutputTypeEnum.BOOLEAN,
            )

            # Update attributes from response
            self.id = str(created_version.scorer_id)
            self.created_at = created_version.created_at
            self.updated_at = created_version.updated_at

            # Refresh to get full scorer details
            self.refresh()

            logger.info(f"Metric.create: id='{self.id}' - completed")
            return self
        except (ValidationError, NotImplementedError):
            raise
        except Exception as e:
            self._set_state(SyncState.FAILED_SYNC, error=e)
            logger.error(f"Metric.create: name='{self.name}' - failed: {e}")
            raise

    @classmethod
    def get(cls, *, id: str | None = None, name: str | None = None) -> Metric | None:
        """
        Get an existing metric by ID or name.

        Args:
            id: The metric ID (UUID).
            name: The metric name.

        Returns
        -------
            Optional[Metric]: The metric if found, None otherwise.

        Raises
        ------
            ValidationError: If neither or both id and name are provided.

        Examples
        --------
            # Get by name
            metric = Metric.get(name="factuality-checker")

            # Get by ID
            metric = Metric.get(id="abc-123-def")
        """
        if id is not None and name is not None:
            raise ValidationError("Cannot specify both id and name")
        if id is None and name is None:
            raise ValidationError("Must specify either id or name")

        scorers_service = Scorers()

        if name is not None:
            scorers = scorers_service.list(name=name)
            if not scorers:
                return None
            retrieved_scorer = next((s for s in scorers if s.name == name), None)
            if retrieved_scorer is None:
                return None
        else:
            assert id is not None
            scorers = scorers_service.list()
            retrieved_scorer = next((s for s in scorers if s.id == id), None)
            if retrieved_scorer is None:
                return None

        instance = cls.__new__(cls)
        BusinessObjectMixin.__init__(instance)
        instance._populate_from_scorer_response(retrieved_scorer)
        instance._set_state(SyncState.SYNCED)
        return instance

    @classmethod
    def list(
        cls, *, name_filter: str | None = None, scorer_types: list[ScorerTypes] | None = None
    ) -> builtins.list[Metric]:
        """
        List metrics with optional filtering.

        Args:
            name_filter: Filter metrics by exact name match.
            scorer_types: Filter by scorer types.

        Returns
        -------
            list[Metric]: List of metrics matching the criteria.

        Examples
        --------
            # List all metrics
            metrics = Metric.list()

            # List LLM metrics only
            metrics = Metric.list(scorer_types=[ScorerTypes.LLM])

            # List by name
            metrics = Metric.list(name_filter="factuality")
        """
        logger.debug(f"Metric.list: name_filter='{name_filter}' types={scorer_types} - started")
        scorers_service = Scorers()
        retrieved_scorers = scorers_service.list(name=name_filter, types=scorer_types)
        logger.debug(f"Metric.list: found {len(retrieved_scorers)} metrics - completed")

        result = []
        for retrieved_scorer in retrieved_scorers:
            instance = cls.__new__(cls)
            BusinessObjectMixin.__init__(instance)
            instance._populate_from_scorer_response(retrieved_scorer)
            instance._set_state(SyncState.SYNCED)
            result.append(instance)

        return result

    def _populate_from_scorer_response(self, scorer_response: Any) -> None:
        """Populate instance attributes from a ScorerResponse object."""
        self.id = scorer_response.id
        self.name = scorer_response.name
        self.scorer_type = scorer_response.scorer_type
        self.tags = scorer_response.tags
        self.scorer_fn = None
        self.scorable_types = None
        self.aggregatable_types = None
        self.version = None

        # Handle optional attributes
        self.description = (
            ""
            if isinstance(scorer_response.description, Unset) or scorer_response.description is None
            else scorer_response.description
        )
        self.created_at = None if isinstance(scorer_response.created_at, Unset) else scorer_response.created_at
        self.updated_at = None if isinstance(scorer_response.updated_at, Unset) else scorer_response.updated_at
        self.output_type = None if isinstance(scorer_response.output_type, Unset) else scorer_response.output_type
        self.prompt = None if isinstance(scorer_response.user_prompt, Unset) else scorer_response.user_prompt

        # Extract defaults
        if not isinstance(scorer_response.defaults, Unset) and scorer_response.defaults is not None:
            self.model = (
                scorer_response.defaults.model_name if hasattr(scorer_response.defaults, "model_name") else None
            )
            self.judges = (
                scorer_response.defaults.num_judges if hasattr(scorer_response.defaults, "num_judges") else None
            )
            self.cot_enabled = (
                scorer_response.defaults.cot_enabled if hasattr(scorer_response.defaults, "cot_enabled") else None
            )
        else:
            self.model = None
            self.judges = None
            self.cot_enabled = None

        # Extract scoreable node types
        if not isinstance(scorer_response.scoreable_node_types, Unset) and scorer_response.scoreable_node_types:
            try:
                self.node_level = StepType(scorer_response.scoreable_node_types[0])
            except (ValueError, IndexError):
                self.node_level = None
        else:
            self.node_level = None

    def update(self, **kwargs: Any) -> None:
        """
        Update this metric's properties.

        Currently not implemented as the API doesn't support updating scorers.

        Raises
        ------
            NotImplementedError: Always raised as updates are not supported.
        """
        raise NotImplementedError(
            "Updating metrics is not yet supported by the API. "
            "Consider creating a new metric with the desired properties instead."
        )

    def delete(self) -> None:
        """
        Delete this metric.

        Only works for server-side metrics. Local metrics don't need deletion.

        Raises
        ------
            ValidationError: If this is a local metric.
            ValueError: If the metric is not synced.

        Examples
        --------
            metric = Metric.get(name="factuality-checker")
            metric.delete()
        """
        if self.scorer_fn is not None:
            raise ValidationError("Local metrics (with scorer_fn) don't exist on the server and can't be deleted.")

        if self.id is None:
            raise ValueError("Metric ID is not set. Cannot delete a local-only metric.")

        try:
            logger.info(f"Metric.delete: id='{self.id}' name='{self.name}' - started")
            metrics_service = Metrics()
            metrics_service.delete_metric(name=self.name)
            self._set_state(SyncState.DELETED)
            logger.info(f"Metric.delete: id='{self.id}' - completed")
        except Exception as e:
            self._set_state(SyncState.FAILED_SYNC, error=e)
            logger.error(f"Metric.delete: id='{self.id}' - failed: {e}")
            raise

    def refresh(self) -> None:
        """
        Refresh this metric's state from the API.

        Updates all attributes with the latest values from the remote API.

        Raises
        ------
            ValidationError: If this is a local metric.
            ValueError: If the metric is not synced.
            Exception: If the API call fails or the metric no longer exists.

        Examples
        --------
            metric.refresh()
            assert metric.is_synced()
        """
        if self.scorer_fn is not None:
            raise ValidationError("Local metrics (with scorer_fn) don't exist on the server and can't be refreshed.")

        if self.id is None:
            raise ValueError("Metric ID is not set. Cannot refresh a local-only metric.")

        try:
            logger.debug(f"Metric.refresh: id='{self.id}' - started")
            scorers_service = Scorers()
            scorers = scorers_service.list()
            retrieved_scorer = next((s for s in scorers if s.id == self.id), None)

            if retrieved_scorer is None:
                raise ValueError(f"Metric with id '{self.id}' no longer exists")

            self._populate_from_scorer_response(retrieved_scorer)
            self._set_state(SyncState.SYNCED)
            logger.debug(f"Metric.refresh: id='{self.id}' - completed")
        except Exception as e:
            self._set_state(SyncState.FAILED_SYNC, error=e)
            logger.error(f"Metric.refresh: id='{self.id}' - failed: {e}")
            raise

    def to_legacy_metric(self) -> LegacyMetric:
        """
        Convert to legacy galileo.schema.metrics.Metric format.

        This enables backward compatibility with existing code that uses
        the legacy Metric class.

        Returns
        -------
            LegacyMetric: Legacy metric object with name and version.

        Examples
        --------
            metric = Metric.get(name="my-metric")
            legacy = metric.to_legacy_metric()
            # Use with existing APIs
        """
        return LegacyMetric(name=self.name, version=self.version)

    def to_local_metric_config(self) -> LocalMetricConfig:
        """
        Convert to LocalMetricConfig format.

        Only works for metrics with scorer_fn defined.

        Returns
        -------
            LocalMetricConfig: Local metric configuration.

        Raises
        ------
            ValidationError: If this metric doesn't have a scorer_fn.

        Examples
        --------
            def my_scorer(trace):
                return 0.5

            metric = Metric(name="test", scorer_fn=my_scorer)
            config = metric.to_local_metric_config()
        """
        if self.scorer_fn is None:
            raise ValidationError(
                "Can only convert to LocalMetricConfig if scorer_fn is provided. "
                "This metric is not a local function-based metric."
            )

        return LocalMetricConfig(
            name=self.name,
            scorer_fn=self.scorer_fn,
            scorable_types=self.scorable_types or [StepType.llm],
            aggregatable_types=self.aggregatable_types or [StepType.trace],
        )

    def __str__(self) -> str:
        """String representation of the metric."""
        metric_type = "local" if self.scorer_fn else (self.scorer_type.value if self.scorer_type else "reference")
        return f"Metric(name='{self.name}', id='{self.id}', type='{metric_type}')"

    def __repr__(self) -> str:
        """Detailed string representation of the metric."""
        if self.scorer_fn:
            return f"Metric(name='{self.name}', type='local', scorer_fn={self.scorer_fn.__name__})"
        if self.scorer_type:
            return (
                f"Metric(name='{self.name}', id='{self.id}', type='{self.scorer_type.value}', "
                f"model='{self.model}', judges={self.judges})"
            )
        return f"Metric(name='{self.name}', version={self.version})"
