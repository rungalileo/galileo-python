from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.node_type import NodeType
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.chain_row_inputs_type_0 import ChainRowInputsType0
    from ..models.chain_row_params import ChainRowParams
    from ..models.chain_row_user_metadata import ChainRowUserMetadata


T = TypeVar("T", bound="ChainRow")


@_attrs_define
class ChainRow:
    """
    Attributes:
        node_id (UUID):
        node_type (NodeType):
        chain_root_id (UUID):
        node_name (None | str | Unset):
        node_input (str | Unset):  Default: ''.
        node_output (str | Unset):  Default: ''.
        tools (None | str | Unset):
        chain_id (None | Unset | UUID):
        step (int | Unset):  Default: 0.
        has_children (bool | Unset):  Default: False.
        inputs (ChainRowInputsType0 | None | Unset):
        prompt (None | str | Unset):
        response (None | str | Unset):
        creation_timestamp (int | Unset):
        finish_reason (str | Unset):  Default: ''.
        latency (int | None | Unset):
        query_input_tokens (int | Unset):  Default: 0.
        query_output_tokens (int | Unset):  Default: 0.
        query_total_tokens (int | Unset):  Default: 0.
        params (ChainRowParams | Unset):
        expected_output (None | str | Unset):
        user_metadata (ChainRowUserMetadata | Unset):
    """

    node_id: UUID
    node_type: NodeType
    chain_root_id: UUID
    node_name: None | str | Unset = UNSET
    node_input: str | Unset = ""
    node_output: str | Unset = ""
    tools: None | str | Unset = UNSET
    chain_id: None | Unset | UUID = UNSET
    step: int | Unset = 0
    has_children: bool | Unset = False
    inputs: ChainRowInputsType0 | None | Unset = UNSET
    prompt: None | str | Unset = UNSET
    response: None | str | Unset = UNSET
    creation_timestamp: int | Unset = UNSET
    finish_reason: str | Unset = ""
    latency: int | None | Unset = UNSET
    query_input_tokens: int | Unset = 0
    query_output_tokens: int | Unset = 0
    query_total_tokens: int | Unset = 0
    params: ChainRowParams | Unset = UNSET
    expected_output: None | str | Unset = UNSET
    user_metadata: ChainRowUserMetadata | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.chain_row_inputs_type_0 import ChainRowInputsType0

        node_id = str(self.node_id)

        node_type = self.node_type.value

        chain_root_id = str(self.chain_root_id)

        node_name: None | str | Unset
        if isinstance(self.node_name, Unset):
            node_name = UNSET
        else:
            node_name = self.node_name

        node_input = self.node_input

        node_output = self.node_output

        tools: None | str | Unset
        if isinstance(self.tools, Unset):
            tools = UNSET
        else:
            tools = self.tools

        chain_id: None | str | Unset
        if isinstance(self.chain_id, Unset):
            chain_id = UNSET
        elif isinstance(self.chain_id, UUID):
            chain_id = str(self.chain_id)
        else:
            chain_id = self.chain_id

        step = self.step

        has_children = self.has_children

        inputs: dict[str, Any] | None | Unset
        if isinstance(self.inputs, Unset):
            inputs = UNSET
        elif isinstance(self.inputs, ChainRowInputsType0):
            inputs = self.inputs.to_dict()
        else:
            inputs = self.inputs

        prompt: None | str | Unset
        if isinstance(self.prompt, Unset):
            prompt = UNSET
        else:
            prompt = self.prompt

        response: None | str | Unset
        if isinstance(self.response, Unset):
            response = UNSET
        else:
            response = self.response

        creation_timestamp = self.creation_timestamp

        finish_reason = self.finish_reason

        latency: int | None | Unset
        if isinstance(self.latency, Unset):
            latency = UNSET
        else:
            latency = self.latency

        query_input_tokens = self.query_input_tokens

        query_output_tokens = self.query_output_tokens

        query_total_tokens = self.query_total_tokens

        params: dict[str, Any] | Unset = UNSET
        if not isinstance(self.params, Unset):
            params = self.params.to_dict()

        expected_output: None | str | Unset
        if isinstance(self.expected_output, Unset):
            expected_output = UNSET
        else:
            expected_output = self.expected_output

        user_metadata: dict[str, Any] | Unset = UNSET
        if not isinstance(self.user_metadata, Unset):
            user_metadata = self.user_metadata.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({"node_id": node_id, "node_type": node_type, "chain_root_id": chain_root_id})
        if node_name is not UNSET:
            field_dict["node_name"] = node_name
        if node_input is not UNSET:
            field_dict["node_input"] = node_input
        if node_output is not UNSET:
            field_dict["node_output"] = node_output
        if tools is not UNSET:
            field_dict["tools"] = tools
        if chain_id is not UNSET:
            field_dict["chain_id"] = chain_id
        if step is not UNSET:
            field_dict["step"] = step
        if has_children is not UNSET:
            field_dict["has_children"] = has_children
        if inputs is not UNSET:
            field_dict["inputs"] = inputs
        if prompt is not UNSET:
            field_dict["prompt"] = prompt
        if response is not UNSET:
            field_dict["response"] = response
        if creation_timestamp is not UNSET:
            field_dict["creation_timestamp"] = creation_timestamp
        if finish_reason is not UNSET:
            field_dict["finish_reason"] = finish_reason
        if latency is not UNSET:
            field_dict["latency"] = latency
        if query_input_tokens is not UNSET:
            field_dict["query_input_tokens"] = query_input_tokens
        if query_output_tokens is not UNSET:
            field_dict["query_output_tokens"] = query_output_tokens
        if query_total_tokens is not UNSET:
            field_dict["query_total_tokens"] = query_total_tokens
        if params is not UNSET:
            field_dict["params"] = params
        if expected_output is not UNSET:
            field_dict["expected_output"] = expected_output
        if user_metadata is not UNSET:
            field_dict["user_metadata"] = user_metadata

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.chain_row_inputs_type_0 import ChainRowInputsType0
        from ..models.chain_row_params import ChainRowParams
        from ..models.chain_row_user_metadata import ChainRowUserMetadata

        d = dict(src_dict)
        node_id = UUID(d.pop("node_id"))

        node_type = NodeType(d.pop("node_type"))

        chain_root_id = UUID(d.pop("chain_root_id"))

        def _parse_node_name(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        node_name = _parse_node_name(d.pop("node_name", UNSET))

        node_input = d.pop("node_input", UNSET)

        node_output = d.pop("node_output", UNSET)

        def _parse_tools(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        tools = _parse_tools(d.pop("tools", UNSET))

        def _parse_chain_id(data: object) -> None | Unset | UUID:
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
            return cast(None | Unset | UUID, data)

        chain_id = _parse_chain_id(d.pop("chain_id", UNSET))

        step = d.pop("step", UNSET)

        has_children = d.pop("has_children", UNSET)

        def _parse_inputs(data: object) -> ChainRowInputsType0 | None | Unset:
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
            return cast(ChainRowInputsType0 | None | Unset, data)

        inputs = _parse_inputs(d.pop("inputs", UNSET))

        def _parse_prompt(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        prompt = _parse_prompt(d.pop("prompt", UNSET))

        def _parse_response(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        response = _parse_response(d.pop("response", UNSET))

        creation_timestamp = d.pop("creation_timestamp", UNSET)

        finish_reason = d.pop("finish_reason", UNSET)

        def _parse_latency(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        latency = _parse_latency(d.pop("latency", UNSET))

        query_input_tokens = d.pop("query_input_tokens", UNSET)

        query_output_tokens = d.pop("query_output_tokens", UNSET)

        query_total_tokens = d.pop("query_total_tokens", UNSET)

        _params = d.pop("params", UNSET)
        params: ChainRowParams | Unset
        if isinstance(_params, Unset):
            params = UNSET
        else:
            params = ChainRowParams.from_dict(_params)

        def _parse_expected_output(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        expected_output = _parse_expected_output(d.pop("expected_output", UNSET))

        _user_metadata = d.pop("user_metadata", UNSET)
        user_metadata: ChainRowUserMetadata | Unset
        if isinstance(_user_metadata, Unset):
            user_metadata = UNSET
        else:
            user_metadata = ChainRowUserMetadata.from_dict(_user_metadata)

        chain_row = cls(
            node_id=node_id,
            node_type=node_type,
            chain_root_id=chain_root_id,
            node_name=node_name,
            node_input=node_input,
            node_output=node_output,
            tools=tools,
            chain_id=chain_id,
            step=step,
            has_children=has_children,
            inputs=inputs,
            prompt=prompt,
            response=response,
            creation_timestamp=creation_timestamp,
            finish_reason=finish_reason,
            latency=latency,
            query_input_tokens=query_input_tokens,
            query_output_tokens=query_output_tokens,
            query_total_tokens=query_total_tokens,
            params=params,
            expected_output=expected_output,
            user_metadata=user_metadata,
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
