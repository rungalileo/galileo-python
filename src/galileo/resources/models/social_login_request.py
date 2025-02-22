from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.social_provider import SocialProvider

T = TypeVar("T", bound="SocialLoginRequest")


@_attrs_define
class SocialLoginRequest:
    """
    Attributes:
        id_token (str):
        provider (SocialProvider):
    """

    id_token: str
    provider: SocialProvider
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id_token = self.id_token

        provider = self.provider.value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({"id_token": id_token, "provider": provider})

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        id_token = d.pop("id_token")

        provider = SocialProvider(d.pop("provider"))

        social_login_request = cls(id_token=id_token, provider=provider)

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
