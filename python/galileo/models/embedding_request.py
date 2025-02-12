from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.file_type import FileType
from ..models.split import Split
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.filter_params import FilterParams


T = TypeVar("T", bound="EmbeddingRequest")


@_attrs_define
class EmbeddingRequest:
    """
    Attributes:
        compare_to (Union[None, Split, Unset]):
        file_type (Union[Unset, FileType]):
        filter_params (Union[Unset, FilterParams]):
        include_text_sample (Union[Unset, bool]):  Default: False.
        map_threshold (Union[Unset, float]):  Default: 0.5.
        meta_cols (Union[None, Unset, list[str]]):
        num_samples (Union[None, Unset, int]):
        only_meta_cols (Union[Unset, bool]):  Default: False.
        task (Union[None, Unset, str]):
        text_sample_length (Union[None, Unset, int]):  Default: 500.
        use_seed (Union[Unset, bool]):  Default: True.
    """

    compare_to: Union[None, Split, Unset] = UNSET
    file_type: Union[Unset, FileType] = UNSET
    filter_params: Union[Unset, "FilterParams"] = UNSET
    include_text_sample: Union[Unset, bool] = False
    map_threshold: Union[Unset, float] = 0.5
    meta_cols: Union[None, Unset, list[str]] = UNSET
    num_samples: Union[None, Unset, int] = UNSET
    only_meta_cols: Union[Unset, bool] = False
    task: Union[None, Unset, str] = UNSET
    text_sample_length: Union[None, Unset, int] = 500
    use_seed: Union[Unset, bool] = True
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        compare_to: Union[None, Unset, str]
        if isinstance(self.compare_to, Unset):
            compare_to = UNSET
        elif isinstance(self.compare_to, Split):
            compare_to = self.compare_to.value
        else:
            compare_to = self.compare_to

        file_type: Union[Unset, str] = UNSET
        if not isinstance(self.file_type, Unset):
            file_type = self.file_type.value

        filter_params: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.filter_params, Unset):
            filter_params = self.filter_params.to_dict()

        include_text_sample = self.include_text_sample

        map_threshold = self.map_threshold

        meta_cols: Union[None, Unset, list[str]]
        if isinstance(self.meta_cols, Unset):
            meta_cols = UNSET
        elif isinstance(self.meta_cols, list):
            meta_cols = self.meta_cols

        else:
            meta_cols = self.meta_cols

        num_samples: Union[None, Unset, int]
        if isinstance(self.num_samples, Unset):
            num_samples = UNSET
        else:
            num_samples = self.num_samples

        only_meta_cols = self.only_meta_cols

        task: Union[None, Unset, str]
        if isinstance(self.task, Unset):
            task = UNSET
        else:
            task = self.task

        text_sample_length: Union[None, Unset, int]
        if isinstance(self.text_sample_length, Unset):
            text_sample_length = UNSET
        else:
            text_sample_length = self.text_sample_length

        use_seed = self.use_seed

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if compare_to is not UNSET:
            field_dict["compare_to"] = compare_to
        if file_type is not UNSET:
            field_dict["file_type"] = file_type
        if filter_params is not UNSET:
            field_dict["filter_params"] = filter_params
        if include_text_sample is not UNSET:
            field_dict["include_text_sample"] = include_text_sample
        if map_threshold is not UNSET:
            field_dict["map_threshold"] = map_threshold
        if meta_cols is not UNSET:
            field_dict["meta_cols"] = meta_cols
        if num_samples is not UNSET:
            field_dict["num_samples"] = num_samples
        if only_meta_cols is not UNSET:
            field_dict["only_meta_cols"] = only_meta_cols
        if task is not UNSET:
            field_dict["task"] = task
        if text_sample_length is not UNSET:
            field_dict["text_sample_length"] = text_sample_length
        if use_seed is not UNSET:
            field_dict["use_seed"] = use_seed

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.filter_params import FilterParams

        d = src_dict.copy()

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

        _file_type = d.pop("file_type", UNSET)
        file_type: Union[Unset, FileType]
        if isinstance(_file_type, Unset):
            file_type = UNSET
        else:
            file_type = FileType(_file_type)

        _filter_params = d.pop("filter_params", UNSET)
        filter_params: Union[Unset, FilterParams]
        if isinstance(_filter_params, Unset):
            filter_params = UNSET
        else:
            filter_params = FilterParams.from_dict(_filter_params)

        include_text_sample = d.pop("include_text_sample", UNSET)

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

        def _parse_num_samples(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        num_samples = _parse_num_samples(d.pop("num_samples", UNSET))

        only_meta_cols = d.pop("only_meta_cols", UNSET)

        def _parse_task(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        task = _parse_task(d.pop("task", UNSET))

        def _parse_text_sample_length(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        text_sample_length = _parse_text_sample_length(d.pop("text_sample_length", UNSET))

        use_seed = d.pop("use_seed", UNSET)

        embedding_request = cls(
            compare_to=compare_to,
            file_type=file_type,
            filter_params=filter_params,
            include_text_sample=include_text_sample,
            map_threshold=map_threshold,
            meta_cols=meta_cols,
            num_samples=num_samples,
            only_meta_cols=only_meta_cols,
            task=task,
            text_sample_length=text_sample_length,
            use_seed=use_seed,
        )

        embedding_request.additional_properties = d
        return embedding_request

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
