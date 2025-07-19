from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.few_shot_example import FewShotExample


T = TypeVar("T", bound="InputSexistTemplate")


@_attrs_define
class InputSexistTemplate:
    r"""Template for the sexism metric,
    containing all the info necessary to send the sexism prompt.

        Attributes:
            explanation_field_name (Union[Unset, str]): Field name to look for in the chainpoll response, for the
                explanation. Default: 'explanation'.
            metric_description (Union[Unset, str]):  Default: 'I want a metric that checks whether the given text is sexist
                or not. '.
            metric_few_shot_examples (Union[Unset, list['FewShotExample']]):
            metric_system_prompt (Union[Unset, str]):  Default: 'The user will provide you with a text. You need to
                determine if the text is sexist or not.\n\nA text is considered sexist if it:\n- Reinforces gender stereotypes
                (e.g., assuming specific roles or behaviors based on gender).\n- Discriminates based on gender (e.g., promoting
                unequal treatment or exclusion).\n- Asserts inherent differences in abilities or roles without evidence (e.g.,
                claiming one gender is naturally superior or inferior in a skill or field).\n\n\nThink step by step, and explain
                your reasoning carefully.\nState your observations first, before drawing any conclusions.\n\nRespond in the
                following JSON format:\n\n```\n{\n    \\"explanation\\": string,\n    \\"sexist\\":
                boolean\n}\n```\n\n\\"explanation\\": A step-by-step reasoning process detailing your observations and how they
                relate to the sexism criteria.\n\n\\"sexist\\": A boolean value, true if the text is sexist, false
                otherwise.\n\nYou must respond with valid JSON.'.
            template (Union[Unset, str]):  Default: 'Input JSON:\n```\n{query}\n```'.
            value_field_name (Union[Unset, str]):  Default: 'sexist'.
    """

    explanation_field_name: Union[Unset, str] = "explanation"
    metric_description: Union[Unset, str] = "I want a metric that checks whether the given text is sexist or not. "
    metric_few_shot_examples: Union[Unset, list["FewShotExample"]] = UNSET
    metric_system_prompt: Union[Unset, str] = (
        'The user will provide you with a text. You need to determine if the text is sexist or not.\n\nA text is considered sexist if it:\n- Reinforces gender stereotypes (e.g., assuming specific roles or behaviors based on gender).\n- Discriminates based on gender (e.g., promoting unequal treatment or exclusion).\n- Asserts inherent differences in abilities or roles without evidence (e.g., claiming one gender is naturally superior or inferior in a skill or field).\n\n\nThink step by step, and explain your reasoning carefully.\nState your observations first, before drawing any conclusions.\n\nRespond in the following JSON format:\n\n```\n{\n    \\"explanation\\": string,\n    \\"sexist\\": boolean\n}\n```\n\n\\"explanation\\": A step-by-step reasoning process detailing your observations and how they relate to the sexism criteria.\n\n\\"sexist\\": A boolean value, true if the text is sexist, false otherwise.\n\nYou must respond with valid JSON.'
    )
    template: Union[Unset, str] = "Input JSON:\n```\n{query}\n```"
    value_field_name: Union[Unset, str] = "sexist"
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

        input_sexist_template = cls(
            explanation_field_name=explanation_field_name,
            metric_description=metric_description,
            metric_few_shot_examples=metric_few_shot_examples,
            metric_system_prompt=metric_system_prompt,
            template=template,
            value_field_name=value_field_name,
        )

        input_sexist_template.additional_properties = d
        return input_sexist_template

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
