from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.few_shot_example import FewShotExample


T = TypeVar("T", bound="AgenticSessionSuccessTemplate")


@_attrs_define
class AgenticSessionSuccessTemplate:
    r"""Template for the agentic session success metric,
    containing all the info necessary to send the agentic session success prompt.

        Attributes:
            explanation_field_name (Union[Unset, str]): Field name to look for in the chainpoll response, for the
                explanation. Default: 'explanation'.
            metric_description (Union[Unset, str]):  Default: 'I have a multi-turn chatbot application where the assistant
                is an agent that has access to tools. I want a metric that assesses whether the session should be considered
                successful, in the sense that the assistant fully answered or resolved all user queries and requests.'.
            metric_few_shot_examples (Union[Unset, list['FewShotExample']]):
            metric_system_prompt (Union[Unset, str]):  Default: 'You will receive the complete chat history from a chatbot
                application between a user and an assistant.\n\nIn the chat history, the user will ask questions, which are
                answered with words, or make requests that require calling tools and resolving actions. Sometimes these are
                given as orders; treat them as if they were questions or requests. Each assistant turn may involve several steps
                that combine internal reflections, planning steps, selecting tools, and calling tools, and should always end
                with the assistant replying back to the user.\n\nYou will analyze the entire chat history and will respond back
                in the following JSON format:\n```json\n{\n    \\"all_user_asks\\": list[string],\n    \\"tasks\\":
                list[dict],\n    \\"ai_answered_all_asks\\": boolean,\n    \\"explanation\\": string\n}\n```\nwhere I will now
                explain how to populate each field.\n\n# Populating: all_user_asks\n\nPopulate `all_user_asks` with a list
                containing every user ask from the chat history. Review the chat history and generate a list with one entry for
                each user question, request, order, follow-up, clarification, etc. Ensure that every user ask is a separate
                item, even if this requires splitting the text mid-sentence. Each item should include enough context to be
                understandable on its own. It is acceptable to have shared context between items and to incorporate parts of
                sentences as needed.\n\n# Populating: Tasks\n\nThis is the most complex field to populate. You will write a JSON
                array where each element is called a task and follows the schema:\n\n```json\n{\n    \\"initial_user_ask\\":
                string,\n    \\"user_ask_refinements\\": list[string],\n    \\"final_user_ask\\": string,\n
                \\"direct_answer\\": string,\n    \\"indirect_answer\\": string,\n    \\"tools_input_output\\": list[string],\n
                \\"properties\\" : {\n        \\"coherent\\": boolean,\n        \\"factually_correct\\": boolean,\n
                \\"comprehensively_answers_final_user_ask\\": boolean,\n        \\"does_not_contradict_tools_output\\":
                boolean,\n        \\"tools_output_summary_is_accurate\\": boolean,\n    },\n    \\"boolean_properties\\":
                list[boolean],\n    \\"answer_satisfies_properties\\": boolean\n}\n```\n\nThe high-level goal is to list all
                tasks and their resolutions and to determine whether each task has been successfully accomplished.\n\n## Step 1:
                initial_user_ask, user_ask_refinements and final_user_ask\n\nFirst, identify the `initial_user_ask` that starts
                the task, as well as any `user_ask_refinements` related to the same task. To do this, first loop through the
                entries in `all_user_asks`. If an entry already appears in a previous task, ignore it; otherwise, consider it as
                the `initial_user_ask`. Next, examine the remaining entries in `all_user_asks` and fill `user_ask_refinements`
                with all those related to the `initial_user_ask`, meaning they either refine it or continue the same
                ask.\n\nFinally, create a coherent `final_user_ask` containing the most updated version of the ask by starting
                with the initial one and incorporating or replacing any parts with their refinements. This will be the ask that
                the assistant will attempt to answer.\n\n## Step 2: direct_answer and indirect_answer\n\nExtract every direct
                and indirect answer that responds to the `final_user_ask`.\n\nAn indirect answer is a part of the assistant\'s
                reponse that tries to respond to `final_user_ask` and satisfies any of the following:\n- it mentions limitations
                or the inability to complete the `final_user_ask`,\n- it references a failed attempt to complete the
                `final_user_ask`,\n- it suggests offering help with a different ask than the `final_user_ask`,\n- it requests
                further information or clarifications from the user.\nAdd any piece of the assistant\'s response looking like an
                indirect answer to `indirect_answer`.\n\nA direct answer is a part of an assistant\'s response that either:\n-
                directly responds to the `final_user_ask`,\n- confirms a successful resolution of the `final_user_ask`.\nIf
                there are multiple direct answers, simply concatenate them into a longer answer. If there are no direct answers
                satisfying the above conditions, leave the field `direct_answer` empty.\n\nNote that a piece of an answer cannot
                be both direct and indirect, you should pick the field in which to add it.\n\n## Step 3:
                tools_input_output\n\nIf `direct_answer` is empty, skip this step.\n\nExamine each assistant step and identify
                which tool or function output seemingly contributed to creating any part of the answer from `direct_answer`. If
                an assistant step immediately before or after the tool call mentions using or having used the tool for answering
                the `final_user_ask`, the tool call should be associated with this ask. Additionally, if any part of the answer
                closely aligns with the output of a tool, the tool call should also be associated with this ask.\n\nCreate a
                list containing the concatenated input and output of each tool used in formulating any part of the answer from
                `direct_answer`. The tool input is noted as an assistant step before calling the tool, and the tool output is
                recorded as a tool step.\n\n## Step 4: properties, boolean_properties and answer_satisfies_properties\n\nIf
                `direct_answer` is empty, set every boolean in `properties`, `boolean_properties` and
                `answer_satisfies_properties` to `false`.\n\nFor each part of the answer from `direct_answer`, evaluate the
                following properties one by one to determine which are satisfied and which are not:\n\n- **coherent**: The
                answer is coherent with itself and does not contain internal contradictions.\n- **factually_correct**: The parts
                of the answer that do not come from the output of a tool are factually correct.\n-
                **comprehensively_answers_final_user_ask**: The answer specifically responds to the `final_user_ask`, carefully
                addressing every aspect of the ask without deviation or omission, ensuring that no details or parts of the ask
                are left unanswered.\n- **does_not_contradict_tools_output**: No citation of a tool\'s output contradict any
                text from `tools_input_output`.\n- **tools_output_summary_is_accurate**: Every summary of a tool\'s output is
                accurate with the tool\'s output from `tools_input_output`. In particular it does not omit critical information
                relevant to the `final_user_ask` and does not contain made-up information.\n\nAfter assessing each of these
                properties, copy the resulting boolean values into the list `boolean_properties`.\n\nFinally, set
                `answer_satisfies_properties` to `false` if any entry in `boolean_properties` is set to `false`; otherwise, set
                `answer_satisfies_properties` to `true`.\n\n# Populating: ai_answered_all_asks\n\nRespond `true` if every task
                has `answer_satisfies_properties` set to `true`, otherwise respond `false`. If `all_user_asks` is empty, set
                `answer_satisfies_properties` to `true`.\n\n# Populating: explanation\n\nIf any user ask has
                `answer_satisfies_properties` set to `false`, explain why it didn\'t satisfy all the properties. Otherwise
                summarize in a few words each ask and the provided answer.\n\nIf `all_user_asks` is empty, mention that you did
                not find any user ask. If `direct_answer` is empty, mention that no resultion to the `final_user_ask` was
                provided.\n\nYou must respond with a valid JSON object; be sure to escape special characters.'.
            template (Union[Unset, str]):  Default: 'Here is a the chatbot history:\n```\n{query}\n```\nNow perform the
                evaluation on the chat history as described in the system prompt.'.
            value_field_name (Union[Unset, str]):  Default: 'ai_answered_all_asks'.
    """

    explanation_field_name: Union[Unset, str] = "explanation"
    metric_description: Union[Unset, str] = (
        "I have a multi-turn chatbot application where the assistant is an agent that has access to tools. I want a metric that assesses whether the session should be considered successful, in the sense that the assistant fully answered or resolved all user queries and requests."
    )
    metric_few_shot_examples: Union[Unset, list["FewShotExample"]] = UNSET
    metric_system_prompt: Union[Unset, str] = (
        'You will receive the complete chat history from a chatbot application between a user and an assistant.\n\nIn the chat history, the user will ask questions, which are answered with words, or make requests that require calling tools and resolving actions. Sometimes these are given as orders; treat them as if they were questions or requests. Each assistant turn may involve several steps that combine internal reflections, planning steps, selecting tools, and calling tools, and should always end with the assistant replying back to the user.\n\nYou will analyze the entire chat history and will respond back in the following JSON format:\n```json\n{\n    \\"all_user_asks\\": list[string],\n    \\"tasks\\": list[dict],\n    \\"ai_answered_all_asks\\": boolean,\n    \\"explanation\\": string\n}\n```\nwhere I will now explain how to populate each field.\n\n# Populating: all_user_asks\n\nPopulate `all_user_asks` with a list containing every user ask from the chat history. Review the chat history and generate a list with one entry for each user question, request, order, follow-up, clarification, etc. Ensure that every user ask is a separate item, even if this requires splitting the text mid-sentence. Each item should include enough context to be understandable on its own. It is acceptable to have shared context between items and to incorporate parts of sentences as needed.\n\n# Populating: Tasks\n\nThis is the most complex field to populate. You will write a JSON array where each element is called a task and follows the schema:\n\n```json\n{\n    \\"initial_user_ask\\": string,\n    \\"user_ask_refinements\\": list[string],\n    \\"final_user_ask\\": string,\n    \\"direct_answer\\": string,\n    \\"indirect_answer\\": string,\n    \\"tools_input_output\\": list[string],\n    \\"properties\\" : {\n        \\"coherent\\": boolean,\n        \\"factually_correct\\": boolean,\n        \\"comprehensively_answers_final_user_ask\\": boolean,\n        \\"does_not_contradict_tools_output\\": boolean,\n        \\"tools_output_summary_is_accurate\\": boolean,\n    },\n    \\"boolean_properties\\": list[boolean],\n    \\"answer_satisfies_properties\\": boolean\n}\n```\n\nThe high-level goal is to list all tasks and their resolutions and to determine whether each task has been successfully accomplished.\n\n## Step 1: initial_user_ask, user_ask_refinements and final_user_ask\n\nFirst, identify the `initial_user_ask` that starts the task, as well as any `user_ask_refinements` related to the same task. To do this, first loop through the entries in `all_user_asks`. If an entry already appears in a previous task, ignore it; otherwise, consider it as the `initial_user_ask`. Next, examine the remaining entries in `all_user_asks` and fill `user_ask_refinements` with all those related to the `initial_user_ask`, meaning they either refine it or continue the same ask.\n\nFinally, create a coherent `final_user_ask` containing the most updated version of the ask by starting with the initial one and incorporating or replacing any parts with their refinements. This will be the ask that the assistant will attempt to answer.\n\n## Step 2: direct_answer and indirect_answer\n\nExtract every direct and indirect answer that responds to the `final_user_ask`.\n\nAn indirect answer is a part of the assistant\'s reponse that tries to respond to `final_user_ask` and satisfies any of the following:\n- it mentions limitations or the inability to complete the `final_user_ask`,\n- it references a failed attempt to complete the `final_user_ask`,\n- it suggests offering help with a different ask than the `final_user_ask`,\n- it requests further information or clarifications from the user.\nAdd any piece of the assistant\'s response looking like an indirect answer to `indirect_answer`.\n\nA direct answer is a part of an assistant\'s response that either:\n- directly responds to the `final_user_ask`,\n- confirms a successful resolution of the `final_user_ask`.\nIf there are multiple direct answers, simply concatenate them into a longer answer. If there are no direct answers satisfying the above conditions, leave the field `direct_answer` empty.\n\nNote that a piece of an answer cannot be both direct and indirect, you should pick the field in which to add it.\n\n## Step 3: tools_input_output\n\nIf `direct_answer` is empty, skip this step.\n\nExamine each assistant step and identify which tool or function output seemingly contributed to creating any part of the answer from `direct_answer`. If an assistant step immediately before or after the tool call mentions using or having used the tool for answering the `final_user_ask`, the tool call should be associated with this ask. Additionally, if any part of the answer closely aligns with the output of a tool, the tool call should also be associated with this ask.\n\nCreate a list containing the concatenated input and output of each tool used in formulating any part of the answer from `direct_answer`. The tool input is noted as an assistant step before calling the tool, and the tool output is recorded as a tool step.\n\n## Step 4: properties, boolean_properties and answer_satisfies_properties\n\nIf `direct_answer` is empty, set every boolean in `properties`, `boolean_properties` and `answer_satisfies_properties` to `false`.\n\nFor each part of the answer from `direct_answer`, evaluate the following properties one by one to determine which are satisfied and which are not:\n\n- **coherent**: The answer is coherent with itself and does not contain internal contradictions.\n- **factually_correct**: The parts of the answer that do not come from the output of a tool are factually correct.\n- **comprehensively_answers_final_user_ask**: The answer specifically responds to the `final_user_ask`, carefully addressing every aspect of the ask without deviation or omission, ensuring that no details or parts of the ask are left unanswered.\n- **does_not_contradict_tools_output**: No citation of a tool\'s output contradict any text from `tools_input_output`.\n- **tools_output_summary_is_accurate**: Every summary of a tool\'s output is accurate with the tool\'s output from `tools_input_output`. In particular it does not omit critical information relevant to the `final_user_ask` and does not contain made-up information.\n\nAfter assessing each of these properties, copy the resulting boolean values into the list `boolean_properties`.\n\nFinally, set `answer_satisfies_properties` to `false` if any entry in `boolean_properties` is set to `false`; otherwise, set `answer_satisfies_properties` to `true`.\n\n# Populating: ai_answered_all_asks\n\nRespond `true` if every task has `answer_satisfies_properties` set to `true`, otherwise respond `false`. If `all_user_asks` is empty, set `answer_satisfies_properties` to `true`.\n\n# Populating: explanation\n\nIf any user ask has `answer_satisfies_properties` set to `false`, explain why it didn\'t satisfy all the properties. Otherwise summarize in a few words each ask and the provided answer.\n\nIf `all_user_asks` is empty, mention that you did not find any user ask. If `direct_answer` is empty, mention that no resultion to the `final_user_ask` was provided.\n\nYou must respond with a valid JSON object; be sure to escape special characters.'
    )
    template: Union[Unset, str] = (
        "Here is a the chatbot history:\n```\n{query}\n```\nNow perform the evaluation on the chat history as described in the system prompt."
    )
    value_field_name: Union[Unset, str] = "ai_answered_all_asks"
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
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.few_shot_example import FewShotExample

        d = dict(src_dict)
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

        agentic_session_success_template = cls(
            explanation_field_name=explanation_field_name,
            metric_description=metric_description,
            metric_few_shot_examples=metric_few_shot_examples,
            metric_system_prompt=metric_system_prompt,
            template=template,
            value_field_name=value_field_name,
        )

        agentic_session_success_template.additional_properties = d
        return agentic_session_success_template

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
