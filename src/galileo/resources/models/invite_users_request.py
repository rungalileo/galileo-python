from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.auth_method import AuthMethod
from ..models.user_role import UserRole
from ..types import UNSET, Unset

T = TypeVar("T", bound="InviteUsersRequest")


@_attrs_define
class InviteUsersRequest:
    """
    Attributes:
        emails (list[str]):
        auth_method (AuthMethod | Unset):
        role (UserRole | Unset):
        group_ids (list[str] | Unset):
        send_email (bool | Unset):  Default: True.
    """

    emails: list[str]
    auth_method: AuthMethod | Unset = UNSET
    role: UserRole | Unset = UNSET
    group_ids: list[str] | Unset = UNSET
    send_email: bool | Unset = True
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        emails = self.emails

        auth_method: str | Unset = UNSET
        if not isinstance(self.auth_method, Unset):
            auth_method = self.auth_method.value

        role: str | Unset = UNSET
        if not isinstance(self.role, Unset):
            role = self.role.value

        group_ids: list[str] | Unset = UNSET
        if not isinstance(self.group_ids, Unset):
            group_ids = self.group_ids

        send_email = self.send_email

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({"emails": emails})
        if auth_method is not UNSET:
            field_dict["auth_method"] = auth_method
        if role is not UNSET:
            field_dict["role"] = role
        if group_ids is not UNSET:
            field_dict["group_ids"] = group_ids
        if send_email is not UNSET:
            field_dict["send_email"] = send_email

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        emails = cast(list[str], d.pop("emails"))

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

        group_ids = cast(list[str], d.pop("group_ids", UNSET))

        send_email = d.pop("send_email", UNSET)

        invite_users_request = cls(
            emails=emails, auth_method=auth_method, role=role, group_ids=group_ids, send_email=send_email
        )

        invite_users_request.additional_properties = d
        return invite_users_request

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
