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


def _normalize(value: str | None) -> str | None:
    """Strip and return ``None`` for empty/whitespace-only inputs.

    Mirrors the trimming :meth:`galileo.projects.Projects.get` does internally,
    so the pre-check below sees the same "effectively empty" value the API
    client would see.
    """
    if value is None:
        return None
    stripped = value.strip()
    return stripped or None


def _resolve_project(project_id: str | None, project_name: str | None) -> ProjectRecord:
    """Resolve a project from explicit params or env fallbacks.

    Resolution order matches :meth:`galileo.projects.Projects.get_with_env_fallbacks`:
    explicit ``project_id`` > ``GALILEO_PROJECT_ID`` > explicit ``project_name``
    > ``GALILEO_PROJECT``.

    Raises ``NotFoundError`` (specifically the ``ResourceNotFoundError`` subclass for
    backward compat) when no project can be located. Catching either type works.

    The helper pre-checks "no identifier anywhere" so it never relies on the
    ``ValueError`` ``Projects.get(id=None, name=None)`` raises in that one case —
    unrelated ``ValueError``s from the API client surface unchanged. Inputs are
    trimmed before the pre-check so whitespace-only values follow the same
    not-found path as missing values instead of leaking a client ``ValueError``.
    """
    # Normalize before the pre-check so whitespace-only values (e.g. ``" "``)
    # are treated as missing — otherwise ``Projects.get`` strips them and raises
    # the unrelated "Exactly one of 'id' or 'name'" ValueError downstream.
    normalized_id = _normalize(project_id) or _normalize(_get_project_id_from_env())
    normalized_name = None if normalized_id else (_normalize(project_name) or _normalize(_get_project_from_env()))

    if not normalized_id and not normalized_name:
        raise _project_not_found_error(None, None)

    try:
        project_obj = Projects().get_with_env_fallbacks(id=normalized_id, name=normalized_name)
    except ProjectNotFoundError:
        project_obj = None
    if not project_obj:
        raise _project_not_found_error(normalized_id, normalized_name)
    return project_obj
