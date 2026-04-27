from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.annotation_type import AnnotationType

T = TypeVar("T", bound="AnnotationRatingInfo")


@_attrs_define
class AnnotationRatingInfo:
    """
    Attributes:
        annotation_type (AnnotationType):
        value (bool | int | list[str] | str):
        explanation (None | str):
    """

    annotation_type: AnnotationType
    value: bool | int | list[str] | str
    explanation: None | str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        annotation_type = self.annotation_type.value

        value: bool | int | list[str] | str
        if isinstance(self.value, list):
            value = self.value

        else:
            value = self.value

        explanation: None | str
        explanation = self.explanation

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({"annotation_type": annotation_type, "value": value, "explanation": explanation})

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        annotation_type = AnnotationType(d.pop("annotation_type"))

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

        annotation_rating_info = cls(annotation_type=annotation_type, value=value, explanation=explanation)

        annotation_rating_info.additional_properties = d
        return annotation_rating_info

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
