from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.user_role import UserRole
from ..types import UNSET, Unset

T = TypeVar("T", bound="InviteUsersRequest")


@_attrs_define
class InviteUsersRequest:
    """
    Attributes:
        emails (list[str]):
        group_ids (Union[Unset, list[str]]):
        role (Union[Unset, UserRole]):
        send_email (Union[Unset, bool]):  Default: True.
    """

    emails: list[str]
    group_ids: Union[Unset, list[str]] = UNSET
    role: Union[Unset, UserRole] = UNSET
    send_email: Union[Unset, bool] = True
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        emails = self.emails

        group_ids: Union[Unset, list[str]] = UNSET
        if not isinstance(self.group_ids, Unset):
            group_ids = self.group_ids

        role: Union[Unset, str] = UNSET
        if not isinstance(self.role, Unset):
            role = self.role.value

        send_email = self.send_email

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({"emails": emails})
        if group_ids is not UNSET:
            field_dict["group_ids"] = group_ids
        if role is not UNSET:
            field_dict["role"] = role
        if send_email is not UNSET:
            field_dict["send_email"] = send_email

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        emails = cast(list[str], d.pop("emails"))

        group_ids = cast(list[str], d.pop("group_ids", UNSET))

        _role = d.pop("role", UNSET)
        role: Union[Unset, UserRole]
        if isinstance(_role, Unset):
            role = UNSET
        else:
            role = UserRole(_role)

        send_email = d.pop("send_email", UNSET)

        invite_users_request = cls(emails=emails, group_ids=group_ids, role=role, send_email=send_email)

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
