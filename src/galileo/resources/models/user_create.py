from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.auth_method import AuthMethod
from ..models.user_role import UserRole
from ..types import UNSET, Unset

T = TypeVar("T", bound="UserCreate")


@_attrs_define
class UserCreate:
    """
    Attributes:
        email (str):
        first_name (None | str | Unset):  Default: ''.
        last_name (None | str | Unset):  Default: ''.
        auth_method (AuthMethod | Unset):
        role (UserRole | Unset):
        email_is_verified (bool | None | Unset):  Default: False.
        password (None | str | Unset):
    """

    email: str
    first_name: None | str | Unset = ""
    last_name: None | str | Unset = ""
    auth_method: AuthMethod | Unset = UNSET
    role: UserRole | Unset = UNSET
    email_is_verified: bool | None | Unset = False
    password: None | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        email = self.email

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

        auth_method: str | Unset = UNSET
        if not isinstance(self.auth_method, Unset):
            auth_method = self.auth_method.value

        role: str | Unset = UNSET
        if not isinstance(self.role, Unset):
            role = self.role.value

        email_is_verified: bool | None | Unset
        if isinstance(self.email_is_verified, Unset):
            email_is_verified = UNSET
        else:
            email_is_verified = self.email_is_verified

        password: None | str | Unset
        if isinstance(self.password, Unset):
            password = UNSET
        else:
            password = self.password

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({"email": email})
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
        if password is not UNSET:
            field_dict["password"] = password

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        email = d.pop("email")

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
        if isinstance(_auth_method, Unset):
            auth_method = UNSET
        else:
            auth_method = AuthMethod(_auth_method)

        _role = d.pop("role", UNSET)
        role: UserRole | Unset
        if isinstance(_role, Unset):
            role = UNSET
        else:
            role = UserRole(_role)

        def _parse_email_is_verified(data: object) -> bool | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(bool | None | Unset, data)

        email_is_verified = _parse_email_is_verified(d.pop("email_is_verified", UNSET))

        def _parse_password(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        password = _parse_password(d.pop("password", UNSET))

        user_create = cls(
            email=email,
            first_name=first_name,
            last_name=last_name,
            auth_method=auth_method,
            role=role,
            email_is_verified=email_is_verified,
            password=password,
        )

        user_create.additional_properties = d
        return user_create

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
