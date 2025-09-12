from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.bulk_delete_failure import BulkDeleteFailure


T = TypeVar("T", bound="BulkDeleteDatasetsResponse")


@_attrs_define
class BulkDeleteDatasetsResponse:
    """Response from bulk deletion operation.

    Attributes:
        deleted_count (int):
        message (str):
        failed_deletions (Union[Unset, list['BulkDeleteFailure']]):
    """

    deleted_count: int
    message: str
    failed_deletions: Union[Unset, list["BulkDeleteFailure"]] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        deleted_count = self.deleted_count

        message = self.message

        failed_deletions: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.failed_deletions, Unset):
            failed_deletions = []
            for failed_deletions_item_data in self.failed_deletions:
                failed_deletions_item = failed_deletions_item_data.to_dict()
                failed_deletions.append(failed_deletions_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({"deleted_count": deleted_count, "message": message})
        if failed_deletions is not UNSET:
            field_dict["failed_deletions"] = failed_deletions

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.bulk_delete_failure import BulkDeleteFailure

        d = dict(src_dict)
        deleted_count = d.pop("deleted_count")

        message = d.pop("message")

        failed_deletions = []
        _failed_deletions = d.pop("failed_deletions", UNSET)
        for failed_deletions_item_data in _failed_deletions or []:
            failed_deletions_item = BulkDeleteFailure.from_dict(failed_deletions_item_data)

            failed_deletions.append(failed_deletions_item)

        bulk_delete_datasets_response = cls(
            deleted_count=deleted_count, message=message, failed_deletions=failed_deletions
        )

        bulk_delete_datasets_response.additional_properties = d
        return bulk_delete_datasets_response

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
