from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.document_metadata import DocumentMetadata


T = TypeVar("T", bound="Document")


@_attrs_define
class Document:
    """
    Attributes
    ----------
        content (str): Content of the document.
        metadata (DocumentMetadata | Unset):
    """

    content: str
    metadata: DocumentMetadata | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        content = self.content

        metadata: dict[str, Any] | Unset = UNSET
        if not isinstance(self.metadata, Unset):
            metadata = self.metadata.to_dict()

        field_dict: dict[str, Any] = {}

        field_dict.update({"content": content})
        if metadata is not UNSET:
            field_dict["metadata"] = metadata

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.document_metadata import DocumentMetadata

        d = dict(src_dict)
        content = d.pop("content")

        _metadata = d.pop("metadata", UNSET)
        metadata: DocumentMetadata | Unset
        metadata = UNSET if isinstance(_metadata, Unset) else DocumentMetadata.from_dict(_metadata)

        return cls(content=content, metadata=metadata)
