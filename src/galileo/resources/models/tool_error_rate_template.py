from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.few_shot_example import FewShotExample


T = TypeVar("T", bound="ToolErrorRateTemplate")


@_attrs_define
class ToolErrorRateTemplate:
    r"""Template for the tool error rate metric,
    containing all the info necessary to send the tool error rate prompt.

        Attributes:
            explanation_field_name (Union[Unset, str]): Field name to look for in the chainpoll response, for the
                explanation. Default: 'explanation'.
            metric_description (Union[Unset, str]):  Default: 'I have a multi-turn chatbot application where the assistant
                is an agent that has access to tools. I want a metric to evaluate whether a tool invocation was successful or if
                it resulted in an error.'.
            metric_few_shot_examples (Union[Unset, list['FewShotExample']]):
            metric_system_prompt (Union[Unset, str]):  Default: 'One or more functions have been called, and you will
                receive their output. The output format could be a string containing the tool\'s result, it could be in JSON or
                XML format with additional metadata and information, or it could be a list of the outputs in any such
                format.\n\nYour task is to determine whether at least one function call didn\'t execute correctly and errored
                out. If at least one call failed, then you should consider the entire call as a failure. \nYou should NOT
                evaluate any other aspect of the tool call. In particular you should not evaluate whether the output is well
                formatted, coherent or contains spelling mistakes.\n\nIf you conclude that the call failed, provide an
                explanation as to why. You may summarize any error message you encounter. If the call was successful, no
                explanation is needed.\n\nRespond in the following JSON format:\n\n```\n{\n   \\"function_errored_out\\":
                boolean,\n   \\"explanation\\": string\n}\n```\n\n- **\\"function_errored_out\\"**: Use `false` if all tool
                calls were successful, and `true` if at least one errored out.\n\n- **\\"explanation\\"**: If a tool call
                failed, provide your step-by-step reasoning to determine why it might have failed. If all tool calls were
                succesful, leave this blank.\n\nYou must respond with a valid JSON object; don\'t forget to escape special
                characters.'.
            template (Union[Unset, str]):  Default: 'Tools output:\n```\n{response}\n```'.
            value_field_name (Union[Unset, str]):  Default: 'function_errored_out'.
    """

    explanation_field_name: Union[Unset, str] = "explanation"
    metric_description: Union[Unset, str] = (
        "I have a multi-turn chatbot application where the assistant is an agent that has access to tools. I want a metric to evaluate whether a tool invocation was successful or if it resulted in an error."
    )
    metric_few_shot_examples: Union[Unset, list["FewShotExample"]] = UNSET
    metric_system_prompt: Union[Unset, str] = (
        'One or more functions have been called, and you will receive their output. The output format could be a string containing the tool\'s result, it could be in JSON or XML format with additional metadata and information, or it could be a list of the outputs in any such format.\n\nYour task is to determine whether at least one function call didn\'t execute correctly and errored out. If at least one call failed, then you should consider the entire call as a failure. \nYou should NOT evaluate any other aspect of the tool call. In particular you should not evaluate whether the output is well formatted, coherent or contains spelling mistakes.\n\nIf you conclude that the call failed, provide an explanation as to why. You may summarize any error message you encounter. If the call was successful, no explanation is needed.\n\nRespond in the following JSON format:\n\n```\n{\n   \\"function_errored_out\\": boolean,\n   \\"explanation\\": string\n}\n```\n\n- **\\"function_errored_out\\"**: Use `false` if all tool calls were successful, and `true` if at least one errored out.\n\n- **\\"explanation\\"**: If a tool call failed, provide your step-by-step reasoning to determine why it might have failed. If all tool calls were succesful, leave this blank.\n\nYou must respond with a valid JSON object; don\'t forget to escape special characters.'
    )
    template: Union[Unset, str] = "Tools output:\n```\n{response}\n```"
    value_field_name: Union[Unset, str] = "function_errored_out"
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

        tool_error_rate_template = cls(
            explanation_field_name=explanation_field_name,
            metric_description=metric_description,
            metric_few_shot_examples=metric_few_shot_examples,
            metric_system_prompt=metric_system_prompt,
            template=template,
            value_field_name=value_field_name,
        )

        tool_error_rate_template.additional_properties = d
        return tool_error_rate_template

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
