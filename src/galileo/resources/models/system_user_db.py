from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.system_role import SystemRole
from ..models.system_user_status import SystemUserStatus
from ..types import UNSET, Unset

T = TypeVar("T", bound="SystemUserDB")


@_attrs_define
class SystemUserDB:
    """
    Attributes:
        id (str):
        created_at (datetime.datetime):
        updated_at (datetime.datetime):
        email (str):
        status (SystemUserStatus):
        role (SystemRole):
        auth_method (str):
        first_name (None | str | Unset):
        last_name (None | str | Unset):
        email_is_verified (bool | None | Unset):
    """

    id: str
    created_at: datetime.datetime
    updated_at: datetime.datetime
    email: str
    status: SystemUserStatus
    role: SystemRole
    auth_method: str
    first_name: None | str | Unset = UNSET
    last_name: None | str | Unset = UNSET
    email_is_verified: bool | None | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        created_at = self.created_at.isoformat()

        updated_at = self.updated_at.isoformat()

        email = self.email

        status = self.status.value

        role = self.role.value

        auth_method = self.auth_method

        first_name: None | str | Unset
        if isinstance(self.first_name, Unset):
            first_name = UNSET
        else:
            first_name = self.first_name

        last_name: None | str | Unset
        if isinstance(self.last_name, Unset):
            last_name = UNSET
        else:
            last_name = self.last_name

        email_is_verified: bool | None | Unset
        if isinstance(self.email_is_verified, Unset):
            email_is_verified = UNSET
        else:
            email_is_verified = self.email_is_verified

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "created_at": created_at,
                "updated_at": updated_at,
                "email": email,
                "status": status,
                "role": role,
                "auth_method": auth_method,
            }
        )
        if first_name is not UNSET:
            field_dict["first_name"] = first_name
        if last_name is not UNSET:
            field_dict["last_name"] = last_name
        if email_is_verified is not UNSET:
            field_dict["email_is_verified"] = email_is_verified

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = d.pop("id")

        created_at = isoparse(d.pop("created_at"))

        updated_at = isoparse(d.pop("updated_at"))

        email = d.pop("email")

        status = SystemUserStatus(d.pop("status"))

        role = SystemRole(d.pop("role"))

        auth_method = d.pop("auth_method")

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

        def _parse_email_is_verified(data: object) -> bool | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(bool | None | Unset, data)

        email_is_verified = _parse_email_is_verified(d.pop("email_is_verified", UNSET))

        system_user_db = cls(
            id=id,
            created_at=created_at,
            updated_at=updated_at,
            email=email,
            status=status,
            role=role,
            auth_method=auth_method,
            first_name=first_name,
            last_name=last_name,
            email_is_verified=email_is_verified,
        )

        system_user_db.additional_properties = d
        return system_user_db

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
