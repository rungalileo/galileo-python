from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.model_price_entry import ModelPriceEntry


T = TypeVar("T", bound="ModelPricesResponse")


@_attrs_define
class ModelPricesResponse:
    """Response for GET /models/{model_name}/prices.

    Attributes:
        override (ModelPriceEntry | None | Unset):
        default (ModelPriceEntry | None | Unset):
    """

    override: ModelPriceEntry | None | Unset = UNSET
    default: ModelPriceEntry | None | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.model_price_entry import ModelPriceEntry

        override: dict[str, Any] | None | Unset
        if isinstance(self.override, Unset):
            override = UNSET
        elif isinstance(self.override, ModelPriceEntry):
            override = self.override.to_dict()
        else:
            override = self.override

        default: dict[str, Any] | None | Unset
        if isinstance(self.default, Unset):
            default = UNSET
        elif isinstance(self.default, ModelPriceEntry):
            default = self.default.to_dict()
        else:
            default = self.default

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if override is not UNSET:
            field_dict["override"] = override
        if default is not UNSET:
            field_dict["default"] = default

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.model_price_entry import ModelPriceEntry

        d = dict(src_dict)

        def _parse_override(data: object) -> ModelPriceEntry | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                override_type_0 = ModelPriceEntry.from_dict(data)

                return override_type_0
            except:  # noqa: E722
                pass
            return cast(ModelPriceEntry | None | Unset, data)

        override = _parse_override(d.pop("override", UNSET))

        def _parse_default(data: object) -> ModelPriceEntry | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                default_type_0 = ModelPriceEntry.from_dict(data)

                return default_type_0
            except:  # noqa: E722
                pass
            return cast(ModelPriceEntry | None | Unset, data)

        default = _parse_default(d.pop("default", UNSET))

        model_prices_response = cls(override=override, default=default)

        model_prices_response.additional_properties = d
        return model_prices_response

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
