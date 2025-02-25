from typing import Any, Literal, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="ScoreConstraints")


@_attrs_define
class ScoreConstraints:
    """
    Attributes:
        feedback_type (Literal['score']):
        max_ (int):
        min_ (int):
    """

    feedback_type: Literal["score"]
    max_: int
    min_: int
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        feedback_type = self.feedback_type

        max_ = self.max_

        min_ = self.min_

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({"feedback_type": feedback_type, "max": max_, "min": min_})

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        feedback_type = cast(Literal["score"], d.pop("feedback_type"))
        if feedback_type != "score":
            raise ValueError(f"feedback_type must match const 'score', got '{feedback_type}'")

        max_ = d.pop("max")

        min_ = d.pop("min")

        score_constraints = cls(feedback_type=feedback_type, max_=max_, min_=min_)

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
