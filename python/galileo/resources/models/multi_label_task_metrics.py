from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="MultiLabelTaskMetrics")


@_attrs_define
class MultiLabelTaskMetrics:
    """Metrics per task for multi-label models.

    Attributes:
        f1 (Union[Unset, list[float]]):
        labels (Union[Unset, list[Union[bool, int, str]]]):
        precision (Union[Unset, list[float]]):
        recall (Union[Unset, list[float]]):
    """

    f1: Union[Unset, list[float]] = UNSET
    labels: Union[Unset, list[Union[bool, int, str]]] = UNSET
    precision: Union[Unset, list[float]] = UNSET
    recall: Union[Unset, list[float]] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        f1: Union[Unset, list[float]] = UNSET
        if not isinstance(self.f1, Unset):
            f1 = self.f1

        labels: Union[Unset, list[Union[bool, int, str]]] = UNSET
        if not isinstance(self.labels, Unset):
            labels = []
            for labels_item_data in self.labels:
                labels_item: Union[bool, int, str]
                labels_item = labels_item_data
                labels.append(labels_item)

        precision: Union[Unset, list[float]] = UNSET
        if not isinstance(self.precision, Unset):
            precision = self.precision

        recall: Union[Unset, list[float]] = UNSET
        if not isinstance(self.recall, Unset):
            recall = self.recall

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if f1 is not UNSET:
            field_dict["f1"] = f1
        if labels is not UNSET:
            field_dict["labels"] = labels
        if precision is not UNSET:
            field_dict["precision"] = precision
        if recall is not UNSET:
            field_dict["recall"] = recall

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        f1 = cast(list[float], d.pop("f1", UNSET))

        labels = []
        _labels = d.pop("labels", UNSET)
        for labels_item_data in _labels or []:

            def _parse_labels_item(data: object) -> Union[bool, int, str]:
                return cast(Union[bool, int, str], data)

            labels_item = _parse_labels_item(labels_item_data)

            labels.append(labels_item)

        precision = cast(list[float], d.pop("precision", UNSET))

        recall = cast(list[float], d.pop("recall", UNSET))

        multi_label_task_metrics = cls(f1=f1, labels=labels, precision=precision, recall=recall)

        multi_label_task_metrics.additional_properties = d
        return multi_label_task_metrics

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
