from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.queue_action import QueueAction
from ..types import UNSET, Unset

T = TypeVar("T", bound="UpdateQueueRequest")


@_attrs_define
class UpdateQueueRequest:
    """Request schema for updating a feedback queue state via PATCH.

    Used to perform actions on a queue, such as aborting generation/review or completing the queue.

        Attributes:
            action (QueueAction): Actions that can be performed on a feedback queue.
            target_scorer_version_id (None | str | Unset): Required for 'complete' action: ID of the scorer version that
                feedback was applied to
            result_scorer_id (None | str | Unset): Required for 'complete' action: ID of the scorer that owns the result
                version. For custom LLM scorers this is the same scorer. For preset scorers this is the new custom scorer.
            result_scorer_version_id (None | str | Unset): Required for 'complete' action: ID of the scorer version created
                from this queue's feedback
    """

    action: QueueAction
    target_scorer_version_id: None | str | Unset = UNSET
    result_scorer_id: None | str | Unset = UNSET
    result_scorer_version_id: None | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        action = self.action.value

        target_scorer_version_id: None | str | Unset
        if isinstance(self.target_scorer_version_id, Unset):
            target_scorer_version_id = UNSET
        else:
            target_scorer_version_id = self.target_scorer_version_id

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
        field_dict.update({"action": action})
        if target_scorer_version_id is not UNSET:
            field_dict["target_scorer_version_id"] = target_scorer_version_id
        if result_scorer_id is not UNSET:
            field_dict["result_scorer_id"] = result_scorer_id
        if result_scorer_version_id is not UNSET:
            field_dict["result_scorer_version_id"] = result_scorer_version_id

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        action = QueueAction(d.pop("action"))

        def _parse_target_scorer_version_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        target_scorer_version_id = _parse_target_scorer_version_id(d.pop("target_scorer_version_id", UNSET))

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

        update_queue_request = cls(
            action=action,
            target_scorer_version_id=target_scorer_version_id,
            result_scorer_id=result_scorer_id,
            result_scorer_version_id=result_scorer_version_id,
        )

        update_queue_request.additional_properties = d
        return update_queue_request

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
