from enum import Enum
from typing import Optional

from pydantic import UUID4, BaseModel, Field

from galileo_core.schemas.logging.trace import Trace


class BaseLogStreamOrExperimentModel(BaseModel):
    log_stream_id: Optional[UUID4] = Field(default=None, description="Log stream id associated with the traces.")
    experiment_id: Optional[UUID4] = Field(default=None, description="Experiment id associated with the traces.")


class TracesIngestRequest(BaseLogStreamOrExperimentModel):
    traces: list[Trace] = Field(..., description="List of traces to log.", min_length=1)
    session_id: Optional[UUID4] = Field(default=None, description="Session id associated with the traces.")


class TracesIngestResponse(BaseLogStreamOrExperimentModel):
    project_id: UUID4 = Field(description="Project id associated with the traces.")
    project_name: str = Field(description="Project name associated with the traces.")
    traces_count: int = Field(description="total number of traces ingested")
    records_count: int = Field(description="total number of records (traces & spans) ingested")


class SessionCreateRequest(BaseLogStreamOrExperimentModel):
    name: Optional[str] = Field(default=None, description="Name of the session.")
    previous_session_id: Optional[UUID4] = Field(default=None, description="Previous session id.")
    external_id: Optional[str] = Field(default=None, description="External id of the session.")


class SessionCreateResponse(BaseLogStreamOrExperimentModel):
    id: UUID4 = Field(description="Id of the session.")
    name: Optional[str] = Field(default=None, description="Name of the session.")
    previous_session_id: Optional[UUID4] = Field(default=None, description="Previous session id.")
    external_id: Optional[str] = Field(default=None, description="External id of the session.")
    project_id: UUID4 = Field(description="Project id associated with the session.")
    project_name: str = Field(description="Project name associated with the session.")
    log_stream_id: Optional[UUID4] = Field(default=None, description="Log stream id associated with the session.")


class LogRecordsSearchFilterOperator(str, Enum):
    eq = "eq"
    ne = "ne"
    contains = "contains"
    one_of = "one_of"
    not_in = "not_in"
    gt = "gt"
    gte = "gte"
    lt = "lt"
    lte = "lte"
    between = "between"


class LogRecordsSearchFilterType(str, Enum):
    id = "id"
    date = "date"
    number = "number"
    boolean = "boolean"
    text = "text"


class LogRecordsSearchFilter(BaseModel):
    type: LogRecordsSearchFilterType = Field(description="Type of the log records filter.")
    name: str = Field(description="ID of the column to filter.", alias="column_id")
    value: str = Field(description="Value to filter by.")
    operator: LogRecordsSearchFilterOperator = Field(description="Operator to apply to the filter.")


class LogRecordsSearchRequest(BaseLogStreamOrExperimentModel):
    filters: Optional[list[LogRecordsSearchFilter]] = Field(default=None, description="Filters to apply to the search.")
