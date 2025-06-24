from enum import Enum


class FeedbackRatingInfoFeedbackType(str, Enum):
    LIKE_DISLIKE = "like_dislike"
    SCORE = "score"
    STAR = "star"
    TAGS = "tags"
    TEXT = "text"

    def __str__(self) -> str:
        return str(self.value)
