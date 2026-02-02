from enum import Enum
from typing import Literal, Optional, Union

from pydantic import UUID4, BaseModel, Field

from galileo.resources.models import Document
from galileo_core.schemas.logging.span import Span
from galileo_core.schemas.logging.step import StepAllowedInputType, StepAllowedOutputType
from galileo_core.schemas.logging.trace import Trace

SPAN_TYPE = Literal["llm", "retriever", "tool", "workflow", "agent"]


class LoggingMethod(str, Enum):
    playground = "playground"
    python_client = "python_client"
    typescript_client = "typescript_client"
    api_direct = "api_direct"


class BaseLogStreamOrExperimentModel(BaseModel):
    log_stream_id: Optional[UUID4] = Field(default=None, description="Log stream id associated with the traces.")
    experiment_id: Optional[UUID4] = Field(default=None, description="Experiment id associated with the traces.")


class LogRecordsIngestRequest(BaseLogStreamOrExperimentModel):
    logging_method: LoggingMethod = Field(default=LoggingMethod.api_direct)
    client_version: Union[str, None] = Field(default=None)
    reliable: bool = Field(
        default=False,
        description="Whether or not to use reliable logging.  If set to False, the method will respond immediately before verifying that the traces have been successfully ingested, and no error message will be returned if ingestion fails.  If set to True, the method will wait for the traces to be successfully ingested or return an error message if there is an ingestion failure.",
    )


class TracesIngestRequest(LogRecordsIngestRequest):
    traces: list[Trace] = Field(..., description="List of traces to log.", min_length=1)
    session_id: Optional[UUID4] = Field(default=None, description="Session id associated with the traces.")
    session_external_id: Optional[str] = Field(default=None, description="External id for session grouping.")
    is_complete: Optional[bool] = Field(default=True, description="Is complete.")


class SpansIngestRequest(LogRecordsIngestRequest):
    spans: list[Span] = Field(..., description="List of spans to log.", min_length=1)
    trace_id: UUID4 = Field(description="Trace id associated with the spans.")
    parent_id: UUID4 = Field(description="Parent trace or span id.")


class LogRecordsIngestResponse(BaseLogStreamOrExperimentModel):
    project_id: UUID4 = Field(description="Project id associated with the traces.")
    project_name: str = Field(description="Project name associated with the traces.")
    session_id: UUID4 = Field(description="Session id associated with the traces.")
    records_count: int = Field(description="Total number of records ingested")


class TracesIngestResponse(LogRecordsIngestResponse):
    traces_count: int = Field(description="total number of traces ingested")


class LogTraceUpdateResponse(LogRecordsIngestResponse):
    trace_id: UUID4 = Field(description="Trace id associated with the updated trace.")


class LogSpansIngestResponse(LogRecordsIngestResponse):
    trace_id: UUID4 = Field(description="Trace id associated with the spans.")
    parent_id: UUID4 = Field(description="Parent trace or span id.")


class LogSpanUpdateResponse(LogRecordsIngestResponse):
    span_id: UUID4 = Field(description="Span id associated with the updated span.")


class TraceUpdateRequest(LogRecordsIngestRequest):
    trace_id: UUID4 = Field(..., description="Trace id to update.")
    input: Union[str, None] = Field(
        default=None, description="Input of the trace. Overwrites previous value if present."
    )
    output: Union[str, None] = Field(
        default=None, description="Output of the trace. Overwrites previous value if present."
    )
    status_code: Union[int, None] = Field(
        default=None, description="Status code of the trace. Overwrites previous value if present."
    )
    tags: Union[list[str], None] = Field(default=None, description="Tags to add to the trace.")
    is_complete: Union[bool, None] = Field(
        default=False, description="Whether or not the records in this request are complete."
    )
    duration_ns: Union[int, None] = Field(
        default=None, description="Duration in nanoseconds. Overwrites previous value if present."
    )


class SpanUpdateRequest(LogRecordsIngestRequest):
    span_id: UUID4 = Field(..., description="Span id to update.")
    input: Union[StepAllowedInputType, None] = Field(
        default=None, description="Input of the span. Overwrites previous value if present."
    )
    output: Union[StepAllowedOutputType, None] = Field(
        default=None, description="Output of the span. Overwrites previous value if present."
    )
    tags: Union[list[str], None] = Field(default=None, description="Tags to add to the span.")
    status_code: Union[int, None] = Field(
        default=None, description="Status code of the span. Overwrites previous value if present."
    )
    duration_ns: Union[int, None] = Field(
        default=None, description="Duration in nanoseconds. Overwrites previous value if present."
    )


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


RetrieverSpanAllowedOutputType = Union[
    str, list[str], dict[str, str], list[dict[str, str]], Document, list[Document], None
]
