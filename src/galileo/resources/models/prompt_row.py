from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.node_type import NodeType
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.hallucination_segment import HallucinationSegment
    from ..models.metrics import Metrics
    from ..models.prompt_row_inputs import PromptRowInputs
    from ..models.prompt_row_node_output_type_2 import PromptRowNodeOutputType2


T = TypeVar("T", bound="PromptRow")


@_attrs_define
class PromptRow:
    """
    Attributes:
        index (int):
        bleu (Union[None, Unset, float]):
        chain_id (Union[None, Unset, str]):
        chain_root_id (Union[None, Unset, str]):
        cost (Union[None, Unset, float]):
        hallucination (Union[None, Unset, float]):
        hallucination_severity (Union[Unset, int]):  Default: 0.
        has_children (Union[None, Unset, bool]):
        inputs (Union[Unset, PromptRowInputs]):
        metrics (Union[Unset, Metrics]):
        node_id (Union[None, Unset, str]):
        node_input (Union[None, Unset, str]):
        node_name (Union[None, Unset, str]):
        node_output (Union['PromptRowNodeOutputType2', None, Unset, list[str], str]):
        node_type (Union[NodeType, None, Unset]):
        prompt (Union[None, Unset, str]):
        prompt_hallucination_severity (Union[Unset, int]):  Default: 0.
        prompt_segments (Union[None, Unset, list['HallucinationSegment']]):
        response (Union[None, Unset, str]):
        response_segments (Union[Unset, list['HallucinationSegment']]):
        rouge (Union[None, Unset, float]):
        segments (Union[Unset, list['HallucinationSegment']]):
        target (Union[None, Unset, str]):
    """

    index: int
    bleu: Union[None, Unset, float] = UNSET
    chain_id: Union[None, Unset, str] = UNSET
    chain_root_id: Union[None, Unset, str] = UNSET
    cost: Union[None, Unset, float] = UNSET
    hallucination: Union[None, Unset, float] = UNSET
    hallucination_severity: Union[Unset, int] = 0
    has_children: Union[None, Unset, bool] = UNSET
    inputs: Union[Unset, "PromptRowInputs"] = UNSET
    metrics: Union[Unset, "Metrics"] = UNSET
    node_id: Union[None, Unset, str] = UNSET
    node_input: Union[None, Unset, str] = UNSET
    node_name: Union[None, Unset, str] = UNSET
    node_output: Union["PromptRowNodeOutputType2", None, Unset, list[str], str] = UNSET
    node_type: Union[NodeType, None, Unset] = UNSET
    prompt: Union[None, Unset, str] = UNSET
    prompt_hallucination_severity: Union[Unset, int] = 0
    prompt_segments: Union[None, Unset, list["HallucinationSegment"]] = UNSET
    response: Union[None, Unset, str] = UNSET
    response_segments: Union[Unset, list["HallucinationSegment"]] = UNSET
    rouge: Union[None, Unset, float] = UNSET
    segments: Union[Unset, list["HallucinationSegment"]] = UNSET
    target: Union[None, Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.prompt_row_node_output_type_2 import PromptRowNodeOutputType2

        index = self.index

        bleu: Union[None, Unset, float]
        if isinstance(self.bleu, Unset):
            bleu = UNSET
        else:
            bleu = self.bleu

        chain_id: Union[None, Unset, str]
        if isinstance(self.chain_id, Unset):
            chain_id = UNSET
        else:
            chain_id = self.chain_id

        chain_root_id: Union[None, Unset, str]
        if isinstance(self.chain_root_id, Unset):
            chain_root_id = UNSET
        else:
            chain_root_id = self.chain_root_id

        cost: Union[None, Unset, float]
        if isinstance(self.cost, Unset):
            cost = UNSET
        else:
            cost = self.cost

        hallucination: Union[None, Unset, float]
        if isinstance(self.hallucination, Unset):
            hallucination = UNSET
        else:
            hallucination = self.hallucination

        hallucination_severity = self.hallucination_severity

        has_children: Union[None, Unset, bool]
        if isinstance(self.has_children, Unset):
            has_children = UNSET
        else:
            has_children = self.has_children

        inputs: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.inputs, Unset):
            inputs = self.inputs.to_dict()

        metrics: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.metrics, Unset):
            metrics = self.metrics.to_dict()

        node_id: Union[None, Unset, str]
        if isinstance(self.node_id, Unset):
            node_id = UNSET
        else:
            node_id = self.node_id

        node_input: Union[None, Unset, str]
        if isinstance(self.node_input, Unset):
            node_input = UNSET
        else:
            node_input = self.node_input

        node_name: Union[None, Unset, str]
        if isinstance(self.node_name, Unset):
            node_name = UNSET
        else:
            node_name = self.node_name

        node_output: Union[None, Unset, dict[str, Any], list[str], str]
        if isinstance(self.node_output, Unset):
            node_output = UNSET
        elif isinstance(self.node_output, list):
            node_output = self.node_output

        elif isinstance(self.node_output, PromptRowNodeOutputType2):
            node_output = self.node_output.to_dict()
        else:
            node_output = self.node_output

        node_type: Union[None, Unset, str]
        if isinstance(self.node_type, Unset):
            node_type = UNSET
        elif isinstance(self.node_type, NodeType):
            node_type = self.node_type.value
        else:
            node_type = self.node_type

        prompt: Union[None, Unset, str]
        if isinstance(self.prompt, Unset):
            prompt = UNSET
        else:
            prompt = self.prompt

        prompt_hallucination_severity = self.prompt_hallucination_severity

        prompt_segments: Union[None, Unset, list[dict[str, Any]]]
        if isinstance(self.prompt_segments, Unset):
            prompt_segments = UNSET
        elif isinstance(self.prompt_segments, list):
            prompt_segments = []
            for prompt_segments_type_0_item_data in self.prompt_segments:
                prompt_segments_type_0_item = prompt_segments_type_0_item_data.to_dict()
                prompt_segments.append(prompt_segments_type_0_item)

        else:
            prompt_segments = self.prompt_segments

        response: Union[None, Unset, str]
        if isinstance(self.response, Unset):
            response = UNSET
        else:
            response = self.response

        response_segments: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.response_segments, Unset):
            response_segments = []
            for response_segments_item_data in self.response_segments:
                response_segments_item = response_segments_item_data.to_dict()
                response_segments.append(response_segments_item)

        rouge: Union[None, Unset, float]
        if isinstance(self.rouge, Unset):
            rouge = UNSET
        else:
            rouge = self.rouge

        segments: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.segments, Unset):
            segments = []
            for segments_item_data in self.segments:
                segments_item = segments_item_data.to_dict()
                segments.append(segments_item)

        target: Union[None, Unset, str]
        if isinstance(self.target, Unset):
            target = UNSET
        else:
            target = self.target

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({"index": index})
        if bleu is not UNSET:
            field_dict["bleu"] = bleu
        if chain_id is not UNSET:
            field_dict["chain_id"] = chain_id
        if chain_root_id is not UNSET:
            field_dict["chain_root_id"] = chain_root_id
        if cost is not UNSET:
            field_dict["cost"] = cost
        if hallucination is not UNSET:
            field_dict["hallucination"] = hallucination
        if hallucination_severity is not UNSET:
            field_dict["hallucination_severity"] = hallucination_severity
        if has_children is not UNSET:
            field_dict["has_children"] = has_children
        if inputs is not UNSET:
            field_dict["inputs"] = inputs
        if metrics is not UNSET:
            field_dict["metrics"] = metrics
        if node_id is not UNSET:
            field_dict["node_id"] = node_id
        if node_input is not UNSET:
            field_dict["node_input"] = node_input
        if node_name is not UNSET:
            field_dict["node_name"] = node_name
        if node_output is not UNSET:
            field_dict["node_output"] = node_output
        if node_type is not UNSET:
            field_dict["node_type"] = node_type
        if prompt is not UNSET:
            field_dict["prompt"] = prompt
        if prompt_hallucination_severity is not UNSET:
            field_dict["prompt_hallucination_severity"] = prompt_hallucination_severity
        if prompt_segments is not UNSET:
            field_dict["prompt_segments"] = prompt_segments
        if response is not UNSET:
            field_dict["response"] = response
        if response_segments is not UNSET:
            field_dict["response_segments"] = response_segments
        if rouge is not UNSET:
            field_dict["rouge"] = rouge
        if segments is not UNSET:
            field_dict["segments"] = segments
        if target is not UNSET:
            field_dict["target"] = target

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.hallucination_segment import HallucinationSegment
        from ..models.metrics import Metrics
        from ..models.prompt_row_inputs import PromptRowInputs
        from ..models.prompt_row_node_output_type_2 import PromptRowNodeOutputType2

        d = src_dict.copy()
        index = d.pop("index")

        def _parse_bleu(data: object) -> Union[None, Unset, float]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, float], data)

        bleu = _parse_bleu(d.pop("bleu", UNSET))

        def _parse_chain_id(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        chain_id = _parse_chain_id(d.pop("chain_id", UNSET))

        def _parse_chain_root_id(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        chain_root_id = _parse_chain_root_id(d.pop("chain_root_id", UNSET))

        def _parse_cost(data: object) -> Union[None, Unset, float]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, float], data)

        cost = _parse_cost(d.pop("cost", UNSET))

        def _parse_hallucination(data: object) -> Union[None, Unset, float]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, float], data)

        hallucination = _parse_hallucination(d.pop("hallucination", UNSET))

        hallucination_severity = d.pop("hallucination_severity", UNSET)

        def _parse_has_children(data: object) -> Union[None, Unset, bool]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, bool], data)

        has_children = _parse_has_children(d.pop("has_children", UNSET))

        _inputs = d.pop("inputs", UNSET)
        inputs: Union[Unset, PromptRowInputs]
        if isinstance(_inputs, Unset):
            inputs = UNSET
        else:
            inputs = PromptRowInputs.from_dict(_inputs)

        _metrics = d.pop("metrics", UNSET)
        metrics: Union[Unset, Metrics]
        if isinstance(_metrics, Unset):
            metrics = UNSET
        else:
            metrics = Metrics.from_dict(_metrics)

        def _parse_node_id(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        node_id = _parse_node_id(d.pop("node_id", UNSET))

        def _parse_node_input(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        node_input = _parse_node_input(d.pop("node_input", UNSET))

        def _parse_node_name(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        node_name = _parse_node_name(d.pop("node_name", UNSET))

        def _parse_node_output(data: object) -> Union["PromptRowNodeOutputType2", None, Unset, list[str], str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                node_output_type_1 = cast(list[str], data)

                return node_output_type_1
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                node_output_type_2 = PromptRowNodeOutputType2.from_dict(data)

                return node_output_type_2
            except:  # noqa: E722
                pass
            return cast(Union["PromptRowNodeOutputType2", None, Unset, list[str], str], data)

        node_output = _parse_node_output(d.pop("node_output", UNSET))

        def _parse_node_type(data: object) -> Union[NodeType, None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                node_type_type_0 = NodeType(data)

                return node_type_type_0
            except:  # noqa: E722
                pass
            return cast(Union[NodeType, None, Unset], data)

        node_type = _parse_node_type(d.pop("node_type", UNSET))

        def _parse_prompt(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        prompt = _parse_prompt(d.pop("prompt", UNSET))

        prompt_hallucination_severity = d.pop("prompt_hallucination_severity", UNSET)

        def _parse_prompt_segments(data: object) -> Union[None, Unset, list["HallucinationSegment"]]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                prompt_segments_type_0 = []
                _prompt_segments_type_0 = data
                for prompt_segments_type_0_item_data in _prompt_segments_type_0:
                    prompt_segments_type_0_item = HallucinationSegment.from_dict(prompt_segments_type_0_item_data)

                    prompt_segments_type_0.append(prompt_segments_type_0_item)

                return prompt_segments_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, list["HallucinationSegment"]], data)

        prompt_segments = _parse_prompt_segments(d.pop("prompt_segments", UNSET))

        def _parse_response(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        response = _parse_response(d.pop("response", UNSET))

        response_segments = []
        _response_segments = d.pop("response_segments", UNSET)
        for response_segments_item_data in _response_segments or []:
            response_segments_item = HallucinationSegment.from_dict(response_segments_item_data)

            response_segments.append(response_segments_item)

        def _parse_rouge(data: object) -> Union[None, Unset, float]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, float], data)

        rouge = _parse_rouge(d.pop("rouge", UNSET))

        segments = []
        _segments = d.pop("segments", UNSET)
        for segments_item_data in _segments or []:
            segments_item = HallucinationSegment.from_dict(segments_item_data)

            segments.append(segments_item)

        def _parse_target(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        target = _parse_target(d.pop("target", UNSET))

        prompt_row = cls(
            index=index,
            bleu=bleu,
            chain_id=chain_id,
            chain_root_id=chain_root_id,
            cost=cost,
            hallucination=hallucination,
            hallucination_severity=hallucination_severity,
            has_children=has_children,
            inputs=inputs,
            metrics=metrics,
            node_id=node_id,
            node_input=node_input,
            node_name=node_name,
            node_output=node_output,
            node_type=node_type,
            prompt=prompt,
            prompt_hallucination_severity=prompt_hallucination_severity,
            prompt_segments=prompt_segments,
            response=response,
            response_segments=response_segments,
            rouge=rouge,
            segments=segments,
            target=target,
        )

        prompt_row.additional_properties = d
        return prompt_row

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
