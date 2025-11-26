from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.output_type_enum import OutputTypeEnum

T = TypeVar("T", bound="CreateLLMScorerAutogenRequest")


@_attrs_define
class CreateLLMScorerAutogenRequest:
    """
    Attributes
    ----------
        instructions (str):
        model_name (str):
        output_type (OutputTypeEnum): Enumeration of output types.
        cot_enabled (bool):
        scoreable_node_types (list[str]):
    """

    instructions: str
    model_name: str
    output_type: OutputTypeEnum
    cot_enabled: bool
    scoreable_node_types: list[str]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        instructions = self.instructions

        model_name = self.model_name

        output_type = self.output_type.value

        cot_enabled = self.cot_enabled

        scoreable_node_types = self.scoreable_node_types

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "instructions": instructions,
                "model_name": model_name,
                "output_type": output_type,
                "cot_enabled": cot_enabled,
                "scoreable_node_types": scoreable_node_types,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        instructions = d.pop("instructions")

        model_name = d.pop("model_name")

        output_type = OutputTypeEnum(d.pop("output_type"))

        cot_enabled = d.pop("cot_enabled")

        scoreable_node_types = cast(list[str], d.pop("scoreable_node_types"))

        create_llm_scorer_autogen_request = cls(
            instructions=instructions,
            model_name=model_name,
            output_type=output_type,
            cot_enabled=cot_enabled,
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
