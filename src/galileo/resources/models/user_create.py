from typing import Any, TypeVar, Union, cast

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
        auth_method (Union[Unset, AuthMethod]):
        email_is_verified (Union[None, Unset, bool]):  Default: False.
        first_name (Union[None, Unset, str]):  Default: ''.
        last_name (Union[None, Unset, str]):  Default: ''.
        password (Union[None, Unset, str]):
        role (Union[Unset, UserRole]):
    """

    email: str
    auth_method: Union[Unset, AuthMethod] = UNSET
    email_is_verified: Union[None, Unset, bool] = False
    first_name: Union[None, Unset, str] = ""
    last_name: Union[None, Unset, str] = ""
    password: Union[None, Unset, str] = UNSET
    role: Union[Unset, UserRole] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        email = self.email

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

        password: Union[None, Unset, str]
        if isinstance(self.password, Unset):
            password = UNSET
        else:
            password = self.password

        role: Union[Unset, str] = UNSET
        if not isinstance(self.role, Unset):
            role = self.role.value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({"email": email})
        if auth_method is not UNSET:
            field_dict["auth_method"] = auth_method
        if email_is_verified is not UNSET:
            field_dict["email_is_verified"] = email_is_verified
        if first_name is not UNSET:
            field_dict["first_name"] = first_name
        if last_name is not UNSET:
            field_dict["last_name"] = last_name
        if password is not UNSET:
            field_dict["password"] = password
        if role is not UNSET:
            field_dict["role"] = role

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        email = d.pop("email")

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

        def _parse_password(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        password = _parse_password(d.pop("password", UNSET))

        _role = d.pop("role", UNSET)
        role: Union[Unset, UserRole]
        if isinstance(_role, Unset):
            role = UNSET
        else:
            role = UserRole(_role)

        user_create = cls(
            email=email,
            auth_method=auth_method,
            email_is_verified=email_is_verified,
            first_name=first_name,
            last_name=last_name,
            password=password,
            role=role,
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
