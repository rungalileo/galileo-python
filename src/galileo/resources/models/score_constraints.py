from __future__ import annotations

from collections.abc import Mapping
from typing import Any, Literal, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="ScoreConstraints")


@_attrs_define
class ScoreConstraints:
    """
    Attributes:
        annotation_type (Literal['score']):
        min_ (int):
        max_ (int):
    """

    annotation_type: Literal["score"]
    min_: int
    max_: int
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        annotation_type = self.annotation_type

        min_ = self.min_

        max_ = self.max_

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({"annotation_type": annotation_type, "min": min_, "max": max_})

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        annotation_type = cast(Literal["score"], d.pop("annotation_type"))
        if annotation_type != "score":
            raise ValueError(f"annotation_type must match const 'score', got '{annotation_type}'")

        min_ = d.pop("min")

        max_ = d.pop("max")

        score_constraints = cls(annotation_type=annotation_type, min_=min_, max_=max_)

        score_constraints.additional_properties = d
        return score_constraints

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
