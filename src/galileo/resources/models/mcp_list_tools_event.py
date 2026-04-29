from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, Literal, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.event_status import EventStatus
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.mcp_list_tools_event_metadata_type_0 import MCPListToolsEventMetadataType0
    from ..models.mcp_list_tools_event_tools_type_0_item import MCPListToolsEventToolsType0Item


T = TypeVar("T", bound="MCPListToolsEvent")


@_attrs_define
class MCPListToolsEvent:
    """MCP list tools event - when the model queries available MCP tools.

    Attributes
    ----------
        type_ (Union[Literal['mcp_list_tools'], Unset]):  Default: 'mcp_list_tools'.
        id (Union[None, Unset, str]): Unique identifier for the event
        status (Union[EventStatus, None, Unset]): Status of the event
        metadata (Union['MCPListToolsEventMetadataType0', None, Unset]): Provider-specific metadata and additional
            fields
        error_message (Union[None, Unset, str]): Error message if the event failed
        server_name (Union[None, Unset, str]): Name of the MCP server
        tools (Union[None, Unset, list['MCPListToolsEventToolsType0Item']]): List of available MCP tools
    """

    type_: Union[Literal["mcp_list_tools"], Unset] = "mcp_list_tools"
    id: Union[None, Unset, str] = UNSET
    status: Union[EventStatus, None, Unset] = UNSET
    metadata: Union["MCPListToolsEventMetadataType0", None, Unset] = UNSET
    error_message: Union[None, Unset, str] = UNSET
    server_name: Union[None, Unset, str] = UNSET
    tools: Union[None, Unset, list["MCPListToolsEventToolsType0Item"]] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.mcp_list_tools_event_metadata_type_0 import MCPListToolsEventMetadataType0

        type_ = self.type_

        id: Union[None, Unset, str]
        id = UNSET if isinstance(self.id, Unset) else self.id

        status: Union[None, Unset, str]
        if isinstance(self.status, Unset):
            status = UNSET
        elif isinstance(self.status, EventStatus):
            status = self.status.value
        else:
            status = self.status

        metadata: Union[None, Unset, dict[str, Any]]
        if isinstance(self.metadata, Unset):
            metadata = UNSET
        elif isinstance(self.metadata, MCPListToolsEventMetadataType0):
            metadata = self.metadata.to_dict()
        else:
            metadata = self.metadata

        error_message: Union[None, Unset, str]
        error_message = UNSET if isinstance(self.error_message, Unset) else self.error_message

        server_name: Union[None, Unset, str]
        server_name = UNSET if isinstance(self.server_name, Unset) else self.server_name

        tools: Union[None, Unset, list[dict[str, Any]]]
        if isinstance(self.tools, Unset):
            tools = UNSET
        elif isinstance(self.tools, list):
            tools = []
            for tools_type_0_item_data in self.tools:
                tools_type_0_item = tools_type_0_item_data.to_dict()
                tools.append(tools_type_0_item)

        else:
            tools = self.tools

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
        if server_name is not UNSET:
            field_dict["server_name"] = server_name
        if tools is not UNSET:
            field_dict["tools"] = tools

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.mcp_list_tools_event_metadata_type_0 import MCPListToolsEventMetadataType0
        from ..models.mcp_list_tools_event_tools_type_0_item import MCPListToolsEventToolsType0Item

        d = dict(src_dict)
        type_ = cast(Union[Literal["mcp_list_tools"], Unset], d.pop("type", UNSET))
        if type_ != "mcp_list_tools" and not isinstance(type_, Unset):
            raise ValueError(f"type must match const 'mcp_list_tools', got '{type_}'")

        def _parse_id(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        id = _parse_id(d.pop("id", UNSET))

        def _parse_status(data: object) -> Union[EventStatus, None, Unset]:
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
            return cast(Union[EventStatus, None, Unset], data)

        status = _parse_status(d.pop("status", UNSET))

        def _parse_metadata(data: object) -> Union["MCPListToolsEventMetadataType0", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                return MCPListToolsEventMetadataType0.from_dict(data)

            except:  # noqa: E722
                pass
            return cast(Union["MCPListToolsEventMetadataType0", None, Unset], data)

        metadata = _parse_metadata(d.pop("metadata", UNSET))

        def _parse_error_message(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        error_message = _parse_error_message(d.pop("error_message", UNSET))

        def _parse_server_name(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        server_name = _parse_server_name(d.pop("server_name", UNSET))

        def _parse_tools(data: object) -> Union[None, Unset, list["MCPListToolsEventToolsType0Item"]]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                tools_type_0 = []
                _tools_type_0 = data
                for tools_type_0_item_data in _tools_type_0:
                    tools_type_0_item = MCPListToolsEventToolsType0Item.from_dict(tools_type_0_item_data)

                    tools_type_0.append(tools_type_0_item)

                return tools_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, list["MCPListToolsEventToolsType0Item"]], data)

        tools = _parse_tools(d.pop("tools", UNSET))

        mcp_list_tools_event = cls(
            type_=type_,
            id=id,
            status=status,
            metadata=metadata,
            error_message=error_message,
            server_name=server_name,
            tools=tools,
        )

        mcp_list_tools_event.additional_properties = d
        return mcp_list_tools_event

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
