from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.chain_poll_template_response_schema_type_0 import ChainPollTemplateResponseSchemaType0
    from ..models.few_shot_example import FewShotExample


T = TypeVar("T", bound="ChainPollTemplate")


@_attrs_define
class ChainPollTemplate:
    """Template for a chainpoll metric prompt,
    containing all the info necessary to send a chainpoll prompt.

    Attributes
    ----------
            template (str): Chainpoll prompt template.
            metric_system_prompt (Union[None, Unset, str]): System prompt for the metric.
            metric_description (Union[None, Unset, str]): Description of what the metric should do.
            value_field_name (Union[Unset, str]): Field name to look for in the chainpoll response, for the rating. Default:
                'rating'.
            explanation_field_name (Union[Unset, str]): Field name to look for in the chainpoll response, for the
                explanation. Default: 'explanation'.
            metric_few_shot_examples (Union[Unset, list['FewShotExample']]): Few-shot examples for the metric.
            response_schema (Union['ChainPollTemplateResponseSchemaType0', None, Unset]): Response schema for the output
    """

    template: str
    metric_system_prompt: Union[None, Unset, str] = UNSET
    metric_description: Union[None, Unset, str] = UNSET
    value_field_name: Union[Unset, str] = "rating"
    explanation_field_name: Union[Unset, str] = "explanation"
    metric_few_shot_examples: Union[Unset, list["FewShotExample"]] = UNSET
    response_schema: Union["ChainPollTemplateResponseSchemaType0", None, Unset] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.chain_poll_template_response_schema_type_0 import ChainPollTemplateResponseSchemaType0

        template = self.template

        metric_system_prompt: Union[None, Unset, str]
        metric_system_prompt = UNSET if isinstance(self.metric_system_prompt, Unset) else self.metric_system_prompt

        metric_description: Union[None, Unset, str]
        metric_description = UNSET if isinstance(self.metric_description, Unset) else self.metric_description

        value_field_name = self.value_field_name

        explanation_field_name = self.explanation_field_name

        metric_few_shot_examples: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.metric_few_shot_examples, Unset):
            metric_few_shot_examples = []
            for metric_few_shot_examples_item_data in self.metric_few_shot_examples:
                metric_few_shot_examples_item = metric_few_shot_examples_item_data.to_dict()
                metric_few_shot_examples.append(metric_few_shot_examples_item)

        response_schema: Union[None, Unset, dict[str, Any]]
        if isinstance(self.response_schema, Unset):
            response_schema = UNSET
        elif isinstance(self.response_schema, ChainPollTemplateResponseSchemaType0):
            response_schema = self.response_schema.to_dict()
        else:
            response_schema = self.response_schema

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({"template": template})
        if metric_system_prompt is not UNSET:
            field_dict["metric_system_prompt"] = metric_system_prompt
        if metric_description is not UNSET:
            field_dict["metric_description"] = metric_description
        if value_field_name is not UNSET:
            field_dict["value_field_name"] = value_field_name
        if explanation_field_name is not UNSET:
            field_dict["explanation_field_name"] = explanation_field_name
        if metric_few_shot_examples is not UNSET:
            field_dict["metric_few_shot_examples"] = metric_few_shot_examples
        if response_schema is not UNSET:
            field_dict["response_schema"] = response_schema

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.chain_poll_template_response_schema_type_0 import ChainPollTemplateResponseSchemaType0
        from ..models.few_shot_example import FewShotExample

        d = dict(src_dict)
        template = d.pop("template")

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

        metric_few_shot_examples = []
        _metric_few_shot_examples = d.pop("metric_few_shot_examples", UNSET)
        for metric_few_shot_examples_item_data in _metric_few_shot_examples or []:
            metric_few_shot_examples_item = FewShotExample.from_dict(metric_few_shot_examples_item_data)

            metric_few_shot_examples.append(metric_few_shot_examples_item)

        def _parse_response_schema(data: object) -> Union["ChainPollTemplateResponseSchemaType0", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                return ChainPollTemplateResponseSchemaType0.from_dict(data)

            except:  # noqa: E722
                pass
            return cast(Union["ChainPollTemplateResponseSchemaType0", None, Unset], data)

        response_schema = _parse_response_schema(d.pop("response_schema", UNSET))

        chain_poll_template = cls(
            template=template,
            metric_system_prompt=metric_system_prompt,
            metric_description=metric_description,
            value_field_name=value_field_name,
            explanation_field_name=explanation_field_name,
            metric_few_shot_examples=metric_few_shot_examples,
            response_schema=response_schema,
        )

        chain_poll_template.additional_properties = d
        return chain_poll_template

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
