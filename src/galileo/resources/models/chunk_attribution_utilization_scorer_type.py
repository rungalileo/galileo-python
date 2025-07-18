from typing import Literal, cast

ChunkAttributionUtilizationScorerType = Literal["luna", "plus"]

CHUNK_ATTRIBUTION_UTILIZATION_SCORER_TYPE_VALUES: set[ChunkAttributionUtilizationScorerType] = {"luna", "plus"}


def check_chunk_attribution_utilization_scorer_type(value: str) -> ChunkAttributionUtilizationScorerType:
    if value in CHUNK_ATTRIBUTION_UTILIZATION_SCORER_TYPE_VALUES:
        return cast(ChunkAttributionUtilizationScorerType, value)
    raise TypeError(f"Unexpected value {value!r}. Expected one of {CHUNK_ATTRIBUTION_UTILIZATION_SCORER_TYPE_VALUES!r}")
