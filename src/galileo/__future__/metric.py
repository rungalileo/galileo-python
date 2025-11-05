from __future__ import annotations

import builtins
import logging
import os
from abc import ABC
from datetime import datetime
from typing import Any, Callable

from galileo.__future__.configuration import Configuration
from galileo.__future__.shared.base import StateManagementMixin, SyncState
from galileo.__future__.shared.exceptions import ValidationError
from galileo.config import GalileoPythonConfig
from galileo.metrics import Metrics
from galileo.resources.api.data import (
    create_code_scorer_version_scorers_scorer_id_version_code_post,
    create_scorers_post,
)
from galileo.resources.models import (
    BodyCreateCodeScorerVersionScorersScorerIdVersionCodePost,
    CreateScorerRequest,
    OutputTypeEnum,
    ScorerTypes,
)
from galileo.resources.types import File, Unset
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
        # Try to find the scorer by name (enum names match UI-visible names)
        for scorer in GalileoScorers:
            if scorer.name == name:
                return scorer
        raise AttributeError(f"Built-in scorer '{name}' not found. Available: {[s.name for s in GalileoScorers]}")

    def __dir__(self) -> list[str]:
        """Return list of available scorer names for autocomplete."""
        return [scorer.name for scorer in GalileoScorers]


class Metric(StateManagementMixin, ABC):
    """
    Base class for all Galileo metrics.

    This is an abstract base class that defines common attributes and methods
    for all metric types. Use one of the concrete metric classes instead:

    - **GalileoMetric**: Built-in Galileo scorers (access via Metric.scorers)
    - **LlmMetric**: Custom LLM-based metrics with prompt templates
    - **LocalMetric**: Local function-based metrics
    - **CodeMetric**: Code-based metrics (future support)

    Common Attributes
    -----------------
        id (str | None): The unique metric identifier (UUID).
        name (str): The metric name.
        scorer_type (ScorerTypes | None): The type of scorer.
        description (str): Description of the metric.
        tags (list[str]): Tags associated with the metric.
        created_at (datetime | None): When the metric was created.
        updated_at (datetime | None): When the metric was last updated.
        version (int | None): Metric version number.

    Class Attributes
    ----------------
        scorers (BuiltInScorers): Access built-in Galileo scorers.

    Examples
    --------
        # 1. Use built-in Galileo scorers
        from galileo.__future__ import Metric, GalileoMetric, LlmMetric, LocalMetric, LogStream

        log_stream = LogStream.get(name="my-stream", project_name="my-project")
        log_stream.set_metrics([
            Metric.scorers.correctness,
            Metric.scorers.completeness,
        ])

        # 2. Create custom LLM metric
        llm_metric = LlmMetric(
            name="response_quality",
            prompt="Rate the quality...",
            model="gpt-4o-mini",
            judges=3,
        ).create()

        # 3. Create local function-based metric
        def my_scorer(trace_or_span):
            return 0.5

        local_metric = LocalMetric(
            name="response_length",
            scorer_fn=my_scorer,
        )
    """

    # Class attribute for built-in scorers
    scorers = BuiltInScorers()

    # Type annotations for common instance attributes
    id: str | None
    name: str
    scorer_type: ScorerTypes | None
    description: str
    tags: list[str]
    created_at: datetime | None
    updated_at: datetime | None
    version: int | None

    # Scorer defaults - available for LLM and built-in Galileo metrics
    # These are returned by the API in the ScorerDefaults object
    model: str | None
    judges: int | None
    cot_enabled: bool | None

    def __init__(
        self, name: str, *, description: str = "", tags: list[str] | None = None, version: int | None = None
    ) -> None:
        """
        Initialize a base Metric instance with common attributes.

        Args:
            name: The name of the metric.
            description: Description of the metric.
            tags: Tags associated with the metric.
            version: Specific version to reference (for existing metrics).
        """
        super().__init__()
        self.name = name
        self.description = description
        self.tags = tags if tags is not None else []
        self.version = version
        self.id = None
        self.created_at = None
        self.updated_at = None
        self.scorer_type = None

        # Initialize scorer defaults (populated from API for LLM and Galileo metrics)
        self.model = None
        self.judges = None
        self.cot_enabled = None

        self._set_state(SyncState.LOCAL_ONLY)

    @classmethod
    def _create_metric_from_type(cls, scorer_type: ScorerTypes) -> Metric:
        """
        Create the appropriate Metric subclass instance based on scorer_type.

        This is a factory method that centralizes the logic for instantiating
        the correct metric subclass based on the scorer type returned from the API.

        Args:
            scorer_type: The scorer type from the API response.

        Returns
        -------
            Metric: An uninitialized instance of the appropriate subclass
                   (LlmMetric, CodeMetric, or GalileoMetric).

        Examples
        --------
            instance = Metric._create_metric_from_type(ScorerTypes.LLM)
            # Returns: LlmMetric instance
        """
        if scorer_type == ScorerTypes.LLM:
            return LlmMetric.__new__(LlmMetric)
        if scorer_type == ScorerTypes.CODE:
            return CodeMetric.__new__(CodeMetric)
        # Default to GalileoMetric for built-in scorers (LUNA, PRESET, etc.)
        return GalileoMetric.__new__(GalileoMetric)

    @classmethod
    def get(cls, *, id: str | None = None, name: str | None = None) -> Metric | None:
        """
        Get an existing metric by ID or name.

        Returns the appropriate subclass instance based on scorer_type.

        Args:
            id: The metric ID (UUID).
            name: The metric name.

        Returns
        -------
            Optional[Metric]: The metric if found (GalileoMetric, LlmMetric, or CodeMetric), None otherwise.

        Raises
        ------
            ValidationError: If neither or both id and name are provided.

        Examples
        --------
            # Get by name - returns appropriate subclass
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

        # Create appropriate subclass instance based on scorer_type
        instance = cls._create_metric_from_type(retrieved_scorer.scorer_type)
        StateManagementMixin.__init__(instance)
        instance._populate_from_scorer_response(retrieved_scorer)
        instance._set_state(SyncState.SYNCED)
        return instance

    @classmethod
    def list(
        cls, *, name_filter: str | None = None, scorer_types: list[ScorerTypes] | None = None
    ) -> builtins.list[Metric]:
        """
        List metrics with optional filtering.

        Returns appropriate subclass instances based on scorer_type.

        Args:
            name_filter: Filter metrics by exact name match.
            scorer_types: Filter by scorer types.

        Returns
        -------
            list[Metric]: List of metrics matching the criteria (with appropriate subclass types).

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

        result: builtins.list[Metric] = []
        for retrieved_scorer in retrieved_scorers:
            # Create appropriate subclass instance based on scorer_type
            instance = cls._create_metric_from_type(retrieved_scorer.scorer_type)
            StateManagementMixin.__init__(instance)
            instance._populate_from_scorer_response(retrieved_scorer)
            instance._set_state(SyncState.SYNCED)
            result.append(instance)

        return result

    @classmethod
    def delete_by_name(cls, name: str) -> None:
        """
        Delete a metric by name without retrieving it first.

        This is more efficient than calling `Metric.get(name=...).delete()`
        when you only need to delete and don't need the metric object.

        Args:
            name: The name of the metric to delete.

        Raises
        ------
            ValueError: If no metric with the given name exists.

        Examples
        --------
            # Delete without retrieving first
            Metric.delete_by_name("old-metric")

            # Alternative (less efficient)
            metric = Metric.get(name="old-metric")
            metric.delete()
        """
        logger.info(f"Metric.delete_by_name: name='{name}' - started")
        try:
            metrics_service = Metrics()
            metrics_service.delete_metric(name=name)
            logger.info(f"Metric.delete_by_name: name='{name}' - completed")
        except Exception as e:
            logger.error(f"Metric.delete_by_name: name='{name}' - failed: {e}")
            raise

    def _populate_from_scorer_response(self, scorer_response: Any) -> None:
        """Populate instance attributes from a ScorerResponse object."""
        # Common attributes for all metrics
        self.id = scorer_response.id
        self.name = scorer_response.name
        self.scorer_type = scorer_response.scorer_type
        self.tags = scorer_response.tags
        self.version = None

        # Handle optional common attributes
        self.description = (
            ""
            if isinstance(scorer_response.description, Unset) or scorer_response.description is None
            else scorer_response.description
        )
        self.created_at = None if isinstance(scorer_response.created_at, Unset) else scorer_response.created_at
        self.updated_at = None if isinstance(scorer_response.updated_at, Unset) else scorer_response.updated_at

        # Extract defaults - available for LLM and built-in Galileo metrics
        # These are returned by the API for preset scorers too
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

        # LLM-specific attributes (only set if this is an LlmMetric)
        if isinstance(self, LlmMetric):
            self.output_type = None if isinstance(scorer_response.output_type, Unset) else scorer_response.output_type
            self.prompt = None if isinstance(scorer_response.user_prompt, Unset) else scorer_response.user_prompt

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
        if isinstance(self, LocalMetric):
            raise ValidationError("Local metrics don't exist on the server and can't be deleted.")

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
        if isinstance(self, LocalMetric):
            raise ValidationError("Local metrics don't exist on the server and can't be refreshed.")

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

    def __str__(self) -> str:
        """String representation of the metric."""
        type_name = self.__class__.__name__
        scorer_type_str = self.scorer_type.value if self.scorer_type else "unknown"
        return f"{type_name}(name='{self.name}', id='{self.id}', scorer_type='{scorer_type_str}')"

    def __repr__(self) -> str:
        """Detailed string representation of the metric."""
        type_name = self.__class__.__name__
        return f"{type_name}(name='{self.name}', id='{self.id}')"


# ============================================================================
# Concrete Metric Types
# ============================================================================


class LlmMetric(Metric):
    """
    LLM-based metric with custom prompt templates.

    This metric type allows you to create custom metrics evaluated by an LLM
    judge using a prompt template.

    Attributes
    ----------
        prompt (str | None): Prompt template for the LLM scorer.
        model (str | None): Model name to use for scoring.
        judges (int | None): Number of judges to use for scoring.
        cot_enabled (bool | None): Whether chain-of-thought is enabled.
        node_level (StepType | None): Node level for the metric.
        output_type (OutputTypeEnum | None): Output type for the metric.

    Configuration
    -------------
        Default values for `model` and `judges` can be configured via:
        - Configuration.default_scorer_model (env: GALILEO_DEFAULT_SCORER_MODEL)
        - Configuration.default_scorer_judges (env: GALILEO_DEFAULT_SCORER_JUDGES)

    Examples
    --------
        # Create custom LLM metric
        metric = LlmMetric(
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
            output_type=OutputTypeEnum.PERCENTAGE,
            cot_enabled=True,
        ).create()
    """

    # Type annotations for LLM-specific attributes
    prompt: str | None
    model: str | None
    judges: int | None
    cot_enabled: bool | None
    node_level: StepType | None
    output_type: OutputTypeEnum | None

    def __init__(
        self,
        name: str,
        *,
        # LLM metric parameters (improved API)
        prompt: str | None = None,
        model: str | None = None,
        judges: int | None = None,
        # Backward compatibility aliases
        user_prompt: str | None = None,
        model_name: str | None = None,
        num_judges: int | None = None,
        # LLM-specific parameters
        node_level: StepType | None = None,
        cot_enabled: bool | None = None,
        output_type: str | OutputTypeEnum | None = None,
        # Common parameters
        description: str = "",
        tags: list[str] | None = None,
        version: int | None = None,
    ) -> None:
        """
        Initialize an LLM metric.

        Args:
            name: The name of the metric.
            prompt: Prompt template for LLM scorers (preferred over user_prompt).
            model: Model name to use (preferred over model_name). Defaults to Configuration.default_scorer_model.
            judges: Number of judges (preferred over num_judges). Defaults to Configuration.default_scorer_judges.
            user_prompt: [Deprecated] Use 'prompt' instead.
            model_name: [Deprecated] Use 'model' instead.
            num_judges: [Deprecated] Use 'judges' instead.
            node_level: Node level for the metric. Defaults to StepType.llm.
            cot_enabled: Whether chain-of-thought is enabled. Defaults to True.
            output_type: Output type ("percentage", "boolean", etc.).
            description: Description of the metric.
            tags: Tags associated with the metric.
            version: Specific version to reference (for existing metrics).

        Raises
        ------
            ValidationError: If prompt is not provided.
        """
        super().__init__(name=name, description=description, tags=tags, version=version)

        # Handle parameter aliases (new names preferred)
        final_prompt = prompt or user_prompt
        final_model = model or model_name or Configuration.default_scorer_model
        final_judges = (
            judges
            if judges is not None
            else (num_judges if num_judges is not None else Configuration.default_scorer_judges)
        )

        if final_prompt is None:
            raise ValidationError("'prompt' (or 'user_prompt') must be provided for LLM-based metrics.")

        # Initialize LLM-specific attributes
        self.prompt = final_prompt
        self.model = final_model
        self.judges = final_judges
        self.node_level = node_level or StepType.llm
        self.cot_enabled = cot_enabled if cot_enabled is not None else True

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

        self.scorer_type = ScorerTypes.LLM

    def create(self) -> LlmMetric:
        """
        Persist this LLM metric to the API.

        Returns
        -------
            LlmMetric: This metric instance with updated attributes from the API.

        Raises
        ------
            ValidationError: If configuration is invalid.
            Exception: If the API call fails.

        Examples
        --------
            metric = LlmMetric(
                name="quality_check",
                prompt="Rate the quality...",
                model="gpt-4o-mini"
            ).create()
            assert metric.is_synced()
        """
        try:
            logger.info(f"LlmMetric.create: name='{self.name}' - started")

            metrics_service = Metrics()
            created_version = metrics_service.create_custom_llm_metric(
                name=self.name,
                user_prompt=self.prompt or "",
                node_level=self.node_level if self.node_level is not None else StepType.llm,
                cot_enabled=self.cot_enabled if self.cot_enabled is not None else True,
                model_name=self.model if self.model is not None else Configuration.default_scorer_model,
                num_judges=self.judges if self.judges is not None else Configuration.default_scorer_judges,
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

            logger.info(f"LlmMetric.create: id='{self.id}' - completed")
            return self
        except ValidationError:
            raise
        except Exception as e:
            self._set_state(SyncState.FAILED_SYNC, error=e)
            logger.error(f"LlmMetric.create: name='{self.name}' - failed: {e}")
            raise

    def __repr__(self) -> str:
        """Detailed string representation of the metric."""
        return f"LlmMetric(name='{self.name}', id='{self.id}', model='{self.model}', judges={self.judges})"


class CodeMetric(Metric):
    """
    Code-based metric.

    This metric type is for code-based scorers that execute custom code
    to evaluate traces/spans.

    Attributes
    ----------
        code_file_path (str | None): Path to the code file for the scorer.
        node_level (StepType | None): Node level for the metric.

    Examples
    --------
        # Get existing code metric
        metric = Metric.get(name="my-code-metric")
        assert isinstance(metric, CodeMetric)

        # Create code metric
        metric = CodeMetric(
            name="custom_code_scorer",
            code_file_path="./scorers/my_scorer.py",
            node_level=StepType.llm,
            description="Custom code-based scorer",
            tags=["custom", "code"],
        ).create()
    """

    # Type annotations for code-specific attributes (optional for retrieved metrics)
    code_file_path: str | None
    node_level: StepType | None

    def __init__(
        self,
        name: str,
        *,
        code_file_path: str,
        node_level: StepType,
        description: str = "",
        tags: list[str] | None = None,
        version: int | None = None,
    ) -> None:
        """
        Initialize a Code metric.

        Args:
            name: The name of the metric.
            code_file_path: Path to the code file for the scorer (required for creation).
            node_level: Node level for the metric (required for creation).
            description: Description of the metric.
            tags: Tags associated with the metric.
            version: Specific version to reference (for existing metrics).

        Raises
        ------
            ValidationError: If code_file_path file doesn't exist.
        """
        super().__init__(name=name, description=description, tags=tags, version=version)

        # Validate that the file exists
        if not os.path.isfile(code_file_path):
            raise ValidationError(f"Code file not found: {code_file_path}")

        self.code_file_path = code_file_path
        self.node_level = node_level
        self.scorer_type = ScorerTypes.CODE

    def create(self) -> CodeMetric:
        """
        Persist this Code metric to the API.

        Returns
        -------
            CodeMetric: This metric instance with updated attributes from the API.

        Raises
        ------
            ValidationError: If configuration is invalid or code_file_path is not set.
            Exception: If the API call fails.

        Examples
        --------
            metric = CodeMetric(
                name="custom_code_scorer",
                code_file_path="./scorers/my_scorer.py",
                node_level=StepType.llm
            ).create()
            assert metric.is_synced()
        """
        if self.code_file_path is None:
            raise ValidationError("'code_file_path' must be provided to create a code-based metric.")

        try:
            logger.info(f"CodeMetric.create: name='{self.name}' - started")

            config = GalileoPythonConfig.get()

            # Step 1: Create the scorer
            scorer_request = CreateScorerRequest(
                name=self.name, scorer_type=ScorerTypes.CODE, description=self.description, tags=self.tags
            )

            scorer_response = create_scorers_post.sync(client=config.api_client, body=scorer_request)

            if scorer_response is None:
                logger.debug("CodeMetric.create: No response from create_scorers_post")
                raise ValueError("Failed to create code-based metric: No response from API")

            # Step 2: Create the code scorer version with file upload
            # Read the code file
            with open(self.code_file_path, "rb") as f:
                code_file = File(payload=f)
                version_body = BodyCreateCodeScorerVersionScorersScorerIdVersionCodePost(file=code_file)

                created_version = create_code_scorer_version_scorers_scorer_id_version_code_post.sync(
                    scorer_id=scorer_response.id, client=config.api_client, body=version_body
                )

                if created_version is None:
                    logger.debug(
                        "CodeMetric.create: No response from create_code_scorer_version_scorers_scorer_id_version_code_post"
                    )
                    raise ValueError("Failed to create code-based metric: No response from API")

                # Update attributes from response
                self.id = str(scorer_response.id)
                self.created_at = scorer_response.created_at
                self.updated_at = scorer_response.updated_at

                # Refresh to get full scorer details
                self.refresh()

                logger.info(f"CodeMetric.create: id='{self.id}' - completed")
                return self
        except ValidationError:
            raise
        except Exception as e:
            self._set_state(SyncState.FAILED_SYNC, error=e)
            logger.error(f"CodeMetric.create: name='{self.name}' - failed: {e}")
            raise

    def __repr__(self) -> str:
        """Detailed string representation of the metric."""
        return f"CodeMetric(name='{self.name}', id='{self.id}', code_file_path='{self.code_file_path}')"


class GalileoMetric(Metric):
    """
    Built-in Galileo scorer metric.

    This metric type represents Galileo's built-in scorers like correctness,
    completeness, toxicity, etc. Access these via `Metric.scorers`.

    Examples
    --------
        # Access built-in scorers
        from galileo.__future__ import Metric, LogStream

        log_stream = LogStream.get(name="my-stream", project_name="my-project")
        log_stream.set_metrics([
            Metric.scorers.correctness,
            Metric.scorers.completeness,
            Metric.scorers.toxicity,
        ])

        # Or get by name
        metric = Metric.get(name="correctness")
        assert isinstance(metric, GalileoMetric)
    """

    def __init__(
        self, name: str, *, description: str = "", tags: list[str] | None = None, version: int | None = None
    ) -> None:
        """
        Initialize a Galileo metric.

        Args:
            name: The name of the metric.
            description: Description of the metric.
            tags: Tags associated with the metric.
            version: Specific version to reference (for existing metrics).
        """
        super().__init__(name=name, description=description, tags=tags, version=version)
        # Galileo metrics can have various scorer types, set during population


class LocalMetric(Metric):
    """
    Local function-based metric.

    This metric type uses a Python function to score traces/spans locally
    without making API calls. Useful for simple, deterministic metrics.

    Attributes
    ----------
        scorer_fn (Callable): Scoring function that takes a Trace or Span and returns a score.
        scorable_types (list[StepType]): Types that can be scored.
        aggregatable_types (list[StepType]): Types that can be aggregated.

    Examples
    --------
        # Create local function-based metric
        def response_length_scorer(trace_or_span):
            if hasattr(trace_or_span, "output") and trace_or_span.output:
                return min(len(trace_or_span.output) / 100.0, 1.0)
            return 0.0

        local_metric = LocalMetric(
            name="response_length",
            scorer_fn=response_length_scorer,
            scorable_types=[StepType.llm],
            aggregatable_types=[StepType.trace],
        )

        # Use with log stream
        log_stream.set_metrics([local_metric])
    """

    # Type annotations for local metric attributes
    scorer_fn: Callable[[Trace | Span], MetricValueType]
    scorable_types: list[StepType]
    aggregatable_types: list[StepType]

    def __init__(
        self,
        name: str,
        *,
        scorer_fn: Callable[[Trace | Span], MetricValueType],
        scorable_types: list[StepType] | None = None,
        aggregatable_types: list[StepType] | None = None,
        description: str = "",
        tags: list[str] | None = None,
    ) -> None:
        """
        Initialize a local function-based metric.

        Args:
            name: The name of the metric.
            scorer_fn: Scoring function for the metric.
            scorable_types: Step types that can be scored. Defaults to [StepType.llm].
            aggregatable_types: Step types for aggregation. Defaults to [StepType.trace].
            description: Description of the metric.
            tags: Tags associated with the metric.

        Raises
        ------
            ValidationError: If scorer_fn is not provided.
        """
        super().__init__(name=name, description=description, tags=tags)

        if scorer_fn is None:
            raise ValidationError("'scorer_fn' must be provided for local metrics.")

        self.scorer_fn = scorer_fn
        self.scorable_types = scorable_types or [StepType.llm]
        self.aggregatable_types = aggregatable_types or [StepType.trace]
        self.scorer_type = None  # Local metrics don't have a scorer_type

    def to_local_metric_config(self) -> LocalMetricConfig:
        """
        Convert to LocalMetricConfig format.

        Returns
        -------
            LocalMetricConfig: Local metric configuration for use with the logger.

        Examples
        --------
            def my_scorer(trace):
                return 0.5

            metric = LocalMetric(name="test", scorer_fn=my_scorer)
            config = metric.to_local_metric_config()
        """
        return LocalMetricConfig(
            name=self.name,
            scorer_fn=self.scorer_fn,
            scorable_types=self.scorable_types,
            aggregatable_types=self.aggregatable_types,
        )

    def __repr__(self) -> str:
        """Detailed string representation of the metric."""
        # Handle callables that don't have __name__ (partials, lambdas, callable instances)
        fn_name = getattr(self.scorer_fn, "__name__", f"<{type(self.scorer_fn).__name__}>")
        return f"LocalMetric(name='{self.name}', scorer_fn={fn_name})"
