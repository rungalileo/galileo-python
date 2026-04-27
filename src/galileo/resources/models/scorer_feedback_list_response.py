from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.scorer_feedback_queue_status import ScorerFeedbackQueueStatus
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.enriched_scorer_feedback_item import EnrichedScorerFeedbackItem


T = TypeVar("T", bound="ScorerFeedbackListResponse")


@_attrs_define
class ScorerFeedbackListResponse:
    """Response schema for active queue feedback list.

    Attributes:
        total_count (int): Total number of feedback items in the active queue
        queue_id (None | str | Unset): ID of the active queue, null if no active queue
        queue_status (None | ScorerFeedbackQueueStatus | Unset): Status of the active queue, null if no active queue
        generation_task_id (None | str | Unset): Task ID for polling prompt generation, present when status is
            'generating'
        generation_error_message (None | str | Unset): Error message from the last failed generation attempt
        feedback_items (list[EnrichedScorerFeedbackItem] | Unset): List of feedback items with enriched data
    """

    total_count: int
    queue_id: None | str | Unset = UNSET
    queue_status: None | ScorerFeedbackQueueStatus | Unset = UNSET
    generation_task_id: None | str | Unset = UNSET
    generation_error_message: None | str | Unset = UNSET
    feedback_items: list[EnrichedScorerFeedbackItem] | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        total_count = self.total_count

        queue_id: None | str | Unset
        if isinstance(self.queue_id, Unset):
            queue_id = UNSET
        else:
            queue_id = self.queue_id

        queue_status: None | str | Unset
        if isinstance(self.queue_status, Unset):
            queue_status = UNSET
        elif isinstance(self.queue_status, ScorerFeedbackQueueStatus):
            queue_status = self.queue_status.value
        else:
            queue_status = self.queue_status

        generation_task_id: None | str | Unset
        if isinstance(self.generation_task_id, Unset):
            generation_task_id = UNSET
        else:
            generation_task_id = self.generation_task_id

        generation_error_message: None | str | Unset
        if isinstance(self.generation_error_message, Unset):
            generation_error_message = UNSET
        else:
            generation_error_message = self.generation_error_message

        feedback_items: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.feedback_items, Unset):
            feedback_items = []
            for feedback_items_item_data in self.feedback_items:
                feedback_items_item = feedback_items_item_data.to_dict()
                feedback_items.append(feedback_items_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({"total_count": total_count})
        if queue_id is not UNSET:
            field_dict["queue_id"] = queue_id
        if queue_status is not UNSET:
            field_dict["queue_status"] = queue_status
        if generation_task_id is not UNSET:
            field_dict["generation_task_id"] = generation_task_id
        if generation_error_message is not UNSET:
            field_dict["generation_error_message"] = generation_error_message
        if feedback_items is not UNSET:
            field_dict["feedback_items"] = feedback_items

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.enriched_scorer_feedback_item import EnrichedScorerFeedbackItem

        d = dict(src_dict)
        total_count = d.pop("total_count")

        def _parse_queue_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        queue_id = _parse_queue_id(d.pop("queue_id", UNSET))

        def _parse_queue_status(data: object) -> None | ScorerFeedbackQueueStatus | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                queue_status_type_0 = ScorerFeedbackQueueStatus(data)

                return queue_status_type_0
            except:  # noqa: E722
                pass
            return cast(None | ScorerFeedbackQueueStatus | Unset, data)

        queue_status = _parse_queue_status(d.pop("queue_status", UNSET))

        def _parse_generation_task_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        generation_task_id = _parse_generation_task_id(d.pop("generation_task_id", UNSET))

        def _parse_generation_error_message(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        generation_error_message = _parse_generation_error_message(d.pop("generation_error_message", UNSET))

        _feedback_items = d.pop("feedback_items", UNSET)
        feedback_items: list[EnrichedScorerFeedbackItem] | Unset = UNSET
        if _feedback_items is not UNSET:
            feedback_items = []
            for feedback_items_item_data in _feedback_items:
                feedback_items_item = EnrichedScorerFeedbackItem.from_dict(feedback_items_item_data)

                feedback_items.append(feedback_items_item)

        scorer_feedback_list_response = cls(
            total_count=total_count,
            queue_id=queue_id,
            queue_status=queue_status,
            generation_task_id=generation_task_id,
            generation_error_message=generation_error_message,
            feedback_items=feedback_items,
        )

        scorer_feedback_list_response.additional_properties = d
        return scorer_feedback_list_response

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
