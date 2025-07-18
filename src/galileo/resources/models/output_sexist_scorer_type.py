from typing import Literal, cast

OutputSexistScorerType = Literal["luna", "plus"]

OUTPUT_SEXIST_SCORER_TYPE_VALUES: set[OutputSexistScorerType] = {"luna", "plus"}


def check_output_sexist_scorer_type(value: str) -> OutputSexistScorerType:
    if value in OUTPUT_SEXIST_SCORER_TYPE_VALUES:
        return cast(OutputSexistScorerType, value)
    raise TypeError(f"Unexpected value {value!r}. Expected one of {OUTPUT_SEXIST_SCORER_TYPE_VALUES!r}")
