from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.aggregated_trace_view_edge import AggregatedTraceViewEdge
    from ..models.aggregated_trace_view_node import AggregatedTraceViewNode
    from ..models.histogram import Histogram


T = TypeVar("T", bound="AggregatedTraceViewGraph")


@_attrs_define
class AggregatedTraceViewGraph:
    """
    Attributes
    ----------
        nodes (list['AggregatedTraceViewNode']):
        edges (list['AggregatedTraceViewEdge']):
        edge_occurrences_histogram (Union['Histogram', None, Unset]): Histogram of edge occurrence counts across the
            graph.
    """

    nodes: list["AggregatedTraceViewNode"]
    edges: list["AggregatedTraceViewEdge"]
    edge_occurrences_histogram: Union["Histogram", None, Unset] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.histogram import Histogram

        nodes = []
        for nodes_item_data in self.nodes:
            nodes_item = nodes_item_data.to_dict()
            nodes.append(nodes_item)

        edges = []
        for edges_item_data in self.edges:
            edges_item = edges_item_data.to_dict()
            edges.append(edges_item)

        edge_occurrences_histogram: Union[None, Unset, dict[str, Any]]
        if isinstance(self.edge_occurrences_histogram, Unset):
            edge_occurrences_histogram = UNSET
        elif isinstance(self.edge_occurrences_histogram, Histogram):
            edge_occurrences_histogram = self.edge_occurrences_histogram.to_dict()
        else:
            edge_occurrences_histogram = self.edge_occurrences_histogram

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({"nodes": nodes, "edges": edges})
        if edge_occurrences_histogram is not UNSET:
            field_dict["edge_occurrences_histogram"] = edge_occurrences_histogram

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.aggregated_trace_view_edge import AggregatedTraceViewEdge
        from ..models.aggregated_trace_view_node import AggregatedTraceViewNode
        from ..models.histogram import Histogram

        d = dict(src_dict)
        nodes = []
        _nodes = d.pop("nodes")
        for nodes_item_data in _nodes:
            nodes_item = AggregatedTraceViewNode.from_dict(nodes_item_data)

            nodes.append(nodes_item)

        edges = []
        _edges = d.pop("edges")
        for edges_item_data in _edges:
            edges_item = AggregatedTraceViewEdge.from_dict(edges_item_data)

            edges.append(edges_item)

        def _parse_edge_occurrences_histogram(data: object) -> Union["Histogram", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                return Histogram.from_dict(data)

            except:  # noqa: E722
                pass
            return cast(Union["Histogram", None, Unset], data)

        edge_occurrences_histogram = _parse_edge_occurrences_histogram(d.pop("edge_occurrences_histogram", UNSET))

        aggregated_trace_view_graph = cls(
            nodes=nodes, edges=edges, edge_occurrences_histogram=edge_occurrences_histogram
        )

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
