"""Shared helper for resolving a project from explicit params or env fallbacks.

Lives alongside :func:`galileo.shared.exceptions._project_not_found_error` so the
two helpers — "how to find a project" and "what error to raise when you can't" —
sit in one place and can be reused by every ``__future__`` domain object
(LogStream, Experiment, …) instead of being duplicated per-class.
"""

from __future__ import annotations

from galileo.projects import Project as ProjectRecord
from galileo.projects import ProjectNotFoundError, Projects
from galileo.shared.exceptions import _project_not_found_error, _resolve_project_identifiers


def _resolve_project(project_id: str | None, project_name: str | None) -> ProjectRecord:
    """Resolve a project from explicit params or env fallbacks.

    Identifier precedence and whitespace handling are delegated to
    :func:`galileo.shared.exceptions._resolve_project_identifiers`, which matches
    the contract of :meth:`galileo.projects.Projects.get_with_env_fallbacks`.

    Raises ``NotFoundError`` (specifically the ``ResourceNotFoundError`` subclass for
    backward compat) when no project can be located. Catching either type works.

    The helper pre-checks "no identifier anywhere" so it never relies on the
    ``ValueError`` ``Projects.get(id=None, name=None)`` raises in that one case —
    unrelated ``ValueError``s from the API client surface unchanged.
    """
    resolved_id, resolved_name = _resolve_project_identifiers(project_id, project_name)

    if not resolved_id and not resolved_name:
        raise _project_not_found_error(None, None)

    try:
        project_obj = Projects().get_with_env_fallbacks(id=resolved_id, name=resolved_name)
    except ProjectNotFoundError:
        project_obj = None
    if not project_obj:
        raise _project_not_found_error(resolved_id, resolved_name)
    return project_obj
