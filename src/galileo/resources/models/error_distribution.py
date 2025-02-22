from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="ErrorDistribution")


@_attrs_define
class ErrorDistribution:
    """
    Attributes:
        counts (Union[Unset, list[int]]):
        labels (Union[Unset, list[str]]):
        percentage (Union[Unset, float]):  Default: 0.0.
    """

    counts: Union[Unset, list[int]] = UNSET
    labels: Union[Unset, list[str]] = UNSET
    percentage: Union[Unset, float] = 0.0
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        counts: Union[Unset, list[int]] = UNSET
        if not isinstance(self.counts, Unset):
            counts = self.counts

        labels: Union[Unset, list[str]] = UNSET
        if not isinstance(self.labels, Unset):
            labels = self.labels

        percentage = self.percentage

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if counts is not UNSET:
            field_dict["counts"] = counts
        if labels is not UNSET:
            field_dict["labels"] = labels
        if percentage is not UNSET:
            field_dict["percentage"] = percentage

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        counts = cast(list[int], d.pop("counts", UNSET))

        labels = cast(list[str], d.pop("labels", UNSET))

        percentage = d.pop("percentage", UNSET)

        error_distribution = cls(counts=counts, labels=labels, percentage=percentage)

        error_distribution.additional_properties = d
        return error_distribution

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
