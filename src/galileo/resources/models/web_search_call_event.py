from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, Literal, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.event_status import EventStatus
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.web_search_action import WebSearchAction
    from ..models.web_search_call_event_metadata_type_0 import WebSearchCallEventMetadataType0


T = TypeVar("T", bound="WebSearchCallEvent")


@_attrs_define
class WebSearchCallEvent:
    """An OpenAI-style web search call event.

    Attributes
    ----------
        action (WebSearchAction): Action payload for a web search call event.
        type_ (Union[Literal['web_search_call'], Unset]):  Default: 'web_search_call'.
        id (Union[None, Unset, str]): Unique identifier for the event
        status (Union[EventStatus, None, Unset]): Status of the event
        metadata (Union['WebSearchCallEventMetadataType0', None, Unset]): Provider-specific metadata and additional
            fields
        error_message (Union[None, Unset, str]): Error message if the event failed
    """

    action: "WebSearchAction"
    type_: Union[Literal["web_search_call"], Unset] = "web_search_call"
    id: Union[None, Unset, str] = UNSET
    status: Union[EventStatus, None, Unset] = UNSET
    metadata: Union["WebSearchCallEventMetadataType0", None, Unset] = UNSET
    error_message: Union[None, Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.web_search_call_event_metadata_type_0 import WebSearchCallEventMetadataType0

        action = self.action.to_dict()

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
        elif isinstance(self.metadata, WebSearchCallEventMetadataType0):
            metadata = self.metadata.to_dict()
        else:
            metadata = self.metadata

        error_message: Union[None, Unset, str]
        error_message = UNSET if isinstance(self.error_message, Unset) else self.error_message

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({"action": action})
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

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.web_search_action import WebSearchAction
        from ..models.web_search_call_event_metadata_type_0 import WebSearchCallEventMetadataType0

        d = dict(src_dict)
        action = WebSearchAction.from_dict(d.pop("action"))

        type_ = cast(Union[Literal["web_search_call"], Unset], d.pop("type", UNSET))
        if type_ != "web_search_call" and not isinstance(type_, Unset):
            raise ValueError(f"type must match const 'web_search_call', got '{type_}'")

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

        def _parse_metadata(data: object) -> Union["WebSearchCallEventMetadataType0", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                return WebSearchCallEventMetadataType0.from_dict(data)

            except:  # noqa: E722
                pass
            return cast(Union["WebSearchCallEventMetadataType0", None, Unset], data)

        metadata = _parse_metadata(d.pop("metadata", UNSET))

        def _parse_error_message(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        error_message = _parse_error_message(d.pop("error_message", UNSET))

        web_search_call_event = cls(
            action=action, type_=type_, id=id, status=status, metadata=metadata, error_message=error_message
        )

        web_search_call_event.additional_properties = d
        return web_search_call_event

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
