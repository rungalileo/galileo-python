from collections.abc import Mapping
from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="ScorersConfiguration")


@_attrs_define
class ScorersConfiguration:
    """Configure which scorers to enable for a particular prompt run.

    The keys here are sorted by their approximate execution time to execute the scorers that we anticipate will be the
    fastest first, and the slowest last.

        Attributes:
            action_advancement_luna (Union[Unset, bool]):  Default: False.
            action_completion_luna (Union[Unset, bool]):  Default: False.
            adherence_nli (Union[Unset, bool]):  Default: False.
            agentic_session_success (Union[Unset, bool]):  Default: False.
            agentic_workflow_success (Union[Unset, bool]):  Default: False.
            bleu (Union[Unset, bool]):  Default: True.
            chunk_attribution_utilization_gpt (Union[Unset, bool]):  Default: False.
            chunk_attribution_utilization_nli (Union[Unset, bool]):  Default: False.
            completeness_gpt (Union[Unset, bool]):  Default: False.
            completeness_nli (Union[Unset, bool]):  Default: False.
            context_adherence_luna (Union[Unset, bool]):  Default: False.
            context_relevance (Union[Unset, bool]):  Default: False.
            cost (Union[Unset, bool]):  Default: True.
            factuality (Union[Unset, bool]):  Default: False.
            ground_truth_adherence (Union[Unset, bool]):  Default: False.
            groundedness (Union[Unset, bool]):  Default: False.
            input_pii (Union[Unset, bool]):  Default: False.
            input_sexist (Union[Unset, bool]):  Default: False.
            input_sexist_gpt (Union[Unset, bool]):  Default: False.
            input_tone (Union[Unset, bool]):  Default: False.
            input_toxicity (Union[Unset, bool]):  Default: False.
            input_toxicity_gpt (Union[Unset, bool]):  Default: False.
            instruction_adherence (Union[Unset, bool]):  Default: False.
            latency (Union[Unset, bool]):  Default: True.
            pii (Union[Unset, bool]):  Default: False.
            prompt_injection (Union[Unset, bool]):  Default: False.
            prompt_injection_gpt (Union[Unset, bool]):  Default: False.
            prompt_perplexity (Union[Unset, bool]):  Default: False.
            protect_status (Union[Unset, bool]):  Default: True.
            rouge (Union[Unset, bool]):  Default: True.
            sexist (Union[Unset, bool]):  Default: False.
            sexist_gpt (Union[Unset, bool]):  Default: False.
            tone (Union[Unset, bool]):  Default: False.
            tool_error_rate (Union[Unset, bool]):  Default: False.
            tool_error_rate_luna (Union[Unset, bool]):  Default: False.
            tool_selection_quality (Union[Unset, bool]):  Default: False.
            tool_selection_quality_luna (Union[Unset, bool]):  Default: False.
            toxicity (Union[Unset, bool]):  Default: False.
            toxicity_gpt (Union[Unset, bool]):  Default: False.
            uncertainty (Union[Unset, bool]):  Default: False.
    """

    action_advancement_luna: Union[Unset, bool] = False
    action_completion_luna: Union[Unset, bool] = False
    adherence_nli: Union[Unset, bool] = False
    agentic_session_success: Union[Unset, bool] = False
    agentic_workflow_success: Union[Unset, bool] = False
    bleu: Union[Unset, bool] = True
    chunk_attribution_utilization_gpt: Union[Unset, bool] = False
    chunk_attribution_utilization_nli: Union[Unset, bool] = False
    completeness_gpt: Union[Unset, bool] = False
    completeness_nli: Union[Unset, bool] = False
    context_adherence_luna: Union[Unset, bool] = False
    context_relevance: Union[Unset, bool] = False
    cost: Union[Unset, bool] = True
    factuality: Union[Unset, bool] = False
    ground_truth_adherence: Union[Unset, bool] = False
    groundedness: Union[Unset, bool] = False
    input_pii: Union[Unset, bool] = False
    input_sexist: Union[Unset, bool] = False
    input_sexist_gpt: Union[Unset, bool] = False
    input_tone: Union[Unset, bool] = False
    input_toxicity: Union[Unset, bool] = False
    input_toxicity_gpt: Union[Unset, bool] = False
    instruction_adherence: Union[Unset, bool] = False
    latency: Union[Unset, bool] = True
    pii: Union[Unset, bool] = False
    prompt_injection: Union[Unset, bool] = False
    prompt_injection_gpt: Union[Unset, bool] = False
    prompt_perplexity: Union[Unset, bool] = False
    protect_status: Union[Unset, bool] = True
    rouge: Union[Unset, bool] = True
    sexist: Union[Unset, bool] = False
    sexist_gpt: Union[Unset, bool] = False
    tone: Union[Unset, bool] = False
    tool_error_rate: Union[Unset, bool] = False
    tool_error_rate_luna: Union[Unset, bool] = False
    tool_selection_quality: Union[Unset, bool] = False
    tool_selection_quality_luna: Union[Unset, bool] = False
    toxicity: Union[Unset, bool] = False
    toxicity_gpt: Union[Unset, bool] = False
    uncertainty: Union[Unset, bool] = False
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        action_advancement_luna = self.action_advancement_luna

        action_completion_luna = self.action_completion_luna

        adherence_nli = self.adherence_nli

        agentic_session_success = self.agentic_session_success

        agentic_workflow_success = self.agentic_workflow_success

        bleu = self.bleu

        chunk_attribution_utilization_gpt = self.chunk_attribution_utilization_gpt

        chunk_attribution_utilization_nli = self.chunk_attribution_utilization_nli

        completeness_gpt = self.completeness_gpt

        completeness_nli = self.completeness_nli

        context_adherence_luna = self.context_adherence_luna

        context_relevance = self.context_relevance

        cost = self.cost

        factuality = self.factuality

        ground_truth_adherence = self.ground_truth_adherence

        groundedness = self.groundedness

        input_pii = self.input_pii

        input_sexist = self.input_sexist

        input_sexist_gpt = self.input_sexist_gpt

        input_tone = self.input_tone

        input_toxicity = self.input_toxicity

        input_toxicity_gpt = self.input_toxicity_gpt

        instruction_adherence = self.instruction_adherence

        latency = self.latency

        pii = self.pii

        prompt_injection = self.prompt_injection

        prompt_injection_gpt = self.prompt_injection_gpt

        prompt_perplexity = self.prompt_perplexity

        protect_status = self.protect_status

        rouge = self.rouge

        sexist = self.sexist

        sexist_gpt = self.sexist_gpt

        tone = self.tone

        tool_error_rate = self.tool_error_rate

        tool_error_rate_luna = self.tool_error_rate_luna

        tool_selection_quality = self.tool_selection_quality

        tool_selection_quality_luna = self.tool_selection_quality_luna

        toxicity = self.toxicity

        toxicity_gpt = self.toxicity_gpt

        uncertainty = self.uncertainty

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if action_advancement_luna is not UNSET:
            field_dict["action_advancement_luna"] = action_advancement_luna
        if action_completion_luna is not UNSET:
            field_dict["action_completion_luna"] = action_completion_luna
        if adherence_nli is not UNSET:
            field_dict["adherence_nli"] = adherence_nli
        if agentic_session_success is not UNSET:
            field_dict["agentic_session_success"] = agentic_session_success
        if agentic_workflow_success is not UNSET:
            field_dict["agentic_workflow_success"] = agentic_workflow_success
        if bleu is not UNSET:
            field_dict["bleu"] = bleu
        if chunk_attribution_utilization_gpt is not UNSET:
            field_dict["chunk_attribution_utilization_gpt"] = chunk_attribution_utilization_gpt
        if chunk_attribution_utilization_nli is not UNSET:
            field_dict["chunk_attribution_utilization_nli"] = chunk_attribution_utilization_nli
        if completeness_gpt is not UNSET:
            field_dict["completeness_gpt"] = completeness_gpt
        if completeness_nli is not UNSET:
            field_dict["completeness_nli"] = completeness_nli
        if context_adherence_luna is not UNSET:
            field_dict["context_adherence_luna"] = context_adherence_luna
        if context_relevance is not UNSET:
            field_dict["context_relevance"] = context_relevance
        if cost is not UNSET:
            field_dict["cost"] = cost
        if factuality is not UNSET:
            field_dict["factuality"] = factuality
        if ground_truth_adherence is not UNSET:
            field_dict["ground_truth_adherence"] = ground_truth_adherence
        if groundedness is not UNSET:
            field_dict["groundedness"] = groundedness
        if input_pii is not UNSET:
            field_dict["input_pii"] = input_pii
        if input_sexist is not UNSET:
            field_dict["input_sexist"] = input_sexist
        if input_sexist_gpt is not UNSET:
            field_dict["input_sexist_gpt"] = input_sexist_gpt
        if input_tone is not UNSET:
            field_dict["input_tone"] = input_tone
        if input_toxicity is not UNSET:
            field_dict["input_toxicity"] = input_toxicity
        if input_toxicity_gpt is not UNSET:
            field_dict["input_toxicity_gpt"] = input_toxicity_gpt
        if instruction_adherence is not UNSET:
            field_dict["instruction_adherence"] = instruction_adherence
        if latency is not UNSET:
            field_dict["latency"] = latency
        if pii is not UNSET:
            field_dict["pii"] = pii
        if prompt_injection is not UNSET:
            field_dict["prompt_injection"] = prompt_injection
        if prompt_injection_gpt is not UNSET:
            field_dict["prompt_injection_gpt"] = prompt_injection_gpt
        if prompt_perplexity is not UNSET:
            field_dict["prompt_perplexity"] = prompt_perplexity
        if protect_status is not UNSET:
            field_dict["protect_status"] = protect_status
        if rouge is not UNSET:
            field_dict["rouge"] = rouge
        if sexist is not UNSET:
            field_dict["sexist"] = sexist
        if sexist_gpt is not UNSET:
            field_dict["sexist_gpt"] = sexist_gpt
        if tone is not UNSET:
            field_dict["tone"] = tone
        if tool_error_rate is not UNSET:
            field_dict["tool_error_rate"] = tool_error_rate
        if tool_error_rate_luna is not UNSET:
            field_dict["tool_error_rate_luna"] = tool_error_rate_luna
        if tool_selection_quality is not UNSET:
            field_dict["tool_selection_quality"] = tool_selection_quality
        if tool_selection_quality_luna is not UNSET:
            field_dict["tool_selection_quality_luna"] = tool_selection_quality_luna
        if toxicity is not UNSET:
            field_dict["toxicity"] = toxicity
        if toxicity_gpt is not UNSET:
            field_dict["toxicity_gpt"] = toxicity_gpt
        if uncertainty is not UNSET:
            field_dict["uncertainty"] = uncertainty

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        action_advancement_luna = d.pop("action_advancement_luna", UNSET)

        action_completion_luna = d.pop("action_completion_luna", UNSET)

        adherence_nli = d.pop("adherence_nli", UNSET)

        agentic_session_success = d.pop("agentic_session_success", UNSET)

        agentic_workflow_success = d.pop("agentic_workflow_success", UNSET)

        bleu = d.pop("bleu", UNSET)

        chunk_attribution_utilization_gpt = d.pop("chunk_attribution_utilization_gpt", UNSET)

        chunk_attribution_utilization_nli = d.pop("chunk_attribution_utilization_nli", UNSET)

        completeness_gpt = d.pop("completeness_gpt", UNSET)

        completeness_nli = d.pop("completeness_nli", UNSET)

        context_adherence_luna = d.pop("context_adherence_luna", UNSET)

        context_relevance = d.pop("context_relevance", UNSET)

        cost = d.pop("cost", UNSET)

        factuality = d.pop("factuality", UNSET)

        ground_truth_adherence = d.pop("ground_truth_adherence", UNSET)

        groundedness = d.pop("groundedness", UNSET)

        input_pii = d.pop("input_pii", UNSET)

        input_sexist = d.pop("input_sexist", UNSET)

        input_sexist_gpt = d.pop("input_sexist_gpt", UNSET)

        input_tone = d.pop("input_tone", UNSET)

        input_toxicity = d.pop("input_toxicity", UNSET)

        input_toxicity_gpt = d.pop("input_toxicity_gpt", UNSET)

        instruction_adherence = d.pop("instruction_adherence", UNSET)

        latency = d.pop("latency", UNSET)

        pii = d.pop("pii", UNSET)

        prompt_injection = d.pop("prompt_injection", UNSET)

        prompt_injection_gpt = d.pop("prompt_injection_gpt", UNSET)

        prompt_perplexity = d.pop("prompt_perplexity", UNSET)

        protect_status = d.pop("protect_status", UNSET)

        rouge = d.pop("rouge", UNSET)

        sexist = d.pop("sexist", UNSET)

        sexist_gpt = d.pop("sexist_gpt", UNSET)

        tone = d.pop("tone", UNSET)

        tool_error_rate = d.pop("tool_error_rate", UNSET)

        tool_error_rate_luna = d.pop("tool_error_rate_luna", UNSET)

        tool_selection_quality = d.pop("tool_selection_quality", UNSET)

        tool_selection_quality_luna = d.pop("tool_selection_quality_luna", UNSET)

        toxicity = d.pop("toxicity", UNSET)

        toxicity_gpt = d.pop("toxicity_gpt", UNSET)

        uncertainty = d.pop("uncertainty", UNSET)

        scorers_configuration = cls(
            action_advancement_luna=action_advancement_luna,
            action_completion_luna=action_completion_luna,
            adherence_nli=adherence_nli,
            agentic_session_success=agentic_session_success,
            agentic_workflow_success=agentic_workflow_success,
            bleu=bleu,
            chunk_attribution_utilization_gpt=chunk_attribution_utilization_gpt,
            chunk_attribution_utilization_nli=chunk_attribution_utilization_nli,
            completeness_gpt=completeness_gpt,
            completeness_nli=completeness_nli,
            context_adherence_luna=context_adherence_luna,
            context_relevance=context_relevance,
            cost=cost,
            factuality=factuality,
            ground_truth_adherence=ground_truth_adherence,
            groundedness=groundedness,
            input_pii=input_pii,
            input_sexist=input_sexist,
            input_sexist_gpt=input_sexist_gpt,
            input_tone=input_tone,
            input_toxicity=input_toxicity,
            input_toxicity_gpt=input_toxicity_gpt,
            instruction_adherence=instruction_adherence,
            latency=latency,
            pii=pii,
            prompt_injection=prompt_injection,
            prompt_injection_gpt=prompt_injection_gpt,
            prompt_perplexity=prompt_perplexity,
            protect_status=protect_status,
            rouge=rouge,
            sexist=sexist,
            sexist_gpt=sexist_gpt,
            tone=tone,
            tool_error_rate=tool_error_rate,
            tool_error_rate_luna=tool_error_rate_luna,
            tool_selection_quality=tool_selection_quality,
            tool_selection_quality_luna=tool_selection_quality_luna,
            toxicity=toxicity,
            toxicity_gpt=toxicity_gpt,
            uncertainty=uncertainty,
        )

        scorers_configuration.additional_properties = d
        return scorers_configuration

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
