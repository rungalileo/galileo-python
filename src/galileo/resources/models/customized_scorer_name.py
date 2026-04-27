from enum import Enum


class CustomizedScorerName(str, Enum):
    VALUE_0 = "_customized_agentic_workflow_success"
    VALUE_1 = "_customized_agentic_session_success"
    VALUE_10 = "_customized_tool_selection_quality"
    VALUE_11 = "_customized_sexist_gpt"
    VALUE_12 = "_customized_input_sexist_gpt"
    VALUE_13 = "_customized_toxicity_gpt"
    VALUE_14 = "_customized_input_toxicity_gpt"
    VALUE_2 = "_customized_chunk_attribution_utilization_gpt"
    VALUE_3 = "_customized_completeness_gpt"
    VALUE_4 = "_customized_groundedness"
    VALUE_5 = "_customized_factuality"
    VALUE_6 = "_customized_ground_truth_adherence"
    VALUE_7 = "_customized_instruction_adherence"
    VALUE_8 = "_customized_prompt_injection_gpt"
    VALUE_9 = "_customized_tool_error_rate"

    def __str__(self) -> str:
        return str(self.value)
