import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.content_modality import ContentModality
from ..models.file_source import FileSource
from ..models.file_status import FileStatus
from ..types import UNSET, Unset

T = TypeVar("T", bound="FileMetadata")


@_attrs_define
class FileMetadata:
    """Enriched file metadata returned to UI/SDK.

    Contains presigned URLs and properties for displaying multimodal
    content in the Galileo console and SDKs.

    Attributes
    ----------
            file_id (str):
            modality (ContentModality): Classification of content modality
            source (FileSource): Source of the file data.
            status (FileStatus): Processing status of the file.
            content_type (Union[None, Unset, str]):
            url (Union[None, Unset, str]): Presigned S3 URL or external URL
            url_expires_at (Union[None, Unset, datetime.datetime]): Expiration time
            size_bytes (Union[None, Unset, int]):
            filename (Union[None, Unset, str]):
    """

    file_id: str
    modality: ContentModality
    source: FileSource
    status: FileStatus
    content_type: Union[None, Unset, str] = UNSET
    url: Union[None, Unset, str] = UNSET
    url_expires_at: Union[None, Unset, datetime.datetime] = UNSET
    size_bytes: Union[None, Unset, int] = UNSET
    filename: Union[None, Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        file_id = self.file_id

        modality = self.modality.value

        source = self.source.value

        status = self.status.value

        content_type: Union[None, Unset, str]
        content_type = UNSET if isinstance(self.content_type, Unset) else self.content_type

        url: Union[None, Unset, str]
        url = UNSET if isinstance(self.url, Unset) else self.url

        url_expires_at: Union[None, Unset, str]
        if isinstance(self.url_expires_at, Unset):
            url_expires_at = UNSET
        elif isinstance(self.url_expires_at, datetime.datetime):
            url_expires_at = self.url_expires_at.isoformat()
        else:
            url_expires_at = self.url_expires_at

        size_bytes: Union[None, Unset, int]
        size_bytes = UNSET if isinstance(self.size_bytes, Unset) else self.size_bytes

        filename: Union[None, Unset, str]
        filename = UNSET if isinstance(self.filename, Unset) else self.filename

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({"file_id": file_id, "modality": modality, "source": source, "status": status})
        if content_type is not UNSET:
            field_dict["content_type"] = content_type
        if url is not UNSET:
            field_dict["url"] = url
        if url_expires_at is not UNSET:
            field_dict["url_expires_at"] = url_expires_at
        if size_bytes is not UNSET:
            field_dict["size_bytes"] = size_bytes
        if filename is not UNSET:
            field_dict["filename"] = filename

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        file_id = d.pop("file_id")

        modality = ContentModality(d.pop("modality"))

        source = FileSource(d.pop("source"))

        status = FileStatus(d.pop("status"))

        def _parse_content_type(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        content_type = _parse_content_type(d.pop("content_type", UNSET))

        def _parse_url(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        url = _parse_url(d.pop("url", UNSET))

        def _parse_url_expires_at(data: object) -> Union[None, Unset, datetime.datetime]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                return isoparse(data)

            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, datetime.datetime], data)

        url_expires_at = _parse_url_expires_at(d.pop("url_expires_at", UNSET))

        def _parse_size_bytes(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        size_bytes = _parse_size_bytes(d.pop("size_bytes", UNSET))

        def _parse_filename(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        filename = _parse_filename(d.pop("filename", UNSET))

        file_metadata = cls(
            file_id=file_id,
            modality=modality,
            source=source,
            status=status,
            content_type=content_type,
            url=url,
            url_expires_at=url_expires_at,
            size_bytes=size_bytes,
            filename=filename,
        )

        file_metadata.additional_properties = d
        return file_metadata

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
