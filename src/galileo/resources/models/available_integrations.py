from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.integration_name import IntegrationName

T = TypeVar("T", bound="AvailableIntegrations")


@_attrs_define
class AvailableIntegrations:
    """
    Attributes:
        integrations (list[IntegrationName]):
    """

    integrations: list[IntegrationName]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        integrations = []
        for integrations_item_data in self.integrations:
            integrations_item = integrations_item_data.value
            integrations.append(integrations_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({"integrations": integrations})

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        integrations = []
        _integrations = d.pop("integrations")
        for integrations_item_data in _integrations:
            integrations_item = IntegrationName(integrations_item_data)

            integrations.append(integrations_item)

        available_integrations = cls(integrations=integrations)

        available_integrations.additional_properties = d
        return available_integrations

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
