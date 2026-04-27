from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.webhook import Webhook


T = TypeVar("T", bound="RunAlertSettingsDB")


@_attrs_define
class RunAlertSettingsDB:
    """
    Attributes:
        run_id (str):
        id (str):
        created_at (datetime.datetime):
        updated_at (datetime.datetime):
        emails (list[str] | Unset):
        webhooks (list[Webhook] | Unset):
    """

    run_id: str
    id: str
    created_at: datetime.datetime
    updated_at: datetime.datetime
    emails: list[str] | Unset = UNSET
    webhooks: list[Webhook] | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        run_id = self.run_id

        id = self.id

        created_at = self.created_at.isoformat()

        updated_at = self.updated_at.isoformat()

        emails: list[str] | Unset = UNSET
        if not isinstance(self.emails, Unset):
            emails = self.emails

        webhooks: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.webhooks, Unset):
            webhooks = []
            for webhooks_item_data in self.webhooks:
                webhooks_item = webhooks_item_data.to_dict()
                webhooks.append(webhooks_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({"run_id": run_id, "id": id, "created_at": created_at, "updated_at": updated_at})
        if emails is not UNSET:
            field_dict["emails"] = emails
        if webhooks is not UNSET:
            field_dict["webhooks"] = webhooks

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.webhook import Webhook

        d = dict(src_dict)
        run_id = d.pop("run_id")

        id = d.pop("id")

        created_at = isoparse(d.pop("created_at"))

        updated_at = isoparse(d.pop("updated_at"))

        emails = cast(list[str], d.pop("emails", UNSET))

        _webhooks = d.pop("webhooks", UNSET)
        webhooks: list[Webhook] | Unset = UNSET
        if _webhooks is not UNSET:
            webhooks = []
            for webhooks_item_data in _webhooks:
                webhooks_item = Webhook.from_dict(webhooks_item_data)

                webhooks.append(webhooks_item)

        run_alert_settings_db = cls(
            run_id=run_id, id=id, created_at=created_at, updated_at=updated_at, emails=emails, webhooks=webhooks
        )

        run_alert_settings_db.additional_properties = d
        return run_alert_settings_db

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
