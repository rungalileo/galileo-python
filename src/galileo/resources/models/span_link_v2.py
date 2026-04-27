from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="SpanLinkV2")


@_attrs_define
class SpanLinkV2:
    """
    Attributes:
        trace_id (str):
        span_id (str):
        span_sub_narrative (str):
    """

    trace_id: str
    span_id: str
    span_sub_narrative: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        trace_id = self.trace_id

        span_id = self.span_id

        span_sub_narrative = self.span_sub_narrative

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({"trace_id": trace_id, "span_id": span_id, "span_sub_narrative": span_sub_narrative})

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        trace_id = d.pop("trace_id")

        span_id = d.pop("span_id")

        span_sub_narrative = d.pop("span_sub_narrative")

        span_link_v2 = cls(trace_id=trace_id, span_id=span_id, span_sub_narrative=span_sub_narrative)

        span_link_v2.additional_properties = d
        return span_link_v2

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
