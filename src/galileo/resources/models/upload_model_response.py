from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="UploadModelResponse")


@_attrs_define
class UploadModelResponse:
    """
    Attributes:
        filename (str):
        id (str):
        upload_url (str):
    """

    filename: str
    id: str
    upload_url: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        filename = self.filename

        id = self.id

        upload_url = self.upload_url

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({"filename": filename, "id": id, "upload_url": upload_url})

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        filename = d.pop("filename")

        id = d.pop("id")

        upload_url = d.pop("upload_url")

        upload_model_response = cls(filename=filename, id=id, upload_url=upload_url)

        upload_model_response.additional_properties = d
        return upload_model_response

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
