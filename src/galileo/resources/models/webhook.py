from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.webhook_status import WebhookStatus
from ..types import UNSET, Unset

T = TypeVar("T", bound="Webhook")


@_attrs_define
class Webhook:
    """
    Attributes:
        url (str):
        status (WebhookStatus | Unset):
        notes (str | Unset):  Default: ''.
    """

    url: str
    status: WebhookStatus | Unset = UNSET
    notes: str | Unset = ""
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        url = self.url

        status: str | Unset = UNSET
        if not isinstance(self.status, Unset):
            status = self.status.value

        notes = self.notes

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({"url": url})
        if status is not UNSET:
            field_dict["status"] = status
        if notes is not UNSET:
            field_dict["notes"] = notes

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        url = d.pop("url")

        _status = d.pop("status", UNSET)
        status: WebhookStatus | Unset
        if isinstance(_status, Unset):
            status = UNSET
        else:
            status = WebhookStatus(_status)

        notes = d.pop("notes", UNSET)

        webhook = cls(url=url, status=status, notes=notes)

        webhook.additional_properties = d
        return webhook

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
