import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.aggregated_trace_view_graph import AggregatedTraceViewGraph


T = TypeVar("T", bound="AggregatedTraceViewResponse")


@_attrs_define
class AggregatedTraceViewResponse:
    """
    Attributes:
        graph (AggregatedTraceViewGraph):
        has_all_traces (bool): Whether all traces were returned
        num_sessions (int): Number of sessions in the aggregated view
        num_traces (int): Number of traces in the aggregated view
        end_time (Union[None, Unset, datetime.datetime]): created_at of latest record of the aggregated view
        start_time (Union[None, Unset, datetime.datetime]): created_at of earliest record of the aggregated view
    """

    graph: "AggregatedTraceViewGraph"
    has_all_traces: bool
    num_sessions: int
    num_traces: int
    end_time: Union[None, Unset, datetime.datetime] = UNSET
    start_time: Union[None, Unset, datetime.datetime] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        graph = self.graph.to_dict()

        has_all_traces = self.has_all_traces

        num_sessions = self.num_sessions

        num_traces = self.num_traces

        end_time: Union[None, Unset, str]
        if isinstance(self.end_time, Unset):
            end_time = UNSET
        elif isinstance(self.end_time, datetime.datetime):
            end_time = self.end_time.isoformat()
        else:
            end_time = self.end_time

        start_time: Union[None, Unset, str]
        if isinstance(self.start_time, Unset):
            start_time = UNSET
        elif isinstance(self.start_time, datetime.datetime):
            start_time = self.start_time.isoformat()
        else:
            start_time = self.start_time

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {"graph": graph, "has_all_traces": has_all_traces, "num_sessions": num_sessions, "num_traces": num_traces}
        )
        if end_time is not UNSET:
            field_dict["end_time"] = end_time
        if start_time is not UNSET:
            field_dict["start_time"] = start_time

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.aggregated_trace_view_graph import AggregatedTraceViewGraph

        d = dict(src_dict)
        graph = AggregatedTraceViewGraph.from_dict(d.pop("graph"))

        has_all_traces = d.pop("has_all_traces")

        num_sessions = d.pop("num_sessions")

        num_traces = d.pop("num_traces")

        def _parse_end_time(data: object) -> Union[None, Unset, datetime.datetime]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                end_time_type_0 = isoparse(data)

                return end_time_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, datetime.datetime], data)

        end_time = _parse_end_time(d.pop("end_time", UNSET))

        def _parse_start_time(data: object) -> Union[None, Unset, datetime.datetime]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                start_time_type_0 = isoparse(data)

                return start_time_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, datetime.datetime], data)

        start_time = _parse_start_time(d.pop("start_time", UNSET))

        aggregated_trace_view_response = cls(
            graph=graph,
            has_all_traces=has_all_traces,
            num_sessions=num_sessions,
            num_traces=num_traces,
            end_time=end_time,
            start_time=start_time,
        )

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
