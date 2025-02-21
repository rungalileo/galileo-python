from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.split import Split
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.filter_params import FilterParams
    from ..models.top_insights_response_top_correlation_pairs import TopInsightsResponseTopCorrelationPairs
    from ..models.top_insights_response_top_erroneous_words import TopInsightsResponseTopErroneousWords
    from ..models.top_insights_response_top_misclassified_pairs_item import TopInsightsResponseTopMisclassifiedPairsItem


T = TypeVar("T", bound="TopInsightsResponse")


@_attrs_define
class TopInsightsResponse:
    """
    Attributes:
        top_misclassified_pairs_percentage (float):
        compare_to (Union[None, Split, Unset]):
        filter_params (Union[Unset, FilterParams]):
        map_threshold (Union[Unset, float]):  Default: 0.5.
        meta_cols (Union[None, Unset, list[str]]):
        task (Union[None, Unset, str]):
        top_correlation_pairs (Union[Unset, TopInsightsResponseTopCorrelationPairs]):
        top_erroneous_words (Union[Unset, TopInsightsResponseTopErroneousWords]):
        top_misclassified_pairs (Union[Unset, list['TopInsightsResponseTopMisclassifiedPairsItem']]):
    """

    top_misclassified_pairs_percentage: float
    compare_to: Union[None, Split, Unset] = UNSET
    filter_params: Union[Unset, "FilterParams"] = UNSET
    map_threshold: Union[Unset, float] = 0.5
    meta_cols: Union[None, Unset, list[str]] = UNSET
    task: Union[None, Unset, str] = UNSET
    top_correlation_pairs: Union[Unset, "TopInsightsResponseTopCorrelationPairs"] = UNSET
    top_erroneous_words: Union[Unset, "TopInsightsResponseTopErroneousWords"] = UNSET
    top_misclassified_pairs: Union[Unset, list["TopInsightsResponseTopMisclassifiedPairsItem"]] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        top_misclassified_pairs_percentage = self.top_misclassified_pairs_percentage

        compare_to: Union[None, Unset, str]
        if isinstance(self.compare_to, Unset):
            compare_to = UNSET
        elif isinstance(self.compare_to, Split):
            compare_to = self.compare_to.value
        else:
            compare_to = self.compare_to

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

        task: Union[None, Unset, str]
        if isinstance(self.task, Unset):
            task = UNSET
        else:
            task = self.task

        top_correlation_pairs: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.top_correlation_pairs, Unset):
            top_correlation_pairs = self.top_correlation_pairs.to_dict()

        top_erroneous_words: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.top_erroneous_words, Unset):
            top_erroneous_words = self.top_erroneous_words.to_dict()

        top_misclassified_pairs: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.top_misclassified_pairs, Unset):
            top_misclassified_pairs = []
            for top_misclassified_pairs_item_data in self.top_misclassified_pairs:
                top_misclassified_pairs_item = top_misclassified_pairs_item_data.to_dict()
                top_misclassified_pairs.append(top_misclassified_pairs_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({"top_misclassified_pairs_percentage": top_misclassified_pairs_percentage})
        if compare_to is not UNSET:
            field_dict["compare_to"] = compare_to
        if filter_params is not UNSET:
            field_dict["filter_params"] = filter_params
        if map_threshold is not UNSET:
            field_dict["map_threshold"] = map_threshold
        if meta_cols is not UNSET:
            field_dict["meta_cols"] = meta_cols
        if task is not UNSET:
            field_dict["task"] = task
        if top_correlation_pairs is not UNSET:
            field_dict["top_correlation_pairs"] = top_correlation_pairs
        if top_erroneous_words is not UNSET:
            field_dict["top_erroneous_words"] = top_erroneous_words
        if top_misclassified_pairs is not UNSET:
            field_dict["top_misclassified_pairs"] = top_misclassified_pairs

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.filter_params import FilterParams
        from ..models.top_insights_response_top_correlation_pairs import TopInsightsResponseTopCorrelationPairs
        from ..models.top_insights_response_top_erroneous_words import TopInsightsResponseTopErroneousWords
        from ..models.top_insights_response_top_misclassified_pairs_item import (
            TopInsightsResponseTopMisclassifiedPairsItem,
        )

        d = src_dict.copy()
        top_misclassified_pairs_percentage = d.pop("top_misclassified_pairs_percentage")

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

        def _parse_task(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        task = _parse_task(d.pop("task", UNSET))

        _top_correlation_pairs = d.pop("top_correlation_pairs", UNSET)
        top_correlation_pairs: Union[Unset, TopInsightsResponseTopCorrelationPairs]
        if isinstance(_top_correlation_pairs, Unset):
            top_correlation_pairs = UNSET
        else:
            top_correlation_pairs = TopInsightsResponseTopCorrelationPairs.from_dict(_top_correlation_pairs)

        _top_erroneous_words = d.pop("top_erroneous_words", UNSET)
        top_erroneous_words: Union[Unset, TopInsightsResponseTopErroneousWords]
        if isinstance(_top_erroneous_words, Unset):
            top_erroneous_words = UNSET
        else:
            top_erroneous_words = TopInsightsResponseTopErroneousWords.from_dict(_top_erroneous_words)

        top_misclassified_pairs = []
        _top_misclassified_pairs = d.pop("top_misclassified_pairs", UNSET)
        for top_misclassified_pairs_item_data in _top_misclassified_pairs or []:
            top_misclassified_pairs_item = TopInsightsResponseTopMisclassifiedPairsItem.from_dict(
                top_misclassified_pairs_item_data
            )

            top_misclassified_pairs.append(top_misclassified_pairs_item)

        top_insights_response = cls(
            top_misclassified_pairs_percentage=top_misclassified_pairs_percentage,
            compare_to=compare_to,
            filter_params=filter_params,
            map_threshold=map_threshold,
            meta_cols=meta_cols,
            task=task,
            top_correlation_pairs=top_correlation_pairs,
            top_erroneous_words=top_erroneous_words,
            top_misclassified_pairs=top_misclassified_pairs,
        )

        top_insights_response.additional_properties = d
        return top_insights_response

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
