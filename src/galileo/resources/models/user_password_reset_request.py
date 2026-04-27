from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="UserPasswordResetRequest")


@_attrs_define
class UserPasswordResetRequest:
    """
    Attributes:
        email (str):
        password (None | str | Unset):
        email_is_verified (bool | Unset):  Default: True.
    """

    email: str
    password: None | str | Unset = UNSET
    email_is_verified: bool | Unset = True
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        email = self.email

        password: None | str | Unset
        if isinstance(self.password, Unset):
            password = UNSET
        else:
            password = self.password

        email_is_verified = self.email_is_verified

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({"email": email})
        if password is not UNSET:
            field_dict["password"] = password
        if email_is_verified is not UNSET:
            field_dict["email_is_verified"] = email_is_verified

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        email = d.pop("email")

        def _parse_password(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        password = _parse_password(d.pop("password", UNSET))

        email_is_verified = d.pop("email_is_verified", UNSET)

        user_password_reset_request = cls(email=email, password=password, email_is_verified=email_is_verified)

        user_password_reset_request.additional_properties = d
        return user_password_reset_request

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
