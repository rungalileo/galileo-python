from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.few_shot_example import FewShotExample


T = TypeVar("T", bound="InstructionAdherenceTemplate")


@_attrs_define
class InstructionAdherenceTemplate:
    r"""
    Attributes:
        explanation_field_name (Union[Unset, str]): Field name to look for in the chainpoll response, for the
            explanation. Default: 'explanation'.
        metric_description (Union[Unset, str]):  Default: 'I have a chatbot application.\nMy system prompt contains a
            list of instructions for what the chatbot should and should not do in every interaction. I want a metric that
            checks whether the latest response from the chatbot is consistent with the instructions.\n\nThe metric should
            only evaluate the latest message (the response), not the chat history. It should return false only if the latest
            message violates one or more instructions. Violations earlier in the chat history should not affect whether the
            value is true or false. The value should only depend on whether the latest message was consistent with the
            instructions, considered in context. The metric should only consider instructions that are applicable to the
            latest message.'.
        metric_few_shot_examples (Union[Unset, list['FewShotExample']]):
        metric_system_prompt (Union[Unset, str]):  Default: 'The user will provide you with a prompt that was sent to a
            chatbot system, and the chatbot\'s latest response. Both will be provided as JSON strings.\n\nIn some cases, the
            prompt may be split up into multiple messages. If so, each message will begin with one of the following
            prefixes:\n\n- \\"System: \\"\n- \\"Human: \\"\n- \\"AI: \\"\n\nIf you see these prefixes, pay attention to them
            because they indicate where messages begin and end. Messages prefixed with \\"System: \\" contain system
            instructions which the chatbot should follow. Messages prefixed with \\"Human: \\" are user input. Messages
            prefixed with \\"AI: \\" are system responses to user input.\nIf you do not see these prefixes, treat the prompt
            as though it was a single user input message prefixed with \\"Human: \\".\n\nYour task is to determine whether
            the latest response from the chatbot is consistent with the instructions provided in the system prompt (if there
            is one) or in the first user message (if there is no system prompt).\n\nFocus only on the latest response and
            the instructions. Do not consider the chat history or any previous messages from the chatbot.\n\nThink step by
            step, and explain your reasoning carefully.\nState your observations first, before drawing any
            conclusions.\n\nRespond in the following JSON format:\n\n```\n{\n    \\"explanation\\": string,\n
            \\"is_consistent\\": boolean\n}\n```\n\n\\"explanation\\": Your step-by-step reasoning process. List out the
            relevant instructions and explain whether the latest response adheres to each of them.\n\n\\"is_consistent\\":
            `true` if the latest response is consistent with the instructions, `false` otherwise.\n\nYou must respond with a
            valid JSON string.'.
        template (Union[Unset, str]):  Default: 'Prompt JSON:\n\n```\n{query_json}\n```\n\nResponse
            JSON:\n\n```\n{response_json}\n```'.
        value_field_name (Union[Unset, str]):  Default: 'is_consistent'.
    """

    explanation_field_name: Union[Unset, str] = "explanation"
    metric_description: Union[Unset, str] = (
        "I have a chatbot application.\nMy system prompt contains a list of instructions for what the chatbot should and should not do in every interaction. I want a metric that checks whether the latest response from the chatbot is consistent with the instructions.\n\nThe metric should only evaluate the latest message (the response), not the chat history. It should return false only if the latest message violates one or more instructions. Violations earlier in the chat history should not affect whether the value is true or false. The value should only depend on whether the latest message was consistent with the instructions, considered in context. The metric should only consider instructions that are applicable to the latest message."
    )
    metric_few_shot_examples: Union[Unset, list["FewShotExample"]] = UNSET
    metric_system_prompt: Union[Unset, str] = (
        'The user will provide you with a prompt that was sent to a chatbot system, and the chatbot\'s latest response. Both will be provided as JSON strings.\n\nIn some cases, the prompt may be split up into multiple messages. If so, each message will begin with one of the following prefixes:\n\n- \\"System: \\"\n- \\"Human: \\"\n- \\"AI: \\"\n\nIf you see these prefixes, pay attention to them because they indicate where messages begin and end. Messages prefixed with \\"System: \\" contain system instructions which the chatbot should follow. Messages prefixed with \\"Human: \\" are user input. Messages prefixed with \\"AI: \\" are system responses to user input.\nIf you do not see these prefixes, treat the prompt as though it was a single user input message prefixed with \\"Human: \\".\n\nYour task is to determine whether the latest response from the chatbot is consistent with the instructions provided in the system prompt (if there is one) or in the first user message (if there is no system prompt).\n\nFocus only on the latest response and the instructions. Do not consider the chat history or any previous messages from the chatbot.\n\nThink step by step, and explain your reasoning carefully.\nState your observations first, before drawing any conclusions.\n\nRespond in the following JSON format:\n\n```\n{\n    \\"explanation\\": string,\n    \\"is_consistent\\": boolean\n}\n```\n\n\\"explanation\\": Your step-by-step reasoning process. List out the relevant instructions and explain whether the latest response adheres to each of them.\n\n\\"is_consistent\\": `true` if the latest response is consistent with the instructions, `false` otherwise.\n\nYou must respond with a valid JSON string.'
    )
    template: Union[Unset, str] = (
        "Prompt JSON:\n\n```\n{query_json}\n```\n\nResponse JSON:\n\n```\n{response_json}\n```"
    )
    value_field_name: Union[Unset, str] = "is_consistent"
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        explanation_field_name = self.explanation_field_name

        metric_description = self.metric_description

        metric_few_shot_examples: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.metric_few_shot_examples, Unset):
            metric_few_shot_examples = []
            for metric_few_shot_examples_item_data in self.metric_few_shot_examples:
                metric_few_shot_examples_item = metric_few_shot_examples_item_data.to_dict()
                metric_few_shot_examples.append(metric_few_shot_examples_item)

        metric_system_prompt = self.metric_system_prompt

        template = self.template

        value_field_name = self.value_field_name

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if explanation_field_name is not UNSET:
            field_dict["explanation_field_name"] = explanation_field_name
        if metric_description is not UNSET:
            field_dict["metric_description"] = metric_description
        if metric_few_shot_examples is not UNSET:
            field_dict["metric_few_shot_examples"] = metric_few_shot_examples
        if metric_system_prompt is not UNSET:
            field_dict["metric_system_prompt"] = metric_system_prompt
        if template is not UNSET:
            field_dict["template"] = template
        if value_field_name is not UNSET:
            field_dict["value_field_name"] = value_field_name

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.few_shot_example import FewShotExample

        d = src_dict.copy()
        explanation_field_name = d.pop("explanation_field_name", UNSET)

        metric_description = d.pop("metric_description", UNSET)

        metric_few_shot_examples = []
        _metric_few_shot_examples = d.pop("metric_few_shot_examples", UNSET)
        for metric_few_shot_examples_item_data in _metric_few_shot_examples or []:
            metric_few_shot_examples_item = FewShotExample.from_dict(metric_few_shot_examples_item_data)

            metric_few_shot_examples.append(metric_few_shot_examples_item)

        metric_system_prompt = d.pop("metric_system_prompt", UNSET)

        template = d.pop("template", UNSET)

        value_field_name = d.pop("value_field_name", UNSET)

        instruction_adherence_template = cls(
            explanation_field_name=explanation_field_name,
            metric_description=metric_description,
            metric_few_shot_examples=metric_few_shot_examples,
            metric_system_prompt=metric_system_prompt,
            template=template,
            value_field_name=value_field_name,
        )

        instruction_adherence_template.additional_properties = d
        return instruction_adherence_template

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
