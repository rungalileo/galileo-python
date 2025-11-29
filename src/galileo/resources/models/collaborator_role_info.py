from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.collaborator_role import CollaboratorRole

T = TypeVar("T", bound="CollaboratorRoleInfo")


@_attrs_define
class CollaboratorRoleInfo:
    """
    Attributes
    ----------
        name (CollaboratorRole):
        display_name (str):
        description (str):
    """

    name: CollaboratorRole
    display_name: str
    description: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name = self.name.value

        display_name = self.display_name

        description = self.description

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({"name": name, "display_name": display_name, "description": description})

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        name = CollaboratorRole(d.pop("name"))

        display_name = d.pop("display_name")

        description = d.pop("description")

        collaborator_role_info = cls(name=name, display_name=display_name, description=description)

        collaborator_role_info.additional_properties = d
        return collaborator_role_info

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
