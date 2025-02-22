from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.split import Split
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.filter_params import FilterParams


T = TypeVar("T", bound="InsightChartResponse")


@_attrs_define
class InsightChartResponse:
    """
    Attributes:
        data (list[list[Union[float, int]]]):
        x_labels (list[str]):
        y_labels (list[str]):
        compare_to (Union[None, Split, Unset]):
        filter_params (Union[Unset, FilterParams]):
        map_threshold (Union[Unset, float]):  Default: 0.5.
        meta_cols (Union[None, Unset, list[str]]):
        task (Union[None, Unset, str]):
    """

    data: list[list[Union[float, int]]]
    x_labels: list[str]
    y_labels: list[str]
    compare_to: Union[None, Split, Unset] = UNSET
    filter_params: Union[Unset, "FilterParams"] = UNSET
    map_threshold: Union[Unset, float] = 0.5
    meta_cols: Union[None, Unset, list[str]] = UNSET
    task: Union[None, Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        data = []
        for data_item_data in self.data:
            data_item = []
            for data_item_item_data in data_item_data:
                data_item_item: Union[float, int]
                data_item_item = data_item_item_data
                data_item.append(data_item_item)

            data.append(data_item)

        x_labels = self.x_labels

        y_labels = self.y_labels

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

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({"data": data, "x_labels": x_labels, "y_labels": y_labels})
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

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.filter_params import FilterParams

        d = src_dict.copy()
        data = []
        _data = d.pop("data")
        for data_item_data in _data:
            data_item = []
            _data_item = data_item_data
            for data_item_item_data in _data_item:

                def _parse_data_item_item(data: object) -> Union[float, int]:
                    return cast(Union[float, int], data)

                data_item_item = _parse_data_item_item(data_item_item_data)

                data_item.append(data_item_item)

            data.append(data_item)

        x_labels = cast(list[str], d.pop("x_labels"))

        y_labels = cast(list[str], d.pop("y_labels"))

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

        insight_chart_response = cls(
            data=data,
            x_labels=x_labels,
            y_labels=y_labels,
            compare_to=compare_to,
            filter_params=filter_params,
            map_threshold=map_threshold,
            meta_cols=meta_cols,
            task=task,
        )

        insight_chart_response.additional_properties = d
        return insight_chart_response

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
