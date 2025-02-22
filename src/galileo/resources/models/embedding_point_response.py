from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.split import Split
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.circle import Circle
    from ..models.embedding_data import EmbeddingData
    from ..models.filter_params import FilterParams


T = TypeVar("T", bound="EmbeddingPointResponse")


@_attrs_define
class EmbeddingPointResponse:
    """
    Attributes:
        embedding_data (list['EmbeddingData']):
        circle (Union['Circle', None, Unset]):
        compare_to (Union[None, Split, Unset]):
        filter_params (Union[Unset, FilterParams]):
        ids (Union[Unset, list[int]]):
        map_threshold (Union[Unset, float]):  Default: 0.5.
        meta_cols (Union[None, Unset, list[str]]):
        num_samples (Union[Unset, int]):  Default: 5.
        task (Union[None, Unset, str]):
    """

    embedding_data: list["EmbeddingData"]
    circle: Union["Circle", None, Unset] = UNSET
    compare_to: Union[None, Split, Unset] = UNSET
    filter_params: Union[Unset, "FilterParams"] = UNSET
    ids: Union[Unset, list[int]] = UNSET
    map_threshold: Union[Unset, float] = 0.5
    meta_cols: Union[None, Unset, list[str]] = UNSET
    num_samples: Union[Unset, int] = 5
    task: Union[None, Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.circle import Circle

        embedding_data = []
        for embedding_data_item_data in self.embedding_data:
            embedding_data_item = embedding_data_item_data.to_dict()
            embedding_data.append(embedding_data_item)

        circle: Union[None, Unset, dict[str, Any]]
        if isinstance(self.circle, Unset):
            circle = UNSET
        elif isinstance(self.circle, Circle):
            circle = self.circle.to_dict()
        else:
            circle = self.circle

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

        ids: Union[Unset, list[int]] = UNSET
        if not isinstance(self.ids, Unset):
            ids = self.ids

        map_threshold = self.map_threshold

        meta_cols: Union[None, Unset, list[str]]
        if isinstance(self.meta_cols, Unset):
            meta_cols = UNSET
        elif isinstance(self.meta_cols, list):
            meta_cols = self.meta_cols

        else:
            meta_cols = self.meta_cols

        num_samples = self.num_samples

        task: Union[None, Unset, str]
        if isinstance(self.task, Unset):
            task = UNSET
        else:
            task = self.task

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({"embedding_data": embedding_data})
        if circle is not UNSET:
            field_dict["circle"] = circle
        if compare_to is not UNSET:
            field_dict["compare_to"] = compare_to
        if filter_params is not UNSET:
            field_dict["filter_params"] = filter_params
        if ids is not UNSET:
            field_dict["ids"] = ids
        if map_threshold is not UNSET:
            field_dict["map_threshold"] = map_threshold
        if meta_cols is not UNSET:
            field_dict["meta_cols"] = meta_cols
        if num_samples is not UNSET:
            field_dict["num_samples"] = num_samples
        if task is not UNSET:
            field_dict["task"] = task

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.circle import Circle
        from ..models.embedding_data import EmbeddingData
        from ..models.filter_params import FilterParams

        d = src_dict.copy()
        embedding_data = []
        _embedding_data = d.pop("embedding_data")
        for embedding_data_item_data in _embedding_data:
            embedding_data_item = EmbeddingData.from_dict(embedding_data_item_data)

            embedding_data.append(embedding_data_item)

        def _parse_circle(data: object) -> Union["Circle", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                circle_type_0 = Circle.from_dict(data)

                return circle_type_0
            except:  # noqa: E722
                pass
            return cast(Union["Circle", None, Unset], data)

        circle = _parse_circle(d.pop("circle", UNSET))

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

        ids = cast(list[int], d.pop("ids", UNSET))

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

        num_samples = d.pop("num_samples", UNSET)

        def _parse_task(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        task = _parse_task(d.pop("task", UNSET))

        embedding_point_response = cls(
            embedding_data=embedding_data,
            circle=circle,
            compare_to=compare_to,
            filter_params=filter_params,
            ids=ids,
            map_threshold=map_threshold,
            meta_cols=meta_cols,
            num_samples=num_samples,
            task=task,
        )

        embedding_point_response.additional_properties = d
        return embedding_point_response

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
