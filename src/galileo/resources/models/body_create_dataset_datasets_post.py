from io import BytesIO
from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, File, FileJsonType, Unset

T = TypeVar("T", bound="BodyCreateDatasetDatasetsPost")


@_attrs_define
class BodyCreateDatasetDatasetsPost:
    """
    Attributes:
        draft (Union[Unset, bool]):  Default: False.
        file (Union[File, None, Unset]):
        name (Union[None, Unset, str]):
    """

    draft: Union[Unset, bool] = False
    file: Union[File, None, Unset] = UNSET
    name: Union[None, Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        draft = self.draft

        file: Union[FileJsonType, None, Unset]
        if isinstance(self.file, Unset):
            file = UNSET
        elif isinstance(self.file, File):
            file = self.file.to_tuple()

        else:
            file = self.file

        name: Union[None, Unset, str]
        if isinstance(self.name, Unset):
            name = UNSET
        else:
            name = self.name

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if draft is not UNSET:
            field_dict["draft"] = draft
        if file is not UNSET:
            field_dict["file"] = file
        if name is not UNSET:
            field_dict["name"] = name

        return field_dict

    def to_multipart(self) -> dict[str, Any]:
        draft = self.draft if isinstance(self.draft, Unset) else (None, str(self.draft).encode(), "text/plain")

        file: Union[Unset, tuple[None, bytes, str]]

        if isinstance(self.file, Unset):
            file = UNSET
        elif isinstance(self.file, File):
            file = self.file.to_tuple()
        else:
            file = (None, str(self.file).encode(), "text/plain")

        name: Union[Unset, tuple[None, bytes, str]]

        if isinstance(self.name, Unset):
            name = UNSET
        elif isinstance(self.name, str):
            name = (None, str(self.name).encode(), "text/plain")
        else:
            name = (None, str(self.name).encode(), "text/plain")

        field_dict: dict[str, Any] = {}
        for prop_name, prop in self.additional_properties.items():
            field_dict[prop_name] = (None, str(prop).encode(), "text/plain")

        field_dict.update({})
        if draft is not UNSET:
            field_dict["draft"] = draft
        if file is not UNSET:
            field_dict["file"] = file
        if name is not UNSET:
            field_dict["name"] = name

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
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

        def _parse_name(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        name = _parse_name(d.pop("name", UNSET))

        body_create_dataset_datasets_post = cls(draft=draft, file=file, name=name)

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
