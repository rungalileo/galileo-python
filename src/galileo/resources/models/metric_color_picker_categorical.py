from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, Literal, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.categorical_color_constraint import CategoricalColorConstraint


T = TypeVar("T", bound="MetricColorPickerCategorical")


@_attrs_define
class MetricColorPickerCategorical:
    """Color picker configuration for categorical metrics.

    Each constraint maps one or more category values to a color. A category
    value must not appear in more than one constraint.

    Example:
        {
            "type": "categorical",
            "constraints": [
                {"color": "green", "operator": "eq", "value": "pass"},
                {"color": "red", "operator": "one_of", "value": ["fail", "error"]}
            ]
        }

    Attributes
    ----------
            constraints (list['CategoricalColorConstraint']):
            type_ (Union[Literal['categorical'], Unset]):  Default: 'categorical'.
    """

    constraints: list["CategoricalColorConstraint"]
    type_: Literal["categorical"] | Unset = "categorical"
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
        from ..models.categorical_color_constraint import CategoricalColorConstraint

        d = dict(src_dict)
        constraints = []
        _constraints = d.pop("constraints")
        for constraints_item_data in _constraints:
            constraints_item = CategoricalColorConstraint.from_dict(constraints_item_data)

            constraints.append(constraints_item)

        type_ = cast(Literal["categorical"] | Unset, d.pop("type", UNSET))
        if type_ != "categorical" and not isinstance(type_, Unset):
            raise ValueError(f"type must match const 'categorical', got '{type_}'")

        metric_color_picker_categorical = cls(constraints=constraints, type_=type_)

        metric_color_picker_categorical.additional_properties = d
        return metric_color_picker_categorical

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
