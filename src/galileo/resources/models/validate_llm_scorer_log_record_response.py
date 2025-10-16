from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="ValidateLLMScorerLogRecordResponse")


@_attrs_define
class ValidateLLMScorerLogRecordResponse:
    """Response model for validating a new LLM scorer based on a log record.

    Returns the uuid of the experiment created with the copied log records to store the metric testing results.

    Attributes
    ----------
            metrics_experiment_id (str):
    """

    metrics_experiment_id: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        metrics_experiment_id = self.metrics_experiment_id

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({"metrics_experiment_id": metrics_experiment_id})

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        metrics_experiment_id = d.pop("metrics_experiment_id")

        validate_llm_scorer_log_record_response = cls(metrics_experiment_id=metrics_experiment_id)

        validate_llm_scorer_log_record_response.additional_properties = d
        return validate_llm_scorer_log_record_response

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
