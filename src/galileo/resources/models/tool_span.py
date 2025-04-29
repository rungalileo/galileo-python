import datetime
from typing import TYPE_CHECKING, Any, Literal, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.metrics import Metrics
    from ..models.tool_span_user_metadata import ToolSpanUserMetadata


T = TypeVar("T", bound="ToolSpan")


@_attrs_define
class ToolSpan:
    """
    Attributes:
        input_ (str): Input to the trace or span.
        created_at (Union[Unset, datetime.datetime]): Timestamp of the trace or span's creation.
        metrics (Union[Unset, Metrics]):
        name (Union[Unset, str]): Name of the trace or span. Default: ''.
        output (Union[None, Unset, str]): Output of the trace or span.
        status_code (Union[None, Unset, int]): Status code of the trace or span. Used for logging failure or error
            states.
        tags (Union[Unset, list[str]]): Tags associated with this trace or span.
        tool_call_id (Union[None, Unset, str]): ID of the tool call.
        type_ (Union[Literal['tool'], Unset]): Type of the trace or span. Default: 'tool'.
        user_metadata (Union[Unset, ToolSpanUserMetadata]): Metadata associated with this trace or span.
    """

    input_: str
    created_at: Union[Unset, datetime.datetime] = UNSET
    metrics: Union[Unset, "Metrics"] = UNSET
    name: Union[Unset, str] = ""
    output: Union[None, Unset, str] = UNSET
    status_code: Union[None, Unset, int] = UNSET
    tags: Union[Unset, list[str]] = UNSET
    tool_call_id: Union[None, Unset, str] = UNSET
    type_: Union[Literal["tool"], Unset] = "tool"
    user_metadata: Union[Unset, "ToolSpanUserMetadata"] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        input_ = self.input_

        created_at: Union[Unset, str] = UNSET
        if not isinstance(self.created_at, Unset):
            created_at = self.created_at.isoformat()

        metrics: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.metrics, Unset):
            metrics = self.metrics.to_dict()

        name = self.name

        output: Union[None, Unset, str]
        if isinstance(self.output, Unset):
            output = UNSET
        else:
            output = self.output

        status_code: Union[None, Unset, int]
        if isinstance(self.status_code, Unset):
            status_code = UNSET
        else:
            status_code = self.status_code

        tags: Union[Unset, list[str]] = UNSET
        if not isinstance(self.tags, Unset):
            tags = self.tags

        tool_call_id: Union[None, Unset, str]
        if isinstance(self.tool_call_id, Unset):
            tool_call_id = UNSET
        else:
            tool_call_id = self.tool_call_id

        type_ = self.type_

        user_metadata: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.user_metadata, Unset):
            user_metadata = self.user_metadata.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({"input": input_})
        if created_at is not UNSET:
            field_dict["created_at"] = created_at
        if metrics is not UNSET:
            field_dict["metrics"] = metrics
        if name is not UNSET:
            field_dict["name"] = name
        if output is not UNSET:
            field_dict["output"] = output
        if status_code is not UNSET:
            field_dict["status_code"] = status_code
        if tags is not UNSET:
            field_dict["tags"] = tags
        if tool_call_id is not UNSET:
            field_dict["tool_call_id"] = tool_call_id
        if type_ is not UNSET:
            field_dict["type"] = type_
        if user_metadata is not UNSET:
            field_dict["user_metadata"] = user_metadata

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.metrics import Metrics
        from ..models.tool_span_user_metadata import ToolSpanUserMetadata

        d = src_dict.copy()
        input_ = d.pop("input")

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

        def _parse_output(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        output = _parse_output(d.pop("output", UNSET))

        def _parse_status_code(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        status_code = _parse_status_code(d.pop("status_code", UNSET))

        tags = cast(list[str], d.pop("tags", UNSET))

        def _parse_tool_call_id(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        tool_call_id = _parse_tool_call_id(d.pop("tool_call_id", UNSET))

        type_ = cast(Union[Literal["tool"], Unset], d.pop("type", UNSET))
        if type_ != "tool" and not isinstance(type_, Unset):
            raise ValueError(f"type must match const 'tool', got '{type_}'")

        _user_metadata = d.pop("user_metadata", UNSET)
        user_metadata: Union[Unset, ToolSpanUserMetadata]
        if isinstance(_user_metadata, Unset):
            user_metadata = UNSET
        else:
            user_metadata = ToolSpanUserMetadata.from_dict(_user_metadata)

        tool_span = cls(
            input_=input_,
            created_at=created_at,
            metrics=metrics,
            name=name,
            output=output,
            status_code=status_code,
            tags=tags,
            tool_call_id=tool_call_id,
            type_=type_,
            user_metadata=user_metadata,
        )

        tool_span.additional_properties = d
        return tool_span

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
