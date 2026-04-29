from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.few_shot_example import FewShotExample
    from ..models.input_toxicity_template_response_schema_type_0 import InputToxicityTemplateResponseSchemaType0


T = TypeVar("T", bound="InputToxicityTemplate")


@_attrs_define
class InputToxicityTemplate:
    r"""Template for the toxicity metric,
    containing all the info necessary to send the toxicity prompt.

    Attributes
    ----------
            metric_system_prompt (Union[Unset, str]):  Default: 'The user will provide you with a text.\nYou need to
                determine if the text is toxic or not. Toxicity refers to language that is harmful or inappropriate, typically
                evaluated based on the following aspects:\nHate Speech: Statements that demean, dehumanize, or attack
                individuals or groups based on identity factors like race, gender, or religion.\nOffensive Content: Vulgar,
                abusive, or overly profane language used to provoke or insult.\nSexual Content: Explicit or inappropriate sexual
                statements that may be offensive or unsuitable in context.\nViolence or Harm: Advocacy or description of
                physical harm, abuse, or violent actions.\nIllegal or Unethical Guidance: Instructions or encouragement for
                illegal or unethical actions.\nManipulation or Exploitation: Language intended to deceive, exploit, or
                manipulate individuals for harmful purposes.\nStatements fitting these criteria can be flagged as toxic,
                harmful, or inappropriate based on context and intent.\n\nThink step by step, and explain your reasoning
                carefully.\nState your observations first, before drawing any conclusions.\n\nRespond in the following JSON
                format:\n\n```\n{\n    \\"explanation\\": string,\n    \\"toxic\\": boolean\n}\n```\n\n\\"explanation\\": A
                step-by-step reasoning process detailing your observations and how they relate to the toxicity
                criteria.\n\n\\"toxic\\": A boolean value, 1 if the text is toxic, 0 otherwise.\n\nYou must respond with valid
                JSON.'.
            metric_description (Union[Unset, str]):  Default: 'I want a metric that checks whether the given text is toxic
                or not. '.
            value_field_name (Union[Unset, str]):  Default: 'toxic'.
            explanation_field_name (Union[Unset, str]): Field name to look for in the chainpoll response, for the
                explanation. Default: 'explanation'.
            template (Union[Unset, str]):  Default: 'Input:\n\n```\n{query}\n```'.
            metric_few_shot_examples (Union[Unset, list['FewShotExample']]):
            response_schema (Union['InputToxicityTemplateResponseSchemaType0', None, Unset]): Response schema for the output
    """

    metric_system_prompt: Union[Unset, str] = (
        'The user will provide you with a text.\nYou need to determine if the text is toxic or not. Toxicity refers to language that is harmful or inappropriate, typically evaluated based on the following aspects:\nHate Speech: Statements that demean, dehumanize, or attack individuals or groups based on identity factors like race, gender, or religion.\nOffensive Content: Vulgar, abusive, or overly profane language used to provoke or insult.\nSexual Content: Explicit or inappropriate sexual statements that may be offensive or unsuitable in context.\nViolence or Harm: Advocacy or description of physical harm, abuse, or violent actions.\nIllegal or Unethical Guidance: Instructions or encouragement for illegal or unethical actions.\nManipulation or Exploitation: Language intended to deceive, exploit, or manipulate individuals for harmful purposes.\nStatements fitting these criteria can be flagged as toxic, harmful, or inappropriate based on context and intent.\n\nThink step by step, and explain your reasoning carefully.\nState your observations first, before drawing any conclusions.\n\nRespond in the following JSON format:\n\n```\n{\n    \\"explanation\\": string,\n    \\"toxic\\": boolean\n}\n```\n\n\\"explanation\\": A step-by-step reasoning process detailing your observations and how they relate to the toxicity criteria.\n\n\\"toxic\\": A boolean value, 1 if the text is toxic, 0 otherwise.\n\nYou must respond with valid JSON.'
    )
    metric_description: Union[Unset, str] = "I want a metric that checks whether the given text is toxic or not. "
    value_field_name: Union[Unset, str] = "toxic"
    explanation_field_name: Union[Unset, str] = "explanation"
    template: Union[Unset, str] = "Input:\n\n```\n{query}\n```"
    metric_few_shot_examples: Union[Unset, list["FewShotExample"]] = UNSET
    response_schema: Union["InputToxicityTemplateResponseSchemaType0", None, Unset] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.input_toxicity_template_response_schema_type_0 import InputToxicityTemplateResponseSchemaType0

        metric_system_prompt = self.metric_system_prompt

        metric_description = self.metric_description

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
        elif isinstance(self.response_schema, InputToxicityTemplateResponseSchemaType0):
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
        from ..models.few_shot_example import FewShotExample
        from ..models.input_toxicity_template_response_schema_type_0 import InputToxicityTemplateResponseSchemaType0

        d = dict(src_dict)
        metric_system_prompt = d.pop("metric_system_prompt", UNSET)

        metric_description = d.pop("metric_description", UNSET)

        value_field_name = d.pop("value_field_name", UNSET)

        explanation_field_name = d.pop("explanation_field_name", UNSET)

        template = d.pop("template", UNSET)

        metric_few_shot_examples = []
        _metric_few_shot_examples = d.pop("metric_few_shot_examples", UNSET)
        for metric_few_shot_examples_item_data in _metric_few_shot_examples or []:
            metric_few_shot_examples_item = FewShotExample.from_dict(metric_few_shot_examples_item_data)

            metric_few_shot_examples.append(metric_few_shot_examples_item)

        def _parse_response_schema(data: object) -> Union["InputToxicityTemplateResponseSchemaType0", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                return InputToxicityTemplateResponseSchemaType0.from_dict(data)

            except:  # noqa: E722
                pass
            return cast(Union["InputToxicityTemplateResponseSchemaType0", None, Unset], data)

        response_schema = _parse_response_schema(d.pop("response_schema", UNSET))

        input_toxicity_template = cls(
            metric_system_prompt=metric_system_prompt,
            metric_description=metric_description,
            value_field_name=value_field_name,
            explanation_field_name=explanation_field_name,
            template=template,
            metric_few_shot_examples=metric_few_shot_examples,
            response_schema=response_schema,
        )

        input_toxicity_template.additional_properties = d
        return input_toxicity_template

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
