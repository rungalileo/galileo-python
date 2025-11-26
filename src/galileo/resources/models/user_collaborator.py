import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.collaborator_role import CollaboratorRole
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.permission import Permission


T = TypeVar("T", bound="UserCollaborator")


@_attrs_define
class UserCollaborator:
    """
    Attributes
    ----------
        id (str):
        role (CollaboratorRole):
        created_at (datetime.datetime):
        user_id (str):
        first_name (Union[None, str]):
        last_name (Union[None, str]):
        email (str):
        permissions (Union[Unset, list['Permission']]):
    """

    id: str
    role: CollaboratorRole
    created_at: datetime.datetime
    user_id: str
    first_name: Union[None, str]
    last_name: Union[None, str]
    email: str
    permissions: Union[Unset, list["Permission"]] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        role = self.role.value

        created_at = self.created_at.isoformat()

        user_id = self.user_id

        first_name: Union[None, str]
        first_name = self.first_name

        last_name: Union[None, str]
        last_name = self.last_name

        email = self.email

        permissions: Union[Unset, list[dict[str, Any]]] = UNSET
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
                "role": role,
                "created_at": created_at,
                "user_id": user_id,
                "first_name": first_name,
                "last_name": last_name,
                "email": email,
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

        role = CollaboratorRole(d.pop("role"))

        created_at = isoparse(d.pop("created_at"))

        user_id = d.pop("user_id")

        def _parse_first_name(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        first_name = _parse_first_name(d.pop("first_name"))

        def _parse_last_name(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        last_name = _parse_last_name(d.pop("last_name"))

        email = d.pop("email")

        permissions = []
        _permissions = d.pop("permissions", UNSET)
        for permissions_item_data in _permissions or []:
            permissions_item = Permission.from_dict(permissions_item_data)

            permissions.append(permissions_item)

        user_collaborator = cls(
            id=id,
            role=role,
            created_at=created_at,
            user_id=user_id,
            first_name=first_name,
            last_name=last_name,
            email=email,
            permissions=permissions,
        )

        user_collaborator.additional_properties = d
        return user_collaborator

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
