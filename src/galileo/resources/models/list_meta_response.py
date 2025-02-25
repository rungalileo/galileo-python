from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.split import Split
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.filter_params import FilterParams
    from ..models.meta_info import MetaInfo


T = TypeVar("T", bound="ListMetaResponse")


@_attrs_define
class ListMetaResponse:
    """
    Attributes:
        meta (list['MetaInfo']):
        project_id (str):
        run_id (str):
        split (Split):
        compare_to (Union[None, Split, Unset]):
        filter_params (Union[Unset, FilterParams]):
        inference_name (Union[None, Unset, str]):
        map_threshold (Union[Unset, float]):  Default: 0.5.
        task (Union[None, Unset, str]):
    """

    meta: list["MetaInfo"]
    project_id: str
    run_id: str
    split: Split
    compare_to: Union[None, Split, Unset] = UNSET
    filter_params: Union[Unset, "FilterParams"] = UNSET
    inference_name: Union[None, Unset, str] = UNSET
    map_threshold: Union[Unset, float] = 0.5
    task: Union[None, Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        meta = []
        for meta_item_data in self.meta:
            meta_item = meta_item_data.to_dict()
            meta.append(meta_item)

        project_id = self.project_id

        run_id = self.run_id

        split = self.split.value

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

        inference_name: Union[None, Unset, str]
        if isinstance(self.inference_name, Unset):
            inference_name = UNSET
        else:
            inference_name = self.inference_name

        map_threshold = self.map_threshold

        task: Union[None, Unset, str]
        if isinstance(self.task, Unset):
            task = UNSET
        else:
            task = self.task

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({"meta": meta, "project_id": project_id, "run_id": run_id, "split": split})
        if compare_to is not UNSET:
            field_dict["compare_to"] = compare_to
        if filter_params is not UNSET:
            field_dict["filter_params"] = filter_params
        if inference_name is not UNSET:
            field_dict["inference_name"] = inference_name
        if map_threshold is not UNSET:
            field_dict["map_threshold"] = map_threshold
        if task is not UNSET:
            field_dict["task"] = task

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.filter_params import FilterParams
        from ..models.meta_info import MetaInfo

        d = src_dict.copy()
        meta = []
        _meta = d.pop("meta")
        for meta_item_data in _meta:
            meta_item = MetaInfo.from_dict(meta_item_data)

            meta.append(meta_item)

        project_id = d.pop("project_id")

        run_id = d.pop("run_id")

        split = Split(d.pop("split"))

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

        def _parse_inference_name(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        inference_name = _parse_inference_name(d.pop("inference_name", UNSET))

        map_threshold = d.pop("map_threshold", UNSET)

        def _parse_task(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        task = _parse_task(d.pop("task", UNSET))

        list_meta_response = cls(
            meta=meta,
            project_id=project_id,
            run_id=run_id,
            split=split,
            compare_to=compare_to,
            filter_params=filter_params,
            inference_name=inference_name,
            map_threshold=map_threshold,
            task=task,
        )

        list_meta_response.additional_properties = d
        return list_meta_response

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
