from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.group_role import GroupRole
from ..models.group_visibility import GroupVisibility
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.permission import Permission


T = TypeVar("T", bound="GroupDB")


@_attrs_define
class GroupDB:
    """
    Attributes:
        id (str):
        name (str):
        size (int):
        created_at (datetime.datetime):
        permissions (list[Permission] | Unset):
        description (None | str | Unset):
        visibility (GroupVisibility | Unset):
        role (GroupRole | None | Unset): The role of the current user in the group.
    """

    id: str
    name: str
    size: int
    created_at: datetime.datetime
    permissions: list[Permission] | Unset = UNSET
    description: None | str | Unset = UNSET
    visibility: GroupVisibility | Unset = UNSET
    role: GroupRole | None | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        name = self.name

        size = self.size

        created_at = self.created_at.isoformat()

        permissions: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.permissions, Unset):
            permissions = []
            for permissions_item_data in self.permissions:
                permissions_item = permissions_item_data.to_dict()
                permissions.append(permissions_item)

        description: None | str | Unset
        if isinstance(self.description, Unset):
            description = UNSET
        else:
            description = self.description

        visibility: str | Unset = UNSET
        if not isinstance(self.visibility, Unset):
            visibility = self.visibility.value

        role: None | str | Unset
        if isinstance(self.role, Unset):
            role = UNSET
        elif isinstance(self.role, GroupRole):
            role = self.role.value
        else:
            role = self.role

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({"id": id, "name": name, "size": size, "created_at": created_at})
        if permissions is not UNSET:
            field_dict["permissions"] = permissions
        if description is not UNSET:
            field_dict["description"] = description
        if visibility is not UNSET:
            field_dict["visibility"] = visibility
        if role is not UNSET:
            field_dict["role"] = role

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.permission import Permission

        d = dict(src_dict)
        id = d.pop("id")

        name = d.pop("name")

        size = d.pop("size")

        created_at = isoparse(d.pop("created_at"))

        _permissions = d.pop("permissions", UNSET)
        permissions: list[Permission] | Unset = UNSET
        if _permissions is not UNSET:
            permissions = []
            for permissions_item_data in _permissions:
                permissions_item = Permission.from_dict(permissions_item_data)

                permissions.append(permissions_item)

        def _parse_description(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        description = _parse_description(d.pop("description", UNSET))

        _visibility = d.pop("visibility", UNSET)
        visibility: GroupVisibility | Unset
        if isinstance(_visibility, Unset):
            visibility = UNSET
        else:
            visibility = GroupVisibility(_visibility)

        def _parse_role(data: object) -> GroupRole | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                role_type_0 = GroupRole(data)

                return role_type_0
            except:  # noqa: E722
                pass
            return cast(GroupRole | None | Unset, data)

        role = _parse_role(d.pop("role", UNSET))

        group_db = cls(
            id=id,
            name=name,
            size=size,
            created_at=created_at,
            permissions=permissions,
            description=description,
            visibility=visibility,
            role=role,
        )

        group_db.additional_properties = d
        return group_db

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
