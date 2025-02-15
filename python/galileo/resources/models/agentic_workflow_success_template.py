from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.few_shot_example import FewShotExample


T = TypeVar("T", bound="AgenticWorkflowSuccessTemplate")


@_attrs_define
class AgenticWorkflowSuccessTemplate:
    r"""Template for the agentic workflow success metric,
    containing all the info necessary to send the agentic workflow success prompt.

        Attributes:
            explanation_field_name (Union[Unset, str]): Field name to look for in the chainpoll response, for the
                explanation. Default: 'explanation'.
            metric_description (Union[Unset, str]):  Default: "I have a multi-turn chatbot application where the assistant
                is an agent that has access to tools. An assistant workflow can involves possibly multiple tool selections
                steps, tool calls steps, and finally a reply to the user. I want a metric that assesses whether each assistant's
                workflow was thoughtfully planned and ended up helping answer the queries.\n".
            metric_few_shot_examples (Union[Unset, list['FewShotExample']]):
            metric_system_prompt (Union[Unset, str]):  Default: 'You will receive the chat history from a chatbot
                application. At the end of the conversation, it will be the bot’s turn to act. The bot\'s turn may involve
                several steps such as internal reflections and planning, selecting tools, calling tools, and always ends with
                the bot replying to the user. \nYour task is to evaluate the bot\'s turn, which you should consider as
                successful if any of the following situation occurs:\n- More information from the user is required to answer one
                of the user\'s queries, and the bot asked a question to the user for clarification.\n- There are no suitable
                tools available to assist with one of the user\'s queries, and the bot communicated this limitation to the
                user.\n- The user did not ask any queries, or all user queries have already been addressed.\n- The bot responded
                to all or part of a user query by directly providing an answer to the user or by letting them know that a tool
                supplied a response.\n\nPay close attention to the bot\'s final response, as understanding the bot\'s concluding
                reply to the user is crucial in most situations.\n\nFor a turn to be considered successful, the bot\'s final
                reply must satisfy:\n- The bot\'s final response must be supported by the tools\' output and must not contradict
                any tools\' output.\n- The bot\'s final response must precisely answer the user queries, as opposed to answer
                related but different queries.\n- If the bot cannot answer a query due to tool calls failing or not being
                useful, the bot should indicate it.\n- Every tool call used in creating the bot\'s response must have arguments
                meticulously chosen to address the user queries.\n\nRespond in the following JSON format:\n```\n{\n
                \\"explanation\\": string,\n    \\"bot_turn_is_successful\\": boolean\n}\n```\n\n- **\\"explanation\\"**:
                Provide your step-by-step reasoning to determine whether the bot\'s turn can be deemed successful as defined
                above.\n\n- **\\"bot_turn_is_successful\\"**: Respond `true` if the bot’s turn was successful, and respond
                `false` otherwise.\n\nYou must respond with a valid JSON object; don\'t forget to escape special characters.'.
            template (Union[Unset, str]):  Default: "Chatbot history:\n```\n{query}\n```\n\nThe bot's available
                tools:\n```\n{tools}\n```\n\nThe bot's turn:\n```\n{response}\n```".
            value_field_name (Union[Unset, str]):  Default: 'bot_turn_is_successful'.
    """

    explanation_field_name: Union[Unset, str] = "explanation"
    metric_description: Union[Unset, str] = (
        "I have a multi-turn chatbot application where the assistant is an agent that has access to tools. An assistant workflow can involves possibly multiple tool selections steps, tool calls steps, and finally a reply to the user. I want a metric that assesses whether each assistant's workflow was thoughtfully planned and ended up helping answer the queries.\n"
    )
    metric_few_shot_examples: Union[Unset, list["FewShotExample"]] = UNSET
    metric_system_prompt: Union[Unset, str] = (
        "You will receive the chat history from a chatbot application. At the end of the conversation, it will be the bot’s turn to act. The bot's turn may involve several steps such as internal reflections and planning, selecting tools, calling tools, and always ends with the bot replying to the user. \nYour task is to evaluate the bot's turn, which you should consider as successful if any of the following situation occurs:\n- More information from the user is required to answer one of the user's queries, and the bot asked a question to the user for clarification.\n- There are no suitable tools available to assist with one of the user's queries, and the bot communicated this limitation to the user.\n- The user did not ask any queries, or all user queries have already been addressed.\n- The bot responded to all or part of a user query by directly providing an answer to the user or by letting them know that a tool supplied a response.\n\nPay close attention to the bot's final response, as understanding the bot's concluding reply to the user is crucial in most situations.\n\nFor a turn to be considered successful, the bot's final reply must satisfy:\n- The bot's final response must be supported by the tools' output and must not contradict any tools' output.\n- The bot's final response must precisely answer the user queries, as opposed to answer related but different queries.\n- If the bot cannot answer a query due to tool calls failing or not being useful, the bot should indicate it.\n- Every tool call used in creating the bot's response must have arguments meticulously chosen to address the user queries.\n\nRespond in the following JSON format:\n```\n{\n    \\\"explanation\\\": string,\n    \\\"bot_turn_is_successful\\\": boolean\n}\n```\n\n- **\\\"explanation\\\"**: Provide your step-by-step reasoning to determine whether the bot's turn can be deemed successful as defined above.\n\n- **\\\"bot_turn_is_successful\\\"**: Respond `true` if the bot’s turn was successful, and respond `false` otherwise.\n\nYou must respond with a valid JSON object; don't forget to escape special characters."
    )
    template: Union[Unset, str] = (
        "Chatbot history:\n```\n{query}\n```\n\nThe bot's available tools:\n```\n{tools}\n```\n\nThe bot's turn:\n```\n{response}\n```"
    )
    value_field_name: Union[Unset, str] = "bot_turn_is_successful"
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

        agentic_workflow_success_template = cls(
            explanation_field_name=explanation_field_name,
            metric_description=metric_description,
            metric_few_shot_examples=metric_few_shot_examples,
            metric_system_prompt=metric_system_prompt,
            template=template,
            value_field_name=value_field_name,
        )

        agentic_workflow_success_template.additional_properties = d
        return agentic_workflow_success_template

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
