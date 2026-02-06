from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="SelectColumns")


@_attrs_define
class SelectColumns:
    """
    Attributes
    ----------
        column_ids (Union[Unset, list[str]]):
        include_all_metrics (Union[Unset, bool]):  Default: False.
        include_all_feedback (Union[Unset, bool]):  Default: False.
    """

    column_ids: Union[Unset, list[str]] = UNSET
    include_all_metrics: Union[Unset, bool] = False
    include_all_feedback: Union[Unset, bool] = False
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        column_ids: Union[Unset, list[str]] = UNSET
        if not isinstance(self.column_ids, Unset):
            column_ids = self.column_ids

        include_all_metrics = self.include_all_metrics

        include_all_feedback = self.include_all_feedback

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if column_ids is not UNSET:
            field_dict["column_ids"] = column_ids
        if include_all_metrics is not UNSET:
            field_dict["include_all_metrics"] = include_all_metrics
        if include_all_feedback is not UNSET:
            field_dict["include_all_feedback"] = include_all_feedback

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        column_ids = cast(list[str], d.pop("column_ids", UNSET))

        include_all_metrics = d.pop("include_all_metrics", UNSET)

        include_all_feedback = d.pop("include_all_feedback", UNSET)

        select_columns = cls(
            column_ids=column_ids, include_all_metrics=include_all_metrics, include_all_feedback=include_all_feedback
        )

        select_columns.additional_properties = d
        return select_columns

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
