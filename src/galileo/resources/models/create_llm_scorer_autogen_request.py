from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.output_type_enum import OutputTypeEnum

T = TypeVar("T", bound="CreateLLMScorerAutogenRequest")


@_attrs_define
class CreateLLMScorerAutogenRequest:
    """
    Attributes:
        cot_enabled (bool):
        instructions (str):
        model_name (str):
        output_type (OutputTypeEnum): Enumeration of output types.
        scoreable_node_types (list[str]):
    """

    cot_enabled: bool
    instructions: str
    model_name: str
    output_type: OutputTypeEnum
    scoreable_node_types: list[str]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        cot_enabled = self.cot_enabled

        instructions = self.instructions

        model_name = self.model_name

        output_type = self.output_type.value

        scoreable_node_types = self.scoreable_node_types

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "cot_enabled": cot_enabled,
                "instructions": instructions,
                "model_name": model_name,
                "output_type": output_type,
                "scoreable_node_types": scoreable_node_types,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        cot_enabled = d.pop("cot_enabled")

        instructions = d.pop("instructions")

        model_name = d.pop("model_name")

        output_type = OutputTypeEnum(d.pop("output_type"))

        scoreable_node_types = cast(list[str], d.pop("scoreable_node_types"))

        create_llm_scorer_autogen_request = cls(
            cot_enabled=cot_enabled,
            instructions=instructions,
            model_name=model_name,
            output_type=output_type,
            scoreable_node_types=scoreable_node_types,
        )

        create_llm_scorer_autogen_request.additional_properties = d
        return create_llm_scorer_autogen_request

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
