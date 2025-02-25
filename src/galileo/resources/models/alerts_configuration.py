from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.webhook import Webhook


T = TypeVar("T", bound="AlertsConfiguration")


@_attrs_define
class AlertsConfiguration:
    """
    Attributes:
        emails (Union[Unset, list[str]]):
        webhooks (Union[Unset, list['Webhook']]):
    """

    emails: Union[Unset, list[str]] = UNSET
    webhooks: Union[Unset, list["Webhook"]] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        emails: Union[Unset, list[str]] = UNSET
        if not isinstance(self.emails, Unset):
            emails = self.emails

        webhooks: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.webhooks, Unset):
            webhooks = []
            for webhooks_item_data in self.webhooks:
                webhooks_item = webhooks_item_data.to_dict()
                webhooks.append(webhooks_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if emails is not UNSET:
            field_dict["emails"] = emails
        if webhooks is not UNSET:
            field_dict["webhooks"] = webhooks

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.webhook import Webhook

        d = src_dict.copy()
        emails = cast(list[str], d.pop("emails", UNSET))

        webhooks = []
        _webhooks = d.pop("webhooks", UNSET)
        for webhooks_item_data in _webhooks or []:
            webhooks_item = Webhook.from_dict(webhooks_item_data)

            webhooks.append(webhooks_item)

        alerts_configuration = cls(emails=emails, webhooks=webhooks)

        alerts_configuration.additional_properties = d
        return alerts_configuration

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
