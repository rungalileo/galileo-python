from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.auth_method import AuthMethod
from ..models.user_role import UserRole
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.permission import Permission


T = TypeVar("T", bound="UserDB")


@_attrs_define
class UserDB:
    """
    Attributes
    ----------
        id (str):
        email (str):
        organization_id (str):
        organization_name (str):
        created_at (datetime.datetime):
        updated_at (datetime.datetime):
        permissions (list[Permission] | Unset):
        first_name (None | str | Unset):  Default: ''.
        last_name (None | str | Unset):  Default: ''.
        auth_method (AuthMethod | Unset):
        role (UserRole | Unset):
        email_is_verified (bool | None | Unset):
    """

    id: str
    email: str
    organization_id: str
    organization_name: str
    created_at: datetime.datetime
    updated_at: datetime.datetime
    permissions: list[Permission] | Unset = UNSET
    first_name: None | str | Unset = ""
    last_name: None | str | Unset = ""
    auth_method: AuthMethod | Unset = UNSET
    role: UserRole | Unset = UNSET
    email_is_verified: bool | None | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        email = self.email

        organization_id = self.organization_id

        organization_name = self.organization_name

        created_at = self.created_at.isoformat()

        updated_at = self.updated_at.isoformat()

        permissions: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.permissions, Unset):
            permissions = []
            for permissions_item_data in self.permissions:
                permissions_item = permissions_item_data.to_dict()
                permissions.append(permissions_item)

        first_name: None | str | Unset
        first_name = UNSET if isinstance(self.first_name, Unset) else self.first_name

        last_name: None | str | Unset
        last_name = UNSET if isinstance(self.last_name, Unset) else self.last_name

        auth_method: str | Unset = UNSET
        if not isinstance(self.auth_method, Unset):
            auth_method = self.auth_method.value

        role: str | Unset = UNSET
        if not isinstance(self.role, Unset):
            role = self.role.value

        email_is_verified: bool | None | Unset
        email_is_verified = UNSET if isinstance(self.email_is_verified, Unset) else self.email_is_verified

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "email": email,
                "organization_id": organization_id,
                "organization_name": organization_name,
                "created_at": created_at,
                "updated_at": updated_at,
            }
        )
        if permissions is not UNSET:
            field_dict["permissions"] = permissions
        if first_name is not UNSET:
            field_dict["first_name"] = first_name
        if last_name is not UNSET:
            field_dict["last_name"] = last_name
        if auth_method is not UNSET:
            field_dict["auth_method"] = auth_method
        if role is not UNSET:
            field_dict["role"] = role
        if email_is_verified is not UNSET:
            field_dict["email_is_verified"] = email_is_verified

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.permission import Permission

        d = dict(src_dict)
        id = d.pop("id")

        email = d.pop("email")

        organization_id = d.pop("organization_id")

        organization_name = d.pop("organization_name")

        created_at = isoparse(d.pop("created_at"))

        updated_at = isoparse(d.pop("updated_at"))

        _permissions = d.pop("permissions", UNSET)
        permissions: list[Permission] | Unset = UNSET
        if _permissions is not UNSET:
            permissions = []
            for permissions_item_data in _permissions:
                permissions_item = Permission.from_dict(permissions_item_data)

                permissions.append(permissions_item)

        def _parse_first_name(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        first_name = _parse_first_name(d.pop("first_name", UNSET))

        def _parse_last_name(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        last_name = _parse_last_name(d.pop("last_name", UNSET))

        _auth_method = d.pop("auth_method", UNSET)
        auth_method: AuthMethod | Unset
        auth_method = UNSET if isinstance(_auth_method, Unset) else AuthMethod(_auth_method)

        _role = d.pop("role", UNSET)
        role: UserRole | Unset
        role = UNSET if isinstance(_role, Unset) else UserRole(_role)

        def _parse_email_is_verified(data: object) -> bool | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(bool | None | Unset, data)

        email_is_verified = _parse_email_is_verified(d.pop("email_is_verified", UNSET))

        user_db = cls(
            id=id,
            email=email,
            organization_id=organization_id,
            organization_name=organization_name,
            created_at=created_at,
            updated_at=updated_at,
            permissions=permissions,
            first_name=first_name,
            last_name=last_name,
            auth_method=auth_method,
            role=role,
            email_is_verified=email_is_verified,
        )

        user_db.additional_properties = d
        return user_db

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
