from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.split import Split
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.filter_params import FilterParams


T = TypeVar("T", bound="DistributionRequest")


@_attrs_define
class DistributionRequest:
    """A distribution histogram for a run/filter for a particular numerical column.

    bins are boundaries for the x axis and counts are the y axis. bins will have 1 more value than counts because the
    count at index i is for the range [bin[i], bin[i+1]), with the lower boundary inclusive and the upper boundary
    exclusive

        Attributes:
            col (str):
            compare_to (Union[None, Split, Unset]):
            filter_params (Union[Unset, FilterParams]):
            include_metrics (Union[Unset, bool]):  Default: False.
            limit_max (Union[None, Unset, int]):
            limit_min (Union[None, Unset, int]):
            map_threshold (Union[Unset, float]):  Default: 0.5.
            meta_cols (Union[None, Unset, list[str]]):
            nbins (Union[Unset, int]):  Default: 20.
            remove_outliers (Union[Unset, bool]):  Default: False.
            task (Union[None, Unset, str]):
    """

    col: str
    compare_to: Union[None, Split, Unset] = UNSET
    filter_params: Union[Unset, "FilterParams"] = UNSET
    include_metrics: Union[Unset, bool] = False
    limit_max: Union[None, Unset, int] = UNSET
    limit_min: Union[None, Unset, int] = UNSET
    map_threshold: Union[Unset, float] = 0.5
    meta_cols: Union[None, Unset, list[str]] = UNSET
    nbins: Union[Unset, int] = 20
    remove_outliers: Union[Unset, bool] = False
    task: Union[None, Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        col = self.col

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

        include_metrics = self.include_metrics

        limit_max: Union[None, Unset, int]
        if isinstance(self.limit_max, Unset):
            limit_max = UNSET
        else:
            limit_max = self.limit_max

        limit_min: Union[None, Unset, int]
        if isinstance(self.limit_min, Unset):
            limit_min = UNSET
        else:
            limit_min = self.limit_min

        map_threshold = self.map_threshold

        meta_cols: Union[None, Unset, list[str]]
        if isinstance(self.meta_cols, Unset):
            meta_cols = UNSET
        elif isinstance(self.meta_cols, list):
            meta_cols = self.meta_cols

        else:
            meta_cols = self.meta_cols

        nbins = self.nbins

        remove_outliers = self.remove_outliers

        task: Union[None, Unset, str]
        if isinstance(self.task, Unset):
            task = UNSET
        else:
            task = self.task

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({"col": col})
        if compare_to is not UNSET:
            field_dict["compare_to"] = compare_to
        if filter_params is not UNSET:
            field_dict["filter_params"] = filter_params
        if include_metrics is not UNSET:
            field_dict["include_metrics"] = include_metrics
        if limit_max is not UNSET:
            field_dict["limit_max"] = limit_max
        if limit_min is not UNSET:
            field_dict["limit_min"] = limit_min
        if map_threshold is not UNSET:
            field_dict["map_threshold"] = map_threshold
        if meta_cols is not UNSET:
            field_dict["meta_cols"] = meta_cols
        if nbins is not UNSET:
            field_dict["nbins"] = nbins
        if remove_outliers is not UNSET:
            field_dict["remove_outliers"] = remove_outliers
        if task is not UNSET:
            field_dict["task"] = task

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.filter_params import FilterParams

        d = src_dict.copy()
        col = d.pop("col")

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

        include_metrics = d.pop("include_metrics", UNSET)

        def _parse_limit_max(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        limit_max = _parse_limit_max(d.pop("limit_max", UNSET))

        def _parse_limit_min(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        limit_min = _parse_limit_min(d.pop("limit_min", UNSET))

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

        nbins = d.pop("nbins", UNSET)

        remove_outliers = d.pop("remove_outliers", UNSET)

        def _parse_task(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        task = _parse_task(d.pop("task", UNSET))

        distribution_request = cls(
            col=col,
            compare_to=compare_to,
            filter_params=filter_params,
            include_metrics=include_metrics,
            limit_max=limit_max,
            limit_min=limit_min,
            map_threshold=map_threshold,
            meta_cols=meta_cols,
            nbins=nbins,
            remove_outliers=remove_outliers,
            task=task,
        )

        distribution_request.additional_properties = d
        return distribution_request

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
