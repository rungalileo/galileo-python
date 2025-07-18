from typing import Literal, cast

ModelCostBy = Literal["characters", "tokens"]

MODEL_COST_BY_VALUES: set[ModelCostBy] = {"characters", "tokens"}


def check_model_cost_by(value: str) -> ModelCostBy:
    if value in MODEL_COST_BY_VALUES:
        return cast(ModelCostBy, value)
    raise TypeError(f"Unexpected value {value!r}. Expected one of {MODEL_COST_BY_VALUES!r}")
