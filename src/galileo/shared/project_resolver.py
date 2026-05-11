"""Shared helper for resolving a project from explicit params or env fallbacks.

Lives alongside :func:`galileo.shared.exceptions._project_not_found_error` so the
two helpers — "how to find a project" and "what error to raise when you can't" —
sit in one place and can be reused by every ``__future__`` domain object
(LogStream, Experiment, …) instead of being duplicated per-class.
"""

from __future__ import annotations

from galileo.projects import Project as ProjectRecord
from galileo.projects import ProjectNotFoundError, Projects
from galileo.shared.exceptions import _project_not_found_error
from galileo.utils.env_helpers import _get_project_from_env, _get_project_id_from_env


def _resolve_project(project_id: str | None, project_name: str | None) -> ProjectRecord:
    """Resolve a project from explicit params or env fallbacks.

    Resolution order matches :meth:`galileo.projects.Projects.get_with_env_fallbacks`:
    explicit ``project_id`` > ``GALILEO_PROJECT_ID`` > explicit ``project_name``
    > ``GALILEO_PROJECT``.

    Raises ``NotFoundError`` (specifically the ``ResourceNotFoundError`` subclass for
    backward compat) when no project can be located. Catching either type works.

    The helper pre-checks "no identifier anywhere" so it never relies on the
    ``ValueError`` ``Projects.get(id=None, name=None)`` raises in that one case —
    unrelated ``ValueError``s from the API client surface unchanged.
    """
    # Pre-check before delegating: when no identifier is available anywhere,
    # surface the documented not-found error directly instead of going through
    # the API client (whose only ValueError source for this call is exactly
    # "neither id nor name available", which we already know).
    if not project_id and not project_name and not _get_project_id_from_env() and not _get_project_from_env():
        raise _project_not_found_error(None, None)

    try:
        project_obj = Projects().get_with_env_fallbacks(id=project_id, name=project_name)
    except ProjectNotFoundError:
        project_obj = None
    if not project_obj:
        raise _project_not_found_error(project_id, project_name)
    return project_obj
