import datetime
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.auth_method import AuthMethod
from ..models.user_role import UserRole
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.permission import Permission


T = TypeVar("T", bound="UserPasswordResetResponse")


@_attrs_define
class UserPasswordResetResponse:
    """
    Attributes:
        created_at (datetime.datetime):
        email (str):
        id (str):
        organization_id (str):
        organization_name (str):
        updated_at (datetime.datetime):
        auth_method (Union[Unset, AuthMethod]):
        email_is_verified (Union[None, Unset, bool]):
        first_name (Union[None, Unset, str]):  Default: ''.
        last_name (Union[None, Unset, str]):  Default: ''.
        permissions (Union[Unset, list['Permission']]):
        role (Union[Unset, UserRole]):
    """

    created_at: datetime.datetime
    email: str
    id: str
    organization_id: str
    organization_name: str
    updated_at: datetime.datetime
    auth_method: Union[Unset, AuthMethod] = UNSET
    email_is_verified: Union[None, Unset, bool] = UNSET
    first_name: Union[None, Unset, str] = ""
    last_name: Union[None, Unset, str] = ""
    permissions: Union[Unset, list["Permission"]] = UNSET
    role: Union[Unset, UserRole] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        created_at = self.created_at.isoformat()

        email = self.email

        id = self.id

        organization_id = self.organization_id

        organization_name = self.organization_name

        updated_at = self.updated_at.isoformat()

        auth_method: Union[Unset, str] = UNSET
        if not isinstance(self.auth_method, Unset):
            auth_method = self.auth_method.value

        email_is_verified: Union[None, Unset, bool]
        if isinstance(self.email_is_verified, Unset):
            email_is_verified = UNSET
        else:
            email_is_verified = self.email_is_verified

        first_name: Union[None, Unset, str]
        if isinstance(self.first_name, Unset):
            first_name = UNSET
        else:
            first_name = self.first_name

        last_name: Union[None, Unset, str]
        if isinstance(self.last_name, Unset):
            last_name = UNSET
        else:
            last_name = self.last_name

        permissions: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.permissions, Unset):
            permissions = []
            for permissions_item_data in self.permissions:
                permissions_item = permissions_item_data.to_dict()
                permissions.append(permissions_item)

        role: Union[Unset, str] = UNSET
        if not isinstance(self.role, Unset):
            role = self.role.value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "created_at": created_at,
                "email": email,
                "id": id,
                "organization_id": organization_id,
                "organization_name": organization_name,
                "updated_at": updated_at,
            }
        )
        if auth_method is not UNSET:
            field_dict["auth_method"] = auth_method
        if email_is_verified is not UNSET:
            field_dict["email_is_verified"] = email_is_verified
        if first_name is not UNSET:
            field_dict["first_name"] = first_name
        if last_name is not UNSET:
            field_dict["last_name"] = last_name
        if permissions is not UNSET:
            field_dict["permissions"] = permissions
        if role is not UNSET:
            field_dict["role"] = role

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.permission import Permission

        d = src_dict.copy()
        created_at = isoparse(d.pop("created_at"))

        email = d.pop("email")

        id = d.pop("id")

        organization_id = d.pop("organization_id")

        organization_name = d.pop("organization_name")

        updated_at = isoparse(d.pop("updated_at"))

        _auth_method = d.pop("auth_method", UNSET)
        auth_method: Union[Unset, AuthMethod]
        if isinstance(_auth_method, Unset):
            auth_method = UNSET
        else:
            auth_method = AuthMethod(_auth_method)

        def _parse_email_is_verified(data: object) -> Union[None, Unset, bool]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, bool], data)

        email_is_verified = _parse_email_is_verified(d.pop("email_is_verified", UNSET))

        def _parse_first_name(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        first_name = _parse_first_name(d.pop("first_name", UNSET))

        def _parse_last_name(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        last_name = _parse_last_name(d.pop("last_name", UNSET))

        permissions = []
        _permissions = d.pop("permissions", UNSET)
        for permissions_item_data in _permissions or []:
            permissions_item = Permission.from_dict(permissions_item_data)

            permissions.append(permissions_item)

        _role = d.pop("role", UNSET)
        role: Union[Unset, UserRole]
        if isinstance(_role, Unset):
            role = UNSET
        else:
            role = UserRole(_role)

        user_password_reset_response = cls(
            created_at=created_at,
            email=email,
            id=id,
            organization_id=organization_id,
            organization_name=organization_name,
            updated_at=updated_at,
            auth_method=auth_method,
            email_is_verified=email_is_verified,
            first_name=first_name,
            last_name=last_name,
            permissions=permissions,
            role=role,
        )

        user_password_reset_response.additional_properties = d
        return user_password_reset_response

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
