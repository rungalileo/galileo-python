from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="LogTraceUpdateResponse")


@_attrs_define
class LogTraceUpdateResponse:
    """
    Attributes:
        project_id (str): Project id associated with the traces.
        project_name (str): Project name associated with the traces.
        records_count (int): Total number of records ingested
        session_id (str): Session id associated with the traces.
        trace_id (str): Trace id associated with the updated trace.
        experiment_id (Union[None, Unset, str]): Experiment id associated with the traces.
        log_stream_id (Union[None, Unset, str]): Log stream id associated with the traces.
    """

    project_id: str
    project_name: str
    records_count: int
    session_id: str
    trace_id: str
    experiment_id: Union[None, Unset, str] = UNSET
    log_stream_id: Union[None, Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        project_id = self.project_id

        project_name = self.project_name

        records_count = self.records_count

        session_id = self.session_id

        trace_id = self.trace_id

        experiment_id: Union[None, Unset, str]
        if isinstance(self.experiment_id, Unset):
            experiment_id = UNSET
        else:
            experiment_id = self.experiment_id

        log_stream_id: Union[None, Unset, str]
        if isinstance(self.log_stream_id, Unset):
            log_stream_id = UNSET
        else:
            log_stream_id = self.log_stream_id

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "project_id": project_id,
                "project_name": project_name,
                "records_count": records_count,
                "session_id": session_id,
                "trace_id": trace_id,
            }
        )
        if experiment_id is not UNSET:
            field_dict["experiment_id"] = experiment_id
        if log_stream_id is not UNSET:
            field_dict["log_stream_id"] = log_stream_id

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        project_id = d.pop("project_id")

        project_name = d.pop("project_name")

        records_count = d.pop("records_count")

        session_id = d.pop("session_id")

        trace_id = d.pop("trace_id")

        def _parse_experiment_id(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        experiment_id = _parse_experiment_id(d.pop("experiment_id", UNSET))

        def _parse_log_stream_id(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        log_stream_id = _parse_log_stream_id(d.pop("log_stream_id", UNSET))

        log_trace_update_response = cls(
            project_id=project_id,
            project_name=project_name,
            records_count=records_count,
            session_id=session_id,
            trace_id=trace_id,
            experiment_id=experiment_id,
            log_stream_id=log_stream_id,
        )

        log_trace_update_response.additional_properties = d
        return log_trace_update_response

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
