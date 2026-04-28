from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="MetricThreshold")


@_attrs_define
class MetricThreshold:
    """Threshold configuration for metrics.

    Defines how metric values are bucketed and displayed, including whether
    lower or higher values are considered better.

    Attributes
    ----------
            inverted (bool | Unset): Whether the column should be inverted for thresholds, i.e. if True, lower is better.
                Default: False.
            buckets (list[float | int] | Unset): Threshold buckets for the column. If the column is a metric, these are the
                thresholds for the column.
            display_value_levels (list[str] | Unset): Ordered list of strings that raw values get transformed to for
                displaying.
    """

    inverted: bool | Unset = False
    buckets: list[float | int] | Unset = UNSET
    display_value_levels: list[str] | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        inverted = self.inverted

        buckets: list[float | int] | Unset = UNSET
        if not isinstance(self.buckets, Unset):
            buckets = []
            for buckets_item_data in self.buckets:
                buckets_item: float | int
                buckets_item = buckets_item_data
                buckets.append(buckets_item)

        display_value_levels: list[str] | Unset = UNSET
        if not isinstance(self.display_value_levels, Unset):
            display_value_levels = self.display_value_levels

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if inverted is not UNSET:
            field_dict["inverted"] = inverted
        if buckets is not UNSET:
            field_dict["buckets"] = buckets
        if display_value_levels is not UNSET:
            field_dict["display_value_levels"] = display_value_levels

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        inverted = d.pop("inverted", UNSET)

        _buckets = d.pop("buckets", UNSET)
        buckets: list[float | int] | Unset = UNSET
        if _buckets is not UNSET:
            buckets = []
            for buckets_item_data in _buckets:

                def _parse_buckets_item(data: object) -> float | int:
                    return cast(float | int, data)

                buckets_item = _parse_buckets_item(buckets_item_data)

                buckets.append(buckets_item)

        display_value_levels = cast(list[str], d.pop("display_value_levels", UNSET))

        metric_threshold = cls(inverted=inverted, buckets=buckets, display_value_levels=display_value_levels)

        metric_threshold.additional_properties = d
        return metric_threshold

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
