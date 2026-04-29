from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.collaborator_role import CollaboratorRole
from ..types import UNSET, Unset

T = TypeVar("T", bound="UserCollaboratorCreate")


@_attrs_define
class UserCollaboratorCreate:
    """Create a user collaborator using either user_id or email.

    When using email, if the user doesn't exist in the organization,
    they will be invited automatically.

    Attributes
    ----------
            role (Union[Unset, CollaboratorRole]):
            user_id (Union[None, Unset, str]):
            user_email (Union[None, Unset, str]):
    """

    role: Union[Unset, CollaboratorRole] = UNSET
    user_id: Union[None, Unset, str] = UNSET
    user_email: Union[None, Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        role: Union[Unset, str] = UNSET
        if not isinstance(self.role, Unset):
            role = self.role.value

        user_id: Union[None, Unset, str]
        user_id = UNSET if isinstance(self.user_id, Unset) else self.user_id

        user_email: Union[None, Unset, str]
        user_email = UNSET if isinstance(self.user_email, Unset) else self.user_email

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if role is not UNSET:
            field_dict["role"] = role
        if user_id is not UNSET:
            field_dict["user_id"] = user_id
        if user_email is not UNSET:
            field_dict["user_email"] = user_email

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        _role = d.pop("role", UNSET)
        role: Union[Unset, CollaboratorRole]
        role = UNSET if isinstance(_role, Unset) else CollaboratorRole(_role)

        def _parse_user_id(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        user_id = _parse_user_id(d.pop("user_id", UNSET))

        def _parse_user_email(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        user_email = _parse_user_email(d.pop("user_email", UNSET))

        user_collaborator_create = cls(role=role, user_id=user_id, user_email=user_email)

        user_collaborator_create.additional_properties = d
        return user_collaborator_create

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
