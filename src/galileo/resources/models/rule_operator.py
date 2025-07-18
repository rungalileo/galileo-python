from typing import Literal, cast

RuleOperator = Literal["all", "any", "contains", "empty", "eq", "gt", "gte", "lt", "lte", "neq", "not_empty"]

RULE_OPERATOR_VALUES: set[RuleOperator] = {
    "all",
    "any",
    "contains",
    "empty",
    "eq",
    "gt",
    "gte",
    "lt",
    "lte",
    "neq",
    "not_empty",
}


def check_rule_operator(value: str) -> RuleOperator:
    if value in RULE_OPERATOR_VALUES:
        return cast(RuleOperator, value)
    raise TypeError(f"Unexpected value {value!r}. Expected one of {RULE_OPERATOR_VALUES!r}")
