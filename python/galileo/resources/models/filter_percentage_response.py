from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.split import Split
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.filter_params import FilterParams


T = TypeVar("T", bound="FilterPercentageResponse")


@_attrs_define
class FilterPercentageResponse:
    """
    Attributes:
        percentage (float):
        sample_count (int):
        compare_to (Union[None, Split, Unset]):
        feature_noise_pct (Union[None, Unset, float]):
        filter_params (Union[Unset, FilterParams]):
        gold_box_count (Union[None, Unset, int]):
        gold_box_percentage (Union[None, Unset, float]):
        gold_polygon_count (Union[None, Unset, int]):
        gold_polygon_percentage (Union[None, Unset, float]):
        label_noise_pct (Union[None, Unset, float]):
        map_threshold (Union[Unset, float]):  Default: 0.5.
        meta_cols (Union[None, Unset, list[str]]):
        pred_box_count (Union[None, Unset, int]):
        pred_box_percentage (Union[None, Unset, float]):
        pred_polygon_count (Union[None, Unset, int]):
        pred_polygon_percentage (Union[None, Unset, float]):
        sample_drifted_percentage (Union[None, Unset, float]):
        sample_easy_percentage (Union[None, Unset, float]):
        sample_error_percentage (Union[None, Unset, float]):
        sample_hard_percentage (Union[None, Unset, float]):
        sample_misclassified_percentage (Union[None, Unset, float]):
        sample_mislabeled_percentage (Union[None, Unset, float]):
        sample_otb_percentage (Union[None, Unset, float]):
        span_count (Union[None, Unset, int]):
        span_percentage (Union[None, Unset, float]):
        task (Union[None, Unset, str]):
    """

    percentage: float
    sample_count: int
    compare_to: Union[None, Split, Unset] = UNSET
    feature_noise_pct: Union[None, Unset, float] = UNSET
    filter_params: Union[Unset, "FilterParams"] = UNSET
    gold_box_count: Union[None, Unset, int] = UNSET
    gold_box_percentage: Union[None, Unset, float] = UNSET
    gold_polygon_count: Union[None, Unset, int] = UNSET
    gold_polygon_percentage: Union[None, Unset, float] = UNSET
    label_noise_pct: Union[None, Unset, float] = UNSET
    map_threshold: Union[Unset, float] = 0.5
    meta_cols: Union[None, Unset, list[str]] = UNSET
    pred_box_count: Union[None, Unset, int] = UNSET
    pred_box_percentage: Union[None, Unset, float] = UNSET
    pred_polygon_count: Union[None, Unset, int] = UNSET
    pred_polygon_percentage: Union[None, Unset, float] = UNSET
    sample_drifted_percentage: Union[None, Unset, float] = UNSET
    sample_easy_percentage: Union[None, Unset, float] = UNSET
    sample_error_percentage: Union[None, Unset, float] = UNSET
    sample_hard_percentage: Union[None, Unset, float] = UNSET
    sample_misclassified_percentage: Union[None, Unset, float] = UNSET
    sample_mislabeled_percentage: Union[None, Unset, float] = UNSET
    sample_otb_percentage: Union[None, Unset, float] = UNSET
    span_count: Union[None, Unset, int] = UNSET
    span_percentage: Union[None, Unset, float] = UNSET
    task: Union[None, Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        percentage = self.percentage

        sample_count = self.sample_count

        compare_to: Union[None, Unset, str]
        if isinstance(self.compare_to, Unset):
            compare_to = UNSET
        elif isinstance(self.compare_to, Split):
            compare_to = self.compare_to.value
        else:
            compare_to = self.compare_to

        feature_noise_pct: Union[None, Unset, float]
        if isinstance(self.feature_noise_pct, Unset):
            feature_noise_pct = UNSET
        else:
            feature_noise_pct = self.feature_noise_pct

        filter_params: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.filter_params, Unset):
            filter_params = self.filter_params.to_dict()

        gold_box_count: Union[None, Unset, int]
        if isinstance(self.gold_box_count, Unset):
            gold_box_count = UNSET
        else:
            gold_box_count = self.gold_box_count

        gold_box_percentage: Union[None, Unset, float]
        if isinstance(self.gold_box_percentage, Unset):
            gold_box_percentage = UNSET
        else:
            gold_box_percentage = self.gold_box_percentage

        gold_polygon_count: Union[None, Unset, int]
        if isinstance(self.gold_polygon_count, Unset):
            gold_polygon_count = UNSET
        else:
            gold_polygon_count = self.gold_polygon_count

        gold_polygon_percentage: Union[None, Unset, float]
        if isinstance(self.gold_polygon_percentage, Unset):
            gold_polygon_percentage = UNSET
        else:
            gold_polygon_percentage = self.gold_polygon_percentage

        label_noise_pct: Union[None, Unset, float]
        if isinstance(self.label_noise_pct, Unset):
            label_noise_pct = UNSET
        else:
            label_noise_pct = self.label_noise_pct

        map_threshold = self.map_threshold

        meta_cols: Union[None, Unset, list[str]]
        if isinstance(self.meta_cols, Unset):
            meta_cols = UNSET
        elif isinstance(self.meta_cols, list):
            meta_cols = self.meta_cols

        else:
            meta_cols = self.meta_cols

        pred_box_count: Union[None, Unset, int]
        if isinstance(self.pred_box_count, Unset):
            pred_box_count = UNSET
        else:
            pred_box_count = self.pred_box_count

        pred_box_percentage: Union[None, Unset, float]
        if isinstance(self.pred_box_percentage, Unset):
            pred_box_percentage = UNSET
        else:
            pred_box_percentage = self.pred_box_percentage

        pred_polygon_count: Union[None, Unset, int]
        if isinstance(self.pred_polygon_count, Unset):
            pred_polygon_count = UNSET
        else:
            pred_polygon_count = self.pred_polygon_count

        pred_polygon_percentage: Union[None, Unset, float]
        if isinstance(self.pred_polygon_percentage, Unset):
            pred_polygon_percentage = UNSET
        else:
            pred_polygon_percentage = self.pred_polygon_percentage

        sample_drifted_percentage: Union[None, Unset, float]
        if isinstance(self.sample_drifted_percentage, Unset):
            sample_drifted_percentage = UNSET
        else:
            sample_drifted_percentage = self.sample_drifted_percentage

        sample_easy_percentage: Union[None, Unset, float]
        if isinstance(self.sample_easy_percentage, Unset):
            sample_easy_percentage = UNSET
        else:
            sample_easy_percentage = self.sample_easy_percentage

        sample_error_percentage: Union[None, Unset, float]
        if isinstance(self.sample_error_percentage, Unset):
            sample_error_percentage = UNSET
        else:
            sample_error_percentage = self.sample_error_percentage

        sample_hard_percentage: Union[None, Unset, float]
        if isinstance(self.sample_hard_percentage, Unset):
            sample_hard_percentage = UNSET
        else:
            sample_hard_percentage = self.sample_hard_percentage

        sample_misclassified_percentage: Union[None, Unset, float]
        if isinstance(self.sample_misclassified_percentage, Unset):
            sample_misclassified_percentage = UNSET
        else:
            sample_misclassified_percentage = self.sample_misclassified_percentage

        sample_mislabeled_percentage: Union[None, Unset, float]
        if isinstance(self.sample_mislabeled_percentage, Unset):
            sample_mislabeled_percentage = UNSET
        else:
            sample_mislabeled_percentage = self.sample_mislabeled_percentage

        sample_otb_percentage: Union[None, Unset, float]
        if isinstance(self.sample_otb_percentage, Unset):
            sample_otb_percentage = UNSET
        else:
            sample_otb_percentage = self.sample_otb_percentage

        span_count: Union[None, Unset, int]
        if isinstance(self.span_count, Unset):
            span_count = UNSET
        else:
            span_count = self.span_count

        span_percentage: Union[None, Unset, float]
        if isinstance(self.span_percentage, Unset):
            span_percentage = UNSET
        else:
            span_percentage = self.span_percentage

        task: Union[None, Unset, str]
        if isinstance(self.task, Unset):
            task = UNSET
        else:
            task = self.task

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({"percentage": percentage, "sample_count": sample_count})
        if compare_to is not UNSET:
            field_dict["compare_to"] = compare_to
        if feature_noise_pct is not UNSET:
            field_dict["feature_noise_pct"] = feature_noise_pct
        if filter_params is not UNSET:
            field_dict["filter_params"] = filter_params
        if gold_box_count is not UNSET:
            field_dict["gold_box_count"] = gold_box_count
        if gold_box_percentage is not UNSET:
            field_dict["gold_box_percentage"] = gold_box_percentage
        if gold_polygon_count is not UNSET:
            field_dict["gold_polygon_count"] = gold_polygon_count
        if gold_polygon_percentage is not UNSET:
            field_dict["gold_polygon_percentage"] = gold_polygon_percentage
        if label_noise_pct is not UNSET:
            field_dict["label_noise_pct"] = label_noise_pct
        if map_threshold is not UNSET:
            field_dict["map_threshold"] = map_threshold
        if meta_cols is not UNSET:
            field_dict["meta_cols"] = meta_cols
        if pred_box_count is not UNSET:
            field_dict["pred_box_count"] = pred_box_count
        if pred_box_percentage is not UNSET:
            field_dict["pred_box_percentage"] = pred_box_percentage
        if pred_polygon_count is not UNSET:
            field_dict["pred_polygon_count"] = pred_polygon_count
        if pred_polygon_percentage is not UNSET:
            field_dict["pred_polygon_percentage"] = pred_polygon_percentage
        if sample_drifted_percentage is not UNSET:
            field_dict["sample_drifted_percentage"] = sample_drifted_percentage
        if sample_easy_percentage is not UNSET:
            field_dict["sample_easy_percentage"] = sample_easy_percentage
        if sample_error_percentage is not UNSET:
            field_dict["sample_error_percentage"] = sample_error_percentage
        if sample_hard_percentage is not UNSET:
            field_dict["sample_hard_percentage"] = sample_hard_percentage
        if sample_misclassified_percentage is not UNSET:
            field_dict["sample_misclassified_percentage"] = sample_misclassified_percentage
        if sample_mislabeled_percentage is not UNSET:
            field_dict["sample_mislabeled_percentage"] = sample_mislabeled_percentage
        if sample_otb_percentage is not UNSET:
            field_dict["sample_otb_percentage"] = sample_otb_percentage
        if span_count is not UNSET:
            field_dict["span_count"] = span_count
        if span_percentage is not UNSET:
            field_dict["span_percentage"] = span_percentage
        if task is not UNSET:
            field_dict["task"] = task

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.filter_params import FilterParams

        d = src_dict.copy()
        percentage = d.pop("percentage")

        sample_count = d.pop("sample_count")

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

        def _parse_feature_noise_pct(data: object) -> Union[None, Unset, float]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, float], data)

        feature_noise_pct = _parse_feature_noise_pct(d.pop("feature_noise_pct", UNSET))

        _filter_params = d.pop("filter_params", UNSET)
        filter_params: Union[Unset, FilterParams]
        if isinstance(_filter_params, Unset):
            filter_params = UNSET
        else:
            filter_params = FilterParams.from_dict(_filter_params)

        def _parse_gold_box_count(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        gold_box_count = _parse_gold_box_count(d.pop("gold_box_count", UNSET))

        def _parse_gold_box_percentage(data: object) -> Union[None, Unset, float]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, float], data)

        gold_box_percentage = _parse_gold_box_percentage(d.pop("gold_box_percentage", UNSET))

        def _parse_gold_polygon_count(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        gold_polygon_count = _parse_gold_polygon_count(d.pop("gold_polygon_count", UNSET))

        def _parse_gold_polygon_percentage(data: object) -> Union[None, Unset, float]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, float], data)

        gold_polygon_percentage = _parse_gold_polygon_percentage(d.pop("gold_polygon_percentage", UNSET))

        def _parse_label_noise_pct(data: object) -> Union[None, Unset, float]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, float], data)

        label_noise_pct = _parse_label_noise_pct(d.pop("label_noise_pct", UNSET))

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

        def _parse_pred_box_count(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        pred_box_count = _parse_pred_box_count(d.pop("pred_box_count", UNSET))

        def _parse_pred_box_percentage(data: object) -> Union[None, Unset, float]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, float], data)

        pred_box_percentage = _parse_pred_box_percentage(d.pop("pred_box_percentage", UNSET))

        def _parse_pred_polygon_count(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        pred_polygon_count = _parse_pred_polygon_count(d.pop("pred_polygon_count", UNSET))

        def _parse_pred_polygon_percentage(data: object) -> Union[None, Unset, float]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, float], data)

        pred_polygon_percentage = _parse_pred_polygon_percentage(d.pop("pred_polygon_percentage", UNSET))

        def _parse_sample_drifted_percentage(data: object) -> Union[None, Unset, float]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, float], data)

        sample_drifted_percentage = _parse_sample_drifted_percentage(d.pop("sample_drifted_percentage", UNSET))

        def _parse_sample_easy_percentage(data: object) -> Union[None, Unset, float]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, float], data)

        sample_easy_percentage = _parse_sample_easy_percentage(d.pop("sample_easy_percentage", UNSET))

        def _parse_sample_error_percentage(data: object) -> Union[None, Unset, float]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, float], data)

        sample_error_percentage = _parse_sample_error_percentage(d.pop("sample_error_percentage", UNSET))

        def _parse_sample_hard_percentage(data: object) -> Union[None, Unset, float]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, float], data)

        sample_hard_percentage = _parse_sample_hard_percentage(d.pop("sample_hard_percentage", UNSET))

        def _parse_sample_misclassified_percentage(data: object) -> Union[None, Unset, float]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, float], data)

        sample_misclassified_percentage = _parse_sample_misclassified_percentage(
            d.pop("sample_misclassified_percentage", UNSET)
        )

        def _parse_sample_mislabeled_percentage(data: object) -> Union[None, Unset, float]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, float], data)

        sample_mislabeled_percentage = _parse_sample_mislabeled_percentage(d.pop("sample_mislabeled_percentage", UNSET))

        def _parse_sample_otb_percentage(data: object) -> Union[None, Unset, float]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, float], data)

        sample_otb_percentage = _parse_sample_otb_percentage(d.pop("sample_otb_percentage", UNSET))

        def _parse_span_count(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        span_count = _parse_span_count(d.pop("span_count", UNSET))

        def _parse_span_percentage(data: object) -> Union[None, Unset, float]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, float], data)

        span_percentage = _parse_span_percentage(d.pop("span_percentage", UNSET))

        def _parse_task(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        task = _parse_task(d.pop("task", UNSET))

        filter_percentage_response = cls(
            percentage=percentage,
            sample_count=sample_count,
            compare_to=compare_to,
            feature_noise_pct=feature_noise_pct,
            filter_params=filter_params,
            gold_box_count=gold_box_count,
            gold_box_percentage=gold_box_percentage,
            gold_polygon_count=gold_polygon_count,
            gold_polygon_percentage=gold_polygon_percentage,
            label_noise_pct=label_noise_pct,
            map_threshold=map_threshold,
            meta_cols=meta_cols,
            pred_box_count=pred_box_count,
            pred_box_percentage=pred_box_percentage,
            pred_polygon_count=pred_polygon_count,
            pred_polygon_percentage=pred_polygon_percentage,
            sample_drifted_percentage=sample_drifted_percentage,
            sample_easy_percentage=sample_easy_percentage,
            sample_error_percentage=sample_error_percentage,
            sample_hard_percentage=sample_hard_percentage,
            sample_misclassified_percentage=sample_misclassified_percentage,
            sample_mislabeled_percentage=sample_mislabeled_percentage,
            sample_otb_percentage=sample_otb_percentage,
            span_count=span_count,
            span_percentage=span_percentage,
            task=task,
        )

        filter_percentage_response.additional_properties = d
        return filter_percentage_response

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
