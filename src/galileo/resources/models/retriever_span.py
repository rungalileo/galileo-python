import datetime
from typing import TYPE_CHECKING, Any, Literal, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.document import Document
    from ..models.metrics import Metrics
    from ..models.retriever_span_user_metadata import RetrieverSpanUserMetadata


T = TypeVar("T", bound="RetrieverSpan")


@_attrs_define
class RetrieverSpan:
    """
    Attributes:
        input_ (str): Input to the trace or span.
        output (list['Document']): Output of the trace or span.
        created_at (Union[Unset, datetime.datetime]): Timestamp of the trace or span's creation.
        metrics (Union[Unset, Metrics]):
        name (Union[Unset, str]): Name of the trace or span. Default: ''.
        status_code (Union[None, Unset, int]): Status code of the trace or span. Used for logging failure or error
            states.
        tags (Union[Unset, list[str]]): Tags associated with this trace or span.
        type_ (Union[Literal['retriever'], Unset]): Type of the trace or span. Default: 'retriever'.
        user_metadata (Union[Unset, RetrieverSpanUserMetadata]): Metadata associated with this trace or span.
    """

    input_: str
    output: list["Document"]
    created_at: Union[Unset, datetime.datetime] = UNSET
    metrics: Union[Unset, "Metrics"] = UNSET
    name: Union[Unset, str] = ""
    status_code: Union[None, Unset, int] = UNSET
    tags: Union[Unset, list[str]] = UNSET
    type_: Union[Literal["retriever"], Unset] = "retriever"
    user_metadata: Union[Unset, "RetrieverSpanUserMetadata"] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        input_ = self.input_

        output = []
        for output_item_data in self.output:
            output_item = output_item_data.to_dict()
            output.append(output_item)

        created_at: Union[Unset, str] = UNSET
        if not isinstance(self.created_at, Unset):
            created_at = self.created_at.isoformat()

        metrics: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.metrics, Unset):
            metrics = self.metrics.to_dict()

        name = self.name

        status_code: Union[None, Unset, int]
        if isinstance(self.status_code, Unset):
            status_code = UNSET
        else:
            status_code = self.status_code

        tags: Union[Unset, list[str]] = UNSET
        if not isinstance(self.tags, Unset):
            tags = self.tags

        type_ = self.type_

        user_metadata: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.user_metadata, Unset):
            user_metadata = self.user_metadata.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({"input": input_, "output": output})
        if created_at is not UNSET:
            field_dict["created_at"] = created_at
        if metrics is not UNSET:
            field_dict["metrics"] = metrics
        if name is not UNSET:
            field_dict["name"] = name
        if status_code is not UNSET:
            field_dict["status_code"] = status_code
        if tags is not UNSET:
            field_dict["tags"] = tags
        if type_ is not UNSET:
            field_dict["type"] = type_
        if user_metadata is not UNSET:
            field_dict["user_metadata"] = user_metadata

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.document import Document
        from ..models.metrics import Metrics
        from ..models.retriever_span_user_metadata import RetrieverSpanUserMetadata

        d = src_dict.copy()
        input_ = d.pop("input")

        output = []
        _output = d.pop("output")
        for output_item_data in _output:
            output_item = Document.from_dict(output_item_data)

            output.append(output_item)

        _created_at = d.pop("created_at", UNSET)
        created_at: Union[Unset, datetime.datetime]
        if isinstance(_created_at, Unset):
            created_at = UNSET
        else:
            created_at = isoparse(_created_at)

        _metrics = d.pop("metrics", UNSET)
        metrics: Union[Unset, Metrics]
        if isinstance(_metrics, Unset):
            metrics = UNSET
        else:
            metrics = Metrics.from_dict(_metrics)

        name = d.pop("name", UNSET)

        def _parse_status_code(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        status_code = _parse_status_code(d.pop("status_code", UNSET))

        tags = cast(list[str], d.pop("tags", UNSET))

        type_ = cast(Union[Literal["retriever"], Unset], d.pop("type", UNSET))
        if type_ != "retriever" and not isinstance(type_, Unset):
            raise ValueError(f"type must match const 'retriever', got '{type_}'")

        _user_metadata = d.pop("user_metadata", UNSET)
        user_metadata: Union[Unset, RetrieverSpanUserMetadata]
        if isinstance(_user_metadata, Unset):
            user_metadata = UNSET
        else:
            user_metadata = RetrieverSpanUserMetadata.from_dict(_user_metadata)

        retriever_span = cls(
            input_=input_,
            output=output,
            created_at=created_at,
            metrics=metrics,
            name=name,
            status_code=status_code,
            tags=tags,
            type_=type_,
            user_metadata=user_metadata,
        )

        retriever_span.additional_properties = d
        return retriever_span

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
