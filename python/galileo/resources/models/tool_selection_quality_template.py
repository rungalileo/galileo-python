from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.few_shot_example import FewShotExample


T = TypeVar("T", bound="ToolSelectionQualityTemplate")


@_attrs_define
class ToolSelectionQualityTemplate:
    r"""Template for the tool selection quality metric,
    containing all the info necessary to send the tool selection quality prompt.

        Attributes:
            explanation_field_name (Union[Unset, str]): Field name to look for in the chainpoll response, for the
                explanation. Default: 'explanation'.
            metric_description (Union[Unset, str]):  Default: 'I have a multi-turn chatbot application where the assistant
                is an agent that has access to tools. I want a metric that assesses whether the assistant made the correct
                decision in choosing to either use tools or to directly respond, and in cases where it uses tools, whether it
                selected the correct tools with the correct arguments.'.
            metric_few_shot_examples (Union[Unset, list['FewShotExample']]):
            metric_system_prompt (Union[Unset, str]):  Default: 'You will receive the chat history from a chatbot
                application. At the end of the  conversation, it will be the bot’s turn to act. The bot has several options: it
                can reflect and plan its next steps, choose to call tools, or respond directly to the user. If the bot opts to
                use tools, the tools execute separately, and the bot will subsequently review the output from those tools.
                Ultimately, the bot should reply to the user, choosing the relevant parts of the tools\' output.\n\nYour task is
                to evaluate the bot\'s decision-making process and ensure it follows these guidelines:\n- If all user queries
                have already been answered and can be found in the chat history, the bot should not call tools.\n- If no
                suitable tools are available to assist with user queries, the bot should not call tools.\n- If the chat history
                contains all the necessary information to directly answer all user queries, the bot should not call tools.\n- If
                the bot decided to call tools, the tools and argument values selected must relate to at least part of one user
                query.\n- If the bot decided to call tools, all arguments marked as \\"required\\" in the tools\' schema must be
                provided with values.\n\nRemember that there are many ways the bot\'s actions can comply with these rules. Your
                role is to determine whether the bot fundamentally violated any of these rules, not whether it chose the most
                optimal response.\n\nRespond in the following JSON format:\n```\n{\n    \\"explanation\\": string,\n
                \\"bot_answer_follows_rules\\": boolean\n}\n```\n\n- **\\"explanation\\"**: Provide your step-by-step reasoning
                to determine whether the bot\'s reply follows the above-mentioned guidelines.\n\n-
                **\\"bot_answer_follows_rules\\"**: Respond `true` if you believe the bot followed the above guidelines, respond
                `false` otherwise.\n\nYou must respond with a valid JSON object; don\'t forget to escape special characters.'.
            template (Union[Unset, str]):  Default: "Chatbot history:\n```\n{query}\n```\n\nThe bot's available
                tools:\n```\n{tools}\n```\n\nThe answer to evaluate:\n```\n{response}\n```".
            value_field_name (Union[Unset, str]):  Default: 'bot_answer_follows_rules'.
    """

    explanation_field_name: Union[Unset, str] = "explanation"
    metric_description: Union[Unset, str] = (
        "I have a multi-turn chatbot application where the assistant is an agent that has access to tools. I want a metric that assesses whether the assistant made the correct decision in choosing to either use tools or to directly respond, and in cases where it uses tools, whether it selected the correct tools with the correct arguments."
    )
    metric_few_shot_examples: Union[Unset, list["FewShotExample"]] = UNSET
    metric_system_prompt: Union[Unset, str] = (
        'You will receive the chat history from a chatbot application. At the end of the  conversation, it will be the bot’s turn to act. The bot has several options: it can reflect and plan its next steps, choose to call tools, or respond directly to the user. If the bot opts to use tools, the tools execute separately, and the bot will subsequently review the output from those tools. Ultimately, the bot should reply to the user, choosing the relevant parts of the tools\' output.\n\nYour task is to evaluate the bot\'s decision-making process and ensure it follows these guidelines:\n- If all user queries have already been answered and can be found in the chat history, the bot should not call tools.\n- If no suitable tools are available to assist with user queries, the bot should not call tools.\n- If the chat history contains all the necessary information to directly answer all user queries, the bot should not call tools.\n- If the bot decided to call tools, the tools and argument values selected must relate to at least part of one user query.\n- If the bot decided to call tools, all arguments marked as \\"required\\" in the tools\' schema must be provided with values.\n\nRemember that there are many ways the bot\'s actions can comply with these rules. Your role is to determine whether the bot fundamentally violated any of these rules, not whether it chose the most optimal response.\n\nRespond in the following JSON format:\n```\n{\n    \\"explanation\\": string,\n    \\"bot_answer_follows_rules\\": boolean\n}\n```\n\n- **\\"explanation\\"**: Provide your step-by-step reasoning to determine whether the bot\'s reply follows the above-mentioned guidelines.\n\n- **\\"bot_answer_follows_rules\\"**: Respond `true` if you believe the bot followed the above guidelines, respond `false` otherwise.\n\nYou must respond with a valid JSON object; don\'t forget to escape special characters.'
    )
    template: Union[Unset, str] = (
        "Chatbot history:\n```\n{query}\n```\n\nThe bot's available tools:\n```\n{tools}\n```\n\nThe answer to evaluate:\n```\n{response}\n```"
    )
    value_field_name: Union[Unset, str] = "bot_answer_follows_rules"
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

        tool_selection_quality_template = cls(
            explanation_field_name=explanation_field_name,
            metric_description=metric_description,
            metric_few_shot_examples=metric_few_shot_examples,
            metric_system_prompt=metric_system_prompt,
            template=template,
            value_field_name=value_field_name,
        )

        tool_selection_quality_template.additional_properties = d
        return tool_selection_quality_template

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
