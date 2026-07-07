import datetime
from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

T = TypeVar("T", bound="AnnotationQueueExportUrlResponse")


@_attrs_define
class AnnotationQueueExportUrlResponse:
    """Response for an annotation queue export written to object storage.

    Attributes:
        url (str):
        url_expires_at (datetime.datetime):
        file_name (str):
        content_type (str):
    """

    url: str
    url_expires_at: datetime.datetime
    file_name: str
    content_type: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        url = self.url

        url_expires_at = self.url_expires_at.isoformat()

        file_name = self.file_name

        content_type = self.content_type

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {"url": url, "url_expires_at": url_expires_at, "file_name": file_name, "content_type": content_type}
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        url = d.pop("url")

        url_expires_at = isoparse(d.pop("url_expires_at"))

        file_name = d.pop("file_name")

        content_type = d.pop("content_type")

        annotation_queue_export_url_response = cls(
            url=url, url_expires_at=url_expires_at, file_name=file_name, content_type=content_type
        )

        annotation_queue_export_url_response.additional_properties = d
        return annotation_queue_export_url_response

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
