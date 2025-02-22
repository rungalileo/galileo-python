import datetime
from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="GetTokenResponse")


@_attrs_define
class GetTokenResponse:
    """
    Attributes:
        access_token (str):
        expires_at (datetime.datetime):
        token_type (Union[Unset, str]):  Default: 'bearer'.
    """

    access_token: str
    expires_at: datetime.datetime
    token_type: Union[Unset, str] = "bearer"
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        access_token = self.access_token

        expires_at = self.expires_at.isoformat()

        token_type = self.token_type

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({"access_token": access_token, "expires_at": expires_at})
        if token_type is not UNSET:
            field_dict["token_type"] = token_type

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        access_token = d.pop("access_token")

        expires_at = isoparse(d.pop("expires_at"))

        token_type = d.pop("token_type", UNSET)

        get_token_response = cls(access_token=access_token, expires_at=expires_at, token_type=token_type)

        get_token_response.additional_properties = d
        return get_token_response

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
