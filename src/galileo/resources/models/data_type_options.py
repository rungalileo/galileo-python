from enum import Enum


class DataTypeOptions(str, Enum):
    ARRAY = "array"
    BOOLEAN = "boolean"
    DOLLARS = "dollars"
    FLOATING_POINT = "floating_point"
    HALLUCINATION_SEGMENTS = "hallucination_segments"
    INTEGER = "integer"
    LABEL = "label"
    MILLI_SECONDS = "milli_seconds"
    PERCENTAGE = "percentage"
    SCORE_RATING = "score_rating"
    SCORE_RATING_AGGREGATE = "score_rating_aggregate"
    SEGMENTS = "segments"
    STAR_RATING = "star_rating"
    STAR_RATING_AGGREGATE = "star_rating_aggregate"
    TAGS_RATING = "tags_rating"
    TAGS_RATING_AGGREGATE = "tags_rating_aggregate"
    TEMPLATE_LABEL = "template_label"
    TEXT = "text"
    TEXT_OFFSETS = "text_offsets"
    THUMB_RATING = "thumb_rating"
    THUMB_RATING_AGGREGATE = "thumb_rating_aggregate"
    THUMB_RATING_PERCENTAGE = "thumb_rating_percentage"
    TIMESTAMP = "timestamp"
    UNKNOWN = "unknown"
    USER_ID = "user_id"
    UUID = "uuid"

    def __str__(self) -> str:
        return str(self.value)
