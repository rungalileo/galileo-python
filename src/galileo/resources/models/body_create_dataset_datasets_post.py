from collections.abc import Mapping
from io import BytesIO
from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from .. import types
from ..types import UNSET, File, Unset

T = TypeVar("T", bound="BodyCreateDatasetDatasetsPost")


@_attrs_define
class BodyCreateDatasetDatasetsPost:
    """
    Attributes:
        copy_from_dataset_id (Union[None, Unset, str]):
        copy_from_dataset_version_index (Union[None, Unset, int]):
        draft (Union[Unset, bool]):  Default: False.
        file (Union[File, None, Unset]):
        hidden (Union[Unset, bool]):  Default: False.
        name (Union[None, Unset, str]):
    """

    copy_from_dataset_id: Union[None, Unset, str] = UNSET
    copy_from_dataset_version_index: Union[None, Unset, int] = UNSET
    draft: Union[Unset, bool] = False
    file: Union[File, None, Unset] = UNSET
    hidden: Union[Unset, bool] = False
    name: Union[None, Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        copy_from_dataset_id: Union[None, Unset, str]
        if isinstance(self.copy_from_dataset_id, Unset):
            copy_from_dataset_id = UNSET
        else:
            copy_from_dataset_id = self.copy_from_dataset_id

        copy_from_dataset_version_index: Union[None, Unset, int]
        if isinstance(self.copy_from_dataset_version_index, Unset):
            copy_from_dataset_version_index = UNSET
        else:
            copy_from_dataset_version_index = self.copy_from_dataset_version_index

        draft = self.draft

        file: Union[None, Unset, types.FileTypes]
        if isinstance(self.file, Unset):
            file = UNSET
        elif isinstance(self.file, File):
            file = self.file.to_tuple()

        else:
            file = self.file

        hidden = self.hidden

        name: Union[None, Unset, str]
        if isinstance(self.name, Unset):
            name = UNSET
        else:
            name = self.name

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if copy_from_dataset_id is not UNSET:
            field_dict["copy_from_dataset_id"] = copy_from_dataset_id
        if copy_from_dataset_version_index is not UNSET:
            field_dict["copy_from_dataset_version_index"] = copy_from_dataset_version_index
        if draft is not UNSET:
            field_dict["draft"] = draft
        if file is not UNSET:
            field_dict["file"] = file
        if hidden is not UNSET:
            field_dict["hidden"] = hidden
        if name is not UNSET:
            field_dict["name"] = name

        return field_dict

    def to_multipart(self) -> types.RequestFiles:
        files: types.RequestFiles = []

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

        if not isinstance(self.draft, Unset):
            files.append(("draft", (None, str(self.draft).encode(), "text/plain")))

        if not isinstance(self.file, Unset):
            if isinstance(self.file, File):
                files.append(("file", self.file.to_tuple()))
            else:
                files.append(("file", (None, str(self.file).encode(), "text/plain")))

        if not isinstance(self.hidden, Unset):
            files.append(("hidden", (None, str(self.hidden).encode(), "text/plain")))

        if not isinstance(self.name, Unset):
            if isinstance(self.name, str):
                files.append(("name", (None, str(self.name).encode(), "text/plain")))
            else:
                files.append(("name", (None, str(self.name).encode(), "text/plain")))

        for prop_name, prop in self.additional_properties.items():
            files.append((prop_name, (None, str(prop).encode(), "text/plain")))

        return files

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)

        def _parse_copy_from_dataset_id(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        copy_from_dataset_id = _parse_copy_from_dataset_id(d.pop("copy_from_dataset_id", UNSET))

        def _parse_copy_from_dataset_version_index(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        copy_from_dataset_version_index = _parse_copy_from_dataset_version_index(
            d.pop("copy_from_dataset_version_index", UNSET)
        )

        draft = d.pop("draft", UNSET)

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

        hidden = d.pop("hidden", UNSET)

        def _parse_name(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        name = _parse_name(d.pop("name", UNSET))

        body_create_dataset_datasets_post = cls(
            copy_from_dataset_id=copy_from_dataset_id,
            copy_from_dataset_version_index=copy_from_dataset_version_index,
            draft=draft,
            file=file,
            hidden=hidden,
            name=name,
        )

        body_create_dataset_datasets_post.additional_properties = d
        return body_create_dataset_datasets_post

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
