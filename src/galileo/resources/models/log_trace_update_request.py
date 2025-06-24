from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.logging_method import LoggingMethod
from ..types import UNSET, Unset

T = TypeVar("T", bound="LogTraceUpdateRequest")


@_attrs_define
class LogTraceUpdateRequest:
    """Request model for updating a trace.

    Attributes:
        trace_id (str): Trace id to update.
        client_version (Union[None, Unset, str]):
        experiment_id (Union[None, Unset, str]): Experiment id associated with the traces.
        input_ (Union[None, Unset, str]): Input of the trace. Overwrites previous value if present.
        is_complete (Union[None, Unset, bool]): Whether or not the records in this request are complete. Default: False.
        log_stream_id (Union[None, Unset, str]): Log stream id associated with the traces.
        logging_method (Union[Unset, LoggingMethod]):
        output (Union[None, Unset, str]): Output of the trace. Overwrites previous value if present.
        reliable (Union[Unset, bool]): Whether or not to use reliable logging.  If set to False, the method will respond
            immediately before verifying that the traces have been successfully ingested, and no error message will be
            returned if ingestion fails.  If set to True, the method will wait for the traces to be successfully ingested or
            return an error message if there is an ingestion failure. Default: False.
        status_code (Union[None, Unset, int]): Status code of the trace. Overwrites previous value if present.
        tags (Union[None, Unset, list[str]]): Tags to add to the trace.
    """

    trace_id: str
    client_version: Union[None, Unset, str] = UNSET
    experiment_id: Union[None, Unset, str] = UNSET
    input_: Union[None, Unset, str] = UNSET
    is_complete: Union[None, Unset, bool] = False
    log_stream_id: Union[None, Unset, str] = UNSET
    logging_method: Union[Unset, LoggingMethod] = UNSET
    output: Union[None, Unset, str] = UNSET
    reliable: Union[Unset, bool] = False
    status_code: Union[None, Unset, int] = UNSET
    tags: Union[None, Unset, list[str]] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        trace_id = self.trace_id

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

        input_: Union[None, Unset, str]
        if isinstance(self.input_, Unset):
            input_ = UNSET
        else:
            input_ = self.input_

        is_complete: Union[None, Unset, bool]
        if isinstance(self.is_complete, Unset):
            is_complete = UNSET
        else:
            is_complete = self.is_complete

        log_stream_id: Union[None, Unset, str]
        if isinstance(self.log_stream_id, Unset):
            log_stream_id = UNSET
        else:
            log_stream_id = self.log_stream_id

        logging_method: Union[Unset, str] = UNSET
        if not isinstance(self.logging_method, Unset):
            logging_method = self.logging_method.value

        output: Union[None, Unset, str]
        if isinstance(self.output, Unset):
            output = UNSET
        else:
            output = self.output

        reliable = self.reliable

        status_code: Union[None, Unset, int]
        if isinstance(self.status_code, Unset):
            status_code = UNSET
        else:
            status_code = self.status_code

        tags: Union[None, Unset, list[str]]
        if isinstance(self.tags, Unset):
            tags = UNSET
        elif isinstance(self.tags, list):
            tags = self.tags

        else:
            tags = self.tags

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({"trace_id": trace_id})
        if client_version is not UNSET:
            field_dict["client_version"] = client_version
        if experiment_id is not UNSET:
            field_dict["experiment_id"] = experiment_id
        if input_ is not UNSET:
            field_dict["input"] = input_
        if is_complete is not UNSET:
            field_dict["is_complete"] = is_complete
        if log_stream_id is not UNSET:
            field_dict["log_stream_id"] = log_stream_id
        if logging_method is not UNSET:
            field_dict["logging_method"] = logging_method
        if output is not UNSET:
            field_dict["output"] = output
        if reliable is not UNSET:
            field_dict["reliable"] = reliable
        if status_code is not UNSET:
            field_dict["status_code"] = status_code
        if tags is not UNSET:
            field_dict["tags"] = tags

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        trace_id = d.pop("trace_id")

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

        def _parse_input_(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        input_ = _parse_input_(d.pop("input", UNSET))

        def _parse_is_complete(data: object) -> Union[None, Unset, bool]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, bool], data)

        is_complete = _parse_is_complete(d.pop("is_complete", UNSET))

        def _parse_log_stream_id(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        log_stream_id = _parse_log_stream_id(d.pop("log_stream_id", UNSET))

        _logging_method = d.pop("logging_method", UNSET)
        logging_method: Union[Unset, LoggingMethod]
        if isinstance(_logging_method, Unset):
            logging_method = UNSET
        else:
            logging_method = LoggingMethod(_logging_method)

        def _parse_output(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        output = _parse_output(d.pop("output", UNSET))

        reliable = d.pop("reliable", UNSET)

        def _parse_status_code(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        status_code = _parse_status_code(d.pop("status_code", UNSET))

        def _parse_tags(data: object) -> Union[None, Unset, list[str]]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                tags_type_0 = cast(list[str], data)

                return tags_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, list[str]], data)

        tags = _parse_tags(d.pop("tags", UNSET))

        log_trace_update_request = cls(
            trace_id=trace_id,
            client_version=client_version,
            experiment_id=experiment_id,
            input_=input_,
            is_complete=is_complete,
            log_stream_id=log_stream_id,
            logging_method=logging_method,
            output=output,
            reliable=reliable,
            status_code=status_code,
            tags=tags,
        )

        log_trace_update_request.additional_properties = d
        return log_trace_update_request

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
