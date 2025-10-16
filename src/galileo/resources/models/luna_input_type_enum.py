from enum import Enum


class LunaInputTypeEnum(str, Enum):
    SPAN = "span"
    TRACE_INPUT_OUTPUT_ONLY = "trace_input_output_only"
    TRACE_OBJECT = "trace_object"

    def __str__(self) -> str:
        return str(self.value)
