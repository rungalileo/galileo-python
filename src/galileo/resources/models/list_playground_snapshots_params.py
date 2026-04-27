from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.playground_snapshot_created_at_sort import PlaygroundSnapshotCreatedAtSort


T = TypeVar("T", bound="ListPlaygroundSnapshotsParams")


@_attrs_define
class ListPlaygroundSnapshotsParams:
    """
    Attributes:
        sort (PlaygroundSnapshotCreatedAtSort | Unset):
    """

    sort: PlaygroundSnapshotCreatedAtSort | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        sort: dict[str, Any] | Unset = UNSET
        if not isinstance(self.sort, Unset):
            sort = self.sort.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if sort is not UNSET:
            field_dict["sort"] = sort

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.playground_snapshot_created_at_sort import PlaygroundSnapshotCreatedAtSort

        d = dict(src_dict)
        _sort = d.pop("sort", UNSET)
        sort: PlaygroundSnapshotCreatedAtSort | Unset
        if isinstance(_sort, Unset):
            sort = UNSET
        else:
            sort = PlaygroundSnapshotCreatedAtSort.from_dict(_sort)

        list_playground_snapshots_params = cls(sort=sort)

        list_playground_snapshots_params.additional_properties = d
        return list_playground_snapshots_params

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
