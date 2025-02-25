from io import BytesIO
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.task_type import TaskType
from ..types import UNSET, File, FileJsonType, Unset

if TYPE_CHECKING:
    from ..models.agentic_workflow_success_scorer import AgenticWorkflowSuccessScorer
    from ..models.base_scorer import BaseScorer
    from ..models.bleu_scorer import BleuScorer
    from ..models.chunk_attribution_utilization_scorer import ChunkAttributionUtilizationScorer
    from ..models.completeness_scorer import CompletenessScorer
    from ..models.context_adherence_scorer import ContextAdherenceScorer
    from ..models.context_relevance_scorer import ContextRelevanceScorer
    from ..models.correctness_scorer import CorrectnessScorer
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
    from ..models.tool_error_rate_scorer import ToolErrorRateScorer
    from ..models.tool_selection_quality_scorer import ToolSelectionQualityScorer
    from ..models.uncertainty_scorer import UncertaintyScorer


T = TypeVar("T", bound="CreateJobRequest")


@_attrs_define
class CreateJobRequest:
    """
    Attributes:
        project_id (str):
        run_id (str):
        dataset_id (Union[None, Unset, str]):
        dataset_version_index (Union[None, Unset, int]):
        epoch (Union[Unset, int]):  Default: 0.
        feature_names (Union[None, Unset, list[str]]):
        job_id (Union[None, Unset, str]):
        job_name (Union[Unset, str]):  Default: 'default'.
        labels (Union[Unset, list[list[str]], list[str]]):
        metric_critique_configuration (Union['MetricCritiqueJobConfiguration', None, Unset]):
        migration_name (Union[None, Unset, str]):
        monitor_batch_id (Union[None, Unset, str]):
        ner_labels (Union[None, Unset, list[str]]):
        non_inference_logged (Union[Unset, bool]):  Default: False.
        process_existing_inference_runs (Union[Unset, bool]):  Default: False.
        prompt_customized_scorers_configuration (Union[None, Unset,
            list[Union['CustomizedAgenticWorkflowSuccessGPTScorer', 'CustomizedChunkAttributionUtilizationGPTScorer',
            'CustomizedCompletenessGPTScorer', 'CustomizedFactualityGPTScorer', 'CustomizedGroundTruthAdherenceGPTScorer',
            'CustomizedGroundednessGPTScorer', 'CustomizedInstructionAdherenceGPTScorer',
            'CustomizedToolErrorRateGPTScorer', 'CustomizedToolSelectionQualityGPTScorer']]]):
        prompt_dataset_id (Union[None, Unset, str]):
        prompt_generated_scorers_configuration (Union[None, Unset, list[str]]):
        prompt_optimization_configuration (Union['PromptOptimizationConfiguration', None, Unset]):
        prompt_registered_scorers_configuration (Union[None, Unset, list['RegisteredScorer']]):
        prompt_scorer_settings (Union['BaseScorer', None, Unset]):
        prompt_scorers_configuration (Union['ScorersConfiguration', None, Unset]):
        prompt_settings (Union['PromptRunSettings', None, Unset]):
        prompt_template_version_id (Union[None, Unset, str]):
        protect_scorer_payload (Union[File, None, Unset]):
        protect_trace_id (Union[None, Unset, str]):
        scorers (Union[None, Unset, list['ScorerConfig'], list[Union['AgenticWorkflowSuccessScorer', 'BleuScorer',
            'ChunkAttributionUtilizationScorer', 'CompletenessScorer', 'ContextAdherenceScorer', 'ContextRelevanceScorer',
            'CorrectnessScorer', 'GroundTruthAdherenceScorer', 'InputPIIScorer', 'InputSexistScorer', 'InputToneScorer',
            'InputToxicityScorer', 'InstructionAdherenceScorer', 'OutputPIIScorer', 'OutputSexistScorer',
            'OutputToneScorer', 'OutputToxicityScorer', 'PromptInjectionScorer', 'PromptPerplexityScorer', 'RougeScorer',
            'ToolErrorRateScorer', 'ToolSelectionQualityScorer', 'UncertaintyScorer']]]): For G2.0 we send all scorers as
            ScorerConfig, for G1.0 we send preset scorers  as GalileoScorer
        should_retry (Union[Unset, bool]):  Default: True.
        task_type (Union[None, TaskType, Unset]):
        tasks (Union[None, Unset, list[str]]):
        user_id (Union[None, Unset, str]):
        xray (Union[Unset, bool]):  Default: True.
    """

    project_id: str
    run_id: str
    dataset_id: Union[None, Unset, str] = UNSET
    dataset_version_index: Union[None, Unset, int] = UNSET
    epoch: Union[Unset, int] = 0
    feature_names: Union[None, Unset, list[str]] = UNSET
    job_id: Union[None, Unset, str] = UNSET
    job_name: Union[Unset, str] = "default"
    labels: Union[Unset, list[list[str]], list[str]] = UNSET
    metric_critique_configuration: Union["MetricCritiqueJobConfiguration", None, Unset] = UNSET
    migration_name: Union[None, Unset, str] = UNSET
    monitor_batch_id: Union[None, Unset, str] = UNSET
    ner_labels: Union[None, Unset, list[str]] = UNSET
    non_inference_logged: Union[Unset, bool] = False
    process_existing_inference_runs: Union[Unset, bool] = False
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
    prompt_dataset_id: Union[None, Unset, str] = UNSET
    prompt_generated_scorers_configuration: Union[None, Unset, list[str]] = UNSET
    prompt_optimization_configuration: Union["PromptOptimizationConfiguration", None, Unset] = UNSET
    prompt_registered_scorers_configuration: Union[None, Unset, list["RegisteredScorer"]] = UNSET
    prompt_scorer_settings: Union["BaseScorer", None, Unset] = UNSET
    prompt_scorers_configuration: Union["ScorersConfiguration", None, Unset] = UNSET
    prompt_settings: Union["PromptRunSettings", None, Unset] = UNSET
    prompt_template_version_id: Union[None, Unset, str] = UNSET
    protect_scorer_payload: Union[File, None, Unset] = UNSET
    protect_trace_id: Union[None, Unset, str] = UNSET
    scorers: Union[
        None,
        Unset,
        list["ScorerConfig"],
        list[
            Union[
                "AgenticWorkflowSuccessScorer",
                "BleuScorer",
                "ChunkAttributionUtilizationScorer",
                "CompletenessScorer",
                "ContextAdherenceScorer",
                "ContextRelevanceScorer",
                "CorrectnessScorer",
                "GroundTruthAdherenceScorer",
                "InputPIIScorer",
                "InputSexistScorer",
                "InputToneScorer",
                "InputToxicityScorer",
                "InstructionAdherenceScorer",
                "OutputPIIScorer",
                "OutputSexistScorer",
                "OutputToneScorer",
                "OutputToxicityScorer",
                "PromptInjectionScorer",
                "PromptPerplexityScorer",
                "RougeScorer",
                "ToolErrorRateScorer",
                "ToolSelectionQualityScorer",
                "UncertaintyScorer",
            ]
        ],
    ] = UNSET
    should_retry: Union[Unset, bool] = True
    task_type: Union[None, TaskType, Unset] = UNSET
    tasks: Union[None, Unset, list[str]] = UNSET
    user_id: Union[None, Unset, str] = UNSET
    xray: Union[Unset, bool] = True
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.agentic_workflow_success_scorer import AgenticWorkflowSuccessScorer
        from ..models.base_scorer import BaseScorer
        from ..models.bleu_scorer import BleuScorer
        from ..models.chunk_attribution_utilization_scorer import ChunkAttributionUtilizationScorer
        from ..models.completeness_scorer import CompletenessScorer
        from ..models.context_adherence_scorer import ContextAdherenceScorer
        from ..models.context_relevance_scorer import ContextRelevanceScorer
        from ..models.correctness_scorer import CorrectnessScorer
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
        from ..models.scorers_configuration import ScorersConfiguration
        from ..models.tool_error_rate_scorer import ToolErrorRateScorer
        from ..models.tool_selection_quality_scorer import ToolSelectionQualityScorer

        project_id = self.project_id

        run_id = self.run_id

        dataset_id: Union[None, Unset, str]
        if isinstance(self.dataset_id, Unset):
            dataset_id = UNSET
        else:
            dataset_id = self.dataset_id

        dataset_version_index: Union[None, Unset, int]
        if isinstance(self.dataset_version_index, Unset):
            dataset_version_index = UNSET
        else:
            dataset_version_index = self.dataset_version_index

        epoch = self.epoch

        feature_names: Union[None, Unset, list[str]]
        if isinstance(self.feature_names, Unset):
            feature_names = UNSET
        elif isinstance(self.feature_names, list):
            feature_names = self.feature_names

        else:
            feature_names = self.feature_names

        job_id: Union[None, Unset, str]
        if isinstance(self.job_id, Unset):
            job_id = UNSET
        else:
            job_id = self.job_id

        job_name = self.job_name

        labels: Union[Unset, list[list[str]], list[str]]
        if isinstance(self.labels, Unset):
            labels = UNSET
        elif isinstance(self.labels, list):
            labels = []
            for labels_type_0_item_data in self.labels:
                labels_type_0_item = labels_type_0_item_data

                labels.append(labels_type_0_item)

        else:
            labels = self.labels

        metric_critique_configuration: Union[None, Unset, dict[str, Any]]
        if isinstance(self.metric_critique_configuration, Unset):
            metric_critique_configuration = UNSET
        elif isinstance(self.metric_critique_configuration, MetricCritiqueJobConfiguration):
            metric_critique_configuration = self.metric_critique_configuration.to_dict()
        else:
            metric_critique_configuration = self.metric_critique_configuration

        migration_name: Union[None, Unset, str]
        if isinstance(self.migration_name, Unset):
            migration_name = UNSET
        else:
            migration_name = self.migration_name

        monitor_batch_id: Union[None, Unset, str]
        if isinstance(self.monitor_batch_id, Unset):
            monitor_batch_id = UNSET
        else:
            monitor_batch_id = self.monitor_batch_id

        ner_labels: Union[None, Unset, list[str]]
        if isinstance(self.ner_labels, Unset):
            ner_labels = UNSET
        elif isinstance(self.ner_labels, list):
            ner_labels = self.ner_labels

        else:
            ner_labels = self.ner_labels

        non_inference_logged = self.non_inference_logged

        process_existing_inference_runs = self.process_existing_inference_runs

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

        prompt_dataset_id: Union[None, Unset, str]
        if isinstance(self.prompt_dataset_id, Unset):
            prompt_dataset_id = UNSET
        else:
            prompt_dataset_id = self.prompt_dataset_id

        prompt_generated_scorers_configuration: Union[None, Unset, list[str]]
        if isinstance(self.prompt_generated_scorers_configuration, Unset):
            prompt_generated_scorers_configuration = UNSET
        elif isinstance(self.prompt_generated_scorers_configuration, list):
            prompt_generated_scorers_configuration = self.prompt_generated_scorers_configuration

        else:
            prompt_generated_scorers_configuration = self.prompt_generated_scorers_configuration

        prompt_optimization_configuration: Union[None, Unset, dict[str, Any]]
        if isinstance(self.prompt_optimization_configuration, Unset):
            prompt_optimization_configuration = UNSET
        elif isinstance(self.prompt_optimization_configuration, PromptOptimizationConfiguration):
            prompt_optimization_configuration = self.prompt_optimization_configuration.to_dict()
        else:
            prompt_optimization_configuration = self.prompt_optimization_configuration

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

        prompt_scorer_settings: Union[None, Unset, dict[str, Any]]
        if isinstance(self.prompt_scorer_settings, Unset):
            prompt_scorer_settings = UNSET
        elif isinstance(self.prompt_scorer_settings, BaseScorer):
            prompt_scorer_settings = self.prompt_scorer_settings.to_dict()
        else:
            prompt_scorer_settings = self.prompt_scorer_settings

        prompt_scorers_configuration: Union[None, Unset, dict[str, Any]]
        if isinstance(self.prompt_scorers_configuration, Unset):
            prompt_scorers_configuration = UNSET
        elif isinstance(self.prompt_scorers_configuration, ScorersConfiguration):
            prompt_scorers_configuration = self.prompt_scorers_configuration.to_dict()
        else:
            prompt_scorers_configuration = self.prompt_scorers_configuration

        prompt_settings: Union[None, Unset, dict[str, Any]]
        if isinstance(self.prompt_settings, Unset):
            prompt_settings = UNSET
        elif isinstance(self.prompt_settings, PromptRunSettings):
            prompt_settings = self.prompt_settings.to_dict()
        else:
            prompt_settings = self.prompt_settings

        prompt_template_version_id: Union[None, Unset, str]
        if isinstance(self.prompt_template_version_id, Unset):
            prompt_template_version_id = UNSET
        else:
            prompt_template_version_id = self.prompt_template_version_id

        protect_scorer_payload: Union[FileJsonType, None, Unset]
        if isinstance(self.protect_scorer_payload, Unset):
            protect_scorer_payload = UNSET
        elif isinstance(self.protect_scorer_payload, File):
            protect_scorer_payload = self.protect_scorer_payload.to_tuple()

        else:
            protect_scorer_payload = self.protect_scorer_payload

        protect_trace_id: Union[None, Unset, str]
        if isinstance(self.protect_trace_id, Unset):
            protect_trace_id = UNSET
        else:
            protect_trace_id = self.protect_trace_id

        scorers: Union[None, Unset, list[dict[str, Any]]]
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
                if isinstance(scorers_type_1_item_data, AgenticWorkflowSuccessScorer):
                    scorers_type_1_item = scorers_type_1_item_data.to_dict()
                elif isinstance(scorers_type_1_item_data, BleuScorer):
                    scorers_type_1_item = scorers_type_1_item_data.to_dict()
                elif isinstance(scorers_type_1_item_data, ChunkAttributionUtilizationScorer):
                    scorers_type_1_item = scorers_type_1_item_data.to_dict()
                elif isinstance(scorers_type_1_item_data, CompletenessScorer):
                    scorers_type_1_item = scorers_type_1_item_data.to_dict()
                elif isinstance(scorers_type_1_item_data, ContextAdherenceScorer):
                    scorers_type_1_item = scorers_type_1_item_data.to_dict()
                elif isinstance(scorers_type_1_item_data, ContextRelevanceScorer):
                    scorers_type_1_item = scorers_type_1_item_data.to_dict()
                elif isinstance(scorers_type_1_item_data, CorrectnessScorer):
                    scorers_type_1_item = scorers_type_1_item_data.to_dict()
                elif isinstance(scorers_type_1_item_data, GroundTruthAdherenceScorer):
                    scorers_type_1_item = scorers_type_1_item_data.to_dict()
                elif isinstance(scorers_type_1_item_data, InputPIIScorer):
                    scorers_type_1_item = scorers_type_1_item_data.to_dict()
                elif isinstance(scorers_type_1_item_data, InputSexistScorer):
                    scorers_type_1_item = scorers_type_1_item_data.to_dict()
                elif isinstance(scorers_type_1_item_data, InputToneScorer):
                    scorers_type_1_item = scorers_type_1_item_data.to_dict()
                elif isinstance(scorers_type_1_item_data, InputToxicityScorer):
                    scorers_type_1_item = scorers_type_1_item_data.to_dict()
                elif isinstance(scorers_type_1_item_data, InstructionAdherenceScorer):
                    scorers_type_1_item = scorers_type_1_item_data.to_dict()
                elif isinstance(scorers_type_1_item_data, OutputPIIScorer):
                    scorers_type_1_item = scorers_type_1_item_data.to_dict()
                elif isinstance(scorers_type_1_item_data, OutputSexistScorer):
                    scorers_type_1_item = scorers_type_1_item_data.to_dict()
                elif isinstance(scorers_type_1_item_data, OutputToneScorer):
                    scorers_type_1_item = scorers_type_1_item_data.to_dict()
                elif isinstance(scorers_type_1_item_data, OutputToxicityScorer):
                    scorers_type_1_item = scorers_type_1_item_data.to_dict()
                elif isinstance(scorers_type_1_item_data, PromptInjectionScorer):
                    scorers_type_1_item = scorers_type_1_item_data.to_dict()
                elif isinstance(scorers_type_1_item_data, PromptPerplexityScorer):
                    scorers_type_1_item = scorers_type_1_item_data.to_dict()
                elif isinstance(scorers_type_1_item_data, RougeScorer):
                    scorers_type_1_item = scorers_type_1_item_data.to_dict()
                elif isinstance(scorers_type_1_item_data, ToolErrorRateScorer):
                    scorers_type_1_item = scorers_type_1_item_data.to_dict()
                elif isinstance(scorers_type_1_item_data, ToolSelectionQualityScorer):
                    scorers_type_1_item = scorers_type_1_item_data.to_dict()
                else:
                    scorers_type_1_item = scorers_type_1_item_data.to_dict()

                scorers.append(scorers_type_1_item)

        else:
            scorers = self.scorers

        should_retry = self.should_retry

        task_type: Union[None, Unset, int]
        if isinstance(self.task_type, Unset):
            task_type = UNSET
        elif isinstance(self.task_type, TaskType):
            task_type = self.task_type.value
        else:
            task_type = self.task_type

        tasks: Union[None, Unset, list[str]]
        if isinstance(self.tasks, Unset):
            tasks = UNSET
        elif isinstance(self.tasks, list):
            tasks = self.tasks

        else:
            tasks = self.tasks

        user_id: Union[None, Unset, str]
        if isinstance(self.user_id, Unset):
            user_id = UNSET
        else:
            user_id = self.user_id

        xray = self.xray

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({"project_id": project_id, "run_id": run_id})
        if dataset_id is not UNSET:
            field_dict["dataset_id"] = dataset_id
        if dataset_version_index is not UNSET:
            field_dict["dataset_version_index"] = dataset_version_index
        if epoch is not UNSET:
            field_dict["epoch"] = epoch
        if feature_names is not UNSET:
            field_dict["feature_names"] = feature_names
        if job_id is not UNSET:
            field_dict["job_id"] = job_id
        if job_name is not UNSET:
            field_dict["job_name"] = job_name
        if labels is not UNSET:
            field_dict["labels"] = labels
        if metric_critique_configuration is not UNSET:
            field_dict["metric_critique_configuration"] = metric_critique_configuration
        if migration_name is not UNSET:
            field_dict["migration_name"] = migration_name
        if monitor_batch_id is not UNSET:
            field_dict["monitor_batch_id"] = monitor_batch_id
        if ner_labels is not UNSET:
            field_dict["ner_labels"] = ner_labels
        if non_inference_logged is not UNSET:
            field_dict["non_inference_logged"] = non_inference_logged
        if process_existing_inference_runs is not UNSET:
            field_dict["process_existing_inference_runs"] = process_existing_inference_runs
        if prompt_customized_scorers_configuration is not UNSET:
            field_dict["prompt_customized_scorers_configuration"] = prompt_customized_scorers_configuration
        if prompt_dataset_id is not UNSET:
            field_dict["prompt_dataset_id"] = prompt_dataset_id
        if prompt_generated_scorers_configuration is not UNSET:
            field_dict["prompt_generated_scorers_configuration"] = prompt_generated_scorers_configuration
        if prompt_optimization_configuration is not UNSET:
            field_dict["prompt_optimization_configuration"] = prompt_optimization_configuration
        if prompt_registered_scorers_configuration is not UNSET:
            field_dict["prompt_registered_scorers_configuration"] = prompt_registered_scorers_configuration
        if prompt_scorer_settings is not UNSET:
            field_dict["prompt_scorer_settings"] = prompt_scorer_settings
        if prompt_scorers_configuration is not UNSET:
            field_dict["prompt_scorers_configuration"] = prompt_scorers_configuration
        if prompt_settings is not UNSET:
            field_dict["prompt_settings"] = prompt_settings
        if prompt_template_version_id is not UNSET:
            field_dict["prompt_template_version_id"] = prompt_template_version_id
        if protect_scorer_payload is not UNSET:
            field_dict["protect_scorer_payload"] = protect_scorer_payload
        if protect_trace_id is not UNSET:
            field_dict["protect_trace_id"] = protect_trace_id
        if scorers is not UNSET:
            field_dict["scorers"] = scorers
        if should_retry is not UNSET:
            field_dict["should_retry"] = should_retry
        if task_type is not UNSET:
            field_dict["task_type"] = task_type
        if tasks is not UNSET:
            field_dict["tasks"] = tasks
        if user_id is not UNSET:
            field_dict["user_id"] = user_id
        if xray is not UNSET:
            field_dict["xray"] = xray

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.agentic_workflow_success_scorer import AgenticWorkflowSuccessScorer
        from ..models.base_scorer import BaseScorer
        from ..models.bleu_scorer import BleuScorer
        from ..models.chunk_attribution_utilization_scorer import ChunkAttributionUtilizationScorer
        from ..models.completeness_scorer import CompletenessScorer
        from ..models.context_adherence_scorer import ContextAdherenceScorer
        from ..models.context_relevance_scorer import ContextRelevanceScorer
        from ..models.correctness_scorer import CorrectnessScorer
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
        from ..models.tool_error_rate_scorer import ToolErrorRateScorer
        from ..models.tool_selection_quality_scorer import ToolSelectionQualityScorer
        from ..models.uncertainty_scorer import UncertaintyScorer

        d = src_dict.copy()
        project_id = d.pop("project_id")

        run_id = d.pop("run_id")

        def _parse_dataset_id(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        dataset_id = _parse_dataset_id(d.pop("dataset_id", UNSET))

        def _parse_dataset_version_index(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        dataset_version_index = _parse_dataset_version_index(d.pop("dataset_version_index", UNSET))

        epoch = d.pop("epoch", UNSET)

        def _parse_feature_names(data: object) -> Union[None, Unset, list[str]]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                feature_names_type_0 = cast(list[str], data)

                return feature_names_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, list[str]], data)

        feature_names = _parse_feature_names(d.pop("feature_names", UNSET))

        def _parse_job_id(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        job_id = _parse_job_id(d.pop("job_id", UNSET))

        job_name = d.pop("job_name", UNSET)

        def _parse_labels(data: object) -> Union[Unset, list[list[str]], list[str]]:
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
            labels_type_1 = cast(list[str], data)

            return labels_type_1

        labels = _parse_labels(d.pop("labels", UNSET))

        def _parse_metric_critique_configuration(data: object) -> Union["MetricCritiqueJobConfiguration", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                metric_critique_configuration_type_0 = MetricCritiqueJobConfiguration.from_dict(data)

                return metric_critique_configuration_type_0
            except:  # noqa: E722
                pass
            return cast(Union["MetricCritiqueJobConfiguration", None, Unset], data)

        metric_critique_configuration = _parse_metric_critique_configuration(
            d.pop("metric_critique_configuration", UNSET)
        )

        def _parse_migration_name(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        migration_name = _parse_migration_name(d.pop("migration_name", UNSET))

        def _parse_monitor_batch_id(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        monitor_batch_id = _parse_monitor_batch_id(d.pop("monitor_batch_id", UNSET))

        def _parse_ner_labels(data: object) -> Union[None, Unset, list[str]]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                ner_labels_type_0 = cast(list[str], data)

                return ner_labels_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, list[str]], data)

        ner_labels = _parse_ner_labels(d.pop("ner_labels", UNSET))

        non_inference_logged = d.pop("non_inference_logged", UNSET)

        process_existing_inference_runs = d.pop("process_existing_inference_runs", UNSET)

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

        def _parse_prompt_dataset_id(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        prompt_dataset_id = _parse_prompt_dataset_id(d.pop("prompt_dataset_id", UNSET))

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

        def _parse_prompt_optimization_configuration(
            data: object,
        ) -> Union["PromptOptimizationConfiguration", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                prompt_optimization_configuration_type_0 = PromptOptimizationConfiguration.from_dict(data)

                return prompt_optimization_configuration_type_0
            except:  # noqa: E722
                pass
            return cast(Union["PromptOptimizationConfiguration", None, Unset], data)

        prompt_optimization_configuration = _parse_prompt_optimization_configuration(
            d.pop("prompt_optimization_configuration", UNSET)
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

        def _parse_prompt_scorer_settings(data: object) -> Union["BaseScorer", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                prompt_scorer_settings_type_0 = BaseScorer.from_dict(data)

                return prompt_scorer_settings_type_0
            except:  # noqa: E722
                pass
            return cast(Union["BaseScorer", None, Unset], data)

        prompt_scorer_settings = _parse_prompt_scorer_settings(d.pop("prompt_scorer_settings", UNSET))

        def _parse_prompt_scorers_configuration(data: object) -> Union["ScorersConfiguration", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                prompt_scorers_configuration_type_0 = ScorersConfiguration.from_dict(data)

                return prompt_scorers_configuration_type_0
            except:  # noqa: E722
                pass
            return cast(Union["ScorersConfiguration", None, Unset], data)

        prompt_scorers_configuration = _parse_prompt_scorers_configuration(d.pop("prompt_scorers_configuration", UNSET))

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

        def _parse_prompt_template_version_id(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        prompt_template_version_id = _parse_prompt_template_version_id(d.pop("prompt_template_version_id", UNSET))

        def _parse_protect_scorer_payload(data: object) -> Union[File, None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, bytes):
                    raise TypeError()
                protect_scorer_payload_type_0 = File(payload=BytesIO(data))

                return protect_scorer_payload_type_0
            except:  # noqa: E722
                pass
            return cast(Union[File, None, Unset], data)

        protect_scorer_payload = _parse_protect_scorer_payload(d.pop("protect_scorer_payload", UNSET))

        def _parse_protect_trace_id(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        protect_trace_id = _parse_protect_trace_id(d.pop("protect_trace_id", UNSET))

        def _parse_scorers(
            data: object,
        ) -> Union[
            None,
            Unset,
            list["ScorerConfig"],
            list[
                Union[
                    "AgenticWorkflowSuccessScorer",
                    "BleuScorer",
                    "ChunkAttributionUtilizationScorer",
                    "CompletenessScorer",
                    "ContextAdherenceScorer",
                    "ContextRelevanceScorer",
                    "CorrectnessScorer",
                    "GroundTruthAdherenceScorer",
                    "InputPIIScorer",
                    "InputSexistScorer",
                    "InputToneScorer",
                    "InputToxicityScorer",
                    "InstructionAdherenceScorer",
                    "OutputPIIScorer",
                    "OutputSexistScorer",
                    "OutputToneScorer",
                    "OutputToxicityScorer",
                    "PromptInjectionScorer",
                    "PromptPerplexityScorer",
                    "RougeScorer",
                    "ToolErrorRateScorer",
                    "ToolSelectionQualityScorer",
                    "UncertaintyScorer",
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
                    ) -> Union[
                        "AgenticWorkflowSuccessScorer",
                        "BleuScorer",
                        "ChunkAttributionUtilizationScorer",
                        "CompletenessScorer",
                        "ContextAdherenceScorer",
                        "ContextRelevanceScorer",
                        "CorrectnessScorer",
                        "GroundTruthAdherenceScorer",
                        "InputPIIScorer",
                        "InputSexistScorer",
                        "InputToneScorer",
                        "InputToxicityScorer",
                        "InstructionAdherenceScorer",
                        "OutputPIIScorer",
                        "OutputSexistScorer",
                        "OutputToneScorer",
                        "OutputToxicityScorer",
                        "PromptInjectionScorer",
                        "PromptPerplexityScorer",
                        "RougeScorer",
                        "ToolErrorRateScorer",
                        "ToolSelectionQualityScorer",
                        "UncertaintyScorer",
                    ]:
                        try:
                            if not isinstance(data, dict):
                                raise TypeError()
                            scorers_type_1_item_type_0 = AgenticWorkflowSuccessScorer.from_dict(data)

                            return scorers_type_1_item_type_0
                        except:  # noqa: E722
                            pass
                        try:
                            if not isinstance(data, dict):
                                raise TypeError()
                            scorers_type_1_item_type_1 = BleuScorer.from_dict(data)

                            return scorers_type_1_item_type_1
                        except:  # noqa: E722
                            pass
                        try:
                            if not isinstance(data, dict):
                                raise TypeError()
                            scorers_type_1_item_type_2 = ChunkAttributionUtilizationScorer.from_dict(data)

                            return scorers_type_1_item_type_2
                        except:  # noqa: E722
                            pass
                        try:
                            if not isinstance(data, dict):
                                raise TypeError()
                            scorers_type_1_item_type_3 = CompletenessScorer.from_dict(data)

                            return scorers_type_1_item_type_3
                        except:  # noqa: E722
                            pass
                        try:
                            if not isinstance(data, dict):
                                raise TypeError()
                            scorers_type_1_item_type_4 = ContextAdherenceScorer.from_dict(data)

                            return scorers_type_1_item_type_4
                        except:  # noqa: E722
                            pass
                        try:
                            if not isinstance(data, dict):
                                raise TypeError()
                            scorers_type_1_item_type_5 = ContextRelevanceScorer.from_dict(data)

                            return scorers_type_1_item_type_5
                        except:  # noqa: E722
                            pass
                        try:
                            if not isinstance(data, dict):
                                raise TypeError()
                            scorers_type_1_item_type_6 = CorrectnessScorer.from_dict(data)

                            return scorers_type_1_item_type_6
                        except:  # noqa: E722
                            pass
                        try:
                            if not isinstance(data, dict):
                                raise TypeError()
                            scorers_type_1_item_type_7 = GroundTruthAdherenceScorer.from_dict(data)

                            return scorers_type_1_item_type_7
                        except:  # noqa: E722
                            pass
                        try:
                            if not isinstance(data, dict):
                                raise TypeError()
                            scorers_type_1_item_type_8 = InputPIIScorer.from_dict(data)

                            return scorers_type_1_item_type_8
                        except:  # noqa: E722
                            pass
                        try:
                            if not isinstance(data, dict):
                                raise TypeError()
                            scorers_type_1_item_type_9 = InputSexistScorer.from_dict(data)

                            return scorers_type_1_item_type_9
                        except:  # noqa: E722
                            pass
                        try:
                            if not isinstance(data, dict):
                                raise TypeError()
                            scorers_type_1_item_type_10 = InputToneScorer.from_dict(data)

                            return scorers_type_1_item_type_10
                        except:  # noqa: E722
                            pass
                        try:
                            if not isinstance(data, dict):
                                raise TypeError()
                            scorers_type_1_item_type_11 = InputToxicityScorer.from_dict(data)

                            return scorers_type_1_item_type_11
                        except:  # noqa: E722
                            pass
                        try:
                            if not isinstance(data, dict):
                                raise TypeError()
                            scorers_type_1_item_type_12 = InstructionAdherenceScorer.from_dict(data)

                            return scorers_type_1_item_type_12
                        except:  # noqa: E722
                            pass
                        try:
                            if not isinstance(data, dict):
                                raise TypeError()
                            scorers_type_1_item_type_13 = OutputPIIScorer.from_dict(data)

                            return scorers_type_1_item_type_13
                        except:  # noqa: E722
                            pass
                        try:
                            if not isinstance(data, dict):
                                raise TypeError()
                            scorers_type_1_item_type_14 = OutputSexistScorer.from_dict(data)

                            return scorers_type_1_item_type_14
                        except:  # noqa: E722
                            pass
                        try:
                            if not isinstance(data, dict):
                                raise TypeError()
                            scorers_type_1_item_type_15 = OutputToneScorer.from_dict(data)

                            return scorers_type_1_item_type_15
                        except:  # noqa: E722
                            pass
                        try:
                            if not isinstance(data, dict):
                                raise TypeError()
                            scorers_type_1_item_type_16 = OutputToxicityScorer.from_dict(data)

                            return scorers_type_1_item_type_16
                        except:  # noqa: E722
                            pass
                        try:
                            if not isinstance(data, dict):
                                raise TypeError()
                            scorers_type_1_item_type_17 = PromptInjectionScorer.from_dict(data)

                            return scorers_type_1_item_type_17
                        except:  # noqa: E722
                            pass
                        try:
                            if not isinstance(data, dict):
                                raise TypeError()
                            scorers_type_1_item_type_18 = PromptPerplexityScorer.from_dict(data)

                            return scorers_type_1_item_type_18
                        except:  # noqa: E722
                            pass
                        try:
                            if not isinstance(data, dict):
                                raise TypeError()
                            scorers_type_1_item_type_19 = RougeScorer.from_dict(data)

                            return scorers_type_1_item_type_19
                        except:  # noqa: E722
                            pass
                        try:
                            if not isinstance(data, dict):
                                raise TypeError()
                            scorers_type_1_item_type_20 = ToolErrorRateScorer.from_dict(data)

                            return scorers_type_1_item_type_20
                        except:  # noqa: E722
                            pass
                        try:
                            if not isinstance(data, dict):
                                raise TypeError()
                            scorers_type_1_item_type_21 = ToolSelectionQualityScorer.from_dict(data)

                            return scorers_type_1_item_type_21
                        except:  # noqa: E722
                            pass
                        if not isinstance(data, dict):
                            raise TypeError()
                        scorers_type_1_item_type_22 = UncertaintyScorer.from_dict(data)

                        return scorers_type_1_item_type_22

                    scorers_type_1_item = _parse_scorers_type_1_item(scorers_type_1_item_data)

                    scorers_type_1.append(scorers_type_1_item)

                return scorers_type_1
            except:  # noqa: E722
                pass
            return cast(
                Union[
                    None,
                    Unset,
                    list["ScorerConfig"],
                    list[
                        Union[
                            "AgenticWorkflowSuccessScorer",
                            "BleuScorer",
                            "ChunkAttributionUtilizationScorer",
                            "CompletenessScorer",
                            "ContextAdherenceScorer",
                            "ContextRelevanceScorer",
                            "CorrectnessScorer",
                            "GroundTruthAdherenceScorer",
                            "InputPIIScorer",
                            "InputSexistScorer",
                            "InputToneScorer",
                            "InputToxicityScorer",
                            "InstructionAdherenceScorer",
                            "OutputPIIScorer",
                            "OutputSexistScorer",
                            "OutputToneScorer",
                            "OutputToxicityScorer",
                            "PromptInjectionScorer",
                            "PromptPerplexityScorer",
                            "RougeScorer",
                            "ToolErrorRateScorer",
                            "ToolSelectionQualityScorer",
                            "UncertaintyScorer",
                        ]
                    ],
                ],
                data,
            )

        scorers = _parse_scorers(d.pop("scorers", UNSET))

        should_retry = d.pop("should_retry", UNSET)

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

        def _parse_tasks(data: object) -> Union[None, Unset, list[str]]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                tasks_type_0 = cast(list[str], data)

                return tasks_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, list[str]], data)

        tasks = _parse_tasks(d.pop("tasks", UNSET))

        def _parse_user_id(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        user_id = _parse_user_id(d.pop("user_id", UNSET))

        xray = d.pop("xray", UNSET)

        create_job_request = cls(
            project_id=project_id,
            run_id=run_id,
            dataset_id=dataset_id,
            dataset_version_index=dataset_version_index,
            epoch=epoch,
            feature_names=feature_names,
            job_id=job_id,
            job_name=job_name,
            labels=labels,
            metric_critique_configuration=metric_critique_configuration,
            migration_name=migration_name,
            monitor_batch_id=monitor_batch_id,
            ner_labels=ner_labels,
            non_inference_logged=non_inference_logged,
            process_existing_inference_runs=process_existing_inference_runs,
            prompt_customized_scorers_configuration=prompt_customized_scorers_configuration,
            prompt_dataset_id=prompt_dataset_id,
            prompt_generated_scorers_configuration=prompt_generated_scorers_configuration,
            prompt_optimization_configuration=prompt_optimization_configuration,
            prompt_registered_scorers_configuration=prompt_registered_scorers_configuration,
            prompt_scorer_settings=prompt_scorer_settings,
            prompt_scorers_configuration=prompt_scorers_configuration,
            prompt_settings=prompt_settings,
            prompt_template_version_id=prompt_template_version_id,
            protect_scorer_payload=protect_scorer_payload,
            protect_trace_id=protect_trace_id,
            scorers=scorers,
            should_retry=should_retry,
            task_type=task_type,
            tasks=tasks,
            user_id=user_id,
            xray=xray,
        )

        create_job_request.additional_properties = d
        return create_job_request

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
