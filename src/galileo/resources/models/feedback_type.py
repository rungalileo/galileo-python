from enum import Enum


class FeedbackType(str, Enum):
    CHOICE = "choice"
    LIKE_DISLIKE = "like_dislike"
    SCORE = "score"
    STAR = "star"
    TAGS = "tags"
    TEXT = "text"
    TREE_CHOICE = "tree_choice"

    def __str__(self) -> str:
        return str(self.value)
