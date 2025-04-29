import datetime
from typing import TYPE_CHECKING, Any, Literal, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.llm_metrics import LlmMetrics
    from ..models.llm_span_tools_type_0_item import LlmSpanToolsType0Item
    from ..models.llm_span_user_metadata import LlmSpanUserMetadata
    from ..models.message import Message


T = TypeVar("T", bound="LlmSpan")


@_attrs_define
class LlmSpan:
    """
    Attributes:
        input_ (list['Message']): Input to the trace or span.
        output (Message):
        created_at (Union[Unset, datetime.datetime]): Timestamp of the trace or span's creation.
        finish_reason (Union[None, Unset, str]): Reason for finishing.
        metrics (Union[Unset, LlmMetrics]):
        model (Union[None, Unset, str]): Model used for this span.
        name (Union[Unset, str]): Name of the trace or span. Default: ''.
        status_code (Union[None, Unset, int]): Status code of the trace or span. Used for logging failure or error
            states.
        tags (Union[Unset, list[str]]): Tags associated with this trace or span.
        temperature (Union[None, Unset, float]): Temperature used for generation.
        tools (Union[None, Unset, list['LlmSpanToolsType0Item']]): List of available tools passed to the LLM on
            invocation.
        type_ (Union[Literal['llm'], Unset]): Type of the trace or span. Default: 'llm'.
        user_metadata (Union[Unset, LlmSpanUserMetadata]): Metadata associated with this trace or span.
    """

    input_: list["Message"]
    output: "Message"
    created_at: Union[Unset, datetime.datetime] = UNSET
    finish_reason: Union[None, Unset, str] = UNSET
    metrics: Union[Unset, "LlmMetrics"] = UNSET
    model: Union[None, Unset, str] = UNSET
    name: Union[Unset, str] = ""
    status_code: Union[None, Unset, int] = UNSET
    tags: Union[Unset, list[str]] = UNSET
    temperature: Union[None, Unset, float] = UNSET
    tools: Union[None, Unset, list["LlmSpanToolsType0Item"]] = UNSET
    type_: Union[Literal["llm"], Unset] = "llm"
    user_metadata: Union[Unset, "LlmSpanUserMetadata"] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        input_ = []
        for input_item_data in self.input_:
            input_item = input_item_data.to_dict()
            input_.append(input_item)

        output = self.output.to_dict()

        created_at: Union[Unset, str] = UNSET
        if not isinstance(self.created_at, Unset):
            created_at = self.created_at.isoformat()

        finish_reason: Union[None, Unset, str]
        if isinstance(self.finish_reason, Unset):
            finish_reason = UNSET
        else:
            finish_reason = self.finish_reason

        metrics: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.metrics, Unset):
            metrics = self.metrics.to_dict()

        model: Union[None, Unset, str]
        if isinstance(self.model, Unset):
            model = UNSET
        else:
            model = self.model

        name = self.name

        status_code: Union[None, Unset, int]
        if isinstance(self.status_code, Unset):
            status_code = UNSET
        else:
            status_code = self.status_code

        tags: Union[Unset, list[str]] = UNSET
        if not isinstance(self.tags, Unset):
            tags = self.tags

        temperature: Union[None, Unset, float]
        if isinstance(self.temperature, Unset):
            temperature = UNSET
        else:
            temperature = self.temperature

        tools: Union[None, Unset, list[dict[str, Any]]]
        if isinstance(self.tools, Unset):
            tools = UNSET
        elif isinstance(self.tools, list):
            tools = []
            for tools_type_0_item_data in self.tools:
                tools_type_0_item = tools_type_0_item_data.to_dict()
                tools.append(tools_type_0_item)

        else:
            tools = self.tools

        type_ = self.type_

        user_metadata: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.user_metadata, Unset):
            user_metadata = self.user_metadata.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({"input": input_, "output": output})
        if created_at is not UNSET:
            field_dict["created_at"] = created_at
        if finish_reason is not UNSET:
            field_dict["finish_reason"] = finish_reason
        if metrics is not UNSET:
            field_dict["metrics"] = metrics
        if model is not UNSET:
            field_dict["model"] = model
        if name is not UNSET:
            field_dict["name"] = name
        if status_code is not UNSET:
            field_dict["status_code"] = status_code
        if tags is not UNSET:
            field_dict["tags"] = tags
        if temperature is not UNSET:
            field_dict["temperature"] = temperature
        if tools is not UNSET:
            field_dict["tools"] = tools
        if type_ is not UNSET:
            field_dict["type"] = type_
        if user_metadata is not UNSET:
            field_dict["user_metadata"] = user_metadata

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.llm_metrics import LlmMetrics
        from ..models.llm_span_tools_type_0_item import LlmSpanToolsType0Item
        from ..models.llm_span_user_metadata import LlmSpanUserMetadata
        from ..models.message import Message

        d = src_dict.copy()
        input_ = []
        _input_ = d.pop("input")
        for input_item_data in _input_:
            input_item = Message.from_dict(input_item_data)

            input_.append(input_item)

        output = Message.from_dict(d.pop("output"))

        _created_at = d.pop("created_at", UNSET)
        created_at: Union[Unset, datetime.datetime]
        if isinstance(_created_at, Unset):
            created_at = UNSET
        else:
            created_at = isoparse(_created_at)

        def _parse_finish_reason(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        finish_reason = _parse_finish_reason(d.pop("finish_reason", UNSET))

        _metrics = d.pop("metrics", UNSET)
        metrics: Union[Unset, LlmMetrics]
        if isinstance(_metrics, Unset):
            metrics = UNSET
        else:
            metrics = LlmMetrics.from_dict(_metrics)

        def _parse_model(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        model = _parse_model(d.pop("model", UNSET))

        name = d.pop("name", UNSET)

        def _parse_status_code(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        status_code = _parse_status_code(d.pop("status_code", UNSET))

        tags = cast(list[str], d.pop("tags", UNSET))

        def _parse_temperature(data: object) -> Union[None, Unset, float]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, float], data)

        temperature = _parse_temperature(d.pop("temperature", UNSET))

        def _parse_tools(data: object) -> Union[None, Unset, list["LlmSpanToolsType0Item"]]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                tools_type_0 = []
                _tools_type_0 = data
                for tools_type_0_item_data in _tools_type_0:
                    tools_type_0_item = LlmSpanToolsType0Item.from_dict(tools_type_0_item_data)

                    tools_type_0.append(tools_type_0_item)

                return tools_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, list["LlmSpanToolsType0Item"]], data)

        tools = _parse_tools(d.pop("tools", UNSET))

        type_ = cast(Union[Literal["llm"], Unset], d.pop("type", UNSET))
        if type_ != "llm" and not isinstance(type_, Unset):
            raise ValueError(f"type must match const 'llm', got '{type_}'")

        _user_metadata = d.pop("user_metadata", UNSET)
        user_metadata: Union[Unset, LlmSpanUserMetadata]
        if isinstance(_user_metadata, Unset):
            user_metadata = UNSET
        else:
            user_metadata = LlmSpanUserMetadata.from_dict(_user_metadata)

        llm_span = cls(
            input_=input_,
            output=output,
            created_at=created_at,
            finish_reason=finish_reason,
            metrics=metrics,
            model=model,
            name=name,
            status_code=status_code,
            tags=tags,
            temperature=temperature,
            tools=tools,
            type_=type_,
            user_metadata=user_metadata,
        )

        llm_span.additional_properties = d
        return llm_span

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
