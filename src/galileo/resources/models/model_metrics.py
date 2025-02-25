from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.distribution import Distribution
    from ..models.multi_label_task_metrics import MultiLabelTaskMetrics


T = TypeVar("T", bound="ModelMetrics")


@_attrs_define
class ModelMetrics:
    """
    Attributes:
        accuracy (float):
        f1 (float):
        precision (float):
        recall (float):
        confidence (Union[None, Unset, float]):
        dep_distribution (Union['Distribution', None, Unset]):
        multi_label_task_metrics (Union[Unset, MultiLabelTaskMetrics]): Metrics per task for multi-label models.
    """

    accuracy: float
    f1: float
    precision: float
    recall: float
    confidence: Union[None, Unset, float] = UNSET
    dep_distribution: Union["Distribution", None, Unset] = UNSET
    multi_label_task_metrics: Union[Unset, "MultiLabelTaskMetrics"] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.distribution import Distribution

        accuracy = self.accuracy

        f1 = self.f1

        precision = self.precision

        recall = self.recall

        confidence: Union[None, Unset, float]
        if isinstance(self.confidence, Unset):
            confidence = UNSET
        else:
            confidence = self.confidence

        dep_distribution: Union[None, Unset, dict[str, Any]]
        if isinstance(self.dep_distribution, Unset):
            dep_distribution = UNSET
        elif isinstance(self.dep_distribution, Distribution):
            dep_distribution = self.dep_distribution.to_dict()
        else:
            dep_distribution = self.dep_distribution

        multi_label_task_metrics: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.multi_label_task_metrics, Unset):
            multi_label_task_metrics = self.multi_label_task_metrics.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({"accuracy": accuracy, "f1": f1, "precision": precision, "recall": recall})
        if confidence is not UNSET:
            field_dict["confidence"] = confidence
        if dep_distribution is not UNSET:
            field_dict["dep_distribution"] = dep_distribution
        if multi_label_task_metrics is not UNSET:
            field_dict["multi_label_task_metrics"] = multi_label_task_metrics

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.distribution import Distribution
        from ..models.multi_label_task_metrics import MultiLabelTaskMetrics

        d = src_dict.copy()
        accuracy = d.pop("accuracy")

        f1 = d.pop("f1")

        precision = d.pop("precision")

        recall = d.pop("recall")

        def _parse_confidence(data: object) -> Union[None, Unset, float]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, float], data)

        confidence = _parse_confidence(d.pop("confidence", UNSET))

        def _parse_dep_distribution(data: object) -> Union["Distribution", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                dep_distribution_type_0 = Distribution.from_dict(data)

                return dep_distribution_type_0
            except:  # noqa: E722
                pass
            return cast(Union["Distribution", None, Unset], data)

        dep_distribution = _parse_dep_distribution(d.pop("dep_distribution", UNSET))

        _multi_label_task_metrics = d.pop("multi_label_task_metrics", UNSET)
        multi_label_task_metrics: Union[Unset, MultiLabelTaskMetrics]
        if isinstance(_multi_label_task_metrics, Unset):
            multi_label_task_metrics = UNSET
        else:
            multi_label_task_metrics = MultiLabelTaskMetrics.from_dict(_multi_label_task_metrics)

        model_metrics = cls(
            accuracy=accuracy,
            f1=f1,
            precision=precision,
            recall=recall,
            confidence=confidence,
            dep_distribution=dep_distribution,
            multi_label_task_metrics=multi_label_task_metrics,
        )

        model_metrics.additional_properties = d
        return model_metrics

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
