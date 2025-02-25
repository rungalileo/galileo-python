from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.split import Split
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.filter_params import FilterParams
    from ..models.multi_label_task_metrics import MultiLabelTaskMetrics


T = TypeVar("T", bound="MetricsResponse")


@_attrs_define
class MetricsResponse:
    """
    Attributes:
        accuracy (Union[None, Unset, float]):
        compare_to (Union[None, Split, Unset]):
        confidence (Union[None, Unset, float]):
        data_error_potential (Union[None, Unset, float]):
        f1 (Union[None, Unset, float]):
        filter_params (Union[Unset, FilterParams]):
        map_threshold (Union[Unset, float]):  Default: 0.5.
        meta_cols (Union[None, Unset, list[str]]):
        multi_label_task_metrics (Union[Unset, MultiLabelTaskMetrics]): Metrics per task for multi-label models.
        precision (Union[None, Unset, float]):
        recall (Union[None, Unset, float]):
        task (Union[None, Unset, str]):
    """

    accuracy: Union[None, Unset, float] = UNSET
    compare_to: Union[None, Split, Unset] = UNSET
    confidence: Union[None, Unset, float] = UNSET
    data_error_potential: Union[None, Unset, float] = UNSET
    f1: Union[None, Unset, float] = UNSET
    filter_params: Union[Unset, "FilterParams"] = UNSET
    map_threshold: Union[Unset, float] = 0.5
    meta_cols: Union[None, Unset, list[str]] = UNSET
    multi_label_task_metrics: Union[Unset, "MultiLabelTaskMetrics"] = UNSET
    precision: Union[None, Unset, float] = UNSET
    recall: Union[None, Unset, float] = UNSET
    task: Union[None, Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        accuracy: Union[None, Unset, float]
        if isinstance(self.accuracy, Unset):
            accuracy = UNSET
        else:
            accuracy = self.accuracy

        compare_to: Union[None, Unset, str]
        if isinstance(self.compare_to, Unset):
            compare_to = UNSET
        elif isinstance(self.compare_to, Split):
            compare_to = self.compare_to.value
        else:
            compare_to = self.compare_to

        confidence: Union[None, Unset, float]
        if isinstance(self.confidence, Unset):
            confidence = UNSET
        else:
            confidence = self.confidence

        data_error_potential: Union[None, Unset, float]
        if isinstance(self.data_error_potential, Unset):
            data_error_potential = UNSET
        else:
            data_error_potential = self.data_error_potential

        f1: Union[None, Unset, float]
        if isinstance(self.f1, Unset):
            f1 = UNSET
        else:
            f1 = self.f1

        filter_params: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.filter_params, Unset):
            filter_params = self.filter_params.to_dict()

        map_threshold = self.map_threshold

        meta_cols: Union[None, Unset, list[str]]
        if isinstance(self.meta_cols, Unset):
            meta_cols = UNSET
        elif isinstance(self.meta_cols, list):
            meta_cols = self.meta_cols

        else:
            meta_cols = self.meta_cols

        multi_label_task_metrics: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.multi_label_task_metrics, Unset):
            multi_label_task_metrics = self.multi_label_task_metrics.to_dict()

        precision: Union[None, Unset, float]
        if isinstance(self.precision, Unset):
            precision = UNSET
        else:
            precision = self.precision

        recall: Union[None, Unset, float]
        if isinstance(self.recall, Unset):
            recall = UNSET
        else:
            recall = self.recall

        task: Union[None, Unset, str]
        if isinstance(self.task, Unset):
            task = UNSET
        else:
            task = self.task

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if accuracy is not UNSET:
            field_dict["accuracy"] = accuracy
        if compare_to is not UNSET:
            field_dict["compare_to"] = compare_to
        if confidence is not UNSET:
            field_dict["confidence"] = confidence
        if data_error_potential is not UNSET:
            field_dict["data_error_potential"] = data_error_potential
        if f1 is not UNSET:
            field_dict["f1"] = f1
        if filter_params is not UNSET:
            field_dict["filter_params"] = filter_params
        if map_threshold is not UNSET:
            field_dict["map_threshold"] = map_threshold
        if meta_cols is not UNSET:
            field_dict["meta_cols"] = meta_cols
        if multi_label_task_metrics is not UNSET:
            field_dict["multi_label_task_metrics"] = multi_label_task_metrics
        if precision is not UNSET:
            field_dict["precision"] = precision
        if recall is not UNSET:
            field_dict["recall"] = recall
        if task is not UNSET:
            field_dict["task"] = task

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.filter_params import FilterParams
        from ..models.multi_label_task_metrics import MultiLabelTaskMetrics

        d = src_dict.copy()

        def _parse_accuracy(data: object) -> Union[None, Unset, float]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, float], data)

        accuracy = _parse_accuracy(d.pop("accuracy", UNSET))

        def _parse_compare_to(data: object) -> Union[None, Split, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                compare_to_type_0 = Split(data)

                return compare_to_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Split, Unset], data)

        compare_to = _parse_compare_to(d.pop("compare_to", UNSET))

        def _parse_confidence(data: object) -> Union[None, Unset, float]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, float], data)

        confidence = _parse_confidence(d.pop("confidence", UNSET))

        def _parse_data_error_potential(data: object) -> Union[None, Unset, float]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, float], data)

        data_error_potential = _parse_data_error_potential(d.pop("data_error_potential", UNSET))

        def _parse_f1(data: object) -> Union[None, Unset, float]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, float], data)

        f1 = _parse_f1(d.pop("f1", UNSET))

        _filter_params = d.pop("filter_params", UNSET)
        filter_params: Union[Unset, FilterParams]
        if isinstance(_filter_params, Unset):
            filter_params = UNSET
        else:
            filter_params = FilterParams.from_dict(_filter_params)

        map_threshold = d.pop("map_threshold", UNSET)

        def _parse_meta_cols(data: object) -> Union[None, Unset, list[str]]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                meta_cols_type_0 = cast(list[str], data)

                return meta_cols_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, list[str]], data)

        meta_cols = _parse_meta_cols(d.pop("meta_cols", UNSET))

        _multi_label_task_metrics = d.pop("multi_label_task_metrics", UNSET)
        multi_label_task_metrics: Union[Unset, MultiLabelTaskMetrics]
        if isinstance(_multi_label_task_metrics, Unset):
            multi_label_task_metrics = UNSET
        else:
            multi_label_task_metrics = MultiLabelTaskMetrics.from_dict(_multi_label_task_metrics)

        def _parse_precision(data: object) -> Union[None, Unset, float]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, float], data)

        precision = _parse_precision(d.pop("precision", UNSET))

        def _parse_recall(data: object) -> Union[None, Unset, float]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, float], data)

        recall = _parse_recall(d.pop("recall", UNSET))

        def _parse_task(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        task = _parse_task(d.pop("task", UNSET))

        metrics_response = cls(
            accuracy=accuracy,
            compare_to=compare_to,
            confidence=confidence,
            data_error_potential=data_error_potential,
            f1=f1,
            filter_params=filter_params,
            map_threshold=map_threshold,
            meta_cols=meta_cols,
            multi_label_task_metrics=multi_label_task_metrics,
            precision=precision,
            recall=recall,
            task=task,
        )

        metrics_response.additional_properties = d
        return metrics_response

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
