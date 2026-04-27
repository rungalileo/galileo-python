from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="CreateSignupLinkResponse")


@_attrs_define
class CreateSignupLinkResponse:
    """
    Attributes:
        message (str):
        signup_url (None | str | Unset):
    """

    message: str
    signup_url: None | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        message = self.message

        signup_url: None | str | Unset
        if isinstance(self.signup_url, Unset):
            signup_url = UNSET
        else:
            signup_url = self.signup_url

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({"message": message})
        if signup_url is not UNSET:
            field_dict["signup_url"] = signup_url

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        message = d.pop("message")

        def _parse_signup_url(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        signup_url = _parse_signup_url(d.pop("signup_url", UNSET))

        create_signup_link_response = cls(message=message, signup_url=signup_url)

        create_signup_link_response.additional_properties = d
        return create_signup_link_response

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
