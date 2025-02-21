from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.label_co_occurences import LabelCoOccurences


T = TypeVar("T", bound="MultiLabelCoOccurrence")


@_attrs_define
class MultiLabelCoOccurrence:
    """Label co-occurrence across tasks.

    Attributes:
        co_occurrences (list['LabelCoOccurences']):
        num_samples (int):
        percent_samples (float):
    """

    co_occurrences: list["LabelCoOccurences"]
    num_samples: int
    percent_samples: float
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        co_occurrences = []
        for co_occurrences_item_data in self.co_occurrences:
            co_occurrences_item = co_occurrences_item_data.to_dict()
            co_occurrences.append(co_occurrences_item)

        num_samples = self.num_samples

        percent_samples = self.percent_samples

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {"co_occurrences": co_occurrences, "num_samples": num_samples, "percent_samples": percent_samples}
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.label_co_occurences import LabelCoOccurences

        d = src_dict.copy()
        co_occurrences = []
        _co_occurrences = d.pop("co_occurrences")
        for co_occurrences_item_data in _co_occurrences:
            co_occurrences_item = LabelCoOccurences.from_dict(co_occurrences_item_data)

            co_occurrences.append(co_occurrences_item)

        num_samples = d.pop("num_samples")

        percent_samples = d.pop("percent_samples")

        multi_label_co_occurrence = cls(
            co_occurrences=co_occurrences, num_samples=num_samples, percent_samples=percent_samples
        )

        multi_label_co_occurrence.additional_properties = d
        return multi_label_co_occurrence

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
