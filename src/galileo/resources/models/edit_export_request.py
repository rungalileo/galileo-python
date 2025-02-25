from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.file_type import FileType
from ..models.split import Split
from ..models.tagging_schema import TaggingSchema
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.edit_export_request_col_mapping_type_0 import EditExportRequestColMappingType0
    from ..models.edit_override import EditOverride
    from ..models.filter_params import FilterParams


T = TypeVar("T", bound="EditExportRequest")


@_attrs_define
class EditExportRequest:
    """
    Attributes:
        edit_ids (list[str]):
        all_but (Union[Unset, bool]):  Default: False.
        col_mapping (Union['EditExportRequestColMappingType0', None, Unset]):  Default: None.
        compare_to (Union[None, Split, Unset]):
        edit_overrides (Union[None, Unset, list['EditOverride']]):
        file_type (Union[Unset, FileType]):
        filter_params (Union[Unset, FilterParams]):
        hf_format (Union[Unset, bool]):  Default: False.
        include_cols (Union[None, Unset, list[str]]):
        map_threshold (Union[Unset, float]):  Default: 0.5.
        min_reviews (Union[None, Unset, int]):
        only_export_edited (Union[None, Unset, bool]):  Default: False.
        tagging_schema (Union[None, TaggingSchema, Unset]):
        task (Union[None, Unset, str]):
    """

    edit_ids: list[str]
    all_but: Union[Unset, bool] = False
    col_mapping: Union["EditExportRequestColMappingType0", None, Unset] = None
    compare_to: Union[None, Split, Unset] = UNSET
    edit_overrides: Union[None, Unset, list["EditOverride"]] = UNSET
    file_type: Union[Unset, FileType] = UNSET
    filter_params: Union[Unset, "FilterParams"] = UNSET
    hf_format: Union[Unset, bool] = False
    include_cols: Union[None, Unset, list[str]] = UNSET
    map_threshold: Union[Unset, float] = 0.5
    min_reviews: Union[None, Unset, int] = UNSET
    only_export_edited: Union[None, Unset, bool] = False
    tagging_schema: Union[None, TaggingSchema, Unset] = UNSET
    task: Union[None, Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.edit_export_request_col_mapping_type_0 import EditExportRequestColMappingType0

        edit_ids = self.edit_ids

        all_but = self.all_but

        col_mapping: Union[None, Unset, dict[str, Any]]
        if isinstance(self.col_mapping, Unset):
            col_mapping = UNSET
        elif isinstance(self.col_mapping, EditExportRequestColMappingType0):
            col_mapping = self.col_mapping.to_dict()
        else:
            col_mapping = self.col_mapping

        compare_to: Union[None, Unset, str]
        if isinstance(self.compare_to, Unset):
            compare_to = UNSET
        elif isinstance(self.compare_to, Split):
            compare_to = self.compare_to.value
        else:
            compare_to = self.compare_to

        edit_overrides: Union[None, Unset, list[dict[str, Any]]]
        if isinstance(self.edit_overrides, Unset):
            edit_overrides = UNSET
        elif isinstance(self.edit_overrides, list):
            edit_overrides = []
            for edit_overrides_type_0_item_data in self.edit_overrides:
                edit_overrides_type_0_item = edit_overrides_type_0_item_data.to_dict()
                edit_overrides.append(edit_overrides_type_0_item)

        else:
            edit_overrides = self.edit_overrides

        file_type: Union[Unset, str] = UNSET
        if not isinstance(self.file_type, Unset):
            file_type = self.file_type.value

        filter_params: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.filter_params, Unset):
            filter_params = self.filter_params.to_dict()

        hf_format = self.hf_format

        include_cols: Union[None, Unset, list[str]]
        if isinstance(self.include_cols, Unset):
            include_cols = UNSET
        elif isinstance(self.include_cols, list):
            include_cols = self.include_cols

        else:
            include_cols = self.include_cols

        map_threshold = self.map_threshold

        min_reviews: Union[None, Unset, int]
        if isinstance(self.min_reviews, Unset):
            min_reviews = UNSET
        else:
            min_reviews = self.min_reviews

        only_export_edited: Union[None, Unset, bool]
        if isinstance(self.only_export_edited, Unset):
            only_export_edited = UNSET
        else:
            only_export_edited = self.only_export_edited

        tagging_schema: Union[None, Unset, str]
        if isinstance(self.tagging_schema, Unset):
            tagging_schema = UNSET
        elif isinstance(self.tagging_schema, TaggingSchema):
            tagging_schema = self.tagging_schema.value
        else:
            tagging_schema = self.tagging_schema

        task: Union[None, Unset, str]
        if isinstance(self.task, Unset):
            task = UNSET
        else:
            task = self.task

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({"edit_ids": edit_ids})
        if all_but is not UNSET:
            field_dict["all_but"] = all_but
        if col_mapping is not UNSET:
            field_dict["col_mapping"] = col_mapping
        if compare_to is not UNSET:
            field_dict["compare_to"] = compare_to
        if edit_overrides is not UNSET:
            field_dict["edit_overrides"] = edit_overrides
        if file_type is not UNSET:
            field_dict["file_type"] = file_type
        if filter_params is not UNSET:
            field_dict["filter_params"] = filter_params
        if hf_format is not UNSET:
            field_dict["hf_format"] = hf_format
        if include_cols is not UNSET:
            field_dict["include_cols"] = include_cols
        if map_threshold is not UNSET:
            field_dict["map_threshold"] = map_threshold
        if min_reviews is not UNSET:
            field_dict["min_reviews"] = min_reviews
        if only_export_edited is not UNSET:
            field_dict["only_export_edited"] = only_export_edited
        if tagging_schema is not UNSET:
            field_dict["tagging_schema"] = tagging_schema
        if task is not UNSET:
            field_dict["task"] = task

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.edit_export_request_col_mapping_type_0 import EditExportRequestColMappingType0
        from ..models.edit_override import EditOverride
        from ..models.filter_params import FilterParams

        d = src_dict.copy()
        edit_ids = cast(list[str], d.pop("edit_ids"))

        all_but = d.pop("all_but", UNSET)

        def _parse_col_mapping(data: object) -> Union["EditExportRequestColMappingType0", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                col_mapping_type_0 = EditExportRequestColMappingType0.from_dict(data)

                return col_mapping_type_0
            except:  # noqa: E722
                pass
            return cast(Union["EditExportRequestColMappingType0", None, Unset], data)

        col_mapping = _parse_col_mapping(d.pop("col_mapping", UNSET))

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

        def _parse_edit_overrides(data: object) -> Union[None, Unset, list["EditOverride"]]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                edit_overrides_type_0 = []
                _edit_overrides_type_0 = data
                for edit_overrides_type_0_item_data in _edit_overrides_type_0:
                    edit_overrides_type_0_item = EditOverride.from_dict(edit_overrides_type_0_item_data)

                    edit_overrides_type_0.append(edit_overrides_type_0_item)

                return edit_overrides_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, list["EditOverride"]], data)

        edit_overrides = _parse_edit_overrides(d.pop("edit_overrides", UNSET))

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

        hf_format = d.pop("hf_format", UNSET)

        def _parse_include_cols(data: object) -> Union[None, Unset, list[str]]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                include_cols_type_0 = cast(list[str], data)

                return include_cols_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, list[str]], data)

        include_cols = _parse_include_cols(d.pop("include_cols", UNSET))

        map_threshold = d.pop("map_threshold", UNSET)

        def _parse_min_reviews(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        min_reviews = _parse_min_reviews(d.pop("min_reviews", UNSET))

        def _parse_only_export_edited(data: object) -> Union[None, Unset, bool]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, bool], data)

        only_export_edited = _parse_only_export_edited(d.pop("only_export_edited", UNSET))

        def _parse_tagging_schema(data: object) -> Union[None, TaggingSchema, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                tagging_schema_type_0 = TaggingSchema(data)

                return tagging_schema_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, TaggingSchema, Unset], data)

        tagging_schema = _parse_tagging_schema(d.pop("tagging_schema", UNSET))

        def _parse_task(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        task = _parse_task(d.pop("task", UNSET))

        edit_export_request = cls(
            edit_ids=edit_ids,
            all_but=all_but,
            col_mapping=col_mapping,
            compare_to=compare_to,
            edit_overrides=edit_overrides,
            file_type=file_type,
            filter_params=filter_params,
            hf_format=hf_format,
            include_cols=include_cols,
            map_threshold=map_threshold,
            min_reviews=min_reviews,
            only_export_edited=only_export_edited,
            tagging_schema=tagging_schema,
            task=task,
        )

        edit_export_request.additional_properties = d
        return edit_export_request

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
