from enum import Enum


class GeneratedScorerTaskResultType(str, Enum):
    SCORER_AUTO_GEN = "scorer_auto_gen"
    SCORER_VALIDATION = "scorer_validation"

    def __str__(self) -> str:
        return str(self.value)
