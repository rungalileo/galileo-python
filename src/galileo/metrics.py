import datetime
import logging
from collections.abc import Mapping, Sequence
from typing import Any

from galileo.config import GalileoPythonConfig
from galileo.resources.api.data import (
    create_decision_scorer_version_scorers_scorer_id_version_decision_post,
    create_llm_scorer_version_scorers_scorer_id_version_llm_post,
    create_scorers_post,
    delete_scorer_scorers_scorer_id_delete,
)
from galileo.resources.api.trace import query_metrics_projects_project_id_metrics_search_post
from galileo.resources.models import (
    HTTPValidationError,
    LogRecordsMetricsQueryRequest,
    LogRecordsMetricsResponse,
    ScorerTypes,
)
from galileo.resources.models.base_scorer_version_response import BaseScorerVersionResponse
from galileo.resources.models.create_decision_scorer_version_request import CreateDecisionScorerVersionRequest
from galileo.resources.models.create_llm_scorer_version_request import CreateLLMScorerVersionRequest
from galileo.resources.models.create_scorer_request import CreateScorerRequest
from galileo.resources.models.decision_level import DecisionLevel
from galileo.resources.models.input_type_enum import InputTypeEnum
from galileo.resources.models.output_type_enum import OutputTypeEnum
from galileo.resources.models.scorer_defaults import ScorerDefaults
from galileo.resources.types import UNSET
from galileo.scorers import Scorers
from galileo.search import FilterType
from galileo_core.schemas.logging.step import StepType

_logger = logging.getLogger(__name__)

DEFAULT_DECISION_MODEL_NAME = "jev-1.13.0"

DecisionAnswerOptions = Sequence[str] | Sequence[DecisionLevel | Mapping[str, Any]]


def normalize_decision_answer_options(
    answer_options: DecisionAnswerOptions | None,
) -> list[str] | list[DecisionLevel] | None:
    """Convert user-facing answer options into the request shape.

    Strings pass through (categorical). ``DecisionLevel`` objects and ``{level, label, description}`` dicts
    become ``DecisionLevel`` (discrete). ``None`` stays ``None`` (boolean_probability).
    """
    if answer_options is None:
        return None
    options = list(answer_options)
    if all(isinstance(option, str) for option in options):
        return [str(option) for option in options]
    levels: list[DecisionLevel] = []
    for option in options:
        if isinstance(option, DecisionLevel):
            levels.append(option)
        elif isinstance(option, Mapping):
            levels.append(
                DecisionLevel(
                    level=option["level"], label=option["label"], description=option.get("description") or UNSET
                )
            )
        else:
            raise ValueError(
                "answer_options must be a list of strings (categorical) or a list of DecisionLevel / "
                f"{{level, label, description}} dicts (discrete); got {type(option).__name__}."
            )
    return levels


def _build_decision_version_request(
    model_name: str, question: str, answer_options: list[str] | list[DecisionLevel] | None
) -> CreateDecisionScorerVersionRequest:
    """Build the version request, serializing discrete levels ourselves.

    The generated ``CreateDecisionScorerVersionRequest.to_dict`` has two identical ``isinstance(list)``
    branches for ``list[str] | list[DecisionLevel]``, so it never calls ``DecisionLevel.to_dict`` and would
    send raw objects. ``additional_properties`` is merged into the body verbatim, so levels go there.
    """
    if answer_options and isinstance(answer_options[0], DecisionLevel):
        request = CreateDecisionScorerVersionRequest(model_name=model_name, question=question)
        request.additional_properties["answer_options"] = [
            level.to_dict() for level in answer_options if isinstance(level, DecisionLevel)
        ]
        return request
    return CreateDecisionScorerVersionRequest(model_name=model_name, question=question, answer_options=answer_options)


class Metrics:
    config: GalileoPythonConfig

    def __init__(self) -> None:
        self.config = GalileoPythonConfig.get()

    def delete_metric(self, name: str) -> None:
        scorers_to_delete = Scorers().list(name=name)
        if not scorers_to_delete:
            raise ValueError(f"Scorer with name {name} not found.")

        for scorer in scorers_to_delete:
            response = delete_scorer_scorers_scorer_id_delete.sync(scorer_id=scorer.id, client=self.config.api_client)

            if isinstance(response, HTTPValidationError):
                raise ValueError(response.detail)
            if response is None:
                raise ValueError("Failed to delete metric.")

    def create_custom_llm_metric(
        self,
        name: str,
        user_prompt: str,
        node_level: StepType = StepType.llm,
        cot_enabled: bool = True,
        model_name: str = "gpt-4.1-mini",
        num_judges: int = 3,
        description: str = "",
        tags: list[str] | None = None,
        output_type: OutputTypeEnum = OutputTypeEnum.BOOLEAN,
        ground_truth: bool = False,
    ) -> BaseScorerVersionResponse:
        """
        Create a custom LLM metric.

        Parameters
        ----------
        name: str
            Name of the metric.
        user_prompt: str
            User prompt for the metric.
        node_level: StepType
            Node level for the metric.
        cot_enabled: bool
            Whether chain-of-thought is enabled.
        model_name: str
            Model name to use.
        num_judges: int
            Number of judges for the metric.
        description: str
            Description of the metric.
        tags: List[str]
            Tags associated with the metric.
        output_type: OutputTypeEnum
            Output type for the metric.
        ground_truth: bool
            Whether the scorer requires ground truth (``reference_output``) from the dataset.
            When True, the judge LLM receives the row's ground-truth value in its prompt.

        Returns
        -------
        BaseScorerVersionResponse
            Response containing the created metric details.
        """
        if tags is None:
            tags = []
        create_scorer_request = CreateScorerRequest(
            name=name,
            scorer_type=ScorerTypes.LLM,
            description=description,
            tags=tags,
            defaults=ScorerDefaults(model_name=model_name, num_judges=num_judges, cot_enabled=cot_enabled),
            scoreable_node_types=[node_level],
            output_type=output_type,
            ground_truth=ground_truth,
        )

        scorer = create_scorers_post.sync(body=create_scorer_request, client=self.config.api_client)

        version_req = CreateLLMScorerVersionRequest(user_prompt=user_prompt)
        version_resp = create_llm_scorer_version_scorers_scorer_id_version_llm_post.sync(
            scorer_id=scorer.id, body=version_req, client=self.config.api_client
        )

        _logger.info("Created custom LLM metric: %s", name)

        return version_resp

    def create_decision_metric(
        self,
        name: str,
        question: str,
        node_level: StepType = StepType.llm,
        model_name: str = DEFAULT_DECISION_MODEL_NAME,
        output_type: OutputTypeEnum = OutputTypeEnum.BOOLEAN_PROBABILITY,
        answer_options: DecisionAnswerOptions | None = None,
        input_type: InputTypeEnum | None = None,
        description: str = "",
        tags: list[str] | None = None,
        ground_truth: bool = False,
    ) -> BaseScorerVersionResponse:
        """
        Create a decision metric.

        Parameters
        ----------
        name: str
            Name of the metric.
        question: str
            The question the decision model answers (1-2,000 characters).
        node_level: StepType
            The single node type the metric scores.
        model_name: str
            Decision model registry version, for example ``jev-1.13.0``.
        output_type: OutputTypeEnum
            ``BOOLEAN_PROBABILITY``, ``CATEGORICAL`` or ``DISCRETE``.
        answer_options: list[str] | list[DecisionLevel | dict] | None
            ``None`` for ``BOOLEAN_PROBABILITY``. For ``CATEGORICAL``, a list of 2-255 unique labels. For
            ``DISCRETE``, 2-10 ``DecisionLevel`` objects (or ``{level, label, description}`` dicts) numbered
            0, 1, 2 and so on in order.
        input_type: InputTypeEnum | None
            What the model sees. When ``None``, the server picks a default for the node type.
        description: str
            Description of the metric.
        tags: List[str]
            Tags associated with the metric.
        ground_truth: bool
            Whether the scorer requires ground truth (``reference_output``) from the dataset.

        Returns
        -------
        BaseScorerVersionResponse
            Response containing the created metric version.

        Raises
        ------
        ValueError
            If the API rejects either request. If the scorer was created but its version was rejected,
            the scorer is deleted before the error is raised.
        """
        version_req = _build_decision_version_request(
            model_name=model_name, question=question, answer_options=normalize_decision_answer_options(answer_options)
        )
        create_scorer_request = CreateScorerRequest(
            name=name,
            scorer_type=ScorerTypes.DECISION,
            description=description,
            tags=tags if tags is not None else [],
            scoreable_node_types=[node_level],
            output_type=output_type,
            input_type=input_type if input_type is not None else UNSET,
            ground_truth=ground_truth,
        )

        scorer = create_scorers_post.sync(body=create_scorer_request, client=self.config.api_client)
        if isinstance(scorer, HTTPValidationError):
            raise ValueError(scorer.detail)
        if scorer is None:
            raise ValueError("Failed to create decision metric.")

        try:
            version_resp = create_decision_scorer_version_scorers_scorer_id_version_decision_post.sync(
                scorer_id=scorer.id, body=version_req, client=self.config.api_client
            )
            if isinstance(version_resp, HTTPValidationError):
                raise ValueError(version_resp.detail)
            if version_resp is None:
                raise ValueError("Failed to create decision metric version.")
        except Exception:
            self._delete_scorer_quietly(scorer.id)
            raise

        _logger.info("Created decision metric: %s", name)

        return version_resp

    def _delete_scorer_quietly(self, scorer_id: str) -> None:
        """Best-effort cleanup so a failed create does not leave an empty scorer behind."""
        try:
            delete_scorer_scorers_scorer_id_delete.sync(scorer_id=scorer_id, client=self.config.api_client)
        except Exception:
            _logger.warning(
                "Failed to delete scorer after decision metric creation failed", extra={"scorer_id": scorer_id}
            )

    def query(
        self,
        project_id: str,
        start_time: datetime.datetime,
        end_time: datetime.datetime,
        experiment_id: str | None = None,
        log_stream_id: str | None = None,
        filters: list[FilterType] | None = None,
        group_by: str | None = None,
        interval: int = 5,
    ) -> LogRecordsMetricsResponse:
        body = LogRecordsMetricsQueryRequest(
            start_time=start_time,
            end_time=end_time,
            experiment_id=experiment_id,
            log_stream_id=log_stream_id,
            filters=filters or [],
            group_by=group_by,
            interval=interval,
        )

        response = query_metrics_projects_project_id_metrics_search_post.sync(
            client=self.config.api_client, project_id=str(project_id), body=body
        )

        if isinstance(response, HTTPValidationError):
            raise ValueError(response.detail)
        if response is None:
            raise ValueError("Failed to query for metrics.")

        return response


# Public functions
def create_custom_llm_metric(
    name: str,
    user_prompt: str,
    node_level: StepType = StepType.llm,
    cot_enabled: bool = True,
    model_name: str = "gpt-4.1-mini",
    num_judges: int = 3,
    description: str = "",
    tags: list[str] | None = None,
    output_type: OutputTypeEnum = OutputTypeEnum.BOOLEAN,
    ground_truth: bool = False,
) -> BaseScorerVersionResponse:
    """
    Create a custom LLM metric.

    Parameters
    ----------
    name: str
        Name of the metric.
    user_prompt: str
        User prompt for the metric.
    node_level: StepType
        Node level for the metric.
    cot_enabled: bool
        Whether chain-of-thought is enabled.
    model_name: str
        Model name to use.
    num_judges: int
        Number of judges for the metric.
    description: str
        Description of the metric.
    tags: List[str]
        Tags associated with the metric.
    output_type: OutputTypeEnum
        Output type for the metric.
    ground_truth: bool
        Whether the scorer requires ground truth (``reference_output``) from the dataset.
        When True, the judge LLM receives the row's ground-truth value in its prompt.

    Returns
    -------
    BaseScorerVersionResponse
        Response containing the created metric details.
    """
    if tags is None:
        tags = []
    return Metrics().create_custom_llm_metric(
        name, user_prompt, node_level, cot_enabled, model_name, num_judges, description, tags, output_type, ground_truth
    )


def create_decision_metric(
    name: str,
    question: str,
    node_level: StepType = StepType.llm,
    model_name: str = DEFAULT_DECISION_MODEL_NAME,
    output_type: OutputTypeEnum = OutputTypeEnum.BOOLEAN_PROBABILITY,
    answer_options: DecisionAnswerOptions | None = None,
    input_type: InputTypeEnum | None = None,
    description: str = "",
    tags: list[str] | None = None,
    ground_truth: bool = False,
) -> BaseScorerVersionResponse:
    """
    Create a decision metric.

    A decision metric asks a decision model (for example TypeSafe's Jev) one typed question and
    scores the node with the probabilities of the answers.

    Parameters
    ----------
    name: str
        Name of the metric.
    question: str
        The question the decision model answers (1-2,000 characters).
    node_level: StepType
        The single node type the metric scores.
    model_name: str
        Decision model registry version, for example ``jev-1.13.0``.
    output_type: OutputTypeEnum
        ``BOOLEAN_PROBABILITY``, ``CATEGORICAL`` or ``DISCRETE``.
    answer_options: list[str] | list[DecisionLevel | dict] | None
        ``None`` for ``BOOLEAN_PROBABILITY``. For ``CATEGORICAL``, a list of 2-255 unique labels. For
        ``DISCRETE``, 2-10 ``DecisionLevel`` objects (or ``{level, label, description}`` dicts) numbered
        0, 1, 2 and so on in order.
    input_type: InputTypeEnum | None
        What the model sees. When ``None``, the server picks a default for the node type.
    description: str
        Description of the metric.
    tags: List[str]
        Tags associated with the metric.
    ground_truth: bool
        Whether the scorer requires ground truth (``reference_output``) from the dataset.

    Returns
    -------
    BaseScorerVersionResponse
        Response containing the created metric version.

    Raises
    ------
    ValueError
        If the API rejects either request. If the scorer was created but its version was rejected,
        the scorer is deleted before the error is raised.

    Examples
    --------
        from galileo.metrics import create_decision_metric
        from galileo.resources.models import OutputTypeEnum

        create_decision_metric(
            name="tone",
            question="Is the tone of this response professional?",
            output_type=OutputTypeEnum.CATEGORICAL,
            answer_options=["professional", "casual", "rude"],
        )
    """
    return Metrics().create_decision_metric(
        name=name,
        question=question,
        node_level=node_level,
        model_name=model_name,
        output_type=output_type,
        answer_options=answer_options,
        input_type=input_type,
        description=description,
        tags=tags,
        ground_truth=ground_truth,
    )


def get_metrics(
    project_id: str,
    start_time: datetime.datetime,
    end_time: datetime.datetime,
    experiment_id: str | None = None,
    log_stream_id: str | None = None,
    filters: list[FilterType] | None = None,
    group_by: str | None = None,
    interval: int = 5,
) -> LogRecordsMetricsResponse:
    """Queries for metrics in a project.

    Parameters
    ----------
    project_id
        The unique identifier of the project.
    start_time
        The start of the time range for the query.
    end_time
        The end of the time range for the query.
    experiment_id
        Filter records by a specific experiment ID.
    log_stream_id
        Filter records by a specific run ID.
    filters
        A list of filters to apply to the query.
    group_by
        The field to group the results by.
    interval
        The time interval for the query in seconds.

    Returns
    -------
    LogRecordsMetricsResponse
        A LogRecordsMetricsResponse object containing the query results, or None if the query fails.
    """
    return Metrics().query(
        project_id=project_id,
        start_time=start_time,
        end_time=end_time,
        experiment_id=experiment_id,
        log_stream_id=log_stream_id,
        filters=filters,
        group_by=group_by,
        interval=interval,
    )


def delete_metric(name: str) -> None:
    """
    Deletes a metric by its name.

    Parameters
    ----------
    name
        The name of the metric to delete.
    """
    Metrics().delete_metric(name)
