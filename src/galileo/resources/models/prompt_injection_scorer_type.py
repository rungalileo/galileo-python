from typing import Literal, cast

PromptInjectionScorerType = Literal["luna", "plus"]

PROMPT_INJECTION_SCORER_TYPE_VALUES: set[PromptInjectionScorerType] = {"luna", "plus"}


def check_prompt_injection_scorer_type(value: str) -> PromptInjectionScorerType:
    if value in PROMPT_INJECTION_SCORER_TYPE_VALUES:
        return cast(PromptInjectionScorerType, value)
    raise TypeError(f"Unexpected value {value!r}. Expected one of {PROMPT_INJECTION_SCORER_TYPE_VALUES!r}")
