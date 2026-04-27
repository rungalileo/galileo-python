from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.override_action import OverrideAction
    from ..models.passthrough_action import PassthroughAction
    from ..models.rule import Rule
    from ..models.rule_result import RuleResult


T = TypeVar("T", bound="RulesetResult")


@_attrs_define
class RulesetResult:
    """
    Attributes:
        status (str | Unset): Status of the execution.
        rules (list[Rule] | Unset): List of rules to evaluate. Atleast 1 rule is required.
        action (OverrideAction | PassthroughAction | Unset): Action to take if all the rules are met.
        description (None | str | Unset): Description of the ruleset.
        rule_results (list[RuleResult] | Unset): Results of the rule execution.
    """

    status: str | Unset = UNSET
    rules: list[Rule] | Unset = UNSET
    action: OverrideAction | PassthroughAction | Unset = UNSET
    description: None | str | Unset = UNSET
    rule_results: list[RuleResult] | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.override_action import OverrideAction

        status = self.status

        rules: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.rules, Unset):
            rules = []
            for rules_item_data in self.rules:
                rules_item = rules_item_data.to_dict()
                rules.append(rules_item)

        action: dict[str, Any] | Unset
        if isinstance(self.action, Unset):
            action = UNSET
        elif isinstance(self.action, OverrideAction):
            action = self.action.to_dict()
        else:
            action = self.action.to_dict()

        description: None | str | Unset
        if isinstance(self.description, Unset):
            description = UNSET
        else:
            description = self.description

        rule_results: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.rule_results, Unset):
            rule_results = []
            for rule_results_item_data in self.rule_results:
                rule_results_item = rule_results_item_data.to_dict()
                rule_results.append(rule_results_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if status is not UNSET:
            field_dict["status"] = status
        if rules is not UNSET:
            field_dict["rules"] = rules
        if action is not UNSET:
            field_dict["action"] = action
        if description is not UNSET:
            field_dict["description"] = description
        if rule_results is not UNSET:
            field_dict["rule_results"] = rule_results

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.override_action import OverrideAction
        from ..models.passthrough_action import PassthroughAction
        from ..models.rule import Rule
        from ..models.rule_result import RuleResult

        d = dict(src_dict)
        status = d.pop("status", UNSET)

        _rules = d.pop("rules", UNSET)
        rules: list[Rule] | Unset = UNSET
        if _rules is not UNSET:
            rules = []
            for rules_item_data in _rules:
                rules_item = Rule.from_dict(rules_item_data)

                rules.append(rules_item)

        def _parse_action(data: object) -> OverrideAction | PassthroughAction | Unset:
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

        def _parse_description(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        description = _parse_description(d.pop("description", UNSET))

        _rule_results = d.pop("rule_results", UNSET)
        rule_results: list[RuleResult] | Unset = UNSET
        if _rule_results is not UNSET:
            rule_results = []
            for rule_results_item_data in _rule_results:
                rule_results_item = RuleResult.from_dict(rule_results_item_data)

                rule_results.append(rule_results_item)

        ruleset_result = cls(
            status=status, rules=rules, action=action, description=description, rule_results=rule_results
        )

        ruleset_result.additional_properties = d
        return ruleset_result

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
