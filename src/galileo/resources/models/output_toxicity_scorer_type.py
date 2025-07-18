from typing import Literal, cast

OutputToxicityScorerType = Literal["luna", "plus"]

OUTPUT_TOXICITY_SCORER_TYPE_VALUES: set[OutputToxicityScorerType] = {"luna", "plus"}


def check_output_toxicity_scorer_type(value: str) -> OutputToxicityScorerType:
    if value in OUTPUT_TOXICITY_SCORER_TYPE_VALUES:
        return cast(OutputToxicityScorerType, value)
    raise TypeError(f"Unexpected value {value!r}. Expected one of {OUTPUT_TOXICITY_SCORER_TYPE_VALUES!r}")
