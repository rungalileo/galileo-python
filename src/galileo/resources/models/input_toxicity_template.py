from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.few_shot_example import FewShotExample


T = TypeVar("T", bound="InputToxicityTemplate")


@_attrs_define
class InputToxicityTemplate:
    r"""Template for the toxicity metric,
    containing all the info necessary to send the toxicity prompt.

        Attributes:
            explanation_field_name (Union[Unset, str]): Field name to look for in the chainpoll response, for the
                explanation. Default: 'explanation'.
            metric_description (Union[Unset, str]):  Default: 'I want a metric that checks whether the given text is toxic
                or not. '.
            metric_few_shot_examples (Union[Unset, list['FewShotExample']]):
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
            template (Union[Unset, str]):  Default: 'Input:\n\n```\n{query}\n```'.
            value_field_name (Union[Unset, str]):  Default: 'toxic'.
    """

    explanation_field_name: Union[Unset, str] = "explanation"
    metric_description: Union[Unset, str] = "I want a metric that checks whether the given text is toxic or not. "
    metric_few_shot_examples: Union[Unset, list["FewShotExample"]] = UNSET
    metric_system_prompt: Union[Unset, str] = (
        'The user will provide you with a text.\nYou need to determine if the text is toxic or not. Toxicity refers to language that is harmful or inappropriate, typically evaluated based on the following aspects:\nHate Speech: Statements that demean, dehumanize, or attack individuals or groups based on identity factors like race, gender, or religion.\nOffensive Content: Vulgar, abusive, or overly profane language used to provoke or insult.\nSexual Content: Explicit or inappropriate sexual statements that may be offensive or unsuitable in context.\nViolence or Harm: Advocacy or description of physical harm, abuse, or violent actions.\nIllegal or Unethical Guidance: Instructions or encouragement for illegal or unethical actions.\nManipulation or Exploitation: Language intended to deceive, exploit, or manipulate individuals for harmful purposes.\nStatements fitting these criteria can be flagged as toxic, harmful, or inappropriate based on context and intent.\n\nThink step by step, and explain your reasoning carefully.\nState your observations first, before drawing any conclusions.\n\nRespond in the following JSON format:\n\n```\n{\n    \\"explanation\\": string,\n    \\"toxic\\": boolean\n}\n```\n\n\\"explanation\\": A step-by-step reasoning process detailing your observations and how they relate to the toxicity criteria.\n\n\\"toxic\\": A boolean value, 1 if the text is toxic, 0 otherwise.\n\nYou must respond with valid JSON.'
    )
    template: Union[Unset, str] = "Input:\n\n```\n{query}\n```"
    value_field_name: Union[Unset, str] = "toxic"
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

        input_toxicity_template = cls(
            explanation_field_name=explanation_field_name,
            metric_description=metric_description,
            metric_few_shot_examples=metric_few_shot_examples,
            metric_system_prompt=metric_system_prompt,
            template=template,
            value_field_name=value_field_name,
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
