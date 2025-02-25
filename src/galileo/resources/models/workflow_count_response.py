from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="WorkflowCountResponse")


@_attrs_define
class WorkflowCountResponse:
    """
    Attributes:
        count (int):
        max_rows (Union[Unset, int]):  Default: 512.
        max_rows_exceeded (Union[Unset, bool]):  Default: False.
    """

    count: int
    max_rows: Union[Unset, int] = 512
    max_rows_exceeded: Union[Unset, bool] = False
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        count = self.count

        max_rows = self.max_rows

        max_rows_exceeded = self.max_rows_exceeded

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({"count": count})
        if max_rows is not UNSET:
            field_dict["max_rows"] = max_rows
        if max_rows_exceeded is not UNSET:
            field_dict["max_rows_exceeded"] = max_rows_exceeded

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        count = d.pop("count")

        max_rows = d.pop("max_rows", UNSET)

        max_rows_exceeded = d.pop("max_rows_exceeded", UNSET)

        workflow_count_response = cls(count=count, max_rows=max_rows, max_rows_exceeded=max_rows_exceeded)

        workflow_count_response.additional_properties = d
        return workflow_count_response

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
