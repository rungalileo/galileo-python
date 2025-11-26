from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.file_type import FileType
from ..models.split import Split
from ..models.tagging_schema import TaggingSchema
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.databricks_unity_catalog_export_edits_response_col_mapping_type_0 import (
        DatabricksUnityCatalogExportEditsResponseColMappingType0,
    )
    from ..models.edit_override import EditOverride
    from ..models.filter_params import FilterParams


T = TypeVar("T", bound="DatabricksUnityCatalogExportEditsResponse")


@_attrs_define
class DatabricksUnityCatalogExportEditsResponse:
    """
    Attributes
    ----------
        edit_ids (list[str]):
        results (list[Any]):
        task (Union[None, Unset, str]):
        filter_params (Union[Unset, FilterParams]):
        compare_to (Union[None, Split, Unset]):
        map_threshold (Union[Unset, float]):  Default: 0.5.
        all_but (Union[Unset, bool]):  Default: False.
        file_type (Union[Unset, FileType]):
        include_cols (Union[None, Unset, list[str]]):
        col_mapping (Union['DatabricksUnityCatalogExportEditsResponseColMappingType0', None, Unset]):
        hf_format (Union[Unset, bool]):  Default: False.
        tagging_schema (Union[None, TaggingSchema, Unset]):
        edit_overrides (Union[None, Unset, list['EditOverride']]):
        only_export_edited (Union[None, Unset, bool]):  Default: False.
        min_reviews (Union[None, Unset, int]):
    """

    edit_ids: list[str]
    results: list[Any]
    task: Union[None, Unset, str] = UNSET
    filter_params: Union[Unset, "FilterParams"] = UNSET
    compare_to: Union[None, Split, Unset] = UNSET
    map_threshold: Union[Unset, float] = 0.5
    all_but: Union[Unset, bool] = False
    file_type: Union[Unset, FileType] = UNSET
    include_cols: Union[None, Unset, list[str]] = UNSET
    col_mapping: Union["DatabricksUnityCatalogExportEditsResponseColMappingType0", None, Unset] = UNSET
    hf_format: Union[Unset, bool] = False
    tagging_schema: Union[None, TaggingSchema, Unset] = UNSET
    edit_overrides: Union[None, Unset, list["EditOverride"]] = UNSET
    only_export_edited: Union[None, Unset, bool] = False
    min_reviews: Union[None, Unset, int] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.databricks_unity_catalog_export_edits_response_col_mapping_type_0 import (
            DatabricksUnityCatalogExportEditsResponseColMappingType0,
        )

        edit_ids = self.edit_ids

        results = self.results

        task: Union[None, Unset, str]
        task = UNSET if isinstance(self.task, Unset) else self.task

        filter_params: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.filter_params, Unset):
            filter_params = self.filter_params.to_dict()

        compare_to: Union[None, Unset, str]
        if isinstance(self.compare_to, Unset):
            compare_to = UNSET
        elif isinstance(self.compare_to, Split):
            compare_to = self.compare_to.value
        else:
            compare_to = self.compare_to

        map_threshold = self.map_threshold

        all_but = self.all_but

        file_type: Union[Unset, str] = UNSET
        if not isinstance(self.file_type, Unset):
            file_type = self.file_type.value

        include_cols: Union[None, Unset, list[str]]
        if isinstance(self.include_cols, Unset):
            include_cols = UNSET
        elif isinstance(self.include_cols, list):
            include_cols = self.include_cols

        else:
            include_cols = self.include_cols

        col_mapping: Union[None, Unset, dict[str, Any]]
        if isinstance(self.col_mapping, Unset):
            col_mapping = UNSET
        elif isinstance(self.col_mapping, DatabricksUnityCatalogExportEditsResponseColMappingType0):
            col_mapping = self.col_mapping.to_dict()
        else:
            col_mapping = self.col_mapping

        hf_format = self.hf_format

        tagging_schema: Union[None, Unset, str]
        if isinstance(self.tagging_schema, Unset):
            tagging_schema = UNSET
        elif isinstance(self.tagging_schema, TaggingSchema):
            tagging_schema = self.tagging_schema.value
        else:
            tagging_schema = self.tagging_schema

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

        only_export_edited: Union[None, Unset, bool]
        only_export_edited = UNSET if isinstance(self.only_export_edited, Unset) else self.only_export_edited

        min_reviews: Union[None, Unset, int]
        min_reviews = UNSET if isinstance(self.min_reviews, Unset) else self.min_reviews

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({"edit_ids": edit_ids, "results": results})
        if task is not UNSET:
            field_dict["task"] = task
        if filter_params is not UNSET:
            field_dict["filter_params"] = filter_params
        if compare_to is not UNSET:
            field_dict["compare_to"] = compare_to
        if map_threshold is not UNSET:
            field_dict["map_threshold"] = map_threshold
        if all_but is not UNSET:
            field_dict["all_but"] = all_but
        if file_type is not UNSET:
            field_dict["file_type"] = file_type
        if include_cols is not UNSET:
            field_dict["include_cols"] = include_cols
        if col_mapping is not UNSET:
            field_dict["col_mapping"] = col_mapping
        if hf_format is not UNSET:
            field_dict["hf_format"] = hf_format
        if tagging_schema is not UNSET:
            field_dict["tagging_schema"] = tagging_schema
        if edit_overrides is not UNSET:
            field_dict["edit_overrides"] = edit_overrides
        if only_export_edited is not UNSET:
            field_dict["only_export_edited"] = only_export_edited
        if min_reviews is not UNSET:
            field_dict["min_reviews"] = min_reviews

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.databricks_unity_catalog_export_edits_response_col_mapping_type_0 import (
            DatabricksUnityCatalogExportEditsResponseColMappingType0,
        )
        from ..models.edit_override import EditOverride
        from ..models.filter_params import FilterParams

        d = dict(src_dict)
        edit_ids = cast(list[str], d.pop("edit_ids"))

        results = cast(list[Any], d.pop("results"))

        def _parse_task(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        task = _parse_task(d.pop("task", UNSET))

        _filter_params = d.pop("filter_params", UNSET)
        filter_params: Union[Unset, FilterParams]
        filter_params = UNSET if isinstance(_filter_params, Unset) else FilterParams.from_dict(_filter_params)

        def _parse_compare_to(data: object) -> Union[None, Split, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                return Split(data)

            except:  # noqa: E722
                pass
            return cast(Union[None, Split, Unset], data)

        compare_to = _parse_compare_to(d.pop("compare_to", UNSET))

        map_threshold = d.pop("map_threshold", UNSET)

        all_but = d.pop("all_but", UNSET)

        _file_type = d.pop("file_type", UNSET)
        file_type: Union[Unset, FileType]
        file_type = UNSET if isinstance(_file_type, Unset) else FileType(_file_type)

        def _parse_include_cols(data: object) -> Union[None, Unset, list[str]]:
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

        include_cols = _parse_include_cols(d.pop("include_cols", UNSET))

        def _parse_col_mapping(
            data: object,
        ) -> Union["DatabricksUnityCatalogExportEditsResponseColMappingType0", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                return DatabricksUnityCatalogExportEditsResponseColMappingType0.from_dict(data)

            except:  # noqa: E722
                pass
            return cast(Union["DatabricksUnityCatalogExportEditsResponseColMappingType0", None, Unset], data)

        col_mapping = _parse_col_mapping(d.pop("col_mapping", UNSET))

        hf_format = d.pop("hf_format", UNSET)

        def _parse_tagging_schema(data: object) -> Union[None, TaggingSchema, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                return TaggingSchema(data)

            except:  # noqa: E722
                pass
            return cast(Union[None, TaggingSchema, Unset], data)

        tagging_schema = _parse_tagging_schema(d.pop("tagging_schema", UNSET))

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

        def _parse_only_export_edited(data: object) -> Union[None, Unset, bool]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, bool], data)

        only_export_edited = _parse_only_export_edited(d.pop("only_export_edited", UNSET))

        def _parse_min_reviews(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        min_reviews = _parse_min_reviews(d.pop("min_reviews", UNSET))

        databricks_unity_catalog_export_edits_response = cls(
            edit_ids=edit_ids,
            results=results,
            task=task,
            filter_params=filter_params,
            compare_to=compare_to,
            map_threshold=map_threshold,
            all_but=all_but,
            file_type=file_type,
            include_cols=include_cols,
            col_mapping=col_mapping,
            hf_format=hf_format,
            tagging_schema=tagging_schema,
            edit_overrides=edit_overrides,
            only_export_edited=only_export_edited,
            min_reviews=min_reviews,
        )

        databricks_unity_catalog_export_edits_response.additional_properties = d
        return databricks_unity_catalog_export_edits_response

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
