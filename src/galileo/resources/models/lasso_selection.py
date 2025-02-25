from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="LassoSelection")


@_attrs_define
class LassoSelection:
    """Representation of a lasso selection (used by embeddings)

    x and y correspond to the cursor movement while tracing the lasso. This is natively provided by plotly when creating
    a lasso selection, for example

        Attributes:
            x (list[float]):
            y (list[float]):
    """

    x: list[float]
    y: list[float]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        x = self.x

        y = self.y

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({"x": x, "y": y})

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        x = cast(list[float], d.pop("x"))

        y = cast(list[float], d.pop("y"))

        lasso_selection = cls(x=x, y=y)

        lasso_selection.additional_properties = d
        return lasso_selection

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
