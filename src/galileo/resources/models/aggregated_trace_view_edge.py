from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="AggregatedTraceViewEdge")


@_attrs_define
class AggregatedTraceViewEdge:
    """
    Attributes
    ----------
        source (str):
        target (str):
        weight (float):
        occurrences (int):
        trace_count (int):
        trace_ids (list[str]):
    """

    source: str
    target: str
    weight: float
    occurrences: int
    trace_count: int
    trace_ids: list[str]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        source = self.source

        target = self.target

        weight = self.weight

        occurrences = self.occurrences

        trace_count = self.trace_count

        trace_ids = self.trace_ids

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "source": source,
                "target": target,
                "weight": weight,
                "occurrences": occurrences,
                "trace_count": trace_count,
                "trace_ids": trace_ids,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        source = d.pop("source")

        target = d.pop("target")

        weight = d.pop("weight")

        occurrences = d.pop("occurrences")

        trace_count = d.pop("trace_count")

        trace_ids = cast(list[str], d.pop("trace_ids"))

        aggregated_trace_view_edge = cls(
            source=source,
            target=target,
            weight=weight,
            occurrences=occurrences,
            trace_count=trace_count,
            trace_ids=trace_ids,
        )

        aggregated_trace_view_edge.additional_properties = d
        return aggregated_trace_view_edge

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
