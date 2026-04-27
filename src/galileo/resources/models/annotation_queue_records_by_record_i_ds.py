from __future__ import annotations

from collections.abc import Mapping
from typing import Any, Literal, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="AnnotationQueueRecordsByRecordIDs")


@_attrs_define
class AnnotationQueueRecordsByRecordIDs:
    """
    Attributes:
        record_ids (list[str]): List of log record IDs to select
        type_ (Literal['record_ids'] | Unset):  Default: 'record_ids'.
    """

    record_ids: list[str]
    type_: Literal["record_ids"] | Unset = "record_ids"
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        record_ids = self.record_ids

        type_ = self.type_

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({"record_ids": record_ids})
        if type_ is not UNSET:
            field_dict["type"] = type_

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        record_ids = cast(list[str], d.pop("record_ids"))

        type_ = cast(Literal["record_ids"] | Unset, d.pop("type", UNSET))
        if type_ != "record_ids" and not isinstance(type_, Unset):
            raise ValueError(f"type must match const 'record_ids', got '{type_}'")

        annotation_queue_records_by_record_i_ds = cls(record_ids=record_ids, type_=type_)

        annotation_queue_records_by_record_i_ds.additional_properties = d
        return annotation_queue_records_by_record_i_ds

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
