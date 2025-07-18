from typing import Literal, cast

InputToxicityScorerType = Literal["luna", "plus"]

INPUT_TOXICITY_SCORER_TYPE_VALUES: set[InputToxicityScorerType] = {"luna", "plus"}


def check_input_toxicity_scorer_type(value: str) -> InputToxicityScorerType:
    if value in INPUT_TOXICITY_SCORER_TYPE_VALUES:
        return cast(InputToxicityScorerType, value)
    raise TypeError(f"Unexpected value {value!r}. Expected one of {INPUT_TOXICITY_SCORER_TYPE_VALUES!r}")
