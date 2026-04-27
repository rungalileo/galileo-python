from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.span_link import SpanLink


T = TypeVar("T", bound="InsightExampleOccurrence")


@_attrs_define
class InsightExampleOccurrence:
    """
    Attributes:
        trace_id (str):
        example_narrative (str):
        span_links (list[SpanLink]):
    """

    trace_id: str
    example_narrative: str
    span_links: list[SpanLink]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        trace_id = self.trace_id

        example_narrative = self.example_narrative

        span_links = []
        for span_links_item_data in self.span_links:
            span_links_item = span_links_item_data.to_dict()
            span_links.append(span_links_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({"trace_id": trace_id, "example_narrative": example_narrative, "span_links": span_links})

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.span_link import SpanLink

        d = dict(src_dict)
        trace_id = d.pop("trace_id")

        example_narrative = d.pop("example_narrative")

        span_links = []
        _span_links = d.pop("span_links")
        for span_links_item_data in _span_links:
            span_links_item = SpanLink.from_dict(span_links_item_data)

            span_links.append(span_links_item)

        insight_example_occurrence = cls(trace_id=trace_id, example_narrative=example_narrative, span_links=span_links)

        insight_example_occurrence.additional_properties = d
        return insight_example_occurrence

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
