from collections import deque
from datetime import datetime
from typing import Optional

from pydantic import UUID4

from galileo.logger.interface import IGalileoLogger
from galileo.logger.utils import get_last_output
from galileo.schema.trace import TracesIngestRequest
from galileo.utils.metrics import populate_local_metrics
from galileo_core.schemas.logging.span import (
    LlmSpan,
    LlmSpanAllowedInputType,
    LlmSpanAllowedOutputType,
    StepWithChildSpans,
    WorkflowSpan,
)
from galileo_core.schemas.logging.step import StepAllowedInputType
from galileo_core.schemas.logging.trace import Trace


class GalileoBatchLogger(IGalileoLogger):
    """
    Galileo Batch logger class implements `IGalileoLogger` interface. It's responsible for
    split batch and streaming logic accordingly inside `GalileoLogger` class. So when you need
    to add new method make sure you change IGalileoLogger class first and both loggers must implement
    this logic, if logic same use directly GalileoLogger class.

    Note: You should not use it directly and must use GalileoLogger instead with mode="batch"
    """

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
    ):
        return self.add_trace(
            input=input,
            name=name,
            duration_ns=duration_ns,
            created_at=created_at,
            user_metadata=metadata,
            tags=tags,
            dataset_input=dataset_input,
            dataset_output=dataset_output,
            dataset_metadata=dataset_metadata,
            external_id=external_id,
        )

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
        return super().add_llm_span(
            input=input,
            output=output,
            model=model,
            tools=tools,
            name=name,
            created_at=created_at,
            duration_ns=duration_ns,
            user_metadata=user_metadata,
            tags=tags,
            num_input_tokens=num_input_tokens,
            num_output_tokens=num_output_tokens,
            total_tokens=total_tokens,
            temperature=temperature,
            status_code=status_code,
            time_to_first_token_ns=time_to_first_token_ns,
            step_number=step_number,
        )

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
    ) -> WorkflowSpan:
        return super().add_workflow_span(
            input=input,
            output=output,
            name=name,
            duration_ns=duration_ns,
            created_at=created_at,
            user_metadata=user_metadata,
            tags=tags,
            step_number=step_number,
        )

    def conclude(
        self,
        output: Optional[str] = None,
        duration_ns: Optional[int] = None,
        status_code: Optional[int] = None,
        conclude_all: bool = False,
    ) -> Optional[StepWithChildSpans]:
        if not conclude_all:
            return super().conclude(output=output, duration_ns=duration_ns, status_code=status_code)

        # TODO: Allow the final span output to propagate to the parent spans
        current_parent = None
        while self.current_parent() is not None:
            current_parent = super().conclude(output=output, duration_ns=duration_ns, status_code=status_code)

        return current_parent

    def flush(self) -> list[Trace]:
        """
        Upload all traces to Galileo.

        Returns:
        -------
            List[Trace]: The list of uploaded traces.
        """
        if not self.traces:
            self._logger.info("No traces to flush.")
            return list()

        current_parent = self.current_parent()
        if current_parent is not None:
            self._logger.info("Concluding the active trace...")
            last_output = get_last_output(current_parent)
            self.conclude(output=last_output, conclude_all=True)

        if self.local_metrics:
            self._logger.info("Computing local metrics...")
            # TODO: parallelize, possibly with ThreadPoolExecutor
            for trace in self.traces:
                populate_local_metrics(trace, self.local_metrics)

        self._logger.info("Flushing %d traces...", len(self.traces))

        traces_ingest_request = TracesIngestRequest(
            traces=self.traces, experiment_id=self.experiment_id, session_id=self.session_id
        )
        self._client.ingest_traces_sync(traces_ingest_request)
        logged_traces = self.traces

        self._logger.info("Successfully flushed %d traces.", len(logged_traces))

        self.traces = list()
        self._parent_stack = deque()
        return logged_traces

    async def async_flush(self) -> list[Trace]:
        if not self.traces:
            self._logger.info("No traces to flush.")
            return list()

        current_parent = self.current_parent()
        if current_parent is not None:
            self._logger.info("Concluding the active trace...")
            last_output = get_last_output(current_parent)
            self.conclude(output=last_output, conclude_all=True)

        if self.local_metrics:
            self._logger.info("Computing metrics for local scorers...")
            # TODO: parallelize, possibly with asyncio to_thread/gather
            for trace in self.traces:
                populate_local_metrics(trace, self.local_metrics)

        self._logger.info("Flushing %d traces...", len(self.traces))

        traces_ingest_request = TracesIngestRequest(traces=self.traces, session_id=self.session_id)
        await self._client.ingest_traces(traces_ingest_request)
        logged_traces = self.traces

        self._logger.info("Successfully flushed %d traces.", len(logged_traces))

        self.traces = list()
        self._parent_stack = deque()
        return logged_traces
