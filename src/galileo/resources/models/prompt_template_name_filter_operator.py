from typing import Literal, cast

PromptTemplateNameFilterOperator = Literal["contains", "eq", "ne", "not_in", "one_of"]

PROMPT_TEMPLATE_NAME_FILTER_OPERATOR_VALUES: set[PromptTemplateNameFilterOperator] = {
    "contains",
    "eq",
    "ne",
    "not_in",
    "one_of",
}


def check_prompt_template_name_filter_operator(value: str) -> PromptTemplateNameFilterOperator:
    if value in PROMPT_TEMPLATE_NAME_FILTER_OPERATOR_VALUES:
        return cast(PromptTemplateNameFilterOperator, value)
    raise TypeError(f"Unexpected value {value!r}. Expected one of {PROMPT_TEMPLATE_NAME_FILTER_OPERATOR_VALUES!r}")
