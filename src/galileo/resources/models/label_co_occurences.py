from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.target_labels import TargetLabels


T = TypeVar("T", bound="LabelCoOccurences")


@_attrs_define
class LabelCoOccurences:
    """Structure for each label co-occurrence response.

    Attributes:
        ids (list[int]):
        labels (list['TargetLabels']):
        starting_label (str):
    """

    ids: list[int]
    labels: list["TargetLabels"]
    starting_label: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        ids = self.ids

        labels = []
        for labels_item_data in self.labels:
            labels_item = labels_item_data.to_dict()
            labels.append(labels_item)

        starting_label = self.starting_label

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({"ids": ids, "labels": labels, "starting_label": starting_label})

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.target_labels import TargetLabels

        d = src_dict.copy()
        ids = cast(list[int], d.pop("ids"))

        labels = []
        _labels = d.pop("labels")
        for labels_item_data in _labels:
            labels_item = TargetLabels.from_dict(labels_item_data)

            labels.append(labels_item)

        starting_label = d.pop("starting_label")

        label_co_occurences = cls(ids=ids, labels=labels, starting_label=starting_label)

        label_co_occurences.additional_properties = d
        return label_co_occurences

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
