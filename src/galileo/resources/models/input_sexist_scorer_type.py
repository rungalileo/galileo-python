from typing import Literal, cast

InputSexistScorerType = Literal["luna", "plus"]

INPUT_SEXIST_SCORER_TYPE_VALUES: set[InputSexistScorerType] = {"luna", "plus"}


def check_input_sexist_scorer_type(value: str) -> InputSexistScorerType:
    if value in INPUT_SEXIST_SCORER_TYPE_VALUES:
        return cast(InputSexistScorerType, value)
    raise TypeError(f"Unexpected value {value!r}. Expected one of {INPUT_SEXIST_SCORER_TYPE_VALUES!r}")
