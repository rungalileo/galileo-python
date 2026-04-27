from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.scorer_feedback_queue_status import ScorerFeedbackQueueStatus
from ..types import UNSET, Unset

T = TypeVar("T", bound="ScorerFeedbackQueueStatusResponse")


@_attrs_define
class ScorerFeedbackQueueStatusResponse:
    """Lightweight response for polling queue generation status.

    Attributes:
        queue_id (str): Queue ID
        queue_status (ScorerFeedbackQueueStatus): Status of a scorer feedback queue throughout its lifecycle.
        generation_error_message (None | str | Unset): Error message from the last failed generation attempt
        draft_prompt (None | str | Unset): Draft prompt if generation completed
    """

    queue_id: str
    queue_status: ScorerFeedbackQueueStatus
    generation_error_message: None | str | Unset = UNSET
    draft_prompt: None | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        queue_id = self.queue_id

        queue_status = self.queue_status.value

        generation_error_message: None | str | Unset
        if isinstance(self.generation_error_message, Unset):
            generation_error_message = UNSET
        else:
            generation_error_message = self.generation_error_message

        draft_prompt: None | str | Unset
        if isinstance(self.draft_prompt, Unset):
            draft_prompt = UNSET
        else:
            draft_prompt = self.draft_prompt

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({"queue_id": queue_id, "queue_status": queue_status})
        if generation_error_message is not UNSET:
            field_dict["generation_error_message"] = generation_error_message
        if draft_prompt is not UNSET:
            field_dict["draft_prompt"] = draft_prompt

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        queue_id = d.pop("queue_id")

        queue_status = ScorerFeedbackQueueStatus(d.pop("queue_status"))

        def _parse_generation_error_message(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        generation_error_message = _parse_generation_error_message(d.pop("generation_error_message", UNSET))

        def _parse_draft_prompt(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        draft_prompt = _parse_draft_prompt(d.pop("draft_prompt", UNSET))

        scorer_feedback_queue_status_response = cls(
            queue_id=queue_id,
            queue_status=queue_status,
            generation_error_message=generation_error_message,
            draft_prompt=draft_prompt,
        )

        scorer_feedback_queue_status_response.additional_properties = d
        return scorer_feedback_queue_status_response

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
