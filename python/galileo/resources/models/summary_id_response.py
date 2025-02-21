from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.split import Split
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.filter_params import FilterParams


T = TypeVar("T", bound="SummaryIDResponse")


@_attrs_define
class SummaryIDResponse:
    """
    Attributes:
        ids (list[int]):
        compare_to (Union[None, Split, Unset]):
        filter_params (Union[Unset, FilterParams]):
        hard_easy_threshold (Union[Unset, bool]):  Default: False.
        include_emb (Union[Unset, bool]):  Default: True.
        map_threshold (Union[Unset, float]):  Default: 0.5.
        meta_cols (Union[None, Unset, list[str]]):
        page_num (Union[Unset, int]):  Default: 0.
        sort_ascending (Union[Unset, bool]):  Default: False.
        sort_by (Union[None, Unset, str]):
        sort_by_id_list (Union[Unset, bool]):  Default: False.
        task (Union[None, Unset, str]):
    """

    ids: list[int]
    compare_to: Union[None, Split, Unset] = UNSET
    filter_params: Union[Unset, "FilterParams"] = UNSET
    hard_easy_threshold: Union[Unset, bool] = False
    include_emb: Union[Unset, bool] = True
    map_threshold: Union[Unset, float] = 0.5
    meta_cols: Union[None, Unset, list[str]] = UNSET
    page_num: Union[Unset, int] = 0
    sort_ascending: Union[Unset, bool] = False
    sort_by: Union[None, Unset, str] = UNSET
    sort_by_id_list: Union[Unset, bool] = False
    task: Union[None, Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        ids = self.ids

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

        hard_easy_threshold = self.hard_easy_threshold

        include_emb = self.include_emb

        map_threshold = self.map_threshold

        meta_cols: Union[None, Unset, list[str]]
        if isinstance(self.meta_cols, Unset):
            meta_cols = UNSET
        elif isinstance(self.meta_cols, list):
            meta_cols = self.meta_cols

        else:
            meta_cols = self.meta_cols

        page_num = self.page_num

        sort_ascending = self.sort_ascending

        sort_by: Union[None, Unset, str]
        if isinstance(self.sort_by, Unset):
            sort_by = UNSET
        else:
            sort_by = self.sort_by

        sort_by_id_list = self.sort_by_id_list

        task: Union[None, Unset, str]
        if isinstance(self.task, Unset):
            task = UNSET
        else:
            task = self.task

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({"ids": ids})
        if compare_to is not UNSET:
            field_dict["compare_to"] = compare_to
        if filter_params is not UNSET:
            field_dict["filter_params"] = filter_params
        if hard_easy_threshold is not UNSET:
            field_dict["hard_easy_threshold"] = hard_easy_threshold
        if include_emb is not UNSET:
            field_dict["include_emb"] = include_emb
        if map_threshold is not UNSET:
            field_dict["map_threshold"] = map_threshold
        if meta_cols is not UNSET:
            field_dict["meta_cols"] = meta_cols
        if page_num is not UNSET:
            field_dict["page_num"] = page_num
        if sort_ascending is not UNSET:
            field_dict["sort_ascending"] = sort_ascending
        if sort_by is not UNSET:
            field_dict["sort_by"] = sort_by
        if sort_by_id_list is not UNSET:
            field_dict["sort_by_id_list"] = sort_by_id_list
        if task is not UNSET:
            field_dict["task"] = task

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.filter_params import FilterParams

        d = src_dict.copy()
        ids = cast(list[int], d.pop("ids"))

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

        hard_easy_threshold = d.pop("hard_easy_threshold", UNSET)

        include_emb = d.pop("include_emb", UNSET)

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

        page_num = d.pop("page_num", UNSET)

        sort_ascending = d.pop("sort_ascending", UNSET)

        def _parse_sort_by(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        sort_by = _parse_sort_by(d.pop("sort_by", UNSET))

        sort_by_id_list = d.pop("sort_by_id_list", UNSET)

        def _parse_task(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        task = _parse_task(d.pop("task", UNSET))

        summary_id_response = cls(
            ids=ids,
            compare_to=compare_to,
            filter_params=filter_params,
            hard_easy_threshold=hard_easy_threshold,
            include_emb=include_emb,
            map_threshold=map_threshold,
            meta_cols=meta_cols,
            page_num=page_num,
            sort_ascending=sort_ascending,
            sort_by=sort_by,
            sort_by_id_list=sort_by_id_list,
            task=task,
        )

        summary_id_response.additional_properties = d
        return summary_id_response

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
