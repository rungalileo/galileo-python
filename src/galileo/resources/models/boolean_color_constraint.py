from collections.abc import Mapping
from typing import Any, Literal, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.metric_color import MetricColor

T = TypeVar("T", bound="BooleanColorConstraint")


@_attrs_define
class BooleanColorConstraint:
    """A color constraint for boolean metric values.

    Assigns a color when a boolean score equals the given value.

    Only the 'eq' operator is supported.

    Example:
        {"color": "green", "operator": "eq", "value": true}
        {"color": "red", "operator": "eq", "value": false}

    Attributes
    ----------
            color (MetricColor): Allowed colors for metric threshold visualization in the UI.
            operator (Literal['eq']):
            value (bool):
    """

    color: MetricColor
    operator: Literal["eq"]
    value: bool
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        color = self.color.value

        operator = self.operator

        value = self.value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({"color": color, "operator": operator, "value": value})

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        color = MetricColor(d.pop("color"))

        operator = cast(Literal["eq"], d.pop("operator"))
        if operator != "eq":
            raise ValueError(f"operator must match const 'eq', got '{operator}'")

        value = d.pop("value")

        boolean_color_constraint = cls(color=color, operator=operator, value=value)

        boolean_color_constraint.additional_properties = d
        return boolean_color_constraint

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
