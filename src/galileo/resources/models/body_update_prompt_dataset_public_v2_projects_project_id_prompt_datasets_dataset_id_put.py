from __future__ import annotations

from collections.abc import Mapping
from io import BytesIO
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from .. import types
from ..types import UNSET, File, FileTypes, Unset

T = TypeVar("T", bound="BodyUpdatePromptDatasetPublicV2ProjectsProjectIdPromptDatasetsDatasetIdPut")


@_attrs_define
class BodyUpdatePromptDatasetPublicV2ProjectsProjectIdPromptDatasetsDatasetIdPut:
    """
    Attributes:
        file (File | None | Unset):
        column_names (list[str] | None | Unset):
    """

    file: File | None | Unset = UNSET
    column_names: list[str] | None | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        file: FileTypes | None | Unset
        if isinstance(self.file, Unset):
            file = UNSET
        elif isinstance(self.file, File):
            file = self.file.to_tuple()

        else:
            file = self.file

        column_names: list[str] | None | Unset
        if isinstance(self.column_names, Unset):
            column_names = UNSET
        elif isinstance(self.column_names, list):
            column_names = self.column_names

        else:
            column_names = self.column_names

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if file is not UNSET:
            field_dict["file"] = file
        if column_names is not UNSET:
            field_dict["column_names"] = column_names

        return field_dict

    def to_multipart(self) -> types.RequestFiles:
        files: types.RequestFiles = []

        if not isinstance(self.file, Unset):
            if isinstance(self.file, File):
                files.append(("file", self.file.to_tuple()))
            else:
                files.append(("file", (None, str(self.file).encode(), "text/plain")))

        if not isinstance(self.column_names, Unset):
            if isinstance(self.column_names, list):
                for column_names_type_0_item_element in self.column_names:
                    files.append(("column_names", (None, str(column_names_type_0_item_element).encode(), "text/plain")))
            else:
                files.append(("column_names", (None, str(self.column_names).encode(), "text/plain")))

        for prop_name, prop in self.additional_properties.items():
            files.append((prop_name, (None, str(prop).encode(), "text/plain")))

        return files

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)

        def _parse_file(data: object) -> File | None | Unset:
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
            return cast(File | None | Unset, data)

        file = _parse_file(d.pop("file", UNSET))

        def _parse_column_names(data: object) -> list[str] | None | Unset:
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
            return cast(list[str] | None | Unset, data)

        column_names = _parse_column_names(d.pop("column_names", UNSET))

        body_update_prompt_dataset_public_v2_projects_project_id_prompt_datasets_dataset_id_put = cls(
            file=file, column_names=column_names
        )

        body_update_prompt_dataset_public_v2_projects_project_id_prompt_datasets_dataset_id_put.additional_properties = d
        return body_update_prompt_dataset_public_v2_projects_project_id_prompt_datasets_dataset_id_put

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
