import datetime
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.job_status import JobStatus
from ..models.task_type import TaskType
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.customized_agentic_workflow_success_gpt_scorer import CustomizedAgenticWorkflowSuccessGPTScorer
    from ..models.customized_chunk_attribution_utilization_gpt_scorer import (
        CustomizedChunkAttributionUtilizationGPTScorer,
    )
    from ..models.customized_completeness_gpt_scorer import CustomizedCompletenessGPTScorer
    from ..models.customized_factuality_gpt_scorer import CustomizedFactualityGPTScorer
    from ..models.customized_ground_truth_adherence_gpt_scorer import CustomizedGroundTruthAdherenceGPTScorer
    from ..models.customized_groundedness_gpt_scorer import CustomizedGroundednessGPTScorer
    from ..models.customized_instruction_adherence_gpt_scorer import CustomizedInstructionAdherenceGPTScorer
    from ..models.customized_tool_error_rate_gpt_scorer import CustomizedToolErrorRateGPTScorer
    from ..models.customized_tool_selection_quality_gpt_scorer import CustomizedToolSelectionQualityGPTScorer
    from ..models.get_prompt_run_metrics import GetPromptRunMetrics
    from ..models.prompt_run_settings import PromptRunSettings
    from ..models.registered_scorer import RegisteredScorer
    from ..models.run_tag_db import RunTagDB
    from ..models.scorers_configuration import ScorersConfiguration


T = TypeVar("T", bound="GetPromptRun")


@_attrs_define
class GetPromptRun:
    """
    Attributes:
        created_at (datetime.datetime):
        created_by (str):
        id (str):
        job_id (str):
        job_status (JobStatus):
        last_updated_by (str):
        num_samples (int):
        updated_at (datetime.datetime):
        winner (bool):
        average_bleu (Union[None, Unset, float]):
        average_cost (Union[None, Unset, float]):
        average_hallucination (Union[None, Unset, float]):
        average_latency (Union[None, Unset, float]):
        average_rouge (Union[None, Unset, float]):
        dataset_hash (Union[None, Unset, str]):
        dataset_id (Union[None, Unset, str]):
        hallucination_severity (Union[Unset, int]):  Default: 0.
        metrics (Union[Unset, GetPromptRunMetrics]):
        model_alias (Union[None, Unset, str]):
        name (Union[None, Unset, str]):
        project_id (Union[None, Unset, str]):
        prompt_customized_scorers_configuration (Union[None, Unset,
            list[Union['CustomizedAgenticWorkflowSuccessGPTScorer', 'CustomizedChunkAttributionUtilizationGPTScorer',
            'CustomizedCompletenessGPTScorer', 'CustomizedFactualityGPTScorer', 'CustomizedGroundTruthAdherenceGPTScorer',
            'CustomizedGroundednessGPTScorer', 'CustomizedInstructionAdherenceGPTScorer',
            'CustomizedToolErrorRateGPTScorer', 'CustomizedToolSelectionQualityGPTScorer']]]):
        prompt_generated_scorers_configuration (Union[None, Unset, list[str]]):
        prompt_registered_scorers_configuration (Union[None, Unset, list['RegisteredScorer']]):
        prompt_scorers_configuration (Union[Unset, ScorersConfiguration]): Configure which scorers to enable for a
            particular prompt run.

            The keys here are sorted by their approximate execution time to execute the scorers that we anticipate will be
            the
            fastest first, and the slowest last.
        prompt_settings (Union['PromptRunSettings', None, Unset]):
        run_tags (Union[Unset, list['RunTagDB']]):
        task_type (Union[None, TaskType, Unset]):
        template_id (Union[None, Unset, str]):
        template_version (Union[None, Unset, int]):
        template_version_id (Union[None, Unset, str]):
        template_version_selected (Union[None, Unset, bool]):
        total_cost (Union[None, Unset, float]):
        total_responses (Union[Unset, int]):  Default: 0.
    """

    created_at: datetime.datetime
    created_by: str
    id: str
    job_id: str
    job_status: JobStatus
    last_updated_by: str
    num_samples: int
    updated_at: datetime.datetime
    winner: bool
    average_bleu: Union[None, Unset, float] = UNSET
    average_cost: Union[None, Unset, float] = UNSET
    average_hallucination: Union[None, Unset, float] = UNSET
    average_latency: Union[None, Unset, float] = UNSET
    average_rouge: Union[None, Unset, float] = UNSET
    dataset_hash: Union[None, Unset, str] = UNSET
    dataset_id: Union[None, Unset, str] = UNSET
    hallucination_severity: Union[Unset, int] = 0
    metrics: Union[Unset, "GetPromptRunMetrics"] = UNSET
    model_alias: Union[None, Unset, str] = UNSET
    name: Union[None, Unset, str] = UNSET
    project_id: Union[None, Unset, str] = UNSET
    prompt_customized_scorers_configuration: Union[
        None,
        Unset,
        list[
            Union[
                "CustomizedAgenticWorkflowSuccessGPTScorer",
                "CustomizedChunkAttributionUtilizationGPTScorer",
                "CustomizedCompletenessGPTScorer",
                "CustomizedFactualityGPTScorer",
                "CustomizedGroundTruthAdherenceGPTScorer",
                "CustomizedGroundednessGPTScorer",
                "CustomizedInstructionAdherenceGPTScorer",
                "CustomizedToolErrorRateGPTScorer",
                "CustomizedToolSelectionQualityGPTScorer",
            ]
        ],
    ] = UNSET
    prompt_generated_scorers_configuration: Union[None, Unset, list[str]] = UNSET
    prompt_registered_scorers_configuration: Union[None, Unset, list["RegisteredScorer"]] = UNSET
    prompt_scorers_configuration: Union[Unset, "ScorersConfiguration"] = UNSET
    prompt_settings: Union["PromptRunSettings", None, Unset] = UNSET
    run_tags: Union[Unset, list["RunTagDB"]] = UNSET
    task_type: Union[None, TaskType, Unset] = UNSET
    template_id: Union[None, Unset, str] = UNSET
    template_version: Union[None, Unset, int] = UNSET
    template_version_id: Union[None, Unset, str] = UNSET
    template_version_selected: Union[None, Unset, bool] = UNSET
    total_cost: Union[None, Unset, float] = UNSET
    total_responses: Union[Unset, int] = 0
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.customized_agentic_workflow_success_gpt_scorer import CustomizedAgenticWorkflowSuccessGPTScorer
        from ..models.customized_chunk_attribution_utilization_gpt_scorer import (
            CustomizedChunkAttributionUtilizationGPTScorer,
        )
        from ..models.customized_completeness_gpt_scorer import CustomizedCompletenessGPTScorer
        from ..models.customized_factuality_gpt_scorer import CustomizedFactualityGPTScorer
        from ..models.customized_ground_truth_adherence_gpt_scorer import CustomizedGroundTruthAdherenceGPTScorer
        from ..models.customized_groundedness_gpt_scorer import CustomizedGroundednessGPTScorer
        from ..models.customized_instruction_adherence_gpt_scorer import CustomizedInstructionAdherenceGPTScorer
        from ..models.customized_tool_selection_quality_gpt_scorer import CustomizedToolSelectionQualityGPTScorer
        from ..models.prompt_run_settings import PromptRunSettings

        created_at = self.created_at.isoformat()

        created_by = self.created_by

        id = self.id

        job_id = self.job_id

        job_status = self.job_status.value

        last_updated_by = self.last_updated_by

        num_samples = self.num_samples

        updated_at = self.updated_at.isoformat()

        winner = self.winner

        average_bleu: Union[None, Unset, float]
        if isinstance(self.average_bleu, Unset):
            average_bleu = UNSET
        else:
            average_bleu = self.average_bleu

        average_cost: Union[None, Unset, float]
        if isinstance(self.average_cost, Unset):
            average_cost = UNSET
        else:
            average_cost = self.average_cost

        average_hallucination: Union[None, Unset, float]
        if isinstance(self.average_hallucination, Unset):
            average_hallucination = UNSET
        else:
            average_hallucination = self.average_hallucination

        average_latency: Union[None, Unset, float]
        if isinstance(self.average_latency, Unset):
            average_latency = UNSET
        else:
            average_latency = self.average_latency

        average_rouge: Union[None, Unset, float]
        if isinstance(self.average_rouge, Unset):
            average_rouge = UNSET
        else:
            average_rouge = self.average_rouge

        dataset_hash: Union[None, Unset, str]
        if isinstance(self.dataset_hash, Unset):
            dataset_hash = UNSET
        else:
            dataset_hash = self.dataset_hash

        dataset_id: Union[None, Unset, str]
        if isinstance(self.dataset_id, Unset):
            dataset_id = UNSET
        else:
            dataset_id = self.dataset_id

        hallucination_severity = self.hallucination_severity

        metrics: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.metrics, Unset):
            metrics = self.metrics.to_dict()

        model_alias: Union[None, Unset, str]
        if isinstance(self.model_alias, Unset):
            model_alias = UNSET
        else:
            model_alias = self.model_alias

        name: Union[None, Unset, str]
        if isinstance(self.name, Unset):
            name = UNSET
        else:
            name = self.name

        project_id: Union[None, Unset, str]
        if isinstance(self.project_id, Unset):
            project_id = UNSET
        else:
            project_id = self.project_id

        prompt_customized_scorers_configuration: Union[None, Unset, list[dict[str, Any]]]
        if isinstance(self.prompt_customized_scorers_configuration, Unset):
            prompt_customized_scorers_configuration = UNSET
        elif isinstance(self.prompt_customized_scorers_configuration, list):
            prompt_customized_scorers_configuration = []
            for (
                prompt_customized_scorers_configuration_type_0_item_data
            ) in self.prompt_customized_scorers_configuration:
                prompt_customized_scorers_configuration_type_0_item: dict[str, Any]
                if isinstance(
                    prompt_customized_scorers_configuration_type_0_item_data, CustomizedAgenticWorkflowSuccessGPTScorer
                ):
                    prompt_customized_scorers_configuration_type_0_item = (
                        prompt_customized_scorers_configuration_type_0_item_data.to_dict()
                    )
                elif isinstance(
                    prompt_customized_scorers_configuration_type_0_item_data,
                    CustomizedChunkAttributionUtilizationGPTScorer,
                ):
                    prompt_customized_scorers_configuration_type_0_item = (
                        prompt_customized_scorers_configuration_type_0_item_data.to_dict()
                    )
                elif isinstance(
                    prompt_customized_scorers_configuration_type_0_item_data, CustomizedCompletenessGPTScorer
                ):
                    prompt_customized_scorers_configuration_type_0_item = (
                        prompt_customized_scorers_configuration_type_0_item_data.to_dict()
                    )
                elif isinstance(
                    prompt_customized_scorers_configuration_type_0_item_data, CustomizedFactualityGPTScorer
                ):
                    prompt_customized_scorers_configuration_type_0_item = (
                        prompt_customized_scorers_configuration_type_0_item_data.to_dict()
                    )
                elif isinstance(
                    prompt_customized_scorers_configuration_type_0_item_data, CustomizedGroundednessGPTScorer
                ):
                    prompt_customized_scorers_configuration_type_0_item = (
                        prompt_customized_scorers_configuration_type_0_item_data.to_dict()
                    )
                elif isinstance(
                    prompt_customized_scorers_configuration_type_0_item_data, CustomizedInstructionAdherenceGPTScorer
                ):
                    prompt_customized_scorers_configuration_type_0_item = (
                        prompt_customized_scorers_configuration_type_0_item_data.to_dict()
                    )
                elif isinstance(
                    prompt_customized_scorers_configuration_type_0_item_data, CustomizedGroundTruthAdherenceGPTScorer
                ):
                    prompt_customized_scorers_configuration_type_0_item = (
                        prompt_customized_scorers_configuration_type_0_item_data.to_dict()
                    )
                elif isinstance(
                    prompt_customized_scorers_configuration_type_0_item_data, CustomizedToolSelectionQualityGPTScorer
                ):
                    prompt_customized_scorers_configuration_type_0_item = (
                        prompt_customized_scorers_configuration_type_0_item_data.to_dict()
                    )
                else:
                    prompt_customized_scorers_configuration_type_0_item = (
                        prompt_customized_scorers_configuration_type_0_item_data.to_dict()
                    )

                prompt_customized_scorers_configuration.append(prompt_customized_scorers_configuration_type_0_item)

        else:
            prompt_customized_scorers_configuration = self.prompt_customized_scorers_configuration

        prompt_generated_scorers_configuration: Union[None, Unset, list[str]]
        if isinstance(self.prompt_generated_scorers_configuration, Unset):
            prompt_generated_scorers_configuration = UNSET
        elif isinstance(self.prompt_generated_scorers_configuration, list):
            prompt_generated_scorers_configuration = self.prompt_generated_scorers_configuration

        else:
            prompt_generated_scorers_configuration = self.prompt_generated_scorers_configuration

        prompt_registered_scorers_configuration: Union[None, Unset, list[dict[str, Any]]]
        if isinstance(self.prompt_registered_scorers_configuration, Unset):
            prompt_registered_scorers_configuration = UNSET
        elif isinstance(self.prompt_registered_scorers_configuration, list):
            prompt_registered_scorers_configuration = []
            for (
                prompt_registered_scorers_configuration_type_0_item_data
            ) in self.prompt_registered_scorers_configuration:
                prompt_registered_scorers_configuration_type_0_item = (
                    prompt_registered_scorers_configuration_type_0_item_data.to_dict()
                )
                prompt_registered_scorers_configuration.append(prompt_registered_scorers_configuration_type_0_item)

        else:
            prompt_registered_scorers_configuration = self.prompt_registered_scorers_configuration

        prompt_scorers_configuration: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.prompt_scorers_configuration, Unset):
            prompt_scorers_configuration = self.prompt_scorers_configuration.to_dict()

        prompt_settings: Union[None, Unset, dict[str, Any]]
        if isinstance(self.prompt_settings, Unset):
            prompt_settings = UNSET
        elif isinstance(self.prompt_settings, PromptRunSettings):
            prompt_settings = self.prompt_settings.to_dict()
        else:
            prompt_settings = self.prompt_settings

        run_tags: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.run_tags, Unset):
            run_tags = []
            for run_tags_item_data in self.run_tags:
                run_tags_item = run_tags_item_data.to_dict()
                run_tags.append(run_tags_item)

        task_type: Union[None, Unset, int]
        if isinstance(self.task_type, Unset):
            task_type = UNSET
        elif isinstance(self.task_type, TaskType):
            task_type = self.task_type.value
        else:
            task_type = self.task_type

        template_id: Union[None, Unset, str]
        if isinstance(self.template_id, Unset):
            template_id = UNSET
        else:
            template_id = self.template_id

        template_version: Union[None, Unset, int]
        if isinstance(self.template_version, Unset):
            template_version = UNSET
        else:
            template_version = self.template_version

        template_version_id: Union[None, Unset, str]
        if isinstance(self.template_version_id, Unset):
            template_version_id = UNSET
        else:
            template_version_id = self.template_version_id

        template_version_selected: Union[None, Unset, bool]
        if isinstance(self.template_version_selected, Unset):
            template_version_selected = UNSET
        else:
            template_version_selected = self.template_version_selected

        total_cost: Union[None, Unset, float]
        if isinstance(self.total_cost, Unset):
            total_cost = UNSET
        else:
            total_cost = self.total_cost

        total_responses = self.total_responses

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "created_at": created_at,
                "created_by": created_by,
                "id": id,
                "job_id": job_id,
                "job_status": job_status,
                "last_updated_by": last_updated_by,
                "num_samples": num_samples,
                "updated_at": updated_at,
                "winner": winner,
            }
        )
        if average_bleu is not UNSET:
            field_dict["average_bleu"] = average_bleu
        if average_cost is not UNSET:
            field_dict["average_cost"] = average_cost
        if average_hallucination is not UNSET:
            field_dict["average_hallucination"] = average_hallucination
        if average_latency is not UNSET:
            field_dict["average_latency"] = average_latency
        if average_rouge is not UNSET:
            field_dict["average_rouge"] = average_rouge
        if dataset_hash is not UNSET:
            field_dict["dataset_hash"] = dataset_hash
        if dataset_id is not UNSET:
            field_dict["dataset_id"] = dataset_id
        if hallucination_severity is not UNSET:
            field_dict["hallucination_severity"] = hallucination_severity
        if metrics is not UNSET:
            field_dict["metrics"] = metrics
        if model_alias is not UNSET:
            field_dict["model_alias"] = model_alias
        if name is not UNSET:
            field_dict["name"] = name
        if project_id is not UNSET:
            field_dict["project_id"] = project_id
        if prompt_customized_scorers_configuration is not UNSET:
            field_dict["prompt_customized_scorers_configuration"] = prompt_customized_scorers_configuration
        if prompt_generated_scorers_configuration is not UNSET:
            field_dict["prompt_generated_scorers_configuration"] = prompt_generated_scorers_configuration
        if prompt_registered_scorers_configuration is not UNSET:
            field_dict["prompt_registered_scorers_configuration"] = prompt_registered_scorers_configuration
        if prompt_scorers_configuration is not UNSET:
            field_dict["prompt_scorers_configuration"] = prompt_scorers_configuration
        if prompt_settings is not UNSET:
            field_dict["prompt_settings"] = prompt_settings
        if run_tags is not UNSET:
            field_dict["run_tags"] = run_tags
        if task_type is not UNSET:
            field_dict["task_type"] = task_type
        if template_id is not UNSET:
            field_dict["template_id"] = template_id
        if template_version is not UNSET:
            field_dict["template_version"] = template_version
        if template_version_id is not UNSET:
            field_dict["template_version_id"] = template_version_id
        if template_version_selected is not UNSET:
            field_dict["template_version_selected"] = template_version_selected
        if total_cost is not UNSET:
            field_dict["total_cost"] = total_cost
        if total_responses is not UNSET:
            field_dict["total_responses"] = total_responses

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.customized_agentic_workflow_success_gpt_scorer import CustomizedAgenticWorkflowSuccessGPTScorer
        from ..models.customized_chunk_attribution_utilization_gpt_scorer import (
            CustomizedChunkAttributionUtilizationGPTScorer,
        )
        from ..models.customized_completeness_gpt_scorer import CustomizedCompletenessGPTScorer
        from ..models.customized_factuality_gpt_scorer import CustomizedFactualityGPTScorer
        from ..models.customized_ground_truth_adherence_gpt_scorer import CustomizedGroundTruthAdherenceGPTScorer
        from ..models.customized_groundedness_gpt_scorer import CustomizedGroundednessGPTScorer
        from ..models.customized_instruction_adherence_gpt_scorer import CustomizedInstructionAdherenceGPTScorer
        from ..models.customized_tool_error_rate_gpt_scorer import CustomizedToolErrorRateGPTScorer
        from ..models.customized_tool_selection_quality_gpt_scorer import CustomizedToolSelectionQualityGPTScorer
        from ..models.get_prompt_run_metrics import GetPromptRunMetrics
        from ..models.prompt_run_settings import PromptRunSettings
        from ..models.registered_scorer import RegisteredScorer
        from ..models.run_tag_db import RunTagDB
        from ..models.scorers_configuration import ScorersConfiguration

        d = src_dict.copy()
        created_at = isoparse(d.pop("created_at"))

        created_by = d.pop("created_by")

        id = d.pop("id")

        job_id = d.pop("job_id")

        job_status = JobStatus(d.pop("job_status"))

        last_updated_by = d.pop("last_updated_by")

        num_samples = d.pop("num_samples")

        updated_at = isoparse(d.pop("updated_at"))

        winner = d.pop("winner")

        def _parse_average_bleu(data: object) -> Union[None, Unset, float]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, float], data)

        average_bleu = _parse_average_bleu(d.pop("average_bleu", UNSET))

        def _parse_average_cost(data: object) -> Union[None, Unset, float]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, float], data)

        average_cost = _parse_average_cost(d.pop("average_cost", UNSET))

        def _parse_average_hallucination(data: object) -> Union[None, Unset, float]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, float], data)

        average_hallucination = _parse_average_hallucination(d.pop("average_hallucination", UNSET))

        def _parse_average_latency(data: object) -> Union[None, Unset, float]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, float], data)

        average_latency = _parse_average_latency(d.pop("average_latency", UNSET))

        def _parse_average_rouge(data: object) -> Union[None, Unset, float]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, float], data)

        average_rouge = _parse_average_rouge(d.pop("average_rouge", UNSET))

        def _parse_dataset_hash(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        dataset_hash = _parse_dataset_hash(d.pop("dataset_hash", UNSET))

        def _parse_dataset_id(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        dataset_id = _parse_dataset_id(d.pop("dataset_id", UNSET))

        hallucination_severity = d.pop("hallucination_severity", UNSET)

        _metrics = d.pop("metrics", UNSET)
        metrics: Union[Unset, GetPromptRunMetrics]
        if isinstance(_metrics, Unset):
            metrics = UNSET
        else:
            metrics = GetPromptRunMetrics.from_dict(_metrics)

        def _parse_model_alias(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        model_alias = _parse_model_alias(d.pop("model_alias", UNSET))

        def _parse_name(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        name = _parse_name(d.pop("name", UNSET))

        def _parse_project_id(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        project_id = _parse_project_id(d.pop("project_id", UNSET))

        def _parse_prompt_customized_scorers_configuration(
            data: object,
        ) -> Union[
            None,
            Unset,
            list[
                Union[
                    "CustomizedAgenticWorkflowSuccessGPTScorer",
                    "CustomizedChunkAttributionUtilizationGPTScorer",
                    "CustomizedCompletenessGPTScorer",
                    "CustomizedFactualityGPTScorer",
                    "CustomizedGroundTruthAdherenceGPTScorer",
                    "CustomizedGroundednessGPTScorer",
                    "CustomizedInstructionAdherenceGPTScorer",
                    "CustomizedToolErrorRateGPTScorer",
                    "CustomizedToolSelectionQualityGPTScorer",
                ]
            ],
        ]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                prompt_customized_scorers_configuration_type_0 = []
                _prompt_customized_scorers_configuration_type_0 = data
                for (
                    prompt_customized_scorers_configuration_type_0_item_data
                ) in _prompt_customized_scorers_configuration_type_0:

                    def _parse_prompt_customized_scorers_configuration_type_0_item(
                        data: object,
                    ) -> Union[
                        "CustomizedAgenticWorkflowSuccessGPTScorer",
                        "CustomizedChunkAttributionUtilizationGPTScorer",
                        "CustomizedCompletenessGPTScorer",
                        "CustomizedFactualityGPTScorer",
                        "CustomizedGroundTruthAdherenceGPTScorer",
                        "CustomizedGroundednessGPTScorer",
                        "CustomizedInstructionAdherenceGPTScorer",
                        "CustomizedToolErrorRateGPTScorer",
                        "CustomizedToolSelectionQualityGPTScorer",
                    ]:
                        try:
                            if not isinstance(data, dict):
                                raise TypeError()
                            prompt_customized_scorers_configuration_type_0_item_type_0 = (
                                CustomizedAgenticWorkflowSuccessGPTScorer.from_dict(data)
                            )

                            return prompt_customized_scorers_configuration_type_0_item_type_0
                        except:  # noqa: E722
                            pass
                        try:
                            if not isinstance(data, dict):
                                raise TypeError()
                            prompt_customized_scorers_configuration_type_0_item_type_1 = (
                                CustomizedChunkAttributionUtilizationGPTScorer.from_dict(data)
                            )

                            return prompt_customized_scorers_configuration_type_0_item_type_1
                        except:  # noqa: E722
                            pass
                        try:
                            if not isinstance(data, dict):
                                raise TypeError()
                            prompt_customized_scorers_configuration_type_0_item_type_2 = (
                                CustomizedCompletenessGPTScorer.from_dict(data)
                            )

                            return prompt_customized_scorers_configuration_type_0_item_type_2
                        except:  # noqa: E722
                            pass
                        try:
                            if not isinstance(data, dict):
                                raise TypeError()
                            prompt_customized_scorers_configuration_type_0_item_type_3 = (
                                CustomizedFactualityGPTScorer.from_dict(data)
                            )

                            return prompt_customized_scorers_configuration_type_0_item_type_3
                        except:  # noqa: E722
                            pass
                        try:
                            if not isinstance(data, dict):
                                raise TypeError()
                            prompt_customized_scorers_configuration_type_0_item_type_4 = (
                                CustomizedGroundednessGPTScorer.from_dict(data)
                            )

                            return prompt_customized_scorers_configuration_type_0_item_type_4
                        except:  # noqa: E722
                            pass
                        try:
                            if not isinstance(data, dict):
                                raise TypeError()
                            prompt_customized_scorers_configuration_type_0_item_type_5 = (
                                CustomizedInstructionAdherenceGPTScorer.from_dict(data)
                            )

                            return prompt_customized_scorers_configuration_type_0_item_type_5
                        except:  # noqa: E722
                            pass
                        try:
                            if not isinstance(data, dict):
                                raise TypeError()
                            prompt_customized_scorers_configuration_type_0_item_type_6 = (
                                CustomizedGroundTruthAdherenceGPTScorer.from_dict(data)
                            )

                            return prompt_customized_scorers_configuration_type_0_item_type_6
                        except:  # noqa: E722
                            pass
                        try:
                            if not isinstance(data, dict):
                                raise TypeError()
                            prompt_customized_scorers_configuration_type_0_item_type_7 = (
                                CustomizedToolSelectionQualityGPTScorer.from_dict(data)
                            )

                            return prompt_customized_scorers_configuration_type_0_item_type_7
                        except:  # noqa: E722
                            pass
                        if not isinstance(data, dict):
                            raise TypeError()
                        prompt_customized_scorers_configuration_type_0_item_type_8 = (
                            CustomizedToolErrorRateGPTScorer.from_dict(data)
                        )

                        return prompt_customized_scorers_configuration_type_0_item_type_8

                    prompt_customized_scorers_configuration_type_0_item = (
                        _parse_prompt_customized_scorers_configuration_type_0_item(
                            prompt_customized_scorers_configuration_type_0_item_data
                        )
                    )

                    prompt_customized_scorers_configuration_type_0.append(
                        prompt_customized_scorers_configuration_type_0_item
                    )

                return prompt_customized_scorers_configuration_type_0
            except:  # noqa: E722
                pass
            return cast(
                Union[
                    None,
                    Unset,
                    list[
                        Union[
                            "CustomizedAgenticWorkflowSuccessGPTScorer",
                            "CustomizedChunkAttributionUtilizationGPTScorer",
                            "CustomizedCompletenessGPTScorer",
                            "CustomizedFactualityGPTScorer",
                            "CustomizedGroundTruthAdherenceGPTScorer",
                            "CustomizedGroundednessGPTScorer",
                            "CustomizedInstructionAdherenceGPTScorer",
                            "CustomizedToolErrorRateGPTScorer",
                            "CustomizedToolSelectionQualityGPTScorer",
                        ]
                    ],
                ],
                data,
            )

        prompt_customized_scorers_configuration = _parse_prompt_customized_scorers_configuration(
            d.pop("prompt_customized_scorers_configuration", UNSET)
        )

        def _parse_prompt_generated_scorers_configuration(data: object) -> Union[None, Unset, list[str]]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                prompt_generated_scorers_configuration_type_0 = cast(list[str], data)

                return prompt_generated_scorers_configuration_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, list[str]], data)

        prompt_generated_scorers_configuration = _parse_prompt_generated_scorers_configuration(
            d.pop("prompt_generated_scorers_configuration", UNSET)
        )

        def _parse_prompt_registered_scorers_configuration(
            data: object,
        ) -> Union[None, Unset, list["RegisteredScorer"]]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                prompt_registered_scorers_configuration_type_0 = []
                _prompt_registered_scorers_configuration_type_0 = data
                for (
                    prompt_registered_scorers_configuration_type_0_item_data
                ) in _prompt_registered_scorers_configuration_type_0:
                    prompt_registered_scorers_configuration_type_0_item = RegisteredScorer.from_dict(
                        prompt_registered_scorers_configuration_type_0_item_data
                    )

                    prompt_registered_scorers_configuration_type_0.append(
                        prompt_registered_scorers_configuration_type_0_item
                    )

                return prompt_registered_scorers_configuration_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, list["RegisteredScorer"]], data)

        prompt_registered_scorers_configuration = _parse_prompt_registered_scorers_configuration(
            d.pop("prompt_registered_scorers_configuration", UNSET)
        )

        _prompt_scorers_configuration = d.pop("prompt_scorers_configuration", UNSET)
        prompt_scorers_configuration: Union[Unset, ScorersConfiguration]
        if isinstance(_prompt_scorers_configuration, Unset):
            prompt_scorers_configuration = UNSET
        else:
            prompt_scorers_configuration = ScorersConfiguration.from_dict(_prompt_scorers_configuration)

        def _parse_prompt_settings(data: object) -> Union["PromptRunSettings", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                prompt_settings_type_0 = PromptRunSettings.from_dict(data)

                return prompt_settings_type_0
            except:  # noqa: E722
                pass
            return cast(Union["PromptRunSettings", None, Unset], data)

        prompt_settings = _parse_prompt_settings(d.pop("prompt_settings", UNSET))

        run_tags = []
        _run_tags = d.pop("run_tags", UNSET)
        for run_tags_item_data in _run_tags or []:
            run_tags_item = RunTagDB.from_dict(run_tags_item_data)

            run_tags.append(run_tags_item)

        def _parse_task_type(data: object) -> Union[None, TaskType, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, int):
                    raise TypeError()
                task_type_type_0 = TaskType(data)

                return task_type_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, TaskType, Unset], data)

        task_type = _parse_task_type(d.pop("task_type", UNSET))

        def _parse_template_id(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        template_id = _parse_template_id(d.pop("template_id", UNSET))

        def _parse_template_version(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        template_version = _parse_template_version(d.pop("template_version", UNSET))

        def _parse_template_version_id(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        template_version_id = _parse_template_version_id(d.pop("template_version_id", UNSET))

        def _parse_template_version_selected(data: object) -> Union[None, Unset, bool]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, bool], data)

        template_version_selected = _parse_template_version_selected(d.pop("template_version_selected", UNSET))

        def _parse_total_cost(data: object) -> Union[None, Unset, float]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, float], data)

        total_cost = _parse_total_cost(d.pop("total_cost", UNSET))

        total_responses = d.pop("total_responses", UNSET)

        get_prompt_run = cls(
            created_at=created_at,
            created_by=created_by,
            id=id,
            job_id=job_id,
            job_status=job_status,
            last_updated_by=last_updated_by,
            num_samples=num_samples,
            updated_at=updated_at,
            winner=winner,
            average_bleu=average_bleu,
            average_cost=average_cost,
            average_hallucination=average_hallucination,
            average_latency=average_latency,
            average_rouge=average_rouge,
            dataset_hash=dataset_hash,
            dataset_id=dataset_id,
            hallucination_severity=hallucination_severity,
            metrics=metrics,
            model_alias=model_alias,
            name=name,
            project_id=project_id,
            prompt_customized_scorers_configuration=prompt_customized_scorers_configuration,
            prompt_generated_scorers_configuration=prompt_generated_scorers_configuration,
            prompt_registered_scorers_configuration=prompt_registered_scorers_configuration,
            prompt_scorers_configuration=prompt_scorers_configuration,
            prompt_settings=prompt_settings,
            run_tags=run_tags,
            task_type=task_type,
            template_id=template_id,
            template_version=template_version,
            template_version_id=template_version_id,
            template_version_selected=template_version_selected,
            total_cost=total_cost,
            total_responses=total_responses,
        )

        get_prompt_run.additional_properties = d
        return get_prompt_run

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
