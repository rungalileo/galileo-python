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
                application between a user and an AI. At the end of the chat history, it is AI’s turn to act.\n\nIn the chat
                history, the user can either ask questions, which are answered with words, or make requests that require calling
                tools and actions to resolve. Sometimes these are given as orders, and these should be treated as questions or
                requests. The AI\'s turn may involve several steps which are a combination of internal reflections, planning,
                selecting tools, calling tools, and ends with the AI replying to the user. \nYour task involves the following
                steps:\n\n########################\n\nStep 1: user_last_input and user_ask\n\nFirst, identify the user\'s last
                input in the chat history. From this input, create a list with one entry for each user question, request, or
                order. If there are no user asks in the user\'s last input, leave the list empty and skip ahead, considering the
                AI\'s turn successful.\n\n########################\n\nStep 2: ai_final_response and
                answer_or_resolution\n\nIdentify the AI\'s final response to the user: it is the very last step in the AI\'s
                turn.\n\nFor every user_ask, focus on ai_final_response and try to extract either an answer or a resolution
                using the following definitions:\n- An answer is a part of the AI\'s final response that directly responds to
                all or part of a user\'s question, or asks for further information or clarification.\n- A resolution is a part
                of the AI\'s final response that confirms a successful resolution, or asks for further information or
                clarification in order to answer a user\'s request.\n\nIf the AI\'s final response does not address the user
                ask, simply write \\"No answer or resolution provided in the final response\\". Do not shorten the answer or
                resolution; provide the entire relevant part.\n\n########################\n\nStep 3:
                tools_input_output\n\nExamine every step in the AI\'s turn and identify which tool/function step seemingly
                contributed to creating the answer or resolution. Every tool call should be linked to a user ask. If an AI step
                immediately before or after the tool call mentions planning or using a tool for answering a user ask, the tool
                call should be associated with that user ask. If the answer or resolution strongly resembles the output of a
                tool, the tool call should also be associated with that user ask.\n\nCreate a list containing the concatenation
                of the entire input and output of every tool used in formulating the answer or resolution. The tool input is
                listed as an AI step before calling the tool, and the tool output is listed as a tool
                step.\n\n########################\n\nStep 4: properties, boolean_properties and answer_successful\n\nFor every
                answer or resolution from Step 2, check the following properties one by one to determine which are satisfied:\n-
                factually_wrong: the answer contains factual errors.\n- addresses_different_ask: the answer or resolution
                addresses a slightly different user ask (make sure to differentiate this from asking clarifying questions
                related to the current ask).\n- not_adherent_to_tools_output: the answer or resolution includes citations from a
                tool\'s output, but some are wrongly copied or attributed.\n- mentions_inability: the answer or resolution
                mentions an inability to complete the user ask.\n- mentions_unsuccessful_attempt: the answer or resolution
                mentions an unsuccessful or failed attempt to complete the user ask.\n\nThen copy all the properties (only the
                boolean value) in the list boolean_properties.\n\nFinally, set answer_successful to `false` if any entry in
                boolean_properties is set to `true`, otherwise set answer_successful to
                `true`.\n\n########################\n\nYou must respond in the following JSON format:\n```\n{\n
                \\"user_last_input\\": string,\n    \\"ai_final_response\\": string,\n    \\"asks_and_answers\\": list[dict],\n
                \\"ai_turn_is_successful\\": boolean,\n    \\"explanation\\": string\n}\n```\n\nYour tasks are defined as
                follows:\n\n- **\\"asks_and_answers\\"**: Perform all the tasks described in the steps above. Your answer should
                be a list where each user ask appears as:\n\n```\n{\n    \\"user_ask\\": string,\n
                \\"answer_or_resolution\\": string,\n    \\"tools_input_output\\": list[string],\n    \\"properties\\" : {\n
                \\"factually_wrong\\": boolean,\n        \\"addresses_different_ask\\": boolean,\n
                \\"not_adherent_to_tools_output\\": boolean,\n        \\"mentions_inability\\": boolean,\n
                \\"mentions_unsuccessful_attempt\\": boolean\n    },\n    \\"boolean_properties\\": list[boolean],\n
                \\"answer_successful\\": boolean\n}\n```\n\n- **\\"ai_turn_is_successful\\"**: Respond `true` if at least one
                answer_successful is True, otherwise respond `false`.\n\n- **\\"explanation\\"**: If at least one answer was
                considered successful, explain why. Otherwise explain why all answers were not successful.\n\nYou must respond
                with a valid JSON object; be sure to escape special characters.'.
            template (Union[Unset, str]):  Default: "Chatbot history:\n```\n{query}\n```\n\nAI's
                turn:\n```\n{response}\n```".
            value_field_name (Union[Unset, str]):  Default: 'ai_turn_is_successful'.
    """

    explanation_field_name: Union[Unset, str] = "explanation"
    metric_description: Union[Unset, str] = (
        "I have a multi-turn chatbot application where the assistant is an agent that has access to tools. An assistant workflow can involves possibly multiple tool selections steps, tool calls steps, and finally a reply to the user. I want a metric that assesses whether each assistant's workflow was thoughtfully planned and ended up helping answer the queries.\n"
    )
    metric_few_shot_examples: Union[Unset, list["FewShotExample"]] = UNSET
    metric_system_prompt: Union[Unset, str] = (
        'You will receive the chat history from a chatbot application between a user and an AI. At the end of the chat history, it is AI’s turn to act.\n\nIn the chat history, the user can either ask questions, which are answered with words, or make requests that require calling tools and actions to resolve. Sometimes these are given as orders, and these should be treated as questions or requests. The AI\'s turn may involve several steps which are a combination of internal reflections, planning, selecting tools, calling tools, and ends with the AI replying to the user. \nYour task involves the following steps:\n\n########################\n\nStep 1: user_last_input and user_ask\n\nFirst, identify the user\'s last input in the chat history. From this input, create a list with one entry for each user question, request, or order. If there are no user asks in the user\'s last input, leave the list empty and skip ahead, considering the AI\'s turn successful.\n\n########################\n\nStep 2: ai_final_response and answer_or_resolution\n\nIdentify the AI\'s final response to the user: it is the very last step in the AI\'s turn.\n\nFor every user_ask, focus on ai_final_response and try to extract either an answer or a resolution using the following definitions:\n- An answer is a part of the AI\'s final response that directly responds to all or part of a user\'s question, or asks for further information or clarification.\n- A resolution is a part of the AI\'s final response that confirms a successful resolution, or asks for further information or clarification in order to answer a user\'s request.\n\nIf the AI\'s final response does not address the user ask, simply write \\"No answer or resolution provided in the final response\\". Do not shorten the answer or resolution; provide the entire relevant part.\n\n########################\n\nStep 3: tools_input_output\n\nExamine every step in the AI\'s turn and identify which tool/function step seemingly contributed to creating the answer or resolution. Every tool call should be linked to a user ask. If an AI step immediately before or after the tool call mentions planning or using a tool for answering a user ask, the tool call should be associated with that user ask. If the answer or resolution strongly resembles the output of a tool, the tool call should also be associated with that user ask.\n\nCreate a list containing the concatenation of the entire input and output of every tool used in formulating the answer or resolution. The tool input is listed as an AI step before calling the tool, and the tool output is listed as a tool step.\n\n########################\n\nStep 4: properties, boolean_properties and answer_successful\n\nFor every answer or resolution from Step 2, check the following properties one by one to determine which are satisfied:\n- factually_wrong: the answer contains factual errors.\n- addresses_different_ask: the answer or resolution addresses a slightly different user ask (make sure to differentiate this from asking clarifying questions related to the current ask).\n- not_adherent_to_tools_output: the answer or resolution includes citations from a tool\'s output, but some are wrongly copied or attributed.\n- mentions_inability: the answer or resolution mentions an inability to complete the user ask.\n- mentions_unsuccessful_attempt: the answer or resolution mentions an unsuccessful or failed attempt to complete the user ask.\n\nThen copy all the properties (only the boolean value) in the list boolean_properties.\n\nFinally, set answer_successful to `false` if any entry in boolean_properties is set to `true`, otherwise set answer_successful to `true`.\n\n########################\n\nYou must respond in the following JSON format:\n```\n{\n    \\"user_last_input\\": string,\n    \\"ai_final_response\\": string,\n    \\"asks_and_answers\\": list[dict],\n    \\"ai_turn_is_successful\\": boolean,\n    \\"explanation\\": string\n}\n```\n\nYour tasks are defined as follows:\n\n- **\\"asks_and_answers\\"**: Perform all the tasks described in the steps above. Your answer should be a list where each user ask appears as:\n\n```\n{\n    \\"user_ask\\": string,\n    \\"answer_or_resolution\\": string,\n    \\"tools_input_output\\": list[string],\n    \\"properties\\" : {\n        \\"factually_wrong\\": boolean,\n        \\"addresses_different_ask\\": boolean,\n        \\"not_adherent_to_tools_output\\": boolean,\n        \\"mentions_inability\\": boolean,\n        \\"mentions_unsuccessful_attempt\\": boolean\n    },\n    \\"boolean_properties\\": list[boolean],\n    \\"answer_successful\\": boolean\n}\n```\n\n- **\\"ai_turn_is_successful\\"**: Respond `true` if at least one answer_successful is True, otherwise respond `false`.\n\n- **\\"explanation\\"**: If at least one answer was considered successful, explain why. Otherwise explain why all answers were not successful.\n\nYou must respond with a valid JSON object; be sure to escape special characters.'
    )
    template: Union[Unset, str] = "Chatbot history:\n```\n{query}\n```\n\nAI's turn:\n```\n{response}\n```"
    value_field_name: Union[Unset, str] = "ai_turn_is_successful"
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
