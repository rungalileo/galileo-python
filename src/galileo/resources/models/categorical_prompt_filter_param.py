from typing import Any, Literal, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="CategoricalPromptFilterParam")


@_attrs_define
class CategoricalPromptFilterParam:
    """
    Attributes:
        categories (list[str]):
        column (str):
        filter_type (Literal['category']):
        operator (Union[Unset, Any]): Operator to use when checking if the value is in the categories. If None, we
            default to 'or'. Default: 'any'.
    """

    categories: list[str]
    column: str
    filter_type: Literal["category"]
    operator: Union[Unset, Any] = "any"
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        categories = self.categories

        column = self.column

        filter_type = self.filter_type

        operator = self.operator

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({"categories": categories, "column": column, "filter_type": filter_type})
        if operator is not UNSET:
            field_dict["operator"] = operator

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        categories = cast(list[str], d.pop("categories"))

        column = d.pop("column")

        filter_type = cast(Literal["category"], d.pop("filter_type"))
        if filter_type != "category":
            raise ValueError(f"filter_type must match const 'category', got '{filter_type}'")

        operator = d.pop("operator", UNSET)

        categorical_prompt_filter_param = cls(
            categories=categories, column=column, filter_type=filter_type, operator=operator
        )

        categorical_prompt_filter_param.additional_properties = d
        return categorical_prompt_filter_param

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
