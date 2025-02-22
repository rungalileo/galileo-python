from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.agentic_workflow_success_scorer import AgenticWorkflowSuccessScorer
    from ..models.bleu_scorer import BleuScorer
    from ..models.chain_row import ChainRow
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
    from ..models.generated_scorer_config import GeneratedScorerConfig
    from ..models.ground_truth_adherence_scorer import GroundTruthAdherenceScorer
    from ..models.input_pii_scorer import InputPIIScorer
    from ..models.input_sexist_scorer import InputSexistScorer
    from ..models.input_tone_scorer import InputToneScorer
    from ..models.input_toxicity_scorer import InputToxicityScorer
    from ..models.instruction_adherence_scorer import InstructionAdherenceScorer
    from ..models.output_pii_scorer import OutputPIIScorer
    from ..models.output_sexist_scorer import OutputSexistScorer
    from ..models.output_tone_scorer import OutputToneScorer
    from ..models.output_toxicity_scorer import OutputToxicityScorer
    from ..models.prompt_injection_scorer import PromptInjectionScorer
    from ..models.prompt_perplexity_scorer import PromptPerplexityScorer
    from ..models.registered_scorer import RegisteredScorer
    from ..models.rouge_scorer import RougeScorer
    from ..models.scorers_configuration import ScorersConfiguration
    from ..models.tool_error_rate_scorer import ToolErrorRateScorer
    from ..models.tool_selection_quality_scorer import ToolSelectionQualityScorer
    from ..models.uncertainty_scorer import UncertaintyScorer


T = TypeVar("T", bound="PromptChainIngestRequest")


@_attrs_define
class PromptChainIngestRequest:
    """
    Attributes:
        generated_scorers (Union[None, Unset, list['GeneratedScorerConfig']]):
        prompt_customized_scorers_configuration (Union[None, Unset,
            list[Union['CustomizedAgenticWorkflowSuccessGPTScorer', 'CustomizedChunkAttributionUtilizationGPTScorer',
            'CustomizedCompletenessGPTScorer', 'CustomizedFactualityGPTScorer', 'CustomizedGroundTruthAdherenceGPTScorer',
            'CustomizedGroundednessGPTScorer', 'CustomizedInstructionAdherenceGPTScorer',
            'CustomizedToolErrorRateGPTScorer', 'CustomizedToolSelectionQualityGPTScorer']]]):
        prompt_registered_scorers_configuration (Union[None, Unset, list['RegisteredScorer']]):
        prompt_scorers_configuration (Union['ScorersConfiguration', None, Unset]):
        rows (Union[Unset, list['ChainRow']]):
        scorers (Union[Unset, list[Union['AgenticWorkflowSuccessScorer', 'BleuScorer',
            'ChunkAttributionUtilizationScorer', 'CompletenessScorer', 'ContextAdherenceScorer', 'ContextRelevanceScorer',
            'CorrectnessScorer', 'GroundTruthAdherenceScorer', 'InputPIIScorer', 'InputSexistScorer', 'InputToneScorer',
            'InputToxicityScorer', 'InstructionAdherenceScorer', 'OutputPIIScorer', 'OutputSexistScorer',
            'OutputToneScorer', 'OutputToxicityScorer', 'PromptInjectionScorer', 'PromptPerplexityScorer', 'RougeScorer',
            'ToolErrorRateScorer', 'ToolSelectionQualityScorer', 'UncertaintyScorer']]]):
    """

    generated_scorers: Union[None, Unset, list["GeneratedScorerConfig"]] = UNSET
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
    prompt_registered_scorers_configuration: Union[None, Unset, list["RegisteredScorer"]] = UNSET
    prompt_scorers_configuration: Union["ScorersConfiguration", None, Unset] = UNSET
    rows: Union[Unset, list["ChainRow"]] = UNSET
    scorers: Union[
        Unset,
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
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.agentic_workflow_success_scorer import AgenticWorkflowSuccessScorer
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
        from ..models.output_pii_scorer import OutputPIIScorer
        from ..models.output_sexist_scorer import OutputSexistScorer
        from ..models.output_tone_scorer import OutputToneScorer
        from ..models.output_toxicity_scorer import OutputToxicityScorer
        from ..models.prompt_injection_scorer import PromptInjectionScorer
        from ..models.prompt_perplexity_scorer import PromptPerplexityScorer
        from ..models.rouge_scorer import RougeScorer
        from ..models.scorers_configuration import ScorersConfiguration
        from ..models.tool_error_rate_scorer import ToolErrorRateScorer
        from ..models.tool_selection_quality_scorer import ToolSelectionQualityScorer

        generated_scorers: Union[None, Unset, list[dict[str, Any]]]
        if isinstance(self.generated_scorers, Unset):
            generated_scorers = UNSET
        elif isinstance(self.generated_scorers, list):
            generated_scorers = []
            for generated_scorers_type_0_item_data in self.generated_scorers:
                generated_scorers_type_0_item = generated_scorers_type_0_item_data.to_dict()
                generated_scorers.append(generated_scorers_type_0_item)

        else:
            generated_scorers = self.generated_scorers

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

        prompt_scorers_configuration: Union[None, Unset, dict[str, Any]]
        if isinstance(self.prompt_scorers_configuration, Unset):
            prompt_scorers_configuration = UNSET
        elif isinstance(self.prompt_scorers_configuration, ScorersConfiguration):
            prompt_scorers_configuration = self.prompt_scorers_configuration.to_dict()
        else:
            prompt_scorers_configuration = self.prompt_scorers_configuration

        rows: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.rows, Unset):
            rows = []
            for rows_item_data in self.rows:
                rows_item = rows_item_data.to_dict()
                rows.append(rows_item)

        scorers: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.scorers, Unset):
            scorers = []
            for scorers_item_data in self.scorers:
                scorers_item: dict[str, Any]
                if isinstance(scorers_item_data, AgenticWorkflowSuccessScorer):
                    scorers_item = scorers_item_data.to_dict()
                elif isinstance(scorers_item_data, BleuScorer):
                    scorers_item = scorers_item_data.to_dict()
                elif isinstance(scorers_item_data, ChunkAttributionUtilizationScorer):
                    scorers_item = scorers_item_data.to_dict()
                elif isinstance(scorers_item_data, CompletenessScorer):
                    scorers_item = scorers_item_data.to_dict()
                elif isinstance(scorers_item_data, ContextAdherenceScorer):
                    scorers_item = scorers_item_data.to_dict()
                elif isinstance(scorers_item_data, ContextRelevanceScorer):
                    scorers_item = scorers_item_data.to_dict()
                elif isinstance(scorers_item_data, CorrectnessScorer):
                    scorers_item = scorers_item_data.to_dict()
                elif isinstance(scorers_item_data, GroundTruthAdherenceScorer):
                    scorers_item = scorers_item_data.to_dict()
                elif isinstance(scorers_item_data, InputPIIScorer):
                    scorers_item = scorers_item_data.to_dict()
                elif isinstance(scorers_item_data, InputSexistScorer):
                    scorers_item = scorers_item_data.to_dict()
                elif isinstance(scorers_item_data, InputToneScorer):
                    scorers_item = scorers_item_data.to_dict()
                elif isinstance(scorers_item_data, InputToxicityScorer):
                    scorers_item = scorers_item_data.to_dict()
                elif isinstance(scorers_item_data, InstructionAdherenceScorer):
                    scorers_item = scorers_item_data.to_dict()
                elif isinstance(scorers_item_data, OutputPIIScorer):
                    scorers_item = scorers_item_data.to_dict()
                elif isinstance(scorers_item_data, OutputSexistScorer):
                    scorers_item = scorers_item_data.to_dict()
                elif isinstance(scorers_item_data, OutputToneScorer):
                    scorers_item = scorers_item_data.to_dict()
                elif isinstance(scorers_item_data, OutputToxicityScorer):
                    scorers_item = scorers_item_data.to_dict()
                elif isinstance(scorers_item_data, PromptInjectionScorer):
                    scorers_item = scorers_item_data.to_dict()
                elif isinstance(scorers_item_data, PromptPerplexityScorer):
                    scorers_item = scorers_item_data.to_dict()
                elif isinstance(scorers_item_data, RougeScorer):
                    scorers_item = scorers_item_data.to_dict()
                elif isinstance(scorers_item_data, ToolErrorRateScorer):
                    scorers_item = scorers_item_data.to_dict()
                elif isinstance(scorers_item_data, ToolSelectionQualityScorer):
                    scorers_item = scorers_item_data.to_dict()
                else:
                    scorers_item = scorers_item_data.to_dict()

                scorers.append(scorers_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if generated_scorers is not UNSET:
            field_dict["generated_scorers"] = generated_scorers
        if prompt_customized_scorers_configuration is not UNSET:
            field_dict["prompt_customized_scorers_configuration"] = prompt_customized_scorers_configuration
        if prompt_registered_scorers_configuration is not UNSET:
            field_dict["prompt_registered_scorers_configuration"] = prompt_registered_scorers_configuration
        if prompt_scorers_configuration is not UNSET:
            field_dict["prompt_scorers_configuration"] = prompt_scorers_configuration
        if rows is not UNSET:
            field_dict["rows"] = rows
        if scorers is not UNSET:
            field_dict["scorers"] = scorers

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.agentic_workflow_success_scorer import AgenticWorkflowSuccessScorer
        from ..models.bleu_scorer import BleuScorer
        from ..models.chain_row import ChainRow
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
        from ..models.generated_scorer_config import GeneratedScorerConfig
        from ..models.ground_truth_adherence_scorer import GroundTruthAdherenceScorer
        from ..models.input_pii_scorer import InputPIIScorer
        from ..models.input_sexist_scorer import InputSexistScorer
        from ..models.input_tone_scorer import InputToneScorer
        from ..models.input_toxicity_scorer import InputToxicityScorer
        from ..models.instruction_adherence_scorer import InstructionAdherenceScorer
        from ..models.output_pii_scorer import OutputPIIScorer
        from ..models.output_sexist_scorer import OutputSexistScorer
        from ..models.output_tone_scorer import OutputToneScorer
        from ..models.output_toxicity_scorer import OutputToxicityScorer
        from ..models.prompt_injection_scorer import PromptInjectionScorer
        from ..models.prompt_perplexity_scorer import PromptPerplexityScorer
        from ..models.registered_scorer import RegisteredScorer
        from ..models.rouge_scorer import RougeScorer
        from ..models.scorers_configuration import ScorersConfiguration
        from ..models.tool_error_rate_scorer import ToolErrorRateScorer
        from ..models.tool_selection_quality_scorer import ToolSelectionQualityScorer
        from ..models.uncertainty_scorer import UncertaintyScorer

        d = src_dict.copy()

        def _parse_generated_scorers(data: object) -> Union[None, Unset, list["GeneratedScorerConfig"]]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                generated_scorers_type_0 = []
                _generated_scorers_type_0 = data
                for generated_scorers_type_0_item_data in _generated_scorers_type_0:
                    generated_scorers_type_0_item = GeneratedScorerConfig.from_dict(generated_scorers_type_0_item_data)

                    generated_scorers_type_0.append(generated_scorers_type_0_item)

                return generated_scorers_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, list["GeneratedScorerConfig"]], data)

        generated_scorers = _parse_generated_scorers(d.pop("generated_scorers", UNSET))

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

        rows = []
        _rows = d.pop("rows", UNSET)
        for rows_item_data in _rows or []:
            rows_item = ChainRow.from_dict(rows_item_data)

            rows.append(rows_item)

        scorers = []
        _scorers = d.pop("scorers", UNSET)
        for scorers_item_data in _scorers or []:

            def _parse_scorers_item(
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
                    scorers_item_type_0 = AgenticWorkflowSuccessScorer.from_dict(data)

                    return scorers_item_type_0
                except:  # noqa: E722
                    pass
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    scorers_item_type_1 = BleuScorer.from_dict(data)

                    return scorers_item_type_1
                except:  # noqa: E722
                    pass
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    scorers_item_type_2 = ChunkAttributionUtilizationScorer.from_dict(data)

                    return scorers_item_type_2
                except:  # noqa: E722
                    pass
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    scorers_item_type_3 = CompletenessScorer.from_dict(data)

                    return scorers_item_type_3
                except:  # noqa: E722
                    pass
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    scorers_item_type_4 = ContextAdherenceScorer.from_dict(data)

                    return scorers_item_type_4
                except:  # noqa: E722
                    pass
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    scorers_item_type_5 = ContextRelevanceScorer.from_dict(data)

                    return scorers_item_type_5
                except:  # noqa: E722
                    pass
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    scorers_item_type_6 = CorrectnessScorer.from_dict(data)

                    return scorers_item_type_6
                except:  # noqa: E722
                    pass
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    scorers_item_type_7 = GroundTruthAdherenceScorer.from_dict(data)

                    return scorers_item_type_7
                except:  # noqa: E722
                    pass
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    scorers_item_type_8 = InputPIIScorer.from_dict(data)

                    return scorers_item_type_8
                except:  # noqa: E722
                    pass
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    scorers_item_type_9 = InputSexistScorer.from_dict(data)

                    return scorers_item_type_9
                except:  # noqa: E722
                    pass
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    scorers_item_type_10 = InputToneScorer.from_dict(data)

                    return scorers_item_type_10
                except:  # noqa: E722
                    pass
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    scorers_item_type_11 = InputToxicityScorer.from_dict(data)

                    return scorers_item_type_11
                except:  # noqa: E722
                    pass
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    scorers_item_type_12 = InstructionAdherenceScorer.from_dict(data)

                    return scorers_item_type_12
                except:  # noqa: E722
                    pass
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    scorers_item_type_13 = OutputPIIScorer.from_dict(data)

                    return scorers_item_type_13
                except:  # noqa: E722
                    pass
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    scorers_item_type_14 = OutputSexistScorer.from_dict(data)

                    return scorers_item_type_14
                except:  # noqa: E722
                    pass
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    scorers_item_type_15 = OutputToneScorer.from_dict(data)

                    return scorers_item_type_15
                except:  # noqa: E722
                    pass
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    scorers_item_type_16 = OutputToxicityScorer.from_dict(data)

                    return scorers_item_type_16
                except:  # noqa: E722
                    pass
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    scorers_item_type_17 = PromptInjectionScorer.from_dict(data)

                    return scorers_item_type_17
                except:  # noqa: E722
                    pass
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    scorers_item_type_18 = PromptPerplexityScorer.from_dict(data)

                    return scorers_item_type_18
                except:  # noqa: E722
                    pass
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    scorers_item_type_19 = RougeScorer.from_dict(data)

                    return scorers_item_type_19
                except:  # noqa: E722
                    pass
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    scorers_item_type_20 = ToolErrorRateScorer.from_dict(data)

                    return scorers_item_type_20
                except:  # noqa: E722
                    pass
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    scorers_item_type_21 = ToolSelectionQualityScorer.from_dict(data)

                    return scorers_item_type_21
                except:  # noqa: E722
                    pass
                if not isinstance(data, dict):
                    raise TypeError()
                scorers_item_type_22 = UncertaintyScorer.from_dict(data)

                return scorers_item_type_22

            scorers_item = _parse_scorers_item(scorers_item_data)

            scorers.append(scorers_item)

        prompt_chain_ingest_request = cls(
            generated_scorers=generated_scorers,
            prompt_customized_scorers_configuration=prompt_customized_scorers_configuration,
            prompt_registered_scorers_configuration=prompt_registered_scorers_configuration,
            prompt_scorers_configuration=prompt_scorers_configuration,
            rows=rows,
            scorers=scorers,
        )

        prompt_chain_ingest_request.additional_properties = d
        return prompt_chain_ingest_request

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
