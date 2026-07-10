from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.recommended_models_response_available import RecommendedModelsResponseAvailable
    from ..models.recommended_models_response_supported import RecommendedModelsResponseSupported


T = TypeVar("T", bound="RecommendedModelsResponse")


@_attrs_define
class RecommendedModelsResponse:
    """
    Attributes
    ----------
        supported (RecommendedModelsResponseSupported):
        available (RecommendedModelsResponseAvailable):
    """

    supported: "RecommendedModelsResponseSupported"
    available: "RecommendedModelsResponseAvailable"
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        supported = self.supported.to_dict()

        available = self.available.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({"supported": supported, "available": available})

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.recommended_models_response_available import RecommendedModelsResponseAvailable
        from ..models.recommended_models_response_supported import RecommendedModelsResponseSupported

        d = dict(src_dict)
        supported = RecommendedModelsResponseSupported.from_dict(d.pop("supported"))

        available = RecommendedModelsResponseAvailable.from_dict(d.pop("available"))

        recommended_models_response = cls(supported=supported, available=available)

        recommended_models_response.additional_properties = d
        return recommended_models_response

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
