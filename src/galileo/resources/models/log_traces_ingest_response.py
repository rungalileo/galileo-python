from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="LogTracesIngestResponse")


@_attrs_define
class LogTracesIngestResponse:
    """
    Attributes
    ----------
        project_id (str): Project id associated with the traces.
        project_name (str): Project name associated with the traces.
        records_count (int): Total number of records ingested
        traces_count (int): total number of traces ingested
        log_stream_id (Union[None, Unset, str]): Log stream id associated with the traces.
        experiment_id (Union[None, Unset, str]): Experiment id associated with the traces.
        metrics_testing_id (Union[None, Unset, str]): Metrics testing id associated with the traces.
        session_id (Union[None, Unset, str]): Session id associated with the traces.
        trace_ids (Union[None, Unset, list[str]]): List of trace IDs that were ingested. Only included if
            include_trace_ids=True in request.
    """

    project_id: str
    project_name: str
    records_count: int
    traces_count: int
    log_stream_id: Union[None, Unset, str] = UNSET
    experiment_id: Union[None, Unset, str] = UNSET
    metrics_testing_id: Union[None, Unset, str] = UNSET
    session_id: Union[None, Unset, str] = UNSET
    trace_ids: Union[None, Unset, list[str]] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        project_id = self.project_id

        project_name = self.project_name

        records_count = self.records_count

        traces_count = self.traces_count

        log_stream_id: Union[None, Unset, str]
        log_stream_id = UNSET if isinstance(self.log_stream_id, Unset) else self.log_stream_id

        experiment_id: Union[None, Unset, str]
        experiment_id = UNSET if isinstance(self.experiment_id, Unset) else self.experiment_id

        metrics_testing_id: Union[None, Unset, str]
        metrics_testing_id = UNSET if isinstance(self.metrics_testing_id, Unset) else self.metrics_testing_id

        session_id: Union[None, Unset, str]
        session_id = UNSET if isinstance(self.session_id, Unset) else self.session_id

        trace_ids: Union[None, Unset, list[str]]
        if isinstance(self.trace_ids, Unset):
            trace_ids = UNSET
        elif isinstance(self.trace_ids, list):
            trace_ids = self.trace_ids

        else:
            trace_ids = self.trace_ids

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "project_id": project_id,
                "project_name": project_name,
                "records_count": records_count,
                "traces_count": traces_count,
            }
        )
        if log_stream_id is not UNSET:
            field_dict["log_stream_id"] = log_stream_id
        if experiment_id is not UNSET:
            field_dict["experiment_id"] = experiment_id
        if metrics_testing_id is not UNSET:
            field_dict["metrics_testing_id"] = metrics_testing_id
        if session_id is not UNSET:
            field_dict["session_id"] = session_id
        if trace_ids is not UNSET:
            field_dict["trace_ids"] = trace_ids

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        project_id = d.pop("project_id")

        project_name = d.pop("project_name")

        records_count = d.pop("records_count")

        traces_count = d.pop("traces_count")

        def _parse_log_stream_id(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        log_stream_id = _parse_log_stream_id(d.pop("log_stream_id", UNSET))

        def _parse_experiment_id(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        experiment_id = _parse_experiment_id(d.pop("experiment_id", UNSET))

        def _parse_metrics_testing_id(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        metrics_testing_id = _parse_metrics_testing_id(d.pop("metrics_testing_id", UNSET))

        def _parse_session_id(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        session_id = _parse_session_id(d.pop("session_id", UNSET))

        def _parse_trace_ids(data: object) -> Union[None, Unset, list[str]]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                return cast(list[str], data)

            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, list[str]], data)

        trace_ids = _parse_trace_ids(d.pop("trace_ids", UNSET))

        log_traces_ingest_response = cls(
            project_id=project_id,
            project_name=project_name,
            records_count=records_count,
            traces_count=traces_count,
            log_stream_id=log_stream_id,
            experiment_id=experiment_id,
            metrics_testing_id=metrics_testing_id,
            session_id=session_id,
            trace_ids=trace_ids,
        )

        log_traces_ingest_response.additional_properties = d
        return log_traces_ingest_response

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
