from typing import Literal, cast

ModelType = Literal["code", "llm", "slm"]

MODEL_TYPE_VALUES: set[ModelType] = {"code", "llm", "slm"}


def check_model_type(value: str) -> ModelType:
    if value in MODEL_TYPE_VALUES:
        return cast(ModelType, value)
    raise TypeError(f"Unexpected value {value!r}. Expected one of {MODEL_TYPE_VALUES!r}")
