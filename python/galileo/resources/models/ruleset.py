from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.override_action import OverrideAction
    from ..models.passthrough_action import PassthroughAction
    from ..models.rule import Rule


T = TypeVar("T", bound="Ruleset")


@_attrs_define
class Ruleset:
    """
    Attributes:
        action (Union['OverrideAction', 'PassthroughAction', Unset]): Action to take if all the rules are met.
        description (Union[None, Unset, str]): Description of the ruleset.
        rules (Union[Unset, list['Rule']]): List of rules to evaluate. Atleast 1 rule is required.
    """

    action: Union["OverrideAction", "PassthroughAction", Unset] = UNSET
    description: Union[None, Unset, str] = UNSET
    rules: Union[Unset, list["Rule"]] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.override_action import OverrideAction

        action: Union[Unset, dict[str, Any]]
        if isinstance(self.action, Unset):
            action = UNSET
        elif isinstance(self.action, OverrideAction):
            action = self.action.to_dict()
        else:
            action = self.action.to_dict()

        description: Union[None, Unset, str]
        if isinstance(self.description, Unset):
            description = UNSET
        else:
            description = self.description

        rules: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.rules, Unset):
            rules = []
            for rules_item_data in self.rules:
                rules_item = rules_item_data.to_dict()
                rules.append(rules_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if action is not UNSET:
            field_dict["action"] = action
        if description is not UNSET:
            field_dict["description"] = description
        if rules is not UNSET:
            field_dict["rules"] = rules

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.override_action import OverrideAction
        from ..models.passthrough_action import PassthroughAction
        from ..models.rule import Rule

        d = src_dict.copy()

        def _parse_action(data: object) -> Union["OverrideAction", "PassthroughAction", Unset]:
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                action_type_0 = OverrideAction.from_dict(data)

                return action_type_0
            except:  # noqa: E722
                pass
            if not isinstance(data, dict):
                raise TypeError()
            action_type_1 = PassthroughAction.from_dict(data)

            return action_type_1

        action = _parse_action(d.pop("action", UNSET))

        def _parse_description(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        description = _parse_description(d.pop("description", UNSET))

        rules = []
        _rules = d.pop("rules", UNSET)
        for rules_item_data in _rules or []:
            rules_item = Rule.from_dict(rules_item_data)

            rules.append(rules_item)

        ruleset = cls(action=action, description=description, rules=rules)

        ruleset.additional_properties = d
        return ruleset

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
