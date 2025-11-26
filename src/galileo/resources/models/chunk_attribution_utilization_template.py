from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.chunk_attribution_utilization_template_response_schema_type_0 import (
        ChunkAttributionUtilizationTemplateResponseSchemaType0,
    )
    from ..models.few_shot_example import FewShotExample


T = TypeVar("T", bound="ChunkAttributionUtilizationTemplate")


@_attrs_define
class ChunkAttributionUtilizationTemplate:
    r"""
    Attributes
    ----------
        metric_system_prompt (Union[None, Unset, str]): System prompt for the metric.
        metric_description (Union[None, Unset, str]): Description of what the metric should do.
        value_field_name (Union[Unset, str]): Field name to look for in the chainpoll response, for the rating. Default:
            'rating'.
        explanation_field_name (Union[Unset, str]): Field name to look for in the chainpoll response, for the
            explanation. Default: 'explanation'.
        template (Union[Unset, str]):  Default: 'I asked someone to answer a question based on one or more documents.
            You will tell me which of the documents their answer was sourced from, and which specific sentences from the
            documents they used.\n\nHere are the documents, with each document split up into sentences. Each sentence is
            given a unique key, such as \'0a\' for the first sentence of Document 0. You\'ll use these keys in your response
            to identify which sentences were used.\n\n```\n{chunks}\n```\n\nThe question
            was:\n\n```\n{question}\n```\n\nTheir response was:\n\n```\n{response}\n```\n\nRespond with a JSON object
            matching this schema:\n\n```\n{{\n  \\"source_sentence_keys\\": [string]\n}}\n```\n\nThe source_sentence_keys
            field is a list identifying the sentences in the documents that were used to construct the answer. Each entry
            MUST be a sentence key, such as \'0a\', that appears in the document list above. Include the key of every
            sentence that was used to construct the answer, even if it was not used in its entirety. Omit keys for sentences
            that were not used, and could have been removed from the document without affecting the answer.\n\nYou must
            respond with a valid JSON string.'.
        metric_few_shot_examples (Union[Unset, list['FewShotExample']]): Few-shot examples for the metric.
        response_schema (Union['ChunkAttributionUtilizationTemplateResponseSchemaType0', None, Unset]): Response schema
            for the output.
    """

    metric_system_prompt: Union[None, Unset, str] = UNSET
    metric_description: Union[None, Unset, str] = UNSET
    value_field_name: Union[Unset, str] = "rating"
    explanation_field_name: Union[Unset, str] = "explanation"
    template: Union[Unset, str] = (
        "I asked someone to answer a question based on one or more documents. You will tell me which of the documents their answer was sourced from, and which specific sentences from the documents they used.\n\nHere are the documents, with each document split up into sentences. Each sentence is given a unique key, such as '0a' for the first sentence of Document 0. You'll use these keys in your response to identify which sentences were used.\n\n```\n{chunks}\n```\n\nThe question was:\n\n```\n{question}\n```\n\nTheir response was:\n\n```\n{response}\n```\n\nRespond with a JSON object matching this schema:\n\n```\n{{\n  \\\"source_sentence_keys\\\": [string]\n}}\n```\n\nThe source_sentence_keys field is a list identifying the sentences in the documents that were used to construct the answer. Each entry MUST be a sentence key, such as '0a', that appears in the document list above. Include the key of every sentence that was used to construct the answer, even if it was not used in its entirety. Omit keys for sentences that were not used, and could have been removed from the document without affecting the answer.\n\nYou must respond with a valid JSON string."
    )
    metric_few_shot_examples: Union[Unset, list["FewShotExample"]] = UNSET
    response_schema: Union["ChunkAttributionUtilizationTemplateResponseSchemaType0", None, Unset] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.chunk_attribution_utilization_template_response_schema_type_0 import (
            ChunkAttributionUtilizationTemplateResponseSchemaType0,
        )

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
        elif isinstance(self.response_schema, ChunkAttributionUtilizationTemplateResponseSchemaType0):
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
        from ..models.chunk_attribution_utilization_template_response_schema_type_0 import (
            ChunkAttributionUtilizationTemplateResponseSchemaType0,
        )
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

        def _parse_response_schema(
            data: object,
        ) -> Union["ChunkAttributionUtilizationTemplateResponseSchemaType0", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                return ChunkAttributionUtilizationTemplateResponseSchemaType0.from_dict(data)

            except:  # noqa: E722
                pass
            return cast(Union["ChunkAttributionUtilizationTemplateResponseSchemaType0", None, Unset], data)

        response_schema = _parse_response_schema(d.pop("response_schema", UNSET))

        chunk_attribution_utilization_template = cls(
            metric_system_prompt=metric_system_prompt,
            metric_description=metric_description,
            value_field_name=value_field_name,
            explanation_field_name=explanation_field_name,
            template=template,
            metric_few_shot_examples=metric_few_shot_examples,
            response_schema=response_schema,
        )

        chunk_attribution_utilization_template.additional_properties = d
        return chunk_attribution_utilization_template

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
