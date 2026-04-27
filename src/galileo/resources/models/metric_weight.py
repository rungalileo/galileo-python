from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.group_label import GroupLabel
from ..models.metric_descriptions import MetricDescriptions
from ..types import UNSET, Unset

T = TypeVar("T", bound="MetricWeight")


@_attrs_define
class MetricWeight:
    """
    Attributes:
        label (None | str | Unset):
        group_label (GroupLabel | None | Unset):
        description (MetricDescriptions | None | Unset):
        weight (float | Unset):  Default: 0.5.
    """

    label: None | str | Unset = UNSET
    group_label: GroupLabel | None | Unset = UNSET
    description: MetricDescriptions | None | Unset = UNSET
    weight: float | Unset = 0.5
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        label: None | str | Unset
        if isinstance(self.label, Unset):
            label = UNSET
        else:
            label = self.label

        group_label: None | str | Unset
        if isinstance(self.group_label, Unset):
            group_label = UNSET
        elif isinstance(self.group_label, GroupLabel):
            group_label = self.group_label.value
        else:
            group_label = self.group_label

        description: None | str | Unset
        if isinstance(self.description, Unset):
            description = UNSET
        elif isinstance(self.description, MetricDescriptions):
            description = self.description.value
        else:
            description = self.description

        weight = self.weight

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if label is not UNSET:
            field_dict["label"] = label
        if group_label is not UNSET:
            field_dict["group_label"] = group_label
        if description is not UNSET:
            field_dict["description"] = description
        if weight is not UNSET:
            field_dict["weight"] = weight

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)

        def _parse_label(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        label = _parse_label(d.pop("label", UNSET))

        def _parse_group_label(data: object) -> GroupLabel | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                group_label_type_0 = GroupLabel(data)

                return group_label_type_0
            except:  # noqa: E722
                pass
            return cast(GroupLabel | None | Unset, data)

        group_label = _parse_group_label(d.pop("group_label", UNSET))

        def _parse_description(data: object) -> MetricDescriptions | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                description_type_0 = MetricDescriptions(data)

                return description_type_0
            except:  # noqa: E722
                pass
            return cast(MetricDescriptions | None | Unset, data)

        description = _parse_description(d.pop("description", UNSET))

        weight = d.pop("weight", UNSET)

        metric_weight = cls(label=label, group_label=group_label, description=description, weight=weight)

        metric_weight.additional_properties = d
        return metric_weight

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
