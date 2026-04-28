from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="ScorersConfiguration")


@_attrs_define
class ScorersConfiguration:
    """Configure which scorers to enable for a particular prompt run.

    The keys here are sorted by their approximate execution time to execute the scorers that we anticipate will be the
    fastest first, and the slowest last.

    Attributes
    ----------
            latency (bool | Unset):  Default: True.
            cost (bool | Unset):  Default: True.
            pii (bool | Unset):  Default: False.
            input_pii (bool | Unset):  Default: False.
            bleu (bool | Unset):  Default: True.
            rouge (bool | Unset):  Default: True.
            protect_status (bool | Unset):  Default: True.
            context_relevance (bool | Unset):  Default: False.
            toxicity (bool | Unset):  Default: False.
            input_toxicity (bool | Unset):  Default: False.
            tone (bool | Unset):  Default: False.
            input_tone (bool | Unset):  Default: False.
            sexist (bool | Unset):  Default: False.
            input_sexist (bool | Unset):  Default: False.
            prompt_injection (bool | Unset):  Default: False.
            adherence_nli (bool | Unset):  Default: False.
            chunk_attribution_utilization_nli (bool | Unset):  Default: False.
            context_adherence_luna (bool | Unset):  Default: False.
            context_relevance_luna (bool | Unset):  Default: False.
            chunk_relevance_luna (bool | Unset):  Default: False.
            completeness_nli (bool | Unset):  Default: False.
            tool_error_rate_luna (bool | Unset):  Default: False.
            tool_selection_quality_luna (bool | Unset):  Default: False.
            action_completion_luna (bool | Unset):  Default: False.
            action_advancement_luna (bool | Unset):  Default: False.
            uncertainty (bool | Unset):  Default: False.
            factuality (bool | Unset):  Default: False.
            groundedness (bool | Unset):  Default: False.
            prompt_perplexity (bool | Unset):  Default: False.
            chunk_attribution_utilization_gpt (bool | Unset):  Default: False.
            completeness_gpt (bool | Unset):  Default: False.
            instruction_adherence (bool | Unset):  Default: False.
            ground_truth_adherence (bool | Unset):  Default: False.
            tool_selection_quality (bool | Unset):  Default: False.
            tool_error_rate (bool | Unset):  Default: False.
            agentic_session_success (bool | Unset):  Default: False.
            agentic_workflow_success (bool | Unset):  Default: False.
            prompt_injection_gpt (bool | Unset):  Default: False.
            sexist_gpt (bool | Unset):  Default: False.
            input_sexist_gpt (bool | Unset):  Default: False.
            toxicity_gpt (bool | Unset):  Default: False.
            input_toxicity_gpt (bool | Unset):  Default: False.
    """

    latency: bool | Unset = True
    cost: bool | Unset = True
    pii: bool | Unset = False
    input_pii: bool | Unset = False
    bleu: bool | Unset = True
    rouge: bool | Unset = True
    protect_status: bool | Unset = True
    context_relevance: bool | Unset = False
    toxicity: bool | Unset = False
    input_toxicity: bool | Unset = False
    tone: bool | Unset = False
    input_tone: bool | Unset = False
    sexist: bool | Unset = False
    input_sexist: bool | Unset = False
    prompt_injection: bool | Unset = False
    adherence_nli: bool | Unset = False
    chunk_attribution_utilization_nli: bool | Unset = False
    context_adherence_luna: bool | Unset = False
    context_relevance_luna: bool | Unset = False
    chunk_relevance_luna: bool | Unset = False
    completeness_nli: bool | Unset = False
    tool_error_rate_luna: bool | Unset = False
    tool_selection_quality_luna: bool | Unset = False
    action_completion_luna: bool | Unset = False
    action_advancement_luna: bool | Unset = False
    uncertainty: bool | Unset = False
    factuality: bool | Unset = False
    groundedness: bool | Unset = False
    prompt_perplexity: bool | Unset = False
    chunk_attribution_utilization_gpt: bool | Unset = False
    completeness_gpt: bool | Unset = False
    instruction_adherence: bool | Unset = False
    ground_truth_adherence: bool | Unset = False
    tool_selection_quality: bool | Unset = False
    tool_error_rate: bool | Unset = False
    agentic_session_success: bool | Unset = False
    agentic_workflow_success: bool | Unset = False
    prompt_injection_gpt: bool | Unset = False
    sexist_gpt: bool | Unset = False
    input_sexist_gpt: bool | Unset = False
    toxicity_gpt: bool | Unset = False
    input_toxicity_gpt: bool | Unset = False
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        latency = self.latency

        cost = self.cost

        pii = self.pii

        input_pii = self.input_pii

        bleu = self.bleu

        rouge = self.rouge

        protect_status = self.protect_status

        context_relevance = self.context_relevance

        toxicity = self.toxicity

        input_toxicity = self.input_toxicity

        tone = self.tone

        input_tone = self.input_tone

        sexist = self.sexist

        input_sexist = self.input_sexist

        prompt_injection = self.prompt_injection

        adherence_nli = self.adherence_nli

        chunk_attribution_utilization_nli = self.chunk_attribution_utilization_nli

        context_adherence_luna = self.context_adherence_luna

        context_relevance_luna = self.context_relevance_luna

        chunk_relevance_luna = self.chunk_relevance_luna

        completeness_nli = self.completeness_nli

        tool_error_rate_luna = self.tool_error_rate_luna

        tool_selection_quality_luna = self.tool_selection_quality_luna

        action_completion_luna = self.action_completion_luna

        action_advancement_luna = self.action_advancement_luna

        uncertainty = self.uncertainty

        factuality = self.factuality

        groundedness = self.groundedness

        prompt_perplexity = self.prompt_perplexity

        chunk_attribution_utilization_gpt = self.chunk_attribution_utilization_gpt

        completeness_gpt = self.completeness_gpt

        instruction_adherence = self.instruction_adherence

        ground_truth_adherence = self.ground_truth_adherence

        tool_selection_quality = self.tool_selection_quality

        tool_error_rate = self.tool_error_rate

        agentic_session_success = self.agentic_session_success

        agentic_workflow_success = self.agentic_workflow_success

        prompt_injection_gpt = self.prompt_injection_gpt

        sexist_gpt = self.sexist_gpt

        input_sexist_gpt = self.input_sexist_gpt

        toxicity_gpt = self.toxicity_gpt

        input_toxicity_gpt = self.input_toxicity_gpt

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if latency is not UNSET:
            field_dict["latency"] = latency
        if cost is not UNSET:
            field_dict["cost"] = cost
        if pii is not UNSET:
            field_dict["pii"] = pii
        if input_pii is not UNSET:
            field_dict["input_pii"] = input_pii
        if bleu is not UNSET:
            field_dict["bleu"] = bleu
        if rouge is not UNSET:
            field_dict["rouge"] = rouge
        if protect_status is not UNSET:
            field_dict["protect_status"] = protect_status
        if context_relevance is not UNSET:
            field_dict["context_relevance"] = context_relevance
        if toxicity is not UNSET:
            field_dict["toxicity"] = toxicity
        if input_toxicity is not UNSET:
            field_dict["input_toxicity"] = input_toxicity
        if tone is not UNSET:
            field_dict["tone"] = tone
        if input_tone is not UNSET:
            field_dict["input_tone"] = input_tone
        if sexist is not UNSET:
            field_dict["sexist"] = sexist
        if input_sexist is not UNSET:
            field_dict["input_sexist"] = input_sexist
        if prompt_injection is not UNSET:
            field_dict["prompt_injection"] = prompt_injection
        if adherence_nli is not UNSET:
            field_dict["adherence_nli"] = adherence_nli
        if chunk_attribution_utilization_nli is not UNSET:
            field_dict["chunk_attribution_utilization_nli"] = chunk_attribution_utilization_nli
        if context_adherence_luna is not UNSET:
            field_dict["context_adherence_luna"] = context_adherence_luna
        if context_relevance_luna is not UNSET:
            field_dict["context_relevance_luna"] = context_relevance_luna
        if chunk_relevance_luna is not UNSET:
            field_dict["chunk_relevance_luna"] = chunk_relevance_luna
        if completeness_nli is not UNSET:
            field_dict["completeness_nli"] = completeness_nli
        if tool_error_rate_luna is not UNSET:
            field_dict["tool_error_rate_luna"] = tool_error_rate_luna
        if tool_selection_quality_luna is not UNSET:
            field_dict["tool_selection_quality_luna"] = tool_selection_quality_luna
        if action_completion_luna is not UNSET:
            field_dict["action_completion_luna"] = action_completion_luna
        if action_advancement_luna is not UNSET:
            field_dict["action_advancement_luna"] = action_advancement_luna
        if uncertainty is not UNSET:
            field_dict["uncertainty"] = uncertainty
        if factuality is not UNSET:
            field_dict["factuality"] = factuality
        if groundedness is not UNSET:
            field_dict["groundedness"] = groundedness
        if prompt_perplexity is not UNSET:
            field_dict["prompt_perplexity"] = prompt_perplexity
        if chunk_attribution_utilization_gpt is not UNSET:
            field_dict["chunk_attribution_utilization_gpt"] = chunk_attribution_utilization_gpt
        if completeness_gpt is not UNSET:
            field_dict["completeness_gpt"] = completeness_gpt
        if instruction_adherence is not UNSET:
            field_dict["instruction_adherence"] = instruction_adherence
        if ground_truth_adherence is not UNSET:
            field_dict["ground_truth_adherence"] = ground_truth_adherence
        if tool_selection_quality is not UNSET:
            field_dict["tool_selection_quality"] = tool_selection_quality
        if tool_error_rate is not UNSET:
            field_dict["tool_error_rate"] = tool_error_rate
        if agentic_session_success is not UNSET:
            field_dict["agentic_session_success"] = agentic_session_success
        if agentic_workflow_success is not UNSET:
            field_dict["agentic_workflow_success"] = agentic_workflow_success
        if prompt_injection_gpt is not UNSET:
            field_dict["prompt_injection_gpt"] = prompt_injection_gpt
        if sexist_gpt is not UNSET:
            field_dict["sexist_gpt"] = sexist_gpt
        if input_sexist_gpt is not UNSET:
            field_dict["input_sexist_gpt"] = input_sexist_gpt
        if toxicity_gpt is not UNSET:
            field_dict["toxicity_gpt"] = toxicity_gpt
        if input_toxicity_gpt is not UNSET:
            field_dict["input_toxicity_gpt"] = input_toxicity_gpt

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        latency = d.pop("latency", UNSET)

        cost = d.pop("cost", UNSET)

        pii = d.pop("pii", UNSET)

        input_pii = d.pop("input_pii", UNSET)

        bleu = d.pop("bleu", UNSET)

        rouge = d.pop("rouge", UNSET)

        protect_status = d.pop("protect_status", UNSET)

        context_relevance = d.pop("context_relevance", UNSET)

        toxicity = d.pop("toxicity", UNSET)

        input_toxicity = d.pop("input_toxicity", UNSET)

        tone = d.pop("tone", UNSET)

        input_tone = d.pop("input_tone", UNSET)

        sexist = d.pop("sexist", UNSET)

        input_sexist = d.pop("input_sexist", UNSET)

        prompt_injection = d.pop("prompt_injection", UNSET)

        adherence_nli = d.pop("adherence_nli", UNSET)

        chunk_attribution_utilization_nli = d.pop("chunk_attribution_utilization_nli", UNSET)

        context_adherence_luna = d.pop("context_adherence_luna", UNSET)

        context_relevance_luna = d.pop("context_relevance_luna", UNSET)

        chunk_relevance_luna = d.pop("chunk_relevance_luna", UNSET)

        completeness_nli = d.pop("completeness_nli", UNSET)

        tool_error_rate_luna = d.pop("tool_error_rate_luna", UNSET)

        tool_selection_quality_luna = d.pop("tool_selection_quality_luna", UNSET)

        action_completion_luna = d.pop("action_completion_luna", UNSET)

        action_advancement_luna = d.pop("action_advancement_luna", UNSET)

        uncertainty = d.pop("uncertainty", UNSET)

        factuality = d.pop("factuality", UNSET)

        groundedness = d.pop("groundedness", UNSET)

        prompt_perplexity = d.pop("prompt_perplexity", UNSET)

        chunk_attribution_utilization_gpt = d.pop("chunk_attribution_utilization_gpt", UNSET)

        completeness_gpt = d.pop("completeness_gpt", UNSET)

        instruction_adherence = d.pop("instruction_adherence", UNSET)

        ground_truth_adherence = d.pop("ground_truth_adherence", UNSET)

        tool_selection_quality = d.pop("tool_selection_quality", UNSET)

        tool_error_rate = d.pop("tool_error_rate", UNSET)

        agentic_session_success = d.pop("agentic_session_success", UNSET)

        agentic_workflow_success = d.pop("agentic_workflow_success", UNSET)

        prompt_injection_gpt = d.pop("prompt_injection_gpt", UNSET)

        sexist_gpt = d.pop("sexist_gpt", UNSET)

        input_sexist_gpt = d.pop("input_sexist_gpt", UNSET)

        toxicity_gpt = d.pop("toxicity_gpt", UNSET)

        input_toxicity_gpt = d.pop("input_toxicity_gpt", UNSET)

        scorers_configuration = cls(
            latency=latency,
            cost=cost,
            pii=pii,
            input_pii=input_pii,
            bleu=bleu,
            rouge=rouge,
            protect_status=protect_status,
            context_relevance=context_relevance,
            toxicity=toxicity,
            input_toxicity=input_toxicity,
            tone=tone,
            input_tone=input_tone,
            sexist=sexist,
            input_sexist=input_sexist,
            prompt_injection=prompt_injection,
            adherence_nli=adherence_nli,
            chunk_attribution_utilization_nli=chunk_attribution_utilization_nli,
            context_adherence_luna=context_adherence_luna,
            context_relevance_luna=context_relevance_luna,
            chunk_relevance_luna=chunk_relevance_luna,
            completeness_nli=completeness_nli,
            tool_error_rate_luna=tool_error_rate_luna,
            tool_selection_quality_luna=tool_selection_quality_luna,
            action_completion_luna=action_completion_luna,
            action_advancement_luna=action_advancement_luna,
            uncertainty=uncertainty,
            factuality=factuality,
            groundedness=groundedness,
            prompt_perplexity=prompt_perplexity,
            chunk_attribution_utilization_gpt=chunk_attribution_utilization_gpt,
            completeness_gpt=completeness_gpt,
            instruction_adherence=instruction_adherence,
            ground_truth_adherence=ground_truth_adherence,
            tool_selection_quality=tool_selection_quality,
            tool_error_rate=tool_error_rate,
            agentic_session_success=agentic_session_success,
            agentic_workflow_success=agentic_workflow_success,
            prompt_injection_gpt=prompt_injection_gpt,
            sexist_gpt=sexist_gpt,
            input_sexist_gpt=input_sexist_gpt,
            toxicity_gpt=toxicity_gpt,
            input_toxicity_gpt=input_toxicity_gpt,
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
