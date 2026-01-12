from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, Literal, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.event_status import EventStatus
from ..models.message_role import MessageRole
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.message_event_content_parts_type_0_item import MessageEventContentPartsType0Item
    from ..models.message_event_metadata_type_0 import MessageEventMetadataType0


T = TypeVar("T", bound="MessageEvent")


@_attrs_define
class MessageEvent:
    """An output message from the model.

    Attributes
    ----------
        role (MessageRole):
        type_ (Union[Literal['message'], Unset]):  Default: 'message'.
        id (Union[None, Unset, str]): Unique identifier for the event
        status (Union[EventStatus, None, Unset]): Status of the event
        metadata (Union['MessageEventMetadataType0', None, Unset]): Provider-specific metadata and additional fields
        error_message (Union[None, Unset, str]): Error message if the event failed
        content (Union[None, Unset, str]): Text content of the message
        content_parts (Union[None, Unset, list['MessageEventContentPartsType0Item']]): Structured content items (text,
            audio, images, etc.)
    """

    role: MessageRole
    type_: Union[Literal["message"], Unset] = "message"
    id: Union[None, Unset, str] = UNSET
    status: Union[EventStatus, None, Unset] = UNSET
    metadata: Union["MessageEventMetadataType0", None, Unset] = UNSET
    error_message: Union[None, Unset, str] = UNSET
    content: Union[None, Unset, str] = UNSET
    content_parts: Union[None, Unset, list["MessageEventContentPartsType0Item"]] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.message_event_metadata_type_0 import MessageEventMetadataType0

        role = self.role.value

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
        elif isinstance(self.metadata, MessageEventMetadataType0):
            metadata = self.metadata.to_dict()
        else:
            metadata = self.metadata

        error_message: Union[None, Unset, str]
        error_message = UNSET if isinstance(self.error_message, Unset) else self.error_message

        content: Union[None, Unset, str]
        content = UNSET if isinstance(self.content, Unset) else self.content

        content_parts: Union[None, Unset, list[dict[str, Any]]]
        if isinstance(self.content_parts, Unset):
            content_parts = UNSET
        elif isinstance(self.content_parts, list):
            content_parts = []
            for content_parts_type_0_item_data in self.content_parts:
                content_parts_type_0_item = content_parts_type_0_item_data.to_dict()
                content_parts.append(content_parts_type_0_item)

        else:
            content_parts = self.content_parts

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({"role": role})
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
        if content is not UNSET:
            field_dict["content"] = content
        if content_parts is not UNSET:
            field_dict["content_parts"] = content_parts

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.message_event_content_parts_type_0_item import MessageEventContentPartsType0Item
        from ..models.message_event_metadata_type_0 import MessageEventMetadataType0

        d = dict(src_dict)
        role = MessageRole(d.pop("role"))

        type_ = cast(Union[Literal["message"], Unset], d.pop("type", UNSET))
        if type_ != "message" and not isinstance(type_, Unset):
            raise ValueError(f"type must match const 'message', got '{type_}'")

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

        def _parse_metadata(data: object) -> Union["MessageEventMetadataType0", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                return MessageEventMetadataType0.from_dict(data)

            except:  # noqa: E722
                pass
            return cast(Union["MessageEventMetadataType0", None, Unset], data)

        metadata = _parse_metadata(d.pop("metadata", UNSET))

        def _parse_error_message(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        error_message = _parse_error_message(d.pop("error_message", UNSET))

        def _parse_content(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        content = _parse_content(d.pop("content", UNSET))

        def _parse_content_parts(data: object) -> Union[None, Unset, list["MessageEventContentPartsType0Item"]]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                content_parts_type_0 = []
                _content_parts_type_0 = data
                for content_parts_type_0_item_data in _content_parts_type_0:
                    content_parts_type_0_item = MessageEventContentPartsType0Item.from_dict(
                        content_parts_type_0_item_data
                    )

                    content_parts_type_0.append(content_parts_type_0_item)

                return content_parts_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, list["MessageEventContentPartsType0Item"]], data)

        content_parts = _parse_content_parts(d.pop("content_parts", UNSET))

        message_event = cls(
            role=role,
            type_=type_,
            id=id,
            status=status,
            metadata=metadata,
            error_message=error_message,
            content=content,
            content_parts=content_parts,
        )

        message_event.additional_properties = d
        return message_event

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
