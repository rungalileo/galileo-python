from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.output_type_enum import OutputTypeEnum
from ..types import UNSET, Unset

T = TypeVar("T", bound="GeneratedScorerConfiguration")


@_attrs_define
class GeneratedScorerConfiguration:
    """
    Attributes
    ----------
        model_alias (str | Unset):  Default: 'gpt-4.1-mini'.
        num_judges (int | Unset):  Default: 3.
        output_type (OutputTypeEnum | Unset): Enumeration of output types.
        scoreable_node_types (list[str] | Unset): Types of nodes that can be scored by this scorer.
        cot_enabled (bool | Unset): Whether chain of thought is enabled for this scorer. Default: False.
        ground_truth (bool | Unset): Whether ground truth is enabled for this scorer. Default: False.
    """

    model_alias: str | Unset = "gpt-4.1-mini"
    num_judges: int | Unset = 3
    output_type: OutputTypeEnum | Unset = UNSET
    scoreable_node_types: list[str] | Unset = UNSET
    cot_enabled: bool | Unset = False
    ground_truth: bool | Unset = False
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        model_alias = self.model_alias

        num_judges = self.num_judges

        output_type: str | Unset = UNSET
        if not isinstance(self.output_type, Unset):
            output_type = self.output_type.value

        scoreable_node_types: list[str] | Unset = UNSET
        if not isinstance(self.scoreable_node_types, Unset):
            scoreable_node_types = self.scoreable_node_types

        cot_enabled = self.cot_enabled

        ground_truth = self.ground_truth

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if model_alias is not UNSET:
            field_dict["model_alias"] = model_alias
        if num_judges is not UNSET:
            field_dict["num_judges"] = num_judges
        if output_type is not UNSET:
            field_dict["output_type"] = output_type
        if scoreable_node_types is not UNSET:
            field_dict["scoreable_node_types"] = scoreable_node_types
        if cot_enabled is not UNSET:
            field_dict["cot_enabled"] = cot_enabled
        if ground_truth is not UNSET:
            field_dict["ground_truth"] = ground_truth

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        model_alias = d.pop("model_alias", UNSET)

        num_judges = d.pop("num_judges", UNSET)

        _output_type = d.pop("output_type", UNSET)
        output_type: OutputTypeEnum | Unset
        output_type = UNSET if isinstance(_output_type, Unset) else OutputTypeEnum(_output_type)

        scoreable_node_types = cast(list[str], d.pop("scoreable_node_types", UNSET))

        cot_enabled = d.pop("cot_enabled", UNSET)

        ground_truth = d.pop("ground_truth", UNSET)

        generated_scorer_configuration = cls(
            model_alias=model_alias,
            num_judges=num_judges,
            output_type=output_type,
            scoreable_node_types=scoreable_node_types,
            cot_enabled=cot_enabled,
            ground_truth=ground_truth,
        )

        generated_scorer_configuration.additional_properties = d
        return generated_scorer_configuration

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
