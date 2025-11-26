from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.completeness_template_response_schema_type_0 import CompletenessTemplateResponseSchemaType0
    from ..models.few_shot_example import FewShotExample


T = TypeVar("T", bound="CompletenessTemplate")


@_attrs_define
class CompletenessTemplate:
    r"""
    Attributes
    ----------
        metric_system_prompt (Union[None, Unset, str]): System prompt for the metric.
        metric_description (Union[None, Unset, str]): Description of what the metric should do.
        value_field_name (Union[Unset, str]):  Default: 'completeness'.
        explanation_field_name (Union[Unset, str]): Field name to look for in the chainpoll response, for the
            explanation. Default: 'explanation'.
        template (Union[Unset, str]):  Default: 'I asked someone to answer a question based on one or more documents. On
            a scale of 0 to 1, tell me how well their response covered the relevant information from the documents.\n\nHere
            is what I said to them, as a JSON string:\n\n```\n{query_json}\n```\n\nHere is what they told me, as a JSON
            string:\n\n```\n{response_json}\n```\n\nRespond in the following JSON format:\n\n```\n{{\n    \\"explanation\\":
            string,\n    \\"completeness\\": number\n}}\n```\n\n\\"explanation\\": A string with your step-by-step reasoning
            process. List out each piece of information covered in the documents. For each one, explain why it was or was
            not relevant to the question, and how well the response covered it. Do *not* give an overall assessment of the
            response here, just think step by step about each piece of information, one at a time. Present your work in a
            document-by-document format, considering each document separately, ensure the value is a valid
            string.\n\n\\"completeness\\": A floating-point number rating the Completeness of the response on a scale of 0
            to 1. This number should equal the amount of relevant information that was comprehensively covered in the
            response, divided by the total amount of relevant information in the documents.\n\nYou must respond with a valid
            JSON string.'.
        metric_few_shot_examples (Union[Unset, list['FewShotExample']]): Few-shot examples for the metric.
        response_schema (Union['CompletenessTemplateResponseSchemaType0', None, Unset]): Response schema for the output.
    """

    metric_system_prompt: Union[None, Unset, str] = UNSET
    metric_description: Union[None, Unset, str] = UNSET
    value_field_name: Union[Unset, str] = "completeness"
    explanation_field_name: Union[Unset, str] = "explanation"
    template: Union[Unset, str] = (
        'I asked someone to answer a question based on one or more documents. On a scale of 0 to 1, tell me how well their response covered the relevant information from the documents.\n\nHere is what I said to them, as a JSON string:\n\n```\n{query_json}\n```\n\nHere is what they told me, as a JSON string:\n\n```\n{response_json}\n```\n\nRespond in the following JSON format:\n\n```\n{{\n    \\"explanation\\": string,\n    \\"completeness\\": number\n}}\n```\n\n\\"explanation\\": A string with your step-by-step reasoning process. List out each piece of information covered in the documents. For each one, explain why it was or was not relevant to the question, and how well the response covered it. Do *not* give an overall assessment of the response here, just think step by step about each piece of information, one at a time. Present your work in a document-by-document format, considering each document separately, ensure the value is a valid string.\n\n\\"completeness\\": A floating-point number rating the Completeness of the response on a scale of 0 to 1. This number should equal the amount of relevant information that was comprehensively covered in the response, divided by the total amount of relevant information in the documents.\n\nYou must respond with a valid JSON string.'
    )
    metric_few_shot_examples: Union[Unset, list["FewShotExample"]] = UNSET
    response_schema: Union["CompletenessTemplateResponseSchemaType0", None, Unset] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.completeness_template_response_schema_type_0 import CompletenessTemplateResponseSchemaType0

        metric_system_prompt: Union[None, Unset, str]
        metric_system_prompt = UNSET if isinstance(self.metric_system_prompt, Unset) else self.metric_system_prompt

        metric_description: Union[None, Unset, str]
        metric_description = UNSET if isinstance(self.metric_description, Unset) else self.metric_description

        value_field_name = self.value_field_name

        explanation_field_name = self.explanation_field_name

        template = self.template

        metric_few_shot_examples: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.metric_few_shot_examples, Unset):
            metric_few_shot_examples = []
            for metric_few_shot_examples_item_data in self.metric_few_shot_examples:
                metric_few_shot_examples_item = metric_few_shot_examples_item_data.to_dict()
                metric_few_shot_examples.append(metric_few_shot_examples_item)

        response_schema: Union[None, Unset, dict[str, Any]]
        if isinstance(self.response_schema, Unset):
            response_schema = UNSET
        elif isinstance(self.response_schema, CompletenessTemplateResponseSchemaType0):
            response_schema = self.response_schema.to_dict()
        else:
            response_schema = self.response_schema

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if metric_system_prompt is not UNSET:
            field_dict["metric_system_prompt"] = metric_system_prompt
        if metric_description is not UNSET:
            field_dict["metric_description"] = metric_description
        if value_field_name is not UNSET:
            field_dict["value_field_name"] = value_field_name
        if explanation_field_name is not UNSET:
            field_dict["explanation_field_name"] = explanation_field_name
        if template is not UNSET:
            field_dict["template"] = template
        if metric_few_shot_examples is not UNSET:
            field_dict["metric_few_shot_examples"] = metric_few_shot_examples
        if response_schema is not UNSET:
            field_dict["response_schema"] = response_schema

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.completeness_template_response_schema_type_0 import CompletenessTemplateResponseSchemaType0
        from ..models.few_shot_example import FewShotExample

        d = dict(src_dict)

        def _parse_metric_system_prompt(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        metric_system_prompt = _parse_metric_system_prompt(d.pop("metric_system_prompt", UNSET))

        def _parse_metric_description(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        metric_description = _parse_metric_description(d.pop("metric_description", UNSET))

        value_field_name = d.pop("value_field_name", UNSET)

        explanation_field_name = d.pop("explanation_field_name", UNSET)

        template = d.pop("template", UNSET)

        metric_few_shot_examples = []
        _metric_few_shot_examples = d.pop("metric_few_shot_examples", UNSET)
        for metric_few_shot_examples_item_data in _metric_few_shot_examples or []:
            metric_few_shot_examples_item = FewShotExample.from_dict(metric_few_shot_examples_item_data)

            metric_few_shot_examples.append(metric_few_shot_examples_item)

        def _parse_response_schema(data: object) -> Union["CompletenessTemplateResponseSchemaType0", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                return CompletenessTemplateResponseSchemaType0.from_dict(data)

            except:  # noqa: E722
                pass
            return cast(Union["CompletenessTemplateResponseSchemaType0", None, Unset], data)

        response_schema = _parse_response_schema(d.pop("response_schema", UNSET))

        completeness_template = cls(
            metric_system_prompt=metric_system_prompt,
            metric_description=metric_description,
            value_field_name=value_field_name,
            explanation_field_name=explanation_field_name,
            template=template,
            metric_few_shot_examples=metric_few_shot_examples,
            response_schema=response_schema,
        )

        completeness_template.additional_properties = d
        return completeness_template

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
