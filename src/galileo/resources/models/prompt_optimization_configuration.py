from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.llm_integration import LLMIntegration
from ..types import UNSET, Unset

T = TypeVar("T", bound="PromptOptimizationConfiguration")


@_attrs_define
class PromptOptimizationConfiguration:
    """Configuration for prompt optimization.

    Attributes:
        evaluation_criteria (str):
        evaluation_model_alias (str):
        generation_model_alias (str):
        includes_target (bool):
        iterations (int):
        max_tokens (int):
        num_rows (int):
        prompt (str):
        task_description (str):
        temperature (float):
        integration_name (Union[Unset, LLMIntegration]):
        reasoning_effort (Union[None, Unset, str]):
        verbosity (Union[None, Unset, str]):
    """

    evaluation_criteria: str
    evaluation_model_alias: str
    generation_model_alias: str
    includes_target: bool
    iterations: int
    max_tokens: int
    num_rows: int
    prompt: str
    task_description: str
    temperature: float
    integration_name: Union[Unset, LLMIntegration] = UNSET
    reasoning_effort: Union[None, Unset, str] = UNSET
    verbosity: Union[None, Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        evaluation_criteria = self.evaluation_criteria

        evaluation_model_alias = self.evaluation_model_alias

        generation_model_alias = self.generation_model_alias

        includes_target = self.includes_target

        iterations = self.iterations

        max_tokens = self.max_tokens

        num_rows = self.num_rows

        prompt = self.prompt

        task_description = self.task_description

        temperature = self.temperature

        integration_name: Union[Unset, str] = UNSET
        if not isinstance(self.integration_name, Unset):
            integration_name = self.integration_name.value

        reasoning_effort: Union[None, Unset, str]
        if isinstance(self.reasoning_effort, Unset):
            reasoning_effort = UNSET
        else:
            reasoning_effort = self.reasoning_effort

        verbosity: Union[None, Unset, str]
        if isinstance(self.verbosity, Unset):
            verbosity = UNSET
        else:
            verbosity = self.verbosity

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "evaluation_criteria": evaluation_criteria,
                "evaluation_model_alias": evaluation_model_alias,
                "generation_model_alias": generation_model_alias,
                "includes_target": includes_target,
                "iterations": iterations,
                "max_tokens": max_tokens,
                "num_rows": num_rows,
                "prompt": prompt,
                "task_description": task_description,
                "temperature": temperature,
            }
        )
        if integration_name is not UNSET:
            field_dict["integration_name"] = integration_name
        if reasoning_effort is not UNSET:
            field_dict["reasoning_effort"] = reasoning_effort
        if verbosity is not UNSET:
            field_dict["verbosity"] = verbosity

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        evaluation_criteria = d.pop("evaluation_criteria")

        evaluation_model_alias = d.pop("evaluation_model_alias")

        generation_model_alias = d.pop("generation_model_alias")

        includes_target = d.pop("includes_target")

        iterations = d.pop("iterations")

        max_tokens = d.pop("max_tokens")

        num_rows = d.pop("num_rows")

        prompt = d.pop("prompt")

        task_description = d.pop("task_description")

        temperature = d.pop("temperature")

        _integration_name = d.pop("integration_name", UNSET)
        integration_name: Union[Unset, LLMIntegration]
        if isinstance(_integration_name, Unset):
            integration_name = UNSET
        else:
            integration_name = LLMIntegration(_integration_name)

        def _parse_reasoning_effort(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        reasoning_effort = _parse_reasoning_effort(d.pop("reasoning_effort", UNSET))

        def _parse_verbosity(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        verbosity = _parse_verbosity(d.pop("verbosity", UNSET))

        prompt_optimization_configuration = cls(
            evaluation_criteria=evaluation_criteria,
            evaluation_model_alias=evaluation_model_alias,
            generation_model_alias=generation_model_alias,
            includes_target=includes_target,
            iterations=iterations,
            max_tokens=max_tokens,
            num_rows=num_rows,
            prompt=prompt,
            task_description=task_description,
            temperature=temperature,
            integration_name=integration_name,
            reasoning_effort=reasoning_effort,
            verbosity=verbosity,
        )

        prompt_optimization_configuration.additional_properties = d
        return prompt_optimization_configuration

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
