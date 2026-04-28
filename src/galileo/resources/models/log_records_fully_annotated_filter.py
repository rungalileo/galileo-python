from __future__ import annotations

from collections.abc import Mapping
from typing import Any, Literal, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="LogRecordsFullyAnnotatedFilter")


@_attrs_define
class LogRecordsFullyAnnotatedFilter:
    """Queue-scoped filter for records rated across all queue templates.

    Attributes
    ----------
        column_id (Literal['fully_annotated'] | Unset): Queue-scoped filter identifier. This filter only works for
            annotation-queue searches that provide queue context. Default: 'fully_annotated'.
        type_ (Literal['fully_annotated'] | Unset):  Default: 'fully_annotated'.
        user_ids (list[str] | None | Unset): Optional queue member IDs to require for full annotation in a queue-scoped
            search. If omitted, all tracked queue members visible to the requester are used.
    """

    column_id: Literal["fully_annotated"] | Unset = "fully_annotated"
    type_: Literal["fully_annotated"] | Unset = "fully_annotated"
    user_ids: list[str] | None | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        column_id = self.column_id

        type_ = self.type_

        user_ids: list[str] | None | Unset
        if isinstance(self.user_ids, Unset):
            user_ids = UNSET
        elif isinstance(self.user_ids, list):
            user_ids = self.user_ids

        else:
            user_ids = self.user_ids

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if column_id is not UNSET:
            field_dict["column_id"] = column_id
        if type_ is not UNSET:
            field_dict["type"] = type_
        if user_ids is not UNSET:
            field_dict["user_ids"] = user_ids

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        column_id = cast(Literal["fully_annotated"] | Unset, d.pop("column_id", UNSET))
        if column_id != "fully_annotated" and not isinstance(column_id, Unset):
            raise ValueError(f"column_id must match const 'fully_annotated', got '{column_id}'")

        type_ = cast(Literal["fully_annotated"] | Unset, d.pop("type", UNSET))
        if type_ != "fully_annotated" and not isinstance(type_, Unset):
            raise ValueError(f"type must match const 'fully_annotated', got '{type_}'")

        def _parse_user_ids(data: object) -> list[str] | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                return cast(list[str], data)

            except:  # noqa: E722
                pass
            return cast(list[str] | None | Unset, data)

        user_ids = _parse_user_ids(d.pop("user_ids", UNSET))

        log_records_fully_annotated_filter = cls(column_id=column_id, type_=type_, user_ids=user_ids)

        log_records_fully_annotated_filter.additional_properties = d
        return log_records_fully_annotated_filter

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
