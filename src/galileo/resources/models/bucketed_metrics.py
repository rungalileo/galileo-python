import datetime
from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="BucketedMetrics")


@_attrs_define
class BucketedMetrics:
    """
    Attributes:
        end_bucket_time (datetime.datetime):
        start_bucket_time (datetime.datetime):
        average_agentic_workflow_success (Union[None, Unset, float]):
        average_completeness_gpt (Union[None, Unset, float]):
        average_factuality (Union[None, Unset, float]):
        average_groundedness (Union[None, Unset, float]):
        average_input_sexist (Union[None, Unset, float]):
        average_input_token_length (Union[None, Unset, float]):
        average_input_toxicity (Union[None, Unset, float]):
        average_instruction_adherence (Union[None, Unset, float]):
        average_latency (Union[None, Unset, float]):
        average_output_token_length (Union[None, Unset, float]):
        average_prompt_perplexity (Union[None, Unset, float]):
        average_retriever_attribution (Union[None, Unset, float]):
        average_retriever_utilization (Union[None, Unset, float]):
        average_sexist (Union[None, Unset, float]):
        average_tool_error_rate (Union[None, Unset, float]):
        average_tool_selection_quality (Union[None, Unset, float]):
        average_total_token_length (Union[None, Unset, float]):
        average_toxicity (Union[None, Unset, float]):
        failures_count (Union[None, Unset, int]):  Default: 0.
        input_pii_values_count (Union[None, Unset, str]):
        input_tone_values_count (Union[None, Unset, str]):
        pii_values_count (Union[None, Unset, str]):
        prompt_injection_values_count (Union[None, Unset, str]):
        requests_count (Union[None, Unset, int]):  Default: 0.
        tone_values_count (Union[None, Unset, str]):
        total_cost (Union[None, Unset, float]):  Default: 0.0.
    """

    end_bucket_time: datetime.datetime
    start_bucket_time: datetime.datetime
    average_agentic_workflow_success: Union[None, Unset, float] = UNSET
    average_completeness_gpt: Union[None, Unset, float] = UNSET
    average_factuality: Union[None, Unset, float] = UNSET
    average_groundedness: Union[None, Unset, float] = UNSET
    average_input_sexist: Union[None, Unset, float] = UNSET
    average_input_token_length: Union[None, Unset, float] = UNSET
    average_input_toxicity: Union[None, Unset, float] = UNSET
    average_instruction_adherence: Union[None, Unset, float] = UNSET
    average_latency: Union[None, Unset, float] = UNSET
    average_output_token_length: Union[None, Unset, float] = UNSET
    average_prompt_perplexity: Union[None, Unset, float] = UNSET
    average_retriever_attribution: Union[None, Unset, float] = UNSET
    average_retriever_utilization: Union[None, Unset, float] = UNSET
    average_sexist: Union[None, Unset, float] = UNSET
    average_tool_error_rate: Union[None, Unset, float] = UNSET
    average_tool_selection_quality: Union[None, Unset, float] = UNSET
    average_total_token_length: Union[None, Unset, float] = UNSET
    average_toxicity: Union[None, Unset, float] = UNSET
    failures_count: Union[None, Unset, int] = 0
    input_pii_values_count: Union[None, Unset, str] = UNSET
    input_tone_values_count: Union[None, Unset, str] = UNSET
    pii_values_count: Union[None, Unset, str] = UNSET
    prompt_injection_values_count: Union[None, Unset, str] = UNSET
    requests_count: Union[None, Unset, int] = 0
    tone_values_count: Union[None, Unset, str] = UNSET
    total_cost: Union[None, Unset, float] = 0.0
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        end_bucket_time = self.end_bucket_time.isoformat()

        start_bucket_time = self.start_bucket_time.isoformat()

        average_agentic_workflow_success: Union[None, Unset, float]
        if isinstance(self.average_agentic_workflow_success, Unset):
            average_agentic_workflow_success = UNSET
        else:
            average_agentic_workflow_success = self.average_agentic_workflow_success

        average_completeness_gpt: Union[None, Unset, float]
        if isinstance(self.average_completeness_gpt, Unset):
            average_completeness_gpt = UNSET
        else:
            average_completeness_gpt = self.average_completeness_gpt

        average_factuality: Union[None, Unset, float]
        if isinstance(self.average_factuality, Unset):
            average_factuality = UNSET
        else:
            average_factuality = self.average_factuality

        average_groundedness: Union[None, Unset, float]
        if isinstance(self.average_groundedness, Unset):
            average_groundedness = UNSET
        else:
            average_groundedness = self.average_groundedness

        average_input_sexist: Union[None, Unset, float]
        if isinstance(self.average_input_sexist, Unset):
            average_input_sexist = UNSET
        else:
            average_input_sexist = self.average_input_sexist

        average_input_token_length: Union[None, Unset, float]
        if isinstance(self.average_input_token_length, Unset):
            average_input_token_length = UNSET
        else:
            average_input_token_length = self.average_input_token_length

        average_input_toxicity: Union[None, Unset, float]
        if isinstance(self.average_input_toxicity, Unset):
            average_input_toxicity = UNSET
        else:
            average_input_toxicity = self.average_input_toxicity

        average_instruction_adherence: Union[None, Unset, float]
        if isinstance(self.average_instruction_adherence, Unset):
            average_instruction_adherence = UNSET
        else:
            average_instruction_adherence = self.average_instruction_adherence

        average_latency: Union[None, Unset, float]
        if isinstance(self.average_latency, Unset):
            average_latency = UNSET
        else:
            average_latency = self.average_latency

        average_output_token_length: Union[None, Unset, float]
        if isinstance(self.average_output_token_length, Unset):
            average_output_token_length = UNSET
        else:
            average_output_token_length = self.average_output_token_length

        average_prompt_perplexity: Union[None, Unset, float]
        if isinstance(self.average_prompt_perplexity, Unset):
            average_prompt_perplexity = UNSET
        else:
            average_prompt_perplexity = self.average_prompt_perplexity

        average_retriever_attribution: Union[None, Unset, float]
        if isinstance(self.average_retriever_attribution, Unset):
            average_retriever_attribution = UNSET
        else:
            average_retriever_attribution = self.average_retriever_attribution

        average_retriever_utilization: Union[None, Unset, float]
        if isinstance(self.average_retriever_utilization, Unset):
            average_retriever_utilization = UNSET
        else:
            average_retriever_utilization = self.average_retriever_utilization

        average_sexist: Union[None, Unset, float]
        if isinstance(self.average_sexist, Unset):
            average_sexist = UNSET
        else:
            average_sexist = self.average_sexist

        average_tool_error_rate: Union[None, Unset, float]
        if isinstance(self.average_tool_error_rate, Unset):
            average_tool_error_rate = UNSET
        else:
            average_tool_error_rate = self.average_tool_error_rate

        average_tool_selection_quality: Union[None, Unset, float]
        if isinstance(self.average_tool_selection_quality, Unset):
            average_tool_selection_quality = UNSET
        else:
            average_tool_selection_quality = self.average_tool_selection_quality

        average_total_token_length: Union[None, Unset, float]
        if isinstance(self.average_total_token_length, Unset):
            average_total_token_length = UNSET
        else:
            average_total_token_length = self.average_total_token_length

        average_toxicity: Union[None, Unset, float]
        if isinstance(self.average_toxicity, Unset):
            average_toxicity = UNSET
        else:
            average_toxicity = self.average_toxicity

        failures_count: Union[None, Unset, int]
        if isinstance(self.failures_count, Unset):
            failures_count = UNSET
        else:
            failures_count = self.failures_count

        input_pii_values_count: Union[None, Unset, str]
        if isinstance(self.input_pii_values_count, Unset):
            input_pii_values_count = UNSET
        else:
            input_pii_values_count = self.input_pii_values_count

        input_tone_values_count: Union[None, Unset, str]
        if isinstance(self.input_tone_values_count, Unset):
            input_tone_values_count = UNSET
        else:
            input_tone_values_count = self.input_tone_values_count

        pii_values_count: Union[None, Unset, str]
        if isinstance(self.pii_values_count, Unset):
            pii_values_count = UNSET
        else:
            pii_values_count = self.pii_values_count

        prompt_injection_values_count: Union[None, Unset, str]
        if isinstance(self.prompt_injection_values_count, Unset):
            prompt_injection_values_count = UNSET
        else:
            prompt_injection_values_count = self.prompt_injection_values_count

        requests_count: Union[None, Unset, int]
        if isinstance(self.requests_count, Unset):
            requests_count = UNSET
        else:
            requests_count = self.requests_count

        tone_values_count: Union[None, Unset, str]
        if isinstance(self.tone_values_count, Unset):
            tone_values_count = UNSET
        else:
            tone_values_count = self.tone_values_count

        total_cost: Union[None, Unset, float]
        if isinstance(self.total_cost, Unset):
            total_cost = UNSET
        else:
            total_cost = self.total_cost

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({"end_bucket_time": end_bucket_time, "start_bucket_time": start_bucket_time})
        if average_agentic_workflow_success is not UNSET:
            field_dict["average_agentic_workflow_success"] = average_agentic_workflow_success
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
        if average_tool_error_rate is not UNSET:
            field_dict["average_tool_error_rate"] = average_tool_error_rate
        if average_tool_selection_quality is not UNSET:
            field_dict["average_tool_selection_quality"] = average_tool_selection_quality
        if average_total_token_length is not UNSET:
            field_dict["average_total_token_length"] = average_total_token_length
        if average_toxicity is not UNSET:
            field_dict["average_toxicity"] = average_toxicity
        if failures_count is not UNSET:
            field_dict["failures_count"] = failures_count
        if input_pii_values_count is not UNSET:
            field_dict["input_pii_values_count"] = input_pii_values_count
        if input_tone_values_count is not UNSET:
            field_dict["input_tone_values_count"] = input_tone_values_count
        if pii_values_count is not UNSET:
            field_dict["pii_values_count"] = pii_values_count
        if prompt_injection_values_count is not UNSET:
            field_dict["prompt_injection_values_count"] = prompt_injection_values_count
        if requests_count is not UNSET:
            field_dict["requests_count"] = requests_count
        if tone_values_count is not UNSET:
            field_dict["tone_values_count"] = tone_values_count
        if total_cost is not UNSET:
            field_dict["total_cost"] = total_cost

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        end_bucket_time = isoparse(d.pop("end_bucket_time"))

        start_bucket_time = isoparse(d.pop("start_bucket_time"))

        def _parse_average_agentic_workflow_success(data: object) -> Union[None, Unset, float]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, float], data)

        average_agentic_workflow_success = _parse_average_agentic_workflow_success(
            d.pop("average_agentic_workflow_success", UNSET)
        )

        def _parse_average_completeness_gpt(data: object) -> Union[None, Unset, float]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, float], data)

        average_completeness_gpt = _parse_average_completeness_gpt(d.pop("average_completeness_gpt", UNSET))

        def _parse_average_factuality(data: object) -> Union[None, Unset, float]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, float], data)

        average_factuality = _parse_average_factuality(d.pop("average_factuality", UNSET))

        def _parse_average_groundedness(data: object) -> Union[None, Unset, float]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, float], data)

        average_groundedness = _parse_average_groundedness(d.pop("average_groundedness", UNSET))

        def _parse_average_input_sexist(data: object) -> Union[None, Unset, float]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, float], data)

        average_input_sexist = _parse_average_input_sexist(d.pop("average_input_sexist", UNSET))

        def _parse_average_input_token_length(data: object) -> Union[None, Unset, float]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, float], data)

        average_input_token_length = _parse_average_input_token_length(d.pop("average_input_token_length", UNSET))

        def _parse_average_input_toxicity(data: object) -> Union[None, Unset, float]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, float], data)

        average_input_toxicity = _parse_average_input_toxicity(d.pop("average_input_toxicity", UNSET))

        def _parse_average_instruction_adherence(data: object) -> Union[None, Unset, float]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, float], data)

        average_instruction_adherence = _parse_average_instruction_adherence(
            d.pop("average_instruction_adherence", UNSET)
        )

        def _parse_average_latency(data: object) -> Union[None, Unset, float]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, float], data)

        average_latency = _parse_average_latency(d.pop("average_latency", UNSET))

        def _parse_average_output_token_length(data: object) -> Union[None, Unset, float]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, float], data)

        average_output_token_length = _parse_average_output_token_length(d.pop("average_output_token_length", UNSET))

        def _parse_average_prompt_perplexity(data: object) -> Union[None, Unset, float]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, float], data)

        average_prompt_perplexity = _parse_average_prompt_perplexity(d.pop("average_prompt_perplexity", UNSET))

        def _parse_average_retriever_attribution(data: object) -> Union[None, Unset, float]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, float], data)

        average_retriever_attribution = _parse_average_retriever_attribution(
            d.pop("average_retriever_attribution", UNSET)
        )

        def _parse_average_retriever_utilization(data: object) -> Union[None, Unset, float]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, float], data)

        average_retriever_utilization = _parse_average_retriever_utilization(
            d.pop("average_retriever_utilization", UNSET)
        )

        def _parse_average_sexist(data: object) -> Union[None, Unset, float]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, float], data)

        average_sexist = _parse_average_sexist(d.pop("average_sexist", UNSET))

        def _parse_average_tool_error_rate(data: object) -> Union[None, Unset, float]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, float], data)

        average_tool_error_rate = _parse_average_tool_error_rate(d.pop("average_tool_error_rate", UNSET))

        def _parse_average_tool_selection_quality(data: object) -> Union[None, Unset, float]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, float], data)

        average_tool_selection_quality = _parse_average_tool_selection_quality(
            d.pop("average_tool_selection_quality", UNSET)
        )

        def _parse_average_total_token_length(data: object) -> Union[None, Unset, float]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, float], data)

        average_total_token_length = _parse_average_total_token_length(d.pop("average_total_token_length", UNSET))

        def _parse_average_toxicity(data: object) -> Union[None, Unset, float]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, float], data)

        average_toxicity = _parse_average_toxicity(d.pop("average_toxicity", UNSET))

        def _parse_failures_count(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        failures_count = _parse_failures_count(d.pop("failures_count", UNSET))

        def _parse_input_pii_values_count(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        input_pii_values_count = _parse_input_pii_values_count(d.pop("input_pii_values_count", UNSET))

        def _parse_input_tone_values_count(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        input_tone_values_count = _parse_input_tone_values_count(d.pop("input_tone_values_count", UNSET))

        def _parse_pii_values_count(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        pii_values_count = _parse_pii_values_count(d.pop("pii_values_count", UNSET))

        def _parse_prompt_injection_values_count(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        prompt_injection_values_count = _parse_prompt_injection_values_count(
            d.pop("prompt_injection_values_count", UNSET)
        )

        def _parse_requests_count(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        requests_count = _parse_requests_count(d.pop("requests_count", UNSET))

        def _parse_tone_values_count(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        tone_values_count = _parse_tone_values_count(d.pop("tone_values_count", UNSET))

        def _parse_total_cost(data: object) -> Union[None, Unset, float]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, float], data)

        total_cost = _parse_total_cost(d.pop("total_cost", UNSET))

        bucketed_metrics = cls(
            end_bucket_time=end_bucket_time,
            start_bucket_time=start_bucket_time,
            average_agentic_workflow_success=average_agentic_workflow_success,
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
            average_tool_error_rate=average_tool_error_rate,
            average_tool_selection_quality=average_tool_selection_quality,
            average_total_token_length=average_total_token_length,
            average_toxicity=average_toxicity,
            failures_count=failures_count,
            input_pii_values_count=input_pii_values_count,
            input_tone_values_count=input_tone_values_count,
            pii_values_count=pii_values_count,
            prompt_injection_values_count=prompt_injection_values_count,
            requests_count=requests_count,
            tone_values_count=tone_values_count,
            total_cost=total_cost,
        )

        bucketed_metrics.additional_properties = d
        return bucketed_metrics

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
