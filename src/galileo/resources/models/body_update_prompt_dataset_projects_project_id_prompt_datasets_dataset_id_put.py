from collections.abc import Mapping
from io import BytesIO
from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from .. import types
from ..types import UNSET, File, FileTypes, Unset

T = TypeVar("T", bound="BodyUpdatePromptDatasetProjectsProjectIdPromptDatasetsDatasetIdPut")


@_attrs_define
class BodyUpdatePromptDatasetProjectsProjectIdPromptDatasetsDatasetIdPut:
    """
    Attributes:
        column_names (Union[None, Unset, list[str]]):
        file (Union[File, None, Unset]):
    """

    column_names: Union[None, Unset, list[str]] = UNSET
    file: Union[File, None, Unset] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        column_names: Union[None, Unset, list[str]]
        if isinstance(self.column_names, Unset):
            column_names = UNSET
        elif isinstance(self.column_names, list):
            column_names = self.column_names

        else:
            column_names = self.column_names

        file: Union[FileTypes, None, Unset]
        if isinstance(self.file, Unset):
            file = UNSET
        elif isinstance(self.file, File):
            file = self.file.to_tuple()

        else:
            file = self.file

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if column_names is not UNSET:
            field_dict["column_names"] = column_names
        if file is not UNSET:
            field_dict["file"] = file

        return field_dict

    def to_multipart(self) -> types.RequestFiles:
        files: types.RequestFiles = []

        if not isinstance(self.column_names, Unset):
            if isinstance(self.column_names, list):
                for column_names_type_0_item_element in self.column_names:
                    files.append(("column_names", (None, str(column_names_type_0_item_element).encode(), "text/plain")))
            else:
                files.append(("column_names", (None, str(self.column_names).encode(), "text/plain")))

        if not isinstance(self.file, Unset):
            if isinstance(self.file, File):
                files.append(("file", self.file.to_tuple()))
            else:
                files.append(("file", (None, str(self.file).encode(), "text/plain")))

        for prop_name, prop in self.additional_properties.items():
            files.append((prop_name, (None, str(prop).encode(), "text/plain")))

        return files

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)

        def _parse_column_names(data: object) -> Union[None, Unset, list[str]]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                column_names_type_0 = cast(list[str], data)

                return column_names_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, list[str]], data)

        column_names = _parse_column_names(d.pop("column_names", UNSET))

        def _parse_file(data: object) -> Union[File, None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, bytes):
                    raise TypeError()
                file_type_0 = File(payload=BytesIO(data))

                return file_type_0
            except:  # noqa: E722
                pass
            return cast(Union[File, None, Unset], data)

        file = _parse_file(d.pop("file", UNSET))

        body_update_prompt_dataset_projects_project_id_prompt_datasets_dataset_id_put = cls(
            column_names=column_names, file=file
        )

        body_update_prompt_dataset_projects_project_id_prompt_datasets_dataset_id_put.additional_properties = d
        return body_update_prompt_dataset_projects_project_id_prompt_datasets_dataset_id_put

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
