from enum import Enum


class DataType(str, Enum):
    BOOLEAN = "boolean"
    CATEGORY_COUNTS = "category_counts"
    DATASET = "dataset"
    FLOATING_POINT = "floating_point"
    INTEGER = "integer"
    PLAYGROUND = "playground"
    PROMPT = "prompt"
    RANK = "rank"
    SCORE_RATING_AGGREGATE = "score_rating_aggregate"
    STAR_RATING_AGGREGATE = "star_rating_aggregate"
    STRING_LIST = "string_list"
    TAG = "tag"
    TAGS_RATING_AGGREGATE = "tags_rating_aggregate"
    TEXT = "text"
    TEXT_RATING_AGGREGATE = "text_rating_aggregate"
    THUMB_RATING_AGGREGATE = "thumb_rating_aggregate"
    TIMESTAMP = "timestamp"
    UUID = "uuid"

    def __str__(self) -> str:
        return str(self.value)
