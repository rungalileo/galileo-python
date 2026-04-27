from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="FineTunedScorerWeightsUploadRequest")


@_attrs_define
class FineTunedScorerWeightsUploadRequest:
    """
    Attributes:
        lora_task_id (int):
    """

    lora_task_id: int
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        lora_task_id = self.lora_task_id

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({"lora_task_id": lora_task_id})

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        lora_task_id = d.pop("lora_task_id")

        fine_tuned_scorer_weights_upload_request = cls(lora_task_id=lora_task_id)

        fine_tuned_scorer_weights_upload_request.additional_properties = d
        return fine_tuned_scorer_weights_upload_request

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
