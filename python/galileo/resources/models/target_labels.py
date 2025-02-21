from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="TargetLabels")


@_attrs_define
class TargetLabels:
    """Structure for each target label in a co-occurence response.

    Attributes:
        co_occurrence (float):
        label (str):
    """

    co_occurrence: float
    label: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        co_occurrence = self.co_occurrence

        label = self.label

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({"co_occurrence": co_occurrence, "label": label})

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        co_occurrence = d.pop("co_occurrence")

        label = d.pop("label")

        target_labels = cls(co_occurrence=co_occurrence, label=label)

        target_labels.additional_properties = d
        return target_labels

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
