from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.agentic_workflow_success_scorer import AgenticWorkflowSuccessScorer
    from ..models.bleu_scorer import BleuScorer
    from ..models.chunk_attribution_utilization_scorer import ChunkAttributionUtilizationScorer
    from ..models.completeness_scorer import CompletenessScorer
    from ..models.context_adherence_scorer import ContextAdherenceScorer
    from ..models.context_relevance_scorer import ContextRelevanceScorer
    from ..models.correctness_scorer import CorrectnessScorer
    from ..models.generated_scorer import GeneratedScorer
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
    from ..models.tool_error_rate_scorer import ToolErrorRateScorer
    from ..models.tool_selection_quality_scorer import ToolSelectionQualityScorer
    from ..models.uncertainty_scorer import UncertaintyScorer


T = TypeVar("T", bound="ScorersConfig")


@_attrs_define
class ScorersConfig:
    """
    Attributes:
        generated_scorers (Union[Unset, list['GeneratedScorer']]): List of user generated scorers to enable.
        registered_scorers (Union[Unset, list['RegisteredScorer']]): List of user registered scorers to enable.
        scorers (Union[Unset, list[Union['AgenticWorkflowSuccessScorer', 'BleuScorer',
            'ChunkAttributionUtilizationScorer', 'CompletenessScorer', 'ContextAdherenceScorer', 'ContextRelevanceScorer',
            'CorrectnessScorer', 'GroundTruthAdherenceScorer', 'InputPIIScorer', 'InputSexistScorer', 'InputToneScorer',
            'InputToxicityScorer', 'InstructionAdherenceScorer', 'OutputPIIScorer', 'OutputSexistScorer',
            'OutputToneScorer', 'OutputToxicityScorer', 'PromptInjectionScorer', 'PromptPerplexityScorer', 'RougeScorer',
            'ToolErrorRateScorer', 'ToolSelectionQualityScorer', 'UncertaintyScorer']]]): List of Galileo scorers to enable.
    """

    generated_scorers: Union[Unset, list["GeneratedScorer"]] = UNSET
    registered_scorers: Union[Unset, list["RegisteredScorer"]] = UNSET
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
        from ..models.tool_error_rate_scorer import ToolErrorRateScorer
        from ..models.tool_selection_quality_scorer import ToolSelectionQualityScorer

        generated_scorers: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.generated_scorers, Unset):
            generated_scorers = []
            for generated_scorers_item_data in self.generated_scorers:
                generated_scorers_item = generated_scorers_item_data.to_dict()
                generated_scorers.append(generated_scorers_item)

        registered_scorers: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.registered_scorers, Unset):
            registered_scorers = []
            for registered_scorers_item_data in self.registered_scorers:
                registered_scorers_item = registered_scorers_item_data.to_dict()
                registered_scorers.append(registered_scorers_item)

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
        if registered_scorers is not UNSET:
            field_dict["registered_scorers"] = registered_scorers
        if scorers is not UNSET:
            field_dict["scorers"] = scorers

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.agentic_workflow_success_scorer import AgenticWorkflowSuccessScorer
        from ..models.bleu_scorer import BleuScorer
        from ..models.chunk_attribution_utilization_scorer import ChunkAttributionUtilizationScorer
        from ..models.completeness_scorer import CompletenessScorer
        from ..models.context_adherence_scorer import ContextAdherenceScorer
        from ..models.context_relevance_scorer import ContextRelevanceScorer
        from ..models.correctness_scorer import CorrectnessScorer
        from ..models.generated_scorer import GeneratedScorer
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
        from ..models.tool_error_rate_scorer import ToolErrorRateScorer
        from ..models.tool_selection_quality_scorer import ToolSelectionQualityScorer
        from ..models.uncertainty_scorer import UncertaintyScorer

        d = src_dict.copy()
        generated_scorers = []
        _generated_scorers = d.pop("generated_scorers", UNSET)
        for generated_scorers_item_data in _generated_scorers or []:
            generated_scorers_item = GeneratedScorer.from_dict(generated_scorers_item_data)

            generated_scorers.append(generated_scorers_item)

        registered_scorers = []
        _registered_scorers = d.pop("registered_scorers", UNSET)
        for registered_scorers_item_data in _registered_scorers or []:
            registered_scorers_item = RegisteredScorer.from_dict(registered_scorers_item_data)

            registered_scorers.append(registered_scorers_item)

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

        scorers_config = cls(
            generated_scorers=generated_scorers, registered_scorers=registered_scorers, scorers=scorers
        )

        scorers_config.additional_properties = d
        return scorers_config

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
