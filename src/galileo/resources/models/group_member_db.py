from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.group_role import GroupRole
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.permission import Permission


T = TypeVar("T", bound="GroupMemberDB")


@_attrs_define
class GroupMemberDB:
    """
    Attributes:
        id (str):
        user_id (str):
        group_role (GroupRole):
        first_name (None | str):
        last_name (None | str):
        email (str):
        created_at (datetime.datetime):
        permissions (list[Permission] | Unset):
    """

    id: str
    user_id: str
    group_role: GroupRole
    first_name: None | str
    last_name: None | str
    email: str
    created_at: datetime.datetime
    permissions: list[Permission] | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        user_id = self.user_id

        group_role = self.group_role.value

        first_name: None | str
        first_name = self.first_name

        last_name: None | str
        last_name = self.last_name

        email = self.email

        created_at = self.created_at.isoformat()

        permissions: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.permissions, Unset):
            permissions = []
            for permissions_item_data in self.permissions:
                permissions_item = permissions_item_data.to_dict()
                permissions.append(permissions_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "user_id": user_id,
                "group_role": group_role,
                "first_name": first_name,
                "last_name": last_name,
                "email": email,
                "created_at": created_at,
            }
        )
        if permissions is not UNSET:
            field_dict["permissions"] = permissions

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.permission import Permission

        d = dict(src_dict)
        id = d.pop("id")

        user_id = d.pop("user_id")

        group_role = GroupRole(d.pop("group_role"))

        def _parse_first_name(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        first_name = _parse_first_name(d.pop("first_name"))

        def _parse_last_name(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        last_name = _parse_last_name(d.pop("last_name"))

        email = d.pop("email")

        created_at = isoparse(d.pop("created_at"))

        _permissions = d.pop("permissions", UNSET)
        permissions: list[Permission] | Unset = UNSET
        if _permissions is not UNSET:
            permissions = []
            for permissions_item_data in _permissions:
                permissions_item = Permission.from_dict(permissions_item_data)

                permissions.append(permissions_item)

        group_member_db = cls(
            id=id,
            user_id=user_id,
            group_role=group_role,
            first_name=first_name,
            last_name=last_name,
            email=email,
            created_at=created_at,
            permissions=permissions,
        )

        group_member_db.additional_properties = d
        return group_member_db

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
