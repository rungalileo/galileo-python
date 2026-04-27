from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="DeleteScorerFeedbackResponse")


@_attrs_define
class DeleteScorerFeedbackResponse:
    """Response schema for bulk delete operation.

    Attributes:
        deleted_count (int): Number of feedback items successfully deleted
        deleted_ids (list[str]): List of feedback IDs that were deleted
    """

    deleted_count: int
    deleted_ids: list[str]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        deleted_count = self.deleted_count

        deleted_ids = self.deleted_ids

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({"deleted_count": deleted_count, "deleted_ids": deleted_ids})

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        deleted_count = d.pop("deleted_count")

        deleted_ids = cast(list[str], d.pop("deleted_ids"))

        delete_scorer_feedback_response = cls(deleted_count=deleted_count, deleted_ids=deleted_ids)

        delete_scorer_feedback_response.additional_properties = d
        return delete_scorer_feedback_response

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
