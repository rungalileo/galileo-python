from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="ScoreBucket")


@_attrs_define
class ScoreBucket:
    """
    Attributes:
        min_inclusive (int):
        max_exclusive (int | None):
        count (int):
    """

    min_inclusive: int
    max_exclusive: int | None
    count: int
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        min_inclusive = self.min_inclusive

        max_exclusive: int | None
        max_exclusive = self.max_exclusive

        count = self.count

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({"min_inclusive": min_inclusive, "max_exclusive": max_exclusive, "count": count})

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        min_inclusive = d.pop("min_inclusive")

        def _parse_max_exclusive(data: object) -> int | None:
            if data is None:
                return data
            return cast(int | None, data)

        max_exclusive = _parse_max_exclusive(d.pop("max_exclusive"))

        count = d.pop("count")

        score_bucket = cls(min_inclusive=min_inclusive, max_exclusive=max_exclusive, count=count)

        score_bucket.additional_properties = d
        return score_bucket

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
