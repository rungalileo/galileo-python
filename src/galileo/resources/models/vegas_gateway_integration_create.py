from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="VegasGatewayIntegrationCreate")


@_attrs_define
class VegasGatewayIntegrationCreate:
    """
    Attributes
    ----------
        endpoint (str):
        token (str):
        use_case (str):
    """

    endpoint: str
    token: str
    use_case: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        endpoint = self.endpoint

        token = self.token

        use_case = self.use_case

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({"endpoint": endpoint, "token": token, "use_case": use_case})

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        endpoint = d.pop("endpoint")

        token = d.pop("token")

        use_case = d.pop("use_case")

        vegas_gateway_integration_create = cls(endpoint=endpoint, token=token, use_case=use_case)

        vegas_gateway_integration_create.additional_properties = d
        return vegas_gateway_integration_create

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
