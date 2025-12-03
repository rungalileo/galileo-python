import json
from typing import Union, cast

from pydantic import TypeAdapter, ValidationError

from galileo.schema.trace import Document as GalileoDocument
from galileo.schema.trace import RetrieverSpanAllowedOutputType
from galileo_core.schemas.shared.document import Document

document_adapter = TypeAdapter(list[Document])


def convert_to_documents(data: RetrieverSpanAllowedOutputType, field_name: Union[str, None] = None) -> list[Document]:
    """Convert various input types to a list of Document objects."""
    if data is None:
        return [Document(content="", metadata={})]

    if isinstance(data, list):
        if all(isinstance(doc, Document) for doc in data):
            return cast(list[Document], data)
        if all(isinstance(doc, GalileoDocument) for doc in data):
            return [
                Document(content=doc.content, metadata=doc.metadata.to_dict() if doc.metadata else {})
                for doc in data
                if isinstance(doc, GalileoDocument)
            ]
        if all(isinstance(doc, str) for doc in data):
            return [Document(content=cast(str, doc), metadata={}) for doc in data]
        if all(isinstance(doc, dict) for doc in data):
            try:
                return [Document.model_validate(doc) for doc in data]
            except ValidationError:
                return [Document(content=json.dumps(doc), metadata={}) for doc in data]
        else:
            message = f" for field {field_name}" if field_name else ""
            raise ValueError(
                f"Invalid document output{message}. Expected list of strings, list of dicts, or a Document, but got {type(data)}"
            )
    elif isinstance(data, Document):
        return [data]
    elif isinstance(data, str):
        return [Document(content=data, metadata={})]
    elif isinstance(data, dict):
        try:
            return [Document.model_validate(data)]
        except ValidationError:
            return [Document(content=json.dumps(data), metadata={})]
    else:
        return [Document(content="", metadata={})]
