from collections.abc import Mapping
from typing import Any, Literal, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="ChoiceConstraints")


@_attrs_define
class ChoiceConstraints:
    """
    Attributes
    ----------
        annotation_type (Literal['choice']):
        choices (list[str]):
        allow_other (Union[Unset, bool]):  Default: False.
    """

    annotation_type: Literal["choice"]
    choices: list[str]
    allow_other: Unset | bool = False
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        annotation_type = self.annotation_type

        choices = self.choices

        allow_other = self.allow_other

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({"annotation_type": annotation_type, "choices": choices})
        if allow_other is not UNSET:
            field_dict["allow_other"] = allow_other

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        annotation_type = cast(Literal["choice"], d.pop("annotation_type"))
        if annotation_type != "choice":
            raise ValueError(f"annotation_type must match const 'choice', got '{annotation_type}'")

        choices = cast(list[str], d.pop("choices"))

        allow_other = d.pop("allow_other", UNSET)

        choice_constraints = cls(annotation_type=annotation_type, choices=choices, allow_other=allow_other)

        choice_constraints.additional_properties = d
        return choice_constraints

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
