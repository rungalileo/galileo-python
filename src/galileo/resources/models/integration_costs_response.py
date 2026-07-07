from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.feature_integration_costs import FeatureIntegrationCosts


T = TypeVar("T", bound="IntegrationCostsResponse")


@_attrs_define
class IntegrationCostsResponse:
    """
    Attributes:
        features (Union[Unset, list['FeatureIntegrationCosts']]):
    """

    features: Union[Unset, list["FeatureIntegrationCosts"]] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        features: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.features, Unset):
            features = []
            for features_item_data in self.features:
                features_item = features_item_data.to_dict()
                features.append(features_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if features is not UNSET:
            field_dict["features"] = features

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.feature_integration_costs import FeatureIntegrationCosts

        d = dict(src_dict)
        features = []
        _features = d.pop("features", UNSET)
        for features_item_data in _features or []:
            features_item = FeatureIntegrationCosts.from_dict(features_item_data)

            features.append(features_item)

        integration_costs_response = cls(features=features)

        integration_costs_response.additional_properties = d
        return integration_costs_response

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
