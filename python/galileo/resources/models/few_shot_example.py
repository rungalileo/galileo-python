from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="FewShotExample")


@_attrs_define
class FewShotExample:
    """Few-shot example for a chainpoll metric prompt.

    Attributes:
        evaluating_response (str):
        generation_prompt_and_response (str):
    """

    evaluating_response: str
    generation_prompt_and_response: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        evaluating_response = self.evaluating_response

        generation_prompt_and_response = self.generation_prompt_and_response

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "evaluating_response": evaluating_response,
                "generation_prompt_and_response": generation_prompt_and_response,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        evaluating_response = d.pop("evaluating_response")

        generation_prompt_and_response = d.pop("generation_prompt_and_response")

        few_shot_example = cls(
            evaluating_response=evaluating_response, generation_prompt_and_response=generation_prompt_and_response
        )

        few_shot_example.additional_properties = d
        return few_shot_example

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
