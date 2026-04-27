from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="GeneratePromptResponse")


@_attrs_define
class GeneratePromptResponse:
    """Response schema for generate prompt request (202 Accepted).

    Attributes:
        task_id (str): Celery task ID for polling
        queue_id (str): Queue ID being processed
        scorer_id (str): Scorer ID
        feedback_count (int): Number of feedback items
        status (str): Current status (generating)
        message (str): Message with polling instructions
    """

    task_id: str
    queue_id: str
    scorer_id: str
    feedback_count: int
    status: str
    message: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        task_id = self.task_id

        queue_id = self.queue_id

        scorer_id = self.scorer_id

        feedback_count = self.feedback_count

        status = self.status

        message = self.message

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "task_id": task_id,
                "queue_id": queue_id,
                "scorer_id": scorer_id,
                "feedback_count": feedback_count,
                "status": status,
                "message": message,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        task_id = d.pop("task_id")

        queue_id = d.pop("queue_id")

        scorer_id = d.pop("scorer_id")

        feedback_count = d.pop("feedback_count")

        status = d.pop("status")

        message = d.pop("message")

        generate_prompt_response = cls(
            task_id=task_id,
            queue_id=queue_id,
            scorer_id=scorer_id,
            feedback_count=feedback_count,
            status=status,
            message=message,
        )

        generate_prompt_response.additional_properties = d
        return generate_prompt_response

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
