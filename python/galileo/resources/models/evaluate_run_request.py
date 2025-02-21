from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.agent_step import AgentStep
    from ..models.agentic_workflow_success_scorer import AgenticWorkflowSuccessScorer
    from ..models.bleu_scorer import BleuScorer
    from ..models.chain_step import ChainStep
    from ..models.chunk_attribution_utilization_scorer import ChunkAttributionUtilizationScorer
    from ..models.completeness_scorer import CompletenessScorer
    from ..models.context_adherence_scorer import ContextAdherenceScorer
    from ..models.context_relevance_scorer import ContextRelevanceScorer
    from ..models.correctness_scorer import CorrectnessScorer
    from ..models.generated_scorer_config import GeneratedScorerConfig
    from ..models.ground_truth_adherence_scorer import GroundTruthAdherenceScorer
    from ..models.input_pii_scorer import InputPIIScorer
    from ..models.input_sexist_scorer import InputSexistScorer
    from ..models.input_tone_scorer import InputToneScorer
    from ..models.input_toxicity_scorer import InputToxicityScorer
    from ..models.instruction_adherence_scorer import InstructionAdherenceScorer
    from ..models.llm_step import LlmStep
    from ..models.output_pii_scorer import OutputPIIScorer
    from ..models.output_sexist_scorer import OutputSexistScorer
    from ..models.output_tone_scorer import OutputToneScorer
    from ..models.output_toxicity_scorer import OutputToxicityScorer
    from ..models.prompt_injection_scorer import PromptInjectionScorer
    from ..models.prompt_perplexity_scorer import PromptPerplexityScorer
    from ..models.registered_scorer_config import RegisteredScorerConfig
    from ..models.retriever_step import RetrieverStep
    from ..models.rouge_scorer import RougeScorer
    from ..models.tool_error_rate_scorer import ToolErrorRateScorer
    from ..models.tool_selection_quality_scorer import ToolSelectionQualityScorer
    from ..models.tool_step import ToolStep
    from ..models.uncertainty_scorer import UncertaintyScorer
    from ..models.workflow_step import WorkflowStep


T = TypeVar("T", bound="EvaluateRunRequest")


@_attrs_define
class EvaluateRunRequest:
    """
    Attributes:
        workflows (list[Union['AgentStep', 'ChainStep', 'LlmStep', 'RetrieverStep', 'ToolStep', 'WorkflowStep']]): List
            of workflows to include in the run.
        generated_scorers (Union[Unset, list['GeneratedScorerConfig']]): List of generated scorers to enable.
        project_id (Union[None, Unset, str]): Evaluate Project ID to which the run should be associated.
        project_name (Union[None, Unset, str]): Evaluate Project name to which the run should be associated. If the
            project does not exist, it will be created.
        registered_scorers (Union[Unset, list['RegisteredScorerConfig']]): List of registered scorers to enable.
        run_name (Union[None, Unset, str]): Name of the run. If no name is provided, a timestamp-based name will be
            generated.
        scorers (Union[Unset, list[Union['AgenticWorkflowSuccessScorer', 'BleuScorer',
            'ChunkAttributionUtilizationScorer', 'CompletenessScorer', 'ContextAdherenceScorer', 'ContextRelevanceScorer',
            'CorrectnessScorer', 'GroundTruthAdherenceScorer', 'InputPIIScorer', 'InputSexistScorer', 'InputToneScorer',
            'InputToxicityScorer', 'InstructionAdherenceScorer', 'OutputPIIScorer', 'OutputSexistScorer',
            'OutputToneScorer', 'OutputToxicityScorer', 'PromptInjectionScorer', 'PromptPerplexityScorer', 'RougeScorer',
            'ToolErrorRateScorer', 'ToolSelectionQualityScorer', 'UncertaintyScorer']]]): List of Galileo scorers to enable.
    """

    workflows: list[Union["AgentStep", "ChainStep", "LlmStep", "RetrieverStep", "ToolStep", "WorkflowStep"]]
    generated_scorers: Union[Unset, list["GeneratedScorerConfig"]] = UNSET
    project_id: Union[None, Unset, str] = UNSET
    project_name: Union[None, Unset, str] = UNSET
    registered_scorers: Union[Unset, list["RegisteredScorerConfig"]] = UNSET
    run_name: Union[None, Unset, str] = UNSET
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
        from ..models.chain_step import ChainStep
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
        from ..models.llm_step import LlmStep
        from ..models.output_pii_scorer import OutputPIIScorer
        from ..models.output_sexist_scorer import OutputSexistScorer
        from ..models.output_tone_scorer import OutputToneScorer
        from ..models.output_toxicity_scorer import OutputToxicityScorer
        from ..models.prompt_injection_scorer import PromptInjectionScorer
        from ..models.prompt_perplexity_scorer import PromptPerplexityScorer
        from ..models.retriever_step import RetrieverStep
        from ..models.rouge_scorer import RougeScorer
        from ..models.tool_error_rate_scorer import ToolErrorRateScorer
        from ..models.tool_selection_quality_scorer import ToolSelectionQualityScorer
        from ..models.tool_step import ToolStep
        from ..models.workflow_step import WorkflowStep

        workflows = []
        for workflows_item_data in self.workflows:
            workflows_item: dict[str, Any]
            if isinstance(workflows_item_data, WorkflowStep):
                workflows_item = workflows_item_data.to_dict()
            elif isinstance(workflows_item_data, ChainStep):
                workflows_item = workflows_item_data.to_dict()
            elif isinstance(workflows_item_data, LlmStep):
                workflows_item = workflows_item_data.to_dict()
            elif isinstance(workflows_item_data, RetrieverStep):
                workflows_item = workflows_item_data.to_dict()
            elif isinstance(workflows_item_data, ToolStep):
                workflows_item = workflows_item_data.to_dict()
            else:
                workflows_item = workflows_item_data.to_dict()

            workflows.append(workflows_item)

        generated_scorers: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.generated_scorers, Unset):
            generated_scorers = []
            for generated_scorers_item_data in self.generated_scorers:
                generated_scorers_item = generated_scorers_item_data.to_dict()
                generated_scorers.append(generated_scorers_item)

        project_id: Union[None, Unset, str]
        if isinstance(self.project_id, Unset):
            project_id = UNSET
        else:
            project_id = self.project_id

        project_name: Union[None, Unset, str]
        if isinstance(self.project_name, Unset):
            project_name = UNSET
        else:
            project_name = self.project_name

        registered_scorers: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.registered_scorers, Unset):
            registered_scorers = []
            for registered_scorers_item_data in self.registered_scorers:
                registered_scorers_item = registered_scorers_item_data.to_dict()
                registered_scorers.append(registered_scorers_item)

        run_name: Union[None, Unset, str]
        if isinstance(self.run_name, Unset):
            run_name = UNSET
        else:
            run_name = self.run_name

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
        field_dict.update({"workflows": workflows})
        if generated_scorers is not UNSET:
            field_dict["generated_scorers"] = generated_scorers
        if project_id is not UNSET:
            field_dict["project_id"] = project_id
        if project_name is not UNSET:
            field_dict["project_name"] = project_name
        if registered_scorers is not UNSET:
            field_dict["registered_scorers"] = registered_scorers
        if run_name is not UNSET:
            field_dict["run_name"] = run_name
        if scorers is not UNSET:
            field_dict["scorers"] = scorers

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.agent_step import AgentStep
        from ..models.agentic_workflow_success_scorer import AgenticWorkflowSuccessScorer
        from ..models.bleu_scorer import BleuScorer
        from ..models.chain_step import ChainStep
        from ..models.chunk_attribution_utilization_scorer import ChunkAttributionUtilizationScorer
        from ..models.completeness_scorer import CompletenessScorer
        from ..models.context_adherence_scorer import ContextAdherenceScorer
        from ..models.context_relevance_scorer import ContextRelevanceScorer
        from ..models.correctness_scorer import CorrectnessScorer
        from ..models.generated_scorer_config import GeneratedScorerConfig
        from ..models.ground_truth_adherence_scorer import GroundTruthAdherenceScorer
        from ..models.input_pii_scorer import InputPIIScorer
        from ..models.input_sexist_scorer import InputSexistScorer
        from ..models.input_tone_scorer import InputToneScorer
        from ..models.input_toxicity_scorer import InputToxicityScorer
        from ..models.instruction_adherence_scorer import InstructionAdherenceScorer
        from ..models.llm_step import LlmStep
        from ..models.output_pii_scorer import OutputPIIScorer
        from ..models.output_sexist_scorer import OutputSexistScorer
        from ..models.output_tone_scorer import OutputToneScorer
        from ..models.output_toxicity_scorer import OutputToxicityScorer
        from ..models.prompt_injection_scorer import PromptInjectionScorer
        from ..models.prompt_perplexity_scorer import PromptPerplexityScorer
        from ..models.registered_scorer_config import RegisteredScorerConfig
        from ..models.retriever_step import RetrieverStep
        from ..models.rouge_scorer import RougeScorer
        from ..models.tool_error_rate_scorer import ToolErrorRateScorer
        from ..models.tool_selection_quality_scorer import ToolSelectionQualityScorer
        from ..models.tool_step import ToolStep
        from ..models.uncertainty_scorer import UncertaintyScorer
        from ..models.workflow_step import WorkflowStep

        d = src_dict.copy()
        workflows = []
        _workflows = d.pop("workflows")
        for workflows_item_data in _workflows:

            def _parse_workflows_item(
                data: object,
            ) -> Union["AgentStep", "ChainStep", "LlmStep", "RetrieverStep", "ToolStep", "WorkflowStep"]:
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    workflows_item_type_0 = WorkflowStep.from_dict(data)

                    return workflows_item_type_0
                except:  # noqa: E722
                    pass
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    workflows_item_type_1 = ChainStep.from_dict(data)

                    return workflows_item_type_1
                except:  # noqa: E722
                    pass
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    workflows_item_type_2 = LlmStep.from_dict(data)

                    return workflows_item_type_2
                except:  # noqa: E722
                    pass
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    workflows_item_type_3 = RetrieverStep.from_dict(data)

                    return workflows_item_type_3
                except:  # noqa: E722
                    pass
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    workflows_item_type_4 = ToolStep.from_dict(data)

                    return workflows_item_type_4
                except:  # noqa: E722
                    pass
                if not isinstance(data, dict):
                    raise TypeError()
                workflows_item_type_5 = AgentStep.from_dict(data)

                return workflows_item_type_5

            workflows_item = _parse_workflows_item(workflows_item_data)

            workflows.append(workflows_item)

        generated_scorers = []
        _generated_scorers = d.pop("generated_scorers", UNSET)
        for generated_scorers_item_data in _generated_scorers or []:
            generated_scorers_item = GeneratedScorerConfig.from_dict(generated_scorers_item_data)

            generated_scorers.append(generated_scorers_item)

        def _parse_project_id(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        project_id = _parse_project_id(d.pop("project_id", UNSET))

        def _parse_project_name(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        project_name = _parse_project_name(d.pop("project_name", UNSET))

        registered_scorers = []
        _registered_scorers = d.pop("registered_scorers", UNSET)
        for registered_scorers_item_data in _registered_scorers or []:
            registered_scorers_item = RegisteredScorerConfig.from_dict(registered_scorers_item_data)

            registered_scorers.append(registered_scorers_item)

        def _parse_run_name(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        run_name = _parse_run_name(d.pop("run_name", UNSET))

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

        evaluate_run_request = cls(
            workflows=workflows,
            generated_scorers=generated_scorers,
            project_id=project_id,
            project_name=project_name,
            registered_scorers=registered_scorers,
            run_name=run_name,
            scorers=scorers,
        )

        evaluate_run_request.additional_properties = d
        return evaluate_run_request

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
