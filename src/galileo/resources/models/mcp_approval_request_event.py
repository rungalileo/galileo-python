from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, Literal, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.event_status import EventStatus
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.mcp_approval_request_event_metadata_type_0 import MCPApprovalRequestEventMetadataType0
    from ..models.mcp_approval_request_event_tool_invocation_type_0 import MCPApprovalRequestEventToolInvocationType0


T = TypeVar("T", bound="MCPApprovalRequestEvent")


@_attrs_define
class MCPApprovalRequestEvent:
    """MCP approval request - when human approval is needed for an MCP tool call.

    Attributes
    ----------
        type_ (Literal['mcp_approval_request'] | Unset):  Default: 'mcp_approval_request'.
        id (None | str | Unset): Unique identifier for the event
        status (EventStatus | None | Unset): Status of the event
        metadata (MCPApprovalRequestEventMetadataType0 | None | Unset): Provider-specific metadata and additional fields
        error_message (None | str | Unset): Error message if the event failed
        tool_name (None | str | Unset): Name of the MCP tool requiring approval
        tool_invocation (MCPApprovalRequestEventToolInvocationType0 | None | Unset): Details of the tool invocation
            requiring approval
        approved (bool | None | Unset): Whether the request was approved
    """

    type_: Literal["mcp_approval_request"] | Unset = "mcp_approval_request"
    id: None | str | Unset = UNSET
    status: EventStatus | None | Unset = UNSET
    metadata: MCPApprovalRequestEventMetadataType0 | None | Unset = UNSET
    error_message: None | str | Unset = UNSET
    tool_name: None | str | Unset = UNSET
    tool_invocation: MCPApprovalRequestEventToolInvocationType0 | None | Unset = UNSET
    approved: bool | None | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.mcp_approval_request_event_metadata_type_0 import MCPApprovalRequestEventMetadataType0
        from ..models.mcp_approval_request_event_tool_invocation_type_0 import (
            MCPApprovalRequestEventToolInvocationType0,
        )

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
        elif isinstance(self.metadata, MCPApprovalRequestEventMetadataType0):
            metadata = self.metadata.to_dict()
        else:
            metadata = self.metadata

        error_message: None | str | Unset
        error_message = UNSET if isinstance(self.error_message, Unset) else self.error_message

        tool_name: None | str | Unset
        tool_name = UNSET if isinstance(self.tool_name, Unset) else self.tool_name

        tool_invocation: dict[str, Any] | None | Unset
        if isinstance(self.tool_invocation, Unset):
            tool_invocation = UNSET
        elif isinstance(self.tool_invocation, MCPApprovalRequestEventToolInvocationType0):
            tool_invocation = self.tool_invocation.to_dict()
        else:
            tool_invocation = self.tool_invocation

        approved: bool | None | Unset
        approved = UNSET if isinstance(self.approved, Unset) else self.approved

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
        if tool_invocation is not UNSET:
            field_dict["tool_invocation"] = tool_invocation
        if approved is not UNSET:
            field_dict["approved"] = approved

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.mcp_approval_request_event_metadata_type_0 import MCPApprovalRequestEventMetadataType0
        from ..models.mcp_approval_request_event_tool_invocation_type_0 import (
            MCPApprovalRequestEventToolInvocationType0,
        )

        d = dict(src_dict)
        type_ = cast(Literal["mcp_approval_request"] | Unset, d.pop("type", UNSET))
        if type_ != "mcp_approval_request" and not isinstance(type_, Unset):
            raise ValueError(f"type must match const 'mcp_approval_request', got '{type_}'")

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

        def _parse_metadata(data: object) -> MCPApprovalRequestEventMetadataType0 | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                return MCPApprovalRequestEventMetadataType0.from_dict(data)

            except:  # noqa: E722
                pass
            return cast(MCPApprovalRequestEventMetadataType0 | None | Unset, data)

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

        def _parse_tool_invocation(data: object) -> MCPApprovalRequestEventToolInvocationType0 | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                return MCPApprovalRequestEventToolInvocationType0.from_dict(data)

            except:  # noqa: E722
                pass
            return cast(MCPApprovalRequestEventToolInvocationType0 | None | Unset, data)

        tool_invocation = _parse_tool_invocation(d.pop("tool_invocation", UNSET))

        def _parse_approved(data: object) -> bool | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(bool | None | Unset, data)

        approved = _parse_approved(d.pop("approved", UNSET))

        mcp_approval_request_event = cls(
            type_=type_,
            id=id,
            status=status,
            metadata=metadata,
            error_message=error_message,
            tool_name=tool_name,
            tool_invocation=tool_invocation,
            approved=approved,
        )

        mcp_approval_request_event.additional_properties = d
        return mcp_approval_request_event

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
