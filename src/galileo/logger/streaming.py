import logging
import uuid
from datetime import datetime
from typing import Optional

from pydantic import UUID4

from galileo.logger.interface import IGalileoLogger
from galileo.schema.trace import SpansIngestRequest, TracesIngestRequest
from galileo_core.schemas.logging.agent import AgentType
from galileo_core.schemas.logging.span import (
    AgentSpan,
    LlmMetrics,
    LlmSpan,
    LlmSpanAllowedInputType,
    LlmSpanAllowedOutputType,
    StepWithChildSpans,
    ToolSpan,
    WorkflowSpan,
)
from galileo_core.schemas.logging.step import Metrics, StepAllowedInputType
from galileo_core.schemas.logging.trace import Trace
from galileo_core.schemas.shared.document import Document

_logger = logging.getLogger(__name__)


class GalileoStreamingLogger(IGalileoLogger):
    """
    Galileo Streaming logger class implements `IGalileoLogger` interface.

    Note: You should not instantiate this class directly but use GalileoLogger instead with mode="streaming".
    """

    # def __init__(self):
    #     super().__init__()

    def start_trace(
        self,
        input: StepAllowedInputType,
        name: Optional[str] = None,
        duration_ns: Optional[int] = None,
        created_at: Optional[datetime] = None,
        metadata: Optional[dict[str, str]] = None,
        tags: Optional[list[str]] = None,
        dataset_input: Optional[str] = None,
        dataset_output: Optional[str] = None,
        dataset_metadata: Optional[dict[str, str]] = None,
        external_id: Optional[str] = None,
    ) -> Trace:
        """
        In Streaming mode, this will the following endpoint with a single trace:
        POST /projects/{project_id}/traces

        Args:
            input:
            name:
            duration_ns:
            created_at:
            metadata:
            tags:
            dataset_input:
            dataset_output:
            dataset_metadata:
            external_id:

        Returns:
            Trace
        """
        trace = Trace(
            input=input,
            name=name,
            created_at=created_at,
            user_metadata=metadata,
            tags=tags,
            metrics=Metrics(duration_ns=duration_ns),
            dataset_input=dataset_input,
            dataset_output=dataset_output,
            dataset_metadata=dataset_metadata if dataset_metadata is not None else {},
            external_id=external_id,
            id=str(uuid.uuid4()),
        )
        traces_ingest_request = TracesIngestRequest(
            traces=[trace], experiment_id=self.experiment_id, session_id=self.session_id
        )
        # TODO: use non-blockign wrapper
        self._client.ingest_traces_sync(traces_ingest_request)

        _logger.info("Successfully flushed trace %s.", trace.id)

        return trace

    def add_llm_span(
        self,
        input: LlmSpanAllowedInputType,
        output: LlmSpanAllowedOutputType,
        model: Optional[str],
        tools: Optional[list[dict]] = None,
        name: Optional[str] = None,
        created_at: Optional[datetime] = None,
        duration_ns: Optional[int] = None,
        user_metadata: Optional[dict[str, str]] = None,
        tags: Optional[list[str]] = None,
        num_input_tokens: Optional[int] = None,
        num_output_tokens: Optional[int] = None,
        total_tokens: Optional[int] = None,
        temperature: Optional[float] = None,
        status_code: Optional[int] = None,
        time_to_first_token_ns: Optional[int] = None,
        id: Optional[UUID4] = None,
        step_number: Optional[int] = None,
    ) -> LlmSpan:
        """
        In Streaming mode, this will the following endpoint with a single span:
        POST /projects/{project_id}/spans

        Args:
            input:
            output:
            model:
            tools:
            name:
            created_at:
            duration_ns:
            user_metadata:
            tags:
            num_input_tokens:
            num_output_tokens:
            total_tokens:
            temperature:
            status_code:
            time_to_first_token_ns:
            id:

        Returns:
            LlmSpan
        """
        span = LlmSpan(
            input=input,
            output=output,
            name=name,
            created_at=created_at,
            user_metadata=user_metadata,
            tags=tags,
            metrics=LlmMetrics(
                duration_ns=duration_ns,
                num_input_tokens=num_input_tokens,
                num_output_tokens=num_output_tokens,
                num_total_tokens=total_tokens,
                time_to_first_token_ns=time_to_first_token_ns,
            ),
            tools=tools,
            model=model,
            temperature=temperature,
            status_code=status_code,
            id=id,
        )
        span_ingest_request = SpansIngestRequest(trace_id=self.trace_id, spans=[span])
        self._client.ingest_spans_sync(span_ingest_request)
        return span

    def add_agent_span(
        self,
        input: str,
        output: Optional[str] = None,
        name: Optional[str] = None,
        duration_ns: Optional[int] = None,
        created_at: Optional[datetime] = None,
        user_metadata: Optional[dict[str, str]] = None,
        tags: Optional[list[str]] = None,
        agent_type: Optional[AgentType] = None,
        step_number: Optional[int] = None,
    ) -> AgentSpan:
        pass

    def add_retriever_span(
        self,
        input: str,
        documents: list[Document],
        name: Optional[str] = None,
        duration_ns: Optional[int] = None,
        created_at: Optional[datetime] = None,
        user_metadata: Optional[dict[str, str]] = None,
        tags: Optional[list[str]] = None,
        status_code: Optional[int] = None,
        step_number: Optional[int] = None,
    ): ...

    def add_tool_span(
        self,
        input: str,
        output: Optional[str] = None,
        name: Optional[str] = None,
        duration_ns: Optional[int] = None,
        created_at: Optional[datetime] = None,
        user_metadata: Optional[dict[str, str]] = None,
        tags: Optional[list[str]] = None,
        status_code: Optional[int] = None,
        tool_call_id: Optional[str] = None,
        step_number: Optional[int] = None,
    ) -> ToolSpan:
        pass

    def add_workflow_span(
        self,
        input: str,
        output: Optional[str] = None,
        name: Optional[str] = None,
        duration_ns: Optional[int] = None,
        created_at: Optional[datetime] = None,
        user_metadata: Optional[dict[str, str]] = None,
        tags: Optional[list[str]] = None,
        step_number: Optional[int] = None,
    ) -> WorkflowSpan: ...

    def conclude(
        self,
        output: Optional[str] = None,
        duration_ns: Optional[int] = None,
        status_code: Optional[int] = None,
        conclude_all: bool = False,
    ) -> Optional[StepWithChildSpans]:
        """
        In Streaming mode, this will do the following:
        If the current parent is a Workflow span, this will call the following endpoint:
            PATCH /projects/{project_id}/spans/{span_id}
        If the current parent is a Trace, this will call the following endpoint:
            PATCH /projects/{project_id}/traces/{trace_id}
        Args:
            output:
            duration_ns:
            status_code:
            conclude_all:

        Returns:
        """
        if self.current_parent():
            ...

    def flush(self) -> list[Trace]: ...

    async def async_flush(self) -> list[Trace]: ...
