from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.file_type import FileType
from ..models.split import Split
from ..models.tagging_schema import TaggingSchema
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.databricks_export_response_col_mapping_type_0 import DatabricksExportResponseColMappingType0
    from ..models.filter_params import FilterParams


T = TypeVar("T", bound="DatabricksExportResponse")


@_attrs_define
class DatabricksExportResponse:
    """
    Attributes:
        database_name (str):
        project_id (str):
        run_id (str):
        split (Split):
        table_name (str):
        all_but (Union[Unset, bool]):  Default: False.
        catalog_name (Union[None, Unset, str]):
        col_mapping (Union['DatabricksExportResponseColMappingType0', None, Unset]):  Default: None.
        compare_to (Union[None, Split, Unset]):
        file_type (Union[Unset, FileType]):
        filter_params (Union[Unset, FilterParams]):
        hf_format (Union[Unset, bool]):  Default: False.
        include_cols (Union[None, Unset, list[str]]):
        inference_name (Union[None, Unset, str]):
        map_threshold (Union[Unset, float]):  Default: 0.5.
        tagging_schema (Union[None, TaggingSchema, Unset]):
        task (Union[None, Unset, str]):
    """

    database_name: str
    project_id: str
    run_id: str
    split: Split
    table_name: str
    all_but: Union[Unset, bool] = False
    catalog_name: Union[None, Unset, str] = UNSET
    col_mapping: Union["DatabricksExportResponseColMappingType0", None, Unset] = None
    compare_to: Union[None, Split, Unset] = UNSET
    file_type: Union[Unset, FileType] = UNSET
    filter_params: Union[Unset, "FilterParams"] = UNSET
    hf_format: Union[Unset, bool] = False
    include_cols: Union[None, Unset, list[str]] = UNSET
    inference_name: Union[None, Unset, str] = UNSET
    map_threshold: Union[Unset, float] = 0.5
    tagging_schema: Union[None, TaggingSchema, Unset] = UNSET
    task: Union[None, Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.databricks_export_response_col_mapping_type_0 import DatabricksExportResponseColMappingType0

        database_name = self.database_name

        project_id = self.project_id

        run_id = self.run_id

        split = self.split.value

        table_name = self.table_name

        all_but = self.all_but

        catalog_name: Union[None, Unset, str]
        if isinstance(self.catalog_name, Unset):
            catalog_name = UNSET
        else:
            catalog_name = self.catalog_name

        col_mapping: Union[None, Unset, dict[str, Any]]
        if isinstance(self.col_mapping, Unset):
            col_mapping = UNSET
        elif isinstance(self.col_mapping, DatabricksExportResponseColMappingType0):
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

        inference_name: Union[None, Unset, str]
        if isinstance(self.inference_name, Unset):
            inference_name = UNSET
        else:
            inference_name = self.inference_name

        map_threshold = self.map_threshold

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
        field_dict.update(
            {
                "database_name": database_name,
                "project_id": project_id,
                "run_id": run_id,
                "split": split,
                "table_name": table_name,
            }
        )
        if all_but is not UNSET:
            field_dict["all_but"] = all_but
        if catalog_name is not UNSET:
            field_dict["catalog_name"] = catalog_name
        if col_mapping is not UNSET:
            field_dict["col_mapping"] = col_mapping
        if compare_to is not UNSET:
            field_dict["compare_to"] = compare_to
        if file_type is not UNSET:
            field_dict["file_type"] = file_type
        if filter_params is not UNSET:
            field_dict["filter_params"] = filter_params
        if hf_format is not UNSET:
            field_dict["hf_format"] = hf_format
        if include_cols is not UNSET:
            field_dict["include_cols"] = include_cols
        if inference_name is not UNSET:
            field_dict["inference_name"] = inference_name
        if map_threshold is not UNSET:
            field_dict["map_threshold"] = map_threshold
        if tagging_schema is not UNSET:
            field_dict["tagging_schema"] = tagging_schema
        if task is not UNSET:
            field_dict["task"] = task

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.databricks_export_response_col_mapping_type_0 import DatabricksExportResponseColMappingType0
        from ..models.filter_params import FilterParams

        d = src_dict.copy()
        database_name = d.pop("database_name")

        project_id = d.pop("project_id")

        run_id = d.pop("run_id")

        split = Split(d.pop("split"))

        table_name = d.pop("table_name")

        all_but = d.pop("all_but", UNSET)

        def _parse_catalog_name(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        catalog_name = _parse_catalog_name(d.pop("catalog_name", UNSET))

        def _parse_col_mapping(data: object) -> Union["DatabricksExportResponseColMappingType0", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                col_mapping_type_0 = DatabricksExportResponseColMappingType0.from_dict(data)

                return col_mapping_type_0
            except:  # noqa: E722
                pass
            return cast(Union["DatabricksExportResponseColMappingType0", None, Unset], data)

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

        def _parse_inference_name(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        inference_name = _parse_inference_name(d.pop("inference_name", UNSET))

        map_threshold = d.pop("map_threshold", UNSET)

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

        databricks_export_response = cls(
            database_name=database_name,
            project_id=project_id,
            run_id=run_id,
            split=split,
            table_name=table_name,
            all_but=all_but,
            catalog_name=catalog_name,
            col_mapping=col_mapping,
            compare_to=compare_to,
            file_type=file_type,
            filter_params=filter_params,
            hf_format=hf_format,
            include_cols=include_cols,
            inference_name=inference_name,
            map_threshold=map_threshold,
            tagging_schema=tagging_schema,
            task=task,
        )

        databricks_export_response.additional_properties = d
        return databricks_export_response

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
