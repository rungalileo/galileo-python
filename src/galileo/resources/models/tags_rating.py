from typing import Any, Literal, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="TagsRating")


@_attrs_define
class TagsRating:
    """
    Attributes:
        value (list[str]):
        feedback_type (Union[Literal['tags'], Unset]):  Default: 'tags'.
    """

    value: list[str]
    feedback_type: Union[Literal["tags"], Unset] = "tags"
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        value = self.value

        feedback_type = self.feedback_type

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({"value": value})
        if feedback_type is not UNSET:
            field_dict["feedback_type"] = feedback_type

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        value = cast(list[str], d.pop("value"))

        feedback_type = cast(Union[Literal["tags"], Unset], d.pop("feedback_type", UNSET))
        if feedback_type != "tags" and not isinstance(feedback_type, Unset):
            raise ValueError(f"feedback_type must match const 'tags', got '{feedback_type}'")

        tags_rating = cls(value=value, feedback_type=feedback_type)

        tags_rating.additional_properties = d
        return tags_rating

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
