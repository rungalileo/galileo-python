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

    Attributes
    ----------
        prompt (str):
        evaluation_criteria (str):
        task_description (str):
        includes_target (bool):
        num_rows (int):
        iterations (int):
        max_tokens (int):
        temperature (float):
        generation_model_alias (str):
        evaluation_model_alias (str):
        integration_name (Union[Unset, LLMIntegration]):
        reasoning_effort (Union[None, Unset, str]):
        verbosity (Union[None, Unset, str]):
    """

    prompt: str
    evaluation_criteria: str
    task_description: str
    includes_target: bool
    num_rows: int
    iterations: int
    max_tokens: int
    temperature: float
    generation_model_alias: str
    evaluation_model_alias: str
    integration_name: Union[Unset, LLMIntegration] = UNSET
    reasoning_effort: Union[None, Unset, str] = UNSET
    verbosity: Union[None, Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        prompt = self.prompt

        evaluation_criteria = self.evaluation_criteria

        task_description = self.task_description

        includes_target = self.includes_target

        num_rows = self.num_rows

        iterations = self.iterations

        max_tokens = self.max_tokens

        temperature = self.temperature

        generation_model_alias = self.generation_model_alias

        evaluation_model_alias = self.evaluation_model_alias

        integration_name: Union[Unset, str] = UNSET
        if not isinstance(self.integration_name, Unset):
            integration_name = self.integration_name.value

        reasoning_effort: Union[None, Unset, str]
        reasoning_effort = UNSET if isinstance(self.reasoning_effort, Unset) else self.reasoning_effort

        verbosity: Union[None, Unset, str]
        verbosity = UNSET if isinstance(self.verbosity, Unset) else self.verbosity

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "prompt": prompt,
                "evaluation_criteria": evaluation_criteria,
                "task_description": task_description,
                "includes_target": includes_target,
                "num_rows": num_rows,
                "iterations": iterations,
                "max_tokens": max_tokens,
                "temperature": temperature,
                "generation_model_alias": generation_model_alias,
                "evaluation_model_alias": evaluation_model_alias,
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
        prompt = d.pop("prompt")

        evaluation_criteria = d.pop("evaluation_criteria")

        task_description = d.pop("task_description")

        includes_target = d.pop("includes_target")

        num_rows = d.pop("num_rows")

        iterations = d.pop("iterations")

        max_tokens = d.pop("max_tokens")

        temperature = d.pop("temperature")

        generation_model_alias = d.pop("generation_model_alias")

        evaluation_model_alias = d.pop("evaluation_model_alias")

        _integration_name = d.pop("integration_name", UNSET)
        integration_name: Union[Unset, LLMIntegration]
        integration_name = UNSET if isinstance(_integration_name, Unset) else LLMIntegration(_integration_name)

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
            prompt=prompt,
            evaluation_criteria=evaluation_criteria,
            task_description=task_description,
            includes_target=includes_target,
            num_rows=num_rows,
            iterations=iterations,
            max_tokens=max_tokens,
            temperature=temperature,
            generation_model_alias=generation_model_alias,
            evaluation_model_alias=evaluation_model_alias,
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
