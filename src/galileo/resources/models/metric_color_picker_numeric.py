from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, Literal, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.numeric_color_constraint import NumericColorConstraint


T = TypeVar("T", bound="MetricColorPickerNumeric")


@_attrs_define
class MetricColorPickerNumeric:
    """Color picker configuration for numeric metrics.

    Each constraint maps a numeric condition to a color. The UI uses these
    constraints to color-code metric values (e.g. green for high scores,
    red for low scores).

    Example:
        {
            "type": "numeric",
            "constraints": [
                {"color": "green", "operator": "gte", "value": 0.8},
                {"color": "yellow", "operator": "between", "value": [0.3, 0.8]},
                {"color": "red", "operator": "lt", "value": 0.3}
            ]
        }

        Attributes:
            constraints (list[NumericColorConstraint]):
            type_ (Literal['numeric'] | Unset):  Default: 'numeric'.
    """

    constraints: list[NumericColorConstraint]
    type_: Literal["numeric"] | Unset = "numeric"
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        constraints = []
        for constraints_item_data in self.constraints:
            constraints_item = constraints_item_data.to_dict()
            constraints.append(constraints_item)

        type_ = self.type_

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({"constraints": constraints})
        if type_ is not UNSET:
            field_dict["type"] = type_

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.numeric_color_constraint import NumericColorConstraint

        d = dict(src_dict)
        constraints = []
        _constraints = d.pop("constraints")
        for constraints_item_data in _constraints:
            constraints_item = NumericColorConstraint.from_dict(constraints_item_data)

            constraints.append(constraints_item)

        type_ = cast(Literal["numeric"] | Unset, d.pop("type", UNSET))
        if type_ != "numeric" and not isinstance(type_, Unset):
            raise ValueError(f"type must match const 'numeric', got '{type_}'")

        metric_color_picker_numeric = cls(constraints=constraints, type_=type_)

        metric_color_picker_numeric.additional_properties = d
        return metric_color_picker_numeric

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
