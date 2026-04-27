from enum import Enum


class GeneratedScorerTaskResultType(str, Enum):
    SCORER_AUTO_GEN = "scorer_auto_gen"
    SCORER_AUTO_GEN_V2 = "scorer_auto_gen_v2"
    SCORER_VALIDATION = "scorer_validation"

    def __str__(self) -> str:
        return str(self.value)
