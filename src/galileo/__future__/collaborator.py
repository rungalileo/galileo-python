from __future__ import annotations

import logging
from datetime import datetime
from typing import Any

from galileo.projects import Projects

# Re-export CollaboratorRole from the auto-generated models
from galileo.resources.models.collaborator_role import CollaboratorRole

logger = logging.getLogger(__name__)


class Collaborator:
    """
    Immutable representation of a user's collaboration on a project.

    A Collaborator binds a user to a project with a specific role and permissions.
    Collaborators are contextual - the same user can have different roles on
    different projects.

    Collaborator attributes are immutable. To modify the role, use the update()
    method which returns a new Collaborator instance. To remove access, use remove().

    Attributes
    ----------
        id (str): The unique identifier of this collaboration (UserProject ID).
        user_id (str): The ID of the user who has access to the project.
        project_id (str): The ID of the project this collaboration belongs to.
        role (CollaboratorRole): The role assigned to the user (OWNER, EDITOR, VIEWER, ANNOTATOR).
        created_at (datetime): When this collaboration was created.
        email (str | None): The user's email address.
        first_name (str | None): The user's first name.
        last_name (str | None): The user's last name.
        permissions (list | None): Actions the API caller can perform on this collaborator
            record (e.g., "update" or "delete" this collaboration). None indicates no
            permissions data is available (either omitted by the API or explicitly empty).

    Examples
    --------
        # Get collaborators for a project
        project = Project.get(name="My Project")
        collaborators = project.collaborators

        for collab in collaborators:
            print(f"{collab.email} - {collab.role}")

        # Check if a specific user has access
        viewer = next((c for c in collaborators if c.email == "viewer@example.com"), None)
        if viewer:
            print(f"User has {viewer.role} access")

        # Filter by role using the CollaboratorRole enum
        from galileo.__future__ import CollaboratorRole
        editors = [c for c in collaborators if c.role == CollaboratorRole.EDITOR]

        # Update a collaborator's role directly on the object
        updated_collab = collab.update(role=CollaboratorRole.EDITOR)

        # Remove a collaborator
        collab.remove()
    """

    _id: str
    _user_id: str
    _project_id: str
    _role: CollaboratorRole
    _created_at: datetime | None
    _email: str | None
    _first_name: str | None
    _last_name: str | None
    _permissions: list[Any] | None

    def __init__(
        self,
        *,
        id: str,
        user_id: str,
        project_id: str,
        role: CollaboratorRole,
        created_at: datetime | None = None,
        email: str | None = None,
        first_name: str | None = None,
        last_name: str | None = None,
        permissions: list[Any] | None = None,
    ) -> None:
        """
        Initialize a Collaborator instance.

        This constructor is typically called internally by Project methods.
        Users should not create Collaborator instances directly.

        Args:
            id: The collaboration record ID.
            user_id: The user's ID.
            project_id: The project's ID.
            role: The collaboration role (CollaboratorRole enum).
            created_at: When the collaboration was created.
            email: The user's email address.
            first_name: The user's first name.
            last_name: The user's last name.
            permissions: Actions the API caller can perform on this record. None indicates
                no permissions data is available (either omitted or explicitly empty).
        """
        # Use object.__setattr__ to bypass __setattr__ immutability
        object.__setattr__(self, "_id", id)
        object.__setattr__(self, "_user_id", user_id)
        object.__setattr__(self, "_project_id", project_id)
        object.__setattr__(self, "_role", role)
        object.__setattr__(self, "_created_at", created_at)
        object.__setattr__(self, "_email", email)
        object.__setattr__(self, "_first_name", first_name)
        object.__setattr__(self, "_last_name", last_name)
        object.__setattr__(self, "_permissions", permissions)

    @property
    def id(self) -> str:
        """Get the collaboration record ID."""
        return self._id

    @property
    def user_id(self) -> str:
        """Get the user ID."""
        return self._user_id

    @property
    def project_id(self) -> str:
        """Get the project ID."""
        return self._project_id

    @property
    def role(self) -> CollaboratorRole:
        """Get the collaboration role."""
        return self._role

    @property
    def created_at(self) -> datetime | None:
        """Get the creation timestamp."""
        return self._created_at

    @property
    def email(self) -> str | None:
        """Get the user's email address."""
        return self._email

    @property
    def first_name(self) -> str | None:
        """Get the user's first name."""
        return self._first_name

    @property
    def last_name(self) -> str | None:
        """Get the user's last name."""
        return self._last_name

    @property
    def permissions(self) -> list[Any] | None:
        """Get the permissions for this collaboration.

        Returns None if no permissions data is available (either omitted by
        the API or explicitly empty). A non-empty list indicates specific
        actions the API caller can perform on this collaborator record.
        """
        return self._permissions

    def __str__(self) -> str:
        """String representation of the collaborator."""
        return f"Collaborator(email='{self._email}', role={self._role})"

    def __repr__(self) -> str:
        """Detailed string representation of the collaborator."""
        return f"Collaborator(id='{self._id}', user_id='{self._user_id}', email='{self._email}', role={self._role})"

    def __setattr__(self, name: str, value: Any) -> None:
        """
        Prevent modification of collaborator attributes (immutability).

        Raises
        ------
            AttributeError: Always, since collaborators are immutable.
        """
        raise AttributeError(
            f"Collaborator objects are immutable. Cannot set attribute '{name}'. "
            f"Use collab.update(role=...) to change the role."
        )

    def __delattr__(self, name: str) -> None:
        """
        Prevent deletion of collaborator attributes (immutability).

        Raises
        ------
            AttributeError: Always, since collaborators are immutable.
        """
        raise AttributeError(f"Collaborator objects are immutable. Cannot delete attribute '{name}'.")

    def __eq__(self, other: object) -> bool:
        """
        Check equality based on user_id and project_id.

        Args:
            other: Object to compare with.

        Returns
        -------
            bool: True if collaborators represent the same user-project binding.
        """
        if not isinstance(other, Collaborator):
            return False
        return self._user_id == other._user_id and self._project_id == other._project_id

    def __hash__(self) -> int:
        """
        Hash based on user_id and project_id.

        Returns
        -------
            int: Hash value.
        """
        return hash((self._user_id, self._project_id))

    def to_dict(self) -> dict[str, Any]:
        """
        Convert collaborator to dictionary representation.

        Returns
        -------
            dict: Dictionary with collaborator properties.
        """
        return {
            "id": self._id,
            "user_id": self._user_id,
            "project_id": self._project_id,
            "role": self._role.value,  # Convert enum to string value
            "created_at": self._created_at.isoformat() if self._created_at else None,
            "email": self._email,
            "first_name": self._first_name,
            "last_name": self._last_name,
            "permissions": self._permissions,
        }

    def update(self, role: CollaboratorRole) -> Collaborator:
        """
        Update this collaborator's role.

        Creates a new Collaborator instance with the updated role. The original
        instance remains unchanged (immutability is preserved).

        Args:
            role: The new role to assign (CollaboratorRole enum).

        Returns
        -------
            Collaborator: A new Collaborator instance with the updated role.

        Examples
        --------
            # Update a collaborator's role
            collab = project.collaborators[0]
            updated_collab = collab.update(role=CollaboratorRole.EDITOR)
            print(f"New role: {updated_collab.role}")
        """
        logger.info(
            f"Collaborator.update: project_id='{self._project_id}', user_id='{self._user_id}', role='{role}' - started"
        )

        try:
            projects_service = Projects()
            api_collaborator = projects_service.update_user_project_collaborator(
                project_id=self._project_id, user_id=self._user_id, role=role
            )

            updated = Collaborator._from_api_response(api_collaborator, project_id=self._project_id)
            logger.info(f"Collaborator.update: project_id='{self._project_id}', user_id='{self._user_id}' - completed")
            return updated

        except Exception as e:
            logger.error(
                f"Collaborator.update: project_id='{self._project_id}', user_id='{self._user_id}' - failed: {e}"
            )
            raise

    def remove(self) -> None:
        """
        Remove this collaborator from the project.

        Revokes the user's access to the project. After calling this method,
        the collaborator object should no longer be used.

        Examples
        --------
            # Remove a collaborator
            collab = project.collaborators[0]
            collab.remove()
        """
        logger.info(f"Collaborator.remove: project_id='{self._project_id}', user_id='{self._user_id}' - started")

        try:
            projects_service = Projects()
            projects_service.unshare_project_with_user(project_id=self._project_id, user_id=self._user_id)
            logger.info(f"Collaborator.remove: project_id='{self._project_id}', user_id='{self._user_id}' - completed")

        except Exception as e:
            logger.error(
                f"Collaborator.remove: project_id='{self._project_id}', user_id='{self._user_id}' - failed: {e}"
            )
            raise

    @classmethod
    def _from_api_response(cls, response: Any, project_id: str) -> Collaborator:
        """
        Factory method to create a Collaborator from an API response.

        Args:
            response: The UserCollaborator response from the API.
            project_id: The project ID this collaborator belongs to.

        Returns
        -------
            Collaborator: A new Collaborator instance.
        """
        # Handle permissions - convert to list of dicts if present and non-empty.
        # Note: The API model normalizes missing permissions to an empty list, so we cannot
        # distinguish between "field omitted" and "explicitly empty". Both result in None here.
        permissions = None
        if hasattr(response, "permissions") and response.permissions:
            permissions = [
                {"action": p.action, "allowed": p.allowed, "message": p.message} if hasattr(p, "action") else p
                for p in response.permissions
            ]

        # Handle role - it should already be a CollaboratorRole enum from the API
        role = response.role if hasattr(response, "role") else CollaboratorRole.VIEWER
        if isinstance(role, str):
            role = CollaboratorRole(role)

        return cls(
            id=str(response.id),
            user_id=str(response.user_id),
            project_id=project_id,
            role=role,
            created_at=response.created_at if hasattr(response, "created_at") else None,
            email=response.email if hasattr(response, "email") else None,
            first_name=response.first_name if hasattr(response, "first_name") else None,
            last_name=response.last_name if hasattr(response, "last_name") else None,
            permissions=permissions,
        )
