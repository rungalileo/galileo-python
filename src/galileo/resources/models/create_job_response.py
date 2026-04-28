from __future__ import annotations

from collections.abc import Mapping
from io import BytesIO
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.scorer_name import ScorerName
from ..models.task_type import TaskType
from ..types import UNSET, File, FileTypes, Unset

if TYPE_CHECKING:
    from ..models.agentic_session_success_scorer import AgenticSessionSuccessScorer
    from ..models.agentic_workflow_success_scorer import AgenticWorkflowSuccessScorer
    from ..models.base_scorer import BaseScorer
    from ..models.bleu_scorer import BleuScorer
    from ..models.chunk_attribution_utilization_scorer import ChunkAttributionUtilizationScorer
    from ..models.completeness_scorer import CompletenessScorer
    from ..models.context_adherence_scorer import ContextAdherenceScorer
    from ..models.context_relevance_scorer import ContextRelevanceScorer
    from ..models.correctness_scorer import CorrectnessScorer
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
    from ..models.ground_truth_adherence_scorer import GroundTruthAdherenceScorer
    from ..models.input_pii_scorer import InputPIIScorer
    from ..models.input_sexist_scorer import InputSexistScorer
    from ..models.input_tone_scorer import InputToneScorer
    from ..models.input_toxicity_scorer import InputToxicityScorer
    from ..models.instruction_adherence_scorer import InstructionAdherenceScorer
    from ..models.metric_critique_job_configuration import MetricCritiqueJobConfiguration
    from ..models.output_pii_scorer import OutputPIIScorer
    from ..models.output_sexist_scorer import OutputSexistScorer
    from ..models.output_tone_scorer import OutputToneScorer
    from ..models.output_toxicity_scorer import OutputToxicityScorer
    from ..models.prompt_injection_scorer import PromptInjectionScorer
    from ..models.prompt_optimization_configuration import PromptOptimizationConfiguration
    from ..models.prompt_perplexity_scorer import PromptPerplexityScorer
    from ..models.prompt_run_settings import PromptRunSettings
    from ..models.registered_scorer import RegisteredScorer
    from ..models.rouge_scorer import RougeScorer
    from ..models.scorer_config import ScorerConfig
    from ..models.scorers_configuration import ScorersConfiguration
    from ..models.segment_filter import SegmentFilter
    from ..models.task_resource_limits import TaskResourceLimits
    from ..models.tool_error_rate_scorer import ToolErrorRateScorer
    from ..models.tool_selection_quality_scorer import ToolSelectionQualityScorer
    from ..models.uncertainty_scorer import UncertaintyScorer


T = TypeVar("T", bound="CreateJobResponse")


@_attrs_define
class CreateJobResponse:
    """
    Attributes
    ----------
        project_id (str):
        run_id (str):
        message (str):
        link (str):
        resource_limits (None | TaskResourceLimits | Unset):
        job_id (None | str | Unset):
        job_name (str | Unset):  Default: 'default'.
        should_retry (bool | Unset):  Default: True.
        user_id (None | str | Unset):
        task_type (None | TaskType | Unset):
        labels (list[list[str]] | list[str] | Unset):
        ner_labels (list[str] | None | Unset):
        tasks (list[str] | None | Unset):
        non_inference_logged (bool | Unset):  Default: False.
        migration_name (None | str | Unset):
        xray (bool | Unset):  Default: True.
        process_existing_inference_runs (bool | Unset):  Default: False.
        feature_names (list[str] | None | Unset):
        prompt_dataset_id (None | str | Unset):
        dataset_id (None | str | Unset):
        dataset_version_index (int | None | Unset):
        prompt_template_version_id (None | str | Unset):
        monitor_batch_id (None | str | Unset):
        protect_trace_id (None | str | Unset):
        protect_scorer_payload (File | None | Unset):
        prompt_settings (None | PromptRunSettings | Unset):
        scorers (list[AgenticSessionSuccessScorer | AgenticWorkflowSuccessScorer | BleuScorer |
            ChunkAttributionUtilizationScorer | CompletenessScorer | ContextAdherenceScorer | ContextRelevanceScorer |
            CorrectnessScorer | GroundTruthAdherenceScorer | InputPIIScorer | InputSexistScorer | InputToneScorer |
            InputToxicityScorer | InstructionAdherenceScorer | OutputPIIScorer | OutputSexistScorer | OutputToneScorer |
            OutputToxicityScorer | PromptInjectionScorer | PromptPerplexityScorer | RougeScorer | ToolErrorRateScorer |
            ToolSelectionQualityScorer | UncertaintyScorer] | list[ScorerConfig] | None | Unset): For G2.0 we send all
            scorers as ScorerConfig, for G1.0 we send preset scorers  as GalileoScorer
        prompt_registered_scorers_configuration (list[RegisteredScorer] | None | Unset):
        prompt_generated_scorers_configuration (list[str] | None | Unset):
        prompt_finetuned_scorers_configuration (list[FineTunedScorer] | None | Unset):
        prompt_scorers_configuration (None | ScorersConfiguration | Unset):
        prompt_customized_scorers_configuration (list[CustomizedAgenticSessionSuccessGPTScorer |
            CustomizedAgenticWorkflowSuccessGPTScorer | CustomizedChunkAttributionUtilizationGPTScorer |
            CustomizedCompletenessGPTScorer | CustomizedFactualityGPTScorer | CustomizedGroundednessGPTScorer |
            CustomizedGroundTruthAdherenceGPTScorer | CustomizedInputSexistGPTScorer | CustomizedInputToxicityGPTScorer |
            CustomizedInstructionAdherenceGPTScorer | CustomizedPromptInjectionGPTScorer | CustomizedSexistGPTScorer |
            CustomizedToolErrorRateGPTScorer | CustomizedToolSelectionQualityGPTScorer | CustomizedToxicityGPTScorer] | None
            | Unset):
        prompt_scorer_settings (BaseScorer | None | Unset):
        scorer_config (None | ScorerConfig | Unset):
        sub_scorers (list[ScorerName] | Unset):
        luna_model (None | str | Unset):
        segment_filters (list[SegmentFilter] | None | Unset):
        prompt_optimization_configuration (None | PromptOptimizationConfiguration | Unset):
        epoch (int | Unset):  Default: 0.
        metric_critique_configuration (MetricCritiqueJobConfiguration | None | Unset):
        is_session (bool | None | Unset):
        upload_data_in_separate_task (bool | Unset):  Default: True.
        log_metric_computing_records (bool | Unset):  Default: True.
        stream_metrics (bool | Unset):  Default: False.
        multijudge_average_boolean_metrics (bool | Unset):  Default: False.
    """

    project_id: str
    run_id: str
    message: str
    link: str
    resource_limits: None | TaskResourceLimits | Unset = UNSET
    job_id: None | str | Unset = UNSET
    job_name: str | Unset = "default"
    should_retry: bool | Unset = True
    user_id: None | str | Unset = UNSET
    task_type: None | TaskType | Unset = UNSET
    labels: list[list[str]] | list[str] | Unset = UNSET
    ner_labels: list[str] | None | Unset = UNSET
    tasks: list[str] | None | Unset = UNSET
    non_inference_logged: bool | Unset = False
    migration_name: None | str | Unset = UNSET
    xray: bool | Unset = True
    process_existing_inference_runs: bool | Unset = False
    feature_names: list[str] | None | Unset = UNSET
    prompt_dataset_id: None | str | Unset = UNSET
    dataset_id: None | str | Unset = UNSET
    dataset_version_index: int | None | Unset = UNSET
    prompt_template_version_id: None | str | Unset = UNSET
    monitor_batch_id: None | str | Unset = UNSET
    protect_trace_id: None | str | Unset = UNSET
    protect_scorer_payload: File | None | Unset = UNSET
    prompt_settings: None | PromptRunSettings | Unset = UNSET
    scorers: (
        list[
            AgenticSessionSuccessScorer
            | AgenticWorkflowSuccessScorer
            | BleuScorer
            | ChunkAttributionUtilizationScorer
            | CompletenessScorer
            | ContextAdherenceScorer
            | ContextRelevanceScorer
            | CorrectnessScorer
            | GroundTruthAdherenceScorer
            | InputPIIScorer
            | InputSexistScorer
            | InputToneScorer
            | InputToxicityScorer
            | InstructionAdherenceScorer
            | OutputPIIScorer
            | OutputSexistScorer
            | OutputToneScorer
            | OutputToxicityScorer
            | PromptInjectionScorer
            | PromptPerplexityScorer
            | RougeScorer
            | ToolErrorRateScorer
            | ToolSelectionQualityScorer
            | UncertaintyScorer
        ]
        | list[ScorerConfig]
        | None
        | Unset
    ) = UNSET
    prompt_registered_scorers_configuration: list[RegisteredScorer] | None | Unset = UNSET
    prompt_generated_scorers_configuration: list[str] | None | Unset = UNSET
    prompt_finetuned_scorers_configuration: list[FineTunedScorer] | None | Unset = UNSET
    prompt_scorers_configuration: None | ScorersConfiguration | Unset = UNSET
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
    prompt_scorer_settings: BaseScorer | None | Unset = UNSET
    scorer_config: None | ScorerConfig | Unset = UNSET
    sub_scorers: list[ScorerName] | Unset = UNSET
    luna_model: None | str | Unset = UNSET
    segment_filters: list[SegmentFilter] | None | Unset = UNSET
    prompt_optimization_configuration: None | PromptOptimizationConfiguration | Unset = UNSET
    epoch: int | Unset = 0
    metric_critique_configuration: MetricCritiqueJobConfiguration | None | Unset = UNSET
    is_session: bool | None | Unset = UNSET
    upload_data_in_separate_task: bool | Unset = True
    log_metric_computing_records: bool | Unset = True
    stream_metrics: bool | Unset = False
    multijudge_average_boolean_metrics: bool | Unset = False
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.agentic_session_success_scorer import AgenticSessionSuccessScorer
        from ..models.agentic_workflow_success_scorer import AgenticWorkflowSuccessScorer
        from ..models.base_scorer import BaseScorer
        from ..models.bleu_scorer import BleuScorer
        from ..models.chunk_attribution_utilization_scorer import ChunkAttributionUtilizationScorer
        from ..models.completeness_scorer import CompletenessScorer
        from ..models.context_adherence_scorer import ContextAdherenceScorer
        from ..models.context_relevance_scorer import ContextRelevanceScorer
        from ..models.correctness_scorer import CorrectnessScorer
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
        from ..models.ground_truth_adherence_scorer import GroundTruthAdherenceScorer
        from ..models.input_pii_scorer import InputPIIScorer
        from ..models.input_sexist_scorer import InputSexistScorer
        from ..models.input_tone_scorer import InputToneScorer
        from ..models.input_toxicity_scorer import InputToxicityScorer
        from ..models.instruction_adherence_scorer import InstructionAdherenceScorer
        from ..models.metric_critique_job_configuration import MetricCritiqueJobConfiguration
        from ..models.output_pii_scorer import OutputPIIScorer
        from ..models.output_sexist_scorer import OutputSexistScorer
        from ..models.output_tone_scorer import OutputToneScorer
        from ..models.output_toxicity_scorer import OutputToxicityScorer
        from ..models.prompt_injection_scorer import PromptInjectionScorer
        from ..models.prompt_optimization_configuration import PromptOptimizationConfiguration
        from ..models.prompt_perplexity_scorer import PromptPerplexityScorer
        from ..models.prompt_run_settings import PromptRunSettings
        from ..models.rouge_scorer import RougeScorer
        from ..models.scorer_config import ScorerConfig
        from ..models.scorers_configuration import ScorersConfiguration
        from ..models.task_resource_limits import TaskResourceLimits
        from ..models.tool_error_rate_scorer import ToolErrorRateScorer
        from ..models.tool_selection_quality_scorer import ToolSelectionQualityScorer

        project_id = self.project_id

        run_id = self.run_id

        message = self.message

        link = self.link

        resource_limits: dict[str, Any] | None | Unset
        if isinstance(self.resource_limits, Unset):
            resource_limits = UNSET
        elif isinstance(self.resource_limits, TaskResourceLimits):
            resource_limits = self.resource_limits.to_dict()
        else:
            resource_limits = self.resource_limits

        job_id: None | str | Unset
        job_id = UNSET if isinstance(self.job_id, Unset) else self.job_id

        job_name = self.job_name

        should_retry = self.should_retry

        user_id: None | str | Unset
        user_id = UNSET if isinstance(self.user_id, Unset) else self.user_id

        task_type: int | None | Unset
        if isinstance(self.task_type, Unset):
            task_type = UNSET
        elif isinstance(self.task_type, TaskType):
            task_type = self.task_type.value
        else:
            task_type = self.task_type

        labels: list[list[str]] | list[str] | Unset
        if isinstance(self.labels, Unset):
            labels = UNSET
        elif isinstance(self.labels, list):
            labels = []
            for labels_type_0_item_data in self.labels:
                labels_type_0_item = labels_type_0_item_data

                labels.append(labels_type_0_item)

        else:
            labels = self.labels

        ner_labels: list[str] | None | Unset
        if isinstance(self.ner_labels, Unset):
            ner_labels = UNSET
        elif isinstance(self.ner_labels, list):
            ner_labels = self.ner_labels

        else:
            ner_labels = self.ner_labels

        tasks: list[str] | None | Unset
        if isinstance(self.tasks, Unset):
            tasks = UNSET
        elif isinstance(self.tasks, list):
            tasks = self.tasks

        else:
            tasks = self.tasks

        non_inference_logged = self.non_inference_logged

        migration_name: None | str | Unset
        migration_name = UNSET if isinstance(self.migration_name, Unset) else self.migration_name

        xray = self.xray

        process_existing_inference_runs = self.process_existing_inference_runs

        feature_names: list[str] | None | Unset
        if isinstance(self.feature_names, Unset):
            feature_names = UNSET
        elif isinstance(self.feature_names, list):
            feature_names = self.feature_names

        else:
            feature_names = self.feature_names

        prompt_dataset_id: None | str | Unset
        prompt_dataset_id = UNSET if isinstance(self.prompt_dataset_id, Unset) else self.prompt_dataset_id

        dataset_id: None | str | Unset
        dataset_id = UNSET if isinstance(self.dataset_id, Unset) else self.dataset_id

        dataset_version_index: int | None | Unset
        dataset_version_index = UNSET if isinstance(self.dataset_version_index, Unset) else self.dataset_version_index

        prompt_template_version_id: None | str | Unset
        if isinstance(self.prompt_template_version_id, Unset):
            prompt_template_version_id = UNSET
        else:
            prompt_template_version_id = self.prompt_template_version_id

        monitor_batch_id: None | str | Unset
        monitor_batch_id = UNSET if isinstance(self.monitor_batch_id, Unset) else self.monitor_batch_id

        protect_trace_id: None | str | Unset
        protect_trace_id = UNSET if isinstance(self.protect_trace_id, Unset) else self.protect_trace_id

        protect_scorer_payload: FileTypes | None | Unset
        if isinstance(self.protect_scorer_payload, Unset):
            protect_scorer_payload = UNSET
        elif isinstance(self.protect_scorer_payload, File):
            protect_scorer_payload = self.protect_scorer_payload.to_tuple()

        else:
            protect_scorer_payload = self.protect_scorer_payload

        prompt_settings: dict[str, Any] | None | Unset
        if isinstance(self.prompt_settings, Unset):
            prompt_settings = UNSET
        elif isinstance(self.prompt_settings, PromptRunSettings):
            prompt_settings = self.prompt_settings.to_dict()
        else:
            prompt_settings = self.prompt_settings

        scorers: list[dict[str, Any]] | None | Unset
        if isinstance(self.scorers, Unset):
            scorers = UNSET
        elif isinstance(self.scorers, list):
            scorers = []
            for scorers_type_0_item_data in self.scorers:
                scorers_type_0_item = scorers_type_0_item_data.to_dict()
                scorers.append(scorers_type_0_item)

        elif isinstance(self.scorers, list):
            scorers = []
            for scorers_type_1_item_data in self.scorers:
                scorers_type_1_item: dict[str, Any]
                if isinstance(
                    scorers_type_1_item_data,
                    AgenticWorkflowSuccessScorer
                    | AgenticSessionSuccessScorer
                    | BleuScorer
                    | ChunkAttributionUtilizationScorer
                    | (CompletenessScorer | ContextAdherenceScorer)
                    | ContextRelevanceScorer
                    | CorrectnessScorer
                    | (GroundTruthAdherenceScorer | InputPIIScorer | InputSexistScorer | InputToneScorer)
                    | (InputToxicityScorer | InstructionAdherenceScorer)
                    | OutputPIIScorer
                    | OutputSexistScorer
                    | (
                        OutputToneScorer
                        | OutputToxicityScorer
                        | PromptInjectionScorer
                        | PromptPerplexityScorer
                        | (RougeScorer | ToolErrorRateScorer)
                        | ToolSelectionQualityScorer
                    ),
                ):
                    scorers_type_1_item = scorers_type_1_item_data.to_dict()
                else:
                    scorers_type_1_item = scorers_type_1_item_data.to_dict()

                scorers.append(scorers_type_1_item)

        else:
            scorers = self.scorers

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

        prompt_scorers_configuration: dict[str, Any] | None | Unset
        if isinstance(self.prompt_scorers_configuration, Unset):
            prompt_scorers_configuration = UNSET
        elif isinstance(self.prompt_scorers_configuration, ScorersConfiguration):
            prompt_scorers_configuration = self.prompt_scorers_configuration.to_dict()
        else:
            prompt_scorers_configuration = self.prompt_scorers_configuration

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
                    prompt_customized_scorers_configuration_type_0_item_data,
                    CustomizedAgenticSessionSuccessGPTScorer
                    | CustomizedAgenticWorkflowSuccessGPTScorer
                    | CustomizedChunkAttributionUtilizationGPTScorer
                    | CustomizedCompletenessGPTScorer
                    | (CustomizedFactualityGPTScorer | CustomizedGroundednessGPTScorer)
                    | CustomizedInstructionAdherenceGPTScorer
                    | CustomizedGroundTruthAdherenceGPTScorer
                    | (
                        CustomizedPromptInjectionGPTScorer
                        | CustomizedSexistGPTScorer
                        | CustomizedInputSexistGPTScorer
                        | CustomizedToolSelectionQualityGPTScorer
                    )
                    | (CustomizedToolErrorRateGPTScorer | CustomizedToxicityGPTScorer),
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

        prompt_scorer_settings: dict[str, Any] | None | Unset
        if isinstance(self.prompt_scorer_settings, Unset):
            prompt_scorer_settings = UNSET
        elif isinstance(self.prompt_scorer_settings, BaseScorer):
            prompt_scorer_settings = self.prompt_scorer_settings.to_dict()
        else:
            prompt_scorer_settings = self.prompt_scorer_settings

        scorer_config: dict[str, Any] | None | Unset
        if isinstance(self.scorer_config, Unset):
            scorer_config = UNSET
        elif isinstance(self.scorer_config, ScorerConfig):
            scorer_config = self.scorer_config.to_dict()
        else:
            scorer_config = self.scorer_config

        sub_scorers: list[str] | Unset = UNSET
        if not isinstance(self.sub_scorers, Unset):
            sub_scorers = []
            for sub_scorers_item_data in self.sub_scorers:
                sub_scorers_item = sub_scorers_item_data.value
                sub_scorers.append(sub_scorers_item)

        luna_model: None | str | Unset
        luna_model = UNSET if isinstance(self.luna_model, Unset) else self.luna_model

        segment_filters: list[dict[str, Any]] | None | Unset
        if isinstance(self.segment_filters, Unset):
            segment_filters = UNSET
        elif isinstance(self.segment_filters, list):
            segment_filters = []
            for segment_filters_type_0_item_data in self.segment_filters:
                segment_filters_type_0_item = segment_filters_type_0_item_data.to_dict()
                segment_filters.append(segment_filters_type_0_item)

        else:
            segment_filters = self.segment_filters

        prompt_optimization_configuration: dict[str, Any] | None | Unset
        if isinstance(self.prompt_optimization_configuration, Unset):
            prompt_optimization_configuration = UNSET
        elif isinstance(self.prompt_optimization_configuration, PromptOptimizationConfiguration):
            prompt_optimization_configuration = self.prompt_optimization_configuration.to_dict()
        else:
            prompt_optimization_configuration = self.prompt_optimization_configuration

        epoch = self.epoch

        metric_critique_configuration: dict[str, Any] | None | Unset
        if isinstance(self.metric_critique_configuration, Unset):
            metric_critique_configuration = UNSET
        elif isinstance(self.metric_critique_configuration, MetricCritiqueJobConfiguration):
            metric_critique_configuration = self.metric_critique_configuration.to_dict()
        else:
            metric_critique_configuration = self.metric_critique_configuration

        is_session: bool | None | Unset
        is_session = UNSET if isinstance(self.is_session, Unset) else self.is_session

        upload_data_in_separate_task = self.upload_data_in_separate_task

        log_metric_computing_records = self.log_metric_computing_records

        stream_metrics = self.stream_metrics

        multijudge_average_boolean_metrics = self.multijudge_average_boolean_metrics

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({"project_id": project_id, "run_id": run_id, "message": message, "link": link})
        if resource_limits is not UNSET:
            field_dict["resource_limits"] = resource_limits
        if job_id is not UNSET:
            field_dict["job_id"] = job_id
        if job_name is not UNSET:
            field_dict["job_name"] = job_name
        if should_retry is not UNSET:
            field_dict["should_retry"] = should_retry
        if user_id is not UNSET:
            field_dict["user_id"] = user_id
        if task_type is not UNSET:
            field_dict["task_type"] = task_type
        if labels is not UNSET:
            field_dict["labels"] = labels
        if ner_labels is not UNSET:
            field_dict["ner_labels"] = ner_labels
        if tasks is not UNSET:
            field_dict["tasks"] = tasks
        if non_inference_logged is not UNSET:
            field_dict["non_inference_logged"] = non_inference_logged
        if migration_name is not UNSET:
            field_dict["migration_name"] = migration_name
        if xray is not UNSET:
            field_dict["xray"] = xray
        if process_existing_inference_runs is not UNSET:
            field_dict["process_existing_inference_runs"] = process_existing_inference_runs
        if feature_names is not UNSET:
            field_dict["feature_names"] = feature_names
        if prompt_dataset_id is not UNSET:
            field_dict["prompt_dataset_id"] = prompt_dataset_id
        if dataset_id is not UNSET:
            field_dict["dataset_id"] = dataset_id
        if dataset_version_index is not UNSET:
            field_dict["dataset_version_index"] = dataset_version_index
        if prompt_template_version_id is not UNSET:
            field_dict["prompt_template_version_id"] = prompt_template_version_id
        if monitor_batch_id is not UNSET:
            field_dict["monitor_batch_id"] = monitor_batch_id
        if protect_trace_id is not UNSET:
            field_dict["protect_trace_id"] = protect_trace_id
        if protect_scorer_payload is not UNSET:
            field_dict["protect_scorer_payload"] = protect_scorer_payload
        if prompt_settings is not UNSET:
            field_dict["prompt_settings"] = prompt_settings
        if scorers is not UNSET:
            field_dict["scorers"] = scorers
        if prompt_registered_scorers_configuration is not UNSET:
            field_dict["prompt_registered_scorers_configuration"] = prompt_registered_scorers_configuration
        if prompt_generated_scorers_configuration is not UNSET:
            field_dict["prompt_generated_scorers_configuration"] = prompt_generated_scorers_configuration
        if prompt_finetuned_scorers_configuration is not UNSET:
            field_dict["prompt_finetuned_scorers_configuration"] = prompt_finetuned_scorers_configuration
        if prompt_scorers_configuration is not UNSET:
            field_dict["prompt_scorers_configuration"] = prompt_scorers_configuration
        if prompt_customized_scorers_configuration is not UNSET:
            field_dict["prompt_customized_scorers_configuration"] = prompt_customized_scorers_configuration
        if prompt_scorer_settings is not UNSET:
            field_dict["prompt_scorer_settings"] = prompt_scorer_settings
        if scorer_config is not UNSET:
            field_dict["scorer_config"] = scorer_config
        if sub_scorers is not UNSET:
            field_dict["sub_scorers"] = sub_scorers
        if luna_model is not UNSET:
            field_dict["luna_model"] = luna_model
        if segment_filters is not UNSET:
            field_dict["segment_filters"] = segment_filters
        if prompt_optimization_configuration is not UNSET:
            field_dict["prompt_optimization_configuration"] = prompt_optimization_configuration
        if epoch is not UNSET:
            field_dict["epoch"] = epoch
        if metric_critique_configuration is not UNSET:
            field_dict["metric_critique_configuration"] = metric_critique_configuration
        if is_session is not UNSET:
            field_dict["is_session"] = is_session
        if upload_data_in_separate_task is not UNSET:
            field_dict["upload_data_in_separate_task"] = upload_data_in_separate_task
        if log_metric_computing_records is not UNSET:
            field_dict["log_metric_computing_records"] = log_metric_computing_records
        if stream_metrics is not UNSET:
            field_dict["stream_metrics"] = stream_metrics
        if multijudge_average_boolean_metrics is not UNSET:
            field_dict["multijudge_average_boolean_metrics"] = multijudge_average_boolean_metrics

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.agentic_session_success_scorer import AgenticSessionSuccessScorer
        from ..models.agentic_workflow_success_scorer import AgenticWorkflowSuccessScorer
        from ..models.base_scorer import BaseScorer
        from ..models.bleu_scorer import BleuScorer
        from ..models.chunk_attribution_utilization_scorer import ChunkAttributionUtilizationScorer
        from ..models.completeness_scorer import CompletenessScorer
        from ..models.context_adherence_scorer import ContextAdherenceScorer
        from ..models.context_relevance_scorer import ContextRelevanceScorer
        from ..models.correctness_scorer import CorrectnessScorer
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
        from ..models.ground_truth_adherence_scorer import GroundTruthAdherenceScorer
        from ..models.input_pii_scorer import InputPIIScorer
        from ..models.input_sexist_scorer import InputSexistScorer
        from ..models.input_tone_scorer import InputToneScorer
        from ..models.input_toxicity_scorer import InputToxicityScorer
        from ..models.instruction_adherence_scorer import InstructionAdherenceScorer
        from ..models.metric_critique_job_configuration import MetricCritiqueJobConfiguration
        from ..models.output_pii_scorer import OutputPIIScorer
        from ..models.output_sexist_scorer import OutputSexistScorer
        from ..models.output_tone_scorer import OutputToneScorer
        from ..models.output_toxicity_scorer import OutputToxicityScorer
        from ..models.prompt_injection_scorer import PromptInjectionScorer
        from ..models.prompt_optimization_configuration import PromptOptimizationConfiguration
        from ..models.prompt_perplexity_scorer import PromptPerplexityScorer
        from ..models.prompt_run_settings import PromptRunSettings
        from ..models.registered_scorer import RegisteredScorer
        from ..models.rouge_scorer import RougeScorer
        from ..models.scorer_config import ScorerConfig
        from ..models.scorers_configuration import ScorersConfiguration
        from ..models.segment_filter import SegmentFilter
        from ..models.task_resource_limits import TaskResourceLimits
        from ..models.tool_error_rate_scorer import ToolErrorRateScorer
        from ..models.tool_selection_quality_scorer import ToolSelectionQualityScorer
        from ..models.uncertainty_scorer import UncertaintyScorer

        d = dict(src_dict)
        project_id = d.pop("project_id")

        run_id = d.pop("run_id")

        message = d.pop("message")

        link = d.pop("link")

        def _parse_resource_limits(data: object) -> None | TaskResourceLimits | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                return TaskResourceLimits.from_dict(data)

            except:  # noqa: E722
                pass
            return cast(None | TaskResourceLimits | Unset, data)

        resource_limits = _parse_resource_limits(d.pop("resource_limits", UNSET))

        def _parse_job_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        job_id = _parse_job_id(d.pop("job_id", UNSET))

        job_name = d.pop("job_name", UNSET)

        should_retry = d.pop("should_retry", UNSET)

        def _parse_user_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        user_id = _parse_user_id(d.pop("user_id", UNSET))

        def _parse_task_type(data: object) -> None | TaskType | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, int):
                    raise TypeError()
                return TaskType(data)

            except:  # noqa: E722
                pass
            return cast(None | TaskType | Unset, data)

        task_type = _parse_task_type(d.pop("task_type", UNSET))

        def _parse_labels(data: object) -> list[list[str]] | list[str] | Unset:
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                labels_type_0 = []
                _labels_type_0 = data
                for labels_type_0_item_data in _labels_type_0:
                    labels_type_0_item = cast(list[str], labels_type_0_item_data)

                    labels_type_0.append(labels_type_0_item)

                return labels_type_0
            except:  # noqa: E722
                pass
            if not isinstance(data, list):
                raise TypeError()
            return cast(list[str], data)

        labels = _parse_labels(d.pop("labels", UNSET))

        def _parse_ner_labels(data: object) -> list[str] | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                return cast(list[str], data)

            except:  # noqa: E722
                pass
            return cast(list[str] | None | Unset, data)

        ner_labels = _parse_ner_labels(d.pop("ner_labels", UNSET))

        def _parse_tasks(data: object) -> list[str] | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                return cast(list[str], data)

            except:  # noqa: E722
                pass
            return cast(list[str] | None | Unset, data)

        tasks = _parse_tasks(d.pop("tasks", UNSET))

        non_inference_logged = d.pop("non_inference_logged", UNSET)

        def _parse_migration_name(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        migration_name = _parse_migration_name(d.pop("migration_name", UNSET))

        xray = d.pop("xray", UNSET)

        process_existing_inference_runs = d.pop("process_existing_inference_runs", UNSET)

        def _parse_feature_names(data: object) -> list[str] | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                return cast(list[str], data)

            except:  # noqa: E722
                pass
            return cast(list[str] | None | Unset, data)

        feature_names = _parse_feature_names(d.pop("feature_names", UNSET))

        def _parse_prompt_dataset_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        prompt_dataset_id = _parse_prompt_dataset_id(d.pop("prompt_dataset_id", UNSET))

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

        def _parse_prompt_template_version_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        prompt_template_version_id = _parse_prompt_template_version_id(d.pop("prompt_template_version_id", UNSET))

        def _parse_monitor_batch_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        monitor_batch_id = _parse_monitor_batch_id(d.pop("monitor_batch_id", UNSET))

        def _parse_protect_trace_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        protect_trace_id = _parse_protect_trace_id(d.pop("protect_trace_id", UNSET))

        def _parse_protect_scorer_payload(data: object) -> File | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, bytes):
                    raise TypeError()
                return File(payload=BytesIO(data))

            except:  # noqa: E722
                pass
            return cast(File | None | Unset, data)

        protect_scorer_payload = _parse_protect_scorer_payload(d.pop("protect_scorer_payload", UNSET))

        def _parse_prompt_settings(data: object) -> None | PromptRunSettings | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                return PromptRunSettings.from_dict(data)

            except:  # noqa: E722
                pass
            return cast(None | PromptRunSettings | Unset, data)

        prompt_settings = _parse_prompt_settings(d.pop("prompt_settings", UNSET))

        def _parse_scorers(
            data: object,
        ) -> (
            list[
                AgenticSessionSuccessScorer
                | AgenticWorkflowSuccessScorer
                | BleuScorer
                | ChunkAttributionUtilizationScorer
                | CompletenessScorer
                | ContextAdherenceScorer
                | ContextRelevanceScorer
                | CorrectnessScorer
                | GroundTruthAdherenceScorer
                | InputPIIScorer
                | InputSexistScorer
                | InputToneScorer
                | InputToxicityScorer
                | InstructionAdherenceScorer
                | OutputPIIScorer
                | OutputSexistScorer
                | OutputToneScorer
                | OutputToxicityScorer
                | PromptInjectionScorer
                | PromptPerplexityScorer
                | RougeScorer
                | ToolErrorRateScorer
                | ToolSelectionQualityScorer
                | UncertaintyScorer
            ]
            | list[ScorerConfig]
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
                scorers_type_0 = []
                _scorers_type_0 = data
                for scorers_type_0_item_data in _scorers_type_0:
                    scorers_type_0_item = ScorerConfig.from_dict(scorers_type_0_item_data)

                    scorers_type_0.append(scorers_type_0_item)

                return scorers_type_0
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, list):
                    raise TypeError()
                scorers_type_1 = []
                _scorers_type_1 = data
                for scorers_type_1_item_data in _scorers_type_1:

                    def _parse_scorers_type_1_item(
                        data: object,
                    ) -> (
                        AgenticSessionSuccessScorer
                        | AgenticWorkflowSuccessScorer
                        | BleuScorer
                        | ChunkAttributionUtilizationScorer
                        | CompletenessScorer
                        | ContextAdherenceScorer
                        | ContextRelevanceScorer
                        | CorrectnessScorer
                        | GroundTruthAdherenceScorer
                        | InputPIIScorer
                        | InputSexistScorer
                        | InputToneScorer
                        | InputToxicityScorer
                        | InstructionAdherenceScorer
                        | OutputPIIScorer
                        | OutputSexistScorer
                        | OutputToneScorer
                        | OutputToxicityScorer
                        | PromptInjectionScorer
                        | PromptPerplexityScorer
                        | RougeScorer
                        | ToolErrorRateScorer
                        | ToolSelectionQualityScorer
                        | UncertaintyScorer
                    ):
                        try:
                            if not isinstance(data, dict):
                                raise TypeError()
                            return AgenticWorkflowSuccessScorer.from_dict(data)

                        except:  # noqa: E722
                            pass
                        try:
                            if not isinstance(data, dict):
                                raise TypeError()
                            return AgenticSessionSuccessScorer.from_dict(data)

                        except:  # noqa: E722
                            pass
                        try:
                            if not isinstance(data, dict):
                                raise TypeError()
                            return BleuScorer.from_dict(data)

                        except:  # noqa: E722
                            pass
                        try:
                            if not isinstance(data, dict):
                                raise TypeError()
                            return ChunkAttributionUtilizationScorer.from_dict(data)

                        except:  # noqa: E722
                            pass
                        try:
                            if not isinstance(data, dict):
                                raise TypeError()
                            return CompletenessScorer.from_dict(data)

                        except:  # noqa: E722
                            pass
                        try:
                            if not isinstance(data, dict):
                                raise TypeError()
                            return ContextAdherenceScorer.from_dict(data)

                        except:  # noqa: E722
                            pass
                        try:
                            if not isinstance(data, dict):
                                raise TypeError()
                            return ContextRelevanceScorer.from_dict(data)

                        except:  # noqa: E722
                            pass
                        try:
                            if not isinstance(data, dict):
                                raise TypeError()
                            return CorrectnessScorer.from_dict(data)

                        except:  # noqa: E722
                            pass
                        try:
                            if not isinstance(data, dict):
                                raise TypeError()
                            return GroundTruthAdherenceScorer.from_dict(data)

                        except:  # noqa: E722
                            pass
                        try:
                            if not isinstance(data, dict):
                                raise TypeError()
                            return InputPIIScorer.from_dict(data)

                        except:  # noqa: E722
                            pass
                        try:
                            if not isinstance(data, dict):
                                raise TypeError()
                            return InputSexistScorer.from_dict(data)

                        except:  # noqa: E722
                            pass
                        try:
                            if not isinstance(data, dict):
                                raise TypeError()
                            return InputToneScorer.from_dict(data)

                        except:  # noqa: E722
                            pass
                        try:
                            if not isinstance(data, dict):
                                raise TypeError()
                            return InputToxicityScorer.from_dict(data)

                        except:  # noqa: E722
                            pass
                        try:
                            if not isinstance(data, dict):
                                raise TypeError()
                            return InstructionAdherenceScorer.from_dict(data)

                        except:  # noqa: E722
                            pass
                        try:
                            if not isinstance(data, dict):
                                raise TypeError()
                            return OutputPIIScorer.from_dict(data)

                        except:  # noqa: E722
                            pass
                        try:
                            if not isinstance(data, dict):
                                raise TypeError()
                            return OutputSexistScorer.from_dict(data)

                        except:  # noqa: E722
                            pass
                        try:
                            if not isinstance(data, dict):
                                raise TypeError()
                            return OutputToneScorer.from_dict(data)

                        except:  # noqa: E722
                            pass
                        try:
                            if not isinstance(data, dict):
                                raise TypeError()
                            return OutputToxicityScorer.from_dict(data)

                        except:  # noqa: E722
                            pass
                        try:
                            if not isinstance(data, dict):
                                raise TypeError()
                            return PromptInjectionScorer.from_dict(data)

                        except:  # noqa: E722
                            pass
                        try:
                            if not isinstance(data, dict):
                                raise TypeError()
                            return PromptPerplexityScorer.from_dict(data)

                        except:  # noqa: E722
                            pass
                        try:
                            if not isinstance(data, dict):
                                raise TypeError()
                            return RougeScorer.from_dict(data)

                        except:  # noqa: E722
                            pass
                        try:
                            if not isinstance(data, dict):
                                raise TypeError()
                            return ToolErrorRateScorer.from_dict(data)

                        except:  # noqa: E722
                            pass
                        try:
                            if not isinstance(data, dict):
                                raise TypeError()
                            return ToolSelectionQualityScorer.from_dict(data)

                        except:  # noqa: E722
                            pass
                        if not isinstance(data, dict):
                            raise TypeError()
                        return UncertaintyScorer.from_dict(data)

                    scorers_type_1_item = _parse_scorers_type_1_item(scorers_type_1_item_data)

                    scorers_type_1.append(scorers_type_1_item)

                return scorers_type_1
            except:  # noqa: E722
                pass
            return cast(
                list[
                    AgenticSessionSuccessScorer
                    | AgenticWorkflowSuccessScorer
                    | BleuScorer
                    | ChunkAttributionUtilizationScorer
                    | CompletenessScorer
                    | ContextAdherenceScorer
                    | ContextRelevanceScorer
                    | CorrectnessScorer
                    | GroundTruthAdherenceScorer
                    | InputPIIScorer
                    | InputSexistScorer
                    | InputToneScorer
                    | InputToxicityScorer
                    | InstructionAdherenceScorer
                    | OutputPIIScorer
                    | OutputSexistScorer
                    | OutputToneScorer
                    | OutputToxicityScorer
                    | PromptInjectionScorer
                    | PromptPerplexityScorer
                    | RougeScorer
                    | ToolErrorRateScorer
                    | ToolSelectionQualityScorer
                    | UncertaintyScorer
                ]
                | list[ScorerConfig]
                | None
                | Unset,
                data,
            )

        scorers = _parse_scorers(d.pop("scorers", UNSET))

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
                return cast(list[str], data)

            except:  # noqa: E722
                pass
            return cast(list[str] | None | Unset, data)

        prompt_generated_scorers_configuration = _parse_prompt_generated_scorers_configuration(
            d.pop("prompt_generated_scorers_configuration", UNSET)
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

        def _parse_prompt_scorers_configuration(data: object) -> None | ScorersConfiguration | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                return ScorersConfiguration.from_dict(data)

            except:  # noqa: E722
                pass
            return cast(None | ScorersConfiguration | Unset, data)

        prompt_scorers_configuration = _parse_prompt_scorers_configuration(d.pop("prompt_scorers_configuration", UNSET))

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
                            return CustomizedAgenticSessionSuccessGPTScorer.from_dict(data)

                        except:  # noqa: E722
                            pass
                        try:
                            if not isinstance(data, dict):
                                raise TypeError()
                            return CustomizedAgenticWorkflowSuccessGPTScorer.from_dict(data)

                        except:  # noqa: E722
                            pass
                        try:
                            if not isinstance(data, dict):
                                raise TypeError()
                            return CustomizedChunkAttributionUtilizationGPTScorer.from_dict(data)

                        except:  # noqa: E722
                            pass
                        try:
                            if not isinstance(data, dict):
                                raise TypeError()
                            return CustomizedCompletenessGPTScorer.from_dict(data)

                        except:  # noqa: E722
                            pass
                        try:
                            if not isinstance(data, dict):
                                raise TypeError()
                            return CustomizedFactualityGPTScorer.from_dict(data)

                        except:  # noqa: E722
                            pass
                        try:
                            if not isinstance(data, dict):
                                raise TypeError()
                            return CustomizedGroundednessGPTScorer.from_dict(data)

                        except:  # noqa: E722
                            pass
                        try:
                            if not isinstance(data, dict):
                                raise TypeError()
                            return CustomizedInstructionAdherenceGPTScorer.from_dict(data)

                        except:  # noqa: E722
                            pass
                        try:
                            if not isinstance(data, dict):
                                raise TypeError()
                            return CustomizedGroundTruthAdherenceGPTScorer.from_dict(data)

                        except:  # noqa: E722
                            pass
                        try:
                            if not isinstance(data, dict):
                                raise TypeError()
                            return CustomizedPromptInjectionGPTScorer.from_dict(data)

                        except:  # noqa: E722
                            pass
                        try:
                            if not isinstance(data, dict):
                                raise TypeError()
                            return CustomizedSexistGPTScorer.from_dict(data)

                        except:  # noqa: E722
                            pass
                        try:
                            if not isinstance(data, dict):
                                raise TypeError()
                            return CustomizedInputSexistGPTScorer.from_dict(data)

                        except:  # noqa: E722
                            pass
                        try:
                            if not isinstance(data, dict):
                                raise TypeError()
                            return CustomizedToolSelectionQualityGPTScorer.from_dict(data)

                        except:  # noqa: E722
                            pass
                        try:
                            if not isinstance(data, dict):
                                raise TypeError()
                            return CustomizedToolErrorRateGPTScorer.from_dict(data)

                        except:  # noqa: E722
                            pass
                        try:
                            if not isinstance(data, dict):
                                raise TypeError()
                            return CustomizedToxicityGPTScorer.from_dict(data)

                        except:  # noqa: E722
                            pass
                        if not isinstance(data, dict):
                            raise TypeError()
                        return CustomizedInputToxicityGPTScorer.from_dict(data)

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

        def _parse_prompt_scorer_settings(data: object) -> BaseScorer | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                return BaseScorer.from_dict(data)

            except:  # noqa: E722
                pass
            return cast(BaseScorer | None | Unset, data)

        prompt_scorer_settings = _parse_prompt_scorer_settings(d.pop("prompt_scorer_settings", UNSET))

        def _parse_scorer_config(data: object) -> None | ScorerConfig | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                return ScorerConfig.from_dict(data)

            except:  # noqa: E722
                pass
            return cast(None | ScorerConfig | Unset, data)

        scorer_config = _parse_scorer_config(d.pop("scorer_config", UNSET))

        _sub_scorers = d.pop("sub_scorers", UNSET)
        sub_scorers: list[ScorerName] | Unset = UNSET
        if _sub_scorers is not UNSET:
            sub_scorers = []
            for sub_scorers_item_data in _sub_scorers:
                sub_scorers_item = ScorerName(sub_scorers_item_data)

                sub_scorers.append(sub_scorers_item)

        def _parse_luna_model(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        luna_model = _parse_luna_model(d.pop("luna_model", UNSET))

        def _parse_segment_filters(data: object) -> list[SegmentFilter] | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                segment_filters_type_0 = []
                _segment_filters_type_0 = data
                for segment_filters_type_0_item_data in _segment_filters_type_0:
                    segment_filters_type_0_item = SegmentFilter.from_dict(segment_filters_type_0_item_data)

                    segment_filters_type_0.append(segment_filters_type_0_item)

                return segment_filters_type_0
            except:  # noqa: E722
                pass
            return cast(list[SegmentFilter] | None | Unset, data)

        segment_filters = _parse_segment_filters(d.pop("segment_filters", UNSET))

        def _parse_prompt_optimization_configuration(data: object) -> None | PromptOptimizationConfiguration | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                return PromptOptimizationConfiguration.from_dict(data)

            except:  # noqa: E722
                pass
            return cast(None | PromptOptimizationConfiguration | Unset, data)

        prompt_optimization_configuration = _parse_prompt_optimization_configuration(
            d.pop("prompt_optimization_configuration", UNSET)
        )

        epoch = d.pop("epoch", UNSET)

        def _parse_metric_critique_configuration(data: object) -> MetricCritiqueJobConfiguration | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                return MetricCritiqueJobConfiguration.from_dict(data)

            except:  # noqa: E722
                pass
            return cast(MetricCritiqueJobConfiguration | None | Unset, data)

        metric_critique_configuration = _parse_metric_critique_configuration(
            d.pop("metric_critique_configuration", UNSET)
        )

        def _parse_is_session(data: object) -> bool | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(bool | None | Unset, data)

        is_session = _parse_is_session(d.pop("is_session", UNSET))

        upload_data_in_separate_task = d.pop("upload_data_in_separate_task", UNSET)

        log_metric_computing_records = d.pop("log_metric_computing_records", UNSET)

        stream_metrics = d.pop("stream_metrics", UNSET)

        multijudge_average_boolean_metrics = d.pop("multijudge_average_boolean_metrics", UNSET)

        create_job_response = cls(
            project_id=project_id,
            run_id=run_id,
            message=message,
            link=link,
            resource_limits=resource_limits,
            job_id=job_id,
            job_name=job_name,
            should_retry=should_retry,
            user_id=user_id,
            task_type=task_type,
            labels=labels,
            ner_labels=ner_labels,
            tasks=tasks,
            non_inference_logged=non_inference_logged,
            migration_name=migration_name,
            xray=xray,
            process_existing_inference_runs=process_existing_inference_runs,
            feature_names=feature_names,
            prompt_dataset_id=prompt_dataset_id,
            dataset_id=dataset_id,
            dataset_version_index=dataset_version_index,
            prompt_template_version_id=prompt_template_version_id,
            monitor_batch_id=monitor_batch_id,
            protect_trace_id=protect_trace_id,
            protect_scorer_payload=protect_scorer_payload,
            prompt_settings=prompt_settings,
            scorers=scorers,
            prompt_registered_scorers_configuration=prompt_registered_scorers_configuration,
            prompt_generated_scorers_configuration=prompt_generated_scorers_configuration,
            prompt_finetuned_scorers_configuration=prompt_finetuned_scorers_configuration,
            prompt_scorers_configuration=prompt_scorers_configuration,
            prompt_customized_scorers_configuration=prompt_customized_scorers_configuration,
            prompt_scorer_settings=prompt_scorer_settings,
            scorer_config=scorer_config,
            sub_scorers=sub_scorers,
            luna_model=luna_model,
            segment_filters=segment_filters,
            prompt_optimization_configuration=prompt_optimization_configuration,
            epoch=epoch,
            metric_critique_configuration=metric_critique_configuration,
            is_session=is_session,
            upload_data_in_separate_task=upload_data_in_separate_task,
            log_metric_computing_records=log_metric_computing_records,
            stream_metrics=stream_metrics,
            multijudge_average_boolean_metrics=multijudge_average_boolean_metrics,
        )

        create_job_response.additional_properties = d
        return create_job_response

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
