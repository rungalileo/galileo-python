from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.audit_action import AuditAction
from ..types import UNSET, Unset

T = TypeVar("T", bound="AuditLogRecord")


@_attrs_define
class AuditLogRecord:
    """Single audit log record for query responses.

    Attributes:
        id (int):
        created_at (datetime.datetime):
        user_id (str):
        action (AuditAction):
        raw_event (str):
        ip_address (str | Unset):  Default: ''.
    """

    id: int
    created_at: datetime.datetime
    user_id: str
    action: AuditAction
    raw_event: str
    ip_address: str | Unset = ""
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        created_at = self.created_at.isoformat()

        user_id = self.user_id

        action = self.action.value

        raw_event = self.raw_event

        ip_address = self.ip_address

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {"id": id, "created_at": created_at, "user_id": user_id, "action": action, "raw_event": raw_event}
        )
        if ip_address is not UNSET:
            field_dict["ip_address"] = ip_address

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = d.pop("id")

        created_at = isoparse(d.pop("created_at"))

        user_id = d.pop("user_id")

        action = AuditAction(d.pop("action"))

        raw_event = d.pop("raw_event")

        ip_address = d.pop("ip_address", UNSET)

        audit_log_record = cls(
            id=id, created_at=created_at, user_id=user_id, action=action, raw_event=raw_event, ip_address=ip_address
        )

        audit_log_record.additional_properties = d
        return audit_log_record

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
