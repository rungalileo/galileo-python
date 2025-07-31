import logging

from galileo.base import BaseClientModel
from galileo.resources.api.data import create_llm_scorer_version_scorers_scorer_id_version_llm_post, create_scorers_post
from galileo.resources.models import ScorerTypes
from galileo.resources.models.base_scorer_version_response import BaseScorerVersionResponse
from galileo.resources.models.create_llm_scorer_version_request import CreateLLMScorerVersionRequest
from galileo.resources.models.create_scorer_request import CreateScorerRequest
from galileo.resources.models.output_type_enum import OutputTypeEnum
from galileo.resources.models.scorer_defaults import ScorerDefaults
from galileo_core.schemas.logging.step import StepType

_logger = logging.getLogger(__name__)


class Metrics(BaseClientModel):
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

        scorer = create_scorers_post.sync(body=create_scorer_request, client=self.client)

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
            scorer_id=scorer.id, body=version_req, client=self.client
        )

        _logger.info("Created custom LLM metric: %s", name)

        return version_resp


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
