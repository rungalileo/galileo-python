from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.data_row import DataRow
    from ..models.inference_model_metrics import InferenceModelMetrics


T = TypeVar("T", bound="InferenceResults")


@_attrs_define
class InferenceResults:
    """
    Attributes:
        has_next_page (bool):
        labels (list[str]):
        model_metrics (InferenceModelMetrics):
        sample_count (int):
        split_total_sample_count (int):
        data_metrics (Union[Unset, list['DataRow']]):
        span_count (Union[None, Unset, int]):
        split_total_span_count (Union[None, Unset, int]):
    """

    has_next_page: bool
    labels: list[str]
    model_metrics: "InferenceModelMetrics"
    sample_count: int
    split_total_sample_count: int
    data_metrics: Union[Unset, list["DataRow"]] = UNSET
    span_count: Union[None, Unset, int] = UNSET
    split_total_span_count: Union[None, Unset, int] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        has_next_page = self.has_next_page

        labels = self.labels

        model_metrics = self.model_metrics.to_dict()

        sample_count = self.sample_count

        split_total_sample_count = self.split_total_sample_count

        data_metrics: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.data_metrics, Unset):
            data_metrics = []
            for data_metrics_item_data in self.data_metrics:
                data_metrics_item = data_metrics_item_data.to_dict()
                data_metrics.append(data_metrics_item)

        span_count: Union[None, Unset, int]
        if isinstance(self.span_count, Unset):
            span_count = UNSET
        else:
            span_count = self.span_count

        split_total_span_count: Union[None, Unset, int]
        if isinstance(self.split_total_span_count, Unset):
            split_total_span_count = UNSET
        else:
            split_total_span_count = self.split_total_span_count

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "has_next_page": has_next_page,
                "labels": labels,
                "model_metrics": model_metrics,
                "sample_count": sample_count,
                "split_total_sample_count": split_total_sample_count,
            }
        )
        if data_metrics is not UNSET:
            field_dict["data_metrics"] = data_metrics
        if span_count is not UNSET:
            field_dict["span_count"] = span_count
        if split_total_span_count is not UNSET:
            field_dict["split_total_span_count"] = split_total_span_count

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.data_row import DataRow
        from ..models.inference_model_metrics import InferenceModelMetrics

        d = src_dict.copy()
        has_next_page = d.pop("has_next_page")

        labels = cast(list[str], d.pop("labels"))

        model_metrics = InferenceModelMetrics.from_dict(d.pop("model_metrics"))

        sample_count = d.pop("sample_count")

        split_total_sample_count = d.pop("split_total_sample_count")

        data_metrics = []
        _data_metrics = d.pop("data_metrics", UNSET)
        for data_metrics_item_data in _data_metrics or []:
            data_metrics_item = DataRow.from_dict(data_metrics_item_data)

            data_metrics.append(data_metrics_item)

        def _parse_span_count(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        span_count = _parse_span_count(d.pop("span_count", UNSET))

        def _parse_split_total_span_count(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        split_total_span_count = _parse_split_total_span_count(d.pop("split_total_span_count", UNSET))

        inference_results = cls(
            has_next_page=has_next_page,
            labels=labels,
            model_metrics=model_metrics,
            sample_count=sample_count,
            split_total_sample_count=split_total_sample_count,
            data_metrics=data_metrics,
            span_count=span_count,
            split_total_span_count=split_total_span_count,
        )

        inference_results.additional_properties = d
        return inference_results

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
