"""SDK-local content block types for ingestion.

These types define what the SDK sends to the ingest service for multimodal content.
They are separate from the read-side ContentPart types in galileo-core, which
represent what the API/UI returns after storage.

Ingestion blocks support inline data (base64, URLs, provider file IDs),
while read-side ContentParts reference stored files by file_id.
"""

from typing import Annotated, Literal

from pydantic import BaseModel, Field, model_validator

from galileo_core.schemas.shared.multimodal import ContentModality


class TextContentBlock(BaseModel):
    """A text segment for ingestion."""

    type: Literal["text"] = "text"
    text: str
    index: int | None = None
    metadata: dict[str, str] | None = None


class DataContentBlock(BaseModel):
    """A binary/media content block for ingestion.

    Exactly one of base64 or url must be set.
    """

    type: Literal["data"] = "data"
    modality: ContentModality
    mime_type: str | None = None
    base64: str | None = None
    url: str | None = None
    index: int | None = None
    metadata: dict[str, str] | None = None

    @model_validator(mode="after")
    def _exactly_one_source(self) -> "DataContentBlock":
        sources = sum(v is not None for v in (self.base64, self.url))
        if sources != 1:
            raise ValueError("Exactly one of base64 or url must be set.")
        return self


IngestContentBlock = Annotated[TextContentBlock | DataContentBlock, Field(discriminator="type")]

IngestMessageContent = str | list[IngestContentBlock]


def is_content_block_list(value: object) -> bool:
    """True when value is a (possibly empty) list whose elements are content blocks."""
    return isinstance(value, list) and all(isinstance(v, TextContentBlock | DataContentBlock) for v in value)
