from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, Literal, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.llm_step_input_type_1 import LlmStepInputType1
    from ..models.llm_step_input_type_4_item import LlmStepInputType4Item
    from ..models.llm_step_metadata import LlmStepMetadata
    from ..models.llm_step_output_type_1 import LlmStepOutputType1
    from ..models.llm_step_output_type_4_item import LlmStepOutputType4Item
    from ..models.llm_step_redacted_input_type_1 import LlmStepRedactedInputType1
    from ..models.llm_step_redacted_input_type_4_item import LlmStepRedactedInputType4Item
    from ..models.llm_step_redacted_output_type_1 import LlmStepRedactedOutputType1
    from ..models.llm_step_redacted_output_type_4_item import LlmStepRedactedOutputType4Item
    from ..models.llm_step_tools_type_0_item import LlmStepToolsType0Item
    from ..models.messages_list_item import MessagesListItem


T = TypeVar("T", bound="LlmStep")


@_attrs_define
class LlmStep:
    """
    Attributes:
        input_ (list[LlmStepInputType4Item] | list[MessagesListItem] | list[str] | LlmStepInputType1 | MessagesListItem
            | str): Input to the LLM step.
        type_ (Literal['llm'] | Unset): Type of the step. By default, it is set to llm. Default: 'llm'.
        redacted_input (list[LlmStepRedactedInputType4Item] | list[MessagesListItem] | list[str] |
            LlmStepRedactedInputType1 | MessagesListItem | None | str | Unset): Redacted input of the LLM step. This is used
            to redact sensitive information.
        output (list[LlmStepOutputType4Item] | list[MessagesListItem] | list[str] | LlmStepOutputType1 |
            MessagesListItem | str | Unset): Output of the LLM step. Default: ''.
        redacted_output (list[LlmStepRedactedOutputType4Item] | list[MessagesListItem] | list[str] |
            LlmStepRedactedOutputType1 | MessagesListItem | None | str | Unset): Redacted output of the LLM step. This is
            used to redact sensitive information.
        name (str | Unset): Name of the step. Default: ''.
        created_at_ns (int | Unset): Timestamp of the step's creation, as nanoseconds since epoch.
        duration_ns (int | Unset): Duration of the step in nanoseconds. Default: 0.
        metadata (LlmStepMetadata | Unset): Metadata associated with this step.
        status_code (int | None | Unset): Status code of the step. Used for logging failed/errored steps.
        ground_truth (None | str | Unset): Ground truth expected output for the step.
        tools (list[LlmStepToolsType0Item] | None | Unset): List of available tools passed to the LLM on invocation.
        model (None | str | Unset): Model used for this step.
        input_tokens (int | None | Unset): Number of input tokens.
        output_tokens (int | None | Unset): Number of output tokens.
        total_tokens (int | None | Unset): Total number of tokens.
        temperature (float | None | Unset): Temperature used for generation.
        time_to_first_token_ms (float | None | Unset): Time to first token in milliseconds.
    """

    input_: (
        list[LlmStepInputType4Item] | list[MessagesListItem] | list[str] | LlmStepInputType1 | MessagesListItem | str
    )
    type_: Literal["llm"] | Unset = "llm"
    redacted_input: (
        list[LlmStepRedactedInputType4Item]
        | list[MessagesListItem]
        | list[str]
        | LlmStepRedactedInputType1
        | MessagesListItem
        | None
        | str
        | Unset
    ) = UNSET
    output: (
        list[LlmStepOutputType4Item]
        | list[MessagesListItem]
        | list[str]
        | LlmStepOutputType1
        | MessagesListItem
        | str
        | Unset
    ) = ""
    redacted_output: (
        list[LlmStepRedactedOutputType4Item]
        | list[MessagesListItem]
        | list[str]
        | LlmStepRedactedOutputType1
        | MessagesListItem
        | None
        | str
        | Unset
    ) = UNSET
    name: str | Unset = ""
    created_at_ns: int | Unset = UNSET
    duration_ns: int | Unset = 0
    metadata: LlmStepMetadata | Unset = UNSET
    status_code: int | None | Unset = UNSET
    ground_truth: None | str | Unset = UNSET
    tools: list[LlmStepToolsType0Item] | None | Unset = UNSET
    model: None | str | Unset = UNSET
    input_tokens: int | None | Unset = UNSET
    output_tokens: int | None | Unset = UNSET
    total_tokens: int | None | Unset = UNSET
    temperature: float | None | Unset = UNSET
    time_to_first_token_ms: float | None | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.llm_step_input_type_1 import LlmStepInputType1
        from ..models.llm_step_output_type_1 import LlmStepOutputType1
        from ..models.llm_step_redacted_input_type_1 import LlmStepRedactedInputType1
        from ..models.llm_step_redacted_output_type_1 import LlmStepRedactedOutputType1
        from ..models.messages_list_item import MessagesListItem

        input_: dict[str, Any] | list[dict[str, Any]] | list[str] | str
        if isinstance(self.input_, LlmStepInputType1):
            input_ = self.input_.to_dict()
        elif isinstance(self.input_, MessagesListItem):
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

        type_ = self.type_

        redacted_input: dict[str, Any] | list[dict[str, Any]] | list[str] | None | str | Unset
        if isinstance(self.redacted_input, Unset):
            redacted_input = UNSET
        elif isinstance(self.redacted_input, LlmStepRedactedInputType1):
            redacted_input = self.redacted_input.to_dict()
        elif isinstance(self.redacted_input, MessagesListItem):
            redacted_input = self.redacted_input.to_dict()
        elif isinstance(self.redacted_input, list):
            redacted_input = self.redacted_input

        elif isinstance(self.redacted_input, list):
            redacted_input = []
            for redacted_input_type_4_item_data in self.redacted_input:
                redacted_input_type_4_item = redacted_input_type_4_item_data.to_dict()
                redacted_input.append(redacted_input_type_4_item)

        elif isinstance(self.redacted_input, list):
            redacted_input = []
            for redacted_input_type_5_item_data in self.redacted_input:
                redacted_input_type_5_item = redacted_input_type_5_item_data.to_dict()
                redacted_input.append(redacted_input_type_5_item)

        else:
            redacted_input = self.redacted_input

        output: dict[str, Any] | list[dict[str, Any]] | list[str] | str | Unset
        if isinstance(self.output, Unset):
            output = UNSET
        elif isinstance(self.output, LlmStepOutputType1):
            output = self.output.to_dict()
        elif isinstance(self.output, MessagesListItem):
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

        redacted_output: dict[str, Any] | list[dict[str, Any]] | list[str] | None | str | Unset
        if isinstance(self.redacted_output, Unset):
            redacted_output = UNSET
        elif isinstance(self.redacted_output, LlmStepRedactedOutputType1):
            redacted_output = self.redacted_output.to_dict()
        elif isinstance(self.redacted_output, MessagesListItem):
            redacted_output = self.redacted_output.to_dict()
        elif isinstance(self.redacted_output, list):
            redacted_output = self.redacted_output

        elif isinstance(self.redacted_output, list):
            redacted_output = []
            for redacted_output_type_4_item_data in self.redacted_output:
                redacted_output_type_4_item = redacted_output_type_4_item_data.to_dict()
                redacted_output.append(redacted_output_type_4_item)

        elif isinstance(self.redacted_output, list):
            redacted_output = []
            for redacted_output_type_5_item_data in self.redacted_output:
                redacted_output_type_5_item = redacted_output_type_5_item_data.to_dict()
                redacted_output.append(redacted_output_type_5_item)

        else:
            redacted_output = self.redacted_output

        name = self.name

        created_at_ns = self.created_at_ns

        duration_ns = self.duration_ns

        metadata: dict[str, Any] | Unset = UNSET
        if not isinstance(self.metadata, Unset):
            metadata = self.metadata.to_dict()

        status_code: int | None | Unset
        if isinstance(self.status_code, Unset):
            status_code = UNSET
        else:
            status_code = self.status_code

        ground_truth: None | str | Unset
        if isinstance(self.ground_truth, Unset):
            ground_truth = UNSET
        else:
            ground_truth = self.ground_truth

        tools: list[dict[str, Any]] | None | Unset
        if isinstance(self.tools, Unset):
            tools = UNSET
        elif isinstance(self.tools, list):
            tools = []
            for tools_type_0_item_data in self.tools:
                tools_type_0_item = tools_type_0_item_data.to_dict()
                tools.append(tools_type_0_item)

        else:
            tools = self.tools

        model: None | str | Unset
        if isinstance(self.model, Unset):
            model = UNSET
        else:
            model = self.model

        input_tokens: int | None | Unset
        if isinstance(self.input_tokens, Unset):
            input_tokens = UNSET
        else:
            input_tokens = self.input_tokens

        output_tokens: int | None | Unset
        if isinstance(self.output_tokens, Unset):
            output_tokens = UNSET
        else:
            output_tokens = self.output_tokens

        total_tokens: int | None | Unset
        if isinstance(self.total_tokens, Unset):
            total_tokens = UNSET
        else:
            total_tokens = self.total_tokens

        temperature: float | None | Unset
        if isinstance(self.temperature, Unset):
            temperature = UNSET
        else:
            temperature = self.temperature

        time_to_first_token_ms: float | None | Unset
        if isinstance(self.time_to_first_token_ms, Unset):
            time_to_first_token_ms = UNSET
        else:
            time_to_first_token_ms = self.time_to_first_token_ms

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({"input": input_})
        if type_ is not UNSET:
            field_dict["type"] = type_
        if redacted_input is not UNSET:
            field_dict["redacted_input"] = redacted_input
        if output is not UNSET:
            field_dict["output"] = output
        if redacted_output is not UNSET:
            field_dict["redacted_output"] = redacted_output
        if name is not UNSET:
            field_dict["name"] = name
        if created_at_ns is not UNSET:
            field_dict["created_at_ns"] = created_at_ns
        if duration_ns is not UNSET:
            field_dict["duration_ns"] = duration_ns
        if metadata is not UNSET:
            field_dict["metadata"] = metadata
        if status_code is not UNSET:
            field_dict["status_code"] = status_code
        if ground_truth is not UNSET:
            field_dict["ground_truth"] = ground_truth
        if tools is not UNSET:
            field_dict["tools"] = tools
        if model is not UNSET:
            field_dict["model"] = model
        if input_tokens is not UNSET:
            field_dict["input_tokens"] = input_tokens
        if output_tokens is not UNSET:
            field_dict["output_tokens"] = output_tokens
        if total_tokens is not UNSET:
            field_dict["total_tokens"] = total_tokens
        if temperature is not UNSET:
            field_dict["temperature"] = temperature
        if time_to_first_token_ms is not UNSET:
            field_dict["time_to_first_token_ms"] = time_to_first_token_ms

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.llm_step_input_type_1 import LlmStepInputType1
        from ..models.llm_step_input_type_4_item import LlmStepInputType4Item
        from ..models.llm_step_metadata import LlmStepMetadata
        from ..models.llm_step_output_type_1 import LlmStepOutputType1
        from ..models.llm_step_output_type_4_item import LlmStepOutputType4Item
        from ..models.llm_step_redacted_input_type_1 import LlmStepRedactedInputType1
        from ..models.llm_step_redacted_input_type_4_item import LlmStepRedactedInputType4Item
        from ..models.llm_step_redacted_output_type_1 import LlmStepRedactedOutputType1
        from ..models.llm_step_redacted_output_type_4_item import LlmStepRedactedOutputType4Item
        from ..models.llm_step_tools_type_0_item import LlmStepToolsType0Item
        from ..models.messages_list_item import MessagesListItem

        d = dict(src_dict)

        def _parse_input_(
            data: object,
        ) -> (
            list[LlmStepInputType4Item]
            | list[MessagesListItem]
            | list[str]
            | LlmStepInputType1
            | MessagesListItem
            | str
        ):
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
                input_type_2 = MessagesListItem.from_dict(data)

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
                    input_type_5_item = MessagesListItem.from_dict(input_type_5_item_data)

                    input_type_5.append(input_type_5_item)

                return input_type_5
            except:  # noqa: E722
                pass
            return cast(
                list[LlmStepInputType4Item]
                | list[MessagesListItem]
                | list[str]
                | LlmStepInputType1
                | MessagesListItem
                | str,
                data,
            )

        input_ = _parse_input_(d.pop("input"))

        type_ = cast(Literal["llm"] | Unset, d.pop("type", UNSET))
        if type_ != "llm" and not isinstance(type_, Unset):
            raise ValueError(f"type must match const 'llm', got '{type_}'")

        def _parse_redacted_input(
            data: object,
        ) -> (
            list[LlmStepRedactedInputType4Item]
            | list[MessagesListItem]
            | list[str]
            | LlmStepRedactedInputType1
            | MessagesListItem
            | None
            | str
            | Unset
        ):
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                redacted_input_type_1 = LlmStepRedactedInputType1.from_dict(data)

                return redacted_input_type_1
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                redacted_input_type_2 = MessagesListItem.from_dict(data)

                return redacted_input_type_2
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, list):
                    raise TypeError()
                redacted_input_type_3 = cast(list[str], data)

                return redacted_input_type_3
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, list):
                    raise TypeError()
                redacted_input_type_4 = []
                _redacted_input_type_4 = data
                for redacted_input_type_4_item_data in _redacted_input_type_4:
                    redacted_input_type_4_item = LlmStepRedactedInputType4Item.from_dict(
                        redacted_input_type_4_item_data
                    )

                    redacted_input_type_4.append(redacted_input_type_4_item)

                return redacted_input_type_4
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, list):
                    raise TypeError()
                redacted_input_type_5 = []
                _redacted_input_type_5 = data
                for redacted_input_type_5_item_data in _redacted_input_type_5:
                    redacted_input_type_5_item = MessagesListItem.from_dict(redacted_input_type_5_item_data)

                    redacted_input_type_5.append(redacted_input_type_5_item)

                return redacted_input_type_5
            except:  # noqa: E722
                pass
            return cast(
                list[LlmStepRedactedInputType4Item]
                | list[MessagesListItem]
                | list[str]
                | LlmStepRedactedInputType1
                | MessagesListItem
                | None
                | str
                | Unset,
                data,
            )

        redacted_input = _parse_redacted_input(d.pop("redacted_input", UNSET))

        def _parse_output(
            data: object,
        ) -> (
            list[LlmStepOutputType4Item]
            | list[MessagesListItem]
            | list[str]
            | LlmStepOutputType1
            | MessagesListItem
            | str
            | Unset
        ):
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
                output_type_2 = MessagesListItem.from_dict(data)

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
                    output_type_5_item = MessagesListItem.from_dict(output_type_5_item_data)

                    output_type_5.append(output_type_5_item)

                return output_type_5
            except:  # noqa: E722
                pass
            return cast(
                list[LlmStepOutputType4Item]
                | list[MessagesListItem]
                | list[str]
                | LlmStepOutputType1
                | MessagesListItem
                | str
                | Unset,
                data,
            )

        output = _parse_output(d.pop("output", UNSET))

        def _parse_redacted_output(
            data: object,
        ) -> (
            list[LlmStepRedactedOutputType4Item]
            | list[MessagesListItem]
            | list[str]
            | LlmStepRedactedOutputType1
            | MessagesListItem
            | None
            | str
            | Unset
        ):
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                redacted_output_type_1 = LlmStepRedactedOutputType1.from_dict(data)

                return redacted_output_type_1
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                redacted_output_type_2 = MessagesListItem.from_dict(data)

                return redacted_output_type_2
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, list):
                    raise TypeError()
                redacted_output_type_3 = cast(list[str], data)

                return redacted_output_type_3
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, list):
                    raise TypeError()
                redacted_output_type_4 = []
                _redacted_output_type_4 = data
                for redacted_output_type_4_item_data in _redacted_output_type_4:
                    redacted_output_type_4_item = LlmStepRedactedOutputType4Item.from_dict(
                        redacted_output_type_4_item_data
                    )

                    redacted_output_type_4.append(redacted_output_type_4_item)

                return redacted_output_type_4
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, list):
                    raise TypeError()
                redacted_output_type_5 = []
                _redacted_output_type_5 = data
                for redacted_output_type_5_item_data in _redacted_output_type_5:
                    redacted_output_type_5_item = MessagesListItem.from_dict(redacted_output_type_5_item_data)

                    redacted_output_type_5.append(redacted_output_type_5_item)

                return redacted_output_type_5
            except:  # noqa: E722
                pass
            return cast(
                list[LlmStepRedactedOutputType4Item]
                | list[MessagesListItem]
                | list[str]
                | LlmStepRedactedOutputType1
                | MessagesListItem
                | None
                | str
                | Unset,
                data,
            )

        redacted_output = _parse_redacted_output(d.pop("redacted_output", UNSET))

        name = d.pop("name", UNSET)

        created_at_ns = d.pop("created_at_ns", UNSET)

        duration_ns = d.pop("duration_ns", UNSET)

        _metadata = d.pop("metadata", UNSET)
        metadata: LlmStepMetadata | Unset
        if isinstance(_metadata, Unset):
            metadata = UNSET
        else:
            metadata = LlmStepMetadata.from_dict(_metadata)

        def _parse_status_code(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        status_code = _parse_status_code(d.pop("status_code", UNSET))

        def _parse_ground_truth(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        ground_truth = _parse_ground_truth(d.pop("ground_truth", UNSET))

        def _parse_tools(data: object) -> list[LlmStepToolsType0Item] | None | Unset:
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
            return cast(list[LlmStepToolsType0Item] | None | Unset, data)

        tools = _parse_tools(d.pop("tools", UNSET))

        def _parse_model(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        model = _parse_model(d.pop("model", UNSET))

        def _parse_input_tokens(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        input_tokens = _parse_input_tokens(d.pop("input_tokens", UNSET))

        def _parse_output_tokens(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        output_tokens = _parse_output_tokens(d.pop("output_tokens", UNSET))

        def _parse_total_tokens(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        total_tokens = _parse_total_tokens(d.pop("total_tokens", UNSET))

        def _parse_temperature(data: object) -> float | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(float | None | Unset, data)

        temperature = _parse_temperature(d.pop("temperature", UNSET))

        def _parse_time_to_first_token_ms(data: object) -> float | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(float | None | Unset, data)

        time_to_first_token_ms = _parse_time_to_first_token_ms(d.pop("time_to_first_token_ms", UNSET))

        llm_step = cls(
            input_=input_,
            type_=type_,
            redacted_input=redacted_input,
            output=output,
            redacted_output=redacted_output,
            name=name,
            created_at_ns=created_at_ns,
            duration_ns=duration_ns,
            metadata=metadata,
            status_code=status_code,
            ground_truth=ground_truth,
            tools=tools,
            model=model,
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            total_tokens=total_tokens,
            temperature=temperature,
            time_to_first_token_ms=time_to_first_token_ms,
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
