from typing import Literal, cast

LLMExportFormat = Literal["csv", "jsonl"]

LLM_EXPORT_FORMAT_VALUES: set[LLMExportFormat] = {"csv", "jsonl"}


def check_llm_export_format(value: str) -> LLMExportFormat:
    if value in LLM_EXPORT_FORMAT_VALUES:
        return cast(LLMExportFormat, value)
    raise TypeError(f"Unexpected value {value!r}. Expected one of {LLM_EXPORT_FORMAT_VALUES!r}")
