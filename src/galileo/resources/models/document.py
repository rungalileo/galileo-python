from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.document_metadata import DocumentMetadata


T = TypeVar("T", bound="Document")


@_attrs_define
class Document:
    """
    Attributes:
        page_content (str): Content of the document.
        metadata (Union[Unset, DocumentMetadata]):
    """

    page_content: str
    metadata: Union[Unset, "DocumentMetadata"] = UNSET

    def to_dict(self) -> dict[str, Any]:
        page_content = self.page_content

        metadata: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.metadata, Unset):
            metadata = self.metadata.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update({"page_content": page_content})
        if metadata is not UNSET:
            field_dict["metadata"] = metadata

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.document_metadata import DocumentMetadata

        d = src_dict.copy()
        page_content = d.pop("page_content")

        _metadata = d.pop("metadata", UNSET)
        metadata: Union[Unset, DocumentMetadata]
        if isinstance(_metadata, Unset):
            metadata = UNSET
        else:
            metadata = DocumentMetadata.from_dict(_metadata)

        document = cls(page_content=page_content, metadata=metadata)

        return document
