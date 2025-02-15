from enum import Enum


class CollaboratorRole(str, Enum):
    ANNOTATOR = "annotator"
    EDITOR = "editor"
    OWNER = "owner"
    VIEWER = "viewer"

    def __str__(self) -> str:
        return str(self.value)
