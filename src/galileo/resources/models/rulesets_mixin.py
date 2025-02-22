from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.ruleset import Ruleset


T = TypeVar("T", bound="RulesetsMixin")


@_attrs_define
class RulesetsMixin:
    """
    Attributes:
        prioritized_rulesets (Union[Unset, list['Ruleset']]): Rulesets to be applied to the payload.
    """

    prioritized_rulesets: Union[Unset, list["Ruleset"]] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        prioritized_rulesets: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.prioritized_rulesets, Unset):
            prioritized_rulesets = []
            for prioritized_rulesets_item_data in self.prioritized_rulesets:
                prioritized_rulesets_item = prioritized_rulesets_item_data.to_dict()
                prioritized_rulesets.append(prioritized_rulesets_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if prioritized_rulesets is not UNSET:
            field_dict["prioritized_rulesets"] = prioritized_rulesets

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.ruleset import Ruleset

        d = src_dict.copy()
        prioritized_rulesets = []
        _prioritized_rulesets = d.pop("prioritized_rulesets", UNSET)
        for prioritized_rulesets_item_data in _prioritized_rulesets or []:
            prioritized_rulesets_item = Ruleset.from_dict(prioritized_rulesets_item_data)

            prioritized_rulesets.append(prioritized_rulesets_item)

        rulesets_mixin = cls(prioritized_rulesets=prioritized_rulesets)

        rulesets_mixin.additional_properties = d
        return rulesets_mixin

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
