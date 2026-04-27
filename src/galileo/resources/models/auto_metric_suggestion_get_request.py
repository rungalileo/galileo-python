from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.auto_metric_suggestion_label import AutoMetricSuggestionLabel
from ..types import UNSET, Unset

T = TypeVar("T", bound="AutoMetricSuggestionGetRequest")


@_attrs_define
class AutoMetricSuggestionGetRequest:
    """
    Attributes:
        project_id (str):
        log_stream_id (str):
        label (AutoMetricSuggestionLabel | None | Unset):
        description (None | str | Unset):
        is_restart (bool | None | Unset):  Default: False.
    """

    project_id: str
    log_stream_id: str
    label: AutoMetricSuggestionLabel | None | Unset = UNSET
    description: None | str | Unset = UNSET
    is_restart: bool | None | Unset = False
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        project_id = self.project_id

        log_stream_id = self.log_stream_id

        label: None | str | Unset
        if isinstance(self.label, Unset):
            label = UNSET
        elif isinstance(self.label, AutoMetricSuggestionLabel):
            label = self.label.value
        else:
            label = self.label

        description: None | str | Unset
        if isinstance(self.description, Unset):
            description = UNSET
        else:
            description = self.description

        is_restart: bool | None | Unset
        if isinstance(self.is_restart, Unset):
            is_restart = UNSET
        else:
            is_restart = self.is_restart

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({"project_id": project_id, "log_stream_id": log_stream_id})
        if label is not UNSET:
            field_dict["label"] = label
        if description is not UNSET:
            field_dict["description"] = description
        if is_restart is not UNSET:
            field_dict["is_restart"] = is_restart

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        project_id = d.pop("project_id")

        log_stream_id = d.pop("log_stream_id")

        def _parse_label(data: object) -> AutoMetricSuggestionLabel | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                label_type_0 = AutoMetricSuggestionLabel(data)

                return label_type_0
            except:  # noqa: E722
                pass
            return cast(AutoMetricSuggestionLabel | None | Unset, data)

        label = _parse_label(d.pop("label", UNSET))

        def _parse_description(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        description = _parse_description(d.pop("description", UNSET))

        def _parse_is_restart(data: object) -> bool | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(bool | None | Unset, data)

        is_restart = _parse_is_restart(d.pop("is_restart", UNSET))

        auto_metric_suggestion_get_request = cls(
            project_id=project_id,
            log_stream_id=log_stream_id,
            label=label,
            description=description,
            is_restart=is_restart,
        )

        auto_metric_suggestion_get_request.additional_properties = d
        return auto_metric_suggestion_get_request

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
