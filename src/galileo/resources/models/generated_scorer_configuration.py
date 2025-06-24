from collections.abc import Mapping
from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="GeneratedScorerConfiguration")


@_attrs_define
class GeneratedScorerConfiguration:
    """
    Attributes:
        model_alias (Union[Unset, str]):  Default: 'GPT-4o mini'.
        num_judges (Union[Unset, int]):  Default: 3.
    """

    model_alias: Union[Unset, str] = "GPT-4o mini"
    num_judges: Union[Unset, int] = 3
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        model_alias = self.model_alias

        num_judges = self.num_judges

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if model_alias is not UNSET:
            field_dict["model_alias"] = model_alias
        if num_judges is not UNSET:
            field_dict["num_judges"] = num_judges

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        model_alias = d.pop("model_alias", UNSET)

        num_judges = d.pop("num_judges", UNSET)

        generated_scorer_configuration = cls(model_alias=model_alias, num_judges=num_judges)

        generated_scorer_configuration.additional_properties = d
        return generated_scorer_configuration

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
