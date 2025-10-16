from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.step_type import StepType

if TYPE_CHECKING:
    from ..models.aggregated_trace_view_node_metrics import AggregatedTraceViewNodeMetrics


T = TypeVar("T", bound="AggregatedTraceViewNode")


@_attrs_define
class AggregatedTraceViewNode:
    """
    Attributes
    ----------
        has_children (bool):
        id (str):
        metrics (AggregatedTraceViewNodeMetrics):
        name (Union[None, str]):
        occurrences (int):
        parent_id (Union[None, str]):
        trace_count (int):
        type_ (StepType):
        weight (float):
    """

    has_children: bool
    id: str
    metrics: "AggregatedTraceViewNodeMetrics"
    name: Union[None, str]
    occurrences: int
    parent_id: Union[None, str]
    trace_count: int
    type_: StepType
    weight: float
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        has_children = self.has_children

        id = self.id

        metrics = self.metrics.to_dict()

        name: Union[None, str]
        name = self.name

        occurrences = self.occurrences

        parent_id: Union[None, str]
        parent_id = self.parent_id

        trace_count = self.trace_count

        type_ = self.type_.value

        weight = self.weight

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "has_children": has_children,
                "id": id,
                "metrics": metrics,
                "name": name,
                "occurrences": occurrences,
                "parent_id": parent_id,
                "trace_count": trace_count,
                "type": type_,
                "weight": weight,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.aggregated_trace_view_node_metrics import AggregatedTraceViewNodeMetrics

        d = dict(src_dict)
        has_children = d.pop("has_children")

        id = d.pop("id")

        metrics = AggregatedTraceViewNodeMetrics.from_dict(d.pop("metrics"))

        def _parse_name(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        name = _parse_name(d.pop("name"))

        occurrences = d.pop("occurrences")

        def _parse_parent_id(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        parent_id = _parse_parent_id(d.pop("parent_id"))

        trace_count = d.pop("trace_count")

        type_ = StepType(d.pop("type"))

        weight = d.pop("weight")

        aggregated_trace_view_node = cls(
            has_children=has_children,
            id=id,
            metrics=metrics,
            name=name,
            occurrences=occurrences,
            parent_id=parent_id,
            trace_count=trace_count,
            type_=type_,
            weight=weight,
        )

        aggregated_trace_view_node.additional_properties = d
        return aggregated_trace_view_node

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
