from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.multimodal_capability import MultimodalCapability
from ..models.output_type_enum import OutputTypeEnum
from ..types import UNSET, Unset

T = TypeVar("T", bound="GeneratedScorerConfiguration")


@_attrs_define
class GeneratedScorerConfiguration:
    """
    Attributes
    ----------
        model_alias (Union[Unset, str]):  Default: 'gpt-4.1-mini'.
        num_judges (Union[Unset, int]):  Default: 3.
        output_type (Union[Unset, OutputTypeEnum]): Enumeration of output types.
        scoreable_node_types (Union[Unset, list[str]]): Types of nodes that can be scored by this scorer.
        cot_enabled (Union[Unset, bool]): Whether chain of thought is enabled for this scorer. Default: False.
        ground_truth (Union[Unset, bool]): Whether ground truth is enabled for this scorer. Default: False.
        multimodal_capabilities (Union[None, Unset, list[MultimodalCapability]]): Multimodal capabilities required by
            this scorer.
    """

    model_alias: Unset | str = "gpt-4.1-mini"
    num_judges: Unset | int = 3
    output_type: Unset | OutputTypeEnum = UNSET
    scoreable_node_types: Unset | list[str] = UNSET
    cot_enabled: Unset | bool = False
    ground_truth: Unset | bool = False
    multimodal_capabilities: None | Unset | list[MultimodalCapability] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        model_alias = self.model_alias

        num_judges = self.num_judges

        output_type: Unset | str = UNSET
        if not isinstance(self.output_type, Unset):
            output_type = self.output_type.value

        scoreable_node_types: Unset | list[str] = UNSET
        if not isinstance(self.scoreable_node_types, Unset):
            scoreable_node_types = self.scoreable_node_types

        cot_enabled = self.cot_enabled

        ground_truth = self.ground_truth

        multimodal_capabilities: None | Unset | list[str]
        if isinstance(self.multimodal_capabilities, Unset):
            multimodal_capabilities = UNSET
        elif isinstance(self.multimodal_capabilities, list):
            multimodal_capabilities = []
            for multimodal_capabilities_type_0_item_data in self.multimodal_capabilities:
                multimodal_capabilities_type_0_item = multimodal_capabilities_type_0_item_data.value
                multimodal_capabilities.append(multimodal_capabilities_type_0_item)

        else:
            multimodal_capabilities = self.multimodal_capabilities

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
        if multimodal_capabilities is not UNSET:
            field_dict["multimodal_capabilities"] = multimodal_capabilities

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        model_alias = d.pop("model_alias", UNSET)

        num_judges = d.pop("num_judges", UNSET)

        _output_type = d.pop("output_type", UNSET)
        output_type: Unset | OutputTypeEnum
        output_type = UNSET if isinstance(_output_type, Unset) else OutputTypeEnum(_output_type)

        scoreable_node_types = cast(list[str], d.pop("scoreable_node_types", UNSET))

        cot_enabled = d.pop("cot_enabled", UNSET)

        ground_truth = d.pop("ground_truth", UNSET)

        def _parse_multimodal_capabilities(data: object) -> None | Unset | list[MultimodalCapability]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                multimodal_capabilities_type_0 = []
                _multimodal_capabilities_type_0 = data
                for multimodal_capabilities_type_0_item_data in _multimodal_capabilities_type_0:
                    multimodal_capabilities_type_0_item = MultimodalCapability(multimodal_capabilities_type_0_item_data)

                    multimodal_capabilities_type_0.append(multimodal_capabilities_type_0_item)

                return multimodal_capabilities_type_0
            except:  # noqa: E722
                pass
            return cast(None | Unset | list[MultimodalCapability], data)

        multimodal_capabilities = _parse_multimodal_capabilities(d.pop("multimodal_capabilities", UNSET))

        generated_scorer_configuration = cls(
            model_alias=model_alias,
            num_judges=num_judges,
            output_type=output_type,
            scoreable_node_types=scoreable_node_types,
            cot_enabled=cot_enabled,
            ground_truth=ground_truth,
            multimodal_capabilities=multimodal_capabilities,
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
