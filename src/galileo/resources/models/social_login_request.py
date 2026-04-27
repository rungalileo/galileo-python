from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.social_provider import SocialProvider
from ..types import UNSET, Unset

T = TypeVar("T", bound="SocialLoginRequest")


@_attrs_define
class SocialLoginRequest:
    """
    Attributes:
        provider (SocialProvider):
        id_token (None | str | Unset):
        access_token (None | str | Unset):
    """

    provider: SocialProvider
    id_token: None | str | Unset = UNSET
    access_token: None | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        provider = self.provider.value

        id_token: None | str | Unset
        if isinstance(self.id_token, Unset):
            id_token = UNSET
        else:
            id_token = self.id_token

        access_token: None | str | Unset
        if isinstance(self.access_token, Unset):
            access_token = UNSET
        else:
            access_token = self.access_token

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({"provider": provider})
        if id_token is not UNSET:
            field_dict["id_token"] = id_token
        if access_token is not UNSET:
            field_dict["access_token"] = access_token

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        provider = SocialProvider(d.pop("provider"))

        def _parse_id_token(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        id_token = _parse_id_token(d.pop("id_token", UNSET))

        def _parse_access_token(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        access_token = _parse_access_token(d.pop("access_token", UNSET))

        social_login_request = cls(provider=provider, id_token=id_token, access_token=access_token)

        social_login_request.additional_properties = d
        return social_login_request

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
