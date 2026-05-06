from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.content_modality import ContentModality
from ..models.multimodal_capability import MultimodalCapability
from ..types import UNSET, Unset

T = TypeVar("T", bound="ModelProperties")


@_attrs_define
class ModelProperties:
    """
    Attributes
    ----------
        alias (str):
        name (str):
        input_modalities (list[ContentModality]):
        multimodal_capabilities (Union[Unset, list[MultimodalCapability]]):
    """

    alias: str
    name: str
    input_modalities: list[ContentModality]
    multimodal_capabilities: Unset | list[MultimodalCapability] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        alias = self.alias

        name = self.name

        input_modalities = []
        for input_modalities_item_data in self.input_modalities:
            input_modalities_item = input_modalities_item_data.value
            input_modalities.append(input_modalities_item)

        multimodal_capabilities: Unset | list[str] = UNSET
        if not isinstance(self.multimodal_capabilities, Unset):
            multimodal_capabilities = []
            for multimodal_capabilities_item_data in self.multimodal_capabilities:
                multimodal_capabilities_item = multimodal_capabilities_item_data.value
                multimodal_capabilities.append(multimodal_capabilities_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({"alias": alias, "name": name, "input_modalities": input_modalities})
        if multimodal_capabilities is not UNSET:
            field_dict["multimodal_capabilities"] = multimodal_capabilities

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        alias = d.pop("alias")

        name = d.pop("name")

        input_modalities = []
        _input_modalities = d.pop("input_modalities")
        for input_modalities_item_data in _input_modalities:
            input_modalities_item = ContentModality(input_modalities_item_data)

            input_modalities.append(input_modalities_item)

        multimodal_capabilities = []
        _multimodal_capabilities = d.pop("multimodal_capabilities", UNSET)
        for multimodal_capabilities_item_data in _multimodal_capabilities or []:
            multimodal_capabilities_item = MultimodalCapability(multimodal_capabilities_item_data)

            multimodal_capabilities.append(multimodal_capabilities_item)

        model_properties = cls(
            alias=alias, name=name, input_modalities=input_modalities, multimodal_capabilities=multimodal_capabilities
        )

        model_properties.additional_properties = d
        return model_properties

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
