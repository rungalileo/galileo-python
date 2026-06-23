from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.feedback_type import FeedbackType

T = TypeVar("T", bound="FeedbackRatingInfo")


@_attrs_define
class FeedbackRatingInfo:
    """
    Attributes:
        feedback_type (FeedbackType):
        value (bool | int | list[str] | str):
        explanation (None | str):
    """

    feedback_type: FeedbackType
    value: bool | int | list[str] | str
    explanation: None | str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        feedback_type = self.feedback_type.value

        value: bool | int | list[str] | str
        if isinstance(self.value, list):
            value = self.value

        else:
            value = self.value

        explanation: None | str
        explanation = self.explanation

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({"feedback_type": feedback_type, "value": value, "explanation": explanation})

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        feedback_type = FeedbackType(d.pop("feedback_type"))

        def _parse_value(data: object) -> bool | int | list[str] | str:
            try:
                if not isinstance(data, list):
                    raise TypeError()
                value_type_3 = cast(list[str], data)

                return value_type_3
            except:  # noqa: E722
                pass
            return cast(bool | int | list[str] | str, data)

        value = _parse_value(d.pop("value"))

        def _parse_explanation(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        explanation = _parse_explanation(d.pop("explanation"))

        feedback_rating_info = cls(feedback_type=feedback_type, value=value, explanation=explanation)

        feedback_rating_info.additional_properties = d
        return feedback_rating_info

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
