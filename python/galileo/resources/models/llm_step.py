from typing import TYPE_CHECKING, Any, Literal, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.llm_step_input_type_1 import LlmStepInputType1
    from ..models.llm_step_input_type_4_item import LlmStepInputType4Item
    from ..models.llm_step_metadata import LlmStepMetadata
    from ..models.llm_step_output_type_1 import LlmStepOutputType1
    from ..models.llm_step_output_type_4_item import LlmStepOutputType4Item
    from ..models.llm_step_tools_type_0_item import LlmStepToolsType0Item
    from ..models.message import Message


T = TypeVar("T", bound="LlmStep")


@_attrs_define
class LlmStep:
    """
    Attributes:
        input_ (Union['LlmStepInputType1', 'Message', list['LlmStepInputType4Item'], list['Message'], list[str], str]):
            Input to the LLM step.
        created_at_ns (Union[Unset, int]): Timestamp of the step's creation, as nanoseconds since epoch.
        duration_ns (Union[Unset, int]): Duration of the step in nanoseconds. Default: 0.
        ground_truth (Union[None, Unset, str]): Ground truth expected output for the step.
        input_tokens (Union[None, Unset, int]): Number of input tokens.
        metadata (Union[Unset, LlmStepMetadata]): Metadata associated with this step.
        model (Union[None, Unset, str]): Model used for this step.
        name (Union[Unset, str]): Name of the step. Default: ''.
        output (Union['LlmStepOutputType1', 'Message', Unset, list['LlmStepOutputType4Item'], list['Message'],
            list[str], str]): Output of the LLM step. Default: ''.
        output_tokens (Union[None, Unset, int]): Number of output tokens.
        status_code (Union[None, Unset, int]): Status code of the step. Used for logging failed/errored steps.
        temperature (Union[None, Unset, float]): Temperature used for generation.
        tools (Union[None, Unset, list['LlmStepToolsType0Item']]): List of available tools passed to the LLM on
            invocation.
        total_tokens (Union[None, Unset, int]): Total number of tokens.
        type_ (Union[Literal['llm'], Unset]): Type of the step. By default, it is set to llm. Default: 'llm'.
    """

    input_: Union["LlmStepInputType1", "Message", list["LlmStepInputType4Item"], list["Message"], list[str], str]
    created_at_ns: Union[Unset, int] = UNSET
    duration_ns: Union[Unset, int] = 0
    ground_truth: Union[None, Unset, str] = UNSET
    input_tokens: Union[None, Unset, int] = UNSET
    metadata: Union[Unset, "LlmStepMetadata"] = UNSET
    model: Union[None, Unset, str] = UNSET
    name: Union[Unset, str] = ""
    output: Union[
        "LlmStepOutputType1", "Message", Unset, list["LlmStepOutputType4Item"], list["Message"], list[str], str
    ] = ""
    output_tokens: Union[None, Unset, int] = UNSET
    status_code: Union[None, Unset, int] = UNSET
    temperature: Union[None, Unset, float] = UNSET
    tools: Union[None, Unset, list["LlmStepToolsType0Item"]] = UNSET
    total_tokens: Union[None, Unset, int] = UNSET
    type_: Union[Literal["llm"], Unset] = "llm"
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.llm_step_input_type_1 import LlmStepInputType1
        from ..models.llm_step_output_type_1 import LlmStepOutputType1
        from ..models.message import Message

        input_: Union[dict[str, Any], list[dict[str, Any]], list[str], str]
        if isinstance(self.input_, LlmStepInputType1):
            input_ = self.input_.to_dict()
        elif isinstance(self.input_, Message):
            input_ = self.input_.to_dict()
        elif isinstance(self.input_, list):
            input_ = self.input_

        elif isinstance(self.input_, list):
            input_ = []
            for input_type_4_item_data in self.input_:
                input_type_4_item = input_type_4_item_data.to_dict()
                input_.append(input_type_4_item)

        elif isinstance(self.input_, list):
            input_ = []
            for input_type_5_item_data in self.input_:
                input_type_5_item = input_type_5_item_data.to_dict()
                input_.append(input_type_5_item)

        else:
            input_ = self.input_

        created_at_ns = self.created_at_ns

        duration_ns = self.duration_ns

        ground_truth: Union[None, Unset, str]
        if isinstance(self.ground_truth, Unset):
            ground_truth = UNSET
        else:
            ground_truth = self.ground_truth

        input_tokens: Union[None, Unset, int]
        if isinstance(self.input_tokens, Unset):
            input_tokens = UNSET
        else:
            input_tokens = self.input_tokens

        metadata: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.metadata, Unset):
            metadata = self.metadata.to_dict()

        model: Union[None, Unset, str]
        if isinstance(self.model, Unset):
            model = UNSET
        else:
            model = self.model

        name = self.name

        output: Union[Unset, dict[str, Any], list[dict[str, Any]], list[str], str]
        if isinstance(self.output, Unset):
            output = UNSET
        elif isinstance(self.output, LlmStepOutputType1):
            output = self.output.to_dict()
        elif isinstance(self.output, Message):
            output = self.output.to_dict()
        elif isinstance(self.output, list):
            output = self.output

        elif isinstance(self.output, list):
            output = []
            for output_type_4_item_data in self.output:
                output_type_4_item = output_type_4_item_data.to_dict()
                output.append(output_type_4_item)

        elif isinstance(self.output, list):
            output = []
            for output_type_5_item_data in self.output:
                output_type_5_item = output_type_5_item_data.to_dict()
                output.append(output_type_5_item)

        else:
            output = self.output

        output_tokens: Union[None, Unset, int]
        if isinstance(self.output_tokens, Unset):
            output_tokens = UNSET
        else:
            output_tokens = self.output_tokens

        status_code: Union[None, Unset, int]
        if isinstance(self.status_code, Unset):
            status_code = UNSET
        else:
            status_code = self.status_code

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

        total_tokens: Union[None, Unset, int]
        if isinstance(self.total_tokens, Unset):
            total_tokens = UNSET
        else:
            total_tokens = self.total_tokens

        type_ = self.type_

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({"input": input_})
        if created_at_ns is not UNSET:
            field_dict["created_at_ns"] = created_at_ns
        if duration_ns is not UNSET:
            field_dict["duration_ns"] = duration_ns
        if ground_truth is not UNSET:
            field_dict["ground_truth"] = ground_truth
        if input_tokens is not UNSET:
            field_dict["input_tokens"] = input_tokens
        if metadata is not UNSET:
            field_dict["metadata"] = metadata
        if model is not UNSET:
            field_dict["model"] = model
        if name is not UNSET:
            field_dict["name"] = name
        if output is not UNSET:
            field_dict["output"] = output
        if output_tokens is not UNSET:
            field_dict["output_tokens"] = output_tokens
        if status_code is not UNSET:
            field_dict["status_code"] = status_code
        if temperature is not UNSET:
            field_dict["temperature"] = temperature
        if tools is not UNSET:
            field_dict["tools"] = tools
        if total_tokens is not UNSET:
            field_dict["total_tokens"] = total_tokens
        if type_ is not UNSET:
            field_dict["type"] = type_

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.llm_step_input_type_1 import LlmStepInputType1
        from ..models.llm_step_input_type_4_item import LlmStepInputType4Item
        from ..models.llm_step_metadata import LlmStepMetadata
        from ..models.llm_step_output_type_1 import LlmStepOutputType1
        from ..models.llm_step_output_type_4_item import LlmStepOutputType4Item
        from ..models.llm_step_tools_type_0_item import LlmStepToolsType0Item
        from ..models.message import Message

        d = src_dict.copy()

        def _parse_input_(
            data: object,
        ) -> Union["LlmStepInputType1", "Message", list["LlmStepInputType4Item"], list["Message"], list[str], str]:
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                input_type_1 = LlmStepInputType1.from_dict(data)

                return input_type_1
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                input_type_2 = Message.from_dict(data)

                return input_type_2
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, list):
                    raise TypeError()
                input_type_3 = cast(list[str], data)

                return input_type_3
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, list):
                    raise TypeError()
                input_type_4 = []
                _input_type_4 = data
                for input_type_4_item_data in _input_type_4:
                    input_type_4_item = LlmStepInputType4Item.from_dict(input_type_4_item_data)

                    input_type_4.append(input_type_4_item)

                return input_type_4
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, list):
                    raise TypeError()
                input_type_5 = []
                _input_type_5 = data
                for input_type_5_item_data in _input_type_5:
                    input_type_5_item = Message.from_dict(input_type_5_item_data)

                    input_type_5.append(input_type_5_item)

                return input_type_5
            except:  # noqa: E722
                pass
            return cast(
                Union["LlmStepInputType1", "Message", list["LlmStepInputType4Item"], list["Message"], list[str], str],
                data,
            )

        input_ = _parse_input_(d.pop("input"))

        created_at_ns = d.pop("created_at_ns", UNSET)

        duration_ns = d.pop("duration_ns", UNSET)

        def _parse_ground_truth(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        ground_truth = _parse_ground_truth(d.pop("ground_truth", UNSET))

        def _parse_input_tokens(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        input_tokens = _parse_input_tokens(d.pop("input_tokens", UNSET))

        _metadata = d.pop("metadata", UNSET)
        metadata: Union[Unset, LlmStepMetadata]
        if isinstance(_metadata, Unset):
            metadata = UNSET
        else:
            metadata = LlmStepMetadata.from_dict(_metadata)

        def _parse_model(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        model = _parse_model(d.pop("model", UNSET))

        name = d.pop("name", UNSET)

        def _parse_output(
            data: object,
        ) -> Union[
            "LlmStepOutputType1", "Message", Unset, list["LlmStepOutputType4Item"], list["Message"], list[str], str
        ]:
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                output_type_1 = LlmStepOutputType1.from_dict(data)

                return output_type_1
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                output_type_2 = Message.from_dict(data)

                return output_type_2
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, list):
                    raise TypeError()
                output_type_3 = cast(list[str], data)

                return output_type_3
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, list):
                    raise TypeError()
                output_type_4 = []
                _output_type_4 = data
                for output_type_4_item_data in _output_type_4:
                    output_type_4_item = LlmStepOutputType4Item.from_dict(output_type_4_item_data)

                    output_type_4.append(output_type_4_item)

                return output_type_4
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, list):
                    raise TypeError()
                output_type_5 = []
                _output_type_5 = data
                for output_type_5_item_data in _output_type_5:
                    output_type_5_item = Message.from_dict(output_type_5_item_data)

                    output_type_5.append(output_type_5_item)

                return output_type_5
            except:  # noqa: E722
                pass
            return cast(
                Union[
                    "LlmStepOutputType1",
                    "Message",
                    Unset,
                    list["LlmStepOutputType4Item"],
                    list["Message"],
                    list[str],
                    str,
                ],
                data,
            )

        output = _parse_output(d.pop("output", UNSET))

        def _parse_output_tokens(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        output_tokens = _parse_output_tokens(d.pop("output_tokens", UNSET))

        def _parse_status_code(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        status_code = _parse_status_code(d.pop("status_code", UNSET))

        def _parse_temperature(data: object) -> Union[None, Unset, float]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, float], data)

        temperature = _parse_temperature(d.pop("temperature", UNSET))

        def _parse_tools(data: object) -> Union[None, Unset, list["LlmStepToolsType0Item"]]:
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
                    tools_type_0_item = LlmStepToolsType0Item.from_dict(tools_type_0_item_data)

                    tools_type_0.append(tools_type_0_item)

                return tools_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, list["LlmStepToolsType0Item"]], data)

        tools = _parse_tools(d.pop("tools", UNSET))

        def _parse_total_tokens(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        total_tokens = _parse_total_tokens(d.pop("total_tokens", UNSET))

        type_ = cast(Union[Literal["llm"], Unset], d.pop("type", UNSET))
        if type_ != "llm" and not isinstance(type_, Unset):
            raise ValueError(f"type must match const 'llm', got '{type_}'")

        llm_step = cls(
            input_=input_,
            created_at_ns=created_at_ns,
            duration_ns=duration_ns,
            ground_truth=ground_truth,
            input_tokens=input_tokens,
            metadata=metadata,
            model=model,
            name=name,
            output=output,
            output_tokens=output_tokens,
            status_code=status_code,
            temperature=temperature,
            tools=tools,
            total_tokens=total_tokens,
            type_=type_,
        )

        llm_step.additional_properties = d
        return llm_step

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
