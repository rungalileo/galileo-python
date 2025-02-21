from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.log_data_logging_method import LogDataLoggingMethod
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.trace import Trace


T = TypeVar("T", bound="TracesIngestRequest")


@_attrs_define
class TracesIngestRequest:
    """
    Attributes:
        traces (list['Trace']): List of traces to log.
        client_version (Union[None, Unset, str]):
        experiment_id (Union[None, Unset, str]): Experiment id associated with the traces.
        log_stream_id (Union[None, Unset, str]): Log stream id associated with the traces.
        logging_method (Union[Unset, LogDataLoggingMethod]):
    """

    traces: list["Trace"]
    client_version: Union[None, Unset, str] = UNSET
    experiment_id: Union[None, Unset, str] = UNSET
    log_stream_id: Union[None, Unset, str] = UNSET
    logging_method: Union[Unset, LogDataLoggingMethod] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        traces = []
        for traces_item_data in self.traces:
            traces_item = traces_item_data.to_dict()
            traces.append(traces_item)

        client_version: Union[None, Unset, str]
        if isinstance(self.client_version, Unset):
            client_version = UNSET
        else:
            client_version = self.client_version

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

        logging_method: Union[Unset, str] = UNSET
        if not isinstance(self.logging_method, Unset):
            logging_method = self.logging_method.value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({"traces": traces})
        if client_version is not UNSET:
            field_dict["client_version"] = client_version
        if experiment_id is not UNSET:
            field_dict["experiment_id"] = experiment_id
        if log_stream_id is not UNSET:
            field_dict["log_stream_id"] = log_stream_id
        if logging_method is not UNSET:
            field_dict["logging_method"] = logging_method

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.trace import Trace

        d = src_dict.copy()
        traces = []
        _traces = d.pop("traces")
        for traces_item_data in _traces:
            traces_item = Trace.from_dict(traces_item_data)

            traces.append(traces_item)

        def _parse_client_version(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        client_version = _parse_client_version(d.pop("client_version", UNSET))

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

        _logging_method = d.pop("logging_method", UNSET)
        logging_method: Union[Unset, LogDataLoggingMethod]
        if isinstance(_logging_method, Unset):
            logging_method = UNSET
        else:
            logging_method = LogDataLoggingMethod(_logging_method)

        traces_ingest_request = cls(
            traces=traces,
            client_version=client_version,
            experiment_id=experiment_id,
            log_stream_id=log_stream_id,
            logging_method=logging_method,
        )

        traces_ingest_request.additional_properties = d
        return traces_ingest_request

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
