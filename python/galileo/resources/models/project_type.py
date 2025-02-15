from enum import Enum


class ProjectType(str, Enum):
    GEN_AI = "gen_ai"
    LLM_MONITOR = "llm_monitor"
    PROMPT_EVALUATION = "prompt_evaluation"
    PROTECT = "protect"
    TRAINING_INFERENCE = "training_inference"

    def __str__(self) -> str:
        return str(self.value)
