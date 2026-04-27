from __future__ import annotations

from collections.abc import Mapping
from io import BytesIO
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from .. import types
from ..types import UNSET, File, FileTypes, Unset

T = TypeVar("T", bound="BodyCreateDatasetPublicV2DatasetsPost")


@_attrs_define
class BodyCreateDatasetPublicV2DatasetsPost:
    """
    Attributes:
        draft (bool | Unset):  Default: False.
        hidden (bool | Unset):  Default: False.
        name (None | str | Unset):
        append_suffix_if_duplicate (bool | Unset):  Default: False.
        file (File | None | Unset):
        copy_from_dataset_id (None | str | Unset):
        copy_from_dataset_version_index (int | None | Unset):
        project_id (None | str | Unset):
    """

    draft: bool | Unset = False
    hidden: bool | Unset = False
    name: None | str | Unset = UNSET
    append_suffix_if_duplicate: bool | Unset = False
    file: File | None | Unset = UNSET
    copy_from_dataset_id: None | str | Unset = UNSET
    copy_from_dataset_version_index: int | None | Unset = UNSET
    project_id: None | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        draft = self.draft

        hidden = self.hidden

        name: None | str | Unset
        if isinstance(self.name, Unset):
            name = UNSET
        else:
            name = self.name

        append_suffix_if_duplicate = self.append_suffix_if_duplicate

        file: FileTypes | None | Unset
        if isinstance(self.file, Unset):
            file = UNSET
        elif isinstance(self.file, File):
            file = self.file.to_tuple()

        else:
            file = self.file

        copy_from_dataset_id: None | str | Unset
        if isinstance(self.copy_from_dataset_id, Unset):
            copy_from_dataset_id = UNSET
        else:
            copy_from_dataset_id = self.copy_from_dataset_id

        copy_from_dataset_version_index: int | None | Unset
        if isinstance(self.copy_from_dataset_version_index, Unset):
            copy_from_dataset_version_index = UNSET
        else:
            copy_from_dataset_version_index = self.copy_from_dataset_version_index

        project_id: None | str | Unset
        if isinstance(self.project_id, Unset):
            project_id = UNSET
        else:
            project_id = self.project_id

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if draft is not UNSET:
            field_dict["draft"] = draft
        if hidden is not UNSET:
            field_dict["hidden"] = hidden
        if name is not UNSET:
            field_dict["name"] = name
        if append_suffix_if_duplicate is not UNSET:
            field_dict["append_suffix_if_duplicate"] = append_suffix_if_duplicate
        if file is not UNSET:
            field_dict["file"] = file
        if copy_from_dataset_id is not UNSET:
            field_dict["copy_from_dataset_id"] = copy_from_dataset_id
        if copy_from_dataset_version_index is not UNSET:
            field_dict["copy_from_dataset_version_index"] = copy_from_dataset_version_index
        if project_id is not UNSET:
            field_dict["project_id"] = project_id

        return field_dict

    def to_multipart(self) -> types.RequestFiles:
        files: types.RequestFiles = []

        if not isinstance(self.draft, Unset):
            files.append(("draft", (None, str(self.draft).encode(), "text/plain")))

        if not isinstance(self.hidden, Unset):
            files.append(("hidden", (None, str(self.hidden).encode(), "text/plain")))

        if not isinstance(self.name, Unset):
            if isinstance(self.name, str):
                files.append(("name", (None, str(self.name).encode(), "text/plain")))
            else:
                files.append(("name", (None, str(self.name).encode(), "text/plain")))

        if not isinstance(self.append_suffix_if_duplicate, Unset):
            files.append(
                ("append_suffix_if_duplicate", (None, str(self.append_suffix_if_duplicate).encode(), "text/plain"))
            )

        if not isinstance(self.file, Unset):
            if isinstance(self.file, File):
                files.append(("file", self.file.to_tuple()))
            else:
                files.append(("file", (None, str(self.file).encode(), "text/plain")))

        if not isinstance(self.copy_from_dataset_id, Unset):
            if isinstance(self.copy_from_dataset_id, str):
                files.append(("copy_from_dataset_id", (None, str(self.copy_from_dataset_id).encode(), "text/plain")))
            else:
                files.append(("copy_from_dataset_id", (None, str(self.copy_from_dataset_id).encode(), "text/plain")))

        if not isinstance(self.copy_from_dataset_version_index, Unset):
            if isinstance(self.copy_from_dataset_version_index, int):
                files.append(
                    (
                        "copy_from_dataset_version_index",
                        (None, str(self.copy_from_dataset_version_index).encode(), "text/plain"),
                    )
                )
            else:
                files.append(
                    (
                        "copy_from_dataset_version_index",
                        (None, str(self.copy_from_dataset_version_index).encode(), "text/plain"),
                    )
                )

        if not isinstance(self.project_id, Unset):
            if isinstance(self.project_id, str):
                files.append(("project_id", (None, str(self.project_id).encode(), "text/plain")))
            else:
                files.append(("project_id", (None, str(self.project_id).encode(), "text/plain")))

        for prop_name, prop in self.additional_properties.items():
            files.append((prop_name, (None, str(prop).encode(), "text/plain")))

        return files

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        draft = d.pop("draft", UNSET)

        hidden = d.pop("hidden", UNSET)

        def _parse_name(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        name = _parse_name(d.pop("name", UNSET))

        append_suffix_if_duplicate = d.pop("append_suffix_if_duplicate", UNSET)

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

        def _parse_copy_from_dataset_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        copy_from_dataset_id = _parse_copy_from_dataset_id(d.pop("copy_from_dataset_id", UNSET))

        def _parse_copy_from_dataset_version_index(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        copy_from_dataset_version_index = _parse_copy_from_dataset_version_index(
            d.pop("copy_from_dataset_version_index", UNSET)
        )

        def _parse_project_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        project_id = _parse_project_id(d.pop("project_id", UNSET))

        body_create_dataset_public_v2_datasets_post = cls(
            draft=draft,
            hidden=hidden,
            name=name,
            append_suffix_if_duplicate=append_suffix_if_duplicate,
            file=file,
            copy_from_dataset_id=copy_from_dataset_id,
            copy_from_dataset_version_index=copy_from_dataset_version_index,
            project_id=project_id,
        )

        body_create_dataset_public_v2_datasets_post.additional_properties = d
        return body_create_dataset_public_v2_datasets_post

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
