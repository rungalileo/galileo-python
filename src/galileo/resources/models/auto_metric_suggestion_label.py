from enum import Enum


class AutoMetricSuggestionLabel(str, Enum):
    AGENT = "Agent"
    CODE_GENERATION = "Code Generation"
    MULTI_TURN_DIALOGUE_SYSTEM = "Multi-turn dialogue system"
    RETRIEVER_AUGMENTED_GENERATION_RAG = "Retriever Augmented Generation (RAG)"

    def __str__(self) -> str:
        return str(self.value)
