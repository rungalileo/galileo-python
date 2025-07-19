from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.aggregated_trace_view_graph import AggregatedTraceViewGraph


T = TypeVar("T", bound="AggregatedTraceViewResponse")


@_attrs_define
class AggregatedTraceViewResponse:
    """
    Attributes:
        graph (AggregatedTraceViewGraph):
        num_sessions (int): Number of sessions in the aggregated view
        num_traces (int): Number of traces in the aggregated view
    """

    graph: "AggregatedTraceViewGraph"
    num_sessions: int
    num_traces: int
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        graph = self.graph.to_dict()

        num_sessions = self.num_sessions

        num_traces = self.num_traces

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({"graph": graph, "num_sessions": num_sessions, "num_traces": num_traces})

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.aggregated_trace_view_graph import AggregatedTraceViewGraph

        d = dict(src_dict)
        graph = AggregatedTraceViewGraph.from_dict(d.pop("graph"))

        num_sessions = d.pop("num_sessions")

        num_traces = d.pop("num_traces")

        aggregated_trace_view_response = cls(graph=graph, num_sessions=num_sessions, num_traces=num_traces)

        aggregated_trace_view_response.additional_properties = d
        return aggregated_trace_view_response

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
