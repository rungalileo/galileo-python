from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.file_type import FileType
from ..models.split import Split
from ..models.tagging_schema import TaggingSchema
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.databricks_export_request_col_mapping_type_0 import DatabricksExportRequestColMappingType0
    from ..models.filter_params import FilterParams


T = TypeVar("T", bound="DatabricksExportRequest")


@_attrs_define
class DatabricksExportRequest:
    """Schema for exporting a dataframe to a Delta table.

    Attributes
    ----------
        database_name (str):
        table_name (str):
        project_id (str):
        run_id (str):
        split (Split):
        catalog_name (Union[None, Unset, str]):
        task (Union[None, Unset, str]):
        filter_params (Union[Unset, FilterParams]):
        compare_to (Union[None, Split, Unset]):
        map_threshold (Union[Unset, float]):  Default: 0.5.
        all_but (Union[Unset, bool]):  Default: False.
        file_type (Union[Unset, FileType]):
        include_cols (Union[None, Unset, list[str]]):
        col_mapping (Union['DatabricksExportRequestColMappingType0', None, Unset]):
        hf_format (Union[Unset, bool]):  Default: False.
        tagging_schema (Union[None, TaggingSchema, Unset]):
        inference_name (Union[None, Unset, str]):
    """

    database_name: str
    table_name: str
    project_id: str
    run_id: str
    split: Split
    catalog_name: Union[None, Unset, str] = UNSET
    task: Union[None, Unset, str] = UNSET
    filter_params: Union[Unset, "FilterParams"] = UNSET
    compare_to: Union[None, Split, Unset] = UNSET
    map_threshold: Union[Unset, float] = 0.5
    all_but: Union[Unset, bool] = False
    file_type: Union[Unset, FileType] = UNSET
    include_cols: Union[None, Unset, list[str]] = UNSET
    col_mapping: Union["DatabricksExportRequestColMappingType0", None, Unset] = UNSET
    hf_format: Union[Unset, bool] = False
    tagging_schema: Union[None, TaggingSchema, Unset] = UNSET
    inference_name: Union[None, Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.databricks_export_request_col_mapping_type_0 import DatabricksExportRequestColMappingType0

        database_name = self.database_name

        table_name = self.table_name

        project_id = self.project_id

        run_id = self.run_id

        split = self.split.value

        catalog_name: Union[None, Unset, str]
        catalog_name = UNSET if isinstance(self.catalog_name, Unset) else self.catalog_name

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
        elif isinstance(self.col_mapping, DatabricksExportRequestColMappingType0):
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

        inference_name: Union[None, Unset, str]
        inference_name = UNSET if isinstance(self.inference_name, Unset) else self.inference_name

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "database_name": database_name,
                "table_name": table_name,
                "project_id": project_id,
                "run_id": run_id,
                "split": split,
            }
        )
        if catalog_name is not UNSET:
            field_dict["catalog_name"] = catalog_name
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
        if inference_name is not UNSET:
            field_dict["inference_name"] = inference_name

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.databricks_export_request_col_mapping_type_0 import DatabricksExportRequestColMappingType0
        from ..models.filter_params import FilterParams

        d = dict(src_dict)
        database_name = d.pop("database_name")

        table_name = d.pop("table_name")

        project_id = d.pop("project_id")

        run_id = d.pop("run_id")

        split = Split(d.pop("split"))

        def _parse_catalog_name(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        catalog_name = _parse_catalog_name(d.pop("catalog_name", UNSET))

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

        def _parse_col_mapping(data: object) -> Union["DatabricksExportRequestColMappingType0", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                return DatabricksExportRequestColMappingType0.from_dict(data)

            except:  # noqa: E722
                pass
            return cast(Union["DatabricksExportRequestColMappingType0", None, Unset], data)

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

        def _parse_inference_name(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        inference_name = _parse_inference_name(d.pop("inference_name", UNSET))

        databricks_export_request = cls(
            database_name=database_name,
            table_name=table_name,
            project_id=project_id,
            run_id=run_id,
            split=split,
            catalog_name=catalog_name,
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
            inference_name=inference_name,
        )

        databricks_export_request.additional_properties = d
        return databricks_export_request

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
