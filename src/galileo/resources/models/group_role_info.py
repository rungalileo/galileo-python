from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.group_role import GroupRole

T = TypeVar("T", bound="GroupRoleInfo")


@_attrs_define
class GroupRoleInfo:
    """
    Attributes:
        description (str):
        display_name (str):
        name (GroupRole):
    """

    description: str
    display_name: str
    name: GroupRole
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        description = self.description

        display_name = self.display_name

        name = self.name.value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({"description": description, "display_name": display_name, "name": name})

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        description = d.pop("description")

        display_name = d.pop("display_name")

        name = GroupRole(d.pop("name"))

        group_role_info = cls(description=description, display_name=display_name, name=name)

        group_role_info.additional_properties = d
        return group_role_info

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
