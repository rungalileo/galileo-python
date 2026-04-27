from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, Literal, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.event_status import EventStatus
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.reasoning_event_metadata_type_0 import ReasoningEventMetadataType0
    from ..models.reasoning_event_summary_type_1_item import ReasoningEventSummaryType1Item


T = TypeVar("T", bound="ReasoningEvent")


@_attrs_define
class ReasoningEvent:
    """Internal reasoning/thinking from the model (e.g., OpenAI o1/o3 reasoning tokens).

    Attributes:
        type_ (Literal['reasoning'] | Unset):  Default: 'reasoning'.
        id (None | str | Unset): Unique identifier for the event
        status (EventStatus | None | Unset): Status of the event
        metadata (None | ReasoningEventMetadataType0 | Unset): Provider-specific metadata and additional fields
        error_message (None | str | Unset): Error message if the event failed
        content (None | str | Unset): The reasoning/thinking content
        summary (list[ReasoningEventSummaryType1Item] | None | str | Unset): Summary of the reasoning
    """

    type_: Literal["reasoning"] | Unset = "reasoning"
    id: None | str | Unset = UNSET
    status: EventStatus | None | Unset = UNSET
    metadata: None | ReasoningEventMetadataType0 | Unset = UNSET
    error_message: None | str | Unset = UNSET
    content: None | str | Unset = UNSET
    summary: list[ReasoningEventSummaryType1Item] | None | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.reasoning_event_metadata_type_0 import ReasoningEventMetadataType0

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
        elif isinstance(self.metadata, ReasoningEventMetadataType0):
            metadata = self.metadata.to_dict()
        else:
            metadata = self.metadata

        error_message: None | str | Unset
        if isinstance(self.error_message, Unset):
            error_message = UNSET
        else:
            error_message = self.error_message

        content: None | str | Unset
        if isinstance(self.content, Unset):
            content = UNSET
        else:
            content = self.content

        summary: list[dict[str, Any]] | None | str | Unset
        if isinstance(self.summary, Unset):
            summary = UNSET
        elif isinstance(self.summary, list):
            summary = []
            for summary_type_1_item_data in self.summary:
                summary_type_1_item = summary_type_1_item_data.to_dict()
                summary.append(summary_type_1_item)

        else:
            summary = self.summary

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
        from ..models.reasoning_event_summary_type_1_item import ReasoningEventSummaryType1Item

        d = dict(src_dict)
        type_ = cast(Literal["reasoning"] | Unset, d.pop("type", UNSET))
        if type_ != "reasoning" and not isinstance(type_, Unset):
            raise ValueError(f"type must match const 'reasoning', got '{type_}'")

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

        def _parse_metadata(data: object) -> None | ReasoningEventMetadataType0 | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                metadata_type_0 = ReasoningEventMetadataType0.from_dict(data)

                return metadata_type_0
            except:  # noqa: E722
                pass
            return cast(None | ReasoningEventMetadataType0 | Unset, data)

        metadata = _parse_metadata(d.pop("metadata", UNSET))

        def _parse_error_message(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        error_message = _parse_error_message(d.pop("error_message", UNSET))

        def _parse_content(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        content = _parse_content(d.pop("content", UNSET))

        def _parse_summary(data: object) -> list[ReasoningEventSummaryType1Item] | None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                summary_type_1 = []
                _summary_type_1 = data
                for summary_type_1_item_data in _summary_type_1:
                    summary_type_1_item = ReasoningEventSummaryType1Item.from_dict(summary_type_1_item_data)

                    summary_type_1.append(summary_type_1_item)

                return summary_type_1
            except:  # noqa: E722
                pass
            return cast(list[ReasoningEventSummaryType1Item] | None | str | Unset, data)

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
