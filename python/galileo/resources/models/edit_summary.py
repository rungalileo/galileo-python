from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.edit_action import EditAction

T = TypeVar("T", bound="EditSummary")


@_attrs_define
class EditSummary:
    """
    Attributes:
        count (int):
        edit_action (EditAction): The available actions you can take in an edit.
    """

    count: int
    edit_action: EditAction
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        count = self.count

        edit_action = self.edit_action.value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({"count": count, "edit_action": edit_action})

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        count = d.pop("count")

        edit_action = EditAction(d.pop("edit_action"))

        edit_summary = cls(count=count, edit_action=edit_action)

        edit_summary.additional_properties = d
        return edit_summary

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
