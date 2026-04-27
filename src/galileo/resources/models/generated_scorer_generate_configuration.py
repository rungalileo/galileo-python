from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="GeneratedScorerGenerateConfiguration")


@_attrs_define
class GeneratedScorerGenerateConfiguration:
    """Info necessary to generate a scorer from instructions.

    Attributes:
        instructions (str):
        model_alias (str | Unset):  Default: 'gpt-4.1'.
    """

    instructions: str
    model_alias: str | Unset = "gpt-4.1"
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        instructions = self.instructions

        model_alias = self.model_alias

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({"instructions": instructions})
        if model_alias is not UNSET:
            field_dict["model_alias"] = model_alias

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        instructions = d.pop("instructions")

        model_alias = d.pop("model_alias", UNSET)

        generated_scorer_generate_configuration = cls(instructions=instructions, model_alias=model_alias)

        generated_scorer_generate_configuration.additional_properties = d
        return generated_scorer_generate_configuration

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
