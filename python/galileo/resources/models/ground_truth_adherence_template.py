from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.few_shot_example import FewShotExample


T = TypeVar("T", bound="GroundTruthAdherenceTemplate")


@_attrs_define
class GroundTruthAdherenceTemplate:
    r"""
    Attributes:
        explanation_field_name (Union[Unset, str]): Field name to look for in the chainpoll response, for the
            explanation. Default: 'explanation'.
        metric_description (Union[Unset, str]):  Default: 'This metric computes whether a response from a large language
            model matches a provided ground truth text.'.
        metric_few_shot_examples (Union[Unset, list['FewShotExample']]): Few-shot examples for the metric.
        metric_system_prompt (Union[Unset, str]):  Default: 'I will give you two different texts, called the \\"ground
            truth\\" and the \\"response.\\"\n\nRead both texts, then tell me whether they are \\"equivalent,\\" in the
            sense that they basically mean the same thing.\n\nKeep the following guidelines in mind.\n\n- Two texts can be
            equivalent if they use different phrasing, as long as the phrasing doesn\'t affect meaning.\n- Two texts can be
            equivalent if there are _slight_ differences in meaning that wouldn\'t affect the conclusions that a reasonable
            reader would draw upon reading them.\n- Imagine that you are grading a free-response exam.  The ground truth
            given in the answer key for an exam question, and the response is a student\'s answer to the same question. If
            you would give the student full marks for this question, that means the two texts are equivalent. If you
            wouldn\'t, that means the two texts are not equivalent.\n\nRespond in the following JSON format:\n\n```\n{{\n
            \\"explanation\\": string,\n    \\"equivalent\\": boolean\n}}\n```\n\n\\"explanation\\": A step-by-step
            breakdown of the similarities and differences between the text. For each difference you note (if any), consider
            why the difference might or might not make the texts non-equivalent, note down your reasoning clearly and
            explicitly, and ultimately draw a conclusion about whether that difference makes the text non-
            equivalent.\n\n\\"equivalent\\": `true` if the texts are equivalent in the sense given above, `false` if they
            are non-equivalent.\n\nYou must respond with valid JSON.'.
        template (Union[Unset, str]):  Default: 'Ground
            truth:\n\n```\n{ground_truth}\n```\n\nResponse:\n\n```\n{response}\n```'.
        value_field_name (Union[Unset, str]):  Default: 'equivalent'.
    """

    explanation_field_name: Union[Unset, str] = "explanation"
    metric_description: Union[Unset, str] = (
        "This metric computes whether a response from a large language model matches a provided ground truth text."
    )
    metric_few_shot_examples: Union[Unset, list["FewShotExample"]] = UNSET
    metric_system_prompt: Union[Unset, str] = (
        'I will give you two different texts, called the \\"ground truth\\" and the \\"response.\\"\n\nRead both texts, then tell me whether they are \\"equivalent,\\" in the sense that they basically mean the same thing.\n\nKeep the following guidelines in mind.\n\n- Two texts can be equivalent if they use different phrasing, as long as the phrasing doesn\'t affect meaning.\n- Two texts can be equivalent if there are _slight_ differences in meaning that wouldn\'t affect the conclusions that a reasonable reader would draw upon reading them.\n- Imagine that you are grading a free-response exam.  The ground truth given in the answer key for an exam question, and the response is a student\'s answer to the same question. If you would give the student full marks for this question, that means the two texts are equivalent. If you wouldn\'t, that means the two texts are not equivalent.\n\nRespond in the following JSON format:\n\n```\n{{\n    \\"explanation\\": string,\n    \\"equivalent\\": boolean\n}}\n```\n\n\\"explanation\\": A step-by-step breakdown of the similarities and differences between the text. For each difference you note (if any), consider why the difference might or might not make the texts non-equivalent, note down your reasoning clearly and explicitly, and ultimately draw a conclusion about whether that difference makes the text non-equivalent.\n\n\\"equivalent\\": `true` if the texts are equivalent in the sense given above, `false` if they are non-equivalent.\n\nYou must respond with valid JSON.'
    )
    template: Union[Unset, str] = "Ground truth:\n\n```\n{ground_truth}\n```\n\nResponse:\n\n```\n{response}\n```"
    value_field_name: Union[Unset, str] = "equivalent"
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

        ground_truth_adherence_template = cls(
            explanation_field_name=explanation_field_name,
            metric_description=metric_description,
            metric_few_shot_examples=metric_few_shot_examples,
            metric_system_prompt=metric_system_prompt,
            template=template,
            value_field_name=value_field_name,
        )

        ground_truth_adherence_template.additional_properties = d
        return ground_truth_adherence_template

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
