"""Utility functions for project operations."""

from typing import Optional

from galileo.projects import Projects


def resolve_project_id(
    project_id: Optional[str] = None,
    project_name: Optional[str] = None,
    allow_none: bool = False,
    validate: bool = True,
) -> Optional[str]:
    """
    Resolve project_name to project_id if needed.

    Parameters
    ----------
    project_id : Optional[str], optional
        The project ID. If provided, returns it (optionally validating it exists).
    project_name : Optional[str], optional
        The project name. If provided, looks up and returns the project ID.
    allow_none : bool, optional
        If True, allows both parameters to be None and returns None.
        If False, raises ValueError when both are None. Defaults to False.
    validate : bool, optional
        If True, validates that the project exists. If False, skips validation.
        Defaults to True.

    Returns
    -------
    Optional[str]
        The resolved project ID, or None if neither was provided and allow_none=True.

    Raises
    ------
    ValueError
        If both project_id and project_name are provided,
        or if neither is provided and allow_none=False,
        or if the project doesn't exist (when validate=True).
    """
    if project_id is not None and project_name is not None:
        raise ValueError("Only one of 'project_id' or 'project_name' can be provided, not both")

    if project_name is not None:
        project = Projects().get(name=project_name)
        if not project:
            raise ValueError(f"Project '{project_name}' does not exist")
        return project.id

    if project_id is not None:
        if validate:
            project = Projects().get(id=project_id)
            if not project:
                raise ValueError(f"Project '{project_id}' does not exist")
        return project_id

    if not allow_none:
        raise ValueError("Either project_id or project_name must be provided")

    return None
