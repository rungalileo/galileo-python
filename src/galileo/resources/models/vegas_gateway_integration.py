from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, Literal, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.vegas_gateway_integration_extra_type_0 import VegasGatewayIntegrationExtraType0


T = TypeVar("T", bound="VegasGatewayIntegration")


@_attrs_define
class VegasGatewayIntegration:
    """
    Attributes:
        id (None | str | Unset):
        name (Literal['vegas_gateway'] | Unset):  Default: 'vegas_gateway'.
        extra (None | Unset | VegasGatewayIntegrationExtraType0):
    """

    id: None | str | Unset = UNSET
    name: Literal["vegas_gateway"] | Unset = "vegas_gateway"
    extra: None | Unset | VegasGatewayIntegrationExtraType0 = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.vegas_gateway_integration_extra_type_0 import VegasGatewayIntegrationExtraType0

        id: None | str | Unset
        if isinstance(self.id, Unset):
            id = UNSET
        else:
            id = self.id

        name = self.name

        extra: dict[str, Any] | None | Unset
        if isinstance(self.extra, Unset):
            extra = UNSET
        elif isinstance(self.extra, VegasGatewayIntegrationExtraType0):
            extra = self.extra.to_dict()
        else:
            extra = self.extra

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if id is not UNSET:
            field_dict["id"] = id
        if name is not UNSET:
            field_dict["name"] = name
        if extra is not UNSET:
            field_dict["extra"] = extra

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.vegas_gateway_integration_extra_type_0 import VegasGatewayIntegrationExtraType0

        d = dict(src_dict)

        def _parse_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        id = _parse_id(d.pop("id", UNSET))

        name = cast(Literal["vegas_gateway"] | Unset, d.pop("name", UNSET))
        if name != "vegas_gateway" and not isinstance(name, Unset):
            raise ValueError(f"name must match const 'vegas_gateway', got '{name}'")

        def _parse_extra(data: object) -> None | Unset | VegasGatewayIntegrationExtraType0:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                extra_type_0 = VegasGatewayIntegrationExtraType0.from_dict(data)

                return extra_type_0
            except:  # noqa: E722
                pass
            return cast(None | Unset | VegasGatewayIntegrationExtraType0, data)

        extra = _parse_extra(d.pop("extra", UNSET))

        vegas_gateway_integration = cls(id=id, name=name, extra=extra)

        vegas_gateway_integration.additional_properties = d
        return vegas_gateway_integration

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
