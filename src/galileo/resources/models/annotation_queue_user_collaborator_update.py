from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.collaborator_role import CollaboratorRole
from ..types import UNSET, Unset

T = TypeVar("T", bound="AnnotationQueueUserCollaboratorUpdate")


@_attrs_define
class AnnotationQueueUserCollaboratorUpdate:
    """
    Attributes:
        role (CollaboratorRole):
        track_progress (bool | None | Unset):
    """

    role: CollaboratorRole
    track_progress: bool | None | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        role = self.role.value

        track_progress: bool | None | Unset
        if isinstance(self.track_progress, Unset):
            track_progress = UNSET
        else:
            track_progress = self.track_progress

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({"role": role})
        if track_progress is not UNSET:
            field_dict["track_progress"] = track_progress

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        role = CollaboratorRole(d.pop("role"))

        def _parse_track_progress(data: object) -> bool | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(bool | None | Unset, data)

        track_progress = _parse_track_progress(d.pop("track_progress", UNSET))

        annotation_queue_user_collaborator_update = cls(role=role, track_progress=track_progress)

        annotation_queue_user_collaborator_update.additional_properties = d
        return annotation_queue_user_collaborator_update

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
