from enum import Enum


class CustomizedScorerName(str, Enum):
    VALUE_0 = "_customized_chunk_attribution_utilization_gpt"
    VALUE_1 = "_customized_completeness_gpt"
    VALUE_2 = "_customized_groundedness"
    VALUE_3 = "_customized_factuality"
    VALUE_4 = "_customized_instruction_adherence"
    VALUE_5 = "_customized_tool_error_rate"
    VALUE_6 = "_customized_tool_selection_quality"
    VALUE_7 = "_customized_agentic_workflow_success"

    def __str__(self) -> str:
        return str(self.value)
