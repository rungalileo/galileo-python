from typing import Any, Literal, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="TextConstraints")


@_attrs_define
class TextConstraints:
    """
    Attributes:
        feedback_type (Literal['text']):
    """

    feedback_type: Literal["text"]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        feedback_type = self.feedback_type

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({"feedback_type": feedback_type})

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        feedback_type = cast(Literal["text"], d.pop("feedback_type"))
        if feedback_type != "text":
            raise ValueError(f"feedback_type must match const 'text', got '{feedback_type}'")

        text_constraints = cls(feedback_type=feedback_type)

        text_constraints.additional_properties = d
        return text_constraints

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
