"""SDK-side Pydantic models for experiment-group responses.

These shadow the API's ExperimentGroupResponse until the Client API OpenAPI spec
includes the experiment-group routes and the generated client provides typed
models. When that happens, this file should be deleted in favor of
``galileo.resources.models.experiment_group_response``.
"""

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class ExperimentGroupDataset(BaseModel):
    """Dataset summary attached to an experiment group."""

    id: UUID
    name: str


class ExperimentGroupUserInfo(BaseModel):
    """Creator info embedded on an experiment group response."""

    id: UUID
    email: str
    first_name: str | None = None
    last_name: str | None = None


class ExperimentGroupResponse(BaseModel):
    """A single experiment group as returned by the API.

    Mirrors ``ExperimentGroupResponse`` in ``api/api/schemas/experiment_group.py``.
    Extra fields are ignored so additive backend changes don't break SDK clients.
    """

    model_config = ConfigDict(extra="ignore")

    id: UUID
    name: str
    project_id: UUID
    created_at: datetime
    updated_at: datetime
    description: str | None = None
    is_system: bool = False
    experiment_count: int = 0
    latest_run_date: datetime | None = None
    datasets: list[ExperimentGroupDataset] = []
    created_by: UUID | None = None
    created_by_user: ExperimentGroupUserInfo | None = None
