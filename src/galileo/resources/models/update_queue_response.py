from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="UpdateQueueResponse")


@_attrs_define
class UpdateQueueResponse:
    """Response schema for queue update request (200 OK).

    For abort action: Clears draft_prompt and generation_task_id, returns to pending state.
    For complete action: Sets status to completed and links queue to the resulting scorer version.

        Attributes:
            queue_id (str): Queue ID that was updated
            scorer_id (str): Scorer ID
            target_scorer_version_id (str): Target scorer version for the queue
            status (str): Current queue status after update
            message (str): Confirmation message
            result_scorer_id (None | str | Unset): Scorer that owns the result version (set on complete)
            result_scorer_version_id (None | str | Unset): Scorer version created from this queue (set on complete)
    """

    queue_id: str
    scorer_id: str
    target_scorer_version_id: str
    status: str
    message: str
    result_scorer_id: None | str | Unset = UNSET
    result_scorer_version_id: None | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        queue_id = self.queue_id

        scorer_id = self.scorer_id

        target_scorer_version_id = self.target_scorer_version_id

        status = self.status

        message = self.message

        result_scorer_id: None | str | Unset
        if isinstance(self.result_scorer_id, Unset):
            result_scorer_id = UNSET
        else:
            result_scorer_id = self.result_scorer_id

        result_scorer_version_id: None | str | Unset
        if isinstance(self.result_scorer_version_id, Unset):
            result_scorer_version_id = UNSET
        else:
            result_scorer_version_id = self.result_scorer_version_id

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "queue_id": queue_id,
                "scorer_id": scorer_id,
                "target_scorer_version_id": target_scorer_version_id,
                "status": status,
                "message": message,
            }
        )
        if result_scorer_id is not UNSET:
            field_dict["result_scorer_id"] = result_scorer_id
        if result_scorer_version_id is not UNSET:
            field_dict["result_scorer_version_id"] = result_scorer_version_id

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        queue_id = d.pop("queue_id")

        scorer_id = d.pop("scorer_id")

        target_scorer_version_id = d.pop("target_scorer_version_id")

        status = d.pop("status")

        message = d.pop("message")

        def _parse_result_scorer_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        result_scorer_id = _parse_result_scorer_id(d.pop("result_scorer_id", UNSET))

        def _parse_result_scorer_version_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        result_scorer_version_id = _parse_result_scorer_version_id(d.pop("result_scorer_version_id", UNSET))

        update_queue_response = cls(
            queue_id=queue_id,
            scorer_id=scorer_id,
            target_scorer_version_id=target_scorer_version_id,
            status=status,
            message=message,
            result_scorer_id=result_scorer_id,
            result_scorer_version_id=result_scorer_version_id,
        )

        update_queue_response.additional_properties = d
        return update_queue_response

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
