"""Base classes for lifecycle and state management."""

from __future__ import annotations

import logging
from abc import ABC, abstractmethod
from enum import Enum
from typing import Any

logger = logging.getLogger(__name__)

_SENTINEL = object()


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

    Subclasses may declare a ``_TRACKED_FIELDS`` frozenset to enable automatic
    dirty-tracking: any assignment to a tracked field on a SYNCED object will
    transition it to DIRTY so that callers know a ``save()`` is needed.

    Attributes
    ----------
        _sync_state: Current synchronization state of the object.
        _last_error: Last error encountered during synchronization (optional).
        _TRACKED_FIELDS: frozenset of attribute names whose mutations trigger
            SYNCED → DIRTY transitions.
    """

    _TRACKED_FIELDS: frozenset[str] = frozenset()

    def __init__(self) -> None:
        """Initialize the mixin with default state."""
        self._sync_state: SyncState = SyncState.LOCAL_ONLY
        self._last_error: Exception | None = None

    def __setattr__(self, name: str, value: Any) -> None:
        """
        Override attribute setting to auto-transition SYNCED → DIRTY.

        Only attributes listed in ``type(self)._TRACKED_FIELDS`` trigger the
        transition, and only when the incoming value actually differs from the
        current value (same-value assignments are no-ops).

        Parameters
        ----------
            name: Attribute name being set.
            value: New value for the attribute.
        """
        tracked = type(self)._TRACKED_FIELDS
        if name in tracked:
            current = object.__getattribute__(self, name) if hasattr(self, name) else _SENTINEL
            if current is not _SENTINEL and current != value:
                # Only transition from SYNCED; LOCAL_ONLY/DIRTY/etc. are unaffected
                try:
                    sync_state = object.__getattribute__(self, "_sync_state")
                except AttributeError:
                    sync_state = None
                if sync_state == SyncState.SYNCED:
                    object.__setattr__(self, "_sync_state", SyncState.DIRTY)
        object.__setattr__(self, name, value)

    def _sync_attrs(self, **attrs: Any) -> None:
        """
        Bulk-set attributes without triggering dirty-tracking.

        Use this inside ``create()``, ``refresh()``, and ``save()`` to write
        API-sourced values back onto the instance without transitioning state.

        Parameters
        ----------
            **attrs: Keyword arguments mapping attribute names to their new values.
        """
        for key, value in attrs.items():
            object.__setattr__(self, key, value)

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
