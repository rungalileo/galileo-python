from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.metric_color import MetricColor
from ..models.numeric_color_constraint_operator import NumericColorConstraintOperator

T = TypeVar("T", bound="NumericColorConstraint")


@_attrs_define
class NumericColorConstraint:
    """A color constraint for numeric metric values.

    Assigns a color when a numeric score matches the given operator and value.

    Operators and expected value shapes:
      - eq, gt, gte, lt, lte: value must be a single float.
      - between: value must be a list of exactly 2 floats [low, high] where low < high.
        The range is inclusive on both ends.

    Example:
        {"color": "green", "operator": "gte", "value": 0.8}
        {"color": "yellow", "operator": "between", "value": [0.3, 0.7]}

        Attributes:
            color (MetricColor): Allowed colors for metric threshold visualization in the UI.
            operator (NumericColorConstraintOperator):
            value (float | list[float]):
    """

    color: MetricColor
    operator: NumericColorConstraintOperator
    value: float | list[float]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        color = self.color.value

        operator = self.operator.value

        value: float | list[float]
        if isinstance(self.value, list):
            value = self.value

        else:
            value = self.value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({"color": color, "operator": operator, "value": value})

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        color = MetricColor(d.pop("color"))

        operator = NumericColorConstraintOperator(d.pop("operator"))

        def _parse_value(data: object) -> float | list[float]:
            try:
                if not isinstance(data, list):
                    raise TypeError()
                value_type_1 = cast(list[float], data)

                return value_type_1
            except:  # noqa: E722
                pass
            return cast(float | list[float], data)

        value = _parse_value(d.pop("value"))

        numeric_color_constraint = cls(color=color, operator=operator, value=value)

        numeric_color_constraint.additional_properties = d
        return numeric_color_constraint

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
