from typing import Literal, cast

DataTypeOptions = Literal[
    "array",
    "boolean",
    "dollars",
    "floating_point",
    "hallucination_segments",
    "integer",
    "label",
    "milli_seconds",
    "percentage",
    "score_rating",
    "score_rating_aggregate",
    "segments",
    "star_rating",
    "star_rating_aggregate",
    "tags_rating",
    "tags_rating_aggregate",
    "template_label",
    "text",
    "text_offsets",
    "thumb_rating",
    "thumb_rating_aggregate",
    "thumb_rating_percentage",
    "timestamp",
    "unknown",
    "user_id",
    "uuid",
]

DATA_TYPE_OPTIONS_VALUES: set[DataTypeOptions] = {
    "array",
    "boolean",
    "dollars",
    "floating_point",
    "hallucination_segments",
    "integer",
    "label",
    "milli_seconds",
    "percentage",
    "score_rating",
    "score_rating_aggregate",
    "segments",
    "star_rating",
    "star_rating_aggregate",
    "tags_rating",
    "tags_rating_aggregate",
    "template_label",
    "text",
    "text_offsets",
    "thumb_rating",
    "thumb_rating_aggregate",
    "thumb_rating_percentage",
    "timestamp",
    "unknown",
    "user_id",
    "uuid",
}


def check_data_type_options(value: str) -> DataTypeOptions:
    if value in DATA_TYPE_OPTIONS_VALUES:
        return cast(DataTypeOptions, value)
    raise TypeError(f"Unexpected value {value!r}. Expected one of {DATA_TYPE_OPTIONS_VALUES!r}")
