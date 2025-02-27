# import time
# import traceback
# from collections import defaultdict
# from collections.abc import Sequence
# from datetime import datetime
# from http import HTTPStatus
# from json import loads
# from typing import Any, Optional, Union
# from uuid import UUID

# import pytz
# import tiktoken
# from langchain_core.agents import AgentFinish
# from langchain_core.callbacks import BaseCallbackHandler
# from langchain_core.documents import Document
# from langchain_core.messages import BaseMessage
# from langchain_core.outputs import LLMResult

# from galileo_core.helpers.execution import async_run
# from galileo_core.schemas.shared.workflows.node_type import NodeType
# from galileo_core.schemas.shared.traces.types import Trace, WorkflowSpan

# from galileo.decorator import galileo_context
# # from galileo.logger import GalileoLogger


# class GalileoCallback(BaseCallbackHandler):
#     def __init__(
#         self, project_name: Optional[str] = None, log_stream: Optional[str] = None, *args: Any, **kwargs: Any
#     ) -> None:
#         """LangChain callback handler for Galileo Observe

#         Parameters
#         ----------
#         project_name : str
#             Name of the project to log to
#         version : Optional[str]
#             A version identifier for this system so logs can be attributed
#             to a specific configuration
#         """

#         # if the project and logstream = what's in context, then pick up the current trace (if it exists)
#         # else start a new trace
#         logger = galileo_context.get_logger_instance(project=project_name, log_stream=log_stream)


#         self.records: dict[str, TransactionRecord] = {}
#         self.timers: dict[str, dict[str, float]] = {}
#         self.parent_child_mapping: defaultdict[str, list[str]] = defaultdict(list)
#         super().__init__(*args, **kwargs)

#     def _get_trace(self):
#         if self._trace:
#             return self._trace
#         if (galileo_context.get_current_project() == project_name) and (
#             galileo_context.get_current_log_stream() == log_stream
#         ):
#             _trace = galileo_context.get_current_trace()
#         else:
#             # start a new trace
#             pass

#     def _start_new_span(
#         self, run_id: UUID, parent_run_id: Optional[UUID], node_name: str, serialized: Optional[dict[str, Any]] = None
#     ) -> tuple[str, Optional[str], Optional[str], Optional[str]]:
#         node_id = str(run_id)
#         chain_id = str(parent_run_id) if parent_run_id else None
#         if chain_id:
#             # This check ensures we're actually logging the parent chain
#             if self.records.get(chain_id):
#                 self.records[chain_id].has_children = True
#                 chain_root_id = self.records[chain_id].chain_root_id
#                 self.parent_child_mapping[chain_id].append(node_id)
#             else:
#                 # We're not logging the parent chain, so this is the root
#                 chain_root_id = node_id
#         else:
#             # This node is the root if it doesn't have a parent
#             chain_root_id = node_id
#         # Parse and set the name of the node.
#         node_class_reference = None
#         if serialized is not None and isinstance(serialized, dict):
#             node_name = serialized.get("name") or node_name
#             node_class_reference = serialized.get("id")
#         if node_class_reference and isinstance(node_class_reference, list):
#             node_name = node_class_reference[-1]

#         self.timers[node_id] = {}
#         self.timers[node_id]["start"] = time.perf_counter()

#         return node_id, chain_root_id, chain_id, node_name

#     def _end_span(self, run_id: UUID) -> tuple[str, int]:
#         node_id = str(run_id)

#         self.timers[node_id]["stop"] = time.perf_counter()
#         latency_ms = round((self.timers[node_id]["stop"] - self.timers[node_id]["start"]) * 1000)
#         del self.timers[node_id]

#         return node_id, latency_ms

#     def _finalize_node(self, record: TransactionRecord) -> None:
#         self.records[record.node_id] = record
#         batch_records: list[TransactionRecord] = list()
#         # If this record is closing out a root chain,
#         # then add all records with that chain_root_id to the batch.
#         if record.node_id == record.chain_root_id:
#             for node_id, batch_record in self.records.copy().items():
#                 if batch_record.chain_root_id == record.chain_root_id:
#                     # If the node is a non-chain node,
#                     # or is a parent node with any children, include it.
#                     if batch_record.node_type != NodeType.chain or node_id in self.parent_child_mapping.keys():
#                         batch_records.append(batch_record)
#                     del self.records[node_id]

#             transaction_batch = TransactionRecordBatch(
#                 records=batch_records, logging_method=TransactionLoggingMethod.py_langchain
#             )
#             async_run(self.client.ingest_batch(transaction_batch))

#     def on_llm_start(
#         self,
#         serialized: Optional[dict[str, Any]],
#         prompts: list[str],
#         run_id: UUID,
#         parent_run_id: Optional[UUID] = None,
#         **kwargs: Any,
#     ) -> Any:
#         """Run when LLM starts running."""
#         node_id, chain_root_id, chain_id, node_name = self._start_new_node(
#             run_id, parent_run_id, NodeType.llm, serialized
#         )
#         tags = kwargs.get("tags")
#         metadata = kwargs.get("metadata")
#         invocation_params = kwargs.get("invocation_params", {})
#         model = invocation_params.get("model_name")
#         temperature = invocation_params.get("temperature")
#         self.records[node_id] = TransactionRecord(
#             node_id=node_id,
#             chain_id=chain_id,
#             chain_root_id=chain_root_id,
#             node_name=node_name,
#             input_text=serialize_to_str(prompts),
#             model=model,
#             created_at=datetime.now(tz=pytz.utc).isoformat(),
#             temperature=temperature,
#             tags=tags,
#             user_metadata=metadata,
#             node_type=NodeType.llm,
#             version=self.version,
#         )

#     def on_chat_model_start(
#         self,
#         serialized: Optional[dict[str, Any]],
#         messages: list[list[BaseMessage]],
#         run_id: UUID,
#         parent_run_id: Optional[UUID] = None,
#         **kwargs: Any,
#     ) -> Any:
#         """Run when Chat Model starts running."""
#         node_id, chain_root_id, chain_id, node_name = self._start_new_node(
#             run_id, parent_run_id, NodeType.chat, serialized
#         )
#         tags = kwargs.get("tags")
#         metadata = kwargs.get("metadata")
#         invocation_params = kwargs.get("invocation_params", {})
#         model = invocation_params.get("model", invocation_params.get("_type", "undefined-type"))
#         temperature = invocation_params.get("temperature")
#         tools = invocation_params.get("tools", None)
#         self.records[node_id] = TransactionRecord(
#             node_id=node_id,
#             chain_id=chain_id,
#             chain_root_id=chain_root_id,
#             node_name=node_name,
#             input_text=serialize_to_str(messages),
#             tools=serialize_to_str(tools) if tools else None,
#             model=model,
#             created_at=datetime.now(tz=pytz.utc).isoformat(),
#             temperature=temperature,
#             tags=tags,
#             user_metadata=metadata,
#             node_type=NodeType.chat,
#             version=self.version,
#         )

#     def on_llm_new_token(self, token: str, run_id: UUID, **kwargs: Any) -> Any:
#         """Run when LLM generates a new token."""
#         node_id = str(run_id)
#         model_dict = self.records[node_id].model_dump()
#         if model_dict["time_to_first_token_ms"] is None:
#             root_node_id = model_dict["chain_root_id"]
#             start_time_root = self.timers[root_node_id]["start"]
#             # Calculate time to generate the first token and convert to milliseconds
#             time_to_first_token_ms = (time.perf_counter() - start_time_root) * 1000
#             model_dict.update(time_to_first_token_ms=time_to_first_token_ms)
#             self.records[node_id] = TransactionRecord(**model_dict)

#     def on_llm_end(self, response: LLMResult, run_id: UUID, **kwargs: Any) -> Any:
#         """Run when LLM ends running."""
#         node_id, latency_ms = self._end_node(run_id)

#         output_text = serialize_to_str(response)
#         if response.llm_output:
#             usage = response.llm_output.get("token_usage", response.llm_output.get("usage", {}))
#             num_input_tokens = usage.get("prompt_tokens", usage.get("input_tokens", None))
#             num_output_tokens = usage.get("completion_tokens", usage.get("output_tokens", None))
#             num_total_tokens = usage.get("total_tokens", None)
#         else:
#             try:
#                 # This is because streaming requests don't provide `llm_output`
#                 # This only works for OpenAI models (or "" because typing)
#                 encoding = tiktoken.encoding_for_model(self.records[node_id].model or "")
#                 num_input_tokens = len(encoding.encode(self.records[node_id].input_text))
#                 num_output_tokens = len(encoding.encode(output_text))
#                 num_total_tokens = num_input_tokens + num_output_tokens
#             except KeyError:
#                 num_input_tokens = 0
#                 num_output_tokens = 0
#                 num_total_tokens = 0
#         try:
#             finish_reason = loads(output_text)[0].get("generation_info", {}).get("finish_reason", None)
#         except (IndexError, KeyError):
#             finish_reason = None
#         model_dict = self.records[node_id].model_dump()
#         model_dict.update(
#             output_text=output_text,
#             num_input_tokens=num_input_tokens,
#             num_output_tokens=num_output_tokens,
#             num_total_tokens=num_total_tokens,
#             finish_reason=finish_reason,
#             latency_ms=latency_ms,
#             status_code=HTTPStatus.OK,
#         )

#         self._finalize_node(TransactionRecord(**model_dict))

#     def on_llm_error(self, error: BaseException, run_id: UUID, **kwargs: Any) -> Any:
#         """Run when LLM errors."""
#         node_id, latency_ms = self._end_node(run_id)

#         model_dict = self.records[node_id].model_dump()
#         model_dict.update(
#             output_text=f"ERROR: {error}",
#             num_input_tokens=0,
#             num_output_tokens=0,
#             num_total_tokens=0,
#             latency_ms=latency_ms,
#             status_code=getattr(error, "http_status", HTTPStatus.INTERNAL_SERVER_ERROR),
#         )

#         self._finalize_node(TransactionRecord(**model_dict))

#     def on_chain_start(
#         self,
#         serialized: Optional[dict[str, Any]],
#         inputs: dict[str, Any],
#         run_id: UUID,
#         parent_run_id: Optional[UUID] = None,
#         **kwargs: Any,
#     ) -> Any:
#         """Run when chain starts running."""
#         node_id, chain_root_id, chain_id, node_name = self._start_new_node(
#             run_id, parent_run_id, NodeType.chain, serialized
#         )
#         tags = kwargs.get("tags")
#         metadata = kwargs.get("metadata")
#         node_type = NodeType.chain

#         if kwargs.get("name"):
#             node_name = kwargs["name"]

#         # If the `name` is `LangGraph` or `agent`, set the node type to `agent`.
#         if node_name in ["LangGraph", "agent"]:
#             node_type = NodeType.agent

#         # If the node is tagged with `hidden`, don't log it.
#         if tags and "langsmith:hidden" in tags:
#             return

#         self.records[node_id] = TransactionRecord(
#             node_id=node_id,
#             chain_id=chain_id,
#             chain_root_id=chain_root_id,
#             node_name=node_name,
#             input_text=serialize_to_str(inputs),
#             created_at=datetime.now(tz=pytz.utc).isoformat(),
#             tags=tags,
#             user_metadata=metadata,
#             node_type=node_type,
#             version=self.version,
#         )

#     def on_chain_end(self, outputs: Union[str, dict[str, Any]], run_id: UUID, **kwargs: Any) -> Any:
#         """Run when chain ends running."""
#         # If the node was never started, don't track it.
#         if str(run_id) not in self.records:
#             return
#         node_id, latency_ms = self._end_node(run_id)

#         model_dict = self.records[node_id].model_dump()
#         model_dict.update(
#             output_text=serialize_to_str(outputs),
#             finish_reason="chain_end",
#             latency_ms=latency_ms,
#             status_code=HTTPStatus.OK,
#         )

#         self._finalize_node(TransactionRecord(**model_dict))

#     def on_chain_error(self, error: BaseException, run_id: UUID, **kwargs: Any) -> Any:
#         """Run when chain errors."""
#         # If the node was never started, don't track it.
#         if str(run_id) not in self.records:
#             return
#         node_id, latency_ms = self._end_node(run_id)

#         model_dict = self.records[node_id].model_dump()
#         model_dict.update(
#             output_text=f"ERROR: {error}",
#             latency_ms=latency_ms,
#             status_code=getattr(error, "http_status", HTTPStatus.INTERNAL_SERVER_ERROR),
#         )

#         self._finalize_node(TransactionRecord(**model_dict))

#     def on_agent_finish(self, finish: AgentFinish, *, run_id: UUID, **kwargs: Any) -> Any:
#         """Run on agent end."""
#         # If the node was never started, don't track it.
#         if str(run_id) not in self.records:
#             return
#         node_id = str(run_id)
#         model_dict = self.records[node_id].model_dump()
#         model_dict.update(node_type=NodeType.agent.value)

#         self.records[node_id] = TransactionRecord(**model_dict)

#     def on_tool_start(
#         self,
#         serialized: Optional[dict[str, Any]],
#         input_str: str,
#         *,
#         run_id: UUID,
#         parent_run_id: Optional[UUID] = None,
#         tags: Optional[list[str]] = None,
#         metadata: Optional[dict[str, Any]] = None,
#         **kwargs: Any,
#     ) -> Any:
#         """Run when tool starts running."""
#         node_id, chain_root_id, chain_id, node_name = self._start_new_node(
#             run_id, parent_run_id, NodeType.tool, serialized
#         )
#         tags = kwargs.get("tags")
#         metadata = kwargs.get("metadata")

#         self.records[node_id] = TransactionRecord(
#             node_id=node_id,
#             chain_id=chain_id,
#             chain_root_id=chain_root_id,
#             node_name=node_name,
#             input_text=serialize_to_str(input_str),
#             created_at=datetime.now(tz=pytz.utc).isoformat(),
#             tags=tags,
#             user_metadata=metadata,
#             node_type=NodeType.tool,
#             version=self.version,
#         )

#     def on_tool_end(self, output: Any, *, run_id: UUID, parent_run_id: Optional[UUID] = None, **kwargs: Any) -> Any:
#         """Run when the tool ends running.

#         Args:
#             output (Any): The output of the tool.
#             run_id (UUID): The run ID. This is the ID of the current run.
#             kwargs (Any): Additional keyword arguments.
#         """
#         node_id, latency_ms = self._end_node(run_id)

#         model_dict = self.records[node_id].model_dump()
#         model_dict.update(output_text=serialize_to_str(output), latency_ms=latency_ms, status_code=HTTPStatus.OK)

#         self._finalize_node(TransactionRecord(**model_dict))

#     def on_tool_error(self, error: BaseException, *, run_id: UUID, **kwargs: Any) -> Any:
#         """Run when tool errors."""
#         node_id, latency_ms = self._end_node(run_id)

#         error_text = repr(error)
#         if isinstance(error, BaseException):
#             error_text += "\n" + "".join(traceback.format_exception(type(error), error, error.__traceback__))

#         model_dict = self.records[node_id].model_dump()
#         model_dict.update(
#             output_text=f"ERROR: {error_text}",
#             latency_ms=latency_ms,
#             status_code=getattr(error, "http_status", HTTPStatus.INTERNAL_SERVER_ERROR),
#         )

#         record = TransactionRecord(**model_dict)
#         self._finalize_node(record)

#     def on_retriever_start(
#         self,
#         serialized: Optional[dict[str, Any]],
#         query: str,
#         *,
#         run_id: UUID,
#         parent_run_id: Optional[UUID] = None,
#         tags: Optional[list[str]] = None,
#         metadata: Optional[dict[str, Any]] = None,
#         **kwargs: Any,
#     ) -> None:
#         """Run on retriever start."""
#         node_id, chain_root_id, chain_id, node_name = self._start_new_node(
#             run_id, parent_run_id, NodeType.retriever, serialized
#         )

#         self.records[node_id] = TransactionRecord(
#             node_id=node_id,
#             chain_id=chain_id,
#             chain_root_id=chain_root_id,
#             node_name=node_name,
#             input_text=serialize_to_str(query),
#             created_at=datetime.now(tz=pytz.utc).isoformat(),
#             tags=tags,
#             user_metadata=metadata,
#             node_type=NodeType.retriever,
#             version=self.version,
#         )

#     def on_retriever_end(self, documents: Sequence[Document], *, run_id: UUID, **kwargs: Any) -> None:
#         """Run on retriever end."""
#         node_id, latency_ms = self._end_node(run_id)
#         model_dict = self.records[node_id].model_dump()
#         model_dict.update(
#             output_text=serialize_to_str(documents),
#             finish_reason="retriever_end",
#             latency_ms=latency_ms,
#             status_code=HTTPStatus.OK,
#         )
#         record = TransactionRecord(**model_dict)
#         self._finalize_node(record)

#     def on_retriever_error(self, error: BaseException, *, run_id: UUID, **kwargs: Any) -> None:
#         """Run on retriever error."""
#         node_id, latency_ms = self._end_node(run_id)
#         model_dict = self.records[node_id].model_dump()
#         model_dict.update(
#             output_text=f"ERROR: {str(error)}",
#             latency_ms=latency_ms,
#             status_code=getattr(error, "http_status", HTTPStatus.INTERNAL_SERVER_ERROR),
#         )
