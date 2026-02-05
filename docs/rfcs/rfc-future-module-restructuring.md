# RFC: `__future__` Module Restructuring

| Field       | Value                                      |
|-------------|--------------------------------------------|
| **Status**  | Draft                                      |
| **Created** | 2026-02-05                                 |
| **Package** | `galileo` (PyPI)                           |
| **Scope**   | Internal restructuring, public import paths |

---

## Summary

Restructure the `galileo.__future__` subpackage so that the new object-centric API (Project, Dataset, Experiment, etc.) is importable directly from the `galileo` namespace, eliminating the awkward `__future__` submodule name while preserving backward compatibility.

---

## Motivation

### The naming problem

`galileo.__future__` was chosen as a temporary home for the next-generation object-centric API. The name has two problems:

1. **Conceptual clash with Python's `from __future__ import annotations`** — developers encountering `from galileo.__future__ import Project` may assume it is a language-level future import, not a subpackage.
2. **Temporary by design** — the `__future__` name signals "not ready yet," which is inappropriate for a stable, public API surface.

### Current state

- **Root `__init__.py`** exports 45 items (decorators, logger, spans, exceptions). It does **not** export `Project`, `Dataset`, or any of the new domain classes.
- **`__future__/__init__.py`** exports 23 items (`Project`, `Dataset`, `Experiment`, `Prompt`, `LogStream`, `Configuration`, metrics, exceptions, etc.).
- Legacy service modules (`projects.py`, `datasets.py`, etc.) contain thin helper classes and functions that are only used internally; they are **not** exported from the root.
- No singular files (`project.py`, `dataset.py`, etc.) exist at the package root today.

### Goals

1. **Both legacy and new APIs coexist** in the same package without conflict.
2. **No awkward submodule name** — `__future__`, `v2`, `sdk`, etc.
3. **Permanent import path** — no future migration needed.
4. **Natural, Pythonic imports** — `from galileo import Project` should Just Work.

---

## Options Considered

### Option A: Rename submodule (`galileo.v2` / `galileo.sdk`)

```python
from galileo.v2 import Project, Dataset
```

**Pros:**
- Minimal mechanical change (rename directory + find-replace).
- Clear separation from legacy.

**Cons:**
- Version in import path is an anti-pattern (`v2` implies `v3`).
- `sdk` is redundant (the package IS the SDK).
- Still a submodule — not the cleanest import.
- If ever promoted to root, the `v2` path becomes legacy itself (violates goal 3).

**Verdict:** Rejected. Trades one temporary name for another.

### Option B: Move to root as singular files

```python
from galileo.project import Project
from galileo import Project  # via re-export in __init__.py
```

**Pros:**
- Most Pythonic — singular = class, plural = service is a well-known convention (Django, SQLAlchemy, Stripe SDK).
- `from galileo import Project` is the cleanest possible import.
- Permanent path — no reason to ever change.
- No submodule indirection.

**Cons:**
- `project.py` next to `projects.py` — visual similarity in file listings.
- Root directory grows from ~22 to ~33 `.py` files.
- Larger diff (move files + update imports).

**Verdict:** Recommended. See [Recommendation](#recommendation) below.

### Option C: Re-export from root only (keep `__future__` as private `_future`)

```python
from galileo import Project, Dataset
```

**Pros:**
- Cleanest user-facing import.
- Least disruptive to internal layout.

**Cons:**
- Users who need deeper imports (`ColumnCollection`, `QueryResult`, `Sort`) must import from private `_future.shared`.
- Doesn't clean up the physical layout — just papers over it.
- Submodule-level imports don't work: `from galileo.project import Project` would fail.

**Verdict:** Rejected. Half-measure that creates a confusing private/public split.

### Option D: Namespace the legacy instead

```python
from galileo import Project           # new API gets prime namespace
from galileo._legacy.datasets import create_dataset  # legacy moves
```

**Pros:**
- New API gets the clean namespace.
- Clean long-term.

**Cons:**
- Breaks ALL existing legacy users immediately.
- Premature — `__future__` API still has known issues (see [Known Issues](#known-issues)).

**Verdict:** Rejected. Breaking change without sufficient justification today.

---

## Recommendation

**Option B — Move to root as singular files.**

This is the only option that satisfies all four goals without tradeoffs.

| Goal | How Option B satisfies it |
|------|--------------------------|
| Both APIs coexist | `project.py` (new class) alongside `projects.py` (legacy service) |
| No awkward name | No submodule at all — classes live at `galileo.project`, `galileo.dataset` |
| Permanent path | `from galileo import Project` and `from galileo.project import Project` are both final |
| Pythonic | Singular/plural convention is established across Django, SQLAlchemy, Flask, Stripe SDK |

### Addressing the `project.py` / `projects.py` adjacency concern

This is the most common objection. But it is actually a **feature, not a bug** — the naming convention communicates intent:

- `galileo.project` → "I want the Project object"
- `galileo.projects` → "I want project service functions"

This mirrors Django (`model.py` vs `models.py`), and developers intuitively understand singular = one thing, plural = collection/service.

### Resulting user-facing imports

```python
# New object-centric API (recommended)
from galileo import Project, Dataset, Experiment, Prompt, LogStream
from galileo import Configuration, Metric, LlmMetric

# Module-level import also works
from galileo.project import Project
from galileo.dataset import Dataset

# Legacy service API (unchanged, still works)
from galileo.projects import create_project
from galileo.datasets import create_dataset, get_dataset
from galileo.experiments import run_experiment
```

---

## Design

### Package layout after restructuring

```
src/galileo/
├── __init__.py              # Updated: adds re-exports for domain classes
├── _internal/               # NEW: shared utilities (moved from __future__/shared/)
│   ├── __init__.py
│   ├── base.py              # StateManagementMixin, SyncState
│   ├── column.py            # Column, ColumnCollection
│   ├── exceptions.py        # GalileoError, APIError, ConfigurationError, etc.
│   ├── experiment_result.py # ExperimentRunResult, ExperimentPhaseInfo
│   ├── filter.py            # TextFilter, NumberFilter, DateFilter, BooleanFilter
│   ├── query_result.py      # QueryResult
│   ├── sort.py              # Sort
│   └── utils.py             # classproperty
│
├── project.py               # NEW: Project domain object (moved from __future__/)
├── dataset.py               # NEW: Dataset domain object
├── experiment.py            # NEW: Experiment domain object
├── prompt.py                # NEW: Prompt domain object
├── log_stream.py            # NEW: LogStream domain object
├── metric.py                # NEW: Metric classes
├── configuration.py         # NEW: Configuration management
├── integration.py           # NEW: Integration domain object
├── collaborator.py          # NEW: Collaborator domain object
├── model.py                 # NEW: Model domain object
├── provider.py              # NEW: Provider domain object
│
├── __future__/              # KEPT: re-exports from new locations (for internal scripts)
│   └── __init__.py          # Re-exports only, no deprecation warning
│
├── projects.py              # UNCHANGED: legacy service functions
├── datasets.py              # UNCHANGED: legacy service functions
├── experiments.py           # UNCHANGED: legacy service functions
├── prompts.py               # UNCHANGED: legacy service functions
├── log_streams.py           # UNCHANGED: legacy service functions
│
├── config.py                # UNCHANGED
├── decorator.py             # MINOR EDIT: update lazy import path
├── exceptions.py            # UNCHANGED
├── logger/                  # UNCHANGED
├── handlers/                # UNCHANGED
├── openai/                  # UNCHANGED
├── resources/               # UNCHANGED (auto-generated)
├── schema/                  # UNCHANGED
├── utils/                   # MINOR EDIT: update import path in validations.py
└── ...                      # Other existing modules unchanged
```

### Exception naming

As part of this move, rename `GalileoFutureError` to `GalileoError`:

```python
# Before (in __future__/shared/exceptions.py)
class GalileoFutureError(Exception): ...

# After (in _internal/exceptions.py)
class GalileoError(Exception): ...
GalileoFutureError = GalileoError  # backward-compat alias
```

The `Future` qualifier no longer makes sense once the classes are promoted out of `__future__`.

---

## Implementation Plan

The implementation is split into seven phases that can each be committed independently. Each phase leaves the codebase in a working state.

### Phase 1: Move `shared/` to `_internal/`

Move `src/galileo/__future__/shared/` to `src/galileo/_internal/`.

**Files to move:**

| Source | Destination |
|--------|-------------|
| `__future__/shared/base.py` | `_internal/base.py` |
| `__future__/shared/column.py` | `_internal/column.py` |
| `__future__/shared/exceptions.py` | `_internal/exceptions.py` |
| `__future__/shared/experiment_result.py` | `_internal/experiment_result.py` |
| `__future__/shared/filter.py` | `_internal/filter.py` |
| `__future__/shared/query_result.py` | `_internal/query_result.py` |
| `__future__/shared/sort.py` | `_internal/sort.py` |
| `__future__/shared/utils.py` | `_internal/utils.py` |

**Additional changes:**
- Rename `GalileoFutureError` → `GalileoError` in `_internal/exceptions.py` (keep alias for backward compat).
- Update all internal imports: `galileo.__future__.shared.X` → `galileo._internal.X`.
- Make `__future__/shared/__init__.py` re-export from `_internal` for backward compat.

### Phase 2: Move domain modules to root

Move each domain module from `__future__/` to the package root with singular filenames.

| Source | Destination | Notes |
|--------|-------------|-------|
| `__future__/project.py` | `project.py` | |
| `__future__/dataset.py` | `dataset.py` | |
| `__future__/experiment.py` | `experiment.py` | |
| `__future__/prompt.py` | `prompt.py` | |
| `__future__/log_stream.py` | `log_stream.py` | |
| `__future__/metric.py` | `metric.py` | |
| `__future__/configuration.py` | `configuration.py` | |
| `__future__/integration.py` | `integration.py` | |
| `__future__/collaborator.py` | `collaborator.py` | |
| `__future__/model.py` | `model.py` | |
| `__future__/provider.py` | `provider.py` | |

`__future__/types.py` is **not moved** — it contains only `MetricSpec` (a type alias), which is inlined into `metric.py` during the move. The file is deleted.

**Additional changes:**
- Inline `MetricSpec` type alias from `__future__/types.py` into `metric.py` and delete `types.py`.
- Update all internal imports within the moved files: `galileo.__future__.X` → `galileo.X`.

### Phase 3: Update root `__init__.py`

Add re-exports so top-level imports work:

```python
# Domain objects (new object-centric API)
from galileo.project import Project
from galileo.dataset import Dataset
from galileo.experiment import Experiment
from galileo.prompt import Prompt
from galileo.log_stream import LogStream
from galileo.configuration import Configuration
from galileo.integration import Integration
from galileo.collaborator import Collaborator, CollaboratorRole
from galileo.model import Model
from galileo.metric import Metric, LlmMetric, CodeMetric, GalileoMetric, LocalMetric
from galileo._internal.exceptions import (
    GalileoError,
    APIError,
    ConfigurationError,
    ResourceConflictError,
    ResourceNotFoundError,
    ValidationError,
)
```

All additions appended to `__all__`.

### Phase 4: Rewrite `__future__` as re-export shim

Since `__future__` was never published, there are no external users to deprecate. However, internal scripts and notebooks may already reference it. Rewrite `src/galileo/__future__/__init__.py` to re-export from the new locations (no deprecation warning needed):

```python
"""Re-exports for internal backward compatibility.

The __future__ package was never published. New code should import
directly from galileo: `from galileo import Project, Dataset, ...`
"""

from galileo.project import Project
from galileo.dataset import Dataset
from galileo.experiment import Experiment
from galileo.prompt import Prompt
from galileo.log_stream import LogStream
from galileo.configuration import Configuration
from galileo.collaborator import Collaborator, CollaboratorRole
from galileo.integration import Integration
from galileo.model import Model
from galileo.metric import CodeMetric, GalileoMetric, LlmMetric, LocalMetric, Metric
from galileo._internal.exceptions import (
    APIError,
    ConfigurationError,
    GalileoError as GalileoFutureError,
    ResourceConflictError,
    ResourceNotFoundError,
    ValidationError,
)
from galileo.schema.message import Message
from galileo.search import RecordType
from galileo.utils.log_config import enable_console_logging
from galileo_core.schemas.logging.llm import MessageRole
from galileo_core.schemas.logging.step import StepType

__all__ = [
    "APIError",
    "CodeMetric",
    "Collaborator",
    "CollaboratorRole",
    "Configuration",
    "ConfigurationError",
    "Dataset",
    "Experiment",
    "GalileoFutureError",
    "GalileoMetric",
    "Integration",
    "LlmMetric",
    "LocalMetric",
    "LogStream",
    "Message",
    "MessageRole",
    "Metric",
    "Model",
    "Project",
    "Prompt",
    "RecordType",
    "ResourceConflictError",
    "ResourceNotFoundError",
    "StepType",
    "ValidationError",
    "enable_console_logging",
]
```

The `GalileoFutureError` name is preserved via alias for any internal scripts that reference it. The shim can be removed entirely once internal usage is confirmed migrated.

### Phase 5: Update internal references

Specific files that import from `__future__` outside of the `__future__` package itself:

| File | Change |
|------|--------|
| `src/galileo/decorator.py` (line ~630) | Lazy import of `ConfigurationError` → `galileo._internal.exceptions` |
| `src/galileo/utils/validations.py` | Import of `ValidationError` → `galileo._internal.exceptions` |
| `scripts/create_docs.py` | Update ignore list for new file locations |

### Phase 6: Update tests

- Rename `tests/future/` → `tests/test_domain/` (or similar).
- Update all import paths in test files (~15 files) from `galileo.__future__.*` to `galileo.*`.
- Verify `__future__` re-export shim still works (no deprecation warning, just re-exports).

### Phase 7: Update documentation

- Update `CLAUDE.md` and `AGENTS.md` import examples and package structure diagrams.
- Update README with new API import examples.
- Remove references to `__future__` as the primary import path.

### Phase 8: Deprecate legacy service modules and functions

Mark all legacy service modules and their public functions/classes as deprecated. They will continue to work, but IDEs (via `typing_extensions.deprecated` / `warnings.deprecated`) will show strikethrough or warnings to nudge users toward the new API.

**Mechanism:** Use `typing_extensions.deprecated` (Python 3.13+ has `warnings.deprecated`; for older versions use the `typing_extensions` backport). This decorator is recognized by type checkers (mypy, pyright) and IDEs (VS Code, PyCharm), which display the deprecation inline without requiring runtime execution.

```python
from typing_extensions import deprecated

@deprecated("Use `from galileo import create_project` or `Project(...).create()` instead.")
def create_project(name: str, ...) -> ...:
    ...
```

For deprecated classes, apply `@deprecated` to the class:

```python
@deprecated("Use `from galileo import Dataset` instead of `galileo.datasets.Dataset`.")
class Dataset:
    ...
```

For modules that are entirely deprecated, add a module-level docstring indicating deprecation and a `__deprecated__` marker that documentation generators can pick up:

```python
"""
.. deprecated::
    This module is deprecated. Use :mod:`galileo.project` and :class:`galileo.Project` instead.
"""
__deprecated__ = True
```

**Modules and functions to deprecate:**

| Module | Public functions | Public classes | Replacement |
|--------|-----------------|----------------|-------------|
| `projects.py` | `get_project`, `list_projects`, `create_project`, `delete_project`, `share_project_with_user`, `unshare_project_with_user`, `list_user_project_collaborators`, `update_user_project_collaborator` | `Project`, `Projects` | `galileo.project.Project` |
| `datasets.py` | `get_dataset`, `list_datasets`, `create_dataset`, `delete_dataset`, `get_dataset_version_history`, `get_dataset_version`, `extend_dataset`, `list_dataset_projects`, `convert_dataset_row_to_record` | `Dataset`, `Datasets` | `galileo.dataset.Dataset` |
| `experiments.py` | `run_experiment`, `create_experiment`, `get_experiment`, `get_experiments`, `process_row` | `Experiments` | `galileo.experiment.Experiment` |
| `prompts.py` | `get_prompt`, `delete_prompt`, `update_prompt`, `create_prompt`, `get_prompts`, `render_template`, `create_prompt_template`\*, `list_prompt_templates`\*, `get_prompt_template`\* | `PromptTemplate`, `PromptTemplateVersion`, `GlobalPromptTemplates`, `PromptTemplates`\* | `galileo.prompt.Prompt` |
| `log_streams.py` | `get_log_stream`, `list_log_streams`, `create_log_stream`, `enable_metrics` | `LogStream`, `LogStreams` | `galileo.log_stream.LogStream` |

\* Already deprecated — update their deprecation messages to point to the new locations.

Exception classes in these modules (`ProjectsAPIException`, `DatasetAPIException`, `PromptTemplateAPIException`) should also be deprecated in favor of the unified exceptions in `galileo._internal.exceptions`.

**Documentation generation:** The `@deprecated` decorator from `typing_extensions` sets a `__deprecated__` attribute on the decorated object. Documentation generators (Sphinx via `autodoc`, mkdocstrings, etc.) should be configured to render deprecated items with a visible marker (e.g., strikethrough, badge, or admonition). For Sphinx, the built-in `.. deprecated::` directive in the docstring is sufficient. For mkdocstrings, the `__deprecated__` attribute can be detected in templates. The `scripts/create_docs.py` script should be updated to:
1. Detect `__deprecated__` on functions/classes.
2. Render a "Deprecated" badge or admonition in the generated reference docs.
3. Include the deprecation message (which contains the replacement guidance).

**IDE behavior after this phase:**
- **VS Code (Pylance/pyright):** Shows deprecated symbols with ~~strikethrough~~ in autocomplete and on hover.
- **PyCharm:** Shows deprecated symbols with ~~strikethrough~~ and a "deprecated" gutter icon.
- **mypy:** Reports usage of deprecated symbols as warnings (with `--warn-deprecated`, or via plugin).

---

## Migration Guide

Since `galileo.__future__` was never published to PyPI, there are no external users to migrate. The new public API surface is:

```python
from galileo import Project, Dataset, Experiment, Prompt, LogStream
from galileo import Configuration, Metric, LlmMetric
from galileo import GalileoError
```

The `__future__` re-export shim is retained temporarily for internal scripts and notebooks that may already use `from galileo.__future__ import ...`. These will continue to work without warnings. The shim can be removed once internal usage is confirmed migrated.

### Exception rename

| Old name | New name | Notes |
|----------|----------|-------|
| `GalileoFutureError` | `GalileoError` | Alias preserved in `__future__` shim |

All other exception names (`APIError`, `ConfigurationError`, `ResourceConflictError`, `ResourceNotFoundError`, `ValidationError`) are unchanged.

---

## Files Changed

### Moved (source → destination)

| Source | Destination | Count |
|--------|-------------|-------|
| `src/galileo/__future__/shared/*.py` | `src/galileo/_internal/*.py` | 8 files |
| `src/galileo/__future__/*.py` | `src/galileo/*.py` | 11 files (types.py inlined into metric.py and deleted) |

### Edited

| File | Change |
|------|--------|
| `src/galileo/__init__.py` | Add re-exports for domain classes |
| `src/galileo/__future__/__init__.py` | Rewrite as re-export shim |
| `src/galileo/decorator.py` | Update lazy import path |
| `src/galileo/utils/validations.py` | Update import path |
| `scripts/create_docs.py` | Update ignore list |
| All moved files | Update internal import paths |
| `tests/future/*` (~15 files) | Update import paths |
| `CLAUDE.md`, `AGENTS.md` | Update documentation |
| `src/galileo/projects.py` | Add `@deprecated` to all public functions and classes |
| `src/galileo/datasets.py` | Add `@deprecated` to all public functions and classes |
| `src/galileo/experiments.py` | Add `@deprecated` to all public functions and classes |
| `src/galileo/prompts.py` | Add `@deprecated` (update existing deprecations to point to new locations) |
| `src/galileo/log_streams.py` | Add `@deprecated` to all public functions and classes |
| `scripts/create_docs.py` | Detect `__deprecated__` attribute and render deprecation badges |

### Unchanged

| Files | Reason |
|-------|--------|
| `src/galileo/handlers/*` | No `__future__` references |
| `src/galileo/resources/*` | Auto-generated — never edit manually |
| `src/galileo/logger/*` | No `__future__` references |
| `src/galileo/openai/*` | No `__future__` references |

---

## Verification Checklist

1. **All existing tests pass**: `poetry run pytest` — ensures no regressions.
2. **New imports work**: `from galileo import Project, Dataset, Experiment` resolves correctly.
3. **Module-level imports work**: `from galileo.project import Project` resolves correctly.
4. **Legacy imports unchanged**: `from galileo.projects import create_project` still works.
5. **Internal compat shim**: `from galileo.__future__ import Project` still works (re-export, no warning).
6. **Type checking**: `inv type-check` passes.
7. **Linting**: `poetry run ruff check src/` passes.
8. **Legacy deprecation visible in IDE**: Importing `from galileo.projects import create_project` shows strikethrough in VS Code/PyCharm.
9. **Deprecation in docs**: Generated reference docs show a "Deprecated" marker on legacy functions/classes.

---

## Known Issues

These existing issues in the `__future__` API are **not** addressed by this RFC. They remain as-is and should be tackled separately:

1. **`galileo-core` dependency** — The SDK still depends on `galileo-core` for shared schemas. Ongoing work to reduce this dependency is tracked separately.
2. **Configuration state management** — `connect()` must be called explicitly; lazy initialization is incomplete.
3. **Prompt version management** — `Prompt.create_version()` creates a new prompt (with timestamp suffix), not a true version.
4. **Dataset version indexing** — API uses 1-based version indexing.
5. **Experiment-Playground conflation** — The `Experiment` class conflates two distinct API concepts.

---

## Risks

| Risk | Mitigation |
|------|------------|
| Internal scripts using `galileo.__future__` break | Re-export shim keeps old imports working; `__future__` was never published so no external users affected |
| `project.py` / `projects.py` confusion in file listings | Naming convention is well-established (Django, SQLAlchemy); documented in CLAUDE.md |
| Large diff increases review burden | Phased implementation — each phase is a reviewable, independently-valid commit |
| Type checker struggles with re-exports | Explicit `__all__` lists in all modules; verify with `inv type-check` |
| Circular imports from root re-exports | Domain modules don't import from root `__init__.py`; verified in Phase 3 |
| Legacy deprecation warnings are noisy at runtime | `typing_extensions.deprecated` is primarily a static analysis tool — it does emit `DeprecationWarning` at runtime, but only when the function is called, not on import; this is standard Python behavior |
| `typing_extensions` not available | Already a transitive dependency via pydantic; add explicit dependency if not present |

---

## Timeline

| Phase | Estimated Effort | Dependency |
|-------|-----------------|------------|
| Phase 1: Move `shared/` to `_internal/` | Small | None |
| Phase 2: Move domain modules to root | Medium | Phase 1 |
| Phase 3: Update root `__init__.py` | Small | Phase 2 |
| Phase 4: Backward-compat shim | Small | Phase 2 |
| Phase 5: Update internal references | Small | Phase 2 |
| Phase 6: Update tests | Medium | Phases 1–5 |
| Phase 7: Update documentation | Small | Phases 1–5 |
| Phase 8: Deprecate legacy modules | Medium | Phase 2 (new classes must exist at new paths) |

Phases 3, 4, 5, and 8 can be done in parallel after Phase 2 completes.

---

## Alternatives Not Pursued

- **Keeping `__future__` indefinitely**: Rejected because the name actively confuses users and signals instability.
- **Creating a separate package (`galileo-sdk`)**: Rejected because it fragments the ecosystem and complicates dependency management.
- **Using `__init__.py`-only re-exports without moving files**: This is Option C above — rejected because it prevents module-level imports and doesn't clean up the physical layout.
