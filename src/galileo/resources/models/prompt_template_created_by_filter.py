from collections.abc import Mapping
from typing import Any, Literal, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.prompt_template_created_by_filter_operator import PromptTemplateCreatedByFilterOperator
from ..types import UNSET, Unset

T = TypeVar("T", bound="PromptTemplateCreatedByFilter")


@_attrs_define
class PromptTemplateCreatedByFilter:
    """
    Attributes:
        value (Union[list[str], str]):
        name (Union[Literal['creator'], Unset]):  Default: 'creator'.
        operator (Union[Unset, PromptTemplateCreatedByFilterOperator]):  Default:
            PromptTemplateCreatedByFilterOperator.EQ.
    """

    value: Union[list[str], str]
    name: Union[Literal["creator"], Unset] = "creator"
    operator: Union[Unset, PromptTemplateCreatedByFilterOperator] = PromptTemplateCreatedByFilterOperator.EQ
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        value: Union[list[str], str]
        if isinstance(self.value, list):
            value = self.value

        else:
            value = self.value

        name = self.name

        operator: Union[Unset, str] = UNSET
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

        def _parse_value(data: object) -> Union[list[str], str]:
            try:
                if not isinstance(data, list):
                    raise TypeError()
                value_type_1 = cast(list[str], data)

                return value_type_1
            except:  # noqa: E722
                pass
            return cast(Union[list[str], str], data)

        value = _parse_value(d.pop("value"))

        name = cast(Union[Literal["creator"], Unset], d.pop("name", UNSET))
        if name != "creator" and not isinstance(name, Unset):
            raise ValueError(f"name must match const 'creator', got '{name}'")

        _operator = d.pop("operator", UNSET)
        operator: Union[Unset, PromptTemplateCreatedByFilterOperator]
        if isinstance(_operator, Unset):
            operator = UNSET
        else:
            operator = PromptTemplateCreatedByFilterOperator(_operator)

        prompt_template_created_by_filter = cls(value=value, name=name, operator=operator)

        prompt_template_created_by_filter.additional_properties = d
        return prompt_template_created_by_filter

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
