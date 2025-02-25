from io import BytesIO
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import File

T = TypeVar("T", bound="BodyUploadFileProjectsProjectIdUploadFilePost")


@_attrs_define
class BodyUploadFileProjectsProjectIdUploadFilePost:
    """
    Attributes:
        file (File):
        upload_metadata (str):
    """

    file: File
    upload_metadata: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        file = self.file.to_tuple()

        upload_metadata = self.upload_metadata

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({"file": file, "upload_metadata": upload_metadata})

        return field_dict

    def to_multipart(self) -> dict[str, Any]:
        file = self.file.to_tuple()

        upload_metadata = (None, str(self.upload_metadata).encode(), "text/plain")

        field_dict: dict[str, Any] = {}
        for prop_name, prop in self.additional_properties.items():
            field_dict[prop_name] = (None, str(prop).encode(), "text/plain")

        field_dict.update({"file": file, "upload_metadata": upload_metadata})

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        file = File(payload=BytesIO(d.pop("file")))

        upload_metadata = d.pop("upload_metadata")

        body_upload_file_projects_project_id_upload_file_post = cls(file=file, upload_metadata=upload_metadata)

        body_upload_file_projects_project_id_upload_file_post.additional_properties = d
        return body_upload_file_projects_project_id_upload_file_post

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
