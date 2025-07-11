from enum import Enum


class SyntheticDataTypes(str, Enum):
    GENERAL_QUERY = "General Query"
    MULTIPLE_QUESTIONS_IN_QUERY = "Multiple Questions in Query"
    OFF_TOPIC_QUERY = "Off-Topic Query"
    PROMPT_INJECTION = "Prompt Injection"
    SEXIST_CONTENT_IN_QUERY = "Sexist Content in Query"
    TOXIC_CONTENT_IN_QUERY = "Toxic Content in Query"

    def __str__(self) -> str:
        return str(self.value)
