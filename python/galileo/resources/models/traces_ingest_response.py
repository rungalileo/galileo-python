from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="TracesIngestResponse")


@_attrs_define
class TracesIngestResponse:
    """
    Attributes:
        project_id (str): Project id associated with the traces.
        project_name (str): Project name associated with the traces.
        records_count (int): total number of records (traces & spans) ingested
        traces_count (int): total number of traces ingested
        experiment_id (Union[None, Unset, str]): Experiment id associated with the traces.
        log_stream_id (Union[None, Unset, str]): Log stream id associated with the traces.
    """

    project_id: str
    project_name: str
    records_count: int
    traces_count: int
    experiment_id: Union[None, Unset, str] = UNSET
    log_stream_id: Union[None, Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        project_id = self.project_id

        project_name = self.project_name

        records_count = self.records_count

        traces_count = self.traces_count

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
                "traces_count": traces_count,
            }
        )
        if experiment_id is not UNSET:
            field_dict["experiment_id"] = experiment_id
        if log_stream_id is not UNSET:
            field_dict["log_stream_id"] = log_stream_id

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        project_id = d.pop("project_id")

        project_name = d.pop("project_name")

        records_count = d.pop("records_count")

        traces_count = d.pop("traces_count")

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

        traces_ingest_response = cls(
            project_id=project_id,
            project_name=project_name,
            records_count=records_count,
            traces_count=traces_count,
            experiment_id=experiment_id,
            log_stream_id=log_stream_id,
        )

        traces_ingest_response.additional_properties = d
        return traces_ingest_response

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
