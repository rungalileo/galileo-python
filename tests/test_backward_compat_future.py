"""Tests that all migrated symbols remain importable from galileo.__future__ and resolve to the same objects."""


def test_project_is_same_class():
    from galileo.__future__ import Project as FutureProject
    from galileo.project import Project as RootProject

    assert FutureProject is RootProject


def test_collaborator_is_same_class():
    from galileo.__future__ import Collaborator as FutureCollaborator
    from galileo.collaborator import Collaborator as RootCollaborator

    assert FutureCollaborator is RootCollaborator


def test_collaborator_role_is_same_class():
    from galileo.__future__ import CollaboratorRole as FutureRole
    from galileo.collaborator import CollaboratorRole as RootRole

    assert FutureRole is RootRole


def test_sync_state_is_same_class():
    from galileo.__future__.shared.base import SyncState as FutureSyncState
    from galileo.shared.base import SyncState as RootSyncState

    assert FutureSyncState is RootSyncState


def test_state_management_mixin_is_same_class():
    from galileo.__future__.shared.base import StateManagementMixin as FutureMixin
    from galileo.shared.base import StateManagementMixin as RootMixin

    assert FutureMixin is RootMixin


def test_exceptions_are_same_classes():
    from galileo.__future__.shared.exceptions import APIError as FutureAPIError
    from galileo.__future__.shared.exceptions import ConfigurationError as FutureConfigError
    from galileo.__future__.shared.exceptions import GalileoFutureError as FutureBaseError
    from galileo.__future__.shared.exceptions import IntegrationNotConfiguredError as FutureIntError
    from galileo.__future__.shared.exceptions import ResourceConflictError as FutureConflictError
    from galileo.__future__.shared.exceptions import ResourceNotFoundError as FutureNotFoundError
    from galileo.__future__.shared.exceptions import SyncError as FutureSyncError
    from galileo.__future__.shared.exceptions import ValidationError as FutureValidationError
    from galileo.shared.exceptions import (
        APIError,
        ConfigurationError,
        GalileoFutureError,
        IntegrationNotConfiguredError,
        ResourceConflictError,
        ResourceNotFoundError,
        SyncError,
        ValidationError,
    )

    assert FutureAPIError is APIError
    assert FutureConfigError is ConfigurationError
    assert FutureBaseError is GalileoFutureError
    assert FutureIntError is IntegrationNotConfiguredError
    assert FutureConflictError is ResourceConflictError
    assert FutureNotFoundError is ResourceNotFoundError
    assert FutureSyncError is SyncError
    assert FutureValidationError is ValidationError


def test_root_init_exports():
    """Test that the new exports are available from the galileo package root."""
    from galileo import Collaborator, CollaboratorRole, Project, SyncState

    assert Project is not None
    assert Collaborator is not None
    assert CollaboratorRole is not None
    assert SyncState is not None
