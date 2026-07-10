from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.recommended_models_response_supported_additional_property import (
        RecommendedModelsResponseSupportedAdditionalProperty,
    )


T = TypeVar("T", bound="RecommendedModelsResponseSupported")


@_attrs_define
class RecommendedModelsResponseSupported:
    """ """

    additional_properties: dict[str, "RecommendedModelsResponseSupportedAdditionalProperty"] = _attrs_field(
        init=False, factory=dict
    )

    def to_dict(self) -> dict[str, Any]:
        field_dict: dict[str, Any] = {}
        for prop_name, prop in self.additional_properties.items():
            field_dict[prop_name] = prop.to_dict()

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.recommended_models_response_supported_additional_property import (
            RecommendedModelsResponseSupportedAdditionalProperty,
        )

        d = dict(src_dict)
        recommended_models_response_supported = cls()

        additional_properties = {}
        for prop_name, prop_dict in d.items():
            additional_property = RecommendedModelsResponseSupportedAdditionalProperty.from_dict(prop_dict)

            additional_properties[prop_name] = additional_property

        recommended_models_response_supported.additional_properties = additional_properties
        return recommended_models_response_supported

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> "RecommendedModelsResponseSupportedAdditionalProperty":
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: "RecommendedModelsResponseSupportedAdditionalProperty") -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
