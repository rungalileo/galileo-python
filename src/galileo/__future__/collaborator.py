"""Deprecated: use galileo.collaborator instead of galileo.__future__.collaborator."""

import warnings

warnings.warn(
    "Importing from galileo.__future__.collaborator is deprecated. Use galileo.collaborator instead.",
    DeprecationWarning,
    stacklevel=2,
)

from galileo.collaborator import Collaborator, CollaboratorRole  # noqa: E402

__all__ = ["Collaborator", "CollaboratorRole"]
