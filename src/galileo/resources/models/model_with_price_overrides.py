from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.model_price_entry import ModelPriceEntry


T = TypeVar("T", bound="ModelWithPriceOverrides")


@_attrs_define
class ModelWithPriceOverrides:
    """Single item in GET /models/price_overrides response.

    Attributes:
        name (str):
        price_overrides (ModelPriceEntry): A pair of input/output prices — used for requests and responses.
    """

    name: str
    price_overrides: ModelPriceEntry
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        price_overrides = self.price_overrides.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({"name": name, "price_overrides": price_overrides})

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.model_price_entry import ModelPriceEntry

        d = dict(src_dict)
        name = d.pop("name")

        price_overrides = ModelPriceEntry.from_dict(d.pop("price_overrides"))

        model_with_price_overrides = cls(name=name, price_overrides=price_overrides)

        model_with_price_overrides.additional_properties = d
        return model_with_price_overrides

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
