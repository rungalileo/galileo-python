from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="AggregateMetrics")


@_attrs_define
class AggregateMetrics:
    """
    Attributes:
        average_action_advancement_luna (float | None | Unset):
        average_action_completion_luna (float | None | Unset):
        average_agentic_workflow_success (float | None | Unset):
        average_agentic_session_success (float | None | Unset):
        average_completeness_gpt (float | None | Unset):
        average_factuality (float | None | Unset):
        average_groundedness (float | None | Unset):
        average_input_sexist (float | None | Unset):
        average_input_token_length (float | None | Unset):
        average_input_toxicity (float | None | Unset):
        average_instruction_adherence (float | None | Unset):
        average_latency (float | None | Unset):
        average_output_token_length (float | None | Unset):
        average_prompt_perplexity (float | None | Unset):
        average_retriever_attribution (float | None | Unset):
        average_retriever_utilization (float | None | Unset):
        average_sexist (float | None | Unset):
        average_tool_selection_quality (float | None | Unset):
        average_tool_selection_quality_luna (float | None | Unset):
        average_tool_error_rate (float | None | Unset):
        average_tool_error_rate_luna (float | None | Unset):
        count_tool_error_rate (float | None | Unset):
        average_toxicity (float | None | Unset):
        average_total_token_length (float | None | Unset):
        failures_count (int | None | Unset):  Default: 0.
        requests_count (int | None | Unset):  Default: 0.
        total_cost (float | None | Unset):  Default: 0.0.
    """

    average_action_advancement_luna: float | None | Unset = UNSET
    average_action_completion_luna: float | None | Unset = UNSET
    average_agentic_workflow_success: float | None | Unset = UNSET
    average_agentic_session_success: float | None | Unset = UNSET
    average_completeness_gpt: float | None | Unset = UNSET
    average_factuality: float | None | Unset = UNSET
    average_groundedness: float | None | Unset = UNSET
    average_input_sexist: float | None | Unset = UNSET
    average_input_token_length: float | None | Unset = UNSET
    average_input_toxicity: float | None | Unset = UNSET
    average_instruction_adherence: float | None | Unset = UNSET
    average_latency: float | None | Unset = UNSET
    average_output_token_length: float | None | Unset = UNSET
    average_prompt_perplexity: float | None | Unset = UNSET
    average_retriever_attribution: float | None | Unset = UNSET
    average_retriever_utilization: float | None | Unset = UNSET
    average_sexist: float | None | Unset = UNSET
    average_tool_selection_quality: float | None | Unset = UNSET
    average_tool_selection_quality_luna: float | None | Unset = UNSET
    average_tool_error_rate: float | None | Unset = UNSET
    average_tool_error_rate_luna: float | None | Unset = UNSET
    count_tool_error_rate: float | None | Unset = UNSET
    average_toxicity: float | None | Unset = UNSET
    average_total_token_length: float | None | Unset = UNSET
    failures_count: int | None | Unset = 0
    requests_count: int | None | Unset = 0
    total_cost: float | None | Unset = 0.0
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        average_action_advancement_luna: float | None | Unset
        if isinstance(self.average_action_advancement_luna, Unset):
            average_action_advancement_luna = UNSET
        else:
            average_action_advancement_luna = self.average_action_advancement_luna

        average_action_completion_luna: float | None | Unset
        if isinstance(self.average_action_completion_luna, Unset):
            average_action_completion_luna = UNSET
        else:
            average_action_completion_luna = self.average_action_completion_luna

        average_agentic_workflow_success: float | None | Unset
        if isinstance(self.average_agentic_workflow_success, Unset):
            average_agentic_workflow_success = UNSET
        else:
            average_agentic_workflow_success = self.average_agentic_workflow_success

        average_agentic_session_success: float | None | Unset
        if isinstance(self.average_agentic_session_success, Unset):
            average_agentic_session_success = UNSET
        else:
            average_agentic_session_success = self.average_agentic_session_success

        average_completeness_gpt: float | None | Unset
        if isinstance(self.average_completeness_gpt, Unset):
            average_completeness_gpt = UNSET
        else:
            average_completeness_gpt = self.average_completeness_gpt

        average_factuality: float | None | Unset
        if isinstance(self.average_factuality, Unset):
            average_factuality = UNSET
        else:
            average_factuality = self.average_factuality

        average_groundedness: float | None | Unset
        if isinstance(self.average_groundedness, Unset):
            average_groundedness = UNSET
        else:
            average_groundedness = self.average_groundedness

        average_input_sexist: float | None | Unset
        if isinstance(self.average_input_sexist, Unset):
            average_input_sexist = UNSET
        else:
            average_input_sexist = self.average_input_sexist

        average_input_token_length: float | None | Unset
        if isinstance(self.average_input_token_length, Unset):
            average_input_token_length = UNSET
        else:
            average_input_token_length = self.average_input_token_length

        average_input_toxicity: float | None | Unset
        if isinstance(self.average_input_toxicity, Unset):
            average_input_toxicity = UNSET
        else:
            average_input_toxicity = self.average_input_toxicity

        average_instruction_adherence: float | None | Unset
        if isinstance(self.average_instruction_adherence, Unset):
            average_instruction_adherence = UNSET
        else:
            average_instruction_adherence = self.average_instruction_adherence

        average_latency: float | None | Unset
        if isinstance(self.average_latency, Unset):
            average_latency = UNSET
        else:
            average_latency = self.average_latency

        average_output_token_length: float | None | Unset
        if isinstance(self.average_output_token_length, Unset):
            average_output_token_length = UNSET
        else:
            average_output_token_length = self.average_output_token_length

        average_prompt_perplexity: float | None | Unset
        if isinstance(self.average_prompt_perplexity, Unset):
            average_prompt_perplexity = UNSET
        else:
            average_prompt_perplexity = self.average_prompt_perplexity

        average_retriever_attribution: float | None | Unset
        if isinstance(self.average_retriever_attribution, Unset):
            average_retriever_attribution = UNSET
        else:
            average_retriever_attribution = self.average_retriever_attribution

        average_retriever_utilization: float | None | Unset
        if isinstance(self.average_retriever_utilization, Unset):
            average_retriever_utilization = UNSET
        else:
            average_retriever_utilization = self.average_retriever_utilization

        average_sexist: float | None | Unset
        if isinstance(self.average_sexist, Unset):
            average_sexist = UNSET
        else:
            average_sexist = self.average_sexist

        average_tool_selection_quality: float | None | Unset
        if isinstance(self.average_tool_selection_quality, Unset):
            average_tool_selection_quality = UNSET
        else:
            average_tool_selection_quality = self.average_tool_selection_quality

        average_tool_selection_quality_luna: float | None | Unset
        if isinstance(self.average_tool_selection_quality_luna, Unset):
            average_tool_selection_quality_luna = UNSET
        else:
            average_tool_selection_quality_luna = self.average_tool_selection_quality_luna

        average_tool_error_rate: float | None | Unset
        if isinstance(self.average_tool_error_rate, Unset):
            average_tool_error_rate = UNSET
        else:
            average_tool_error_rate = self.average_tool_error_rate

        average_tool_error_rate_luna: float | None | Unset
        if isinstance(self.average_tool_error_rate_luna, Unset):
            average_tool_error_rate_luna = UNSET
        else:
            average_tool_error_rate_luna = self.average_tool_error_rate_luna

        count_tool_error_rate: float | None | Unset
        if isinstance(self.count_tool_error_rate, Unset):
            count_tool_error_rate = UNSET
        else:
            count_tool_error_rate = self.count_tool_error_rate

        average_toxicity: float | None | Unset
        if isinstance(self.average_toxicity, Unset):
            average_toxicity = UNSET
        else:
            average_toxicity = self.average_toxicity

        average_total_token_length: float | None | Unset
        if isinstance(self.average_total_token_length, Unset):
            average_total_token_length = UNSET
        else:
            average_total_token_length = self.average_total_token_length

        failures_count: int | None | Unset
        if isinstance(self.failures_count, Unset):
            failures_count = UNSET
        else:
            failures_count = self.failures_count

        requests_count: int | None | Unset
        if isinstance(self.requests_count, Unset):
            requests_count = UNSET
        else:
            requests_count = self.requests_count

        total_cost: float | None | Unset
        if isinstance(self.total_cost, Unset):
            total_cost = UNSET
        else:
            total_cost = self.total_cost

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if average_action_advancement_luna is not UNSET:
            field_dict["average_action_advancement_luna"] = average_action_advancement_luna
        if average_action_completion_luna is not UNSET:
            field_dict["average_action_completion_luna"] = average_action_completion_luna
        if average_agentic_workflow_success is not UNSET:
            field_dict["average_agentic_workflow_success"] = average_agentic_workflow_success
        if average_agentic_session_success is not UNSET:
            field_dict["average_agentic_session_success"] = average_agentic_session_success
        if average_completeness_gpt is not UNSET:
            field_dict["average_completeness_gpt"] = average_completeness_gpt
        if average_factuality is not UNSET:
            field_dict["average_factuality"] = average_factuality
        if average_groundedness is not UNSET:
            field_dict["average_groundedness"] = average_groundedness
        if average_input_sexist is not UNSET:
            field_dict["average_input_sexist"] = average_input_sexist
        if average_input_token_length is not UNSET:
            field_dict["average_input_token_length"] = average_input_token_length
        if average_input_toxicity is not UNSET:
            field_dict["average_input_toxicity"] = average_input_toxicity
        if average_instruction_adherence is not UNSET:
            field_dict["average_instruction_adherence"] = average_instruction_adherence
        if average_latency is not UNSET:
            field_dict["average_latency"] = average_latency
        if average_output_token_length is not UNSET:
            field_dict["average_output_token_length"] = average_output_token_length
        if average_prompt_perplexity is not UNSET:
            field_dict["average_prompt_perplexity"] = average_prompt_perplexity
        if average_retriever_attribution is not UNSET:
            field_dict["average_retriever_attribution"] = average_retriever_attribution
        if average_retriever_utilization is not UNSET:
            field_dict["average_retriever_utilization"] = average_retriever_utilization
        if average_sexist is not UNSET:
            field_dict["average_sexist"] = average_sexist
        if average_tool_selection_quality is not UNSET:
            field_dict["average_tool_selection_quality"] = average_tool_selection_quality
        if average_tool_selection_quality_luna is not UNSET:
            field_dict["average_tool_selection_quality_luna"] = average_tool_selection_quality_luna
        if average_tool_error_rate is not UNSET:
            field_dict["average_tool_error_rate"] = average_tool_error_rate
        if average_tool_error_rate_luna is not UNSET:
            field_dict["average_tool_error_rate_luna"] = average_tool_error_rate_luna
        if count_tool_error_rate is not UNSET:
            field_dict["count_tool_error_rate"] = count_tool_error_rate
        if average_toxicity is not UNSET:
            field_dict["average_toxicity"] = average_toxicity
        if average_total_token_length is not UNSET:
            field_dict["average_total_token_length"] = average_total_token_length
        if failures_count is not UNSET:
            field_dict["failures_count"] = failures_count
        if requests_count is not UNSET:
            field_dict["requests_count"] = requests_count
        if total_cost is not UNSET:
            field_dict["total_cost"] = total_cost

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)

        def _parse_average_action_advancement_luna(data: object) -> float | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(float | None | Unset, data)

        average_action_advancement_luna = _parse_average_action_advancement_luna(
            d.pop("average_action_advancement_luna", UNSET)
        )

        def _parse_average_action_completion_luna(data: object) -> float | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(float | None | Unset, data)

        average_action_completion_luna = _parse_average_action_completion_luna(
            d.pop("average_action_completion_luna", UNSET)
        )

        def _parse_average_agentic_workflow_success(data: object) -> float | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(float | None | Unset, data)

        average_agentic_workflow_success = _parse_average_agentic_workflow_success(
            d.pop("average_agentic_workflow_success", UNSET)
        )

        def _parse_average_agentic_session_success(data: object) -> float | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(float | None | Unset, data)

        average_agentic_session_success = _parse_average_agentic_session_success(
            d.pop("average_agentic_session_success", UNSET)
        )

        def _parse_average_completeness_gpt(data: object) -> float | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(float | None | Unset, data)

        average_completeness_gpt = _parse_average_completeness_gpt(d.pop("average_completeness_gpt", UNSET))

        def _parse_average_factuality(data: object) -> float | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(float | None | Unset, data)

        average_factuality = _parse_average_factuality(d.pop("average_factuality", UNSET))

        def _parse_average_groundedness(data: object) -> float | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(float | None | Unset, data)

        average_groundedness = _parse_average_groundedness(d.pop("average_groundedness", UNSET))

        def _parse_average_input_sexist(data: object) -> float | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(float | None | Unset, data)

        average_input_sexist = _parse_average_input_sexist(d.pop("average_input_sexist", UNSET))

        def _parse_average_input_token_length(data: object) -> float | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(float | None | Unset, data)

        average_input_token_length = _parse_average_input_token_length(d.pop("average_input_token_length", UNSET))

        def _parse_average_input_toxicity(data: object) -> float | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(float | None | Unset, data)

        average_input_toxicity = _parse_average_input_toxicity(d.pop("average_input_toxicity", UNSET))

        def _parse_average_instruction_adherence(data: object) -> float | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(float | None | Unset, data)

        average_instruction_adherence = _parse_average_instruction_adherence(
            d.pop("average_instruction_adherence", UNSET)
        )

        def _parse_average_latency(data: object) -> float | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(float | None | Unset, data)

        average_latency = _parse_average_latency(d.pop("average_latency", UNSET))

        def _parse_average_output_token_length(data: object) -> float | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(float | None | Unset, data)

        average_output_token_length = _parse_average_output_token_length(d.pop("average_output_token_length", UNSET))

        def _parse_average_prompt_perplexity(data: object) -> float | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(float | None | Unset, data)

        average_prompt_perplexity = _parse_average_prompt_perplexity(d.pop("average_prompt_perplexity", UNSET))

        def _parse_average_retriever_attribution(data: object) -> float | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(float | None | Unset, data)

        average_retriever_attribution = _parse_average_retriever_attribution(
            d.pop("average_retriever_attribution", UNSET)
        )

        def _parse_average_retriever_utilization(data: object) -> float | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(float | None | Unset, data)

        average_retriever_utilization = _parse_average_retriever_utilization(
            d.pop("average_retriever_utilization", UNSET)
        )

        def _parse_average_sexist(data: object) -> float | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(float | None | Unset, data)

        average_sexist = _parse_average_sexist(d.pop("average_sexist", UNSET))

        def _parse_average_tool_selection_quality(data: object) -> float | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(float | None | Unset, data)

        average_tool_selection_quality = _parse_average_tool_selection_quality(
            d.pop("average_tool_selection_quality", UNSET)
        )

        def _parse_average_tool_selection_quality_luna(data: object) -> float | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(float | None | Unset, data)

        average_tool_selection_quality_luna = _parse_average_tool_selection_quality_luna(
            d.pop("average_tool_selection_quality_luna", UNSET)
        )

        def _parse_average_tool_error_rate(data: object) -> float | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(float | None | Unset, data)

        average_tool_error_rate = _parse_average_tool_error_rate(d.pop("average_tool_error_rate", UNSET))

        def _parse_average_tool_error_rate_luna(data: object) -> float | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(float | None | Unset, data)

        average_tool_error_rate_luna = _parse_average_tool_error_rate_luna(d.pop("average_tool_error_rate_luna", UNSET))

        def _parse_count_tool_error_rate(data: object) -> float | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(float | None | Unset, data)

        count_tool_error_rate = _parse_count_tool_error_rate(d.pop("count_tool_error_rate", UNSET))

        def _parse_average_toxicity(data: object) -> float | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(float | None | Unset, data)

        average_toxicity = _parse_average_toxicity(d.pop("average_toxicity", UNSET))

        def _parse_average_total_token_length(data: object) -> float | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(float | None | Unset, data)

        average_total_token_length = _parse_average_total_token_length(d.pop("average_total_token_length", UNSET))

        def _parse_failures_count(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        failures_count = _parse_failures_count(d.pop("failures_count", UNSET))

        def _parse_requests_count(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        requests_count = _parse_requests_count(d.pop("requests_count", UNSET))

        def _parse_total_cost(data: object) -> float | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(float | None | Unset, data)

        total_cost = _parse_total_cost(d.pop("total_cost", UNSET))

        aggregate_metrics = cls(
            average_action_advancement_luna=average_action_advancement_luna,
            average_action_completion_luna=average_action_completion_luna,
            average_agentic_workflow_success=average_agentic_workflow_success,
            average_agentic_session_success=average_agentic_session_success,
            average_completeness_gpt=average_completeness_gpt,
            average_factuality=average_factuality,
            average_groundedness=average_groundedness,
            average_input_sexist=average_input_sexist,
            average_input_token_length=average_input_token_length,
            average_input_toxicity=average_input_toxicity,
            average_instruction_adherence=average_instruction_adherence,
            average_latency=average_latency,
            average_output_token_length=average_output_token_length,
            average_prompt_perplexity=average_prompt_perplexity,
            average_retriever_attribution=average_retriever_attribution,
            average_retriever_utilization=average_retriever_utilization,
            average_sexist=average_sexist,
            average_tool_selection_quality=average_tool_selection_quality,
            average_tool_selection_quality_luna=average_tool_selection_quality_luna,
            average_tool_error_rate=average_tool_error_rate,
            average_tool_error_rate_luna=average_tool_error_rate_luna,
            count_tool_error_rate=count_tool_error_rate,
            average_toxicity=average_toxicity,
            average_total_token_length=average_total_token_length,
            failures_count=failures_count,
            requests_count=requests_count,
            total_cost=total_cost,
        )

        aggregate_metrics.additional_properties = d
        return aggregate_metrics

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
