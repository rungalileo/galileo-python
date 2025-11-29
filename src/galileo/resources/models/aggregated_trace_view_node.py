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
        id (str):
        name (Union[None, str]):
        type_ (StepType):
        occurrences (int):
        parent_id (Union[None, str]):
        has_children (bool):
        metrics (AggregatedTraceViewNodeMetrics):
        trace_count (int):
        weight (float):
    """

    id: str
    name: Union[None, str]
    type_: StepType
    occurrences: int
    parent_id: Union[None, str]
    has_children: bool
    metrics: "AggregatedTraceViewNodeMetrics"
    trace_count: int
    weight: float
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        name: Union[None, str]
        name = self.name

        type_ = self.type_.value

        occurrences = self.occurrences

        parent_id: Union[None, str]
        parent_id = self.parent_id

        has_children = self.has_children

        metrics = self.metrics.to_dict()

        trace_count = self.trace_count

        weight = self.weight

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "name": name,
                "type": type_,
                "occurrences": occurrences,
                "parent_id": parent_id,
                "has_children": has_children,
                "metrics": metrics,
                "trace_count": trace_count,
                "weight": weight,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.aggregated_trace_view_node_metrics import AggregatedTraceViewNodeMetrics

        d = dict(src_dict)
        id = d.pop("id")

        def _parse_name(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        name = _parse_name(d.pop("name"))

        type_ = StepType(d.pop("type"))

        occurrences = d.pop("occurrences")

        def _parse_parent_id(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        parent_id = _parse_parent_id(d.pop("parent_id"))

        has_children = d.pop("has_children")

        metrics = AggregatedTraceViewNodeMetrics.from_dict(d.pop("metrics"))

        trace_count = d.pop("trace_count")

        weight = d.pop("weight")

        aggregated_trace_view_node = cls(
            id=id,
            name=name,
            type_=type_,
            occurrences=occurrences,
            parent_id=parent_id,
            has_children=has_children,
            metrics=metrics,
            trace_count=trace_count,
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
