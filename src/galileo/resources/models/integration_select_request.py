from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.integration_name import IntegrationName

T = TypeVar("T", bound="IntegrationSelectRequest")


@_attrs_define
class IntegrationSelectRequest:
    """
    Attributes:
        integration_name (IntegrationName):
        integration_id (str):
    """

    integration_name: IntegrationName
    integration_id: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        integration_name = self.integration_name.value

        integration_id = self.integration_id

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({"integration_name": integration_name, "integration_id": integration_id})

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        integration_name = IntegrationName(d.pop("integration_name"))

        integration_id = d.pop("integration_id")

        integration_select_request = cls(integration_name=integration_name, integration_id=integration_id)

        integration_select_request.additional_properties = d
        return integration_select_request

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
