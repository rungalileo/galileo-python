from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.execution_status import ExecutionStatus
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
        action (Union['OverrideAction', 'PassthroughAction', Unset]): Action to take if all the rules are met.
        description (Union[None, Unset, str]): Description of the ruleset.
        rule_results (Union[Unset, list['RuleResult']]): Results of the rule execution.
        rules (Union[Unset, list['Rule']]): List of rules to evaluate. Atleast 1 rule is required.
        status (Union[Unset, ExecutionStatus]): Status of the execution.
    """

    action: Union["OverrideAction", "PassthroughAction", Unset] = UNSET
    description: Union[None, Unset, str] = UNSET
    rule_results: Union[Unset, list["RuleResult"]] = UNSET
    rules: Union[Unset, list["Rule"]] = UNSET
    status: Union[Unset, ExecutionStatus] = UNSET
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

        rule_results: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.rule_results, Unset):
            rule_results = []
            for rule_results_item_data in self.rule_results:
                rule_results_item = rule_results_item_data.to_dict()
                rule_results.append(rule_results_item)

        rules: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.rules, Unset):
            rules = []
            for rules_item_data in self.rules:
                rules_item = rules_item_data.to_dict()
                rules.append(rules_item)

        status: Union[Unset, str] = UNSET
        if not isinstance(self.status, Unset):
            status = self.status.value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if action is not UNSET:
            field_dict["action"] = action
        if description is not UNSET:
            field_dict["description"] = description
        if rule_results is not UNSET:
            field_dict["rule_results"] = rule_results
        if rules is not UNSET:
            field_dict["rules"] = rules
        if status is not UNSET:
            field_dict["status"] = status

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.override_action import OverrideAction
        from ..models.passthrough_action import PassthroughAction
        from ..models.rule import Rule
        from ..models.rule_result import RuleResult

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

        rule_results = []
        _rule_results = d.pop("rule_results", UNSET)
        for rule_results_item_data in _rule_results or []:
            rule_results_item = RuleResult.from_dict(rule_results_item_data)

            rule_results.append(rule_results_item)

        rules = []
        _rules = d.pop("rules", UNSET)
        for rules_item_data in _rules or []:
            rules_item = Rule.from_dict(rules_item_data)

            rules.append(rules_item)

        _status = d.pop("status", UNSET)
        status: Union[Unset, ExecutionStatus]
        if isinstance(_status, Unset):
            status = UNSET
        else:
            status = ExecutionStatus(_status)

        ruleset_result = cls(
            action=action, description=description, rule_results=rule_results, rules=rules, status=status
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
