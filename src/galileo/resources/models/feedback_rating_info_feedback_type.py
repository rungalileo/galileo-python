from typing import Literal, cast

FeedbackRatingInfoFeedbackType = Literal["like_dislike", "score", "star", "tags", "text"]

FEEDBACK_RATING_INFO_FEEDBACK_TYPE_VALUES: set[FeedbackRatingInfoFeedbackType] = {
    "like_dislike",
    "score",
    "star",
    "tags",
    "text",
}


def check_feedback_rating_info_feedback_type(value: str) -> FeedbackRatingInfoFeedbackType:
    if value in FEEDBACK_RATING_INFO_FEEDBACK_TYPE_VALUES:
        return cast(FeedbackRatingInfoFeedbackType, value)
    raise TypeError(f"Unexpected value {value!r}. Expected one of {FEEDBACK_RATING_INFO_FEEDBACK_TYPE_VALUES!r}")
