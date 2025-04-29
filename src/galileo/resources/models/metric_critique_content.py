from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="MetricCritiqueContent")


@_attrs_define
class MetricCritiqueContent:
    """
    Attributes:
        critique (str):
        intended_value (bool):
        original_explanation (str):
    """

    critique: str
    intended_value: bool
    original_explanation: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        critique = self.critique

        intended_value = self.intended_value

        original_explanation = self.original_explanation

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {"critique": critique, "intended_value": intended_value, "original_explanation": original_explanation}
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        critique = d.pop("critique")

        intended_value = d.pop("intended_value")

        original_explanation = d.pop("original_explanation")

        metric_critique_content = cls(
            critique=critique, intended_value=intended_value, original_explanation=original_explanation
        )

        metric_critique_content.additional_properties = d
        return metric_critique_content

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
