from enum import Enum


class GroupLabel(str, Enum):
    AGENT_QUALITY = "Agent Quality"
    CONFIGURATION = "Configuration"
    CUSTOM_METRICS = "Custom Metrics"
    DATASET = "Dataset"
    GENERIC_PARAMETERS = "Generic Parameters"
    INPUT_QUALITY = "Input Quality"
    LLM_PARAMETERS = "LLM Parameters"
    OUTPUT_QUALITY = "Output Quality"
    PROTECT = "Protect"
    RAG_PARAMETERS = "RAG Parameters"
    RAG_QUALITY = "RAG Quality"
    RATING_SUMMARY = "Rating Summary"
    SAFETY_METRICS = "Safety Metrics"
    SECURITY = "Security"
    SYSTEM_METRICS = "System Metrics"

    def __str__(self) -> str:
        return str(self.value)
