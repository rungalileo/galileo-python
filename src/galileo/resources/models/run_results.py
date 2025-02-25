from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.data_row import DataRow
    from ..models.run_results_top_erroneous_words_type_0 import RunResultsTopErroneousWordsType0


T = TypeVar("T", bound="RunResults")


@_attrs_define
class RunResults:
    """
    Attributes:
        has_next_page (bool):
        labels (list[str]):
        sample_count (int):
        sample_easy_percentage (float):
        sample_hard_percentage (float):
        sample_misclassified_percentage (float):
        split_total_sample_count (int):
        data_metrics (Union[Unset, list['DataRow']]):
        easy_samples_threshold (Union[None, Unset, float]):
        hard_samples_threshold (Union[None, Unset, float]):
        span_count (Union[None, Unset, int]):
        split_total_span_count (Union[None, Unset, int]):
        top_erroneous_words (Union['RunResultsTopErroneousWordsType0', None, Unset]):
    """

    has_next_page: bool
    labels: list[str]
    sample_count: int
    sample_easy_percentage: float
    sample_hard_percentage: float
    sample_misclassified_percentage: float
    split_total_sample_count: int
    data_metrics: Union[Unset, list["DataRow"]] = UNSET
    easy_samples_threshold: Union[None, Unset, float] = UNSET
    hard_samples_threshold: Union[None, Unset, float] = UNSET
    span_count: Union[None, Unset, int] = UNSET
    split_total_span_count: Union[None, Unset, int] = UNSET
    top_erroneous_words: Union["RunResultsTopErroneousWordsType0", None, Unset] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.run_results_top_erroneous_words_type_0 import RunResultsTopErroneousWordsType0

        has_next_page = self.has_next_page

        labels = self.labels

        sample_count = self.sample_count

        sample_easy_percentage = self.sample_easy_percentage

        sample_hard_percentage = self.sample_hard_percentage

        sample_misclassified_percentage = self.sample_misclassified_percentage

        split_total_sample_count = self.split_total_sample_count

        data_metrics: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.data_metrics, Unset):
            data_metrics = []
            for data_metrics_item_data in self.data_metrics:
                data_metrics_item = data_metrics_item_data.to_dict()
                data_metrics.append(data_metrics_item)

        easy_samples_threshold: Union[None, Unset, float]
        if isinstance(self.easy_samples_threshold, Unset):
            easy_samples_threshold = UNSET
        else:
            easy_samples_threshold = self.easy_samples_threshold

        hard_samples_threshold: Union[None, Unset, float]
        if isinstance(self.hard_samples_threshold, Unset):
            hard_samples_threshold = UNSET
        else:
            hard_samples_threshold = self.hard_samples_threshold

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

        top_erroneous_words: Union[None, Unset, dict[str, Any]]
        if isinstance(self.top_erroneous_words, Unset):
            top_erroneous_words = UNSET
        elif isinstance(self.top_erroneous_words, RunResultsTopErroneousWordsType0):
            top_erroneous_words = self.top_erroneous_words.to_dict()
        else:
            top_erroneous_words = self.top_erroneous_words

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "has_next_page": has_next_page,
                "labels": labels,
                "sample_count": sample_count,
                "sample_easy_percentage": sample_easy_percentage,
                "sample_hard_percentage": sample_hard_percentage,
                "sample_misclassified_percentage": sample_misclassified_percentage,
                "split_total_sample_count": split_total_sample_count,
            }
        )
        if data_metrics is not UNSET:
            field_dict["data_metrics"] = data_metrics
        if easy_samples_threshold is not UNSET:
            field_dict["easy_samples_threshold"] = easy_samples_threshold
        if hard_samples_threshold is not UNSET:
            field_dict["hard_samples_threshold"] = hard_samples_threshold
        if span_count is not UNSET:
            field_dict["span_count"] = span_count
        if split_total_span_count is not UNSET:
            field_dict["split_total_span_count"] = split_total_span_count
        if top_erroneous_words is not UNSET:
            field_dict["top_erroneous_words"] = top_erroneous_words

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.data_row import DataRow
        from ..models.run_results_top_erroneous_words_type_0 import RunResultsTopErroneousWordsType0

        d = src_dict.copy()
        has_next_page = d.pop("has_next_page")

        labels = cast(list[str], d.pop("labels"))

        sample_count = d.pop("sample_count")

        sample_easy_percentage = d.pop("sample_easy_percentage")

        sample_hard_percentage = d.pop("sample_hard_percentage")

        sample_misclassified_percentage = d.pop("sample_misclassified_percentage")

        split_total_sample_count = d.pop("split_total_sample_count")

        data_metrics = []
        _data_metrics = d.pop("data_metrics", UNSET)
        for data_metrics_item_data in _data_metrics or []:
            data_metrics_item = DataRow.from_dict(data_metrics_item_data)

            data_metrics.append(data_metrics_item)

        def _parse_easy_samples_threshold(data: object) -> Union[None, Unset, float]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, float], data)

        easy_samples_threshold = _parse_easy_samples_threshold(d.pop("easy_samples_threshold", UNSET))

        def _parse_hard_samples_threshold(data: object) -> Union[None, Unset, float]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, float], data)

        hard_samples_threshold = _parse_hard_samples_threshold(d.pop("hard_samples_threshold", UNSET))

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

        def _parse_top_erroneous_words(data: object) -> Union["RunResultsTopErroneousWordsType0", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                top_erroneous_words_type_0 = RunResultsTopErroneousWordsType0.from_dict(data)

                return top_erroneous_words_type_0
            except:  # noqa: E722
                pass
            return cast(Union["RunResultsTopErroneousWordsType0", None, Unset], data)

        top_erroneous_words = _parse_top_erroneous_words(d.pop("top_erroneous_words", UNSET))

        run_results = cls(
            has_next_page=has_next_page,
            labels=labels,
            sample_count=sample_count,
            sample_easy_percentage=sample_easy_percentage,
            sample_hard_percentage=sample_hard_percentage,
            sample_misclassified_percentage=sample_misclassified_percentage,
            split_total_sample_count=split_total_sample_count,
            data_metrics=data_metrics,
            easy_samples_threshold=easy_samples_threshold,
            hard_samples_threshold=hard_samples_threshold,
            span_count=span_count,
            split_total_span_count=split_total_span_count,
            top_erroneous_words=top_erroneous_words,
        )

        run_results.additional_properties = d
        return run_results

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
