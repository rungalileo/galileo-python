from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.categorical_color_constraint_operator import CategoricalColorConstraintOperator
from ..models.metric_color import MetricColor

T = TypeVar("T", bound="CategoricalColorConstraint")


@_attrs_define
class CategoricalColorConstraint:
    """A color constraint for categorical or multi-label metric values.

    Assigns a color when a categorical score matches the given operator and value.

    Operators and expected value shapes:
      - eq: value must be a single string.
      - one_of: value must be a list of strings.

    Example:
        {"color": "green", "operator": "eq", "value": "pass"}
        {"color": "red", "operator": "one_of", "value": ["fail", "error"]}

    Attributes
    ----------
            color (MetricColor): Allowed colors for metric threshold visualization in the UI.
            operator (CategoricalColorConstraintOperator):
            value (list[str] | str):
    """

    color: MetricColor
    operator: CategoricalColorConstraintOperator
    value: list[str] | str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        color = self.color.value

        operator = self.operator.value

        value: list[str] | str
        value = self.value if isinstance(self.value, list) else self.value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({"color": color, "operator": operator, "value": value})

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        color = MetricColor(d.pop("color"))

        operator = CategoricalColorConstraintOperator(d.pop("operator"))

        def _parse_value(data: object) -> list[str] | str:
            try:
                if not isinstance(data, list):
                    raise TypeError()
                return cast(list[str], data)

            except:  # noqa: E722
                pass
            return cast(list[str] | str, data)

        value = _parse_value(d.pop("value"))

        categorical_color_constraint = cls(color=color, operator=operator, value=value)

        categorical_color_constraint.additional_properties = d
        return categorical_color_constraint

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
