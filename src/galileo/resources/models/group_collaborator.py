import datetime
from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.collaborator_role import CollaboratorRole
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.permission import Permission


T = TypeVar("T", bound="GroupCollaborator")


@_attrs_define
class GroupCollaborator:
    """
    Attributes:
        created_at (datetime.datetime):
        group_id (str):
        group_name (str):
        id (str):
        role (CollaboratorRole):
        permissions (Union[Unset, list['Permission']]):
    """

    created_at: datetime.datetime
    group_id: str
    group_name: str
    id: str
    role: CollaboratorRole
    permissions: Union[Unset, list["Permission"]] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        created_at = self.created_at.isoformat()

        group_id = self.group_id

        group_name = self.group_name

        id = self.id

        role = self.role.value

        permissions: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.permissions, Unset):
            permissions = []
            for permissions_item_data in self.permissions:
                permissions_item = permissions_item_data.to_dict()
                permissions.append(permissions_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {"created_at": created_at, "group_id": group_id, "group_name": group_name, "id": id, "role": role}
        )
        if permissions is not UNSET:
            field_dict["permissions"] = permissions

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.permission import Permission

        d = src_dict.copy()
        created_at = isoparse(d.pop("created_at"))

        group_id = d.pop("group_id")

        group_name = d.pop("group_name")

        id = d.pop("id")

        role = CollaboratorRole(d.pop("role"))

        permissions = []
        _permissions = d.pop("permissions", UNSET)
        for permissions_item_data in _permissions or []:
            permissions_item = Permission.from_dict(permissions_item_data)

            permissions.append(permissions_item)

        group_collaborator = cls(
            created_at=created_at, group_id=group_id, group_name=group_name, id=id, role=role, permissions=permissions
        )

        group_collaborator.additional_properties = d
        return group_collaborator

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
