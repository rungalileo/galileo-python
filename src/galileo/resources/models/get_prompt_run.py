from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.job_status import JobStatus
from ..models.task_type import TaskType
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.customized_agentic_session_success_gpt_scorer import CustomizedAgenticSessionSuccessGPTScorer
    from ..models.customized_agentic_workflow_success_gpt_scorer import CustomizedAgenticWorkflowSuccessGPTScorer
    from ..models.customized_chunk_attribution_utilization_gpt_scorer import (
        CustomizedChunkAttributionUtilizationGPTScorer,
    )
    from ..models.customized_completeness_gpt_scorer import CustomizedCompletenessGPTScorer
    from ..models.customized_factuality_gpt_scorer import CustomizedFactualityGPTScorer
    from ..models.customized_ground_truth_adherence_gpt_scorer import CustomizedGroundTruthAdherenceGPTScorer
    from ..models.customized_groundedness_gpt_scorer import CustomizedGroundednessGPTScorer
    from ..models.customized_input_sexist_gpt_scorer import CustomizedInputSexistGPTScorer
    from ..models.customized_input_toxicity_gpt_scorer import CustomizedInputToxicityGPTScorer
    from ..models.customized_instruction_adherence_gpt_scorer import CustomizedInstructionAdherenceGPTScorer
    from ..models.customized_prompt_injection_gpt_scorer import CustomizedPromptInjectionGPTScorer
    from ..models.customized_sexist_gpt_scorer import CustomizedSexistGPTScorer
    from ..models.customized_tool_error_rate_gpt_scorer import CustomizedToolErrorRateGPTScorer
    from ..models.customized_tool_selection_quality_gpt_scorer import CustomizedToolSelectionQualityGPTScorer
    from ..models.customized_toxicity_gpt_scorer import CustomizedToxicityGPTScorer
    from ..models.fine_tuned_scorer import FineTunedScorer
    from ..models.get_prompt_run_metrics import GetPromptRunMetrics
    from ..models.prompt_run_settings_output import PromptRunSettingsOutput
    from ..models.registered_scorer import RegisteredScorer
    from ..models.run_tag_db import RunTagDB
    from ..models.scorers_configuration import ScorersConfiguration


T = TypeVar("T", bound="GetPromptRun")


@_attrs_define
class GetPromptRun:
    """
    Attributes:
        created_by (str):
        num_samples (int):
        winner (bool):
        id (str):
        created_at (datetime.datetime):
        updated_at (datetime.datetime):
        last_updated_by (str):
        job_id (str):
        job_status (JobStatus):
        hallucination_severity (int | Unset):  Default: 0.
        name (None | str | Unset):
        project_id (None | str | Unset):
        dataset_hash (None | str | Unset):
        dataset_version_id (None | str | Unset):
        task_type (None | TaskType | Unset):
        run_tags (list[RunTagDB] | Unset):
        model_alias (None | str | Unset):
        template_id (None | str | Unset):
        dataset_id (None | str | Unset):
        dataset_version_index (int | None | Unset):
        template_version_id (None | str | Unset):
        template_version (int | None | Unset):
        template_version_selected (bool | None | Unset):
        total_responses (int | Unset):  Default: 0.
        metrics (GetPromptRunMetrics | Unset):
        average_hallucination (float | None | Unset):
        average_bleu (float | None | Unset):
        average_rouge (float | None | Unset):
        average_cost (float | None | Unset):
        average_latency (float | None | Unset):
        total_cost (float | None | Unset):
        prompt_settings (None | PromptRunSettingsOutput | Unset):
        prompt_scorers_configuration (ScorersConfiguration | Unset): Configure which scorers to enable for a particular
            prompt run.

            The keys here are sorted by their approximate execution time to execute the scorers that we anticipate will be
            the
            fastest first, and the slowest last.
        prompt_registered_scorers_configuration (list[RegisteredScorer] | None | Unset):
        prompt_generated_scorers_configuration (list[str] | None | Unset):
        prompt_customized_scorers_configuration (list[CustomizedAgenticSessionSuccessGPTScorer |
            CustomizedAgenticWorkflowSuccessGPTScorer | CustomizedChunkAttributionUtilizationGPTScorer |
            CustomizedCompletenessGPTScorer | CustomizedFactualityGPTScorer | CustomizedGroundednessGPTScorer |
            CustomizedGroundTruthAdherenceGPTScorer | CustomizedInputSexistGPTScorer | CustomizedInputToxicityGPTScorer |
            CustomizedInstructionAdherenceGPTScorer | CustomizedPromptInjectionGPTScorer | CustomizedSexistGPTScorer |
            CustomizedToolErrorRateGPTScorer | CustomizedToolSelectionQualityGPTScorer | CustomizedToxicityGPTScorer] | None
            | Unset):
        prompt_finetuned_scorers_configuration (list[FineTunedScorer] | None | Unset):
    """

    created_by: str
    num_samples: int
    winner: bool
    id: str
    created_at: datetime.datetime
    updated_at: datetime.datetime
    last_updated_by: str
    job_id: str
    job_status: JobStatus
    hallucination_severity: int | Unset = 0
    name: None | str | Unset = UNSET
    project_id: None | str | Unset = UNSET
    dataset_hash: None | str | Unset = UNSET
    dataset_version_id: None | str | Unset = UNSET
    task_type: None | TaskType | Unset = UNSET
    run_tags: list[RunTagDB] | Unset = UNSET
    model_alias: None | str | Unset = UNSET
    template_id: None | str | Unset = UNSET
    dataset_id: None | str | Unset = UNSET
    dataset_version_index: int | None | Unset = UNSET
    template_version_id: None | str | Unset = UNSET
    template_version: int | None | Unset = UNSET
    template_version_selected: bool | None | Unset = UNSET
    total_responses: int | Unset = 0
    metrics: GetPromptRunMetrics | Unset = UNSET
    average_hallucination: float | None | Unset = UNSET
    average_bleu: float | None | Unset = UNSET
    average_rouge: float | None | Unset = UNSET
    average_cost: float | None | Unset = UNSET
    average_latency: float | None | Unset = UNSET
    total_cost: float | None | Unset = UNSET
    prompt_settings: None | PromptRunSettingsOutput | Unset = UNSET
    prompt_scorers_configuration: ScorersConfiguration | Unset = UNSET
    prompt_registered_scorers_configuration: list[RegisteredScorer] | None | Unset = UNSET
    prompt_generated_scorers_configuration: list[str] | None | Unset = UNSET
    prompt_customized_scorers_configuration: (
        list[
            CustomizedAgenticSessionSuccessGPTScorer
            | CustomizedAgenticWorkflowSuccessGPTScorer
            | CustomizedChunkAttributionUtilizationGPTScorer
            | CustomizedCompletenessGPTScorer
            | CustomizedFactualityGPTScorer
            | CustomizedGroundednessGPTScorer
            | CustomizedGroundTruthAdherenceGPTScorer
            | CustomizedInputSexistGPTScorer
            | CustomizedInputToxicityGPTScorer
            | CustomizedInstructionAdherenceGPTScorer
            | CustomizedPromptInjectionGPTScorer
            | CustomizedSexistGPTScorer
            | CustomizedToolErrorRateGPTScorer
            | CustomizedToolSelectionQualityGPTScorer
            | CustomizedToxicityGPTScorer
        ]
        | None
        | Unset
    ) = UNSET
    prompt_finetuned_scorers_configuration: list[FineTunedScorer] | None | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.customized_agentic_session_success_gpt_scorer import CustomizedAgenticSessionSuccessGPTScorer
        from ..models.customized_agentic_workflow_success_gpt_scorer import CustomizedAgenticWorkflowSuccessGPTScorer
        from ..models.customized_chunk_attribution_utilization_gpt_scorer import (
            CustomizedChunkAttributionUtilizationGPTScorer,
        )
        from ..models.customized_completeness_gpt_scorer import CustomizedCompletenessGPTScorer
        from ..models.customized_factuality_gpt_scorer import CustomizedFactualityGPTScorer
        from ..models.customized_ground_truth_adherence_gpt_scorer import CustomizedGroundTruthAdherenceGPTScorer
        from ..models.customized_groundedness_gpt_scorer import CustomizedGroundednessGPTScorer
        from ..models.customized_input_sexist_gpt_scorer import CustomizedInputSexistGPTScorer
        from ..models.customized_instruction_adherence_gpt_scorer import CustomizedInstructionAdherenceGPTScorer
        from ..models.customized_prompt_injection_gpt_scorer import CustomizedPromptInjectionGPTScorer
        from ..models.customized_sexist_gpt_scorer import CustomizedSexistGPTScorer
        from ..models.customized_tool_error_rate_gpt_scorer import CustomizedToolErrorRateGPTScorer
        from ..models.customized_tool_selection_quality_gpt_scorer import CustomizedToolSelectionQualityGPTScorer
        from ..models.customized_toxicity_gpt_scorer import CustomizedToxicityGPTScorer
        from ..models.prompt_run_settings_output import PromptRunSettingsOutput

        created_by = self.created_by

        num_samples = self.num_samples

        winner = self.winner

        id = self.id

        created_at = self.created_at.isoformat()

        updated_at = self.updated_at.isoformat()

        last_updated_by = self.last_updated_by

        job_id = self.job_id

        job_status = self.job_status.value

        hallucination_severity = self.hallucination_severity

        name: None | str | Unset
        if isinstance(self.name, Unset):
            name = UNSET
        else:
            name = self.name

        project_id: None | str | Unset
        if isinstance(self.project_id, Unset):
            project_id = UNSET
        else:
            project_id = self.project_id

        dataset_hash: None | str | Unset
        if isinstance(self.dataset_hash, Unset):
            dataset_hash = UNSET
        else:
            dataset_hash = self.dataset_hash

        dataset_version_id: None | str | Unset
        if isinstance(self.dataset_version_id, Unset):
            dataset_version_id = UNSET
        else:
            dataset_version_id = self.dataset_version_id

        task_type: int | None | Unset
        if isinstance(self.task_type, Unset):
            task_type = UNSET
        elif isinstance(self.task_type, TaskType):
            task_type = self.task_type.value
        else:
            task_type = self.task_type

        run_tags: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.run_tags, Unset):
            run_tags = []
            for run_tags_item_data in self.run_tags:
                run_tags_item = run_tags_item_data.to_dict()
                run_tags.append(run_tags_item)

        model_alias: None | str | Unset
        if isinstance(self.model_alias, Unset):
            model_alias = UNSET
        else:
            model_alias = self.model_alias

        template_id: None | str | Unset
        if isinstance(self.template_id, Unset):
            template_id = UNSET
        else:
            template_id = self.template_id

        dataset_id: None | str | Unset
        if isinstance(self.dataset_id, Unset):
            dataset_id = UNSET
        else:
            dataset_id = self.dataset_id

        dataset_version_index: int | None | Unset
        if isinstance(self.dataset_version_index, Unset):
            dataset_version_index = UNSET
        else:
            dataset_version_index = self.dataset_version_index

        template_version_id: None | str | Unset
        if isinstance(self.template_version_id, Unset):
            template_version_id = UNSET
        else:
            template_version_id = self.template_version_id

        template_version: int | None | Unset
        if isinstance(self.template_version, Unset):
            template_version = UNSET
        else:
            template_version = self.template_version

        template_version_selected: bool | None | Unset
        if isinstance(self.template_version_selected, Unset):
            template_version_selected = UNSET
        else:
            template_version_selected = self.template_version_selected

        total_responses = self.total_responses

        metrics: dict[str, Any] | Unset = UNSET
        if not isinstance(self.metrics, Unset):
            metrics = self.metrics.to_dict()

        average_hallucination: float | None | Unset
        if isinstance(self.average_hallucination, Unset):
            average_hallucination = UNSET
        else:
            average_hallucination = self.average_hallucination

        average_bleu: float | None | Unset
        if isinstance(self.average_bleu, Unset):
            average_bleu = UNSET
        else:
            average_bleu = self.average_bleu

        average_rouge: float | None | Unset
        if isinstance(self.average_rouge, Unset):
            average_rouge = UNSET
        else:
            average_rouge = self.average_rouge

        average_cost: float | None | Unset
        if isinstance(self.average_cost, Unset):
            average_cost = UNSET
        else:
            average_cost = self.average_cost

        average_latency: float | None | Unset
        if isinstance(self.average_latency, Unset):
            average_latency = UNSET
        else:
            average_latency = self.average_latency

        total_cost: float | None | Unset
        if isinstance(self.total_cost, Unset):
            total_cost = UNSET
        else:
            total_cost = self.total_cost

        prompt_settings: dict[str, Any] | None | Unset
        if isinstance(self.prompt_settings, Unset):
            prompt_settings = UNSET
        elif isinstance(self.prompt_settings, PromptRunSettingsOutput):
            prompt_settings = self.prompt_settings.to_dict()
        else:
            prompt_settings = self.prompt_settings

        prompt_scorers_configuration: dict[str, Any] | Unset = UNSET
        if not isinstance(self.prompt_scorers_configuration, Unset):
            prompt_scorers_configuration = self.prompt_scorers_configuration.to_dict()

        prompt_registered_scorers_configuration: list[dict[str, Any]] | None | Unset
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

        prompt_generated_scorers_configuration: list[str] | None | Unset
        if isinstance(self.prompt_generated_scorers_configuration, Unset):
            prompt_generated_scorers_configuration = UNSET
        elif isinstance(self.prompt_generated_scorers_configuration, list):
            prompt_generated_scorers_configuration = self.prompt_generated_scorers_configuration

        else:
            prompt_generated_scorers_configuration = self.prompt_generated_scorers_configuration

        prompt_customized_scorers_configuration: list[dict[str, Any]] | None | Unset
        if isinstance(self.prompt_customized_scorers_configuration, Unset):
            prompt_customized_scorers_configuration = UNSET
        elif isinstance(self.prompt_customized_scorers_configuration, list):
            prompt_customized_scorers_configuration = []
            for (
                prompt_customized_scorers_configuration_type_0_item_data
            ) in self.prompt_customized_scorers_configuration:
                prompt_customized_scorers_configuration_type_0_item: dict[str, Any]
                if isinstance(
                    prompt_customized_scorers_configuration_type_0_item_data, CustomizedAgenticSessionSuccessGPTScorer
                ):
                    prompt_customized_scorers_configuration_type_0_item = (
                        prompt_customized_scorers_configuration_type_0_item_data.to_dict()
                    )
                elif isinstance(
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
                    prompt_customized_scorers_configuration_type_0_item_data, CustomizedPromptInjectionGPTScorer
                ):
                    prompt_customized_scorers_configuration_type_0_item = (
                        prompt_customized_scorers_configuration_type_0_item_data.to_dict()
                    )
                elif isinstance(prompt_customized_scorers_configuration_type_0_item_data, CustomizedSexistGPTScorer):
                    prompt_customized_scorers_configuration_type_0_item = (
                        prompt_customized_scorers_configuration_type_0_item_data.to_dict()
                    )
                elif isinstance(
                    prompt_customized_scorers_configuration_type_0_item_data, CustomizedInputSexistGPTScorer
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
                elif isinstance(
                    prompt_customized_scorers_configuration_type_0_item_data, CustomizedToolErrorRateGPTScorer
                ):
                    prompt_customized_scorers_configuration_type_0_item = (
                        prompt_customized_scorers_configuration_type_0_item_data.to_dict()
                    )
                elif isinstance(prompt_customized_scorers_configuration_type_0_item_data, CustomizedToxicityGPTScorer):
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

        prompt_finetuned_scorers_configuration: list[dict[str, Any]] | None | Unset
        if isinstance(self.prompt_finetuned_scorers_configuration, Unset):
            prompt_finetuned_scorers_configuration = UNSET
        elif isinstance(self.prompt_finetuned_scorers_configuration, list):
            prompt_finetuned_scorers_configuration = []
            for prompt_finetuned_scorers_configuration_type_0_item_data in self.prompt_finetuned_scorers_configuration:
                prompt_finetuned_scorers_configuration_type_0_item = (
                    prompt_finetuned_scorers_configuration_type_0_item_data.to_dict()
                )
                prompt_finetuned_scorers_configuration.append(prompt_finetuned_scorers_configuration_type_0_item)

        else:
            prompt_finetuned_scorers_configuration = self.prompt_finetuned_scorers_configuration

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "created_by": created_by,
                "num_samples": num_samples,
                "winner": winner,
                "id": id,
                "created_at": created_at,
                "updated_at": updated_at,
                "last_updated_by": last_updated_by,
                "job_id": job_id,
                "job_status": job_status,
            }
        )
        if hallucination_severity is not UNSET:
            field_dict["hallucination_severity"] = hallucination_severity
        if name is not UNSET:
            field_dict["name"] = name
        if project_id is not UNSET:
            field_dict["project_id"] = project_id
        if dataset_hash is not UNSET:
            field_dict["dataset_hash"] = dataset_hash
        if dataset_version_id is not UNSET:
            field_dict["dataset_version_id"] = dataset_version_id
        if task_type is not UNSET:
            field_dict["task_type"] = task_type
        if run_tags is not UNSET:
            field_dict["run_tags"] = run_tags
        if model_alias is not UNSET:
            field_dict["model_alias"] = model_alias
        if template_id is not UNSET:
            field_dict["template_id"] = template_id
        if dataset_id is not UNSET:
            field_dict["dataset_id"] = dataset_id
        if dataset_version_index is not UNSET:
            field_dict["dataset_version_index"] = dataset_version_index
        if template_version_id is not UNSET:
            field_dict["template_version_id"] = template_version_id
        if template_version is not UNSET:
            field_dict["template_version"] = template_version
        if template_version_selected is not UNSET:
            field_dict["template_version_selected"] = template_version_selected
        if total_responses is not UNSET:
            field_dict["total_responses"] = total_responses
        if metrics is not UNSET:
            field_dict["metrics"] = metrics
        if average_hallucination is not UNSET:
            field_dict["average_hallucination"] = average_hallucination
        if average_bleu is not UNSET:
            field_dict["average_bleu"] = average_bleu
        if average_rouge is not UNSET:
            field_dict["average_rouge"] = average_rouge
        if average_cost is not UNSET:
            field_dict["average_cost"] = average_cost
        if average_latency is not UNSET:
            field_dict["average_latency"] = average_latency
        if total_cost is not UNSET:
            field_dict["total_cost"] = total_cost
        if prompt_settings is not UNSET:
            field_dict["prompt_settings"] = prompt_settings
        if prompt_scorers_configuration is not UNSET:
            field_dict["prompt_scorers_configuration"] = prompt_scorers_configuration
        if prompt_registered_scorers_configuration is not UNSET:
            field_dict["prompt_registered_scorers_configuration"] = prompt_registered_scorers_configuration
        if prompt_generated_scorers_configuration is not UNSET:
            field_dict["prompt_generated_scorers_configuration"] = prompt_generated_scorers_configuration
        if prompt_customized_scorers_configuration is not UNSET:
            field_dict["prompt_customized_scorers_configuration"] = prompt_customized_scorers_configuration
        if prompt_finetuned_scorers_configuration is not UNSET:
            field_dict["prompt_finetuned_scorers_configuration"] = prompt_finetuned_scorers_configuration

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.customized_agentic_session_success_gpt_scorer import CustomizedAgenticSessionSuccessGPTScorer
        from ..models.customized_agentic_workflow_success_gpt_scorer import CustomizedAgenticWorkflowSuccessGPTScorer
        from ..models.customized_chunk_attribution_utilization_gpt_scorer import (
            CustomizedChunkAttributionUtilizationGPTScorer,
        )
        from ..models.customized_completeness_gpt_scorer import CustomizedCompletenessGPTScorer
        from ..models.customized_factuality_gpt_scorer import CustomizedFactualityGPTScorer
        from ..models.customized_ground_truth_adherence_gpt_scorer import CustomizedGroundTruthAdherenceGPTScorer
        from ..models.customized_groundedness_gpt_scorer import CustomizedGroundednessGPTScorer
        from ..models.customized_input_sexist_gpt_scorer import CustomizedInputSexistGPTScorer
        from ..models.customized_input_toxicity_gpt_scorer import CustomizedInputToxicityGPTScorer
        from ..models.customized_instruction_adherence_gpt_scorer import CustomizedInstructionAdherenceGPTScorer
        from ..models.customized_prompt_injection_gpt_scorer import CustomizedPromptInjectionGPTScorer
        from ..models.customized_sexist_gpt_scorer import CustomizedSexistGPTScorer
        from ..models.customized_tool_error_rate_gpt_scorer import CustomizedToolErrorRateGPTScorer
        from ..models.customized_tool_selection_quality_gpt_scorer import CustomizedToolSelectionQualityGPTScorer
        from ..models.customized_toxicity_gpt_scorer import CustomizedToxicityGPTScorer
        from ..models.fine_tuned_scorer import FineTunedScorer
        from ..models.get_prompt_run_metrics import GetPromptRunMetrics
        from ..models.prompt_run_settings_output import PromptRunSettingsOutput
        from ..models.registered_scorer import RegisteredScorer
        from ..models.run_tag_db import RunTagDB
        from ..models.scorers_configuration import ScorersConfiguration

        d = dict(src_dict)
        created_by = d.pop("created_by")

        num_samples = d.pop("num_samples")

        winner = d.pop("winner")

        id = d.pop("id")

        created_at = isoparse(d.pop("created_at"))

        updated_at = isoparse(d.pop("updated_at"))

        last_updated_by = d.pop("last_updated_by")

        job_id = d.pop("job_id")

        job_status = JobStatus(d.pop("job_status"))

        hallucination_severity = d.pop("hallucination_severity", UNSET)

        def _parse_name(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        name = _parse_name(d.pop("name", UNSET))

        def _parse_project_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        project_id = _parse_project_id(d.pop("project_id", UNSET))

        def _parse_dataset_hash(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        dataset_hash = _parse_dataset_hash(d.pop("dataset_hash", UNSET))

        def _parse_dataset_version_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        dataset_version_id = _parse_dataset_version_id(d.pop("dataset_version_id", UNSET))

        def _parse_task_type(data: object) -> None | TaskType | Unset:
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
            return cast(None | TaskType | Unset, data)

        task_type = _parse_task_type(d.pop("task_type", UNSET))

        _run_tags = d.pop("run_tags", UNSET)
        run_tags: list[RunTagDB] | Unset = UNSET
        if _run_tags is not UNSET:
            run_tags = []
            for run_tags_item_data in _run_tags:
                run_tags_item = RunTagDB.from_dict(run_tags_item_data)

                run_tags.append(run_tags_item)

        def _parse_model_alias(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        model_alias = _parse_model_alias(d.pop("model_alias", UNSET))

        def _parse_template_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        template_id = _parse_template_id(d.pop("template_id", UNSET))

        def _parse_dataset_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        dataset_id = _parse_dataset_id(d.pop("dataset_id", UNSET))

        def _parse_dataset_version_index(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        dataset_version_index = _parse_dataset_version_index(d.pop("dataset_version_index", UNSET))

        def _parse_template_version_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        template_version_id = _parse_template_version_id(d.pop("template_version_id", UNSET))

        def _parse_template_version(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        template_version = _parse_template_version(d.pop("template_version", UNSET))

        def _parse_template_version_selected(data: object) -> bool | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(bool | None | Unset, data)

        template_version_selected = _parse_template_version_selected(d.pop("template_version_selected", UNSET))

        total_responses = d.pop("total_responses", UNSET)

        _metrics = d.pop("metrics", UNSET)
        metrics: GetPromptRunMetrics | Unset
        if isinstance(_metrics, Unset):
            metrics = UNSET
        else:
            metrics = GetPromptRunMetrics.from_dict(_metrics)

        def _parse_average_hallucination(data: object) -> float | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(float | None | Unset, data)

        average_hallucination = _parse_average_hallucination(d.pop("average_hallucination", UNSET))

        def _parse_average_bleu(data: object) -> float | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(float | None | Unset, data)

        average_bleu = _parse_average_bleu(d.pop("average_bleu", UNSET))

        def _parse_average_rouge(data: object) -> float | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(float | None | Unset, data)

        average_rouge = _parse_average_rouge(d.pop("average_rouge", UNSET))

        def _parse_average_cost(data: object) -> float | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(float | None | Unset, data)

        average_cost = _parse_average_cost(d.pop("average_cost", UNSET))

        def _parse_average_latency(data: object) -> float | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(float | None | Unset, data)

        average_latency = _parse_average_latency(d.pop("average_latency", UNSET))

        def _parse_total_cost(data: object) -> float | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(float | None | Unset, data)

        total_cost = _parse_total_cost(d.pop("total_cost", UNSET))

        def _parse_prompt_settings(data: object) -> None | PromptRunSettingsOutput | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                prompt_settings_type_0 = PromptRunSettingsOutput.from_dict(data)

                return prompt_settings_type_0
            except:  # noqa: E722
                pass
            return cast(None | PromptRunSettingsOutput | Unset, data)

        prompt_settings = _parse_prompt_settings(d.pop("prompt_settings", UNSET))

        _prompt_scorers_configuration = d.pop("prompt_scorers_configuration", UNSET)
        prompt_scorers_configuration: ScorersConfiguration | Unset
        if isinstance(_prompt_scorers_configuration, Unset):
            prompt_scorers_configuration = UNSET
        else:
            prompt_scorers_configuration = ScorersConfiguration.from_dict(_prompt_scorers_configuration)

        def _parse_prompt_registered_scorers_configuration(data: object) -> list[RegisteredScorer] | None | Unset:
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
            return cast(list[RegisteredScorer] | None | Unset, data)

        prompt_registered_scorers_configuration = _parse_prompt_registered_scorers_configuration(
            d.pop("prompt_registered_scorers_configuration", UNSET)
        )

        def _parse_prompt_generated_scorers_configuration(data: object) -> list[str] | None | Unset:
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
            return cast(list[str] | None | Unset, data)

        prompt_generated_scorers_configuration = _parse_prompt_generated_scorers_configuration(
            d.pop("prompt_generated_scorers_configuration", UNSET)
        )

        def _parse_prompt_customized_scorers_configuration(
            data: object,
        ) -> (
            list[
                CustomizedAgenticSessionSuccessGPTScorer
                | CustomizedAgenticWorkflowSuccessGPTScorer
                | CustomizedChunkAttributionUtilizationGPTScorer
                | CustomizedCompletenessGPTScorer
                | CustomizedFactualityGPTScorer
                | CustomizedGroundednessGPTScorer
                | CustomizedGroundTruthAdherenceGPTScorer
                | CustomizedInputSexistGPTScorer
                | CustomizedInputToxicityGPTScorer
                | CustomizedInstructionAdherenceGPTScorer
                | CustomizedPromptInjectionGPTScorer
                | CustomizedSexistGPTScorer
                | CustomizedToolErrorRateGPTScorer
                | CustomizedToolSelectionQualityGPTScorer
                | CustomizedToxicityGPTScorer
            ]
            | None
            | Unset
        ):
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
                    ) -> (
                        CustomizedAgenticSessionSuccessGPTScorer
                        | CustomizedAgenticWorkflowSuccessGPTScorer
                        | CustomizedChunkAttributionUtilizationGPTScorer
                        | CustomizedCompletenessGPTScorer
                        | CustomizedFactualityGPTScorer
                        | CustomizedGroundednessGPTScorer
                        | CustomizedGroundTruthAdherenceGPTScorer
                        | CustomizedInputSexistGPTScorer
                        | CustomizedInputToxicityGPTScorer
                        | CustomizedInstructionAdherenceGPTScorer
                        | CustomizedPromptInjectionGPTScorer
                        | CustomizedSexistGPTScorer
                        | CustomizedToolErrorRateGPTScorer
                        | CustomizedToolSelectionQualityGPTScorer
                        | CustomizedToxicityGPTScorer
                    ):
                        try:
                            if not isinstance(data, dict):
                                raise TypeError()
                            prompt_customized_scorers_configuration_type_0_item_type_0 = (
                                CustomizedAgenticSessionSuccessGPTScorer.from_dict(data)
                            )

                            return prompt_customized_scorers_configuration_type_0_item_type_0
                        except:  # noqa: E722
                            pass
                        try:
                            if not isinstance(data, dict):
                                raise TypeError()
                            prompt_customized_scorers_configuration_type_0_item_type_1 = (
                                CustomizedAgenticWorkflowSuccessGPTScorer.from_dict(data)
                            )

                            return prompt_customized_scorers_configuration_type_0_item_type_1
                        except:  # noqa: E722
                            pass
                        try:
                            if not isinstance(data, dict):
                                raise TypeError()
                            prompt_customized_scorers_configuration_type_0_item_type_2 = (
                                CustomizedChunkAttributionUtilizationGPTScorer.from_dict(data)
                            )

                            return prompt_customized_scorers_configuration_type_0_item_type_2
                        except:  # noqa: E722
                            pass
                        try:
                            if not isinstance(data, dict):
                                raise TypeError()
                            prompt_customized_scorers_configuration_type_0_item_type_3 = (
                                CustomizedCompletenessGPTScorer.from_dict(data)
                            )

                            return prompt_customized_scorers_configuration_type_0_item_type_3
                        except:  # noqa: E722
                            pass
                        try:
                            if not isinstance(data, dict):
                                raise TypeError()
                            prompt_customized_scorers_configuration_type_0_item_type_4 = (
                                CustomizedFactualityGPTScorer.from_dict(data)
                            )

                            return prompt_customized_scorers_configuration_type_0_item_type_4
                        except:  # noqa: E722
                            pass
                        try:
                            if not isinstance(data, dict):
                                raise TypeError()
                            prompt_customized_scorers_configuration_type_0_item_type_5 = (
                                CustomizedGroundednessGPTScorer.from_dict(data)
                            )

                            return prompt_customized_scorers_configuration_type_0_item_type_5
                        except:  # noqa: E722
                            pass
                        try:
                            if not isinstance(data, dict):
                                raise TypeError()
                            prompt_customized_scorers_configuration_type_0_item_type_6 = (
                                CustomizedInstructionAdherenceGPTScorer.from_dict(data)
                            )

                            return prompt_customized_scorers_configuration_type_0_item_type_6
                        except:  # noqa: E722
                            pass
                        try:
                            if not isinstance(data, dict):
                                raise TypeError()
                            prompt_customized_scorers_configuration_type_0_item_type_7 = (
                                CustomizedGroundTruthAdherenceGPTScorer.from_dict(data)
                            )

                            return prompt_customized_scorers_configuration_type_0_item_type_7
                        except:  # noqa: E722
                            pass
                        try:
                            if not isinstance(data, dict):
                                raise TypeError()
                            prompt_customized_scorers_configuration_type_0_item_type_8 = (
                                CustomizedPromptInjectionGPTScorer.from_dict(data)
                            )

                            return prompt_customized_scorers_configuration_type_0_item_type_8
                        except:  # noqa: E722
                            pass
                        try:
                            if not isinstance(data, dict):
                                raise TypeError()
                            prompt_customized_scorers_configuration_type_0_item_type_9 = (
                                CustomizedSexistGPTScorer.from_dict(data)
                            )

                            return prompt_customized_scorers_configuration_type_0_item_type_9
                        except:  # noqa: E722
                            pass
                        try:
                            if not isinstance(data, dict):
                                raise TypeError()
                            prompt_customized_scorers_configuration_type_0_item_type_10 = (
                                CustomizedInputSexistGPTScorer.from_dict(data)
                            )

                            return prompt_customized_scorers_configuration_type_0_item_type_10
                        except:  # noqa: E722
                            pass
                        try:
                            if not isinstance(data, dict):
                                raise TypeError()
                            prompt_customized_scorers_configuration_type_0_item_type_11 = (
                                CustomizedToolSelectionQualityGPTScorer.from_dict(data)
                            )

                            return prompt_customized_scorers_configuration_type_0_item_type_11
                        except:  # noqa: E722
                            pass
                        try:
                            if not isinstance(data, dict):
                                raise TypeError()
                            prompt_customized_scorers_configuration_type_0_item_type_12 = (
                                CustomizedToolErrorRateGPTScorer.from_dict(data)
                            )

                            return prompt_customized_scorers_configuration_type_0_item_type_12
                        except:  # noqa: E722
                            pass
                        try:
                            if not isinstance(data, dict):
                                raise TypeError()
                            prompt_customized_scorers_configuration_type_0_item_type_13 = (
                                CustomizedToxicityGPTScorer.from_dict(data)
                            )

                            return prompt_customized_scorers_configuration_type_0_item_type_13
                        except:  # noqa: E722
                            pass
                        if not isinstance(data, dict):
                            raise TypeError()
                        prompt_customized_scorers_configuration_type_0_item_type_14 = (
                            CustomizedInputToxicityGPTScorer.from_dict(data)
                        )

                        return prompt_customized_scorers_configuration_type_0_item_type_14

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
                list[
                    CustomizedAgenticSessionSuccessGPTScorer
                    | CustomizedAgenticWorkflowSuccessGPTScorer
                    | CustomizedChunkAttributionUtilizationGPTScorer
                    | CustomizedCompletenessGPTScorer
                    | CustomizedFactualityGPTScorer
                    | CustomizedGroundednessGPTScorer
                    | CustomizedGroundTruthAdherenceGPTScorer
                    | CustomizedInputSexistGPTScorer
                    | CustomizedInputToxicityGPTScorer
                    | CustomizedInstructionAdherenceGPTScorer
                    | CustomizedPromptInjectionGPTScorer
                    | CustomizedSexistGPTScorer
                    | CustomizedToolErrorRateGPTScorer
                    | CustomizedToolSelectionQualityGPTScorer
                    | CustomizedToxicityGPTScorer
                ]
                | None
                | Unset,
                data,
            )

        prompt_customized_scorers_configuration = _parse_prompt_customized_scorers_configuration(
            d.pop("prompt_customized_scorers_configuration", UNSET)
        )

        def _parse_prompt_finetuned_scorers_configuration(data: object) -> list[FineTunedScorer] | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                prompt_finetuned_scorers_configuration_type_0 = []
                _prompt_finetuned_scorers_configuration_type_0 = data
                for (
                    prompt_finetuned_scorers_configuration_type_0_item_data
                ) in _prompt_finetuned_scorers_configuration_type_0:
                    prompt_finetuned_scorers_configuration_type_0_item = FineTunedScorer.from_dict(
                        prompt_finetuned_scorers_configuration_type_0_item_data
                    )

                    prompt_finetuned_scorers_configuration_type_0.append(
                        prompt_finetuned_scorers_configuration_type_0_item
                    )

                return prompt_finetuned_scorers_configuration_type_0
            except:  # noqa: E722
                pass
            return cast(list[FineTunedScorer] | None | Unset, data)

        prompt_finetuned_scorers_configuration = _parse_prompt_finetuned_scorers_configuration(
            d.pop("prompt_finetuned_scorers_configuration", UNSET)
        )

        get_prompt_run = cls(
            created_by=created_by,
            num_samples=num_samples,
            winner=winner,
            id=id,
            created_at=created_at,
            updated_at=updated_at,
            last_updated_by=last_updated_by,
            job_id=job_id,
            job_status=job_status,
            hallucination_severity=hallucination_severity,
            name=name,
            project_id=project_id,
            dataset_hash=dataset_hash,
            dataset_version_id=dataset_version_id,
            task_type=task_type,
            run_tags=run_tags,
            model_alias=model_alias,
            template_id=template_id,
            dataset_id=dataset_id,
            dataset_version_index=dataset_version_index,
            template_version_id=template_version_id,
            template_version=template_version,
            template_version_selected=template_version_selected,
            total_responses=total_responses,
            metrics=metrics,
            average_hallucination=average_hallucination,
            average_bleu=average_bleu,
            average_rouge=average_rouge,
            average_cost=average_cost,
            average_latency=average_latency,
            total_cost=total_cost,
            prompt_settings=prompt_settings,
            prompt_scorers_configuration=prompt_scorers_configuration,
            prompt_registered_scorers_configuration=prompt_registered_scorers_configuration,
            prompt_generated_scorers_configuration=prompt_generated_scorers_configuration,
            prompt_customized_scorers_configuration=prompt_customized_scorers_configuration,
            prompt_finetuned_scorers_configuration=prompt_finetuned_scorers_configuration,
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
