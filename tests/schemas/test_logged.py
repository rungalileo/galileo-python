"""Tests for SDK-local ingestion models (Logged variants and content blocks)."""

import builtins
import importlib

import pytest
from pydantic import ValidationError

import galileo.logger.control as control_module
import galileo.schema.logged as logged_module
from galileo.schema.content_blocks import DataContentBlock, TextContentBlock
from galileo.schema.logged import LoggedAgentSpan, LoggedControlSpan, LoggedLlmSpan, LoggedTrace, LoggedWorkflowSpan
from galileo.schema.message import LoggedMessage
from galileo.schema.trace import TracesIngestRequest
from galileo_core.schemas.logging.llm import MessageRole
from galileo_core.schemas.logging.span import AgentSpan, LlmSpan, RetrieverSpan, ToolSpan, WorkflowSpan
from galileo_core.schemas.logging.trace import Trace
from galileo_core.schemas.shared.document import Document
from galileo_core.schemas.shared.multimodal import ContentModality


class TestTextContentBlock:
    def test_basic_text_block(self) -> None:
        # Given: a plain text string
        block = TextContentBlock(text="hello world")

        # Then: fields are set correctly
        assert block.type == "text"
        assert block.text == "hello world"
        assert block.index is None
        assert block.metadata is None

    def test_text_block_with_metadata(self) -> None:
        # Given: a text block with index and metadata
        block = TextContentBlock(text="chunk", index=0, metadata={"source": "doc1"})

        # Then: all fields are preserved
        assert block.index == 0
        assert block.metadata == {"source": "doc1"}


class TestDataContentBlock:
    def test_base64_source(self) -> None:
        # Given: a data block with base64 content
        block = DataContentBlock(modality=ContentModality.image, mime_type="image/png", base64="iVBORw0KGgoAAAANS")

        # Then: source is base64
        assert block.type == "data"
        assert block.modality == ContentModality.image
        assert block.base64 is not None
        assert block.url is None

    def test_url_source(self) -> None:
        # Given: a data block with URL content
        block = DataContentBlock(modality=ContentModality.image, url="https://example.com/image.png")

        # Then: source is url
        assert block.url == "https://example.com/image.png"
        assert block.base64 is None

    def test_no_source_raises(self) -> None:
        # When/Then: missing all source fields raises
        with pytest.raises(ValidationError, match="Exactly one of"):
            DataContentBlock(modality=ContentModality.image)

    def test_multiple_sources_raises(self) -> None:
        # When/Then: multiple source fields raises
        with pytest.raises(ValidationError, match="Exactly one of"):
            DataContentBlock(modality=ContentModality.image, base64="abc", url="https://example.com/img.png")


class TestTracesIngestRequestBoundary:
    def test_rejects_core_trace(self) -> None:
        # When/Then: a plain core Trace is rejected since TracesIngestRequest expects LoggedTrace
        with pytest.raises(ValidationError, match="Input should be a valid dictionary or instance of LoggedTrace"):
            TracesIngestRequest(traces=[Trace(input="plain text")])


class TestJsonRoundtripNoCoercion:
    """Verify that model_dump(mode='json') → model_validate preserves types, nothing coerced to str."""

    def test_logged_trace_roundtrip(self) -> None:
        # Given: a LoggedTrace with content block input and nested LLM span
        trace = LoggedTrace(
            input=[
                TextContentBlock(text="Analyze this image"),
                DataContentBlock(modality=ContentModality.image, base64="abc"),
            ],
            output="done",
            spans=[
                LoggedLlmSpan(
                    input=[LoggedMessage(content="prompt", role=MessageRole.user)],
                    output=LoggedMessage(content="response", role=MessageRole.assistant),
                )
            ],
        )

        # When: JSON dump
        raw = trace.model_dump(mode="json")

        # Then: serialized structure is correct
        assert isinstance(raw["input"], list)
        assert raw["input"][0]["type"] == "text"
        assert raw["input"][1]["type"] == "data"
        assert raw["output"] == "done"

        # When: validated back
        restored = LoggedTrace.model_validate(raw)

        # Then: restored types are exact, not coerced to string
        assert isinstance(restored.input, list)
        assert type(restored.input[0]) is TextContentBlock
        assert type(restored.input[1]) is DataContentBlock
        assert restored.input[1].base64 == "abc"
        assert isinstance(restored.output, str)
        assert type(restored.spans[0]) is LoggedLlmSpan

    def test_logged_workflow_span_roundtrip(self) -> None:
        # Given: a LoggedWorkflowSpan with message input and child LLM span
        span = LoggedWorkflowSpan(
            input=[LoggedMessage(content="workflow input", role=MessageRole.user)],
            output=LoggedMessage(content="workflow output", role=MessageRole.assistant),
            spans=[
                LoggedLlmSpan(
                    input=[LoggedMessage(content="inner", role=MessageRole.user)],
                    output=LoggedMessage(content="inner out", role=MessageRole.assistant),
                )
            ],
        )

        # When: JSON roundtrip
        raw = span.model_dump(mode="json")
        restored = LoggedWorkflowSpan.model_validate(raw)

        # Then: input stayed as list of messages, not coerced to string
        assert isinstance(restored.input, list)
        assert type(restored.input[0]) is LoggedMessage
        assert restored.input[0].content == "workflow input"
        assert type(restored.output) is LoggedMessage
        assert type(restored.spans[0]) is LoggedLlmSpan

    def test_logged_agent_span_roundtrip(self) -> None:
        # Given: a LoggedAgentSpan with multimodal message input
        span = LoggedAgentSpan(
            input=[
                LoggedMessage(
                    content=[
                        TextContentBlock(text="agent task"),
                        DataContentBlock(modality=ContentModality.document, url="https://example.com/doc.pdf"),
                    ],
                    role=MessageRole.user,
                )
            ],
            output="agent result",
        )

        # When: JSON roundtrip
        raw = span.model_dump(mode="json")
        restored = LoggedAgentSpan.model_validate(raw)

        # Then: multimodal content preserved, not stringified
        assert isinstance(restored.input, list)
        assert type(restored.input[0]) is LoggedMessage
        assert isinstance(restored.input[0].content, list)
        assert type(restored.input[0].content[0]) is TextContentBlock
        assert type(restored.input[0].content[1]) is DataContentBlock
        assert restored.input[0].content[1].url == "https://example.com/doc.pdf"

    def test_logged_llm_span_roundtrip(self) -> None:
        # Given: a LoggedLlmSpan with multimodal input messages
        span = LoggedLlmSpan(
            input=[
                LoggedMessage(
                    content=[
                        TextContentBlock(text="What is this?"),
                        DataContentBlock(modality=ContentModality.image, base64="img_data"),
                    ],
                    role=MessageRole.user,
                )
            ],
            output=LoggedMessage(content="A cat", role=MessageRole.assistant),
        )

        # When: JSON dump
        raw = span.model_dump(mode="json")

        # Then: serialized message content is a list of typed dicts
        assert isinstance(raw["input"][0]["content"], list)
        assert raw["input"][0]["content"][0]["type"] == "text"
        assert raw["input"][0]["content"][1]["type"] == "data"
        assert isinstance(raw["output"]["content"], str)

        # When: validated back
        restored = LoggedLlmSpan.model_validate(raw)

        # Then: input messages preserved with typed content blocks
        assert type(restored.input[0]) is LoggedMessage
        assert isinstance(restored.input[0].content, list)
        assert type(restored.input[0].content[0]) is TextContentBlock
        assert type(restored.input[0].content[1]) is DataContentBlock
        assert restored.input[0].content[1].base64 == "img_data"
        assert type(restored.output) is LoggedMessage
        assert restored.output.content == "A cat"

    def test_logged_trace_content_blocks_output_roundtrip(self) -> None:
        # Given: a LoggedTrace with list[IngestContentBlock] output
        trace = LoggedTrace(
            input="query",
            output=[TextContentBlock(text="result"), DataContentBlock(modality=ContentModality.image, base64="img")],
        )

        # When: JSON roundtrip
        raw = trace.model_dump(mode="json")
        restored = LoggedTrace.model_validate(raw)

        # Then: output is a list of content blocks
        assert isinstance(restored.output, list)
        assert len(restored.output) == 2
        assert type(restored.output[0]) is TextContentBlock
        assert restored.output[0].text == "result"
        assert type(restored.output[1]) is DataContentBlock
        assert restored.output[1].base64 == "img"

    def test_logged_workflow_span_document_output_roundtrip(self) -> None:
        # Given: a LoggedWorkflowSpan with Sequence[Document] output
        span = LoggedWorkflowSpan(input="search query", output=[Document(content="result 1")])

        # When: JSON roundtrip
        raw = span.model_dump(mode="json")
        restored = LoggedWorkflowSpan.model_validate(raw)

        # Then: output preserved as list of Documents
        assert isinstance(restored.output, list)
        assert type(restored.output[0]) is Document

    def test_retriever_span_roundtrip(self) -> None:
        # Given: a trace containing a RetrieverSpan
        trace = LoggedTrace(
            input="find docs",
            spans=[
                RetrieverSpan(
                    input="search query", output=[Document(content="retrieved doc", metadata={"score": "0.95"})]
                )
            ],
        )

        # When: JSON roundtrip
        raw = trace.model_dump(mode="json")
        restored = LoggedTrace.model_validate(raw)

        # Then: RetrieverSpan and its Document output are preserved
        assert type(restored.spans[0]) is RetrieverSpan
        assert restored.spans[0].output[0].content == "retrieved doc"

    def test_tool_span_roundtrip(self) -> None:
        # Given: a trace containing a ToolSpan
        trace = LoggedTrace(input="use tool", spans=[ToolSpan(input="tool_call(arg=1)", output="tool result")])

        # When: JSON roundtrip
        raw = trace.model_dump(mode="json")
        restored = LoggedTrace.model_validate(raw)

        # Then: ToolSpan is preserved
        assert type(restored.spans[0]) is ToolSpan
        assert restored.spans[0].output == "tool result"

    def test_full_ingest_request_roundtrip(self) -> None:
        # Given: a TracesIngestRequest exercising all 5 span types and all output variants
        request = TracesIngestRequest(
            traces=[
                LoggedTrace(
                    input=[TextContentBlock(text="top-level with content blocks")],
                    output="trace string output",
                    spans=[
                        LoggedAgentSpan(
                            input=[LoggedMessage(content="agent task", role=MessageRole.user)],
                            output="agent done",
                            spans=[
                                LoggedWorkflowSpan(
                                    input=[LoggedMessage(content="wf", role=MessageRole.user)],
                                    output=LoggedMessage(content="wf result", role=MessageRole.assistant),
                                    spans=[
                                        LoggedLlmSpan(
                                            input=[
                                                LoggedMessage(
                                                    content=[
                                                        TextContentBlock(text="deep"),
                                                        DataContentBlock(
                                                            modality=ContentModality.audio, base64="audio_b64"
                                                        ),
                                                    ],
                                                    role=MessageRole.user,
                                                )
                                            ],
                                            output=LoggedMessage(content="deep answer", role=MessageRole.assistant),
                                        ),
                                        RetrieverSpan(input="retrieve context", output=[Document(content="ctx doc")]),
                                        ToolSpan(input="calc(2+2)", output="4"),
                                    ],
                                )
                            ],
                        )
                    ],
                )
            ]
        )

        # When: JSON roundtrip
        raw = request.model_dump(mode="json")
        restored = TracesIngestRequest.model_validate(raw)

        # Then: walk the full tree and verify types
        trace = restored.traces[0]
        assert type(trace) is LoggedTrace
        assert isinstance(trace.input, list)
        assert type(trace.input[0]) is TextContentBlock
        assert trace.output == "trace string output"

        agent = trace.spans[0]
        assert type(agent) is LoggedAgentSpan
        assert isinstance(agent.input, list)
        assert type(agent.input[0]) is LoggedMessage

        wf = agent.spans[0]
        assert type(wf) is LoggedWorkflowSpan
        assert type(wf.output) is LoggedMessage

        llm = wf.spans[0]
        assert type(llm) is LoggedLlmSpan
        assert isinstance(llm.input[0].content, list)
        assert type(llm.input[0].content[0]) is TextContentBlock
        assert type(llm.input[0].content[1]) is DataContentBlock
        assert llm.input[0].content[1].base64 == "audio_b64"

        retriever = wf.spans[1]
        assert type(retriever) is RetrieverSpan
        assert retriever.output[0].content == "ctx doc"

        tool = wf.spans[2]
        assert type(tool) is ToolSpan
        assert tool.output == "4"

    def test_logged_trace_roundtrip_with_fallback_control_span(self, monkeypatch: pytest.MonkeyPatch) -> None:
        # Given: galileo.logger.control is reloaded without native ControlSpan support
        original_import = builtins.__import__

        def force_fallback_import(name, globals=None, locals=None, fromlist=(), level=0):
            if name == "galileo_core.schemas.logging.control":
                raise ImportError("forced fallback for test")
            return original_import(name, globals, locals, fromlist, level)

        try:
            with monkeypatch.context() as context:
                context.setattr(builtins, "__import__", force_fallback_import)
                importlib.reload(control_module)
                importlib.reload(logged_module)

                # When: constructing and validating a LoggedTrace containing the fallback ControlSpan payload
                control_payload = control_module.ControlSpan(input="selected text").model_dump(mode="python")
                trace = logged_module.LoggedTrace(input="query", spans=[control_payload])
                restored = logged_module.LoggedTrace.model_validate(trace.model_dump(mode="json"))

                # Then: the discriminated union resolves the fallback ControlSpan cleanly
                assert control_module.HAS_NATIVE_CONTROL_SPAN is False
                assert restored.spans[0].type == "control"
                assert restored.spans[0].__class__.__name__ == "LoggedControlSpan"
                assert restored.spans[0].model_dump(mode="json")["input"] == "selected text"
        finally:
            importlib.reload(control_module)
            importlib.reload(logged_module)

    @pytest.mark.parametrize("field_name", ["id", "session_id", "trace_id", "parent_id"])
    def test_fallback_control_span_rejects_non_uuidish_id_fields(
        self, field_name: str, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        # Given: galileo.logger.control is reloaded without native ControlSpan support
        original_import = builtins.__import__

        def force_fallback_import(name, globals=None, locals=None, fromlist=(), level=0):
            if name == "galileo_core.schemas.logging.control":
                raise ImportError("forced fallback for test")
            return original_import(name, globals, locals, fromlist, level)

        try:
            with monkeypatch.context() as context:
                context.setattr(builtins, "__import__", force_fallback_import)
                importlib.reload(control_module)

                # When/Then: non-UUID-ish id fields are rejected by the fallback schema
                assert control_module.HAS_NATIVE_CONTROL_SPAN is False
                with pytest.raises(ValidationError):
                    control_module.ControlSpan(input="selected text", **{field_name: 123})
        finally:
            importlib.reload(control_module)


class TestLoggedAndCoreParity:
    """Verify Trace/LoggedTrace and Span/LoggedSpan behave identically for plain string content."""

    def test_trace_string_io_parity(self) -> None:
        # Given: the same plain-string fields
        kwargs = dict(input="hello", output="world", name="t")

        # When: constructing both variants
        core = Trace(**kwargs)
        logged = LoggedTrace(**kwargs)

        # Then: field values and serialized output match
        assert core.input == logged.input
        assert core.output == logged.output
        assert core.model_dump(include={"input", "output", "name"}) == logged.model_dump(
            include={"input", "output", "name"}
        )

    def test_workflow_span_string_io_parity(self) -> None:
        kwargs = dict(input="query", output="answer", name="wf")
        core = WorkflowSpan(**kwargs)
        logged = LoggedWorkflowSpan(**kwargs)

        assert core.input == logged.input
        assert core.output == logged.output
        assert core.model_dump(include={"input", "output", "name"}) == logged.model_dump(
            include={"input", "output", "name"}
        )

    def test_agent_span_string_io_parity(self) -> None:
        kwargs = dict(input="task", output="result", name="ag")
        core = AgentSpan(**kwargs)
        logged = LoggedAgentSpan(**kwargs)

        assert core.input == logged.input
        assert core.output == logged.output
        assert core.model_dump(include={"input", "output", "name"}) == logged.model_dump(
            include={"input", "output", "name"}
        )

    def test_llm_span_string_io_parity(self) -> None:
        core = LlmSpan(input="prompt", output="completion", name="llm", model="gpt-4")
        logged = LoggedLlmSpan(input="prompt", output="completion", name="llm", model="gpt-4")

        assert core.input == logged.input
        assert core.output == logged.output
        assert core.model_dump(include={"input", "output", "name", "model"}) == logged.model_dump(
            include={"input", "output", "name", "model"}
        )

    def test_logged_trace_is_instance_of_trace(self) -> None:
        logged = LoggedTrace(input="x")

        assert isinstance(logged, Trace)
        assert isinstance(logged, LoggedTrace)

    def test_logged_spans_are_instances_of_core(self) -> None:
        assert isinstance(LoggedWorkflowSpan(input="x"), WorkflowSpan)
        assert isinstance(LoggedAgentSpan(input="x"), AgentSpan)
        assert isinstance(LoggedLlmSpan(input="x"), LlmSpan)


class TestLoggedTraceTypeRestrictions:
    """Verify LoggedTrace no longer accepts Sequence[LoggedMessage] or LoggedMessage."""

    def test_logged_trace_rejects_message_input(self) -> None:
        # Given: LoggedTrace input is now Union[str, list[IngestContentBlock]]
        messages = [LoggedMessage(content="prompt", role=MessageRole.user)]

        # When/Then: creating a LoggedTrace with messages raises ValidationError
        with pytest.raises(ValidationError):
            LoggedTrace(input=messages)

    def test_logged_trace_rejects_message_output(self) -> None:
        # When/Then: creating a LoggedTrace with a LoggedMessage output raises ValidationError
        with pytest.raises(ValidationError):
            LoggedTrace(input="hello", output=LoggedMessage(content="response", role=MessageRole.assistant))

    def test_logged_trace_rejects_document_output(self) -> None:
        # When/Then: creating a LoggedTrace with Sequence[Document] output raises ValidationError
        with pytest.raises(ValidationError):
            LoggedTrace(input="hello", output=[Document(content="doc")])

    def test_logged_control_span_rejects_non_string_input(self) -> None:
        # When/Then: creating a LoggedControlSpan with non-string input raises ValidationError
        with pytest.raises(ValidationError):
            LoggedControlSpan(input=["selected", "text"])


class TestContentBlocksOnSpans:
    """Verify LoggedWorkflowSpan and LoggedAgentSpan accept list[IngestContentBlock]."""

    def test_workflow_span_with_content_blocks(self) -> None:
        # Given: content blocks as workflow span input/output
        span = LoggedWorkflowSpan(
            input=[TextContentBlock(text="plan"), DataContentBlock(modality=ContentModality.image, base64="img")],
            output=[TextContentBlock(text="result")],
        )

        # Then: content blocks are accepted and preserved
        assert isinstance(span.input, list)
        assert type(span.input[0]) is TextContentBlock
        assert type(span.input[1]) is DataContentBlock

    def test_workflow_span_content_blocks_roundtrip(self) -> None:
        # Given: a workflow span with content blocks
        span = LoggedWorkflowSpan(
            input=[TextContentBlock(text="step 1"), DataContentBlock(modality=ContentModality.audio, base64="aud")],
            output=[TextContentBlock(text="done")],
        )

        # When: JSON roundtrip
        raw = span.model_dump(mode="json")
        restored = LoggedWorkflowSpan.model_validate(raw)

        # Then: content blocks survive
        assert isinstance(restored.input, list)
        assert type(restored.input[0]) is TextContentBlock
        assert type(restored.input[1]) is DataContentBlock
        assert restored.input[1].base64 == "aud"

    def test_agent_span_with_content_blocks(self) -> None:
        # Given: content blocks as agent span input
        span = LoggedAgentSpan(
            input=[
                TextContentBlock(text="task"),
                DataContentBlock(modality=ContentModality.image, url="https://x.com/img.png"),
            ],
            output=[TextContentBlock(text="completed")],
        )

        # Then: content blocks are accepted
        assert isinstance(span.input, list)
        assert type(span.input[0]) is TextContentBlock
        assert type(span.input[1]) is DataContentBlock

    def test_agent_span_content_blocks_roundtrip(self) -> None:
        # Given: an agent span with content blocks
        span = LoggedAgentSpan(
            input=[
                TextContentBlock(text="analyze"),
                DataContentBlock(modality=ContentModality.document, url="https://x.com/doc.pdf"),
            ],
            output="analysis complete",
        )

        # When: JSON roundtrip
        raw = span.model_dump(mode="json")
        restored = LoggedAgentSpan.model_validate(raw)

        # Then: content blocks survive
        assert isinstance(restored.input, list)
        assert type(restored.input[0]) is TextContentBlock
        assert type(restored.input[1]) is DataContentBlock
        assert restored.input[1].url == "https://x.com/doc.pdf"

    def test_workflow_span_accepts_messages(self) -> None:
        # Given: workflow spans still support Sequence[LoggedMessage]
        messages = [LoggedMessage(content="query", role=MessageRole.user)]

        # When: creating a workflow span with messages
        span = LoggedWorkflowSpan(input=messages, output="answer")

        # Then: messages are preserved
        assert isinstance(span.input, list)
        assert type(span.input[0]) is LoggedMessage

    def test_agent_span_accepts_messages(self) -> None:
        # Given: agent spans still support Sequence[LoggedMessage]
        messages = [LoggedMessage(content="task", role=MessageRole.user)]

        # When: creating an agent span with messages
        span = LoggedAgentSpan(input=messages, output="done")

        # Then: messages are preserved
        assert isinstance(span.input, list)
        assert type(span.input[0]) is LoggedMessage
