from collections.abc import Mapping
from typing import Any, TypeVar, Optional, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast

if TYPE_CHECKING:
    from ..models.aggregated_trace_view_node import AggregatedTraceViewNode
    from ..models.aggregated_trace_view_edge import AggregatedTraceViewEdge


T = TypeVar("T", bound="AggregatedTraceViewGraph")


@_attrs_define
class AggregatedTraceViewGraph:
    """
    Attributes:
        edges (list['AggregatedTraceViewEdge']):
        nodes (list['AggregatedTraceViewNode']):
    """

    edges: list["AggregatedTraceViewEdge"]
    nodes: list["AggregatedTraceViewNode"]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.aggregated_trace_view_node import AggregatedTraceViewNode
        from ..models.aggregated_trace_view_edge import AggregatedTraceViewEdge

        edges = []
        for edges_item_data in self.edges:
            edges_item = edges_item_data.to_dict()
            edges.append(edges_item)

        nodes = []
        for nodes_item_data in self.nodes:
            nodes_item = nodes_item_data.to_dict()
            nodes.append(nodes_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({"edges": edges, "nodes": nodes})

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.aggregated_trace_view_node import AggregatedTraceViewNode
        from ..models.aggregated_trace_view_edge import AggregatedTraceViewEdge

        d = dict(src_dict)
        edges = []
        _edges = d.pop("edges")
        for edges_item_data in _edges:
            edges_item = AggregatedTraceViewEdge.from_dict(edges_item_data)

            edges.append(edges_item)

        nodes = []
        _nodes = d.pop("nodes")
        for nodes_item_data in _nodes:
            nodes_item = AggregatedTraceViewNode.from_dict(nodes_item_data)

            nodes.append(nodes_item)

        aggregated_trace_view_graph = cls(edges=edges, nodes=nodes)

        aggregated_trace_view_graph.additional_properties = d
        return aggregated_trace_view_graph

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
