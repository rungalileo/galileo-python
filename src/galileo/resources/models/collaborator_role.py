from typing import Literal, cast

CollaboratorRole = Literal["annotator", "editor", "owner", "viewer"]

COLLABORATOR_ROLE_VALUES: set[CollaboratorRole] = {"annotator", "editor", "owner", "viewer"}


def check_collaborator_role(value: str) -> CollaboratorRole:
    if value in COLLABORATOR_ROLE_VALUES:
        return cast(CollaboratorRole, value)
    raise TypeError(f"Unexpected value {value!r}. Expected one of {COLLABORATOR_ROLE_VALUES!r}")
