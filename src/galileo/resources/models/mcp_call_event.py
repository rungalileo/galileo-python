from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, Literal, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.event_status import EventStatus
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.mcp_call_event_arguments_type_0 import MCPCallEventArgumentsType0
    from ..models.mcp_call_event_metadata_type_0 import MCPCallEventMetadataType0
    from ..models.mcp_call_event_result_type_0 import MCPCallEventResultType0


T = TypeVar("T", bound="MCPCallEvent")


@_attrs_define
class MCPCallEvent:
    """A Model Context Protocol (MCP) tool call.

    MCP is a protocol for connecting LLMs to external tools/data sources.
    This is distinct from internal tools because it involves external integrations.

        Attributes:
            type_ (Literal['mcp_call'] | Unset):  Default: 'mcp_call'.
            id (None | str | Unset): Unique identifier for the event
            status (EventStatus | None | Unset): Status of the event
            metadata (MCPCallEventMetadataType0 | None | Unset): Provider-specific metadata and additional fields
            error_message (None | str | Unset): Error message if the event failed
            tool_name (None | str | Unset): Name of the MCP tool being called
            server_name (None | str | Unset): Name of the MCP server
            arguments (MCPCallEventArgumentsType0 | None | Unset): Arguments for the MCP tool call
            result (MCPCallEventResultType0 | None | Unset): Result from the MCP tool call
    """

    type_: Literal["mcp_call"] | Unset = "mcp_call"
    id: None | str | Unset = UNSET
    status: EventStatus | None | Unset = UNSET
    metadata: MCPCallEventMetadataType0 | None | Unset = UNSET
    error_message: None | str | Unset = UNSET
    tool_name: None | str | Unset = UNSET
    server_name: None | str | Unset = UNSET
    arguments: MCPCallEventArgumentsType0 | None | Unset = UNSET
    result: MCPCallEventResultType0 | None | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.mcp_call_event_arguments_type_0 import MCPCallEventArgumentsType0
        from ..models.mcp_call_event_metadata_type_0 import MCPCallEventMetadataType0
        from ..models.mcp_call_event_result_type_0 import MCPCallEventResultType0

        type_ = self.type_

        id: None | str | Unset
        if isinstance(self.id, Unset):
            id = UNSET
        else:
            id = self.id

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
        elif isinstance(self.metadata, MCPCallEventMetadataType0):
            metadata = self.metadata.to_dict()
        else:
            metadata = self.metadata

        error_message: None | str | Unset
        if isinstance(self.error_message, Unset):
            error_message = UNSET
        else:
            error_message = self.error_message

        tool_name: None | str | Unset
        if isinstance(self.tool_name, Unset):
            tool_name = UNSET
        else:
            tool_name = self.tool_name

        server_name: None | str | Unset
        if isinstance(self.server_name, Unset):
            server_name = UNSET
        else:
            server_name = self.server_name

        arguments: dict[str, Any] | None | Unset
        if isinstance(self.arguments, Unset):
            arguments = UNSET
        elif isinstance(self.arguments, MCPCallEventArgumentsType0):
            arguments = self.arguments.to_dict()
        else:
            arguments = self.arguments

        result: dict[str, Any] | None | Unset
        if isinstance(self.result, Unset):
            result = UNSET
        elif isinstance(self.result, MCPCallEventResultType0):
            result = self.result.to_dict()
        else:
            result = self.result

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
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
        if tool_name is not UNSET:
            field_dict["tool_name"] = tool_name
        if server_name is not UNSET:
            field_dict["server_name"] = server_name
        if arguments is not UNSET:
            field_dict["arguments"] = arguments
        if result is not UNSET:
            field_dict["result"] = result

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.mcp_call_event_arguments_type_0 import MCPCallEventArgumentsType0
        from ..models.mcp_call_event_metadata_type_0 import MCPCallEventMetadataType0
        from ..models.mcp_call_event_result_type_0 import MCPCallEventResultType0

        d = dict(src_dict)
        type_ = cast(Literal["mcp_call"] | Unset, d.pop("type", UNSET))
        if type_ != "mcp_call" and not isinstance(type_, Unset):
            raise ValueError(f"type must match const 'mcp_call', got '{type_}'")

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
                status_type_0 = EventStatus(data)

                return status_type_0
            except:  # noqa: E722
                pass
            return cast(EventStatus | None | Unset, data)

        status = _parse_status(d.pop("status", UNSET))

        def _parse_metadata(data: object) -> MCPCallEventMetadataType0 | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                metadata_type_0 = MCPCallEventMetadataType0.from_dict(data)

                return metadata_type_0
            except:  # noqa: E722
                pass
            return cast(MCPCallEventMetadataType0 | None | Unset, data)

        metadata = _parse_metadata(d.pop("metadata", UNSET))

        def _parse_error_message(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        error_message = _parse_error_message(d.pop("error_message", UNSET))

        def _parse_tool_name(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        tool_name = _parse_tool_name(d.pop("tool_name", UNSET))

        def _parse_server_name(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        server_name = _parse_server_name(d.pop("server_name", UNSET))

        def _parse_arguments(data: object) -> MCPCallEventArgumentsType0 | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                arguments_type_0 = MCPCallEventArgumentsType0.from_dict(data)

                return arguments_type_0
            except:  # noqa: E722
                pass
            return cast(MCPCallEventArgumentsType0 | None | Unset, data)

        arguments = _parse_arguments(d.pop("arguments", UNSET))

        def _parse_result(data: object) -> MCPCallEventResultType0 | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                result_type_0 = MCPCallEventResultType0.from_dict(data)

                return result_type_0
            except:  # noqa: E722
                pass
            return cast(MCPCallEventResultType0 | None | Unset, data)

        result = _parse_result(d.pop("result", UNSET))

        mcp_call_event = cls(
            type_=type_,
            id=id,
            status=status,
            metadata=metadata,
            error_message=error_message,
            tool_name=tool_name,
            server_name=server_name,
            arguments=arguments,
            result=result,
        )

        mcp_call_event.additional_properties = d
        return mcp_call_event

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
