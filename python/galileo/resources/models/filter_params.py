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
    Attributes:
        cbo_clusters (Union[None, Unset, list[int]]):
        class_filter (Union[None, Unset, list[str]]):
        cluster_ids (Union[None, Unset, list[int]]):
        confidence_high (Union[None, Unset, float]):
        confidence_low (Union[None, Unset, float]):
        correctly_classified (Union[None, Unset, bool]):
        data_embs (Union[None, Unset, bool]):  Default: False.
        data_error_potential_high (Union[None, Unset, float]):
        data_error_potential_low (Union[None, Unset, float]):
        drift_score_threshold (Union[None, Unset, float]):
        exclude_ids (Union[Unset, list[int]]):
        gold_filter (Union[None, Unset, list[str]]):
        ids (Union[Unset, list[int]]):
        image_ids (Union[None, Unset, list[int]]):
        is_drifted (Union[None, Unset, bool]):
        is_edited (Union[None, Unset, bool]):
        is_otb (Union[None, Unset, bool]):
        lasso (Union['LassoSelection', None, Unset]):
        likely_mislabeled (Union[None, Unset, bool]):
        likely_mislabeled_dep_percentile (Union[None, Unset, int]):  Default: 0.
        meta_filter (Union[None, Unset, list['MetaFilter']]):
        misclassified_only (Union[None, Unset, bool]):
        num_similar_to (Union[None, Unset, int]):
        pred_filter (Union[None, Unset, list[str]]):
        regex (Union[None, Unset, bool]):
        similar_to (Union[None, Unset, list[int]]):
        span_regex (Union[None, Unset, bool]):  Default: False.
        span_sample_ids (Union[None, Unset, list[int]]):
        span_text (Union[None, Unset, str]):
        text_pat (Union[None, Unset, str]):
    """

    cbo_clusters: Union[None, Unset, list[int]] = UNSET
    class_filter: Union[None, Unset, list[str]] = UNSET
    cluster_ids: Union[None, Unset, list[int]] = UNSET
    confidence_high: Union[None, Unset, float] = UNSET
    confidence_low: Union[None, Unset, float] = UNSET
    correctly_classified: Union[None, Unset, bool] = UNSET
    data_embs: Union[None, Unset, bool] = False
    data_error_potential_high: Union[None, Unset, float] = UNSET
    data_error_potential_low: Union[None, Unset, float] = UNSET
    drift_score_threshold: Union[None, Unset, float] = UNSET
    exclude_ids: Union[Unset, list[int]] = UNSET
    gold_filter: Union[None, Unset, list[str]] = UNSET
    ids: Union[Unset, list[int]] = UNSET
    image_ids: Union[None, Unset, list[int]] = UNSET
    is_drifted: Union[None, Unset, bool] = UNSET
    is_edited: Union[None, Unset, bool] = UNSET
    is_otb: Union[None, Unset, bool] = UNSET
    lasso: Union["LassoSelection", None, Unset] = UNSET
    likely_mislabeled: Union[None, Unset, bool] = UNSET
    likely_mislabeled_dep_percentile: Union[None, Unset, int] = 0
    meta_filter: Union[None, Unset, list["MetaFilter"]] = UNSET
    misclassified_only: Union[None, Unset, bool] = UNSET
    num_similar_to: Union[None, Unset, int] = UNSET
    pred_filter: Union[None, Unset, list[str]] = UNSET
    regex: Union[None, Unset, bool] = UNSET
    similar_to: Union[None, Unset, list[int]] = UNSET
    span_regex: Union[None, Unset, bool] = False
    span_sample_ids: Union[None, Unset, list[int]] = UNSET
    span_text: Union[None, Unset, str] = UNSET
    text_pat: Union[None, Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.lasso_selection import LassoSelection

        cbo_clusters: Union[None, Unset, list[int]]
        if isinstance(self.cbo_clusters, Unset):
            cbo_clusters = UNSET
        elif isinstance(self.cbo_clusters, list):
            cbo_clusters = self.cbo_clusters

        else:
            cbo_clusters = self.cbo_clusters

        class_filter: Union[None, Unset, list[str]]
        if isinstance(self.class_filter, Unset):
            class_filter = UNSET
        elif isinstance(self.class_filter, list):
            class_filter = self.class_filter

        else:
            class_filter = self.class_filter

        cluster_ids: Union[None, Unset, list[int]]
        if isinstance(self.cluster_ids, Unset):
            cluster_ids = UNSET
        elif isinstance(self.cluster_ids, list):
            cluster_ids = self.cluster_ids

        else:
            cluster_ids = self.cluster_ids

        confidence_high: Union[None, Unset, float]
        if isinstance(self.confidence_high, Unset):
            confidence_high = UNSET
        else:
            confidence_high = self.confidence_high

        confidence_low: Union[None, Unset, float]
        if isinstance(self.confidence_low, Unset):
            confidence_low = UNSET
        else:
            confidence_low = self.confidence_low

        correctly_classified: Union[None, Unset, bool]
        if isinstance(self.correctly_classified, Unset):
            correctly_classified = UNSET
        else:
            correctly_classified = self.correctly_classified

        data_embs: Union[None, Unset, bool]
        if isinstance(self.data_embs, Unset):
            data_embs = UNSET
        else:
            data_embs = self.data_embs

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

        drift_score_threshold: Union[None, Unset, float]
        if isinstance(self.drift_score_threshold, Unset):
            drift_score_threshold = UNSET
        else:
            drift_score_threshold = self.drift_score_threshold

        exclude_ids: Union[Unset, list[int]] = UNSET
        if not isinstance(self.exclude_ids, Unset):
            exclude_ids = self.exclude_ids

        gold_filter: Union[None, Unset, list[str]]
        if isinstance(self.gold_filter, Unset):
            gold_filter = UNSET
        elif isinstance(self.gold_filter, list):
            gold_filter = self.gold_filter

        else:
            gold_filter = self.gold_filter

        ids: Union[Unset, list[int]] = UNSET
        if not isinstance(self.ids, Unset):
            ids = self.ids

        image_ids: Union[None, Unset, list[int]]
        if isinstance(self.image_ids, Unset):
            image_ids = UNSET
        elif isinstance(self.image_ids, list):
            image_ids = self.image_ids

        else:
            image_ids = self.image_ids

        is_drifted: Union[None, Unset, bool]
        if isinstance(self.is_drifted, Unset):
            is_drifted = UNSET
        else:
            is_drifted = self.is_drifted

        is_edited: Union[None, Unset, bool]
        if isinstance(self.is_edited, Unset):
            is_edited = UNSET
        else:
            is_edited = self.is_edited

        is_otb: Union[None, Unset, bool]
        if isinstance(self.is_otb, Unset):
            is_otb = UNSET
        else:
            is_otb = self.is_otb

        lasso: Union[None, Unset, dict[str, Any]]
        if isinstance(self.lasso, Unset):
            lasso = UNSET
        elif isinstance(self.lasso, LassoSelection):
            lasso = self.lasso.to_dict()
        else:
            lasso = self.lasso

        likely_mislabeled: Union[None, Unset, bool]
        if isinstance(self.likely_mislabeled, Unset):
            likely_mislabeled = UNSET
        else:
            likely_mislabeled = self.likely_mislabeled

        likely_mislabeled_dep_percentile: Union[None, Unset, int]
        if isinstance(self.likely_mislabeled_dep_percentile, Unset):
            likely_mislabeled_dep_percentile = UNSET
        else:
            likely_mislabeled_dep_percentile = self.likely_mislabeled_dep_percentile

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

        misclassified_only: Union[None, Unset, bool]
        if isinstance(self.misclassified_only, Unset):
            misclassified_only = UNSET
        else:
            misclassified_only = self.misclassified_only

        num_similar_to: Union[None, Unset, int]
        if isinstance(self.num_similar_to, Unset):
            num_similar_to = UNSET
        else:
            num_similar_to = self.num_similar_to

        pred_filter: Union[None, Unset, list[str]]
        if isinstance(self.pred_filter, Unset):
            pred_filter = UNSET
        elif isinstance(self.pred_filter, list):
            pred_filter = self.pred_filter

        else:
            pred_filter = self.pred_filter

        regex: Union[None, Unset, bool]
        if isinstance(self.regex, Unset):
            regex = UNSET
        else:
            regex = self.regex

        similar_to: Union[None, Unset, list[int]]
        if isinstance(self.similar_to, Unset):
            similar_to = UNSET
        elif isinstance(self.similar_to, list):
            similar_to = self.similar_to

        else:
            similar_to = self.similar_to

        span_regex: Union[None, Unset, bool]
        if isinstance(self.span_regex, Unset):
            span_regex = UNSET
        else:
            span_regex = self.span_regex

        span_sample_ids: Union[None, Unset, list[int]]
        if isinstance(self.span_sample_ids, Unset):
            span_sample_ids = UNSET
        elif isinstance(self.span_sample_ids, list):
            span_sample_ids = self.span_sample_ids

        else:
            span_sample_ids = self.span_sample_ids

        span_text: Union[None, Unset, str]
        if isinstance(self.span_text, Unset):
            span_text = UNSET
        else:
            span_text = self.span_text

        text_pat: Union[None, Unset, str]
        if isinstance(self.text_pat, Unset):
            text_pat = UNSET
        else:
            text_pat = self.text_pat

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if cbo_clusters is not UNSET:
            field_dict["cbo_clusters"] = cbo_clusters
        if class_filter is not UNSET:
            field_dict["class_filter"] = class_filter
        if cluster_ids is not UNSET:
            field_dict["cluster_ids"] = cluster_ids
        if confidence_high is not UNSET:
            field_dict["confidence_high"] = confidence_high
        if confidence_low is not UNSET:
            field_dict["confidence_low"] = confidence_low
        if correctly_classified is not UNSET:
            field_dict["correctly_classified"] = correctly_classified
        if data_embs is not UNSET:
            field_dict["data_embs"] = data_embs
        if data_error_potential_high is not UNSET:
            field_dict["data_error_potential_high"] = data_error_potential_high
        if data_error_potential_low is not UNSET:
            field_dict["data_error_potential_low"] = data_error_potential_low
        if drift_score_threshold is not UNSET:
            field_dict["drift_score_threshold"] = drift_score_threshold
        if exclude_ids is not UNSET:
            field_dict["exclude_ids"] = exclude_ids
        if gold_filter is not UNSET:
            field_dict["gold_filter"] = gold_filter
        if ids is not UNSET:
            field_dict["ids"] = ids
        if image_ids is not UNSET:
            field_dict["image_ids"] = image_ids
        if is_drifted is not UNSET:
            field_dict["is_drifted"] = is_drifted
        if is_edited is not UNSET:
            field_dict["is_edited"] = is_edited
        if is_otb is not UNSET:
            field_dict["is_otb"] = is_otb
        if lasso is not UNSET:
            field_dict["lasso"] = lasso
        if likely_mislabeled is not UNSET:
            field_dict["likely_mislabeled"] = likely_mislabeled
        if likely_mislabeled_dep_percentile is not UNSET:
            field_dict["likely_mislabeled_dep_percentile"] = likely_mislabeled_dep_percentile
        if meta_filter is not UNSET:
            field_dict["meta_filter"] = meta_filter
        if misclassified_only is not UNSET:
            field_dict["misclassified_only"] = misclassified_only
        if num_similar_to is not UNSET:
            field_dict["num_similar_to"] = num_similar_to
        if pred_filter is not UNSET:
            field_dict["pred_filter"] = pred_filter
        if regex is not UNSET:
            field_dict["regex"] = regex
        if similar_to is not UNSET:
            field_dict["similar_to"] = similar_to
        if span_regex is not UNSET:
            field_dict["span_regex"] = span_regex
        if span_sample_ids is not UNSET:
            field_dict["span_sample_ids"] = span_sample_ids
        if span_text is not UNSET:
            field_dict["span_text"] = span_text
        if text_pat is not UNSET:
            field_dict["text_pat"] = text_pat

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.lasso_selection import LassoSelection
        from ..models.meta_filter import MetaFilter

        d = src_dict.copy()

        def _parse_cbo_clusters(data: object) -> Union[None, Unset, list[int]]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                cbo_clusters_type_0 = cast(list[int], data)

                return cbo_clusters_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, list[int]], data)

        cbo_clusters = _parse_cbo_clusters(d.pop("cbo_clusters", UNSET))

        def _parse_class_filter(data: object) -> Union[None, Unset, list[str]]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                class_filter_type_0 = cast(list[str], data)

                return class_filter_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, list[str]], data)

        class_filter = _parse_class_filter(d.pop("class_filter", UNSET))

        def _parse_cluster_ids(data: object) -> Union[None, Unset, list[int]]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                cluster_ids_type_0 = cast(list[int], data)

                return cluster_ids_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, list[int]], data)

        cluster_ids = _parse_cluster_ids(d.pop("cluster_ids", UNSET))

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

        def _parse_correctly_classified(data: object) -> Union[None, Unset, bool]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, bool], data)

        correctly_classified = _parse_correctly_classified(d.pop("correctly_classified", UNSET))

        def _parse_data_embs(data: object) -> Union[None, Unset, bool]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, bool], data)

        data_embs = _parse_data_embs(d.pop("data_embs", UNSET))

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

        def _parse_drift_score_threshold(data: object) -> Union[None, Unset, float]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, float], data)

        drift_score_threshold = _parse_drift_score_threshold(d.pop("drift_score_threshold", UNSET))

        exclude_ids = cast(list[int], d.pop("exclude_ids", UNSET))

        def _parse_gold_filter(data: object) -> Union[None, Unset, list[str]]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                gold_filter_type_0 = cast(list[str], data)

                return gold_filter_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, list[str]], data)

        gold_filter = _parse_gold_filter(d.pop("gold_filter", UNSET))

        ids = cast(list[int], d.pop("ids", UNSET))

        def _parse_image_ids(data: object) -> Union[None, Unset, list[int]]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                image_ids_type_0 = cast(list[int], data)

                return image_ids_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, list[int]], data)

        image_ids = _parse_image_ids(d.pop("image_ids", UNSET))

        def _parse_is_drifted(data: object) -> Union[None, Unset, bool]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, bool], data)

        is_drifted = _parse_is_drifted(d.pop("is_drifted", UNSET))

        def _parse_is_edited(data: object) -> Union[None, Unset, bool]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, bool], data)

        is_edited = _parse_is_edited(d.pop("is_edited", UNSET))

        def _parse_is_otb(data: object) -> Union[None, Unset, bool]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, bool], data)

        is_otb = _parse_is_otb(d.pop("is_otb", UNSET))

        def _parse_lasso(data: object) -> Union["LassoSelection", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                lasso_type_0 = LassoSelection.from_dict(data)

                return lasso_type_0
            except:  # noqa: E722
                pass
            return cast(Union["LassoSelection", None, Unset], data)

        lasso = _parse_lasso(d.pop("lasso", UNSET))

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

        def _parse_misclassified_only(data: object) -> Union[None, Unset, bool]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, bool], data)

        misclassified_only = _parse_misclassified_only(d.pop("misclassified_only", UNSET))

        def _parse_num_similar_to(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        num_similar_to = _parse_num_similar_to(d.pop("num_similar_to", UNSET))

        def _parse_pred_filter(data: object) -> Union[None, Unset, list[str]]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                pred_filter_type_0 = cast(list[str], data)

                return pred_filter_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, list[str]], data)

        pred_filter = _parse_pred_filter(d.pop("pred_filter", UNSET))

        def _parse_regex(data: object) -> Union[None, Unset, bool]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, bool], data)

        regex = _parse_regex(d.pop("regex", UNSET))

        def _parse_similar_to(data: object) -> Union[None, Unset, list[int]]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                similar_to_type_0 = cast(list[int], data)

                return similar_to_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, list[int]], data)

        similar_to = _parse_similar_to(d.pop("similar_to", UNSET))

        def _parse_span_regex(data: object) -> Union[None, Unset, bool]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, bool], data)

        span_regex = _parse_span_regex(d.pop("span_regex", UNSET))

        def _parse_span_sample_ids(data: object) -> Union[None, Unset, list[int]]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                span_sample_ids_type_0 = cast(list[int], data)

                return span_sample_ids_type_0
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

        def _parse_text_pat(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        text_pat = _parse_text_pat(d.pop("text_pat", UNSET))

        filter_params = cls(
            cbo_clusters=cbo_clusters,
            class_filter=class_filter,
            cluster_ids=cluster_ids,
            confidence_high=confidence_high,
            confidence_low=confidence_low,
            correctly_classified=correctly_classified,
            data_embs=data_embs,
            data_error_potential_high=data_error_potential_high,
            data_error_potential_low=data_error_potential_low,
            drift_score_threshold=drift_score_threshold,
            exclude_ids=exclude_ids,
            gold_filter=gold_filter,
            ids=ids,
            image_ids=image_ids,
            is_drifted=is_drifted,
            is_edited=is_edited,
            is_otb=is_otb,
            lasso=lasso,
            likely_mislabeled=likely_mislabeled,
            likely_mislabeled_dep_percentile=likely_mislabeled_dep_percentile,
            meta_filter=meta_filter,
            misclassified_only=misclassified_only,
            num_similar_to=num_similar_to,
            pred_filter=pred_filter,
            regex=regex,
            similar_to=similar_to,
            span_regex=span_regex,
            span_sample_ids=span_sample_ids,
            span_text=span_text,
            text_pat=text_pat,
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
