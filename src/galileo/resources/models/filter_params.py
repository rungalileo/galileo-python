from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.lasso_selection import LassoSelection
    from ..models.meta_filter import MetaFilter


T = TypeVar("T", bound="FilterParams")


@_attrs_define
class FilterParams:
    """
    Attributes
    ----------
        ids (Union[Unset, list[int]]):
        similar_to (Union[None, Unset, list[int]]):
        num_similar_to (Union[None, Unset, int]):
        text_pat (Union[None, Unset, str]):
        regex (Union[None, Unset, bool]):
        data_error_potential_high (Union[None, Unset, float]):
        data_error_potential_low (Union[None, Unset, float]):
        misclassified_only (Union[None, Unset, bool]):
        gold_filter (Union[None, Unset, list[str]]):
        pred_filter (Union[None, Unset, list[str]]):
        meta_filter (Union[None, Unset, list['MetaFilter']]):
        drift_score_threshold (Union[None, Unset, float]):
        is_drifted (Union[None, Unset, bool]):
        span_sample_ids (Union[None, Unset, list[int]]):
        span_text (Union[None, Unset, str]):
        span_regex (Union[None, Unset, bool]):  Default: False.
        exclude_ids (Union[Unset, list[int]]):
        lasso (Union['LassoSelection', None, Unset]):
        class_filter (Union[None, Unset, list[str]]):
        likely_mislabeled (Union[None, Unset, bool]):
        likely_mislabeled_dep_percentile (Union[None, Unset, int]):  Default: 0.
        cbo_clusters (Union[None, Unset, list[int]]):
        data_embs (Union[None, Unset, bool]):  Default: False.
        confidence_high (Union[None, Unset, float]):
        confidence_low (Union[None, Unset, float]):
        is_otb (Union[None, Unset, bool]):
        image_ids (Union[None, Unset, list[int]]):
        cluster_ids (Union[None, Unset, list[int]]):
        correctly_classified (Union[None, Unset, bool]):
        is_edited (Union[None, Unset, bool]):
    """

    ids: Union[Unset, list[int]] = UNSET
    similar_to: Union[None, Unset, list[int]] = UNSET
    num_similar_to: Union[None, Unset, int] = UNSET
    text_pat: Union[None, Unset, str] = UNSET
    regex: Union[None, Unset, bool] = UNSET
    data_error_potential_high: Union[None, Unset, float] = UNSET
    data_error_potential_low: Union[None, Unset, float] = UNSET
    misclassified_only: Union[None, Unset, bool] = UNSET
    gold_filter: Union[None, Unset, list[str]] = UNSET
    pred_filter: Union[None, Unset, list[str]] = UNSET
    meta_filter: Union[None, Unset, list["MetaFilter"]] = UNSET
    drift_score_threshold: Union[None, Unset, float] = UNSET
    is_drifted: Union[None, Unset, bool] = UNSET
    span_sample_ids: Union[None, Unset, list[int]] = UNSET
    span_text: Union[None, Unset, str] = UNSET
    span_regex: Union[None, Unset, bool] = False
    exclude_ids: Union[Unset, list[int]] = UNSET
    lasso: Union["LassoSelection", None, Unset] = UNSET
    class_filter: Union[None, Unset, list[str]] = UNSET
    likely_mislabeled: Union[None, Unset, bool] = UNSET
    likely_mislabeled_dep_percentile: Union[None, Unset, int] = 0
    cbo_clusters: Union[None, Unset, list[int]] = UNSET
    data_embs: Union[None, Unset, bool] = False
    confidence_high: Union[None, Unset, float] = UNSET
    confidence_low: Union[None, Unset, float] = UNSET
    is_otb: Union[None, Unset, bool] = UNSET
    image_ids: Union[None, Unset, list[int]] = UNSET
    cluster_ids: Union[None, Unset, list[int]] = UNSET
    correctly_classified: Union[None, Unset, bool] = UNSET
    is_edited: Union[None, Unset, bool] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.lasso_selection import LassoSelection

        ids: Union[Unset, list[int]] = UNSET
        if not isinstance(self.ids, Unset):
            ids = self.ids

        similar_to: Union[None, Unset, list[int]]
        if isinstance(self.similar_to, Unset):
            similar_to = UNSET
        elif isinstance(self.similar_to, list):
            similar_to = self.similar_to

        else:
            similar_to = self.similar_to

        num_similar_to: Union[None, Unset, int]
        num_similar_to = UNSET if isinstance(self.num_similar_to, Unset) else self.num_similar_to

        text_pat: Union[None, Unset, str]
        text_pat = UNSET if isinstance(self.text_pat, Unset) else self.text_pat

        regex: Union[None, Unset, bool]
        regex = UNSET if isinstance(self.regex, Unset) else self.regex

        data_error_potential_high: Union[None, Unset, float]
        if isinstance(self.data_error_potential_high, Unset):
            data_error_potential_high = UNSET
        else:
            data_error_potential_high = self.data_error_potential_high

        data_error_potential_low: Union[None, Unset, float]
        if isinstance(self.data_error_potential_low, Unset):
            data_error_potential_low = UNSET
        else:
            data_error_potential_low = self.data_error_potential_low

        misclassified_only: Union[None, Unset, bool]
        misclassified_only = UNSET if isinstance(self.misclassified_only, Unset) else self.misclassified_only

        gold_filter: Union[None, Unset, list[str]]
        if isinstance(self.gold_filter, Unset):
            gold_filter = UNSET
        elif isinstance(self.gold_filter, list):
            gold_filter = self.gold_filter

        else:
            gold_filter = self.gold_filter

        pred_filter: Union[None, Unset, list[str]]
        if isinstance(self.pred_filter, Unset):
            pred_filter = UNSET
        elif isinstance(self.pred_filter, list):
            pred_filter = self.pred_filter

        else:
            pred_filter = self.pred_filter

        meta_filter: Union[None, Unset, list[dict[str, Any]]]
        if isinstance(self.meta_filter, Unset):
            meta_filter = UNSET
        elif isinstance(self.meta_filter, list):
            meta_filter = []
            for meta_filter_type_0_item_data in self.meta_filter:
                meta_filter_type_0_item = meta_filter_type_0_item_data.to_dict()
                meta_filter.append(meta_filter_type_0_item)

        else:
            meta_filter = self.meta_filter

        drift_score_threshold: Union[None, Unset, float]
        drift_score_threshold = UNSET if isinstance(self.drift_score_threshold, Unset) else self.drift_score_threshold

        is_drifted: Union[None, Unset, bool]
        is_drifted = UNSET if isinstance(self.is_drifted, Unset) else self.is_drifted

        span_sample_ids: Union[None, Unset, list[int]]
        if isinstance(self.span_sample_ids, Unset):
            span_sample_ids = UNSET
        elif isinstance(self.span_sample_ids, list):
            span_sample_ids = self.span_sample_ids

        else:
            span_sample_ids = self.span_sample_ids

        span_text: Union[None, Unset, str]
        span_text = UNSET if isinstance(self.span_text, Unset) else self.span_text

        span_regex: Union[None, Unset, bool]
        span_regex = UNSET if isinstance(self.span_regex, Unset) else self.span_regex

        exclude_ids: Union[Unset, list[int]] = UNSET
        if not isinstance(self.exclude_ids, Unset):
            exclude_ids = self.exclude_ids

        lasso: Union[None, Unset, dict[str, Any]]
        if isinstance(self.lasso, Unset):
            lasso = UNSET
        elif isinstance(self.lasso, LassoSelection):
            lasso = self.lasso.to_dict()
        else:
            lasso = self.lasso

        class_filter: Union[None, Unset, list[str]]
        if isinstance(self.class_filter, Unset):
            class_filter = UNSET
        elif isinstance(self.class_filter, list):
            class_filter = self.class_filter

        else:
            class_filter = self.class_filter

        likely_mislabeled: Union[None, Unset, bool]
        likely_mislabeled = UNSET if isinstance(self.likely_mislabeled, Unset) else self.likely_mislabeled

        likely_mislabeled_dep_percentile: Union[None, Unset, int]
        if isinstance(self.likely_mislabeled_dep_percentile, Unset):
            likely_mislabeled_dep_percentile = UNSET
        else:
            likely_mislabeled_dep_percentile = self.likely_mislabeled_dep_percentile

        cbo_clusters: Union[None, Unset, list[int]]
        if isinstance(self.cbo_clusters, Unset):
            cbo_clusters = UNSET
        elif isinstance(self.cbo_clusters, list):
            cbo_clusters = self.cbo_clusters

        else:
            cbo_clusters = self.cbo_clusters

        data_embs: Union[None, Unset, bool]
        data_embs = UNSET if isinstance(self.data_embs, Unset) else self.data_embs

        confidence_high: Union[None, Unset, float]
        confidence_high = UNSET if isinstance(self.confidence_high, Unset) else self.confidence_high

        confidence_low: Union[None, Unset, float]
        confidence_low = UNSET if isinstance(self.confidence_low, Unset) else self.confidence_low

        is_otb: Union[None, Unset, bool]
        is_otb = UNSET if isinstance(self.is_otb, Unset) else self.is_otb

        image_ids: Union[None, Unset, list[int]]
        if isinstance(self.image_ids, Unset):
            image_ids = UNSET
        elif isinstance(self.image_ids, list):
            image_ids = self.image_ids

        else:
            image_ids = self.image_ids

        cluster_ids: Union[None, Unset, list[int]]
        if isinstance(self.cluster_ids, Unset):
            cluster_ids = UNSET
        elif isinstance(self.cluster_ids, list):
            cluster_ids = self.cluster_ids

        else:
            cluster_ids = self.cluster_ids

        correctly_classified: Union[None, Unset, bool]
        correctly_classified = UNSET if isinstance(self.correctly_classified, Unset) else self.correctly_classified

        is_edited: Union[None, Unset, bool]
        is_edited = UNSET if isinstance(self.is_edited, Unset) else self.is_edited

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if ids is not UNSET:
            field_dict["ids"] = ids
        if similar_to is not UNSET:
            field_dict["similar_to"] = similar_to
        if num_similar_to is not UNSET:
            field_dict["num_similar_to"] = num_similar_to
        if text_pat is not UNSET:
            field_dict["text_pat"] = text_pat
        if regex is not UNSET:
            field_dict["regex"] = regex
        if data_error_potential_high is not UNSET:
            field_dict["data_error_potential_high"] = data_error_potential_high
        if data_error_potential_low is not UNSET:
            field_dict["data_error_potential_low"] = data_error_potential_low
        if misclassified_only is not UNSET:
            field_dict["misclassified_only"] = misclassified_only
        if gold_filter is not UNSET:
            field_dict["gold_filter"] = gold_filter
        if pred_filter is not UNSET:
            field_dict["pred_filter"] = pred_filter
        if meta_filter is not UNSET:
            field_dict["meta_filter"] = meta_filter
        if drift_score_threshold is not UNSET:
            field_dict["drift_score_threshold"] = drift_score_threshold
        if is_drifted is not UNSET:
            field_dict["is_drifted"] = is_drifted
        if span_sample_ids is not UNSET:
            field_dict["span_sample_ids"] = span_sample_ids
        if span_text is not UNSET:
            field_dict["span_text"] = span_text
        if span_regex is not UNSET:
            field_dict["span_regex"] = span_regex
        if exclude_ids is not UNSET:
            field_dict["exclude_ids"] = exclude_ids
        if lasso is not UNSET:
            field_dict["lasso"] = lasso
        if class_filter is not UNSET:
            field_dict["class_filter"] = class_filter
        if likely_mislabeled is not UNSET:
            field_dict["likely_mislabeled"] = likely_mislabeled
        if likely_mislabeled_dep_percentile is not UNSET:
            field_dict["likely_mislabeled_dep_percentile"] = likely_mislabeled_dep_percentile
        if cbo_clusters is not UNSET:
            field_dict["cbo_clusters"] = cbo_clusters
        if data_embs is not UNSET:
            field_dict["data_embs"] = data_embs
        if confidence_high is not UNSET:
            field_dict["confidence_high"] = confidence_high
        if confidence_low is not UNSET:
            field_dict["confidence_low"] = confidence_low
        if is_otb is not UNSET:
            field_dict["is_otb"] = is_otb
        if image_ids is not UNSET:
            field_dict["image_ids"] = image_ids
        if cluster_ids is not UNSET:
            field_dict["cluster_ids"] = cluster_ids
        if correctly_classified is not UNSET:
            field_dict["correctly_classified"] = correctly_classified
        if is_edited is not UNSET:
            field_dict["is_edited"] = is_edited

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.lasso_selection import LassoSelection
        from ..models.meta_filter import MetaFilter

        d = dict(src_dict)
        ids = cast(list[int], d.pop("ids", UNSET))

        def _parse_similar_to(data: object) -> Union[None, Unset, list[int]]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                return cast(list[int], data)

            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, list[int]], data)

        similar_to = _parse_similar_to(d.pop("similar_to", UNSET))

        def _parse_num_similar_to(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        num_similar_to = _parse_num_similar_to(d.pop("num_similar_to", UNSET))

        def _parse_text_pat(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        text_pat = _parse_text_pat(d.pop("text_pat", UNSET))

        def _parse_regex(data: object) -> Union[None, Unset, bool]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, bool], data)

        regex = _parse_regex(d.pop("regex", UNSET))

        def _parse_data_error_potential_high(data: object) -> Union[None, Unset, float]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, float], data)

        data_error_potential_high = _parse_data_error_potential_high(d.pop("data_error_potential_high", UNSET))

        def _parse_data_error_potential_low(data: object) -> Union[None, Unset, float]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, float], data)

        data_error_potential_low = _parse_data_error_potential_low(d.pop("data_error_potential_low", UNSET))

        def _parse_misclassified_only(data: object) -> Union[None, Unset, bool]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, bool], data)

        misclassified_only = _parse_misclassified_only(d.pop("misclassified_only", UNSET))

        def _parse_gold_filter(data: object) -> Union[None, Unset, list[str]]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                return cast(list[str], data)

            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, list[str]], data)

        gold_filter = _parse_gold_filter(d.pop("gold_filter", UNSET))

        def _parse_pred_filter(data: object) -> Union[None, Unset, list[str]]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                return cast(list[str], data)

            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, list[str]], data)

        pred_filter = _parse_pred_filter(d.pop("pred_filter", UNSET))

        def _parse_meta_filter(data: object) -> Union[None, Unset, list["MetaFilter"]]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                meta_filter_type_0 = []
                _meta_filter_type_0 = data
                for meta_filter_type_0_item_data in _meta_filter_type_0:
                    meta_filter_type_0_item = MetaFilter.from_dict(meta_filter_type_0_item_data)

                    meta_filter_type_0.append(meta_filter_type_0_item)

                return meta_filter_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, list["MetaFilter"]], data)

        meta_filter = _parse_meta_filter(d.pop("meta_filter", UNSET))

        def _parse_drift_score_threshold(data: object) -> Union[None, Unset, float]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, float], data)

        drift_score_threshold = _parse_drift_score_threshold(d.pop("drift_score_threshold", UNSET))

        def _parse_is_drifted(data: object) -> Union[None, Unset, bool]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, bool], data)

        is_drifted = _parse_is_drifted(d.pop("is_drifted", UNSET))

        def _parse_span_sample_ids(data: object) -> Union[None, Unset, list[int]]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                return cast(list[int], data)

            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, list[int]], data)

        span_sample_ids = _parse_span_sample_ids(d.pop("span_sample_ids", UNSET))

        def _parse_span_text(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        span_text = _parse_span_text(d.pop("span_text", UNSET))

        def _parse_span_regex(data: object) -> Union[None, Unset, bool]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, bool], data)

        span_regex = _parse_span_regex(d.pop("span_regex", UNSET))

        exclude_ids = cast(list[int], d.pop("exclude_ids", UNSET))

        def _parse_lasso(data: object) -> Union["LassoSelection", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                return LassoSelection.from_dict(data)

            except:  # noqa: E722
                pass
            return cast(Union["LassoSelection", None, Unset], data)

        lasso = _parse_lasso(d.pop("lasso", UNSET))

        def _parse_class_filter(data: object) -> Union[None, Unset, list[str]]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                return cast(list[str], data)

            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, list[str]], data)

        class_filter = _parse_class_filter(d.pop("class_filter", UNSET))

        def _parse_likely_mislabeled(data: object) -> Union[None, Unset, bool]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, bool], data)

        likely_mislabeled = _parse_likely_mislabeled(d.pop("likely_mislabeled", UNSET))

        def _parse_likely_mislabeled_dep_percentile(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        likely_mislabeled_dep_percentile = _parse_likely_mislabeled_dep_percentile(
            d.pop("likely_mislabeled_dep_percentile", UNSET)
        )

        def _parse_cbo_clusters(data: object) -> Union[None, Unset, list[int]]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                return cast(list[int], data)

            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, list[int]], data)

        cbo_clusters = _parse_cbo_clusters(d.pop("cbo_clusters", UNSET))

        def _parse_data_embs(data: object) -> Union[None, Unset, bool]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, bool], data)

        data_embs = _parse_data_embs(d.pop("data_embs", UNSET))

        def _parse_confidence_high(data: object) -> Union[None, Unset, float]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, float], data)

        confidence_high = _parse_confidence_high(d.pop("confidence_high", UNSET))

        def _parse_confidence_low(data: object) -> Union[None, Unset, float]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, float], data)

        confidence_low = _parse_confidence_low(d.pop("confidence_low", UNSET))

        def _parse_is_otb(data: object) -> Union[None, Unset, bool]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, bool], data)

        is_otb = _parse_is_otb(d.pop("is_otb", UNSET))

        def _parse_image_ids(data: object) -> Union[None, Unset, list[int]]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                return cast(list[int], data)

            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, list[int]], data)

        image_ids = _parse_image_ids(d.pop("image_ids", UNSET))

        def _parse_cluster_ids(data: object) -> Union[None, Unset, list[int]]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                return cast(list[int], data)

            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, list[int]], data)

        cluster_ids = _parse_cluster_ids(d.pop("cluster_ids", UNSET))

        def _parse_correctly_classified(data: object) -> Union[None, Unset, bool]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, bool], data)

        correctly_classified = _parse_correctly_classified(d.pop("correctly_classified", UNSET))

        def _parse_is_edited(data: object) -> Union[None, Unset, bool]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, bool], data)

        is_edited = _parse_is_edited(d.pop("is_edited", UNSET))

        filter_params = cls(
            ids=ids,
            similar_to=similar_to,
            num_similar_to=num_similar_to,
            text_pat=text_pat,
            regex=regex,
            data_error_potential_high=data_error_potential_high,
            data_error_potential_low=data_error_potential_low,
            misclassified_only=misclassified_only,
            gold_filter=gold_filter,
            pred_filter=pred_filter,
            meta_filter=meta_filter,
            drift_score_threshold=drift_score_threshold,
            is_drifted=is_drifted,
            span_sample_ids=span_sample_ids,
            span_text=span_text,
            span_regex=span_regex,
            exclude_ids=exclude_ids,
            lasso=lasso,
            class_filter=class_filter,
            likely_mislabeled=likely_mislabeled,
            likely_mislabeled_dep_percentile=likely_mislabeled_dep_percentile,
            cbo_clusters=cbo_clusters,
            data_embs=data_embs,
            confidence_high=confidence_high,
            confidence_low=confidence_low,
            is_otb=is_otb,
            image_ids=image_ids,
            cluster_ids=cluster_ids,
            correctly_classified=correctly_classified,
            is_edited=is_edited,
        )

        filter_params.additional_properties = d
        return filter_params

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
