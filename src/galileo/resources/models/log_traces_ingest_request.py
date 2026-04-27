from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.logging_method import LoggingMethod
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.trace import Trace


T = TypeVar("T", bound="LogTracesIngestRequest")


@_attrs_define
class LogTracesIngestRequest:
    """Request model for ingesting traces.

    Attributes:
        traces (list[Trace]): List of traces to log.
        log_stream_id (None | str | Unset): Log stream id associated with the traces.
        experiment_id (None | str | Unset): Experiment id associated with the traces.
        metrics_testing_id (None | str | Unset): Metrics testing id associated with the traces.
        logging_method (LoggingMethod | Unset):
        client_version (None | str | Unset):
        reliable (bool | Unset): Whether or not to use reliable logging.  If set to False, the method will respond
            immediately before verifying that the traces have been successfully ingested, and no error message will be
            returned if ingestion fails.  If set to True, the method will wait for the traces to be successfully ingested or
            return an error message if there is an ingestion failure. Default: True.
        session_id (None | str | Unset): Session id associated with the traces.
        session_external_id (None | str | Unset): External id of the session (e.g., OTEL session.id from span
            attributes).
        is_complete (bool | Unset): Whether or not the records in this request are complete. Default: True.
        include_trace_ids (bool | Unset): If True, include the list of ingested trace IDs in the response. Default:
            False.
    """

    traces: list[Trace]
    log_stream_id: None | str | Unset = UNSET
    experiment_id: None | str | Unset = UNSET
    metrics_testing_id: None | str | Unset = UNSET
    logging_method: LoggingMethod | Unset = UNSET
    client_version: None | str | Unset = UNSET
    reliable: bool | Unset = True
    session_id: None | str | Unset = UNSET
    session_external_id: None | str | Unset = UNSET
    is_complete: bool | Unset = True
    include_trace_ids: bool | Unset = False
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        traces = []
        for traces_item_data in self.traces:
            traces_item = traces_item_data.to_dict()
            traces.append(traces_item)

        log_stream_id: None | str | Unset
        if isinstance(self.log_stream_id, Unset):
            log_stream_id = UNSET
        else:
            log_stream_id = self.log_stream_id

        experiment_id: None | str | Unset
        if isinstance(self.experiment_id, Unset):
            experiment_id = UNSET
        else:
            experiment_id = self.experiment_id

        metrics_testing_id: None | str | Unset
        if isinstance(self.metrics_testing_id, Unset):
            metrics_testing_id = UNSET
        else:
            metrics_testing_id = self.metrics_testing_id

        logging_method: str | Unset = UNSET
        if not isinstance(self.logging_method, Unset):
            logging_method = self.logging_method.value

        client_version: None | str | Unset
        if isinstance(self.client_version, Unset):
            client_version = UNSET
        else:
            client_version = self.client_version

        reliable = self.reliable

        session_id: None | str | Unset
        if isinstance(self.session_id, Unset):
            session_id = UNSET
        else:
            session_id = self.session_id

        session_external_id: None | str | Unset
        if isinstance(self.session_external_id, Unset):
            session_external_id = UNSET
        else:
            session_external_id = self.session_external_id

        is_complete = self.is_complete

        include_trace_ids = self.include_trace_ids

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({"traces": traces})
        if log_stream_id is not UNSET:
            field_dict["log_stream_id"] = log_stream_id
        if experiment_id is not UNSET:
            field_dict["experiment_id"] = experiment_id
        if metrics_testing_id is not UNSET:
            field_dict["metrics_testing_id"] = metrics_testing_id
        if logging_method is not UNSET:
            field_dict["logging_method"] = logging_method
        if client_version is not UNSET:
            field_dict["client_version"] = client_version
        if reliable is not UNSET:
            field_dict["reliable"] = reliable
        if session_id is not UNSET:
            field_dict["session_id"] = session_id
        if session_external_id is not UNSET:
            field_dict["session_external_id"] = session_external_id
        if is_complete is not UNSET:
            field_dict["is_complete"] = is_complete
        if include_trace_ids is not UNSET:
            field_dict["include_trace_ids"] = include_trace_ids

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.trace import Trace

        d = dict(src_dict)
        traces = []
        _traces = d.pop("traces")
        for traces_item_data in _traces:
            traces_item = Trace.from_dict(traces_item_data)

            traces.append(traces_item)

        def _parse_log_stream_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        log_stream_id = _parse_log_stream_id(d.pop("log_stream_id", UNSET))

        def _parse_experiment_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        experiment_id = _parse_experiment_id(d.pop("experiment_id", UNSET))

        def _parse_metrics_testing_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        metrics_testing_id = _parse_metrics_testing_id(d.pop("metrics_testing_id", UNSET))

        _logging_method = d.pop("logging_method", UNSET)
        logging_method: LoggingMethod | Unset
        if isinstance(_logging_method, Unset):
            logging_method = UNSET
        else:
            logging_method = LoggingMethod(_logging_method)

        def _parse_client_version(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        client_version = _parse_client_version(d.pop("client_version", UNSET))

        reliable = d.pop("reliable", UNSET)

        def _parse_session_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        session_id = _parse_session_id(d.pop("session_id", UNSET))

        def _parse_session_external_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        session_external_id = _parse_session_external_id(d.pop("session_external_id", UNSET))

        is_complete = d.pop("is_complete", UNSET)

        include_trace_ids = d.pop("include_trace_ids", UNSET)

        log_traces_ingest_request = cls(
            traces=traces,
            log_stream_id=log_stream_id,
            experiment_id=experiment_id,
            metrics_testing_id=metrics_testing_id,
            logging_method=logging_method,
            client_version=client_version,
            reliable=reliable,
            session_id=session_id,
            session_external_id=session_external_id,
            is_complete=is_complete,
            include_trace_ids=include_trace_ids,
        )

        log_traces_ingest_request.additional_properties = d
        return log_traces_ingest_request

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
