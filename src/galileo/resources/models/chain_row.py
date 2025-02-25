from typing import TYPE_CHECKING, Any, TypeVar, Union, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.node_type import NodeType
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.chain_row_inputs_type_0 import ChainRowInputsType0
    from ..models.chain_row_params import ChainRowParams


T = TypeVar("T", bound="ChainRow")


@_attrs_define
class ChainRow:
    """
    Attributes:
        chain_root_id (UUID):
        node_id (UUID):
        node_type (NodeType):
        chain_id (Union[None, UUID, Unset]):
        creation_timestamp (Union[Unset, int]):
        expected_output (Union[None, Unset, str]):
        finish_reason (Union[Unset, str]):  Default: ''.
        has_children (Union[Unset, bool]):  Default: False.
        inputs (Union['ChainRowInputsType0', None, Unset]):
        latency (Union[None, Unset, int]):
        node_input (Union[Unset, str]):  Default: ''.
        node_name (Union[None, Unset, str]):
        node_output (Union[Unset, str]):  Default: ''.
        params (Union[Unset, ChainRowParams]):
        prompt (Union[None, Unset, str]):
        query_input_tokens (Union[Unset, int]):  Default: 0.
        query_output_tokens (Union[Unset, int]):  Default: 0.
        query_total_tokens (Union[Unset, int]):  Default: 0.
        response (Union[None, Unset, str]):
        step (Union[Unset, int]):  Default: 0.
        tools (Union[None, Unset, str]):
    """

    chain_root_id: UUID
    node_id: UUID
    node_type: NodeType
    chain_id: Union[None, UUID, Unset] = UNSET
    creation_timestamp: Union[Unset, int] = UNSET
    expected_output: Union[None, Unset, str] = UNSET
    finish_reason: Union[Unset, str] = ""
    has_children: Union[Unset, bool] = False
    inputs: Union["ChainRowInputsType0", None, Unset] = UNSET
    latency: Union[None, Unset, int] = UNSET
    node_input: Union[Unset, str] = ""
    node_name: Union[None, Unset, str] = UNSET
    node_output: Union[Unset, str] = ""
    params: Union[Unset, "ChainRowParams"] = UNSET
    prompt: Union[None, Unset, str] = UNSET
    query_input_tokens: Union[Unset, int] = 0
    query_output_tokens: Union[Unset, int] = 0
    query_total_tokens: Union[Unset, int] = 0
    response: Union[None, Unset, str] = UNSET
    step: Union[Unset, int] = 0
    tools: Union[None, Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.chain_row_inputs_type_0 import ChainRowInputsType0

        chain_root_id = str(self.chain_root_id)

        node_id = str(self.node_id)

        node_type = self.node_type.value

        chain_id: Union[None, Unset, str]
        if isinstance(self.chain_id, Unset):
            chain_id = UNSET
        elif isinstance(self.chain_id, UUID):
            chain_id = str(self.chain_id)
        else:
            chain_id = self.chain_id

        creation_timestamp = self.creation_timestamp

        expected_output: Union[None, Unset, str]
        if isinstance(self.expected_output, Unset):
            expected_output = UNSET
        else:
            expected_output = self.expected_output

        finish_reason = self.finish_reason

        has_children = self.has_children

        inputs: Union[None, Unset, dict[str, Any]]
        if isinstance(self.inputs, Unset):
            inputs = UNSET
        elif isinstance(self.inputs, ChainRowInputsType0):
            inputs = self.inputs.to_dict()
        else:
            inputs = self.inputs

        latency: Union[None, Unset, int]
        if isinstance(self.latency, Unset):
            latency = UNSET
        else:
            latency = self.latency

        node_input = self.node_input

        node_name: Union[None, Unset, str]
        if isinstance(self.node_name, Unset):
            node_name = UNSET
        else:
            node_name = self.node_name

        node_output = self.node_output

        params: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.params, Unset):
            params = self.params.to_dict()

        prompt: Union[None, Unset, str]
        if isinstance(self.prompt, Unset):
            prompt = UNSET
        else:
            prompt = self.prompt

        query_input_tokens = self.query_input_tokens

        query_output_tokens = self.query_output_tokens

        query_total_tokens = self.query_total_tokens

        response: Union[None, Unset, str]
        if isinstance(self.response, Unset):
            response = UNSET
        else:
            response = self.response

        step = self.step

        tools: Union[None, Unset, str]
        if isinstance(self.tools, Unset):
            tools = UNSET
        else:
            tools = self.tools

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({"chain_root_id": chain_root_id, "node_id": node_id, "node_type": node_type})
        if chain_id is not UNSET:
            field_dict["chain_id"] = chain_id
        if creation_timestamp is not UNSET:
            field_dict["creation_timestamp"] = creation_timestamp
        if expected_output is not UNSET:
            field_dict["expected_output"] = expected_output
        if finish_reason is not UNSET:
            field_dict["finish_reason"] = finish_reason
        if has_children is not UNSET:
            field_dict["has_children"] = has_children
        if inputs is not UNSET:
            field_dict["inputs"] = inputs
        if latency is not UNSET:
            field_dict["latency"] = latency
        if node_input is not UNSET:
            field_dict["node_input"] = node_input
        if node_name is not UNSET:
            field_dict["node_name"] = node_name
        if node_output is not UNSET:
            field_dict["node_output"] = node_output
        if params is not UNSET:
            field_dict["params"] = params
        if prompt is not UNSET:
            field_dict["prompt"] = prompt
        if query_input_tokens is not UNSET:
            field_dict["query_input_tokens"] = query_input_tokens
        if query_output_tokens is not UNSET:
            field_dict["query_output_tokens"] = query_output_tokens
        if query_total_tokens is not UNSET:
            field_dict["query_total_tokens"] = query_total_tokens
        if response is not UNSET:
            field_dict["response"] = response
        if step is not UNSET:
            field_dict["step"] = step
        if tools is not UNSET:
            field_dict["tools"] = tools

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.chain_row_inputs_type_0 import ChainRowInputsType0
        from ..models.chain_row_params import ChainRowParams

        d = src_dict.copy()
        chain_root_id = UUID(d.pop("chain_root_id"))

        node_id = UUID(d.pop("node_id"))

        node_type = NodeType(d.pop("node_type"))

        def _parse_chain_id(data: object) -> Union[None, UUID, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                chain_id_type_0 = UUID(data)

                return chain_id_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, UUID, Unset], data)

        chain_id = _parse_chain_id(d.pop("chain_id", UNSET))

        creation_timestamp = d.pop("creation_timestamp", UNSET)

        def _parse_expected_output(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        expected_output = _parse_expected_output(d.pop("expected_output", UNSET))

        finish_reason = d.pop("finish_reason", UNSET)

        has_children = d.pop("has_children", UNSET)

        def _parse_inputs(data: object) -> Union["ChainRowInputsType0", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                inputs_type_0 = ChainRowInputsType0.from_dict(data)

                return inputs_type_0
            except:  # noqa: E722
                pass
            return cast(Union["ChainRowInputsType0", None, Unset], data)

        inputs = _parse_inputs(d.pop("inputs", UNSET))

        def _parse_latency(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        latency = _parse_latency(d.pop("latency", UNSET))

        node_input = d.pop("node_input", UNSET)

        def _parse_node_name(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        node_name = _parse_node_name(d.pop("node_name", UNSET))

        node_output = d.pop("node_output", UNSET)

        _params = d.pop("params", UNSET)
        params: Union[Unset, ChainRowParams]
        if isinstance(_params, Unset):
            params = UNSET
        else:
            params = ChainRowParams.from_dict(_params)

        def _parse_prompt(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        prompt = _parse_prompt(d.pop("prompt", UNSET))

        query_input_tokens = d.pop("query_input_tokens", UNSET)

        query_output_tokens = d.pop("query_output_tokens", UNSET)

        query_total_tokens = d.pop("query_total_tokens", UNSET)

        def _parse_response(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        response = _parse_response(d.pop("response", UNSET))

        step = d.pop("step", UNSET)

        def _parse_tools(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        tools = _parse_tools(d.pop("tools", UNSET))

        chain_row = cls(
            chain_root_id=chain_root_id,
            node_id=node_id,
            node_type=node_type,
            chain_id=chain_id,
            creation_timestamp=creation_timestamp,
            expected_output=expected_output,
            finish_reason=finish_reason,
            has_children=has_children,
            inputs=inputs,
            latency=latency,
            node_input=node_input,
            node_name=node_name,
            node_output=node_output,
            params=params,
            prompt=prompt,
            query_input_tokens=query_input_tokens,
            query_output_tokens=query_output_tokens,
            query_total_tokens=query_total_tokens,
            response=response,
            step=step,
            tools=tools,
        )

        chain_row.additional_properties = d
        return chain_row

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
