from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.logging_method import LoggingMethod
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.control_result import ControlResult
    from ..models.document import Document
    from ..models.file_content_part import FileContentPart
    from ..models.message import Message
    from ..models.text_content_part import TextContentPart


T = TypeVar("T", bound="LogSpanUpdateRequest")


@_attrs_define
class LogSpanUpdateRequest:
    """Request model for updating a span.

    Attributes
    ----------
        span_id (str): Span id to update.
        log_stream_id (None | str | Unset): Log stream id associated with the traces.
        experiment_id (None | str | Unset): Experiment id associated with the traces.
        metrics_testing_id (None | str | Unset): Metrics testing id associated with the traces.
        logging_method (LoggingMethod | Unset):
        client_version (None | str | Unset):
        reliable (bool | Unset): Whether or not to use reliable logging.  If set to False, the method will respond
            immediately before verifying that the traces have been successfully ingested, and no error message will be
            returned if ingestion fails.  If set to True, the method will wait for the traces to be successfully ingested or
            return an error message if there is an ingestion failure. Default: True.
        input_ (list[FileContentPart | TextContentPart] | list[Message] | None | str | Unset): Input of the span.
            Overwrites previous value if present.
        output (ControlResult | list[Document] | list[FileContentPart | TextContentPart] | Message | None | str |
            Unset): Output of the span. Overwrites previous value if present.
        tags (list[str] | None | Unset): Tags to add to the span.
        status_code (int | None | Unset): Status code of the span. Overwrites previous value if present.
        duration_ns (int | None | Unset): Duration in nanoseconds. Overwrites previous value if present.
    """

    span_id: str
    log_stream_id: None | str | Unset = UNSET
    experiment_id: None | str | Unset = UNSET
    metrics_testing_id: None | str | Unset = UNSET
    logging_method: LoggingMethod | Unset = UNSET
    client_version: None | str | Unset = UNSET
    reliable: bool | Unset = True
    input_: list[FileContentPart | TextContentPart] | list[Message] | None | str | Unset = UNSET
    output: ControlResult | list[Document] | list[FileContentPart | TextContentPart] | Message | None | str | Unset = (
        UNSET
    )
    tags: list[str] | None | Unset = UNSET
    status_code: int | None | Unset = UNSET
    duration_ns: int | None | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.control_result import ControlResult
        from ..models.message import Message
        from ..models.text_content_part import TextContentPart

        span_id = self.span_id

        log_stream_id: None | str | Unset
        log_stream_id = UNSET if isinstance(self.log_stream_id, Unset) else self.log_stream_id

        experiment_id: None | str | Unset
        experiment_id = UNSET if isinstance(self.experiment_id, Unset) else self.experiment_id

        metrics_testing_id: None | str | Unset
        metrics_testing_id = UNSET if isinstance(self.metrics_testing_id, Unset) else self.metrics_testing_id

        logging_method: str | Unset = UNSET
        if not isinstance(self.logging_method, Unset):
            logging_method = self.logging_method.value

        client_version: None | str | Unset
        client_version = UNSET if isinstance(self.client_version, Unset) else self.client_version

        reliable = self.reliable

        input_: list[dict[str, Any]] | None | str | Unset
        if isinstance(self.input_, Unset):
            input_ = UNSET
        elif isinstance(self.input_, list):
            input_ = []
            for input_type_1_item_data in self.input_:
                input_type_1_item = input_type_1_item_data.to_dict()
                input_.append(input_type_1_item)

        elif isinstance(self.input_, list):
            input_ = []
            for input_type_2_item_data in self.input_:
                input_type_2_item: dict[str, Any]
                if isinstance(input_type_2_item_data, TextContentPart):
                    input_type_2_item = input_type_2_item_data.to_dict()
                else:
                    input_type_2_item = input_type_2_item_data.to_dict()

                input_.append(input_type_2_item)

        else:
            input_ = self.input_

        output: dict[str, Any] | list[dict[str, Any]] | None | str | Unset
        if isinstance(self.output, Unset):
            output = UNSET
        elif isinstance(self.output, Message):
            output = self.output.to_dict()
        elif isinstance(self.output, list):
            output = []
            for output_type_2_item_data in self.output:
                output_type_2_item = output_type_2_item_data.to_dict()
                output.append(output_type_2_item)

        elif isinstance(self.output, list):
            output = []
            for output_type_3_item_data in self.output:
                output_type_3_item: dict[str, Any]
                if isinstance(output_type_3_item_data, TextContentPart):
                    output_type_3_item = output_type_3_item_data.to_dict()
                else:
                    output_type_3_item = output_type_3_item_data.to_dict()

                output.append(output_type_3_item)

        elif isinstance(self.output, ControlResult):
            output = self.output.to_dict()
        else:
            output = self.output

        tags: list[str] | None | Unset
        if isinstance(self.tags, Unset):
            tags = UNSET
        elif isinstance(self.tags, list):
            tags = self.tags

        else:
            tags = self.tags

        status_code: int | None | Unset
        status_code = UNSET if isinstance(self.status_code, Unset) else self.status_code

        duration_ns: int | None | Unset
        duration_ns = UNSET if isinstance(self.duration_ns, Unset) else self.duration_ns

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({"span_id": span_id})
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
        if input_ is not UNSET:
            field_dict["input"] = input_
        if output is not UNSET:
            field_dict["output"] = output
        if tags is not UNSET:
            field_dict["tags"] = tags
        if status_code is not UNSET:
            field_dict["status_code"] = status_code
        if duration_ns is not UNSET:
            field_dict["duration_ns"] = duration_ns

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.control_result import ControlResult
        from ..models.document import Document
        from ..models.file_content_part import FileContentPart
        from ..models.message import Message
        from ..models.text_content_part import TextContentPart

        d = dict(src_dict)
        span_id = d.pop("span_id")

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
        logging_method = UNSET if isinstance(_logging_method, Unset) else LoggingMethod(_logging_method)

        def _parse_client_version(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        client_version = _parse_client_version(d.pop("client_version", UNSET))

        reliable = d.pop("reliable", UNSET)

        def _parse_input_(data: object) -> list[FileContentPart | TextContentPart] | list[Message] | None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                input_type_1 = []
                _input_type_1 = data
                for input_type_1_item_data in _input_type_1:
                    input_type_1_item = Message.from_dict(input_type_1_item_data)

                    input_type_1.append(input_type_1_item)

                return input_type_1
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, list):
                    raise TypeError()
                input_type_2 = []
                _input_type_2 = data
                for input_type_2_item_data in _input_type_2:

                    def _parse_input_type_2_item(data: object) -> FileContentPart | TextContentPart:
                        try:
                            if not isinstance(data, dict):
                                raise TypeError()
                            return TextContentPart.from_dict(data)

                        except:  # noqa: E722
                            pass
                        if not isinstance(data, dict):
                            raise TypeError()
                        return FileContentPart.from_dict(data)

                    input_type_2_item = _parse_input_type_2_item(input_type_2_item_data)

                    input_type_2.append(input_type_2_item)

                return input_type_2
            except:  # noqa: E722
                pass
            return cast(list[FileContentPart | TextContentPart] | list[Message] | None | str | Unset, data)

        input_ = _parse_input_(d.pop("input", UNSET))

        def _parse_output(
            data: object,
        ) -> ControlResult | list[Document] | list[FileContentPart | TextContentPart] | Message | None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                return Message.from_dict(data)

            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, list):
                    raise TypeError()
                output_type_2 = []
                _output_type_2 = data
                for output_type_2_item_data in _output_type_2:
                    output_type_2_item = Document.from_dict(output_type_2_item_data)

                    output_type_2.append(output_type_2_item)

                return output_type_2
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, list):
                    raise TypeError()
                output_type_3 = []
                _output_type_3 = data
                for output_type_3_item_data in _output_type_3:

                    def _parse_output_type_3_item(data: object) -> FileContentPart | TextContentPart:
                        try:
                            if not isinstance(data, dict):
                                raise TypeError()
                            return TextContentPart.from_dict(data)

                        except:  # noqa: E722
                            pass
                        if not isinstance(data, dict):
                            raise TypeError()
                        return FileContentPart.from_dict(data)

                    output_type_3_item = _parse_output_type_3_item(output_type_3_item_data)

                    output_type_3.append(output_type_3_item)

                return output_type_3
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                return ControlResult.from_dict(data)

            except:  # noqa: E722
                pass
            return cast(
                ControlResult | list[Document] | list[FileContentPart | TextContentPart] | Message | None | str | Unset,
                data,
            )

        output = _parse_output(d.pop("output", UNSET))

        def _parse_tags(data: object) -> list[str] | None | Unset:
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
            return cast(list[str] | None | Unset, data)

        tags = _parse_tags(d.pop("tags", UNSET))

        def _parse_status_code(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        status_code = _parse_status_code(d.pop("status_code", UNSET))

        def _parse_duration_ns(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        duration_ns = _parse_duration_ns(d.pop("duration_ns", UNSET))

        log_span_update_request = cls(
            span_id=span_id,
            log_stream_id=log_stream_id,
            experiment_id=experiment_id,
            metrics_testing_id=metrics_testing_id,
            logging_method=logging_method,
            client_version=client_version,
            reliable=reliable,
            input_=input_,
            output=output,
            tags=tags,
            status_code=status_code,
            duration_ns=duration_ns,
        )

        log_span_update_request.additional_properties = d
        return log_span_update_request

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
