from collections.abc import Mapping
from typing import Any, Literal, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.scorer_is_global_filter_operator import ScorerIsGlobalFilterOperator
from ..types import UNSET, Unset

T = TypeVar("T", bound="ScorerIsGlobalFilter")


@_attrs_define
class ScorerIsGlobalFilter:
    """Filters on the access scope tier: is_global=True (global metrics) vs
    is_global=False (project-scoped metrics).

    Attributes
    ----------
            value (bool):
            name (Union[Literal['is_global'], Unset]):  Default: 'is_global'.
            operator (Union[Unset, ScorerIsGlobalFilterOperator]):  Default: ScorerIsGlobalFilterOperator.EQ.
    """

    value: bool
    name: Literal["is_global"] | Unset = "is_global"
    operator: Unset | ScorerIsGlobalFilterOperator = ScorerIsGlobalFilterOperator.EQ
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        value = self.value

        name = self.name

        operator: Unset | str = UNSET
        if not isinstance(self.operator, Unset):
            operator = self.operator.value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({"value": value})
        if name is not UNSET:
            field_dict["name"] = name
        if operator is not UNSET:
            field_dict["operator"] = operator

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        value = d.pop("value")

        name = cast(Literal["is_global"] | Unset, d.pop("name", UNSET))
        if name != "is_global" and not isinstance(name, Unset):
            raise ValueError(f"name must match const 'is_global', got '{name}'")

        _operator = d.pop("operator", UNSET)
        operator: Unset | ScorerIsGlobalFilterOperator
        operator = UNSET if isinstance(_operator, Unset) else ScorerIsGlobalFilterOperator(_operator)

        scorer_is_global_filter = cls(value=value, name=name, operator=operator)

        scorer_is_global_filter.additional_properties = d
        return scorer_is_global_filter

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
