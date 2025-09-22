import datetime
import logging
from typing import Optional

from galileo.config import GalileoPythonConfig
from galileo.resources.api.data import create_llm_scorer_version_scorers_scorer_id_version_llm_post, create_scorers_post
from galileo.resources.api.trace import query_metrics_projects_project_id_metrics_search_post
from galileo.resources.models import (
    HTTPValidationError,
    LogRecordsMetricsQueryRequest,
    LogRecordsMetricsResponse,
    ScorerTypes,
)
from galileo.resources.models.base_scorer_version_response import BaseScorerVersionResponse
from galileo.resources.models.create_llm_scorer_version_request import CreateLLMScorerVersionRequest
from galileo.resources.models.create_scorer_request import CreateScorerRequest
from galileo.resources.models.output_type_enum import OutputTypeEnum
from galileo.resources.models.scorer_defaults import ScorerDefaults
from galileo.search import FilterType
from galileo_core.schemas.logging.step import StepType

_logger = logging.getLogger(__name__)


class Metrics:
    config: GalileoPythonConfig

    def __init__(self) -> None:
        self.config = GalileoPythonConfig.get()

    def create_custom_llm_metric(
        self,
        name: str,
        user_prompt: str,
        node_level: StepType = StepType.llm,
        cot_enabled: bool = True,
        model_name: str = "gpt-4.1-mini",
        num_judges: int = 3,
        description: str = "",
        tags: list[str] = [],
        output_type: OutputTypeEnum = OutputTypeEnum.BOOLEAN,
    ) -> BaseScorerVersionResponse:
        """
        Create a custom LLM metric.

        Args:
            name (str): Name of the metric.
            user_prompt (str): User prompt for the metric.
            node_level (StepType): Node level for the metric.
            cot_enabled (bool): Whether chain-of-thought is enabled.
            model_name (str): Model name to use.
            num_judges (int): Number of judges for the metric.
            description (str): Description of the metric.
            tags (List[str]): Tags associated with the metric.
            output_type (OutputTypeEnum): Output type for the metric.

        Returns:
            BaseScorerVersionResponse: Response containing the created metric details.
        """

        create_scorer_request = CreateScorerRequest(
            name=name,
            scorer_type=ScorerTypes.LLM,
            description=description,
            tags=tags,
            defaults=ScorerDefaults(model_name=model_name, num_judges=num_judges),
        )

        scorer = create_scorers_post.sync(body=create_scorer_request, client=self.config.api_client)

        scoreable_node_types = [node_level]
        version_req = CreateLLMScorerVersionRequest(
            user_prompt=user_prompt,
            scoreable_node_types=scoreable_node_types,
            cot_enabled=cot_enabled,
            output_type=output_type,
            model_name=model_name,
            num_judges=num_judges,
        )
        version_resp = create_llm_scorer_version_scorers_scorer_id_version_llm_post.sync(
            scorer_id=scorer.id, body=version_req, client=self.config.api_client
        )

        _logger.info("Created custom LLM metric: %s", name)

        return version_resp

    def query(
        self,
        project_id: str,
        start_time: datetime.datetime,
        end_time: datetime.datetime,
        experiment_id: Optional[str] = None,
        log_stream_id: Optional[str] = None,
        filters: Optional[list[FilterType]] = None,
        group_by: Optional[str] = None,
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
    tags: list[str] = [],
    output_type: OutputTypeEnum = OutputTypeEnum.BOOLEAN,
) -> BaseScorerVersionResponse:
    """
    Create a custom LLM metric.

    Args:
        name (str): Name of the metric.
        user_prompt (str): User prompt for the metric.
        node_level (StepType): Node level for the metric.
        cot_enabled (bool): Whether chain-of-thought is enabled.
        model_name (str): Model name to use.
        num_judges (int): Number of judges for the metric.
        description (str): Description of the metric.
        tags (List[str]): Tags associated with the metric.
        output_type (OutputTypeEnum): Output type for the metric.

    Returns:
        BaseScorerVersionResponse: Response containing the created metric details.
    """
    return Metrics().create_custom_llm_metric(
        name, user_prompt, node_level, cot_enabled, model_name, num_judges, description, tags, output_type
    )


def get_metrics(
    project_id: str,
    start_time: datetime.datetime,
    end_time: datetime.datetime,
    experiment_id: Optional[str] = None,
    log_stream_id: Optional[str] = None,
    filters: Optional[list[FilterType]] = None,
    group_by: Optional[str] = None,
    interval: int = 5,
) -> LogRecordsMetricsResponse:
    """Queries for metrics in a project.

    Args:
        project_id: The unique identifier of the project.
        start_time: The start of the time range for the query.
        end_time: The end of the time range for the query.
        experiment_id: Filter records by a specific experiment ID.
        log_stream_id: Filter records by a specific run ID.
        filters: A list of filters to apply to the query.
        group_by: The field to group the results by.
        interval: The time interval for the query in seconds.

    Returns:
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
