from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="BulkDeleteFailure")


@_attrs_define
class BulkDeleteFailure:
    """Details about a failed deletion.

    Attributes:
        dataset_id (str):
        dataset_name (str):
        reason (str):
    """

    dataset_id: str
    dataset_name: str
    reason: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        dataset_id = self.dataset_id

        dataset_name = self.dataset_name

        reason = self.reason

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({"dataset_id": dataset_id, "dataset_name": dataset_name, "reason": reason})

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        dataset_id = d.pop("dataset_id")

        dataset_name = d.pop("dataset_name")

        reason = d.pop("reason")

        bulk_delete_failure = cls(dataset_id=dataset_id, dataset_name=dataset_name, reason=reason)

        bulk_delete_failure.additional_properties = d
        return bulk_delete_failure

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
