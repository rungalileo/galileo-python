from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="JobProgress")


@_attrs_define
class JobProgress:
    """
    Attributes:
        progress_message (None | str | Unset):
        steps_completed (int | None | Unset):
        steps_total (int | None | Unset):
    """

    progress_message: None | str | Unset = UNSET
    steps_completed: int | None | Unset = UNSET
    steps_total: int | None | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        progress_message: None | str | Unset
        if isinstance(self.progress_message, Unset):
            progress_message = UNSET
        else:
            progress_message = self.progress_message

        steps_completed: int | None | Unset
        if isinstance(self.steps_completed, Unset):
            steps_completed = UNSET
        else:
            steps_completed = self.steps_completed

        steps_total: int | None | Unset
        if isinstance(self.steps_total, Unset):
            steps_total = UNSET
        else:
            steps_total = self.steps_total

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if progress_message is not UNSET:
            field_dict["progress_message"] = progress_message
        if steps_completed is not UNSET:
            field_dict["steps_completed"] = steps_completed
        if steps_total is not UNSET:
            field_dict["steps_total"] = steps_total

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)

        def _parse_progress_message(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        progress_message = _parse_progress_message(d.pop("progress_message", UNSET))

        def _parse_steps_completed(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        steps_completed = _parse_steps_completed(d.pop("steps_completed", UNSET))

        def _parse_steps_total(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        steps_total = _parse_steps_total(d.pop("steps_total", UNSET))

        job_progress = cls(progress_message=progress_message, steps_completed=steps_completed, steps_total=steps_total)

        job_progress.additional_properties = d
        return job_progress

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
