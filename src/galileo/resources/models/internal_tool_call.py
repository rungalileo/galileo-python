from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, Literal, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.event_status import EventStatus
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.internal_tool_call_input_type_0 import InternalToolCallInputType0
    from ..models.internal_tool_call_metadata_type_0 import InternalToolCallMetadataType0
    from ..models.internal_tool_call_output_type_0 import InternalToolCallOutputType0


T = TypeVar("T", bound="InternalToolCall")


@_attrs_define
class InternalToolCall:
    """A tool call executed internally by the model during reasoning.

    This represents internal tools like web search, code execution, file search, etc.
    that the model invokes (not user-defined functions or MCP tools).

    Attributes
    ----------
            name (str): Name of the internal tool (e.g., 'web_search', 'code_interpreter', 'file_search')
            type_ (Literal['internal_tool_call'] | Unset):  Default: 'internal_tool_call'.
            id (None | str | Unset): Unique identifier for the event
            status (EventStatus | None | Unset): Status of the event
            metadata (InternalToolCallMetadataType0 | None | Unset): Provider-specific metadata and additional fields
            error_message (None | str | Unset): Error message if the event failed
            input_ (InternalToolCallInputType0 | None | Unset): Input/arguments to the tool call
            output (InternalToolCallOutputType0 | None | Unset): Output/results from the tool call
    """

    name: str
    type_: Literal["internal_tool_call"] | Unset = "internal_tool_call"
    id: None | str | Unset = UNSET
    status: EventStatus | None | Unset = UNSET
    metadata: InternalToolCallMetadataType0 | None | Unset = UNSET
    error_message: None | str | Unset = UNSET
    input_: InternalToolCallInputType0 | None | Unset = UNSET
    output: InternalToolCallOutputType0 | None | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.internal_tool_call_input_type_0 import InternalToolCallInputType0
        from ..models.internal_tool_call_metadata_type_0 import InternalToolCallMetadataType0
        from ..models.internal_tool_call_output_type_0 import InternalToolCallOutputType0

        name = self.name

        type_ = self.type_

        id: None | str | Unset
        id = UNSET if isinstance(self.id, Unset) else self.id

        status: None | str | Unset
        if isinstance(self.status, Unset):
            status = UNSET
        elif isinstance(self.status, EventStatus):
            status = self.status.value
        else:
            status = self.status

        metadata: dict[str, Any] | None | Unset
        if isinstance(self.metadata, Unset):
            metadata = UNSET
        elif isinstance(self.metadata, InternalToolCallMetadataType0):
            metadata = self.metadata.to_dict()
        else:
            metadata = self.metadata

        error_message: None | str | Unset
        error_message = UNSET if isinstance(self.error_message, Unset) else self.error_message

        input_: dict[str, Any] | None | Unset
        if isinstance(self.input_, Unset):
            input_ = UNSET
        elif isinstance(self.input_, InternalToolCallInputType0):
            input_ = self.input_.to_dict()
        else:
            input_ = self.input_

        output: dict[str, Any] | None | Unset
        if isinstance(self.output, Unset):
            output = UNSET
        elif isinstance(self.output, InternalToolCallOutputType0):
            output = self.output.to_dict()
        else:
            output = self.output

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({"name": name})
        if type_ is not UNSET:
            field_dict["type"] = type_
        if id is not UNSET:
            field_dict["id"] = id
        if status is not UNSET:
            field_dict["status"] = status
        if metadata is not UNSET:
            field_dict["metadata"] = metadata
        if error_message is not UNSET:
            field_dict["error_message"] = error_message
        if input_ is not UNSET:
            field_dict["input"] = input_
        if output is not UNSET:
            field_dict["output"] = output

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.internal_tool_call_input_type_0 import InternalToolCallInputType0
        from ..models.internal_tool_call_metadata_type_0 import InternalToolCallMetadataType0
        from ..models.internal_tool_call_output_type_0 import InternalToolCallOutputType0

        d = dict(src_dict)
        name = d.pop("name")

        type_ = cast(Literal["internal_tool_call"] | Unset, d.pop("type", UNSET))
        if type_ != "internal_tool_call" and not isinstance(type_, Unset):
            raise ValueError(f"type must match const 'internal_tool_call', got '{type_}'")

        def _parse_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        id = _parse_id(d.pop("id", UNSET))

        def _parse_status(data: object) -> EventStatus | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                return EventStatus(data)

            except:  # noqa: E722
                pass
            return cast(EventStatus | None | Unset, data)

        status = _parse_status(d.pop("status", UNSET))

        def _parse_metadata(data: object) -> InternalToolCallMetadataType0 | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                return InternalToolCallMetadataType0.from_dict(data)

            except:  # noqa: E722
                pass
            return cast(InternalToolCallMetadataType0 | None | Unset, data)

        metadata = _parse_metadata(d.pop("metadata", UNSET))

        def _parse_error_message(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        error_message = _parse_error_message(d.pop("error_message", UNSET))

        def _parse_input_(data: object) -> InternalToolCallInputType0 | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                return InternalToolCallInputType0.from_dict(data)

            except:  # noqa: E722
                pass
            return cast(InternalToolCallInputType0 | None | Unset, data)

        input_ = _parse_input_(d.pop("input", UNSET))

        def _parse_output(data: object) -> InternalToolCallOutputType0 | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                return InternalToolCallOutputType0.from_dict(data)

            except:  # noqa: E722
                pass
            return cast(InternalToolCallOutputType0 | None | Unset, data)

        output = _parse_output(d.pop("output", UNSET))

        internal_tool_call = cls(
            name=name,
            type_=type_,
            id=id,
            status=status,
            metadata=metadata,
            error_message=error_message,
            input_=input_,
            output=output,
        )

        internal_tool_call.additional_properties = d
        return internal_tool_call

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
