from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.model_prices_response import ModelPricesResponse


T = TypeVar("T", bound="ModelWithPrices")


@_attrs_define
class ModelWithPrices:
    """Single item in GET /models response.

    Attributes:
        name (str):
        prices (ModelPricesResponse | None | Unset):
    """

    name: str
    prices: ModelPricesResponse | None | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.model_prices_response import ModelPricesResponse

        name = self.name

        prices: dict[str, Any] | None | Unset
        if isinstance(self.prices, Unset):
            prices = UNSET
        elif isinstance(self.prices, ModelPricesResponse):
            prices = self.prices.to_dict()
        else:
            prices = self.prices

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({"name": name})
        if prices is not UNSET:
            field_dict["prices"] = prices

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.model_prices_response import ModelPricesResponse

        d = dict(src_dict)
        name = d.pop("name")

        def _parse_prices(data: object) -> ModelPricesResponse | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                prices_type_0 = ModelPricesResponse.from_dict(data)

                return prices_type_0
            except:  # noqa: E722
                pass
            return cast(ModelPricesResponse | None | Unset, data)

        prices = _parse_prices(d.pop("prices", UNSET))

        model_with_prices = cls(name=name, prices=prices)

        model_with_prices.additional_properties = d
        return model_with_prices

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
