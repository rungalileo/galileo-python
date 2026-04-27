from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="SpanNoteV2")


@_attrs_define
class SpanNoteV2:
    """
    Attributes:
        trace_id (str):
        span_id (str):
        span_note (str):
        unique_span_identifying_substring (None | str | Unset):
    """

    trace_id: str
    span_id: str
    span_note: str
    unique_span_identifying_substring: None | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        trace_id = self.trace_id

        span_id = self.span_id

        span_note = self.span_note

        unique_span_identifying_substring: None | str | Unset
        if isinstance(self.unique_span_identifying_substring, Unset):
            unique_span_identifying_substring = UNSET
        else:
            unique_span_identifying_substring = self.unique_span_identifying_substring

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({"trace_id": trace_id, "span_id": span_id, "span_note": span_note})
        if unique_span_identifying_substring is not UNSET:
            field_dict["unique_span_identifying_substring"] = unique_span_identifying_substring

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        trace_id = d.pop("trace_id")

        span_id = d.pop("span_id")

        span_note = d.pop("span_note")

        def _parse_unique_span_identifying_substring(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        unique_span_identifying_substring = _parse_unique_span_identifying_substring(
            d.pop("unique_span_identifying_substring", UNSET)
        )

        span_note_v2 = cls(
            trace_id=trace_id,
            span_id=span_id,
            span_note=span_note,
            unique_span_identifying_substring=unique_span_identifying_substring,
        )

        span_note_v2.additional_properties = d
        return span_note_v2

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
