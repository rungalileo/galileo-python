from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.audit_log_record import AuditLogRecord


T = TypeVar("T", bound="AuditLogListResponse")


@_attrs_define
class AuditLogListResponse:
    """Response for audit log list endpoint.

    Attributes:
        records (list[AuditLogRecord]):
        next_cursor_id (int | None | Unset):
    """

    records: list[AuditLogRecord]
    next_cursor_id: int | None | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        records = []
        for records_item_data in self.records:
            records_item = records_item_data.to_dict()
            records.append(records_item)

        next_cursor_id: int | None | Unset
        if isinstance(self.next_cursor_id, Unset):
            next_cursor_id = UNSET
        else:
            next_cursor_id = self.next_cursor_id

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({"records": records})
        if next_cursor_id is not UNSET:
            field_dict["next_cursor_id"] = next_cursor_id

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.audit_log_record import AuditLogRecord

        d = dict(src_dict)
        records = []
        _records = d.pop("records")
        for records_item_data in _records:
            records_item = AuditLogRecord.from_dict(records_item_data)

            records.append(records_item)

        def _parse_next_cursor_id(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        next_cursor_id = _parse_next_cursor_id(d.pop("next_cursor_id", UNSET))

        audit_log_list_response = cls(records=records, next_cursor_id=next_cursor_id)

        audit_log_list_response.additional_properties = d
        return audit_log_list_response

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
