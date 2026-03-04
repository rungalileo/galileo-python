from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.step_type import StepType
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.aggregated_trace_view_node_metrics import AggregatedTraceViewNodeMetrics
    from ..models.insight_summary import InsightSummary


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
        has_children (bool):
        metrics (AggregatedTraceViewNodeMetrics):
        trace_count (int):
        weight (float):
        parent_id (Union[None, Unset, str]):
        insights (Union[Unset, list['InsightSummary']]):
    """

    id: str
    name: Union[None, str]
    type_: StepType
    occurrences: int
    has_children: bool
    metrics: "AggregatedTraceViewNodeMetrics"
    trace_count: int
    weight: float
    parent_id: Union[None, Unset, str] = UNSET
    insights: Union[Unset, list["InsightSummary"]] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        name: Union[None, str]
        name = self.name

        type_ = self.type_.value

        occurrences = self.occurrences

        has_children = self.has_children

        metrics = self.metrics.to_dict()

        trace_count = self.trace_count

        weight = self.weight

        parent_id: Union[None, Unset, str]
        parent_id = UNSET if isinstance(self.parent_id, Unset) else self.parent_id

        insights: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.insights, Unset):
            insights = []
            for insights_item_data in self.insights:
                insights_item = insights_item_data.to_dict()
                insights.append(insights_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "name": name,
                "type": type_,
                "occurrences": occurrences,
                "has_children": has_children,
                "metrics": metrics,
                "trace_count": trace_count,
                "weight": weight,
            }
        )
        if parent_id is not UNSET:
            field_dict["parent_id"] = parent_id
        if insights is not UNSET:
            field_dict["insights"] = insights

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.aggregated_trace_view_node_metrics import AggregatedTraceViewNodeMetrics
        from ..models.insight_summary import InsightSummary

        d = dict(src_dict)
        id = d.pop("id")

        def _parse_name(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        name = _parse_name(d.pop("name"))

        type_ = StepType(d.pop("type"))

        occurrences = d.pop("occurrences")

        has_children = d.pop("has_children")

        metrics = AggregatedTraceViewNodeMetrics.from_dict(d.pop("metrics"))

        trace_count = d.pop("trace_count")

        weight = d.pop("weight")

        def _parse_parent_id(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        parent_id = _parse_parent_id(d.pop("parent_id", UNSET))

        insights = []
        _insights = d.pop("insights", UNSET)
        for insights_item_data in _insights or []:
            insights_item = InsightSummary.from_dict(insights_item_data)

            insights.append(insights_item)

        aggregated_trace_view_node = cls(
            id=id,
            name=name,
            type_=type_,
            occurrences=occurrences,
            has_children=has_children,
            metrics=metrics,
            trace_count=trace_count,
            weight=weight,
            parent_id=parent_id,
            insights=insights,
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
