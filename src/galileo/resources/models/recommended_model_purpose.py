from enum import Enum


class RecommendedModelPurpose(str, Enum):
    AI_ASSISTANT = "ai_assistant"
    AUTOTUNE = "autotune"
    CUSTOM_METRIC_AUTOGEN = "custom_metric_autogen"
    CUSTOM_METRIC_JUDGE = "custom_metric_judge"
    SIGNALS = "signals"

    def __str__(self) -> str:
        return str(self.value)
