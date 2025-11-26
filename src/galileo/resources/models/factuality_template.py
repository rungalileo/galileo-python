from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.factuality_template_response_schema_type_0 import FactualityTemplateResponseSchemaType0
    from ..models.few_shot_example import FewShotExample


T = TypeVar("T", bound="FactualityTemplate")


@_attrs_define
class FactualityTemplate:
    r"""
    Attributes
    ----------
        metric_system_prompt (Union[Unset, str]):  Default: '# Task\n\nYou will be given a prompt that was sent to a
            large language model (LLM), and the LLM\'s response. Your task is to assess whether the response is factually
            correct.\n\n## Task output format\n\nYou must respond in the following JSON format:\n\n```\n{\n
            \\"explanation\\": string\n    \\"was_factual\\": boolean\n}\n```\n\n\\"explanation\\": Your step-by-step
            reasoning process. List out the claims made in the response, and for each claim, provide a detailed explanation
            of why that claim is or is not factual.\n\n\\"was_factual\\": `true` if the response was completely factually
            correct according to the instructions above, `false` otherwise.\n\nYou must respond with a valid JSON
            string.\n\n## Task guidelines\n\n### Input format\n\nIn some cases, the prompt may include multiple messages of
            chat history. If so, each message will begin with one of the following prefixes:\n\n- \\"System: \\"\n-
            \\"Human: \\"\n- \\"AI: \\"\n\n### How to determine the value of `was_factual`\n\n- was_factual should be false
            if anything in the response is factually incorrect, and true otherwise.\n- If the response omits some useful
            information, but does not include any falsehoods, was_factual should be true.\n- The prompt itself may contain
            false information. If the response repeats this false information, was_factual should be false. In other words,
            do not assume that the prompt is factually correct when evaluating the response.\n- If the prompt and response
            involve a domain where the concept of \\"factual accuracy\\" doesn\'t strictly apply, assess whatever quality of
            the response is most intuitively similar to factual accuracy. For example, if the prompt asks the LLM to write
            code, assess whether the code is free of syntax errors and implements the intended logic.\n\n### Writing the
            explanation\n\n- As stated above, a typical explanation should list out the claims made in the response, and for
            each claim, provide a detailed explanation of why that claim is or is not factual.\n- If the response doesn\'t
            make claims per se, break down the response into constituent parts in the most natural way given its content.
            For example, in code generation tasks, you might break down the response into individual functions or lines of
            code.\n- Work step by step, and do not give an overall assessment of the response until the end of your
            explanation.'.
        metric_description (Union[None, Unset, str]): Description of what the metric should do.
        value_field_name (Union[Unset, str]):  Default: 'was_factual'.
        explanation_field_name (Union[Unset, str]): Field name to look for in the chainpoll response, for the
            explanation. Default: 'explanation'.
        template (Union[Unset, str]):  Default: 'The prompt was:\n\n```\n{query}\n```\n\nThe response
            was:\n\n```\n{response}\n```\n\nRespond with a JSON object having two fields: `explanation` (string) and
            `was_factual` (boolean). Everything in your response should be valid JSON.\n\nREMEMBER: if the prompt asks the
            LLM to compose an answer on the basis of a \\"context\\" or other reference text or texts, you MUST IGNORE these
            texts when evaluating the response. Evaluate the response as though the reference texts were NOT provided. Do
            NOT refer to these texts in your evaluation.'.
        metric_few_shot_examples (Union[Unset, list['FewShotExample']]):
        response_schema (Union['FactualityTemplateResponseSchemaType0', None, Unset]): Response schema for the output.
    """

    metric_system_prompt: Union[Unset, str] = (
        '# Task\n\nYou will be given a prompt that was sent to a large language model (LLM), and the LLM\'s response. Your task is to assess whether the response is factually correct.\n\n## Task output format\n\nYou must respond in the following JSON format:\n\n```\n{\n    \\"explanation\\": string\n    \\"was_factual\\": boolean\n}\n```\n\n\\"explanation\\": Your step-by-step reasoning process. List out the claims made in the response, and for each claim, provide a detailed explanation of why that claim is or is not factual.\n\n\\"was_factual\\": `true` if the response was completely factually correct according to the instructions above, `false` otherwise.\n\nYou must respond with a valid JSON string.\n\n## Task guidelines\n\n### Input format\n\nIn some cases, the prompt may include multiple messages of chat history. If so, each message will begin with one of the following prefixes:\n\n- \\"System: \\"\n- \\"Human: \\"\n- \\"AI: \\"\n\n### How to determine the value of `was_factual`\n\n- was_factual should be false if anything in the response is factually incorrect, and true otherwise.\n- If the response omits some useful information, but does not include any falsehoods, was_factual should be true.\n- The prompt itself may contain false information. If the response repeats this false information, was_factual should be false. In other words, do not assume that the prompt is factually correct when evaluating the response.\n- If the prompt and response involve a domain where the concept of \\"factual accuracy\\" doesn\'t strictly apply, assess whatever quality of the response is most intuitively similar to factual accuracy. For example, if the prompt asks the LLM to write code, assess whether the code is free of syntax errors and implements the intended logic.\n\n### Writing the explanation\n\n- As stated above, a typical explanation should list out the claims made in the response, and for each claim, provide a detailed explanation of why that claim is or is not factual.\n- If the response doesn\'t make claims per se, break down the response into constituent parts in the most natural way given its content. For example, in code generation tasks, you might break down the response into individual functions or lines of code.\n- Work step by step, and do not give an overall assessment of the response until the end of your explanation.'
    )
    metric_description: Union[None, Unset, str] = UNSET
    value_field_name: Union[Unset, str] = "was_factual"
    explanation_field_name: Union[Unset, str] = "explanation"
    template: Union[Unset, str] = (
        'The prompt was:\n\n```\n{query}\n```\n\nThe response was:\n\n```\n{response}\n```\n\nRespond with a JSON object having two fields: `explanation` (string) and `was_factual` (boolean). Everything in your response should be valid JSON.\n\nREMEMBER: if the prompt asks the LLM to compose an answer on the basis of a \\"context\\" or other reference text or texts, you MUST IGNORE these texts when evaluating the response. Evaluate the response as though the reference texts were NOT provided. Do NOT refer to these texts in your evaluation.'
    )
    metric_few_shot_examples: Union[Unset, list["FewShotExample"]] = UNSET
    response_schema: Union["FactualityTemplateResponseSchemaType0", None, Unset] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.factuality_template_response_schema_type_0 import FactualityTemplateResponseSchemaType0

        metric_system_prompt = self.metric_system_prompt

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
        elif isinstance(self.response_schema, FactualityTemplateResponseSchemaType0):
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
        from ..models.factuality_template_response_schema_type_0 import FactualityTemplateResponseSchemaType0
        from ..models.few_shot_example import FewShotExample

        d = dict(src_dict)
        metric_system_prompt = d.pop("metric_system_prompt", UNSET)

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

        def _parse_response_schema(data: object) -> Union["FactualityTemplateResponseSchemaType0", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                return FactualityTemplateResponseSchemaType0.from_dict(data)

            except:  # noqa: E722
                pass
            return cast(Union["FactualityTemplateResponseSchemaType0", None, Unset], data)

        response_schema = _parse_response_schema(d.pop("response_schema", UNSET))

        factuality_template = cls(
            metric_system_prompt=metric_system_prompt,
            metric_description=metric_description,
            value_field_name=value_field_name,
            explanation_field_name=explanation_field_name,
            template=template,
            metric_few_shot_examples=metric_few_shot_examples,
            response_schema=response_schema,
        )

        factuality_template.additional_properties = d
        return factuality_template

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
