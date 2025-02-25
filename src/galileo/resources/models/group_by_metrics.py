from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="GroupByMetrics")


@_attrs_define
class GroupByMetrics:
    """Metrics for a cohort returned in columnar format.

    Each field in the class is of equal length (or len 0), mapping to the y-axis
    of each chart. The labels field contains the x-axis labels which apply to all
    y-axes for all charts created for this data.

    ex:
        labels: ["apple", "banana", "orange"]
        precision: [0.95, 0.55, 0.83]
        recall: [0.93, 0.25, 0.88]
        ...

        Attributes:
            confidence (Union[Unset, list[float]]):
            data_error_potential (Union[Unset, list[float]]):
            f1 (Union[Unset, list[float]]):
            ghost_span (Union[Unset, list[int]]):
            labels (Union[Unset, list[Union[bool, int, str]]]):
            missed_label (Union[Unset, list[int]]):
            precision (Union[Unset, list[float]]):
            recall (Union[Unset, list[float]]):
            span_shift (Union[Unset, list[int]]):
            support (Union[Unset, list[int]]):
            total_errors (Union[Unset, list[int]]):
            wrong_tag (Union[Unset, list[int]]):
    """

    confidence: Union[Unset, list[float]] = UNSET
    data_error_potential: Union[Unset, list[float]] = UNSET
    f1: Union[Unset, list[float]] = UNSET
    ghost_span: Union[Unset, list[int]] = UNSET
    labels: Union[Unset, list[Union[bool, int, str]]] = UNSET
    missed_label: Union[Unset, list[int]] = UNSET
    precision: Union[Unset, list[float]] = UNSET
    recall: Union[Unset, list[float]] = UNSET
    span_shift: Union[Unset, list[int]] = UNSET
    support: Union[Unset, list[int]] = UNSET
    total_errors: Union[Unset, list[int]] = UNSET
    wrong_tag: Union[Unset, list[int]] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        confidence: Union[Unset, list[float]] = UNSET
        if not isinstance(self.confidence, Unset):
            confidence = self.confidence

        data_error_potential: Union[Unset, list[float]] = UNSET
        if not isinstance(self.data_error_potential, Unset):
            data_error_potential = self.data_error_potential

        f1: Union[Unset, list[float]] = UNSET
        if not isinstance(self.f1, Unset):
            f1 = self.f1

        ghost_span: Union[Unset, list[int]] = UNSET
        if not isinstance(self.ghost_span, Unset):
            ghost_span = self.ghost_span

        labels: Union[Unset, list[Union[bool, int, str]]] = UNSET
        if not isinstance(self.labels, Unset):
            labels = []
            for labels_item_data in self.labels:
                labels_item: Union[bool, int, str]
                labels_item = labels_item_data
                labels.append(labels_item)

        missed_label: Union[Unset, list[int]] = UNSET
        if not isinstance(self.missed_label, Unset):
            missed_label = self.missed_label

        precision: Union[Unset, list[float]] = UNSET
        if not isinstance(self.precision, Unset):
            precision = self.precision

        recall: Union[Unset, list[float]] = UNSET
        if not isinstance(self.recall, Unset):
            recall = self.recall

        span_shift: Union[Unset, list[int]] = UNSET
        if not isinstance(self.span_shift, Unset):
            span_shift = self.span_shift

        support: Union[Unset, list[int]] = UNSET
        if not isinstance(self.support, Unset):
            support = self.support

        total_errors: Union[Unset, list[int]] = UNSET
        if not isinstance(self.total_errors, Unset):
            total_errors = self.total_errors

        wrong_tag: Union[Unset, list[int]] = UNSET
        if not isinstance(self.wrong_tag, Unset):
            wrong_tag = self.wrong_tag

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if confidence is not UNSET:
            field_dict["confidence"] = confidence
        if data_error_potential is not UNSET:
            field_dict["data_error_potential"] = data_error_potential
        if f1 is not UNSET:
            field_dict["f1"] = f1
        if ghost_span is not UNSET:
            field_dict["ghost_span"] = ghost_span
        if labels is not UNSET:
            field_dict["labels"] = labels
        if missed_label is not UNSET:
            field_dict["missed_label"] = missed_label
        if precision is not UNSET:
            field_dict["precision"] = precision
        if recall is not UNSET:
            field_dict["recall"] = recall
        if span_shift is not UNSET:
            field_dict["span_shift"] = span_shift
        if support is not UNSET:
            field_dict["support"] = support
        if total_errors is not UNSET:
            field_dict["total_errors"] = total_errors
        if wrong_tag is not UNSET:
            field_dict["wrong_tag"] = wrong_tag

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        confidence = cast(list[float], d.pop("confidence", UNSET))

        data_error_potential = cast(list[float], d.pop("data_error_potential", UNSET))

        f1 = cast(list[float], d.pop("f1", UNSET))

        ghost_span = cast(list[int], d.pop("ghost_span", UNSET))

        labels = []
        _labels = d.pop("labels", UNSET)
        for labels_item_data in _labels or []:

            def _parse_labels_item(data: object) -> Union[bool, int, str]:
                return cast(Union[bool, int, str], data)

            labels_item = _parse_labels_item(labels_item_data)

            labels.append(labels_item)

        missed_label = cast(list[int], d.pop("missed_label", UNSET))

        precision = cast(list[float], d.pop("precision", UNSET))

        recall = cast(list[float], d.pop("recall", UNSET))

        span_shift = cast(list[int], d.pop("span_shift", UNSET))

        support = cast(list[int], d.pop("support", UNSET))

        total_errors = cast(list[int], d.pop("total_errors", UNSET))

        wrong_tag = cast(list[int], d.pop("wrong_tag", UNSET))

        group_by_metrics = cls(
            confidence=confidence,
            data_error_potential=data_error_potential,
            f1=f1,
            ghost_span=ghost_span,
            labels=labels,
            missed_label=missed_label,
            precision=precision,
            recall=recall,
            span_shift=span_shift,
            support=support,
            total_errors=total_errors,
            wrong_tag=wrong_tag,
        )

        group_by_metrics.additional_properties = d
        return group_by_metrics

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
