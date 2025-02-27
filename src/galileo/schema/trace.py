from typing import Optional

from pydantic import UUID4, BaseModel, Field

from galileo_core.schemas.logging.trace import Trace


class BaseLogStreamOrExperimentModel(BaseModel):
    log_stream_id: Optional[UUID4] = Field(default=None, description="Log stream id associated with the traces.")
    experiment_id: Optional[UUID4] = Field(default=None, description="Experiment id associated with the traces.")


class TracesIngestRequest(BaseLogStreamOrExperimentModel):
    traces: list[Trace] = Field(..., description="List of traces to log.", min_length=1)


class TracesIngestResponse(BaseLogStreamOrExperimentModel):
    project_id: UUID4 = Field(description="Project id associated with the traces.")
    project_name: str = Field(description="Project name associated with the traces.")
    traces_count: int = Field(description="total number of traces ingested")
    records_count: int = Field(description="total number of records (traces & spans) ingested")
