from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, Literal, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.event_status import EventStatus
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.reasoning_event_metadata_type_0 import ReasoningEventMetadataType0


T = TypeVar("T", bound="ReasoningEvent")


@_attrs_define
class ReasoningEvent:
    """Internal reasoning/thinking from the model (e.g., OpenAI o1/o3 reasoning tokens).

    Attributes
    ----------
        type_ (Union[Literal['reasoning'], Unset]):  Default: 'reasoning'.
        id (Union[None, Unset, str]): Unique identifier for the event
        status (Union[EventStatus, None, Unset]): Status of the event
        metadata (Union['ReasoningEventMetadataType0', None, Unset]): Provider-specific metadata and additional fields
        error_message (Union[None, Unset, str]): Error message if the event failed
        content (Union[None, Unset, str]): The reasoning/thinking content
        summary (Union[None, Unset, str]): Summary of the reasoning
    """

    type_: Union[Literal["reasoning"], Unset] = "reasoning"
    id: Union[None, Unset, str] = UNSET
    status: Union[EventStatus, None, Unset] = UNSET
    metadata: Union["ReasoningEventMetadataType0", None, Unset] = UNSET
    error_message: Union[None, Unset, str] = UNSET
    content: Union[None, Unset, str] = UNSET
    summary: Union[None, Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.reasoning_event_metadata_type_0 import ReasoningEventMetadataType0

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
        elif isinstance(self.metadata, ReasoningEventMetadataType0):
            metadata = self.metadata.to_dict()
        else:
            metadata = self.metadata

        error_message: Union[None, Unset, str]
        error_message = UNSET if isinstance(self.error_message, Unset) else self.error_message

        content: Union[None, Unset, str]
        content = UNSET if isinstance(self.content, Unset) else self.content

        summary: Union[None, Unset, str]
        summary = UNSET if isinstance(self.summary, Unset) else self.summary

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
        if content is not UNSET:
            field_dict["content"] = content
        if summary is not UNSET:
            field_dict["summary"] = summary

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.reasoning_event_metadata_type_0 import ReasoningEventMetadataType0

        d = dict(src_dict)
        type_ = cast(Union[Literal["reasoning"], Unset], d.pop("type", UNSET))
        if type_ != "reasoning" and not isinstance(type_, Unset):
            raise ValueError(f"type must match const 'reasoning', got '{type_}'")

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

        def _parse_metadata(data: object) -> Union["ReasoningEventMetadataType0", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                return ReasoningEventMetadataType0.from_dict(data)

            except:  # noqa: E722
                pass
            return cast(Union["ReasoningEventMetadataType0", None, Unset], data)

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

        def _parse_summary(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        summary = _parse_summary(d.pop("summary", UNSET))

        reasoning_event = cls(
            type_=type_,
            id=id,
            status=status,
            metadata=metadata,
            error_message=error_message,
            content=content,
            summary=summary,
        )

        reasoning_event.additional_properties = d
        return reasoning_event

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
