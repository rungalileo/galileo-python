"""Base classes for lifecycle and state management."""

from __future__ import annotations

import logging
from abc import ABC, abstractmethod
from enum import Enum

logger = logging.getLogger(__name__)


class SyncState(Enum):
    """
    Enumeration of possible synchronization states for business objects.

    Attributes
    ----------
        LOCAL_ONLY: Object exists only in memory, not yet persisted remotely.
        SYNCED: Local and remote states match.
        DIRTY: Local changes exist that have not been saved.
        FAILED_SYNC: Last attempt to sync failed.
        DELETED: Object was deleted remotely, local object still exists.
    """

    LOCAL_ONLY = "local_only"
    SYNCED = "synced"
    DIRTY = "dirty"
    FAILED_SYNC = "failed_sync"
    DELETED = "deleted"


class StateManagementMixin(ABC):
    """
    Base mixin for business objects providing lifecycle state management.

    This mixin provides state tracking and helper methods for objects that
    need to synchronize between local and remote (API) states.

    Attributes
    ----------
        _sync_state: Current synchronization state of the object.
        _last_error: Last error encountered during synchronization (optional).
    """

    def __init__(self) -> None:
        """Initialize the mixin with default state."""
        self._sync_state: SyncState = SyncState.LOCAL_ONLY
        self._last_error: Exception | None = None

    @property
    def sync_state(self) -> SyncState:
        """
        Get the current synchronization state.

        Returns
        -------
            SyncState: The current state of the object.
        """
        return self._sync_state

    def _set_state(self, state: SyncState, error: Exception | None = None) -> None:
        """
        Set the synchronization state and optionally store an error.

        Args:
            state: The new synchronization state.
            error: Optional exception that caused the state transition.
        """
        old_state = self._sync_state
        self._sync_state = state
        self._last_error = error

        # Log state transitions at DEBUG level
        obj_name = self.__class__.__name__
        obj_id = getattr(self, "id", "unknown")
        obj_name_attr = getattr(self, "name", "unknown")

        if error:
            logger.debug(
                f"{obj_name} state transition: {old_state.value} → {state.value} "
                f"(id={obj_id}, name={obj_name_attr}, error={str(error)[:100]})"
            )
        else:
            logger.debug(
                f"{obj_name} state transition: {old_state.value} → {state.value} (id={obj_id}, name={obj_name_attr})"
            )

    def is_synced(self) -> bool:
        """
        Check if the object is synchronized with the remote state.

        Returns
        -------
            bool: True if the object is synced, False otherwise.
        """
        return self._sync_state == SyncState.SYNCED

    def is_dirty(self) -> bool:
        """
        Check if the object has unsaved local changes.

        Returns
        -------
            bool: True if the object has unsaved changes, False otherwise.
        """
        return self._sync_state == SyncState.DIRTY

    def is_local_only(self) -> bool:
        """
        Check if the object exists only locally.

        Returns
        -------
            bool: True if the object has not been persisted, False otherwise.
        """
        return self._sync_state == SyncState.LOCAL_ONLY

    def has_failed(self) -> bool:
        """
        Check if the last synchronization attempt failed.

        Returns
        -------
            bool: True if the last sync failed, False otherwise.
        """
        return self._sync_state == SyncState.FAILED_SYNC

    def is_deleted(self) -> bool:
        """
        Check if the object has been deleted remotely.

        Returns
        -------
            bool: True if the object was deleted, False otherwise.
        """
        return self._sync_state == SyncState.DELETED

    @abstractmethod
    def refresh(self) -> None:
        """
        Refresh the object state from the remote API.

        This method should:
        1. Fetch the latest state from the API
        2. Update all local attributes
        3. Set the state to SYNCED on success

        Raises
        ------
            NotImplementedError: If not implemented by subclass.
        """
        raise NotImplementedError("Subclasses must implement refresh()")
